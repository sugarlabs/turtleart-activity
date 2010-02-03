#Copyright (c) 2007, Playful Invention Company
#Copyright (c) 2008-9, Walter Bender
#Copyright (c) 2009, Raul Gutierrez Segales

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import logging
_logger = logging.getLogger('turtleart-activity')

import sugar
from sugar.activity import activity
try: # 0.86 toolbar widgets
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarBox
    from sugar.graphics.toolbarbox import ToolbarButton
except ImportError:
    pass
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore

import telepathy
from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject
from sugar.presence import presenceservice
from sugar.presence.tubeconn import TubeConnection

from sugar import profile
from gettext import gettext as _
import locale
import os.path
import subprocess
import tarfile
import sys

from taconstants import *
from taexporthtml import save_html
from taexportlogo import save_logo
from tautils import data_to_file, data_to_string, data_from_string
from tawindow import TurtleArtWindow

SERVICE = 'org.laptop.TurtleArtActivity'
IFACE = SERVICE
PATH = '/org/laptop/TurtleArtActivity'

class TurtleArtActivity(activity.Activity):

    def __init__(self, handle):
        super(TurtleArtActivity,self).__init__(handle)

        datapath = self._get_datapath()
        
        self._setup_visibility_handler()

        self._setup_toolbar()

        canvas = self._setup_scrolled_window()

        lang = self._check_ver_lang_change(datapath)

        self._setup_canvas(canvas, lang)

        self._load_python_code()

        self._setup_sharing()


    """ Activity toolbar callbacks """

    def _do_save_as_html_cb(self, button):
        # write html out to datastore
        self.save_as_html.set_icon("htmlon")
        _logger.debug("saving html code")
        # until we expose the option to choose, always embed images
        embed_flag = True

        # grab code from stacks
        html = save_html(self,self.tw,embed_flag)
        if len(html) == 0:
            return

        # save the html code to the instance directory
        datapath = os.path.join(activity.get_activity_root(), "instance")

        html_file = os.path.join(datapath, "portfolio.html")
        f = file(html_file, "w")
        f.write(html)
        f.close()

        if embed_flag == False:
        # need to make a tarball that includes the images
            tar_path = os.path.join(datapath, 'portfolio.tar')
            tar_fd = tarfile.open(tar_path, 'w')
            try:
                tar_fd.add(html_file, "portfolio.html")
                import glob
                image_list = glob.glob(os.path.join(datapath, 'image*'))
                for i in image_list:
                    tar_fd.add(i, os.path.basename(i))
            finally:
                tar_fd.close()

        # Create a datastore object
        dsobject = datastore.create()

        # Write any metadata (here we specifically set the title of the file
        # and specify that this is a plain text file). 
        dsobject.metadata['title'] = self.metadata['title'] + " " + \
                                     _("presentation")
        dsobject.metadata['icon-color'] = profile.get_color().to_string()
        if embed_flag == True:
            dsobject.metadata['mime_type'] = 'text/html'
            dsobject.set_file_path(html_file)
        else:
            dsobject.metadata['mime_type'] = 'application/x-tar'
            dsobject.set_file_path(tar_path)

        dsobject.metadata['activity'] = 'org.laptop.WebActivity'
        datastore.write(dsobject)
        dsobject.destroy()
        gobject.timeout_add(250,self.save_as_html.set_icon, "htmloff")
        return

    def _do_save_as_logo_cb(self, button):
        # write logo code out to datastore
        self.save_as_logo.set_icon("logo-saveon")
        # grab code from stacks
        logocode = save_logo(self,self.tw)
        if len(logocode) == 0:
            return
        filename = "logosession.lg"

        # Create a datastore object
        dsobject = datastore.create()

        # Write any metadata (here we specifically set the title of the file
        # and specify that this is a plain text file). 
        dsobject.metadata['title'] = self.metadata['title'] + ".lg"
        dsobject.metadata['mime_type'] = 'text/plain'
        dsobject.metadata['icon-color'] = profile.get_color().to_string()

        # save the html code to the instance directory
        datapath = os.path.join(activity.get_activity_root(), "instance")

        # Write the file to the data directory of this activity's root. 
        file_path = os.path.join(datapath, filename)
        f = open(file_path, 'w')
        try:
            f.write(logocode)
        finally:
            f.close()

        # Set the file_path in the datastore.
        dsobject.set_file_path(file_path)

        datastore.write(dsobject)
        gobject.timeout_add(250,self.save_as_logo.set_icon, "logo-saveoff")
        return

    def _do_load_ta_project_cb(self, button):
        from sugar.graphics.objectchooser import ObjectChooser
        chooser = ObjectChooser(_("Project"), None, gtk.DIALOG_MODAL | \
            gtk.DIALOG_DESTROY_WITH_PARENT)
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                dsobject = chooser.get_selected_object()
                try:
                    _logger.debug("opening %s " % dsobject.file_path)
                    self.read_file(dsobject.file_path, False)
                except:
                    _logger.debug("couldn't open %s" % dsobject.file_path)
                dsobject.destroy()
        finally:
            chooser.destroy()
            del chooser
        return 

    def _do_load_python_cb(self, button):
        self.load_python.set_icon("pippy-openon")
        self.import_py()
        gobject.timeout_add(250,self.load_python.set_icon, "pippy-openoff")
        return

    # Import Python code from the Journal to load into "myblock"
    def import_py(self):
        from sugar.graphics.objectchooser import ObjectChooser
        chooser = ObjectChooser('Python code', None, gtk.DIALOG_MODAL | \
            gtk.DIALOG_DESTROY_WITH_PARENT)
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                dsobject = chooser.get_selected_object()
                self._load_python(dsobject)
        finally:
            chooser.destroy()
            del chooser

    def _load_python(self,dsobject):
        try:
            _logger.debug("opening %s " % dsobject.file_path)
            FILE = open(dsobject.file_path, "r")
            self.tw.myblock = FILE.read()
            FILE.close()
            self.tw.set_userdefined()
            # save reference to Pythin code in the project metadata
            self.metadata['python code'] = dsobject.object_id
        except:
            _logger.debug("couldn't open %s" % dsobject.file_path)
        dsobject.destroy()

    def _do_save_as_image_cb(self, button):
        self.save_as_image.set_icon("image-saveon")
        _logger.debug("saving image to journal")

        filename = "ta.png"
        # save the image to the instance directory
        datapath = os.path.join(activity.get_activity_root(), "instance")

        # Write the file to the instance directory of this activity's root. 
        file_path = os.path.join(datapath, filename)
        save_picture(self.tw.canvas, file_path)

        # Create a datastore object
        dsobject = datastore.create()

        # Write metadata
        dsobject.metadata['title'] = self.metadata['title'] + " " + _("image")
        dsobject.metadata['icon-color'] = profile.get_color().to_string()
        dsobject.metadata['mime_type'] = 'image/png'
        dsobject.set_file_path(file_path)

        datastore.write(dsobject)
        dsobject.destroy()
        gobject.timeout_add(250,self.save_as_image.set_icon, "image-saveoff")
        return

    """ Save snapshot """
    def _do_keep_cb(self, button):
        # Create a datastore object
        # save the current state of the project to the instance directory

        # work-around Rainbow which doesn't seem to like tempfile.mkstemp
        try:
            tmppath = os.path.join(activity.get_activity_root(), "instance")
        except:
            # Early versions of Sugar (e.g., 656) didn't support
            # get_activity_root()
            tmppath = os.path.join( \
                os.environ['HOME'], \
                ".sugar/default/org.laptop.TurtleArtActivity/instance")

        tafile = os.path.join(tmppath,"tmpfile.ta")
        print tafile
        try:
            data_to_file(self.tw.assemble_data_to_save(), tafile)
        except:
            _logger.debug("couldn't save snapshot to journal")

        # Create a datastore object
        dsobject = datastore.create()

        # Write any metadata
        dsobject.metadata['title'] = self.metadata['title'] + " " + \
                                     _("snapshot")
        dsobject.metadata['icon-color'] = profile.get_color().to_string()
        dsobject.metadata['mime_type'] = 'application/x-turtle-art'
        dsobject.metadata['activity'] = 'org.laptop.TurtleArtActivity'
        dsobject.set_file_path(tafile)
        datastore.write(dsobject)

        # Clean up
        dsobject.destroy()
        os.remove(tafile)
        return

    """ Main toolbar button callbacks """
    """ Show/hide palette """
    def _do_palette_cb(self, button):
        if self.tw.palette == True:
            self.tw.hideshow_palette(False)
            self.palette_button.set_icon("blockson")
            self.palette_button.set_tooltip(_('Show palette'))
        else:
            self.tw.hideshow_palette(True)
            self.palette_button.set_icon("blocksoff")
            self.palette_button.set_tooltip(_('Hide palette'))

    """ These methods are called both from buttons and blocks """
    def do_hidepalette(self):
        # print "in do_hidepalette"
        self.palette_button.set_icon("blockson")
        self.palette_button.set_tooltip(_('Show palette'))

    def do_showpalette(self):
        # print "in do_showpalette"
        self.palette_button.set_icon("blocksoff")
        self.palette_button.set_tooltip(_('Hide palette'))

    def _do_hideshow_cb(self, button):
        self.tw.hideshow_button()
        if self.tw.hide == True: # we just hid the blocks
            self.blocks_button.set_icon("hideshowon")
            self.blocks_button.set_tooltip(_('Show blocks'))
        else:
            self.blocks_button.set_icon("hideshowoff")
            self.blocks_button.set_tooltip(_('Hide blocks'))
        # update palette buttons too
        if self.tw.palette == False: 
            self.palette_button.set_icon("blockson")
            self.palette_button.set_tooltip(_('Show palette'))
        else:
            self.palette_button.set_icon("blocksoff")
            self.palette_button.set_tooltip(_('Hide palette'))

    def do_hide(self):
        self.blocks_button.set_icon("hideshowon")
        self.blocks_button.set_tooltip(_('Show blocks'))
        self.palette_button.set_icon("blockson")
        self.palette_button.set_tooltip(_('Show palette'))

    def do_show(self):
        self.blocks_button.set_icon("hideshowoff")
        self.blocks_button.set_tooltip(_('Hide blocks'))
        self.palette_button.set_icon("blocksoff")
        self.palette_button.set_tooltip(_('Hide palette'))

    def _do_eraser_cb(self, button):
        self.eraser_button.set_icon("eraseroff")
        self.recenter()
        self.tw.eraser_button()
        gobject.timeout_add(250,self.eraser_button.set_icon,"eraseron")

    def _do_run_cb(self, button):
        self.run_button.set_icon("run-faston")
        self.stop_button.set_icon("stopiton")
        self.tw.lc.trace = 0
        self.tw.run_button(0)
        gobject.timeout_add(1000,self.run_button.set_icon,"run-fastoff")

    def _do_step_cb(self, button):
        self.step_button.set_icon("run-slowon")
        self.stop_button.set_icon("stopiton")
        self.tw.lc.trace = 0
        self.tw.run_button(3)
        gobject.timeout_add(1000,self.step_button.set_icon,"run-slowoff")

    def _do_debug_cb(self, button):
        self.debug_button.set_icon("debugon")
        self.stop_button.set_icon("stopiton")
        self.tw.lc.trace = 1
        self.tw.run_button(6)
        gobject.timeout_add(1000,self.debug_button.set_icon,"debugoff")

    def _do_stop_cb(self, button):
        self.stop_button.set_icon("stopitoff")
        self.tw.stop_button()
        self.step_button.set_icon("run-slowoff")
        self.run_button.set_icon("run-fastoff")

    """ Sample projects open dialog """
    def _do_samples_cb(self, button):
        # FIXME: encapsulation!
        self.tw.load_file(True)
        # run the activity
        self.stop_button.set_icon("stopiton")
        self.tw.run_button(0)

    """
    Recenter scrolled window around canvas
    """
    def recenter(self):
        hadj = self.sw.get_hadjustment()
        # print hadj
        hadj.set_value(0)
        self.sw.set_hadjustment(hadj)
        vadj = self.sw.get_vadjustment()
        # print vadj
        vadj.set_value(0)
        self.sw.set_vadjustment(vadj)

    def _do_fullscreen_cb(self, button):    
        self.fullscreen()
        self.recenter()

    """
    Display coordinate grids
    """
    def _do_cartesian_cb(self, button):
        if self.tw.cartesian is True:
            self.tw.overlay_shapes['Cartesian'].hide()
            self.tw.cartesian = False
        else:
            self.tw.overlay_shapes['Cartesian'].set_layer(OVERLAY_LAYER)
            self.tw.cartesian = True

    def _do_polar_cb(self, button):
        if self.tw.polar is True:
            self.tw.overlay_shapes['polar'].hide()
            self.tw.polar = False
        else:
            self.tw.overlay_shapes['polar'].set_layer(OVERLAY_LAYER)
            self.tw.polar = True

    """
    Rescale coordinate system to 100 == height/2 or 100 == 100 pixels (default)
    """
    def _do_rescale_cb(self, button):
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height/200
            self.rescale_button.set_icon("contract-coordinates")
            self.rescale_button.set_tooltip(_('Rescale coordinates down'))
            self.tw.eraser_button()
        else:
            self.tw.coord_scale = 1
            self.rescale_button.set_icon("expand-coordinates")
            self.rescale_button.set_tooltip(_('Rescale coordinates up'))
            self.tw.eraser_button()

    """
    Either set up initial share...
    """
    def _shared_cb(self, activity):
        if self._shared_activity is None:
            _logger.error("Failed to share or join activity ... \
                _shared_activity is null in _shared_cb()")
            return

        self.initiating = True
        self.waiting_for_blocks = False
        _logger.debug('I am sharing...')

        self.conn = self._shared_activity.telepathy_conn
        self.tubes_chan = self._shared_activity.telepathy_tubes_chan
        self.text_chan = self._shared_activity.telepathy_text_chan
        
        # call back for "NewTube" signal
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal \
            ('NewTube', self._new_tube_cb)

        _logger.debug('This is my activity: making a tube...')
        id = self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferDBusTube(
            SERVICE, {})

    """
    ...or join an exisiting share.
    """
    def _joined_cb(self, activity):
        if self._shared_activity is None:
            _logger.error("Failed to share or join activity ... \
                _shared_activity is null in _shared_cb()")
            return

        self.initiating = False
        _logger.debug('I joined a shared activity.')

        self.conn = self._shared_activity.telepathy_conn
        self.tubes_chan = self._shared_activity.telepathy_tubes_chan
        self.text_chan = self._shared_activity.telepathy_text_chan
        
        # call back for "NewTube" signal
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal( \
            'NewTube', self._new_tube_cb)

        _logger.debug('I am joining an activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb, 
            error_handler=self._list_tubes_error_cb)

        # joiner should request current state from sharer
        self.waiting_for_blocks = True

    def _list_tubes_reply_cb(self, tubes):
        for tube_info in tubes:
            self._new_tube_cb(*tube_info)

    def _list_tubes_error_cb(self, e):
        _logger.error('ListTubes() failed: %s', e)

    """
    Create a new tube
    """
    def _new_tube_cb(self, id, initiator, type, service, params, state):
        _logger.debug('New tube: ID=%d initator=%d type=%d service=%s '
                     'params=%r state=%d', id, initiator, type, service, 
                     params, state)

        if (type == telepathy.TUBE_TYPE_DBUS and service == SERVICE):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[ \
                              telepathy.CHANNEL_TYPE_TUBES].AcceptDBusTube(id)

            tube_conn = TubeConnection(self.conn, 
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES], id, \
                group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])

            # we'll use a chat tube to send serialized stacks back and forth
            self.chattube = ChatTube(tube_conn, self.initiating, \
                self.event_received_cb)

            # now that we have the tube, we can ask for an initialization
            if self.waiting_for_blocks is True:
                self._send_event("i")

    """
    Handle the receiving of events in share
    Events are sent as a tuple
        cmd:data
    where cmd is a mouse or keyboard event and data are x,y coordinates
    or a keysroke
    """
    def event_received_cb(self, text):
        # maybe we can use a stack to share events to new-comers?
        # self._share += "text + "\n"
        if text[0] == 'p': # button press
            e,x,y,mask = text.split(":")
            # _logger.debug("receiving button press: "+x+" "+y+" "+mask)
            if mask == 'T':
                self.tw.button_press(True,int(x),int(y),False)
            else:
                self.tw.button_press(False,int(x),int(y),False)
        elif text[0] == 'r': # block release
            e,x,y = text.split(":")
            # _logger.debug("receiving button release: " + x + " " + y)
            self.tw.button_release(int(x),int(y),False)
        elif text[0] == 'm': # mouse move
            e,x,y = text.split(":")
            _logger.debug("receiving move: " + x + " " + y)
            self.tw.mouse_move(0,0,False,int(x),int(y))
        elif text[0] == 'k': # typing
            e,mask,keyname = text.split(":",3)
            # _logger.debug("recieving key press: " + mask + " " + keyname)
            if mask == 'T':
                self.tw.key_press(True,keyname,False)
            else:
                self.tw.key_press(False,keyname,False)
        elif text[0] == 'i': # request for current state
            # sharer should send current state to joiner
            if self.initiating is True:
                _logger.debug("serialize the project and send to joiner")
                text = data_to_string(self.tw.assemble_data_to_save(True, True))
                self._send_event("I:" + text)
                self.tw.show_palette()
        elif text[0] == 'I': # receiving current state
            if self.waiting_for_blocks:
                _logger.debug("receiving project from sharer")
                e,text = text.split(":",2)
                if len(text) > 0:
                    self.tw.new_project()
                    self.tw.process_data(data_from_string(text))
                # all caught up
                self.waiting_for_blocks = False

    """
    Send event through the tube
    """
    def _send_event(self, entry):
        # nick = profile.get_nick_name()
        # nick = nick.upper()
        if hasattr(self, 'chattube') and self.chattube is not None:
            self.chattube.SendText(entry)

    """
    Callback method for when the activity's visibility changes
    """
    def __visibility_notify_cb(self, window, event):
        if event.state == gtk.gdk.VISIBILITY_FULLY_OBSCURED:
            # _logger.debug("I am not visible so I should free the audio")
            self.tw.lc.ag = None
        elif event.state in \
            [gtk.gdk.VISIBILITY_UNOBSCURED, gtk.gdk.VISIBILITY_PARTIAL]:
            pass

    def update_title_cb(self, widget, event, toolbox):
        toolbox._activity_toolbar._update_title_cb()
        toolbox._activity_toolbar._update_title_sid = True

    def _keep_clicked_cb(self, button):
        self.jobject_new_patch()


    """
    Setup toolbar according to Sugar version
    """
    def _setup_toolbar(self):

        try: 
            # Use 0.86 toolbar design
            toolbar_box = ToolbarBox()
            # Buttons added to the Activity toolbar
            activity_button = ActivityToolbarButton(self)

            # Save snapshot is like Keep, but it creates a new activity id
            self.keep_button = ToolButton('filesave')
            self.keep_button.set_tooltip(_("Save snapshot"))
            self.keep_button.connect('clicked', self._do_keep_cb)
            self.keep_button.show()
            activity_button.props.page.insert(self.keep_button, -1)
            separator = gtk.SeparatorToolItem()
            separator.props.draw = True
            activity_button.props.page.insert(separator, -1)
            separator.show()

            # Save as HTML
            self.save_as_html = ToolButton('htmloff')
            self.save_as_html.set_tooltip(_("Save as HTML"))
            self.save_as_html.connect('clicked', self._do_save_as_html_cb)
            self.save_as_html.show()
            activity_button.props.page.insert(self.save_as_html, -1)

            # Save as Logo
            self.save_as_logo = ToolButton('logo-saveoff')
            self.save_as_logo.set_tooltip(_("Save as Logo"))
            self.save_as_logo.connect('clicked', self._do_save_as_logo_cb)
            self.save_as_logo.show()
            activity_button.props.page.insert(self.save_as_logo, -1)

            # Save as image
            self.save_as_image = ToolButton('image-saveoff')
            self.save_as_image.set_tooltip(_("Save as image"))
            self.save_as_image.connect('clicked', self._do_save_as_image_cb)
            self.save_as_image.show()
            activity_button.props.page.insert(self.save_as_image, -1)

            # Load Python code into programmable brick
            self.load_python = ToolButton('pippy-openoff')
            self.load_python.set_tooltip(_("Load my block"))
            self.load_python.connect('clicked', self._do_load_python_cb)
            self.load_python.show()
            activity_button.props.page.insert(self.load_python, -1)

            # Open project from the Journal 
            self.load_ta_project = ToolButton('load-from-journal')
            self.load_ta_project.set_tooltip(\
                                           _("Import project from the Journal"))
            self.load_ta_project.connect('clicked', self._do_load_ta_project_cb)
            self.load_ta_project.show()
            activity_button.props.page.insert(self.load_ta_project, -1)

            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            # The edit toolbar -- copy and paste
            edit_toolbar = EditToolbar(self)
            edit_toolbar_button = ToolbarButton(
                    page=edit_toolbar,
                    icon_name='toolbar-edit')
            edit_toolbar.show()
            toolbar_box.toolbar.insert(edit_toolbar_button, -1)
            edit_toolbar_button.show()

            # The view toolbar
            view_toolbar = gtk.Toolbar()
            fullscreen_button = ToolButton('view-fullscreen')
            fullscreen_button.set_tooltip(_("Fullscreen"))
            fullscreen_button.props.accelerator = '<Alt>Enter'
            fullscreen_button.connect('clicked', self._do_fullscreen_cb)
            view_toolbar.insert(fullscreen_button,-1)
            fullscreen_button.show()

            cartesian_button = ToolButton('view-Cartesian')
            cartesian_button.set_tooltip(_("Cartesian coordinates"))
            cartesian_button.connect('clicked', self._do_cartesian_cb)
            view_toolbar.insert(cartesian_button,-1)
            cartesian_button.show()

            polar_button = ToolButton('view-polar')
            polar_button.set_tooltip(_("polar coordinates"))
            polar_button.connect('clicked', self._do_polar_cb)
            view_toolbar.insert(polar_button,-1)
            polar_button.show()
    
            separator = gtk.SeparatorToolItem()
            separator.props.draw = True
            view_toolbar.insert(separator, -1)
            separator.show()

            self.coordinates_label = \
              gtk.Label(_("xcor") + " = 0 " + _("ycor") + " = 0 " + \
                        _("heading") + " = 0")
            self.coordinates_label.set_line_wrap(True)
            self.coordinates_label.show()
            self.coordinates_toolitem = gtk.ToolItem()
            self.coordinates_toolitem.add(self.coordinates_label)
            view_toolbar.insert(self.coordinates_toolitem,-1)
            self.coordinates_toolitem.show()

            view_toolbar_button = ToolbarButton(
                    page=view_toolbar,
                    icon_name='toolbar-view')
            view_toolbar.show()
            toolbar_box.toolbar.insert(view_toolbar_button, -1)
            view_toolbar_button.show()

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            view_toolbar.insert(separator, -1)
            separator.show()

            self.rescale_button = ToolButton('expand-coordinates')
            self.rescale_button.set_tooltip(_("Rescale coordinates up"))
            self.rescale_button.connect('clicked', self._do_rescale_cb)
            view_toolbar.insert(self.rescale_button,-1)
            self.rescale_button.show()

            # palette button (blocks)
            self.palette_button = ToolButton( "blocksoff" )
            self.palette_button.set_tooltip(_('Hide palette'))
            self.palette_button.props.sensitive = True
            self.palette_button.connect('clicked', self._do_palette_cb)
            self.palette_button.props.accelerator = _('<Ctrl>p')
            toolbar_box.toolbar.insert(self.palette_button, -1)
            self.palette_button.show()

            # blocks button (hideshow)
            self.blocks_button = ToolButton( "hideshowoff" )
            self.blocks_button.set_tooltip(_('Hide blocks'))
            self.blocks_button.props.sensitive = True
            self.blocks_button.connect('clicked', self._do_hideshow_cb)
            self.blocks_button.props.accelerator = _('<Ctrl>b')
            toolbar_box.toolbar.insert(self.blocks_button, -1)
            self.blocks_button.show()

            # eraser button
            self.eraser_button = ToolButton( "eraseron" )
            self.eraser_button.set_tooltip(_('Clean'))
            self.eraser_button.props.sensitive = True
            self.eraser_button.connect('clicked', self._do_eraser_cb)
            self.eraser_button.props.accelerator = _('<Ctrl>e')
            toolbar_box.toolbar.insert(self.eraser_button, -1)
            self.eraser_button.show()

            # run button
            self.run_button = ToolButton( "run-fastoff" )
            self.run_button.set_tooltip(_('Run'))
            self.run_button.props.sensitive = True
            self.run_button.connect('clicked', self._do_run_cb)
            self.run_button.props.accelerator = _('<Ctrl>r')
            toolbar_box.toolbar.insert(self.run_button, -1)
            self.run_button.show()

            # step button
            self.step_button = ToolButton( "run-slowoff" )
            self.step_button.set_tooltip(_('Step'))
            self.step_button.props.sensitive = True
            self.step_button.connect('clicked', self._do_step_cb)
            self.step_button.props.accelerator = _('<Ctrl>w')
            toolbar_box.toolbar.insert(self.step_button, -1)
            self.step_button.show()

            # debug button
            self.debug_button = ToolButton( "debugoff" )
            self.debug_button.set_tooltip(_('Debug'))
            self.debug_button.props.sensitive = True
            self.debug_button.connect('clicked', self._do_debug_cb)
            self.debug_button.props.accelerator = _('<Alt>d')
            toolbar_box.toolbar.insert(self.debug_button, -1)
            self.debug_button.show()

            # stop button
            self.stop_button = ToolButton( "stopitoff" )
            self.stop_button.set_tooltip(_('Stop turtle'))
            self.stop_button.props.sensitive = True
            self.stop_button.connect('clicked', self._do_stop_cb)
            self.stop_button.props.accelerator = _('<Ctrl>s')
            toolbar_box.toolbar.insert(self.stop_button, -1)
            self.stop_button.show()

            separator = gtk.SeparatorToolItem()
            separator.set_draw(True)
            toolbar_box.toolbar.insert(separator, -1)
            separator.show()

            # The Help toolbar -- sample code and hover help
            help_toolbar = gtk.Toolbar()
            samples_button = ToolButton( "stock-open" )
            samples_button.set_tooltip(_('Samples'))
            samples_button.connect('clicked', self._do_samples_cb)
            samples_button.show()
            help_toolbar.insert(samples_button, -1)
    
            separator = gtk.SeparatorToolItem()
            separator.props.draw = True
            help_toolbar.insert(separator, -1)
            separator.show()

            self.hover_help_label = \
              gtk.Label(_("Move the cursor over the orange palette for help."))
            self.hover_help_label.set_line_wrap(True)
            self.hover_help_label.show()
            self.hover_toolitem = gtk.ToolItem()
            self.hover_toolitem.add(self.hover_help_label)
            help_toolbar.insert(self.hover_toolitem,-1)
            self.hover_toolitem.show()

            help_toolbar_button = ToolbarButton(
                    label=_("Help"),
                    page=help_toolbar,
                    icon_name='help-toolbar')
            help_toolbar.show()
            toolbar_box.toolbar.insert(help_toolbar_button, -1)
            help_toolbar_button.show()

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            toolbar_box.toolbar.insert(separator, -1)
            separator.show()

            # The ever-present Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()

        except NameError:
            # Use pre-0.86 toolbar design
            self.toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self.toolbox)

            # Add additional panels
            self.projectToolbar = ProjectToolbar(self)
            self.toolbox.add_toolbar( _('Project'), self.projectToolbar )
            self.viewToolbar = ViewToolbar(self)
            self.toolbox.add_toolbar(_('View'), self.viewToolbar)
            self.editToolbar = EditToolbar(self)
            self.toolbox.add_toolbar(_('Edit'), self.editToolbar)
            self.saveasToolbar = SaveAsToolbar(self)
            self.toolbox.add_toolbar( _('Import/Export'), self.saveasToolbar )
            self.helpToolbar = HelpToolbar(self)
            self.toolbox.add_toolbar(_('Help'),self.helpToolbar)
            self.toolbox.show()

            # Set the project toolbar as the initial one selected
            self.toolbox.set_current_toolbar(1)

    """
    Create a scrolled window to contain the turtle canvas
    """
    def _setup_scrolled_window(self):
        self.sw = gtk.ScrolledWindow()
        self.set_canvas(self.sw)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.show()
        canvas = gtk.DrawingArea()
        width = gtk.gdk.screen_width() * 2
        height = gtk.gdk.screen_height() * 2
        canvas.set_size_request(width, height) 
        self.sw.add_with_viewport(canvas)
        canvas.show()
        return canvas

    """
    To be replaced with date checking in tasetup.py; 
    each language group should be stored in it's own sub-directory
    """
    def _check_ver_lang_change(self, datapath):
        # Check to see if the version or language has changed
        try:
            version = os.environ['SUGAR_BUNDLE_VERSION']
        except:
            version = " unknown"

        lang = locale.getdefaultlocale()[0]
        if not lang:
            lang = 'en'
        lang = lang[0:2]
        if not os.path.isdir(os.path.join(activity.get_bundle_path(), \
                             'images', lang)):
            lang = 'en'

        # If either has changed, remove the old png files
        filename = "version.dat"
        versiondata = []
        newversion = True
        try:
            FILE = open(os.path.join(datapath, filename), "r")
            if FILE.readline() == lang + version:
                newversion = False
            else:
                _logger.debug("out with the old, in with the new")
                cmd = "rm " + os.path.join(datapath, '*.png')
                subprocess.check_call(cmd, shell=True)
        except:
            _logger.debug("writing new version data")
            _logger.debug("and creating a tamyblock.py Journal entry")

        # Make sure there is a copy of tamyblock.py in the Journal
        if newversion is True:
            dsobject = datastore.create()
            dsobject.metadata['title'] = 'tamyblock.py'
            dsobject.metadata['icon-color'] = \
                profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'text/x-python'
            dsobject.metadata['activity'] = 'org.laptop.Pippy'
            dsobject.set_file_path(os.path.join( \
                activity.get_bundle_path(), 'tamyblock.py'))
            datastore.write(dsobject)
            dsobject.destroy()

        versiondata.append(lang + version)
        FILE = open(os.path.join(datapath, filename), "w")
        FILE.writelines(versiondata)
        FILE.close()

        return lang
    
    """
    Initialize the turtle art canvas
    """
    def _setup_canvas(self, canvas, lang):
        bundle_path = activity.get_bundle_path()
        self.tw = TurtleArtWindow(canvas, bundle_path, lang, self,
                                  profile.get_color().to_string())
        self.tw.activity = self
        self.tw.window.grab_focus()
        path = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'], 'data')
        self.tw.save_folder= path

        if self._jobject and self._jobject.file_path:
            self.read_file(self._jobject.file_path)
        else: # if new, load a start brick onto the canvas
            self.tw.load_start()

    """
    Check to see if there is Python code to be loaded
    """
    def _load_python_code(self):
        try:
            dsobject = datastore.get(self.metadata['python code'])
            self._load_python(dsobject)
        except:
            pass


    """
    A simplistic sharing model: the sharer is the master;
    TODO: hand off role of master is sharer leaves
    """
    def _setup_sharing(self):
        # Get the Presence Service
        self.pservice = presenceservice.get_instance()
        self.initiating = None # sharing (True) or joining (False)

        # Add my buddy object to the list
        owner = self.pservice.get_owner()
        self.owner = owner
        self.tw.buddies.append(self.owner)
        self._share = ""

        self.connect('shared', self._shared_cb)
        self.connect('joined', self._joined_cb)

    """
    get datapath
    """
    def _get_datapath(self):
        try:
            datapath = os.path.join(activity.get_activity_root(), "data")
        except:
            # Early versions of Sugar (e.g., 656) didn't support
            # get_activity_root()
            datapath = os.path.join( \
                os.environ['HOME'], \
                    ".sugar/default/org.laptop.TurtleArtActivity/data")
        return datapath

    """
    Notify when the visibility state changes
    """
    def _setup_visibility_handler(self):
        self.add_events(gtk.gdk.VISIBILITY_NOTIFY_MASK)
        self.connect("visibility-notify-event", self.__visibility_notify_cb)


    """
    Write the project to the Journal
    """
    def write_file(self, file_path):
        _logger.debug("Write file: %s" % file_path)
        self.metadata['mime_type'] = 'application/x-turtle-art'
        data_to_file(self.tw.assemble_data_to_save(), file_path)

    """
    Read a project in and then run it
    """
    def read_file(self, file_path, run_it = True):
        import tarfile,os,tempfile,shutil

        if hasattr(self, 'tw'):
            _logger.debug("Read file: %s" %  file_path)
            # Could be a gtar (newer builds) or tar (767) file
            if file_path[-5:] == ".gtar" or file_path[-4:] == ".tar":
                tar_fd = tarfile.open(file_path, 'r')
                tmpdir = tempfile.mkdtemp()
                try:
                    # We'll get 'ta_code.ta' and possibly a 'ta_image.png'
                    # but we will ignore the .png file
                    # If run_it is True, we want to create a new project
                    tar_fd.extractall(tmpdir)
                    self.tw.load_files(os.path.join(tmpdir,'ta_code.ta'), \
                                        run_it) # create a new project flag
                finally:
                    shutil.rmtree(tmpdir)
                    tar_fd.close()
            # Otherwise, assume it is a .ta file
            else:
                print "trying to open a .ta file:" + file_path
                self.tw.load_files(file_path, run_it)
  
            # run the activity
            if run_it:
                try:
                    # Use 0.86 toolbar design
                    self.stop_button.set_icon("stopiton")
                except:
                    # Use pre-0.86 toolbar design
                    self.projectToolbar.stop.set_icon("stopiton")

                self.tw.run_button(0)
        else:
            _logger.debug("Deferring reading file %s" %  file_path)

    """
    Save instance to Journal
    """
    def jobject_new_patch(self):
        oldj = self._jobject
        self._jobject = datastore.create()
        self._jobject.metadata['title'] = oldj.metadata['title']
        self._jobject.metadata['title_set_by_user'] = \
            oldj.metadata['title_set_by_user']
        # self._jobject.metadata['activity'] = self.get_service_name()
        self._jobject.metadata['activity_id'] = self.get_id()
        self._jobject.metadata['keep'] = '0'
        # Is this the correct syntax for saving the buddies list?
        # self._jobject.metadata['buddies'] = self.tw.buddies
        self._jobject.metadata['preview'] = ''
        self._jobject.metadata['icon-color'] = profile.get_color().to_string()
        self._jobject.file_path = ''
        datastore.write(self._jobject,
                reply_handler=self._internal_jobject_create_cb,
                error_handler=self._internal_jobject_error_cb)
        self._jobject.destroy()

