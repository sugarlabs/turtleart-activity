#Copyright (c) 2007, Playful Invention Company
#Copyright (c) 2008-12, Walter Bender
#Copyright (c) 2009-10 Raul Gutierrez Segales
#Copyright (c) 2012 Alan Aguiar

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
import cairo
import gobject
import dbus

import logging
_logger = logging.getLogger('turtleart-activity')

from sugar.activity import activity
try:  # 0.86 toolbar widgets
    from sugar.activity.widgets import ActivityToolbarButton, StopButton
    from sugar.graphics.toolbarbox import ToolbarBox, ToolbarButton
    HAS_TOOLBARBOX = True
except ImportError:
    HAS_TOOLBARBOX = False
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.graphics.alert import ConfirmationAlert, NotifyAlert
from sugar.graphics import style
from sugar.datastore import datastore
from sugar import profile

import os
import tarfile
import subprocess
import ConfigParser
import shutil
import tempfile

# installs the global _() magic (reverted as it is broken)
# import TurtleArt.tagettext
from gettext import gettext as _

from TurtleArt.tapalette import palette_names, help_strings, help_palettes, \
                                help_windows
from TurtleArt.taconstants import ICON_SIZE, BLOCK_SCALE, XO1, XO15, XO175, \
                                  XO30
from TurtleArt.taexporthtml import save_html
from TurtleArt.taexportlogo import save_logo
from TurtleArt.tautils import data_to_file, data_to_string, data_from_string, \
                              get_path, chooser, get_hardware
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.tacollaboration import Collaboration

if HAS_TOOLBARBOX:
    from util.helpbutton import HelpButton, add_section, add_paragraph


