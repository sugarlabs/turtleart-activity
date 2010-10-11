#Copyright (c) 2007, Playful Invention Company
#Copyright (c) 2008-10, Walter Bender
#Copyright (c) 2009,10 Raul Gutierrez Segales

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

from sugar.activity import activity
try: # 0.86 toolbar widgets
    from sugar.activity.widgets import ActivityToolbarButton, StopButton,\
                                       EditToolbar, ActivityToolbox
    from sugar.graphics.toolbarbox import ToolbarBox, ToolbarButton
    NEW_SUGAR_SYSTEM = True
except ImportError:
    NEW_SUGAR_SYSTEM = False
from sugar.graphics.toolbutton import ToolButton
from sugar.datastore import datastore

import telepathy
from dbus.service import signal
from dbus.gobject_service import ExportedGObject
from sugar.presence import presenceservice
from sugar.presence.tubeconn import TubeConnection

from sugar import profile
from gettext import gettext as _
import os.path
import tarfile

from TurtleArt.taconstants import PALETTE_NAMES, OVERLAY_LAYER, HELP_STRINGS
from TurtleArt.taexporthtml import save_html
from TurtleArt.taexportlogo import save_logo
from TurtleArt.tautils import data_to_file, data_to_string, data_from_string, \
                              get_path, chooser
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.taturtle import Turtle

SERVICE = 'org.laptop.TurtleArtActivity'
IFACE = SERVICE
PATH = '/org/laptop/TurtleArtActivity'


def _add_label(string, toolbar):
    """ add a label to a toolbar """
    label = gtk.Label(string)
    label.set_line_wrap(True)
    label.show()
    toolitem = gtk.ToolItem()
    toolitem.add(label)
    toolbar.insert(toolitem, -1)
    toolitem.show()
    return label


def _add_separator(toolbar, expand=False):
    """ add a separator to a toolbar """
    separator = gtk.SeparatorToolItem()
    separator.props.draw = True
    separator.set_expand(expand)
    toolbar.insert(separator, -1)
    separator.show()


def _add_button(name, tooltip, callback, toolbar, accelerator=None, arg=None):
    """ add a button to a toolbar """
    button = ToolButton(name)
    button.set_tooltip(tooltip)
    if arg is None:
        button.connect('clicked', callback)
    else:
        button.connect('clicked', callback, arg)
    if accelerator is not None:
        try:
            button.props.accelerator = accelerator
        except AttributeError:
            pass
    button.show()
    if hasattr(toolbar, 'insert'): # the main toolbar
        toolbar.insert(button, -1)
    else:  # or a secondary toolbar
        toolbar.props.page.insert(button, -1)
    return button