"""
Class for setting up tube for sharing
"""
class ChatTube(ExportedGObject):
 
    def __init__(self, tube, is_initiator, stack_received_cb):
        super(ChatTube, self).__init__(tube, PATH)
        self.tube = tube
        self.is_initiator = is_initiator # Are we sharing or joining activity?
        self.stack_received_cb = stack_received_cb
        self.stack = ''

        self.tube.add_signal_receiver(self.send_stack_cb, 'SendText', IFACE, \
            path=PATH, sender_keyword='sender')

    def send_stack_cb(self, text, sender=None):
        if sender == self.tube.get_unique_name():
            return
        self.stack = text
        self.stack_received_cb(text)

    @signal(dbus_interface=IFACE, signature='s')
    def SendText(self, text):
        self.stack = text

"""
View toolbar: fullscreen, Cartesian, polar, coordinates
"""
class ViewToolbar(gtk.Toolbar):
    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # full screen
        self.activity.fullscreen_button = ToolButton( "view-fullscreen" )
        self.activity.fullscreen_button.set_tooltip(_('Fullscreen'))
        self.activity.fullscreen_button.props.sensitive = True
        try:
            self.activity.fullscreen_button.props.accelerator = '<Alt>Enter'
        except:
            pass
        self.activity.fullscreen_button.connect('clicked', \
                                                self.activity._do_fullscreen_cb)
        self.insert(self.activity.fullscreen_button, -1)
        self.activity.fullscreen_button.show()

        # Cartesian coordinates
        self.activity.cartesian_button = ToolButton( "view-Cartesian" )
        self.activity.cartesian_button.set_tooltip(_('Cartesian coordinates'))
        self.activity.cartesian_button.props.sensitive = True
        self.activity.cartesian_button.connect('clicked', \
                                                self.activity._do_cartesian_cb)
        self.insert(self.activity.cartesian_button, -1)
        self.activity.cartesian_button.show()

        # polar coordinates
        self.activity.polar_button = ToolButton( "view-polar" )
        self.activity.polar_button.set_tooltip(_('polar coordinates'))
        self.activity.polar_button.props.sensitive = True
        self.activity.polar_button.connect('clicked', \
                                           self.activity._do_polar_cb)
        self.insert(self.activity.polar_button, -1)
        self.activity.polar_button.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # Coordinates label
        self.activity.coordinates_label = \
          gtk.Label(_("xcor") + "= 0 " + _("ycor") + "= 0 " + \
                    _("heading") + "= 0")
        self.activity.coordinates_label.show()
        self.activity.coordinates_toolitem = gtk.ToolItem()
        self.activity.coordinates_toolitem.add(self.activity.coordinates_label)
        self.insert(self.activity.coordinates_toolitem,-1)
        self.activity.coordinates_toolitem.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(False)
        separator.set_expand(True)
        self.insert(separator, -1)
        separator.show()

        self.activity.rescale_button = ToolButton('expand-coordinates')
        self.activity.rescale_button.set_tooltip(_("Rescale coordinates up"))
        self.activity.rescale_button.connect('clicked', \
                                             self.activity._do_rescale_cb)
        self.insert(self.activity.rescale_button,-1)
        self.activity.rescale_button.show()