class TurtleArtActivity(activity.Activity):
    ''' Activity subclass for Turtle Art '''

    def __init__(self, handle):
        ''' Set up the toolbars, canvas, sharing, etc. '''
        try:
            super(TurtleArtActivity, self).__init__(handle)
        except dbus.exceptions.DBusException, e:
            _logger.error(str(e))

        self._check_ver_change(get_path(activity, 'data'))
        self._setup_visibility_handler()

        self.has_toolbarbox = HAS_TOOLBARBOX
        _logger.debug('_setup_toolbar')
        self._setup_toolbar()

        _logger.debug('_setup_canvas')
        self._canvas = self._setup_canvas(self._setup_scrolled_window())

        # FIX ME: not sure how or why self.canvas gets overwritten
        # It is set to self.sw in _setup_canvas but None here.
        # We need self.canvas for generating the preview image
        self.canvas = self.sw

        _logger.debug('_setup_palette_toolbar')
        self._setup_palette_toolbar()
        self._setup_extra_controls()

        _logger.debug('_setup_sharing')
        self._setup_sharing()

        # Activity count is the number of times this instance has been
        # accessed
        count = 1
        if hasattr(self, 'metadata') and self.metadata is not None:
            if 'activity count' in self.metadata:
                count = int(self.metadata['activity count'])
                count += 1
            self.metadata['activity count'] = str(count)

        self._defer_palette_move = False

    # Activity toolbar callbacks

    def do_save_as_html_cb(self, button):
        ''' Write html out to datastore. '''
        self.save_as_html.set_icon('htmlon')
        _logger.debug('saving HTML code')
        # Until we have URLs for datastore objects, always embed images.
        embed_flag = True

        # Generate HTML by processing TA code from stacks.
        html = save_html(self, self.tw, embed_flag)
        if len(html) == 0:
            return

        # Save the HTML code to the instance directory.
        datapath = get_path(activity, 'instance')

        save_type = '.html'
        if len(self.tw.saved_pictures) > 0:
            if self.tw.saved_pictures[0][1]:  # svg=True
                save_type = '.xml'

        html_file = os.path.join(datapath, 'portfolio' + save_type)
        f = file(html_file, 'w')
        f.write(html)
        f.close()

        if not embed_flag:
            # We need to make a tar ball that includes the images.
            tar_path = os.path.join(datapath, 'portfolio.tar')
            tar_fd = tarfile.open(tar_path, 'w')
            try:
                tar_fd.add(html_file, 'portfolio.html')
                import glob
                image_list = glob.glob(os.path.join(datapath, 'image*'))
                for i in image_list:
                    tar_fd.add(i, os.path.basename(i))
            finally:
                tar_fd.close()

        dsobject = datastore.create()
        dsobject.metadata['title'] = self.metadata['title'] + ' ' + \
                                     _('presentation')
        dsobject.metadata['icon-color'] = profile.get_color().to_string()
        if embed_flag:
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

        gobject.timeout_add(250, self.save_as_html.set_icon, 'htmloff')

        self.tw.saved_pictures = []  # Clear queue of pictures we have viewed.
        if embed_flag:
            os.remove(html_file)
        else:
            os.remove(tar_file)

        self._notify_successful_save(title=_('Save as HTML'))

    def do_save_as_logo_cb(self, button):
        ''' Write UCB logo code to datastore. '''
        self.save_as_logo.set_icon('logo-saveon')
        logo_code_path = self._dump_logo_code()
        if logo_code_path is None:
            return

        dsobject = datastore.create()
        dsobject.metadata['title'] = self.metadata['title'] + '.lg'
        dsobject.metadata['mime_type'] = 'text/plain'
        dsobject.metadata['icon-color'] = profile.get_color().to_string()
        dsobject.set_file_path(logo_code_path)
        datastore.write(dsobject)
        dsobject.destroy()

        os.remove(logo_code_path)
        gobject.timeout_add(250, self.save_as_logo.set_icon, 'logo-saveoff')
        self._notify_successful_save(title=_('Save as Logo'))

    def do_load_ta_project_cb(self, button):
        ''' Load a project from the Journal. '''
        chooser(self, 'org.laptop.TurtleArtActivity', self._load_ta_project)

    def _load_ta_project(self, dsobject):
        ''' Load a TA project from the datastore. '''
        try:
            _logger.debug('Opening %s ' % dsobject.file_path)
            self.read_file(dsobject.file_path, run_it=False, plugin=False)
        except:
            _logger.debug("Couldn't open %s" % dsobject.file_path)

    def do_load_ta_plugin_cb(self, button):
        ''' Load a plugin from the Journal. '''
        # FIXME: we are looking for tar files
        chooser(self, '', self._load_ta_plugin)

    def _load_ta_plugin(self, dsobject):
        ''' Load a TA plugin from the datastore. '''
        _logger.debug('Opening %s ' % dsobject.file_path)
        self.read_file(dsobject.file_path, run_it=False, plugin=True)

    def do_load_python_cb(self, button):
        ''' Load Python code from the Journal. '''
        self.load_python.set_icon('pippy-openon')
        self.tw.load_python_code_from_file(fname=None, add_new_block=True)
        gobject.timeout_add(250, self.load_python.set_icon, 'pippy-openoff')

    def do_save_as_image_cb(self, button):
        ''' Save the canvas to the Journal. '''
        self.save_as_image.set_icon('image-saveon')
        _logger.debug('saving image to journal')

        self.tw.save_as_image()
        gobject.timeout_add(250, self.save_as_image.set_icon, 'image-saveoff')
        self._notify_successful_save(title=_('Save as image'))

    def do_keep_cb(self, button):
        ''' Save a snapshot of the project to the Journal. '''
        tmpfile = self._dump_ta_code()
        if tmpfile is not None:
            dsobject = datastore.create()
            dsobject.metadata['title'] = self.metadata['title'] + ' ' + \
                _('snapshot')
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'application/x-turtle-art'
            dsobject.metadata['activity'] = 'org.laptop.TurtleArtActivity'
            dsobject.set_file_path(tmpfile)
            datastore.write(dsobject)
            dsobject.destroy()
            os.remove(tmpfile)
            self._notify_successful_save(title=_('Save snapshot'))

    # Main/palette toolbar button callbacks

    def do_palette_cb(self, button):
        ''' Show/hide palette '''
        if self.tw.palette:
            self.tw.hideshow_palette(False)
            self.do_hidepalette()
            if self.has_toolbarbox and self.tw.selected_palette is not None:
                self.palette_buttons[self.tw.selected_palette].set_icon(
                    palette_names[self.tw.selected_palette] + 'off')
        else:
            self.tw.hideshow_palette(True)
            self.do_showpalette()
            if self.has_toolbarbox:
                self.palette_buttons[0].set_icon(palette_names[0] + 'on')

    def do_palette_buttons_cb(self, button, i):
        ''' Palette selector buttons '''
        if self.tw.selected_palette is not None:
            if not self.has_toolbarbox:
                self.palette_buttons[self.tw.selected_palette].set_icon(
                    palette_names[self.tw.selected_palette] + 'off')
            if self.tw.selected_palette == i:
                # Hide the palette if it is already selected.
                self.tw.hideshow_palette(False)
                self.tw.selected_palette = None
                return
        if not self.has_toolbarbox:
            self.palette_buttons[i].set_icon(palette_names[i] + 'on')
        else:
            self._help_button.set_current_palette(palette_names[i])
        self.tw.show_palette(n=i)
        self.do_showpalette()

    def _do_hover_help_toggle(self, button):
        ''' Toggle hover help '''
        if self.tw.no_help:
            self.tw.no_help = False
            self._hover_help_toggle.set_icon('help-off')
            self._hover_help_toggle.set_tooltip(_('Turn off hover help'))
        else:
            self.tw.no_help = True
            self.tw.last_label = None
            self.tw.status_spr.hide()
            self._hover_help_toggle.set_icon('help-on')
            self._hover_help_toggle.set_tooltip(_('Turn on hover help'))

    # These methods are called both from toolbar buttons and blocks.

    def do_hidepalette(self):
        ''' Hide the palette. '''
        if hasattr(self, 'palette_button'):
            self.palette_button.set_icon('paletteon')
            self.palette_button.set_tooltip(_('Show palette'))

    def do_showpalette(self):
        ''' Show the palette. '''
        if hasattr(self, 'palette_button'):
            self.palette_button.set_icon('paletteoff')
            self.palette_button.set_tooltip(_('Hide palette'))

    def do_hide_blocks(self):
        ''' Hide blocks. '''
        self.do_hidepalette()

    def do_show_blocks(self):
        ''' Show blocks. '''
        self.do_showpalette()

    def do_eraser_cb(self, button):
        ''' Clear the screen and recenter. '''
        self.eraser_button.set_icon('eraseroff')
        self.recenter()
        self.tw.eraser_button()
        gobject.timeout_add(250, self.eraser_button.set_icon, 'eraseron')

    def do_run_cb(self, button):
        ''' Callback for run button (rabbit) '''
        self.run_button.set_icon('run-faston')
        self.tw.lc.trace = 0
        # Autohide blocks and palettes on run
        self.tw.hideblocks()
        self.tw.run_button(0, running_from_button_push=True)
        gobject.timeout_add(1000, self.run_button.set_icon, 'run-fastoff')

    def do_step_cb(self, button):
        ''' Callback for step button (turtle) '''
        self.step_button.set_icon('run-slowon')
        self.tw.lc.trace = 1
        self.tw.run_button(3, running_from_button_push=True)
        gobject.timeout_add(1000, self.step_button.set_icon, 'run-slowoff')

    def do_debug_cb(self, button):
        ''' Callback for debug button (bug) '''
        self.debug_button.set_icon('debugon')
        self.tw.lc.trace = 1
        self.tw.run_button(9, running_from_button_push=True)
        gobject.timeout_add(1000, self.debug_button.set_icon, 'debugoff')

    def do_stop_cb(self, button):
        ''' Callback for stop button. '''
        self.stop_turtle_button.set_icon('stopitoff')
        self.stop_turtle_button.set_tooltip(_('Stop turtle'))
        self.tw.stop_button()
        # Auto show blocks after stop
        self.tw.showblocks()
        self.step_button.set_icon('run-slowoff')
        self.run_button.set_icon('run-fastoff')

    def do_samples_cb(self, button):
        ''' Sample-projects open dialog '''
        self.tw.load_file(True)

    def adjust_sw(self, dx, dy):
        ''' Adjust the scrolled window position. '''
        hadj = self.sw.get_hadjustment()
        hvalue = hadj.get_value() + dx
        if hvalue < hadj.get_lower():
            hvalue = hadj.get_lower()
        elif hvalue > hadj.get_upper():
            hvalue = hadj.get_upper()
        hadj.set_value(hvalue)
        self.sw.set_hadjustment(hadj)
        vadj = self.sw.get_vadjustment()
        vvalue = vadj.get_value() + dy
        if vvalue < vadj.get_lower():
            vvalue = vadj.get_lower()
        elif vvalue > vadj.get_upper():
            vvalue = vadj.get_upper()
        vadj.set_value(vvalue)
        self.sw.set_vadjustment(vadj)
        self._defer_palette_move = True

    def adjust_palette(self):
        ''' Align palette to scrolled window position. '''
        if not self.tw.hw in [XO1]:
            self.tw.move_palettes(self.sw.get_hadjustment().get_value(),
                                  self.sw.get_vadjustment().get_value())
        self._defer_palette_move = False

    def recenter(self):
        ''' Recenter scrolled window around canvas. '''
        self.hadj_value = 0
        hadj = self.sw.get_hadjustment()
        hadj.set_value(self.hadj_value)
        self.sw.set_hadjustment(hadj)
        self.vadj_value = 0
        vadj = self.sw.get_vadjustment()
        vadj.set_value(self.vadj_value)
        self.sw.set_vadjustment(vadj)
        self.adjust_palette()

    def do_fullscreen_cb(self, button):
        ''' Hide the Sugar toolbars. '''
        self.fullscreen()
        self.recenter()

    def do_grow_blocks_cb(self, button):
        ''' Grow the blocks. '''
        self.do_resize_blocks(1)

    def do_shrink_blocks_cb(self, button):
        ''' Shrink the blocks. '''
        self.do_resize_blocks(-1)

    def do_resize_blocks(self, inc):
        ''' Scale the blocks. '''
        if self.tw.block_scale in BLOCK_SCALE:
            i = BLOCK_SCALE.index(self.tw.block_scale) + inc
        else:
            i = BLOCK_SCALE[3]  # 2.0
        if i < 0:
            self.tw.block_scale = BLOCK_SCALE[0]
        elif i == len(BLOCK_SCALE):
            self.tw.block_scale = BLOCK_SCALE[-1]
        else:
            self.tw.block_scale = BLOCK_SCALE[i]
        self.tw.resize_blocks()

    def do_cartesian_cb(self, button):
        ''' Display Cartesian-coordinate grid. '''
        if self.tw.cartesian:
            self.tw.set_cartesian(False)
        else:
            self.tw.set_cartesian(True)

    def do_polar_cb(self, button):
        ''' Display polar-coordinate grid. '''
        if self.tw.polar:
            self.tw.set_polar(False)
        else:
            self.tw.set_polar(True)

    def do_metric_cb(self, button):
        ''' Display metric-coordinate grid. '''
        if self.tw.metric:
            self.tw.set_metric(False)
        else:
            self.tw.set_metric(True)

    def do_rescale_cb(self, button):
        ''' Rescale coordinate system (100==height/2 or 100 pixels). '''
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height / 200
            self.rescale_button.set_icon('contract-coordinates')
            self.rescale_button.set_tooltip(_('Rescale coordinates down'))
        else:
            self.tw.coord_scale = 1
            self.rescale_button.set_icon('expand-coordinates')
            self.rescale_button.set_tooltip(_('Rescale coordinates up'))
        self.tw.eraser_button()
        # Given the change in how overlays are handled (v123), there is no way
        # to erase and then redraw the overlays.

    def get_document_path(self, async_cb, async_err_cb):
        '''  View TA code as part of view source.  '''
        ta_code_path = self._dump_ta_code()
        if ta_code_path is not None:
            async_cb(ta_code_path)

    def _dump_logo_code(self):
        '''  Save Logo code to temporary file. '''
        datapath = get_path(activity, 'instance')
        tmpfile = os.path.join(datapath, 'tmpfile.lg')
        code = save_logo(self.tw)
        if len(code) == 0:
            _logger.debug('save_logo returned None')
            return None
        try:
            f = file(tmpfile, 'w')
            f.write(code)
            f.close()
        except Exception, e:
            _logger.error("Couldn't save Logo code: " + str(e))
            tmpfile = None
        return tmpfile

    def _dump_ta_code(self):
        '''  Save TA code to temporary file. '''
        datapath = get_path(activity, 'instance')
        tmpfile = os.path.join(datapath, 'tmpfile.ta')
        try:
            data_to_file(self.tw.assemble_data_to_save(), tmpfile)
        except Exception, e:
            _logger.error("Couldn't save project code: " + str(e))
            tmpfile = None
        return tmpfile

    def __visibility_notify_cb(self, window, event):
        ''' Callback method for when the activity's visibility changes. '''
        if event.state == gtk.gdk.VISIBILITY_FULLY_OBSCURED:
            self.tw.background_plugins()
        elif event.state in \
            [gtk.gdk.VISIBILITY_UNOBSCURED, gtk.gdk.VISIBILITY_PARTIAL]:
            self.tw.foreground_plugins()

    def _keep_clicked_cb(self, button):
        ''' Keep-button clicked. '''
        self.jobject_new_patch()

    def _setup_toolbar(self):
        ''' Setup toolbar according to Sugar version. '''
        if self.has_toolbarbox:
            self._setup_toolbar_help()
            self._toolbox = ToolbarBox()

            self.activity_toolbar_button = ActivityToolbarButton(self)

            edit_toolbar = gtk.Toolbar()
            self.edit_toolbar_button = ToolbarButton(label=_('Edit'),
                                                page=edit_toolbar,
                                                icon_name='toolbar-edit')

            view_toolbar = gtk.Toolbar()
            self.view_toolbar_button = ToolbarButton(label=_('View'),
                                                page=view_toolbar,
                                                icon_name='toolbar-view')
            self._palette_toolbar = gtk.Toolbar()
            self.palette_toolbar_button = ToolbarButton(
                page=self._palette_toolbar, icon_name='palette')

            self._help_button = HelpButton(self)

            self._make_load_save_buttons(self.activity_toolbar_button)

            self.activity_toolbar_button.show()
            self._toolbox.toolbar.insert(self.activity_toolbar_button, -1)
            self.edit_toolbar_button.show()
            self._toolbox.toolbar.insert(self.edit_toolbar_button, -1)
            self.view_toolbar_button.show()
            self._toolbox.toolbar.insert(self.view_toolbar_button, -1)
            self.palette_toolbar_button.show()
            self._toolbox.toolbar.insert(self.palette_toolbar_button, -1)

            self.set_toolbar_box(self._toolbox)
            self.palette_toolbar_button.set_expanded(True)
        else:
            self._toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self._toolbox)

            self._project_toolbar = gtk.Toolbar()
            self._toolbox.add_toolbar(_('Project'), self._project_toolbar)
            view_toolbar = gtk.Toolbar()
            self._toolbox.add_toolbar(_('View'), view_toolbar)
            edit_toolbar = gtk.Toolbar()
            self._toolbox.add_toolbar(_('Edit'), edit_toolbar)
            journal_toolbar = gtk.Toolbar()
            self._toolbox.add_toolbar(_('Save/Load'), journal_toolbar)

            self._make_palette_buttons(self._project_toolbar,
                                       palette_button=True)

            self._add_separator(self._project_toolbar)
            self._make_load_save_buttons(journal_toolbar)

        self._add_button('edit-copy', _('Copy'), self._copy_cb,
                         edit_toolbar, '<Ctrl>c')
        self._add_button('edit-paste', _('Paste'), self._paste_cb,
                         edit_toolbar, '<Ctrl>v')
        self._add_button('view-fullscreen', _('Fullscreen'),
                         self.do_fullscreen_cb, view_toolbar, '<Alt>Return')
        self._add_button('view-Cartesian', _('Cartesian coordinates'),
                         self.do_cartesian_cb, view_toolbar)
        self._add_button('view-polar', _('Polar coordinates'),
                         self.do_polar_cb, view_toolbar)
        if get_hardware() in [XO1, XO15, XO175]:
            self._add_button('view-metric', _('Metric coordinates'),
                             self.do_metric_cb, view_toolbar)
        self._add_separator(view_toolbar, visible=False)
        self.coordinates_label = self._add_label(_('xcor') + ' = 0 ' + \
            _('ycor') + ' = 0 ' + _('heading') + ' = 0', view_toolbar)
        self._add_separator(view_toolbar, expand=True, visible=False)
        self.rescale_button = self._add_button(
            'expand-coordinates', _('Rescale coordinates up'),
            self.do_rescale_cb, view_toolbar)
        self.resize_up_button = self._add_button(
            'resize+', _('Grow blocks'), self.do_grow_blocks_cb, view_toolbar)
        self.resize_down_button = self._add_button(
            'resize-', _('Shrink blocks'), self.do_shrink_blocks_cb,
            view_toolbar)
        self._hover_help_toggle = self._add_button(
            'help-off', _('Turn off hover help'), self._do_hover_help_toggle,
            view_toolbar)

        edit_toolbar.show()
        view_toolbar.show()
        self._toolbox.show()

        if not self.has_toolbarbox:
            self._toolbox.set_current_toolbar(1)

    def _setup_extra_controls(self):
        ''' Add the rest of the buttons to the main toolbar '''
        if not self.has_toolbarbox:
            self._make_project_buttons(self._project_toolbar)
            return

        self._make_project_buttons(self._toolbox.toolbar)

        if not self.tw.hw in [XO30]:
            self._add_separator(self._toolbox.toolbar, expand=True,
                                visible=False)

        self.samples_button = self._add_button(
            'ta-open', _('Load example'), self.do_samples_cb,
            self._toolbox.toolbar)

        self._toolbox.toolbar.insert(self._help_button, -1)
        self._help_button.show()

        stop_button = StopButton(self)
        stop_button.props.accelerator = '<Ctrl>Q'
        self._toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

    def _setup_toolbar_help(self):
        ''' Set up a help palette for the main toolbars '''
        help_box = gtk.VBox()
        help_box.set_homogeneous(False)
        help_palettes['main-toolbar'] = help_box
        help_windows['main-toolbar'] = gtk.ScrolledWindow()
        help_windows['main-toolbar'].set_size_request(
            int(gtk.gdk.screen_width() / 3),
            gtk.gdk.screen_height() - style.GRID_CELL_SIZE * 3)
        help_windows['main-toolbar'].set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        help_windows['main-toolbar'].add_with_viewport(
            help_palettes['main-toolbar'])
        help_palettes['main-toolbar'].show()

        add_section(help_box, _('Save/Load'), icon='turtleoff')
        add_section(help_box, _('Edit'), icon='toolbar-edit')
        add_section(help_box, _('View'), icon='toolbar-view')
        add_section(help_box, _('Project'), icon='palette')
        add_paragraph(help_box, _('Clean'), icon='eraseron')
        add_paragraph(help_box, _('Run'), icon='run-fastoff')
        add_paragraph(help_box, _('Step'), icon='run-slowoff')
        add_paragraph(help_box, _('Debug'), icon='debugoff')
        add_paragraph(help_box, _('Stop turtle'), icon='stopitoff')
        add_paragraph(help_box, _('Show blocks'), icon='hideshowoff')
        add_paragraph(help_box, _('Load example'), icon='ta-open')
        add_paragraph(help_box, _('Help'), icon='help-toolbar')
        add_paragraph(help_box, _('Stop'), icon='activity-stop')

        help_box = gtk.VBox()
        help_box.set_homogeneous(False)
        help_palettes['activity-toolbar'] = help_box
        help_windows['activity-toolbar'] = gtk.ScrolledWindow()
        help_windows['activity-toolbar'].set_size_request(
            int(gtk.gdk.screen_width() / 3),
            gtk.gdk.screen_height() - style.GRID_CELL_SIZE * 3)
        help_windows['activity-toolbar'].set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        help_windows['activity-toolbar'].add_with_viewport(
            help_palettes['activity-toolbar'])
        help_palettes['activity-toolbar'].show()

        if gtk.gdk.screen_width() < 1200:
            add_paragraph(help_box, _('Save/Load'), icon='save-load')
        else:
            add_section(help_box, _('Save/Load'), icon='turtleoff')
        add_paragraph(help_box, _('Save as image'), icon='image-saveoff')
        add_paragraph(help_box, _('Save as HTML'), icon='htmloff')
        add_paragraph(help_box, _('Save as Logo'), icon='logo-saveoff')
        add_paragraph(help_box, _('Save snapshot'), icon='filesaveoff')
        add_paragraph(help_box, _('Load project'), icon='load-from-journal')
        home = os.environ['HOME']
        if activity.get_bundle_path()[0:len(home)] == home:
            add_paragraph(help_box, _('Load plugin'), icon='pluginoff')
        add_paragraph(help_box, _('Load Python block'),
                      icon='pippy-openoff')

        help_box = gtk.VBox()
        help_box.set_homogeneous(False)
        help_palettes['edit-toolbar'] = help_box
        help_windows['edit-toolbar'] = gtk.ScrolledWindow()
        help_windows['edit-toolbar'].set_size_request(
            int(gtk.gdk.screen_width() / 3),
            gtk.gdk.screen_height() - style.GRID_CELL_SIZE * 3)
        help_windows['edit-toolbar'].set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        help_windows['edit-toolbar'].add_with_viewport(
            help_palettes['edit-toolbar'])
        help_palettes['edit-toolbar'].show()

        add_section(help_box, _('Edit'), icon='toolbar-edit')
        add_paragraph(help_box, _('Copy'), icon='edit-copy')
        add_paragraph(help_box, _('Paste'), icon='edit-paste')

        help_box = gtk.VBox()
        help_box.set_homogeneous(False)
        help_palettes['view-toolbar'] = help_box
        help_windows['view-toolbar'] = gtk.ScrolledWindow()
        help_windows['view-toolbar'].set_size_request(
            int(gtk.gdk.screen_width() / 3),
            gtk.gdk.screen_height() - style.GRID_CELL_SIZE * 3)
        help_windows['view-toolbar'].set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        help_windows['view-toolbar'].add_with_viewport(
            help_palettes['view-toolbar'])
        help_palettes['view-toolbar'].show()

        add_section(help_box, _('View'), icon='toolbar-view')
        add_paragraph(help_box, _('Fullscreen'), icon='view-fullscreen')
        add_paragraph(help_box, _('Cartesian coordinates'),
                      icon='view-Cartesian')
        add_paragraph(help_box, _('Polar coordinates'), icon='view-polar')
        if get_hardware() in [XO1, XO15, XO175]:
            add_paragraph(help_box, _('Metric coordinates'),
                          icon='view-metric')
        add_paragraph(help_box, _('Rescale coordinates up'),
                           icon='expand-coordinates')
        add_paragraph(help_box, _('Grow blocks'), icon='resize+')
        add_paragraph(help_box, _('Shrink blocks'), icon='resize-')
        add_paragraph(help_box, _('Turn off hover help'), icon='help-off')

    def _setup_palette_toolbar(self):
        ''' The palette toolbar must be setup *after* plugins are loaded. '''
        if self.has_toolbarbox:
            self.palette_buttons = []
            for i, palette_name in enumerate(palette_names):
                if i == 0:
                    palette_group = None
                else:
                    palette_group = self.palette_buttons[0]
                _logger.debug('palette_buttons.append %s', palette_name)
                self.palette_buttons.append(self._radio_button_factory(
                        palette_name + 'off',
                        self._palette_toolbar,
                        self.do_palette_buttons_cb, i,
                        help_strings[palette_name],
                        palette_group))
            if self.tw.hw in [XO1, XO15, XO175]:
                self._add_separator(self._palette_toolbar, expand=True,
                                    visible=False)
            self._make_palette_buttons(self._palette_toolbar)
            self._palette_toolbar.show()

    def _make_load_save_buttons(self, toolbar):
        ''' Additional toolbar buttons for file IO '''
        home = os.environ['HOME']
        if self.has_toolbarbox and gtk.gdk.screen_width() < 1200:
            save_load_button = self._add_button(
                'save-load', _('Save/Load'), self._save_load_palette_cb,
                toolbar)
            self._palette = save_load_button.get_palette()
            button_box = gtk.VBox()
            self.save_as_image = self._add_button_and_label(
                'image-saveoff', _('Save as image'), self.do_save_as_image_cb,
                button_box)
            self.save_as_html = self._add_button_and_label(
                'htmloff', _('Save as HTML'), self.do_save_as_html_cb,
                button_box)
            self.save_as_logo = self._add_button_and_label(
                'logo-saveoff', _('Save as Logo'), self.do_save_as_logo_cb,
                button_box)
            self.keep_button = self._add_button_and_label(
                'filesaveoff', _('Save snapshot'), self.do_keep_cb, button_box)
            self.load_ta_project = self._add_button_and_label(
                'load-from-journal', _('Load project'),
                self.do_load_ta_project_cb, button_box)
            # Only enable plugin loading if installed in $HOME
            if activity.get_bundle_path()[0:len(home)] == home:
                self.load_ta_plugin = self._add_button_and_label(
                    'pluginoff', _('Load plugin'),
                    self.do_load_ta_plugin_cb, button_box)
            self.load_python = self._add_button_and_label(
                'pippy-openoff', _('Load Python block'),
                self.do_load_python_cb, button_box)
            button_box.show_all()
            self._palette.set_content(button_box)
        else:
            self.save_as_image = self._add_button(
                'image-saveoff', _('Save as image'), self.do_save_as_image_cb,
                toolbar)
            self.save_as_html = self._add_button(
                'htmloff', _('Save as HTML'), self.do_save_as_html_cb, toolbar)
            self.save_as_logo = self._add_button(
                'logo-saveoff', _('Save as Logo'), self.do_save_as_logo_cb,
                toolbar)
            self.keep_button = self._add_button(
                'filesaveoff', _('Save snapshot'), self.do_keep_cb, toolbar)
            self._add_separator(toolbar)
            self.load_ta_project = self._add_button(
                'load-from-journal', _('Load project'),
                self.do_load_ta_project_cb, toolbar)
            # Only enable plugin loading if installed in $HOME
            if activity.get_bundle_path()[0:len(home)] == home:
                self.load_ta_plugin = self._add_button(
                    'pluginoff', _('Load plugin'),
                    self.do_load_ta_plugin_cb, toolbar)
            self.load_python = self._add_button(
                'pippy-openoff', _('Load Python block'),
                self.do_load_python_cb, toolbar)

    def _save_load_palette_cb(self, button):
        if self._palette:
            if not self._palette.is_up():
                self._palette.popup(immediate=True,
                                    state=self._palette.SECONDARY)
            else:
                self._palette.popdown(immediate=True)
            return

    def _make_palette_buttons(self, toolbar, palette_button=False):
        ''' Creates the palette and block buttons for both toolbar types'''
        if palette_button:  # old-style toolbars need this button
            self.palette_button = self._add_button(
                'paletteoff', _('Hide palette'), self.do_palette_cb,
                toolbar, _('<Ctrl>p'))

    def _make_project_buttons(self, toolbar):
        ''' Creates the turtle buttons for both toolbar types'''
        self.eraser_button = self._add_button(
            'eraseron', _('Clean'), self.do_eraser_cb, toolbar, _('<Ctrl>e'))
        self.run_button = self._add_button(
            'run-fastoff', _('Run'), self.do_run_cb, toolbar, _('<Ctrl>r'))
        self.step_button = self._add_button(
            'run-slowoff', _('Step'), self.do_step_cb, toolbar, _('<Ctrl>w'))
        if self.tw.hw not in [XO30]:
            self.debug_button = self._add_button(
                'debugoff', _('Debug'), self.do_debug_cb, toolbar,
                _('<Ctrl>d'))
        self.stop_turtle_button = self._add_button(
            'stopitoff', _('Stop turtle'), self.do_stop_cb, toolbar,
            _('<Ctrl>s'))

    def _check_ver_change(self, datapath):
        ''' Check to see if the version has changed. '''
        # We don't do anything with this info at the moment.
        try:
            version = os.environ['SUGAR_BUNDLE_VERSION']
        except KeyError:
            version = 'unknown'

        filename = 'version.dat'
        version_data = []
        new_version = True
        try:
            file_handle = open(os.path.join(datapath, filename), 'r')
            if file_handle.readline() == version:
                new_version = False
            file_handle.close()
        except IOError:
            _logger.debug("Couldn't read version number.")

        version_data.append(version)
        try:
            file_handle = open(os.path.join(datapath, filename), 'w')
            file_handle.writelines(version_data)
            file_handle.close()
        except IOError:
            _logger.debug("Couldn't write version number.")

        return new_version

    def _setup_scrolled_window(self):
        ''' Create a scrolled window to contain the turtle canvas. '''
        self.sw = gtk.ScrolledWindow()
        self.set_canvas(self.sw)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.show()

        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width() * 2,
                                gtk.gdk.screen_height() * 2)
        self.sw.add_with_viewport(canvas)
        hadj = self.sw.get_hadjustment()
        hadj.connect('value-changed', self._scroll_cb)
        vadj = self.sw.get_vadjustment()
        vadj.connect('value-changed', self._scroll_cb)
        self.hadj_value = 0
        self.vadj_value = 0
        canvas.show()
        self.sw.show()
        self.show_all()
        return canvas

    def _scroll_cb(self, window):
        ''' The scrolling window has been changed, so move the
        floating palettes. '''
        hadj = self.sw.get_hadjustment()
        self.hadj_value = hadj.get_value()
        vadj = self.sw.get_vadjustment()
        self.vadj_value = vadj.get_value()
        if not self.tw.hw in [XO1] and not self._defer_palette_move:
            gobject.idle_add(self.tw.move_palettes, self.hadj_value,
                             self.vadj_value)

    def _setup_canvas(self, canvas_window):
        ''' Initialize the turtle art canvas. '''
        #win = canvas_window.get_window()  # self._canvas.get_window()
        win = canvas_window.window
        cr = win.cairo_create()
        surface = cr.get_target()
        self.turtle_canvas = surface.create_similar(
            cairo.CONTENT_COLOR, gtk.gdk.screen_width() * 2,
            gtk.gdk.screen_height() * 2)
        bundle_path = activity.get_bundle_path()
        self.tw = TurtleArtWindow(canvas_window, bundle_path, self,
                                  mycolors=profile.get_color().to_string(),
                                  mynick=profile.get_nick_name(),
                                  turtle_canvas=self.turtle_canvas)
        self.tw.window.grab_focus()
        self.tw.save_folder = os.path.join(
            os.environ['SUGAR_ACTIVITY_ROOT'], 'data')

        # Try restoring an existing project...
        if self._jobject and self._jobject.file_path:
            self.read_file(self._jobject.file_path)
        else:  # ...or else, load a Start Block onto the canvas.
            self.tw.load_start()

    def _setup_sharing(self):
        ''' Setup the Collabora stack. '''
        self._collaboration = Collaboration(self.tw, self)
        self._collaboration.setup()

    def send_xy(self):
        ''' Resync xy position (and orientation) of my turtle. '''
        self._collaboration.send_my_xy()

    def _setup_visibility_handler(self):
        ''' Notify me when the visibility state changes. '''
        self.add_events(gtk.gdk.VISIBILITY_NOTIFY_MASK)
        self.connect('visibility-notify-event', self.__visibility_notify_cb)

    def can_close(self):
        ''' Override activity class can_close inorder to notify plugins '''
        self.tw.quit_plugins()
        return True

    def write_file(self, file_path):
        ''' Write the project to the Journal. '''
        data_to_file(self.tw.assemble_data_to_save(), file_path)
        self.metadata['mime_type'] = 'application/x-turtle-art'
        self.metadata['turtle blocks'] = ''.join(self.tw.used_block_list)
        self.metadata['public'] = data_to_string(['activity count',
                                                  'turtle blocks'])
        _logger.debug('Wrote to file: %s' % file_path)

    def _load_a_plugin(self, tmp_dir):
        ''' Load a plugin from the Journal and initialize it '''
        plugin_path = os.path.join(tmp_dir, 'plugin.info')
        _logger.debug(plugin_path)
        file_info = ConfigParser.ConfigParser()
        if len(file_info.read(plugin_path)) == 0:
            _logger.debug('Required file plugin.info could not be found.')
            self.tw.showlabel('status',
                              label=_('Plugin could not be installed.'))
        elif not file_info.has_option('Plugin', 'name'):
            _logger.debug('Required open name not found in \
Plugin section of plugin.info file.')
            self.tw.showlabel(
                'status', label=_('Plugin could not be installed.'))
        else:
            plugin_name = file_info.get('Plugin', 'name')
            _logger.debug('Plugin name: %s' % (plugin_name))
            tmp_path = os.path.join(tmp_dir, plugin_name)
            plugin_path = os.path.join(activity.get_bundle_path(), 'plugins')
            if os.path.exists(os.path.join(plugin_path, plugin_name)):
                self._reload_plugin_alert(tmp_dir, tmp_path, plugin_path,
                                          plugin_name, file_info)
            else:
                self._complete_plugin_install(tmp_dir, tmp_path, plugin_path,
                                              plugin_name, file_info)

    def _complete_plugin_install(self, tmp_dir, tmp_path, plugin_path,
                                 plugin_name, file_info):
        ''' We complete the installation directly or from ConfirmationAlert '''
        status = subprocess.call(['cp', '-r', tmp_path, plugin_path + '/'])
        if status == 0:
            # Save the plugin.info file in the plugin directory
            subprocess.call(['cp', os.path.join(tmp_dir, 'plugin.info'),
                             os.path.join(plugin_path, plugin_name) + '/'])
            _logger.debug('Plugin installed successfully.')
            if self.has_toolbarbox:
                palette_name_list = []
                if file_info.has_option('Plugin', 'palette'):
                    palette_name_list = file_info.get(
                        'Plugin', 'palette').split(',')
                    create_palette = []
                    for palette_name in palette_name_list:
                        if not palette_name.strip() in palette_names:
                            create_palette.append(True)
                        else:
                            create_palette.append(False)
                _logger.debug('Initializing plugin...')
                self.tw.init_plugin(plugin_name)
                self.tw._plugins[-1].setup()
                self.tw.load_media_shapes()
                for i, palette_name in enumerate(palette_name_list):
                    if create_palette[i]:
                        _logger.debug('Creating plugin palette %s...' % (
                                palette_name.strip()))
                        j = len(self.palette_buttons)
                        self.palette_buttons.insert(j - 1,
                            self._radio_button_factory(
                                palette_name.strip() + 'off',
                                self._palette_toolbar,
                                self.do_palette_buttons_cb,
                                j - 1,
                                help_strings[palette_name.strip()],
                                self.palette_buttons[0],
                                position=j - 1))
                        self.tw.palettes.insert(j - 1, [])
                        self.tw.palette_sprs.insert(j - 1, [None, None])
                    else:
                        _logger.debug('Palette already exists... \
skipping insert')
                # We need to change the index associated with the
                # Trash Palette Button.
                j = len(palette_names)
                self.palette_buttons[j - 1].connect(
                    'clicked', self.do_palette_buttons_cb, j - 1)
            else:
                self.tw.showlabel('status',
                                  label=_('Please restart Turtle Art \
in order to use the plugin.'))
        else:
            self.tw.showlabel(
                'status', label=_('Plugin could not be installed.'))
        status = subprocess.call(['rm', '-r', tmp_path])
        if status != 0:
            _logger.debug('Problems cleaning up tmp_path.')
        shutil.rmtree(tmp_dir)

    def _cancel_plugin_install(self, tmp_dir):
        ''' If we cancel, just cleanup '''
        shutil.rmtree(tmp_dir)

    def _reload_plugin_alert(self, tmp_dir, tmp_path, plugin_path, plugin_name,
                             file_info):
        ''' We warn the user if the plugin was previously loaded '''
        alert = ConfirmationAlert()
        alert.props.title = _('Plugin %s already installed.') % (plugin_name)
        alert.props.msg = _('Do you want to reinstall %s?') % (plugin_name)

        def _reload_plugin_alert_response_cb(alert, response_id, self,
                                             tmp_dir, tmp_path, plugin_path,
                                             plugin_name, file_info):
            if response_id is gtk.RESPONSE_OK:
                _logger.debug('continue to install')
                self.remove_alert(alert)
                self._complete_plugin_install(tmp_dir, tmp_path, plugin_path,
                                              plugin_name, file_info)
            elif response_id is gtk.RESPONSE_CANCEL:
                _logger.debug('cancel install')
                self.remove_alert(alert)
                self._cancel_plugin_install(tmp_dir)

        alert.connect('response', _reload_plugin_alert_response_cb, self,
                      tmp_dir, tmp_path, plugin_path, plugin_name, file_info)
        self.add_alert(alert)
        alert.show()

    def read_file(self, file_path, run_it=False, plugin=False):
        ''' Open a project or plugin and then run it. '''
        if hasattr(self, 'tw'):
            _logger.debug('Read file: %s' % (file_path))
            # Could be a plugin or deprecated gtar or tar file...
            if plugin or file_path.endswith(('.gtar', '.tar', '.tar.gz')):
                try:
                    status = subprocess.call(['gunzip', file_path])
                    if status == 0:
                        tar_fd = tarfile.open(file_path[:-3], 'r')
                    else:
                        tar_fd = tarfile.open(file_path, 'r')
                except:
                    tar_fd = tarfile.open(file_path, 'r')

                tmp_dir = tempfile.mkdtemp()

                try:
                    tar_fd.extractall(tmp_dir)
                    if not plugin:
                        # Looking for a .ta file
                        self.tw.load_files(os.path.join(tmp_dir, 'ta_code.ta'),
                                           run_it)
                        turtle_code = os.path.join(tmp_dir, 'ta_code.ta')
                        if os.path.exists(turtle_code):
                            self.tw.load_files(turtle_code, run_it)
                    else:
                        self._load_a_plugin(tmp_dir)
                except:
                    _logger.debug('Could not extract files from %s.' % (
                            file_path))
                finally:
                    if not plugin:
                        shutil.rmtree(tmp_dir)
                    tar_fd.close()
            # ...otherwise, assume it is a .ta file.
            else:
                _logger.debug('Trying to open a .ta file:' + file_path)
                self.tw.load_files(file_path, run_it)

            # Finally, run the project.
            if run_it:
                self.tw.run_button(0)
        else:
            _logger.debug('Deferring reading file %s' % (file_path))

    def jobject_new_patch(self):
        ''' Save instance to Journal. '''
        oldj = self._jobject
        self._jobject = datastore.create()
        self._jobject.metadata['title'] = oldj.metadata['title']
        self._jobject.metadata['title_set_by_user'] = \
            oldj.metadata['title_set_by_user']
        self._jobject.metadata['activity_id'] = self.get_id()
        self._jobject.metadata['keep'] = '0'
        self._jobject.metadata['preview'] = ''
        self._jobject.metadata['icon-color'] = profile.get_color().to_string()
        self._jobject.file_path = ''
        datastore.write(
            self._jobject, reply_handler=self._internal_jobject_create_cb,
            error_handler=self._internal_jobject_error_cb)
        self._jobject.destroy()

    def _copy_cb(self, button):
        ''' Copy to the clipboard. '''
        clipboard = gtk.Clipboard()
        _logger.debug('Serialize the project and copy to clipboard.')
        data = self.tw.assemble_data_to_save(False, False)
        if data is not []:
            text = data_to_string(data)
            clipboard.set_text(text)
        self.tw.paste_offset = 20

    def _paste_cb(self, button):
        ''' Paste from the clipboard. '''
        clipboard = gtk.Clipboard()
        _logger.debug('Paste to the project.')
        text = clipboard.wait_for_text()
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

    def _add_label(self, string, toolbar, width=None):
        ''' Add a label to a toolbar. '''
        label = gtk.Label(string)
        label.set_line_wrap(True)
        if width is not None:
            label.set_size_request(width, -1)
        label.show()
        toolitem = gtk.ToolItem()
        toolitem.add(label)
        toolbar.insert(toolitem, -1)
        toolitem.show()
        return label

    def _add_separator(self, toolbar, expand=False, visible=True):
        ''' Add a separator to a toolbar. '''
        separator = gtk.SeparatorToolItem()
        separator.props.draw = visible
        separator.set_expand(expand)
        if hasattr(toolbar, 'insert'):
            toolbar.insert(separator, -1)
        else:
            toolbar.props.page.insert(separator, -1)
        separator.show()

    def _add_button(self, name, tooltip, callback, toolbar, accelerator=None,
                    arg=None):
        ''' Add a button to a toolbar. '''
        button = ToolButton(name)
        if tooltip is not None:
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
        if toolbar is not None:
            if hasattr(toolbar, 'insert'):  # Add button to the main toolbar...
                toolbar.insert(button, -1)
            else:  # ...or a secondary toolbar.
                toolbar.props.page.insert(button, -1)

        if not name in help_strings:
            help_strings[name] = tooltip
        return button

    def _radio_button_factory(self, button_name, toolbar, cb, arg, tooltip,
                              group, position=-1):
        ''' Add a radio button to a toolbar '''
        button = RadioToolButton(group=group)
        button.set_named_icon(button_name)
        if cb is not None:
            if arg is None:
                button.connect('clicked', cb)
            else:
                button.connect('clicked', cb, arg)
        if hasattr(toolbar, 'insert'):  # Add button to the main toolbar...
            toolbar.insert(button, position)
        else:  # ...or a secondary toolbar.
            toolbar.props.page.insert(button, position)
        button.show()
        if tooltip is not None:
            button.set_tooltip(tooltip)
        return button

    def _add_button_and_label(self, icon_name, tooltip, cb, box):
        ''' Add a button and a label to a box '''
        button_and_label = gtk.HBox()
        button = self._add_button(icon_name, None, cb, None)
        label = gtk.Label(tooltip)
        label.show()
        button_and_label.pack_start(button)
        button_and_label.pack_start(label)
        box.pack_start(button_and_label)
        button_and_label.show()
        return button

    def _notify_successful_save(self, title='', msg=''):
        ''' Notify user when saves are completed '''

        def _notification_alert_response_cb(alert, response_id, self):
            self.remove_alert(alert)

        alert = NotifyAlert()
        alert.props.title = title
        alert.connect('response', _notification_alert_response_cb, self)
        alert.props.msg = msg
        self.add_alert(alert)
        alert.show()