class TurtleArtActivity(activity.Activity):

    def __init__(self, handle):
        """ Activity subclass for Turtle Art """
        super(TurtleArtActivity, self).__init__(handle)

        datapath = get_path(activity, 'data')

        self._setup_visibility_handler()

        self.new_sugar_system = NEW_SUGAR_SYSTEM
        self._setup_toolbar()

        canvas = self._setup_scrolled_window()

        self._check_ver_change(datapath)

        self._setup_canvas(canvas)

        self._load_python_code()

        self._setup_sharing()

    # Activity toolbar callbacks

    def do_save_as_html_cb(self, button):
        """ Write html out to datastore. """
        self.save_as_html.set_icon("htmlon")
        _logger.debug("saving html code")
        # until we have URLs for datastore objects, always embed images
        embed_flag = True

        # grab code from stacks
        html = save_html(self, self.tw, embed_flag)
        if len(html) == 0:
            return

        # save the html code to the instance directory
        datapath = get_path(activity, 'instance')

        save_type = '.html'
        if len(self.tw.saved_pictures) > 0:
            if self.tw.saved_pictures[0].endswith(('.svg')):
                save_type = '.xml'

        html_file = os.path.join(datapath, "portfolio" + save_type)
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
            if save_type == '.xml':
                dsobject.metadata['mime_type'] = 'application/xml'
            else:
                dsobject.metadata['mime_type'] = 'text/html'
            dsobject.set_file_path(html_file)
        else:
            dsobject.metadata['mime_type'] = 'application/x-tar'
            dsobject.set_file_path(tar_path)

        dsobject.metadata['activity'] = 'org.laptop.WebActivity'
        datastore.write(dsobject)
        dsobject.destroy()
        gobject.timeout_add(250, self.save_as_html.set_icon, "htmloff")

        self.tw.saved_pictures = []
        return

    def do_save_as_logo_cb(self, button):
        """ Write logo code out to datastore. """
        self.save_as_logo.set_icon("logo-saveon")
        logo_code_path = self._dump_logo_code()
        if logo_code_path is None:
            return

        # Create a datastore object
        dsobject = datastore.create()

        # Write any metadata (here we specifically set the title of the file
        # and specify that this is a plain text file).
        dsobject.metadata['title'] = self.metadata['title'] + ".lg"
        dsobject.metadata['mime_type'] = 'text/plain'
        dsobject.metadata['icon-color'] = profile.get_color().to_string()

        # Set the file_path in the datastore.
        dsobject.set_file_path(logo_code_path)

        datastore.write(dsobject)
        gobject.timeout_add(250, self.save_as_logo.set_icon, "logo-saveoff")
        return

    def do_load_ta_project_cb(self, button):
        """ Load a project from the Journal """
        chooser(self, SERVICE, self._load_ta_project)

    def _load_ta_project(self, dsobject):
        """ Load a ta project from the datastore """
        try:
            _logger.debug("opening %s " % dsobject.file_path)
            self.read_file(dsobject.file_path, False)
        except:
            _logger.debug("couldn't open %s" % dsobject.file_path)

    def do_load_python_cb(self, button):
        """ Load Python code from the Journal. """
        self.load_python.set_icon("pippy-openon")
        self.import_py()
        gobject.timeout_add(250, self.load_python.set_icon, "pippy-openoff")

    def import_py(self):
        """ Import Python code from the Journal to load into 'myblock'. """
        chooser(self, 'org.laptop.Pippy', self._load_python)

    def _load_python(self, dsobject):
        """ Read the Python code from the Journal object """
        try:
            _logger.debug("opening %s " % dsobject.file_path)
            file_handle = open(dsobject.file_path, "r")
            self.tw.myblock = file_handle.read()
            file_handle.close()
            self.tw.set_userdefined()
            # save reference to Pythin code in the project metadata
            self.metadata['python code'] = dsobject.object_id
        except:
            _logger.debug("couldn't open %s" % dsobject.file_path)

    def do_save_as_image_cb(self, button):
        """ Save the canvas to the Journal. """
        self.save_as_image.set_icon("image-saveon")
        _logger.debug("saving image to journal")

        self.tw.save_as_image()
        gobject.timeout_add(250, self.save_as_image.set_icon, "image-saveoff")
        return

    def do_keep_cb(self, button):
        """ Save a snapshot of the project to the Journal. """
        tmpfile = self._dump_ta_code()
        if tmpfile is not None:
            # Create a datastore object
            dsobject = datastore.create()

            # Write any metadata
            dsobject.metadata['title'] = self.metadata['title'] + " " + \
                _("snapshot")
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'application/x-turtle-art'
            dsobject.metadata['activity'] = 'org.laptop.TurtleArtActivity'
            dsobject.set_file_path(tmpfile)
            datastore.write(dsobject)

            # Clean up
            dsobject.destroy()
            os.remove(tmpfile)
        return

    # Main toolbar button callbacks

    def do_palette_cb(self, button):
        """ Show/hide palette """
        if self.tw.palette == True:
            self.tw.hideshow_palette(False)
            self.palette_button.set_icon("paletteon")
            self.palette_button.set_tooltip(_('Show palette'))
            if self.new_sugar_system and self.tw.selected_palette is not None:
                self.palette_buttons[self.tw.selected_palette].set_icon(
                    PALETTE_NAMES[self.tw.selected_palette] + 'off')
        else:
            self.tw.hideshow_palette(True)
            self.palette_button.set_icon("paletteoff")
            self.palette_button.set_tooltip(_('Hide palette'))
            if self.new_sugar_system:
                self.palette_buttons[0].set_icon(PALETTE_NAMES[0] + 'on')

    def do_palette_buttons_cb(self, button, i):
        """ Palette selector buttons """
        if self.tw.selected_palette is not None:
            if self.tw.selected_palette != i:
                self.palette_buttons[self.tw.selected_palette].set_icon(
                    PALETTE_NAMES[self.tw.selected_palette] + 'off')
        self.palette_buttons[i].set_icon(PALETTE_NAMES[i] + 'on')
        self.tw.show_palette(i)
        self.palette_button.set_icon("paletteoff")
        self.palette_button.set_tooltip(_('Hide palette'))

    # These methods are called both from buttons and palette.

    def do_hidepalette(self):
        """ Hide the palette. """
        self.palette_button.set_icon("paletteon")
        self.palette_button.set_tooltip(_('Show palette'))

    def do_showpalette(self):
        """ Show the palette. """
        self.palette_button.set_icon("paletteoff")
        self.palette_button.set_tooltip(_('Hide palette'))

    def do_hideshow_cb(self, button):
        """ Toggle visibility. """
        self.tw.hideshow_button()
        if self.tw.hide == True: # we just hid the blocks
            self.blocks_button.set_icon("hideshowon")
            self.blocks_button.set_tooltip(_('Show blocks'))
        else:
            self.blocks_button.set_icon("hideshowoff")
            self.blocks_button.set_tooltip(_('Hide blocks'))
        # update palette buttons too
        if self.tw.palette == False:
            self.palette_button.set_icon("paletteon")
            self.palette_button.set_tooltip(_('Show palette'))
        else:
            self.palette_button.set_icon("paletteoff")
            self.palette_button.set_tooltip(_('Hide palette'))

    def do_hide(self):
        """ Hide blocks. """
        self.blocks_button.set_icon("hideshowon")
        self.blocks_button.set_tooltip(_('Show blocks'))
        self.palette_button.set_icon("paletteon")
        self.palette_button.set_tooltip(_('Show palette'))

    def do_show(self):
        """ Show blocks. """
        self.blocks_button.set_icon("hideshowoff")
        self.blocks_button.set_tooltip(_('Hide blocks'))
        self.palette_button.set_icon("paletteoff")
        self.palette_button.set_tooltip(_('Hide palette'))

    def do_eraser_cb(self, button):
        """ Clear the screen and recenter. """
        self.eraser_button.set_icon("eraseroff")
        self.recenter()
        self.tw.eraser_button()
        gobject.timeout_add(250, self.eraser_button.set_icon, "eraseron")

    def do_run_cb(self, button):
        """ Callback for run button (rabbit). """
        self.run_button.set_icon("run-faston")
        self.tw.lc.trace = 0
        self.tw.run_button(0)
        gobject.timeout_add(1000, self.run_button.set_icon, "run-fastoff")

    def do_step_cb(self, button):
        """ Callback for step button (turtle). """
        self.step_button.set_icon("run-slowon")
        self.tw.lc.trace = 0
        self.tw.run_button(3)
        gobject.timeout_add(1000, self.step_button.set_icon, "run-slowoff")

    def do_debug_cb(self, button):
        """ Callback for debug button (bug). """
        self.debug_button.set_icon("debugon")
        self.tw.lc.trace = 1
        self.tw.run_button(6)
        gobject.timeout_add(1000, self.debug_button.set_icon, "debugoff")

    def do_stop_cb(self, button):
        """ Callback for stop button. """
        self.stop_turtle_button.set_icon("stopitoff")
        self.tw.stop_button()
        self.step_button.set_icon("run-slowoff")
        self.run_button.set_icon("run-fastoff")

    def do_samples_cb(self, button):
        """ Sample projects open dialog """
        # FIXME: encapsulation!
        self.tw.load_file(True)
        # run the activity
        self.stop_turtle_button.set_icon("stopiton")
        self.tw.run_button(0)

    def recenter(self):
        """ Recenter scrolled window around canvas. """
        hadj = self.sw.get_hadjustment()
        hadj.set_value(0)
        self.sw.set_hadjustment(hadj)
        vadj = self.sw.get_vadjustment()
        vadj.set_value(0)
        self.sw.set_vadjustment(vadj)

    def do_fullscreen_cb(self, button):
        """ Hide the Sugar toolbars. """
        self.fullscreen()
        self.recenter()

    def do_grow_blocks_cb(self, button):
        """ Grow the blocks. """
        self.do_resize_blocks(1.5)

    def do_shrink_blocks_cb(self, button):
        """ Shrink the blocks. """
        self.do_resize_blocks(0.67)

    def do_resize_blocks(self, scale_factor):
        """ Scale the blocks. """
        self.tw.block_scale *= scale_factor
        self.tw.resize_blocks()

    def do_cartesian_cb(self, button):
        """ Display Cartesian coordinate grid. """
        if self.tw.cartesian:
            self.tw.set_cartesian(False)
        else:
            self.tw.set_cartesian(True)

    def do_polar_cb(self, button):
        """ Display Polar coordinate grid. """
        if self.tw.polar:
            self.tw.set_polar(False)
        else:
            self.tw.set_polar(True)

    def do_rescale_cb(self, button):
        """ Rescale coordinate system (100==height/2 or 100 pixels). """
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height / 200
            self.rescale_button.set_icon("contract-coordinates")
            self.rescale_button.set_tooltip(_('Rescale coordinates down'))
            self.tw.eraser_button()
            if self.tw.cartesian:
                self.tw.overlay_shapes['Cartesian_labeled'].hide()
                self.tw.overlay_shapes['Cartesian'].set_layer(OVERLAY_LAYER)
        else:
            self.tw.coord_scale = 1
            self.rescale_button.set_icon("expand-coordinates")
            self.rescale_button.set_tooltip(_('Rescale coordinates up'))
            self.tw.eraser_button()
            if self.tw.cartesian:
                self.tw.overlay_shapes['Cartesian'].hide()
                self.tw.overlay_shapes['Cartesian_labeled'].set_layer(
                                                              OVERLAY_LAYER)

    def get_document_path(self, async_cb, async_err_cb):
        """  View TA code as part of view source.  """
        ta_code_path = self._dump_ta_code()
        if ta_code_path is not None:
            async_cb(ta_code_path)
            os.remove(tmpfile)

    def _dump_logo_code(self):
        """  Save Logo code to temporary file. """
        datapath = get_path(activity, 'instance')
        tmpfile = os.path.join(datapath, 'tmpfile.lg')
        code = save_logo(self.tw)
        if len(code) == 0:
            _logger.debug('save_logo returned None')
            return None
        try:
            f = file(tmpfile, "w")
            f.write(code)
            f.close()
        except Exception, e:
            _logger.error("Couldn't dump code to view source: " + str(e))
        return tmpfile

    def _dump_ta_code(self):
        """  Save TA code to temporary file. """
        datapath = get_path(activity, 'instance')
        tmpfile = os.path.join(datapath, 'tmpfile.ta')
        try:
            data_to_file(self.tw.assemble_data_to_save(), tmpfile)
        except:
            _logger.debug("couldn't save snapshot to journal")
            tmpfile = None
        return tmpfile

    # Sharing-related callbacks

    def _shared_cb(self, activity):
        """ Either set up initial share... """
        if self._shared_activity is None:
            _logger.error("Failed to share or join activity ... \
                _shared_activity is null in _shared_cb()")
            return

        self.initiating = True
        self.waiting_for_turtles = False
        self.turtle_dictionary = \
            {profile.get_nick_name(): profile.get_color().to_string()}
        _logger.debug('I am sharing...')

        self.conn = self._shared_activity.telepathy_conn
        self.tubes_chan = self._shared_activity.telepathy_tubes_chan
        self.text_chan = self._shared_activity.telepathy_text_chan

        # call back for "NewTube" signal
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal(
            'NewTube', self._new_tube_cb)

        _logger.debug('This is my activity: making a tube...')
        id = self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferDBusTube(
            SERVICE, {})

    def _joined_cb(self, activity):
        """ ...or join an exisiting share. """
        if self._shared_activity is None:
            _logger.error("Failed to share or join activity ... \
                _shared_activity is null in _shared_cb()")
            return

        self.initiating = False
        self.conn = self._shared_activity.telepathy_conn
        self.tubes_chan = self._shared_activity.telepathy_tubes_chan
        self.text_chan = self._shared_activity.telepathy_text_chan

        # call back for "NewTube" signal
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal(
            'NewTube', self._new_tube_cb)

        _logger.debug('I am joining an activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb,
            error_handler=self._list_tubes_error_cb)

        # Joiner should request current state from sharer.
        self.waiting_for_turtles = True

    def _list_tubes_reply_cb(self, tubes):
        for tube_info in tubes:
            self._new_tube_cb(*tube_info)

    def _list_tubes_error_cb(self, e):
        _logger.error('ListTubes() failed: %s', e)

    def _new_tube_cb(self, id, initiator, type, service, params, state):
        """ Create a new tube. """
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

            # We'll use a chat tube to send serialized stacks back and forth.
            self.chattube = ChatTube(tube_conn, self.initiating, \
                self.event_received_cb)

            # Now that we have the tube, we can ask for the turtle dictionary.
            if self.waiting_for_turtles:
                _logger.debug("Sending a request for the turtle dictionary")
                # we need to send our own nick and colors
                colors = profile.get_color().to_string()
                _logger.debug("t|" + data_to_string([self.tw.nick, colors]))
                self.send_event("t|%s" % \
                                (data_to_string([self.tw.nick, colors])))

    def event_received_cb(self, text):
        """ Handle the receiving of events in share """
        # _logger.debug(text)

        """
        Events are sent as a tuple, nick|cmd, where nick is a turle name
        and cmd is a turtle event. Everyone gets the turtle dictionary from
        the sharer and watches for 't' events, which indicate that a new
        turtle has joined.
        """
        if len(text) == 0:
            return
        # Save active Turtle
        save_active_turtle = self.tw.active_turtle
        e = text.split("|", 2)
        text = e[1]
        if e[0] == 't': # request for turtle dictionary
            if text > 0:
                [nick, colors] = data_from_string(text)
                if nick != self.tw.nick:
                    # There may not be a turtle dictionary.
                    if hasattr(self, "turtle_dictionary"):
                        self.turtle_dictionary[nick] = colors
                    else:
                        self.turtle_dictionary = {nick: colors}
                    # Add new turtle for the joiner.
                    self.tw.canvas.set_turtle(nick, colors)
            # Sharer should send turtle dictionary.
            if self.initiating:
                text = data_to_string(self.turtle_dictionary)
                self.send_event("T|" + text)
        elif e[0] == 'T': # Receiving the turtle dictionary.
            if self.waiting_for_turtles:
                if len(text) > 0:
                    self.turtle_dictionary = data_from_string(text)
                    for nick in self.turtle_dictionary:
                        if nick != self.tw.nick:
                            colors = self.turtle_dictionary[nick]
                            # add new turtle for the joiner
                            self.tw.canvas.set_turtle(nick, colors)
                self.waiting_for_turtles = False
        elif e[0] == 'f': # move a turtle forward
            if len(text) > 0:
                [nick, x] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.forward(x, False)
        elif e[0] == 'a': # move a turtle in an arc
            if len(text) > 0:
                [nick, [a, r]] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.arc(a, r, False)
        elif e[0] == 'r': # rotate turtle
            if len(text) > 0:
                [nick, h] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.seth(h, False)
        elif e[0] == 'x': # set turtle xy position
            if len(text) > 0:
                [nick, [x, y]] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.setxy(x, y, False)
        elif e[0] == 'c': # set turtle pen color
            if len(text) > 0:
                [nick, x] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.setcolor(x, False)
        elif e[0] == 'g': # set turtle pen gray level
            if len(text) > 0:
                [nick, x] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.setgray(x, False)
        elif e[0] == 's': # set turtle pen shade
            if len(text) > 0:
                [nick, x] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.setshade(x, False)
        elif e[0] == 'w': # set turtle pen width
            if len(text) > 0:
                [nick, x] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.setpensize(x, False)
        elif e[0] == 'p': # set turtle pen state
            if len(text) > 0:
                [nick, x] = data_from_string(text)
                if nick != self.tw.nick:
                    self.tw.canvas.set_turtle(nick)
                    self.tw.canvas.setpen(x, False)
        # Restore active Turtle
        self.tw.canvas.set_turtle(self.tw.turtles.get_turtle_key(
                save_active_turtle))

    def send_event(self, entry):
        """ Send event through the tube. """
        if hasattr(self, 'chattube') and self.chattube is not None:
            self.chattube.SendText(entry)

    def __visibility_notify_cb(self, window, event):
        """ Callback method for when the activity's visibility changes. """
        if event.state == gtk.gdk.VISIBILITY_FULLY_OBSCURED:
            self.tw.lc.ag = None
        elif event.state in \
            [gtk.gdk.VISIBILITY_UNOBSCURED, gtk.gdk.VISIBILITY_PARTIAL]:
            pass

    def update_title_cb(self, widget, event, toolbox):
        """ Update the title. """
        toolbox._activity_toolbar._update_title_cb()
        toolbox._activity_toolbar._update_title_sid = True

    def _keep_clicked_cb(self, button):
        """ Keep button clicked. """
        self.jobject_new_patch()

    def _setup_toolbar(self):
        """ Setup toolbar according to Sugar version """
        if self.new_sugar_system:
            # Use 0.86 toolbar design
            # Create toolbox and secondary toolbars
            toolbox = ToolbarBox()

            activity_toolbar_button = ActivityToolbarButton(self)

            edit_toolbar = gtk.Toolbar()
            edit_toolbar_button = ToolbarButton(label=_('Edit'),
                                                page=edit_toolbar,
                                                icon_name='toolbar-edit')
            view_toolbar = gtk.Toolbar()
            view_toolbar_button = ToolbarButton(label=_('View'),
                                                page=view_toolbar,
                                                icon_name='toolbar-view')
            palette_toolbar = gtk.Toolbar()
            palette_toolbar_button = ToolbarButton(page=palette_toolbar,
                                                   icon_name='palette')
            help_toolbar = gtk.Toolbar()
            help_toolbar_button = ToolbarButton(label=_("Help"),
                                                page=help_toolbar,
                                                icon_name='help-toolbar')

            # Add the toolbars and buttons to the toolbox
            activity_toolbar_button.show()
            toolbox.toolbar.insert(activity_toolbar_button, -1)
            edit_toolbar_button.show()
            toolbox.toolbar.insert(edit_toolbar_button, -1)
            view_toolbar_button.show()
            toolbox.toolbar.insert(view_toolbar_button, -1)
            toolbox.toolbar.insert(palette_toolbar_button, -1)
            palette_toolbar_button.show()

            _add_separator(toolbox.toolbar)

            self._make_project_buttons(toolbox.toolbar)

            _add_separator(toolbox.toolbar)

            toolbox.toolbar.insert(help_toolbar_button, -1)
            help_toolbar_button.show()

            _add_separator(toolbox.toolbar, True)

            # Sugar Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

        else:
            # Use pre-0.86 toolbar design
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)

            project_toolbar = gtk.Toolbar()
            toolbox.add_toolbar(_('Project'), project_toolbar)

            view_toolbar = gtk.Toolbar()
            toolbox.add_toolbar(_('View'), view_toolbar)
            view_toolbar_button = view_toolbar
            edit_toolbar = gtk.Toolbar()
            toolbox.add_toolbar(_('Edit'), edit_toolbar)
            edit_toolbar_button = edit_toolbar
            save_toolbar = gtk.Toolbar()
            toolbox.add_toolbar(_('Import/Export'), save_toolbar)
            activity_toolbar_button = save_toolbar
            help_toolbar = gtk.Toolbar()
            toolbox.add_toolbar(_('Help'), help_toolbar)
            help_toolbar_button = help_toolbar

            self._make_palette_buttons(project_toolbar)

            _add_separator(project_toolbar)

            self._make_project_buttons(project_toolbar)

        self.keep_button = _add_button('filesave', _("Save snapshot"),
                                       self.do_keep_cb,
                                       activity_toolbar_button)
        self.save_as_html = _add_button('htmloff', _("Save as HTML"),
                                        self.do_save_as_html_cb,
                                        activity_toolbar_button)
        self.save_as_logo = _add_button('logo-saveoff', _("Save as Logo"),
                                        self.do_save_as_logo_cb,
                                        activity_toolbar_button)
        self.save_as_image = _add_button('image-saveoff', _("Save as image"),
                                         self.do_save_as_image_cb,
                                         activity_toolbar_button)
        self.load_python = _add_button('pippy-openoff', _("Load my block"),
                                       self.do_load_python_cb,
                                       activity_toolbar_button)
        self.load_ta_project = _add_button('load-from-journal',
            _("Import project from the Journal"), self.do_load_ta_project_cb,
                                           activity_toolbar_button)
        copy = _add_button('edit-copy', _('Copy'), self._copy_cb,
                           edit_toolbar_button, '<Ctrl>c')
        paste = _add_button('edit-paste', _('Paste'), self._paste_cb,
                            edit_toolbar_button, '<Ctrl>v')
        fullscreen_button = _add_button('view-fullscreen', _("Fullscreen"),
                                        self.do_fullscreen_cb,
                                        view_toolbar_button, '<Alt>Return')
        cartesian_button = _add_button('view-Cartesian',
                                       _("Cartesian coordinates"),
                                       self.do_cartesian_cb,
                                       view_toolbar_button)
        polar_button = _add_button('view-polar', _("Polar coordinates"),
                                   self.do_polar_cb, view_toolbar_button)
        _add_separator(view_toolbar)
        self.coordinates_label = _add_label(
            _("xcor") + " = 0 " + _("ycor") + " = 0 " + _("heading") + " = 0",
            view_toolbar)
        _add_separator(view_toolbar, True)
        self.rescale_button = _add_button('expand-coordinates',
            _("Rescale coordinates up"), self.do_rescale_cb,
                                          view_toolbar_button)
        self.resize_up_button = _add_button('resize+', _("Grow blocks"),
            self.do_grow_blocks_cb, view_toolbar_button)
        self.resize_down_button = _add_button('resize-', _("Shrink blocks"),
            self.do_shrink_blocks_cb, view_toolbar_button)
        self.samples_button = _add_button("stock-open", _('Samples'),
            self.do_samples_cb, help_toolbar_button)
        _add_separator(help_toolbar)
        self.hover_help_label = _add_label(
            _("Move the cursor over the orange palette for help."),
            help_toolbar)

        # The palette toolbar is only used with 0.86+
        if self.new_sugar_system:
            self.palette_buttons = []
            for i, name in enumerate(PALETTE_NAMES):
                if i > 0:
                    suffix = 'off'
                else:
                    suffix = 'on'
                self.palette_buttons.append(_add_button(name + suffix,
                    HELP_STRINGS[name], self.do_palette_buttons_cb,
                    palette_toolbar_button, None, i))
            _add_separator(palette_toolbar, True)

            self._make_palette_buttons(palette_toolbar_button)

            self.set_toolbar_box(toolbox)
            palette_toolbar.show()

        edit_toolbar.show()
        view_toolbar.show()
        help_toolbar.show()
        toolbox.show()

        if self.new_sugar_system:
            # Hack as a workaround for #2050
            edit_toolbar_button.set_expanded(True)
            edit_toolbar_button.set_expanded(False)

            palette_toolbar_button.set_expanded(True)
        else:
            toolbox.set_current_toolbar(1)

    def _make_palette_buttons(self, toolbar):
        """ Creates the palette and block buttons for both toolbar types"""
        self.palette_button = _add_button("paletteoff", _('Hide palette'),
            self.do_palette_cb, toolbar, _('<Ctrl>p'))
        self.blocks_button = _add_button("hideshowoff", _('Hide blocks'),
            self.do_hideshow_cb, toolbar, _('<Ctrl>b'))

    def _make_project_buttons(self, toolbar):
        """ Creates the turtle buttons for both toolbar types"""
        self.eraser_button = _add_button("eraseron", _('Clean'),
            self.do_eraser_cb, toolbar, _('<Ctrl>e'))
        self.run_button = _add_button("run-fastoff", _('Run'), self.do_run_cb,
                                      toolbar, _('<Ctrl>r'))
        self.step_button = _add_button("run-slowoff", _('Step'),
                                       self.do_step_cb, toolbar, _('<Ctrl>w'))
        self.debug_button = _add_button("debugoff", _('Debug'),
            self.do_debug_cb, toolbar, _('<Ctrl>d'))
        self.stop_turtle_button = _add_button("stopitoff", _('Stop turtle'),
            self.do_stop_cb, toolbar, _('<Ctrl>s'))

    def _setup_scrolled_window(self):
        """ Create a scrolled window to contain the turtle canvas. """
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

    def _check_ver_change(self, datapath):
        """ To be replaced with date checking. """
        # Check to see if the version has changed
        try:
            version = os.environ['SUGAR_BUNDLE_VERSION']
        except:
            version = "unknown"

        filename = "version.dat"
        versiondata = []
        newversion = True
        try:
            FILE = open(os.path.join(datapath, filename), "r")
            if FILE.readline() == version:
                newversion = False
        except IOError:
            _logger.debug("Creating a tamyblock.py Journal entry")

        # Make sure there is a copy of tamyblock.py in the Journal
        if newversion:
            dsobject = datastore.create()
            dsobject.metadata['title'] = 'tamyblock.py'
            dsobject.metadata['icon-color'] = \
                profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'text/x-python'
            dsobject.metadata['activity'] = 'org.laptop.Pippy'
            dsobject.set_file_path(os.path.join(activity.get_bundle_path(),
                                                'TurtleArt/tamyblock.py'))
            try:
                datastore.write(dsobject)
            except IOError:
                _logger.error("Error copying %s to the datastore" % \
                                  (os.path.join(activity.get_bundle_path(),
                                                'TurtleArt/tamyblock.py')))
            dsobject.destroy()

        versiondata.append(version)
        file_handle = open(os.path.join(datapath, filename), "w")
        file_handle.writelines(versiondata)
        file_handle.close()
        return

    def _setup_canvas(self, canvas):
        """ Initialize the turtle art canvas. """
        bundle_path = activity.get_bundle_path()
        self.tw = TurtleArtWindow(canvas, bundle_path, self,
                                  profile.get_color().to_string(),
                                  profile.get_nick_name())
        # self.tw.activity = self
        self.tw.window.grab_focus()
        path = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'], 'data')
        self.tw.save_folder = path

        if self._jobject and self._jobject.file_path:
            self.read_file(self._jobject.file_path)
        else: # if new, load a start brick onto the canvas
            self.tw.load_start()

    def _load_python_code(self):
        """ Check to see if there is Python code to be loaded. """
        try:
            dsobject = datastore.get(self.metadata['python code'])
            self._load_python(dsobject)
        except:
            pass

    def _setup_sharing(self):
        """ A simplistic sharing model: the sharer is the master """
        # TODO: hand off role of master is sharer leaves
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

    def _setup_visibility_handler(self):
        """ Notify when the visibility state changes """
        self.add_events(gtk.gdk.VISIBILITY_NOTIFY_MASK)
        self.connect("visibility-notify-event", self.__visibility_notify_cb)

    def write_file(self, file_path):
        """ Write the project to the Journal. """
        _logger.debug("Write file: %s" % file_path)
        self.metadata['mime_type'] = 'application/x-turtle-art'
        data_to_file(self.tw.assemble_data_to_save(), file_path)

    def read_file(self, file_path, run_it=True):
        """ Read a project in and then run it. """
        import tarfile
        import os
        import tempfile
        import shutil

        if hasattr(self, 'tw'):
            _logger.debug("Read file: %s" % (file_path))
            # Could be a gtar (newer builds) or tar (767) file
            if file_path.endswith(('.gtar', '.tar')):
                tar_fd = tarfile.open(file_path, 'r')
                tmpdir = tempfile.mkdtemp()
                try:
                    # We'll get 'ta_code.ta' and possibly a 'ta_image.png'
                    # but we will ignore the .png file
                    # If run_it is True, we want to create a new project
                    tar_fd.extractall(tmpdir)
                    self.tw.load_files(os.path.join(tmpdir, 'ta_code.ta'), \
                                        run_it) # create a new project flag
                finally:
                    shutil.rmtree(tmpdir)
                    tar_fd.close()
            # Otherwise, assume it is a .ta file
            else:
                _logger.debug("trying to open a .ta file:" + file_path)
                self.tw.load_files(file_path, run_it)

            # run the activity
            if run_it:
                self.stop_turtle_button.set_icon("stopiton")
                self.tw.run_button(0)
        else:
            _logger.debug("Deferring reading file %s" % (file_path))

    def jobject_new_patch(self):
        """ Save instance to Journal. """
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

    def _copy_cb(self, button):
        clipBoard = gtk.Clipboard()
        _logger.debug("serialize the project and copy to clipboard")
        data = self.tw.assemble_data_to_save(False, False)
        if data is not []:
            text = data_to_string(data)
            clipBoard.set_text(text)
        self.tw.paste_offset = 20

    def _paste_cb(self, button):
        clipBoard = gtk.Clipboard()
        _logger.debug("paste to the project")
        text = clipBoard.wait_for_text()
        if text is not None:
            if self.tw.selected_blk is not None and \
               self.tw.selected_blk.name == 'string':
                for i in text:
                    self.tw.process_alphanumeric_input(i, -1)
                self.tw.selected_blk.resize()
            else:
                self.tw.process_data(data_from_string(text),
                                     self.tw.paste_offset)
                self.tw.paste_offset += 20


class ChatTube(ExportedGObject):

    def __init__(self, tube, is_initiator, stack_received_cb):
        """Class for setting up tube for sharing."""
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