"""
Edit toolbar: copy and paste text and stacks
"""
class EditToolbar(gtk.Toolbar):
    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # Copy button
        self.copy = ToolButton( "edit-copy" )
        self.copy.set_tooltip(_('Copy'))
        self.copy.props.sensitive = True
        self.copy.connect('clicked', self._copy_cb)
        try:
            self.copy.props.accelerator = '<Ctrl>C'
        except:
            pass
        self.insert(self.copy, -1)
        self.copy.show()

        # Paste button
        self.paste = ToolButton( "edit-paste" )
        self.paste.set_tooltip(_('Paste'))
        self.paste.props.sensitive = True
        self.paste.connect('clicked', self._paste_cb)
        try:
            self.paste.props.accelerator = '<Ctrl>V'
        except:
            pass
        self.insert(self.paste, -1)
        self.paste.show()

    def _copy_cb(self, button):
        clipBoard = gtk.Clipboard()
        _logger.debug("serialize the project and copy to clipboard")
        data = self.activity.tw.assemble_data_to_save(False, False)
        if data is not []:
            text = data_to_string(data)
            clipBoard.set_text(text)

    def _paste_cb(self, button):
        clipBoard = gtk.Clipboard()
        _logger.debug("paste to the project")
        text = clipBoard.wait_for_text()
        if text is not None:
            self.activity.tw.process_data(data_from_string(text))

"""
Help toolbar: Just an icon and a label for displaying hover help
"""
class HelpToolbar(gtk.Toolbar):
    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # Help icon
        self.help = ToolButton( "help-toolbar" )
        self.help.props.sensitive = False
        self.insert(self.help, -1)
        self.help.show()

        # Help label
        self.activity.hover_help_label = \
          gtk.Label(_("Move the cursor over the orange palette for help."))
        self.activity.hover_help_label.set_line_wrap(True)
        self.activity.hover_help_label.show()
        self.activity.hover_toolitem = gtk.ToolItem()
        self.activity.hover_toolitem.add(self.activity.hover_help_label)
        self.insert(self.activity.hover_toolitem,-1)
        self.activity.hover_toolitem.show()

"""
SaveAs toolbar: (1) load samples; (2) save as HTML; (3) save as LOGO;
(4) save as PNG; and (5) import Python code.
"""
class SaveAsToolbar(gtk.Toolbar):
    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # HTML save source button
        self.activity.save_as_html = ToolButton( "htmloff" )
        self.activity.save_as_html.set_tooltip(_('Save as HTML'))
        self.activity.save_as_html.props.sensitive = True
        self.activity.save_as_html.connect('clicked', \
                                           self.activity._do_save_as_html_cb)
        self.insert(self.activity.save_as_html, -1)
        self.activity.save_as_html.show()

        # Berkeley Logo save source button
        self.activity.save_as_logo = ToolButton( "logo-saveoff" )
        self.activity.save_as_logo.set_tooltip(_('Save Logo'))
        self.activity.save_as_logo.props.sensitive = True
        self.activity.save_as_logo.connect('clicked', \
                                           self.activity._do_save_as_logo_cb)
        self.insert(self.activity.save_as_logo, -1)
        self.activity.save_as_logo.show()

        # Save as image button
        self.activity.save_as_image = ToolButton( "image-saveoff" )
        self.activity.save_as_image.set_tooltip(_('Save as image'))
        self.activity.save_as_image.props.sensitive = True
        self.activity.save_as_image.connect('clicked', \
                                   self.activity._do_save_as_image_cb)
        self.insert(self.activity.save_as_image, -1)
        self.activity.save_as_image.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # Pippy load myblock source button
        self.activity.load_python = ToolButton( "pippy-openoff" )
        self.activity.load_python.set_tooltip(_('Load my block'))
        self.activity.load_python.props.sensitive = True
        self.activity.load_python.connect('clicked', \
                                          self.activity._do_load_python_cb)
        self.insert(self.activity.load_python, -1)
        self.activity.load_python.show()

        # Open TA project from the Journal 
        self.activity.load_ta_project = ToolButton('load-from-journal')
        self.activity.load_ta_project.set_tooltip(\
                                  _("Import project from the Journal"))
        self.activity.load_ta_project.props.sensitive = True
        self.activity.load_ta_project.connect('clicked', \
                                     self.activity._do_load_ta_project_cb)
        self.insert(self.activity.load_ta_project, -1)
        self.activity.load_ta_project.show()


"""
Project toolbar: show/hide palettes; show/hide blocks; run; walk; stop; erase;
                 save as snapshot
"""
class ProjectToolbar(gtk.Toolbar):

    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # palette button (blocks)
        self.activity.palette_button = ToolButton( "blocksoff" )
        self.activity.palette_button.set_tooltip(_('Hide palette'))
        self.activity.palette_button.props.sensitive = True
        self.activity.palette_button.connect('clicked', \
                                             self.activity._do_palette_cb)
        try:
            self.activity.palette_button.props.accelerator = _('<Ctrl>p')
        except:
            pass
        self.insert(self.activity.palette_button, -1)
        self.activity.palette_button.show()

        # blocks button (hideshow)
        self.activity.blocks_button = ToolButton( "hideshowoff" )
        self.activity.blocks_button.set_tooltip(_('Hide blocks'))
        self.activity.blocks_button.props.sensitive = True
        self.activity.blocks_button.connect('clicked', \
                                            self.activity._do_hideshow_cb)
        try:
            self.activity.blocks_button.props.accelerator = _('<Ctrl>b')
        except:
            pass
        self.insert(self.activity.blocks_button, -1)
        self.activity.blocks_button.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # run button
        self.activity.run_button = ToolButton( "run-fastoff" )
        self.activity.run_button.set_tooltip(_('Run'))
        self.activity.run_button.props.sensitive = True
        self.activity.run_button.connect('clicked', self.activity._do_run_cb)
        try:
            self.activity.run_button.props.accelerator = _('<Ctrl>r')
        except:
            pass
        self.insert(self.activity.run_button, -1)
        self.activity.run_button.show()

        # step button
        self.activity.step_button = ToolButton( "run-slowoff" )
        self.activity.step_button.set_tooltip(_('Step'))
        self.activity.step_button.props.sensitive = True
        self.activity.step_button.connect('clicked', self.activity._do_step_cb)
        try:
            self.activity.step_button.props.accelerator = _('<Ctrl>w')
        except:
            pass
        self.insert(self.activity.step_button, -1)
        self.activity.step_button.show()

        # debug button
        self.activity.debug_button = ToolButton( "debugoff" )
        self.activity.debug_button.set_tooltip(_('Debug'))
        self.activity.debug_button.props.sensitive = True
        self.activity.debug_button.connect('clicked', \
                                           self.activity._do_debug_cb)
        try:
            self.activity.debug_button.props.accelerator = _('<Ctrl>d')
        except:
            pass
        self.insert(self.activity.debug_button, -1)
        self.activity.debug_button.show()

        # stop button
        self.activity.stop_button = ToolButton( "stopitoff" )
        self.activity.stop_button.set_tooltip(_('Stop turtle'))
        self.activity.stop_button.props.sensitive = True
        self.activity.stop_button.connect('clicked', self.activity._do_stop_cb)
        try:
            self.activity.stop_button.props.accelerator = _('<Ctrl>s')
        except:
            pass
        self.insert(self.activity.stop_button, -1)
        self.activity.stop_button.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # eraser button
        self.activity.eraser_button = ToolButton( "eraseron" )
        self.activity.eraser_button.set_tooltip(_('Clean'))
        self.activity.eraser_button.props.sensitive = True
        self.activity.eraser_button.connect('clicked', \
                                            self.activity._do_eraser_cb)
        try:
            self.activity.eraser_button.props.accelerator = _('<Ctrl>e')
        except:
            pass
        self.insert(self.activity.eraser_button, -1)
        self.activity.eraser_button.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # Save snapshot ("keep")
        self.activity.keep_button = ToolButton( "filesave" )
        self.activity.keep_button.set_tooltip(_('Save snapshot'))
        self.activity.keep_button.props.sensitive = True
        try:
            self.activity.keep_button.props.accelerator = '<Alt>S'
        except:
            pass
        self.activity.keep_button.connect('clicked', \
                                    self.activity._do_keep_cb)
        self.insert(self.activity.keep_button, -1)
        self.activity.keep_button.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # project open
        self.activity.samples_button = ToolButton( "stock-open" )
        self.activity.samples_button.set_tooltip(_('Samples'))
        self.activity.samples_button.props.sensitive = True
        self.activity.samples_button.connect('clicked', \
                                             self.activity._do_samples_cb)
        try:
             self.activity.samples_button.props.accelerator = _('<Ctrl>o')
        except:
            pass
        self.insert(self.activity.samples_button, -1)
        self.activity.samples_button.show()


