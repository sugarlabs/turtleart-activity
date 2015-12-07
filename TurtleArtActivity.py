# -*- coding: utf-8 -*-
# Copyright (c) 2007, Playful Invention Company
# Copyright (c) 2008-14, Walter Bender
# Copyright (c) 2009-13 Raul Gutierrez Segales
# Copyright (c) 2012 Alan Aguiar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
    from sugar.activity.widgets import (ActivityToolbarButton, StopButton)
    from sugar.graphics.toolbarbox import (ToolbarBox, ToolbarButton)
    HAS_TOOLBARBOX = True
except ImportError:
    HAS_TOOLBARBOX = False
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.graphics.alert import (ConfirmationAlert, Alert, NotifyAlert)
from sugar.graphics import style
from sugar.graphics.icon import Icon
from sugar.graphics.xocolor import XoColor
from sugar.datastore import datastore
from sugar import profile

import os
import glob
import tarfile
import subprocess
import ConfigParser
import shutil
import tempfile
try:
    import gconf
    HAS_GCONF = True
except ImportError:
    HAS_GCONF = False

from gettext import gettext as _

from TurtleArt.taplugin import (load_a_plugin, cancel_plugin_install,
                                complete_plugin_install)
from TurtleArt.tapalette import (palette_names, help_strings, help_palettes,
                                 help_windows, default_values)
from TurtleArt.taconstants import (BLOCK_SCALE, XO1, XO15, XO175, XO4,
                                   MIMETYPE, TMP_SVG_PATH, TMP_ODP_PATH,
                                   PASTE_OFFSET)
from TurtleArt.taexportlogo import save_logo
from TurtleArt.taexportpython import save_python
from TurtleArt.tautils import (data_to_file, data_to_string, data_from_string,
                               get_path, chooser_dialog, get_hardware)
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.tacollaboration import Collaboration
from TurtleArt.taprimitive import PyExportError

if HAS_TOOLBARBOX:
    from TurtleArt.util.helpbutton import (HelpButton, add_section,
                                           add_paragraph)


class TurtleArtActivity(activity.Activity):

    ''' Activity subclass for Turtle Art '''
    _HOVER_HELP = '/desktop/sugar/activities/turtleart/hoverhelp'
    _ORIENTATION = '/desktop/sugar/activities/turtleart/orientation'
    _COORDINATE_SCALE = '/desktop/sugar/activities/turtleart/coordinatescale'

    def __init__(self, handle):
        ''' Set up the toolbars, canvas, sharing, etc. '''
        try:
            super(TurtleArtActivity, self).__init__(handle)
        except dbus.exceptions.DBusException as e:
            _logger.error(str(e))

        self.tw = None
        self.init_complete = False

        self.bundle_path = activity.get_bundle_path()

        self.error_list = []

        self.palette_buttons = []
        self._palette_names = []
        self._overflow_buttons = []

        self._check_ver_change(get_path(activity, 'data'))
        self.connect("notify::active", self._notify_active_cb)

        self.has_toolbarbox = HAS_TOOLBARBOX
        _logger.debug('_setup_toolbar')
        self._setup_toolbar()
        self.label_offset = style.GRID_CELL_SIZE

        _logger.debug('_setup_canvas')
        self._setup_canvas(self._setup_scrolled_window())

        _logger.debug('_setup_palette_toolbar')
        self._setup_palette_toolbar()
        self._setup_extra_controls()

        _logger.debug('_setup_sharing')
        if self.shared_activity:
            # We're joining
            if not self.get_shared():
                xocolors = XoColor(profile.get_color().to_string())
                share_icon = Icon(icon_name='zoom-neighborhood',
                                  xo_color=xocolors)
                self._joined_alert = Alert()
                self._joined_alert.props.icon = share_icon
                self._joined_alert.props.title = _('Please wait')
                self._joined_alert.props.msg = _('Starting connection...')
                self.add_alert(self._joined_alert)

                # Wait for joined signal
                self.connect("joined", self._joined_cb)

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
        # Now called from lazy_init
        # self.check_buttons_for_fit()
        if HAS_GCONF:
            self.client = gconf.client_get_default()
            if self.client.get_int(self._HOVER_HELP) == 1:
                self._do_hover_help_toggle(None)
            if not self.client.get_int(self._COORDINATE_SCALE) in [0, 1]:
                self.tw.coord_scale = 1
                self.do_rescale_cb(None)
            else:
                self.tw.coord_scale = 0
                self.do_rescale_cb(None)

        self._selected_sample = None
        self._sample_window = None

        self.init_complete = True

    def update_palette_from_metadata(self):
        if HAS_GCONF:
            # We have to wait to set the orientation for the palettes
            # to be loaded.
            self.client = gconf.client_get_default()
            if self.client.get_int(self._ORIENTATION) == 1:
                self.tw.set_orientation(1)

        if 'palette' in self.metadata:
            n = int(self.metadata['palette'])
            if n == -1:
                self.tw.hideshow_palette(False)
            else:
                # Try to set radio button to active
                if n < len(self.palette_buttons):
                    self.palette_buttons[n].set_active(True)
                else:
                    self.tw.show_palette(n=0)
                if 'orientation' in self.metadata:
                    self.tw.set_orientation(int(self.metadata['orientation']))
        else:
            # Else start on the Turtle palette
            self.tw.show_palette(n=0)

    def check_buttons_for_fit(self):
        ''' Check to see which set of buttons to display '''
        if not self.has_toolbarbox:
            return

        # If there are too many palettes to fit, put them in a
        # scrolling window
        self._setup_palette_toolbar()

        if self.samples_button in self.toolbox.toolbar:
            self.toolbox.toolbar.remove(self.extras_separator)
            self.toolbox.toolbar.remove(self.samples_button)
            self.toolbox.toolbar.remove(self.stop_separator)
        self.toolbox.toolbar.remove(self.stop_button)
        self._view_toolbar.remove(self._coordinates_toolitem)

        if gtk.gdk.screen_width() / 14 < style.GRID_CELL_SIZE:
            self.samples_button2.show()
            self.samples_label2.show()
            self.toolbox.toolbar.insert(self.stop_button, -1)
        else:
            self.samples_button2.hide()
            self.samples_label2.hide()
            self.toolbox.toolbar.insert(self.extras_separator, -1)
            self.extras_separator.props.draw = True
            self.extras_separator.show()
            self.toolbox.toolbar.insert(self.samples_button, -1)
            self.samples_button.show()
            self.toolbox.toolbar.insert(self.stop_separator, -1)
            self.stop_separator.show()
            self.toolbox.toolbar.insert(self.stop_button, -1)
            self._view_toolbar.insert(self._coordinates_toolitem, -1)

        self.toolbox.show_all()

    # Activity toolbar callbacks
    def do_save_as_logo_cb(self, button):
        ''' Write UCB logo code to datastore. '''
        self.save_as_logo.set_icon('logo-saveon')
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.timeout_add(250, self.__save_as_logo)

    def __save_as_logo(self):
        logo_code_path = self._dump_logo_code()
        if logo_code_path is not None:
            dsobject = datastore.create()
            dsobject.metadata['title'] = self.metadata['title'] + '.lg'
            dsobject.metadata['mime_type'] = 'text/plain'
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.set_file_path(logo_code_path)
            datastore.write(dsobject)
            dsobject.destroy()
            os.remove(logo_code_path)
        self.save_as_logo.set_icon('logo-saveoff')
        if hasattr(self, 'get_window'):
            self.get_window().set_cursor(self._old_cursor)

    def do_save_as_python_cb(self, widget):
        ''' Callback for saving the project as Python code. '''
        self.save_as_python.set_icon('python-saveon')
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.timeout_add(250, self.__save_as_python)

    def __save_as_python(self):
        # catch PyExportError and display a user-friendly message instead
        try:
            pythoncode = save_python(self.tw)
        except PyExportError as pyee:
            if pyee.block is not None:
                pyee.block.highlight()
            self.tw.showlabel('status', str(pyee))
            _logger.debug(pyee)

        if pythoncode:
            datapath = get_path(activity, 'instance')
            python_code_path = os.path.join(datapath, 'tmpfile.py')
            f = file(python_code_path, 'w')
            f.write(pythoncode)
            f.close()

            dsobject = datastore.create()
            dsobject.metadata['title'] = self.metadata['title'] + '.py'
            dsobject.metadata['mime_type'] = 'text/x-python'
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.set_file_path(python_code_path)
            datastore.write(dsobject)
            dsobject.destroy()

            os.remove(python_code_path)
        else:
            title = _("Export as python")
            msg = _("Error: You must use a Start Block when exporting to Python.")
            alert = NotifyAlert(5)
            alert.props.title = title
            alert.props.msg = msg
            alert.connect(
                'response',
                lambda alert,
                response: self.remove_alert(alert))
            self.add_alert(alert)

        self.save_as_python.set_icon('python-saveoff')
        if hasattr(self, 'get_window'):
            self.get_window().set_cursor(self._old_cursor)

    def do_load_ta_project_cb(self, button, new=False):
        ''' Load a project from the Journal. '''
        self._create_new = new
        if hasattr(self, 'get_window'):
            _logger.debug('setting watch cursor')
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        chooser_dialog(self, 'org.laptop.TurtleArtActivity',
                       self._load_ta_project)

    def _load_ta_project(self, dsobject):
        ''' Load a TA project from the datastore. '''
        if dsobject is None:
            self.restore_cursor()
            return
        try:
            _logger.debug('Opening %s ' % (dsobject.file_path))
            self._tmp_dsobject = dsobject
            self.read_file(dsobject.file_path, plugin=False)
        except:
            _logger.debug("Couldn't open %s" % (dsobject.file_path))

    def do_load_ta_plugin_cb(self, button):
        ''' Load a plugin from the Journal. '''
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        # FIXME: we are looking for tar files
        chooser_dialog(self, '', self._load_ta_plugin)

    def _load_ta_plugin(self, dsobject):
        ''' Load a TA plugin from the datastore. '''
        if dsobject is None:
            self.restore_cursor()
            return
        _logger.debug('Opening %s ' % (dsobject.file_path))
        self.read_file(dsobject.file_path, plugin=True)
        dsobject.destroy()

    def do_load_python_cb(self, button):
        ''' Load Python code from the Journal. '''
        self.load_python.set_icon('pippy-openon')
        self.tw.load_python_code_from_file(fname=None, add_new_block=True)
        gobject.timeout_add(250, self.load_python.set_icon, 'pippy-openoff')

    def do_save_as_odp_cb(self, button):
        _logger.debug('saving odp to journal')
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.timeout_add(250, self.__save_as_odp)

    def __save_as_odp(self):
        self.tw.save_as_odp()
        if hasattr(self, 'get_window'):
            self.get_window().set_cursor(self._old_cursor)

    def do_save_as_icon_cb(self, button):
        _logger.debug('saving icon to journal')
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.timeout_add(250, self.__save_as_icon)

    def __save_as_icon(self):
        self.tw.write_svg_operation()
        self.tw.save_as_icon()
        if hasattr(self, 'get_window'):
            self.get_window().set_cursor(self._old_cursor)

    def do_save_as_image_cb(self, button):
        ''' Save the canvas to the Journal. '''
        self.save_as_image.set_icon('image-saveon')
        _logger.debug('saving image to journal')
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.timeout_add(250, self.__save_as_image)

    def __save_as_image(self):
        self.tw.save_as_image()
        self.save_as_image.set_icon('image-saveoff')
        if hasattr(self, 'get_window'):
            self.get_window().set_cursor(self._old_cursor)

    def do_keep_cb(self, button):
        ''' Save a snapshot of the project to the Journal. '''
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.timeout_add(250, self.__keep)

    def __keep(self):
        tmpfile = self._dump_ta_code()
        if tmpfile is not None:
            dsobject = datastore.create()
            dsobject.metadata['title'] = self.metadata['title'] + ' ' + \
                _('snapshot')
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = MIMETYPE[0]
            dsobject.metadata['activity'] = 'org.laptop.TurtleArtActivity'
            dsobject.set_file_path(tmpfile)
            datastore.write(dsobject)
            dsobject.destroy()
            os.remove(tmpfile)

        if hasattr(self, 'get_window'):
            self.get_window().set_cursor(self._old_cursor)

    # Main/palette toolbar button callbacks

    def do_palette_cb(self, button):
        ''' Show/hide palette '''
        if self.tw.palette:
            self.tw.hideshow_palette(False)
            self.do_hidepalette()
            if not self.has_toolbarbox and \
               self.tw.selected_palette is not None:
                self.palette_buttons[self.tw.selected_palette].set_icon(
                    palette_names[self.tw.selected_palette] + 'off')
        else:
            self.tw.hideshow_palette(True)
            self.do_showpalette()
            if self.has_toolbarbox:
                self.palette_buttons[0].set_icon(palette_names[0] + 'on')

    def do_palette_buttons_cb(self, button, i):
        ''' Palette selector buttons '''
        if hasattr(button, 'get_active') and not button.get_active():
            return
        if self._overflow_palette.is_up():
            self._overflow_palette.popdown(immediate=True)
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
            if HAS_GCONF:
                self.client.set_int(self._HOVER_HELP, 0)
        else:
            self.tw.no_help = True
            self.tw.last_label = None
            if self.tw.status_spr is not None:
                self.tw.status_spr.hide()
            self._hover_help_toggle.set_icon('help-on')
            self._hover_help_toggle.set_tooltip(_('Turn on hover help'))
            if HAS_GCONF:
                self.client.set_int(self._HOVER_HELP, 1)

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
        self.step_button.set_icon('run-slowoff')
        self.tw.lc.trace = 0
        self.tw.step_time = 0
        # Autohide blocks and palettes on run
        self.tw.hideblocks()
        self.tw.display_coordinates(clear=True)
        self.tw.run_button(self.tw.step_time, running_from_button_push=True)

    def do_step_cb(self, button):
        ''' Callback for step button (turtle) '''
        self.step_button.set_icon('run-slowon')
        self.run_button.set_icon('run-fastoff')
        self.tw.lc.trace = 1
        self.tw.step_time = 3
        self.tw.run_button(self.tw.step_time, running_from_button_push=True)

    def do_stop_cb(self, button):
        ''' Callback for stop button. '''
        # Auto show blocks after stop
        if not self.tw.hide and not self.tw.running_blocks:
            self.tw.hideblocks()
            self.stop_turtle_button.set_icon('hideshowon')
            self.stop_turtle_button.set_tooltip(_('Show blocks'))
        else:
            self.tw.showblocks()
            self.stop_turtle_button.set_icon('hideshowoff')
            self.stop_turtle_button.set_tooltip(_('Hide blocks'))
        # Note: We leave the old button state highlighted to indicate
        # speed if blocks are clicked to run.
        # self.run_button.set_icon('run-fastoff')
        # self.step_button.set_icon('run-slowoff')
        self.tw.stop_button()
        self.tw.display_coordinates()

    def do_samples_cb(self, button):
        ''' Sample-projects open dialog '''
        if hasattr(self, 'get_window'):
            _logger.debug('setting watch cursor')
            if hasattr(self.get_window(), 'get_cursor'):
                self._old_cursor = self.get_window().get_cursor()
            self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        self._create_store()
        # self.tw.load_file_from_chooser(True)
        # Now that the file is loaded, restore the cursor
        _logger.debug('restoring cursor')
        self.restore_cursor()

    def adjust_sw(self, dx, dy):
        ''' Adjust the scrolled window position. '''
        if not self.tw.hw in [XO1]:
            self._defer_palette_move = True
        hadj = self.sw.get_hadjustment()
        hvalue = hadj.get_value() + dx
        try:
            if hvalue < hadj.get_lower():
                hvalue = hadj.get_lower()
            elif hvalue > hadj.get_upper():
                hvalue = hadj.get_upper()
        except AttributeError:
            _logger.debug(
                'get_lower, get_upper only available in PyGTK 2.14 and above.')
        hadj.set_value(hvalue)
        self.sw.set_hadjustment(hadj)
        vadj = self.sw.get_vadjustment()
        vvalue = vadj.get_value() + dy
        try:
            if vvalue < vadj.get_lower():
                vvalue = vadj.get_lower()
            elif vvalue > vadj.get_upper():
                vvalue = vadj.get_upper()
        except AttributeError:
            _logger.debug(
                'get_lower, get_upper only available in PyGTK 2.14 and above.')
        vadj.set_value(vvalue)
        self.sw.set_vadjustment(vadj)

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
            i = 3
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
        ''' Rescale coordinate system (20==height/2 or 100 pixels). '''
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height / 40
            self.rescale_button.set_icon('contract-coordinates')
            self.rescale_button.set_tooltip(_('Rescale coordinates down'))
            default_values['forward'] = [10]
            default_values['back'] = [10]
            default_values['arc'] = [90, 10]
            default_values['setpensize'] = [1]
            self.tw.turtles.get_active_turtle().set_pen_size(1)
        else:
            self.tw.coord_scale = 1
            self.rescale_button.set_icon('expand-coordinates')
            self.rescale_button.set_tooltip(_('Rescale coordinates up'))
            default_values['forward'] = [100]
            default_values['back'] = [100]
            default_values['arc'] = [90, 100]
            default_values['setpensize'] = [5]
            self.tw.turtles.get_active_turtle().set_pen_size(5)
        if HAS_GCONF:
            self.client.set_int(self._COORDINATE_SCALE, self.tw.coord_scale)

        self.tw.recalculate_constants()

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
        except Exception as e:
            _logger.error("Couldn't save Logo code: " + str(e))
            tmpfile = None
        return tmpfile

    def _dump_ta_code(self):
        '''  Save TA code to temporary file. '''
        datapath = get_path(activity, 'instance')
        tmpfile = os.path.join(datapath, 'tmpfile.ta')
        try:
            data_to_file(self.tw.assemble_data_to_save(), tmpfile)
        except Exception as e:
            _logger.error("Couldn't save project code: " + str(e))
            tmpfile = None
        return tmpfile

    def _keep_clicked_cb(self, button):
        ''' Keep-button clicked. '''
        self.jobject_new_patch()

    def is_fullscreen(self):
        ''' Are we in fullscreen mode (toolbars hidden)? '''
        # Fixme: this should be a exposed as a window property, not private
        return self._is_fullscreen

    def toolbars_expanded(self, palette=False):
        ''' Are any toolbars expanded? '''
        if not self.has_toolbarbox:
            if palette:
                return None
            else:
                return False
        if self.palette_toolbar_button.is_expanded():
            if palette:
                return self.palette_toolbar_button
            else:
                return True
        elif self.edit_toolbar_button.is_expanded():
            if palette:
                return self.edit_toolbar_button
            else:
                return True
        elif self.view_toolbar_button.is_expanded():
            if palette:
                return self.view_toolbar_button
            else:
                return True
        elif self.activity_toolbar_button.is_expanded():
            if palette:
                return self.activity_toolbar_button
            else:
                return True
        else:
            if palette:
                return None
            else:
                return False

    def _setup_toolbar(self):
        ''' Setup toolbar according to Sugar version. '''
        if self.has_toolbarbox:
            self.max_participants = 4

            self._setup_toolbar_help()
            self.toolbox = ToolbarBox()

            self.activity_toolbar_button = ActivityToolbarButton(self)

            edit_toolbar = gtk.Toolbar()
            self.edit_toolbar_button = ToolbarButton(label=_('Edit'),
                                                     page=edit_toolbar,
                                                     icon_name='toolbar-edit')

            self._view_toolbar = gtk.Toolbar()
            self.view_toolbar_button = ToolbarButton(label=_('View'),
                                                     page=self._view_toolbar,
                                                     icon_name='toolbar-view')
            self._palette_toolbar = gtk.Toolbar()
            self.palette_toolbar_button = ToolbarButton(
                page=self._palette_toolbar, icon_name='palette')

            self._help_button = HelpButton(self)

            self._make_load_save_buttons(self.activity_toolbar_button)

            self.activity_toolbar_button.show()
            self.toolbox.toolbar.insert(self.activity_toolbar_button, -1)
            self.edit_toolbar_button.show()
            self.toolbox.toolbar.insert(self.edit_toolbar_button, -1)
            self.view_toolbar_button.show()
            self.toolbox.toolbar.insert(self.view_toolbar_button, -1)
            self.palette_toolbar_button.show()
            self.toolbox.toolbar.insert(self.palette_toolbar_button, -1)

            self.set_toolbar_box(self.toolbox)
        else:
            self.toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self.toolbox)

            self._project_toolbar = gtk.Toolbar()
            self.toolbox.add_toolbar(_('Project'), self._project_toolbar)
            self._view_toolbar = gtk.Toolbar()
            self.toolbox.add_toolbar(_('View'), self._view_toolbar)
            edit_toolbar = gtk.Toolbar()
            self.toolbox.add_toolbar(_('Edit'), edit_toolbar)
            journal_toolbar = gtk.Toolbar()
            self.toolbox.add_toolbar(_('Save/Load'), journal_toolbar)

            self._make_palette_buttons(self._project_toolbar,
                                       palette_button=True)

            self._add_separator(self._project_toolbar)
            self._make_load_save_buttons(journal_toolbar)

        self._add_button('edit-copy', _('Copy'), self._copy_cb,
                         edit_toolbar, '<Ctrl>c')
        self._add_button('edit-paste', _('Paste'), self._paste_cb,
                         edit_toolbar, '<Ctrl>v')
        self._add_button('edit-undo', _('Restore blocks from trash'),
                         self._undo_cb, edit_toolbar)
        self._add_separator(edit_toolbar)
        self._add_button('save-blocks', _('Save stack'), self._save_macro_cb,
                         edit_toolbar)
        self._add_button('delete-blocks', _('Delete stack'),
                         self._delete_macro_cb, edit_toolbar)

        self._add_button('view-fullscreen', _('Fullscreen'),
                         self.do_fullscreen_cb, self._view_toolbar,
                         '<Alt>Return')
        self._add_button('view-Cartesian', _('Cartesian coordinates'),
                         self.do_cartesian_cb, self._view_toolbar)
        self._add_button('view-polar', _('Polar coordinates'),
                         self.do_polar_cb, self._view_toolbar)
        if get_hardware() in [XO1, XO15, XO175, XO4]:
            self._add_button('view-metric', _('Metric coordinates'),
                             self.do_metric_cb, self._view_toolbar)
        self.rescale_button = self._add_button(
            'expand-coordinates', _('Rescale coordinates up'),
            self.do_rescale_cb, self._view_toolbar)
        self.resize_up_button = self._add_button(
            'resize+', _('Grow blocks'), self.do_grow_blocks_cb,
            self._view_toolbar)
        self.resize_down_button = self._add_button(
            'resize-', _('Shrink blocks'), self.do_shrink_blocks_cb,
            self._view_toolbar)
        self._hover_help_toggle = self._add_button(
            'help-off', _('Turn off hover help'), self._do_hover_help_toggle,
            self._view_toolbar)
        self._add_separator(self._view_toolbar, visible=False)
        self.coordinates_label = gtk.Label('(0, 0) 0')
        self.coordinates_label.show()
        self._coordinates_toolitem = gtk.ToolItem()
        self._coordinates_toolitem.add(self.coordinates_label)
        self._coordinates_toolitem.show()
        self._view_toolbar.insert(self._coordinates_toolitem, -1)

        edit_toolbar.show()
        self._view_toolbar.show()
        self.toolbox.show()

        if self.has_toolbarbox:
            self.edit_toolbar_button.set_expanded(True)
            self.edit_toolbar_button.set_expanded(False)
            self.palette_toolbar_button.set_expanded(True)
        else:
            self.toolbox.set_current_toolbar(1)

    def _setup_extra_controls(self):
        ''' Add the rest of the buttons to the main toolbar '''
        if not self.has_toolbarbox:
            self.samples_button = self._add_button(
                'ta-open', _('Load example'), self.do_samples_cb,
                self._project_toolbar)
            self._add_separator(self._project_toolbar, expand=False,
                                visible=True)
            self._make_project_buttons(self._project_toolbar)
            return

        self._make_project_buttons(self.toolbox.toolbar)

        self.extras_separator = self._add_separator(
            self.toolbox.toolbar, expand=False, visible=True)

        self.samples_button = self._add_button(
            'ta-open', _('Load example'), self.do_samples_cb,
            self.toolbox.toolbar)

        self.toolbox.toolbar.insert(self._help_button, -1)
        self._help_button.show()

        self.stop_separator = self._add_separator(
            self.toolbox.toolbar, expand=True, visible=False)

        self.stop_button = StopButton(self)
        self.stop_button.props.accelerator = '<Ctrl>Q'
        self.toolbox.toolbar.insert(self.stop_button, -1)
        self.stop_button.show()

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

        add_paragraph(help_box, _('Share selected blocks'), icon='shareon')
        add_paragraph(help_box, _('Save/Load'), icon='save-load')
        add_paragraph(help_box, _('Save as image'), icon='image-saveoff')

        self.save_as_icon = add_paragraph(
            help_box, _('Save as icon'), icon='image-saveoff')
        self.save_as_icon.connect(
            'expose-event', self._save_as_icon_expose_cb)

        # TRANS: ODP is Open Office presentation
        self.save_as_odp = add_paragraph(help_box, _('Save as ODP'),
                                         icon='odp-saveoff')
        self.save_as_odp.connect('expose-event',
                                 self._save_as_odp_expose_cb)

        add_paragraph(help_box, _('Save as Logo'), icon='logo-saveoff')
        add_paragraph(help_box, _('Save as Python'), icon='python-saveoff')
        add_paragraph(help_box, _('Save snapshot'), icon='filesaveoff')
        add_paragraph(help_box, _('Add project'), icon='load-from-journal')
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
        add_paragraph(help_box, _('Save stack'), icon='save-macro')

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
        if get_hardware() in [XO1, XO15, XO175, XO4]:
            add_paragraph(help_box, _('Metric coordinates'),
                          icon='view-metric')
        add_paragraph(help_box, _('Rescale coordinates up'),
                      icon='expand-coordinates')
        add_paragraph(help_box, _('Grow blocks'), icon='resize+')
        add_paragraph(help_box, _('Shrink blocks'), icon='resize-')
        add_paragraph(help_box, _('Turn off hover help'), icon='help-off')

    def _save_as_icon_expose_cb(self, box, context):
        for widget in box.get_children():
            widget.set_sensitive(self.tw.canvas.cr_svg is not None)

    def _save_as_odp_expose_cb(self, box, context):
        for widget in box.get_children():
            widget.set_sensitive(len(self.tw.saved_pictures) > 0)

    def _setup_palette_toolbar(self):
        ''' The palette toolbar must be setup *after* plugins are loaded. '''
        if self.has_toolbarbox:
            max_palettes = int(gtk.gdk.screen_width() / style.GRID_CELL_SIZE)
            max_palettes -= 2  # the margins
            if len(palette_names) > max_palettes:
                max_palettes -= 1  # Make room for the palette button
            overflow = len(palette_names) - max_palettes
            if overflow < 1 or \
                    gtk.gdk.screen_width() - style.GRID_CELL_SIZE < \
                    int(overflow * (style.GRID_CELL_SIZE + 2)):
                width = gtk.gdk.screen_width() - style.GRID_CELL_SIZE
                height = int(style.GRID_CELL_SIZE * 1.5)
            else:
                width = int(overflow * (style.GRID_CELL_SIZE + 2))
                height = style.GRID_CELL_SIZE

            if len(self.palette_buttons) == 0:
                self._generate_palette_buttons()
                self._overflow_palette = \
                    self._overflow_palette_button.get_palette()
                self._overflow_box = gtk.HBox()
                self._overflow_box.set_homogeneous(False)
                self._overflow_sw = gtk.ScrolledWindow()
                self._overflow_sw.set_policy(gtk.POLICY_AUTOMATIC,
                                             gtk.POLICY_NEVER)
                self._overflow_sw.add_with_viewport(self._overflow_box)
            elif len(self.palette_buttons) < len(palette_names):
                # add new buttons for palettes generated since last time
                self._generate_palette_buttons(add_buttons=True)
                self._remove_palette_buttons()
            else:  # remove the radio buttons and overflow buttons
                self._remove_palette_buttons()

            for i in range(len(self.palette_buttons)):
                if i < max_palettes:
                    self._palette_toolbar.insert(self.palette_buttons[i], -1)
                if i == max_palettes and \
                   max_palettes < len(self.palette_buttons):
                    self._palette_toolbar.insert(
                        self._overflow_palette_button, -1)
                if i >= max_palettes:
                    self._overflow_box.pack_start(self._overflow_buttons[i])

            self._overflow_sw.set_size_request(width, height)
            self._overflow_sw.show()

            '''
            if self.tw.hw in [XO1, XO15, XO175, XO4]:
                self._make_palette_buttons(self._palette_toolbar)
            '''
            self._palette_toolbar.show()
            self._overflow_box.show_all()
            self._overflow_palette.set_content(self._overflow_sw)

    def _remove_palette_buttons(self):
        for button in self.palette_buttons:
            if button in self._palette_toolbar:
                self._palette_toolbar.remove(button)
        for button in self._overflow_buttons:
            if button in self._overflow_box:
                self._overflow_box.remove(button)
        if self._overflow_palette_button in self._palette_toolbar:
            self._palette_toolbar.remove(self._overflow_palette_button)

    def _generate_palette_buttons(self, add_buttons=False):
        ''' Create a radio button and a normal button for each palette '''
        for i, palette_name in enumerate(palette_names):
            if palette_name in self._palette_names:
                continue
            self._palette_names.append(palette_name)
            if i == 0:
                palette_group = None
            else:
                palette_group = self.palette_buttons[0]
            _logger.debug('palette_buttons.append %s', (palette_name))
            self.palette_buttons.append(
                self._radio_button_factory(
                    palette_name + 'off',
                    None,
                    self.do_palette_buttons_cb,
                    i,
                    help_strings[palette_name],
                    palette_group))
            self._overflow_buttons.append(
                self._add_button(
                    palette_name + 'off',
                    None,
                    self.do_palette_buttons_cb,
                    None,
                    arg=i))

        if not add_buttons:
            # And we need an extra button for the overflow
            self._overflow_palette_button = self._radio_button_factory(
                'overflow',
                None,
                self._overflow_palette_cb,
                None,
                _('Palettes'),
                palette_group)

    def _overflow_palette_cb(self, button):
        _logger.debug('overflow palette cb')
        if self._overflow_palette:
            if not self._overflow_palette.is_up():
                self._overflow_palette.popup(
                    immediate=True,
                    state=self._overflow_palette.SECONDARY)
            else:
                self._overflow_palette.popdown(immediate=True)
            return

    def _make_load_save_buttons(self, toolbar):
        ''' Additional toolbar buttons for file IO '''
        home = os.environ['HOME']
        self.share_button = self._add_button('shareoff',
                                             _('Sharing blocks disabled'),
                                             self._share_cb, toolbar)
        if self.has_toolbarbox:
            self._add_separator(toolbar, expand=False, visible=True)
            save_button = self._add_button(
                'save', _('Save'), self._save_load_palette_cb,
                toolbar)
            self._save_palette = save_button.get_palette()
            button_box = gtk.VBox()
            self.save_as_image, label = self._add_button_and_label(
                'image-saveoff', _('Save as image'), self.do_save_as_image_cb,
                None, button_box)
            self.save_as_icon = self._add_button_and_label(
                'image-saveoff', _('Save as icon'), self.do_save_as_icon_cb,
                None, button_box)
            # TRANS: ODP is Open Office presentation
            self.save_as_odp = self._add_button_and_label(
                'odp-saveoff', _('Save as ODP'), self.do_save_as_odp_cb,
                None, button_box)
            self.save_as_icon[0].get_parent().connect(
                'expose-event',
                self._save_as_icon_expose_cb)

            self.save_as_odp[0].get_parent().connect(
                'expose-event',
                self._save_as_odp_expose_cb)

            self.save_as_logo, label = self._add_button_and_label(
                'logo-saveoff', _('Save as Logo'), self.do_save_as_logo_cb,
                None, button_box)
            self.save_as_python, label = self._add_button_and_label(
                'python-saveoff', _('Save as Python'),
                self.do_save_as_python_cb,
                None, button_box)
            self.keep_button2, self.keep_label2 = self._add_button_and_label(
                'filesaveoff', _('Save snapshot'), self.do_keep_cb,
                None, button_box)

            load_button = self._add_button(
                'load', _('Load'), self._save_load_palette_cb,
                toolbar)
            button_box.show_all()
            self._save_palette.set_content(button_box)

            self._load_palette = load_button.get_palette()
            button_box = gtk.VBox()
            # When screen is in portrait mode, the buttons don't fit
            # on the main toolbar, so put them here.
            self.samples_button2, self.samples_label2 = \
                self._add_button_and_label('ta-open',
                                           _('Load example'),
                                           self.do_samples_cb,
                                           None,
                                           button_box)

            self.load_ta_project, label = self._add_button_and_label(
                'load-from-journal', _('Open'),
                self.do_load_ta_project_cb, True, button_box)
            self.load_ta_project, label = self._add_button_and_label(
                'load-from-journal', _('Add project'),
                self.do_load_ta_project_cb, False, button_box)
            # Only enable plugin loading if installed in $HOME
            if activity.get_bundle_path()[0:len(home)] == home:
                self.load_ta_plugin, label = self._add_button_and_label(
                    'pluginoff', _('Load plugin'),
                    self.do_load_ta_plugin_cb, None, button_box)
            self.load_python, label = self._add_button_and_label(
                'pippy-openoff', _('Load Python block'),
                self.do_load_python_cb, None, button_box)
            button_box.show_all()
            self._load_palette.set_content(button_box)
        else:
            self.save_as_image = self._add_button(
                'image-saveoff', _('Save as image'), self.do_save_as_image_cb,
                toolbar)
            self.save_as_icon = self._add_button(
                'image-saveoff', _('Save as icon'), self.do_save_as_icon_cb,
                toolbar)
            # TRANS: ODP is Open Office presentation
            self.save_as_odp = self._add_button(
                'odp-saveoff', _('Save as ODP'), self.do_save_as_odp_cb,
                toolbar)

            self.save_as_icon.connect('expose-event',
                                      self._save_as_icon_expose_cb)
            self.save_as_odp.connect('expose-event',
                                     self._save_as_odp_expose_cb)

            self.save_as_logo = self._add_button(
                'logo-saveoff', _('Save as Logo'), self.do_save_as_logo_cb,
                toolbar)
            self.save_as_python = self._add_button(
                'python-saveoff', _('Save as Python'),
                self.do_save_as_python_cb,
                toolbar)
            self.keep_button = self._add_button(
                'filesaveoff', _('Save snapshot'), self.do_keep_cb, toolbar)
            self.load_ta_project = self._add_button(
                'load-from-journal', _('Add project'),
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
        palette = button.get_palette()
        if palette:
            if not palette.is_up():
                palette.popup(immediate=True, state=palette.SECONDARY)
            else:
                palette.popdown(immediate=True)

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
        self.stop_turtle_button = self._add_button(
            'hideshowoff', _('Hide blocks'), self.do_stop_cb, toolbar,
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

    def _fixed_resize_cb(self, widget=None, rect=None):
        ''' If a toolbar opens or closes, we need to resize the vbox
        holding out scrolling window. '''
        self.vbox.set_size_request(rect[2], rect[3])

    def _setup_scrolled_window(self):
        ''' Create a scrolled window to contain the turtle canvas. We
        add a Fixed container in order to position text Entry widgets
        on top of string and number blocks.'''
        self.fixed = gtk.Fixed()
        self.fixed.connect('size-allocate', self._fixed_resize_cb)
        self.fixed.show()
        self.set_canvas(self.fixed)
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_size_request(gtk.gdk.screen_width(),
                                   gtk.gdk.screen_height() -
                                   2 * style.GRID_CELL_SIZE)
        self.sw = gtk.ScrolledWindow()
        # self.set_canvas(self.sw)
        self.vbox.pack_end(self.sw, True, True)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.show()
        self.vbox.show()
        self.fixed.put(self.vbox, 0, 0)

        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width() * 2,
                                gtk.gdk.screen_height() * 2)
        canvas.show()

        self.sw.add_with_viewport(canvas)
        self.sw.get_hadjustment().connect('value-changed', self._scroll_cb)
        self.sw.get_vadjustment().connect('value-changed', self._scroll_cb)
        self.hadj_value = 0
        self.vadj_value = 0
        canvas.show()
        self.sw.show()
        self.show_all()

        return canvas

    def _scroll_cb(self, window):
        ''' The scrolling window has been changed, so move the
        floating palettes. '''
        self.hadj_value = self.sw.get_hadjustment().get_value()
        self.vadj_value = self.sw.get_vadjustment().get_value()
        if not self._defer_palette_move:
            gobject.idle_add(self.adjust_palette)

    def _setup_canvas(self, canvas_window):
        ''' Initialize the turtle art canvas. '''
        cr = canvas_window.window.cairo_create()
        self.turtle_canvas = cr.get_target().create_similar(
            cairo.CONTENT_COLOR, gtk.gdk.screen_width() * 2,
            gtk.gdk.screen_height() * 2)
        self.tw = TurtleArtWindow(canvas_window,
                                  activity.get_bundle_path(),
                                  activity.get_bundle_path(),
                                  self,
                                  mycolors=profile.get_color().to_string(),
                                  mynick=profile.get_nick_name(),
                                  turtle_canvas=self.turtle_canvas)
        self.tw.window.grab_focus()
        self.tw.save_folder = os.path.join(
            os.environ['SUGAR_ACTIVITY_ROOT'], 'data')

        if hasattr(self, 'get_window') and \
           hasattr(self.get_window(), 'get_cursor'):
            self._old_cursor = self.get_window().get_cursor()
        else:
            self._old_cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)

        # Try restoring an existing project...
        if self._jobject and self._jobject.file_path:
            if hasattr(self, 'get_window'):
                _logger.debug('setting watch cursor')
                if hasattr(self.get_window(), 'get_cursor'):
                    self._old_cursor = self.get_window().get_cursor()
                    self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self.read_file(self._jobject.file_path)
        else:  # ...or else, load a Start Block onto the canvas.
            self.tw.load_start()

        self.tw.copying_blocks = False
        self.tw.sharing_blocks = False
        self.tw.saving_blocks = False

    def _setup_sharing(self):
        ''' Setup the Collabora stack. '''
        self._collaboration = Collaboration(self.tw, self)
        self._collaboration.setup()

    def _joined_cb(self, widget):
        if self._joined_alert is not None:
            self.remove_alert(self._joined_alert)
            self._joined_alert = None
        self.set_canvas(self.fixed)

    def send_xy(self):
        ''' Resync xy position (and orientation) of my turtle. '''
        self._collaboration.send_my_xy()

    def _notify_active_cb(self, widget, event):
        ''' Sugar notify us that the activity is becoming active or
        inactive. Notify plugins. '''
        if self.props.active:
            _logger.debug('going to foreground')
            self.tw.foreground_plugins()
        else:
            # If we go to background, stop media playing.
            if self.tw.gst_available:
                from TurtleArt.tagplay import stop_media
                stop_media(self.tw.lc)
            self.tw.background_plugins()

    def can_close(self):
        ''' Override activity class can_close inorder to notify plugins '''
        self.tw.quit_plugins()
        # Clean up temporary files
        if os.path.exists(TMP_SVG_PATH):
            os.remove(TMP_SVG_PATH)
        if os.path.exists(TMP_ODP_PATH):
            os.remove(TMP_ODP_PATH)
        return True

    def write_file(self, file_path):
        ''' Write the project to the Journal. '''
        data_to_file(self.tw.assemble_data_to_save(), file_path)
        self.metadata['mime_type'] = MIMETYPE[0]
        self.metadata['turtle blocks'] = ''.join(self.tw.used_block_list)
        # Deprecated
        # self.metadata['public'] = data_to_string(['activity count',
        #                                           'turtle blocks'])
        if self.tw.palette:
            self.metadata['palette'] = str(self.tw.selected_palette)
        else:
            self.metadata['palette'] = '-1'
        self.metadata['orientation'] = str(self.tw.orientation)
        if HAS_GCONF:
            self.client.set_int(self._ORIENTATION, self.tw.orientation)
        if len(self.error_list) > 0:
            errors = []
            if 'error_list' in self.metadata:
                for error in data_from_string(self.metadata['error_list']):
                    errors.append(error)
            for error in self.error_list:
                errors.append(error)
            self.metadata['error_list'] = data_to_string(errors)
        _logger.debug('Wrote to file: %s' % (file_path))

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
                complete_plugin_install(self, tmp_dir, tmp_path, plugin_path,
                                        plugin_name, file_info)
            elif response_id is gtk.RESPONSE_CANCEL:
                _logger.debug('cancel install')
                self.remove_alert(alert)
                cancel_plugin_install(self, tmp_dir)

        alert.connect('response', _reload_plugin_alert_response_cb, self,
                      tmp_dir, tmp_path, plugin_path, plugin_name, file_info)
        self.add_alert(alert)
        alert.show()

    def read_file(self, file_path, plugin=False):
        ''' Open a project or plugin and then run it. '''
        if hasattr(self, 'tw') and self.tw is not None:
            if not hasattr(self, '_old_cursor'):
                self._old_cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)
            _logger.debug('Read file: %s' % (file_path))
            # Could be a plugin or deprecated gtar or tar file...
            if plugin or file_path.endswith(('.gtar', '.tar', '.tar.gz')):
                try:
                    # Copy to tmp file since some systems had trouble
                    # with gunzip directly from datastore
                    datapath = get_path(activity, 'instance')
                    tmpfile = os.path.join(datapath, 'tmpfile.tar.gz')
                    subprocess.call(['cp', file_path, tmpfile])
                    status = subprocess.call(['gunzip', tmpfile])
                    if status == 0:
                        _logger.debug('tarfile.open %s' % (tmpfile[:3]))
                        tar_fd = tarfile.open(tmpfile[:-3], 'r')
                    else:
                        _logger.debug('tarfile.open %s' % (tmpfile))
                        tar_fd = tarfile.open(tmpfile, 'r')
                except:
                    _logger.debug('tarfile.open %s' % (file_path))
                    tar_fd = tarfile.open(file_path, 'r')

                tmp_dir = tempfile.mkdtemp()
                _logger.debug('tmp_dir %s' % (tmp_dir))

                try:
                    tar_fd.extractall(tmp_dir)
                    if not plugin:
                        turtle_code = os.path.join(tmp_dir, 'ta_code.ta')
                        if os.path.exists(turtle_code):
                            gobject.idle_add(self._project_loader, turtle_code)
                    else:
                        _logger.debug('load a plugin from %s' % (tmp_dir))
                        load_a_plugin(self, tmp_dir)
                        self.restore_cursor()
                except:
                    _logger.debug('Could not extract files from %s.' %
                                  (file_path))
                    self.restore_cursor()
                finally:
                    if not plugin:
                        shutil.rmtree(tmp_dir)
                    tar_fd.close()
                    # Remove tmpfile.tar
                    subprocess.call(['rm',
                                     os.path.join(datapath, 'tmpfile.tar')])

            # ...otherwise, assume it is a .ta file.
            else:
                gobject.idle_add(self._project_loader, file_path)

        else:
            _logger.debug('Deferring reading file %s' % (file_path))

    def _project_loader(self, file_path):
        ''' Load the turtle file and then restore cursor '''
        _logger.debug('Opening:' + file_path)
        if not hasattr(self, '_create_new'):
            self._create_new = False
        self.tw.load_files(file_path, self._create_new)
        self.restore_cursor()
        if hasattr(self, '_tmp_dsobject') and self._tmp_dsobject is not None:
            _logger.debug('cleaning up after %s' %
                          (self._tmp_dsobject.file_path))
            self._tmp_dsobject.destroy()
            self._tmp_dsobject = None

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

    def restore_cursor(self):
        ''' No longer copying or sharing, so restore standard cursor. '''
        self.tw.copying_blocks = False
        self.tw.sharing_blocks = False
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self.get_window().set_cursor(self._old_cursor)
            else:
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    def _copy_cb(self, button):
        ''' Copy to the clipboard. '''
        if self.tw.copying_blocks:
            self.tw.copying_blocks = False
            self.restore_cursor()
        else:
            self.tw.copying_blocks = True
            if hasattr(self, 'get_window'):
                if hasattr(self.get_window(), 'get_cursor'):
                    self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

    def _save_macro_cb(self, button):
        ''' Save stack to macros_path '''
        if self.tw.saving_blocks:
            self.tw.saving_blocks = False
            self.restore_cursor()
        else:
            self.tw.saving_blocks = True
            if hasattr(self, 'get_window'):
                if hasattr(self.get_window(), 'get_cursor'):
                    self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

    def _delete_macro_cb(self, button):
        ''' Delete stack from macros_path '''
        if self.tw.deleting_blocks:
            self.tw.deleting_blocks = False
            self.restore_cursor()
        else:
            self.tw.deleting_blocks = True
            if hasattr(self, 'get_window'):
                if hasattr(self.get_window(), 'get_cursor'):
                    self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

    def _paste_cb(self, button):
        ''' Paste from the clipboard. '''
        if self.tw.copying_blocks:
            self.restore_cursor()
        clipboard = gtk.Clipboard()
        _logger.debug('Paste to the project.')
        text = clipboard.wait_for_text()
        if text is not None:
            if self.tw.selected_blk is not None and \
               self.tw.selected_blk.name == 'string' and \
               text[0:2] != '[[':  # Don't paste block data into a string
                self.tw.paste_text_in_block_label(text)
                self.tw.selected_blk.resize()
            else:
                self.tw.process_data(data_from_string(text),
                                     self.tw.paste_offset)
                self.tw.paste_offset += PASTE_OFFSET

    def _undo_cb(self, button):
        ''' Restore most recent item added to the trash '''
        self.tw.restore_latest_from_trash()

    def _share_cb(self, button):
        ''' Share a stack of blocks. '''
        if self.tw.sharing_blocks:
            self.restore_cursor()
        else:
            self.tw.sharing_blocks = True
            if hasattr(self, 'get_window'):
                if hasattr(self.get_window(), 'get_cursor'):
                    self._old_cursor = self.get_window().get_cursor()
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

    def empty_trash_alert(self, title, msg):
        ''' We get confirmation from the user before emptying the trash '''
        alert = ConfirmationAlert()
        alert.props.title = title
        alert.props.msg = msg

        def _empty_trash_alert_response_cb(alert, response_id, self):
            if response_id is gtk.RESPONSE_OK:
                _logger.debug('emptying the trash')
                self.remove_alert(alert)
                self.tw._empty_trash()
            elif response_id is gtk.RESPONSE_CANCEL:
                _logger.debug('cancel emptying the trash')
                self.remove_alert(alert)

        alert.connect('response', _empty_trash_alert_response_cb, self)
        self.add_alert(alert)
        alert.show()

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
        return separator

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

        if name not in help_strings:
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
        if toolbar is not None:
            if hasattr(toolbar, 'insert'):  # Add button to the main toolbar...
                toolbar.insert(button, position)
            else:  # ...or a secondary toolbar.
                toolbar.props.page.insert(button, position)
        button.show()
        if tooltip is not None:
            button.set_tooltip(tooltip)
        return button

    def _add_button_and_label(self, name, tooltip, cb, cb_args, box):
        ''' Add a button and a label to a box '''
        button_and_label = gtk.HBox()
        button = self._add_button(name, None, cb, None, arg=cb_args)
        button_and_label.pack_start(button, False, False, padding=5)
        label = gtk.Label(tooltip)
        label.set_justify(gtk.JUSTIFY_LEFT)
        label.set_line_wrap(True)
        label.show()
        button_and_label.pack_start(label, False, False, padding=5)
        box.pack_start(button_and_label)
        button_and_label.show()
        return button, label

    def restore_state(self):
        ''' Anything that needs restoring after a clear screen can go here '''
        pass

    def hide_store(self, widget=None):
        if self._sample_window is not None:
            self._sample_box.hide()

    def _create_store(self, widget=None):
        if self._sample_window is None:
            self._sample_box = gtk.EventBox()
            self._sample_window = gtk.ScrolledWindow()
            self._sample_window.set_policy(gtk.POLICY_NEVER,
                                           gtk.POLICY_AUTOMATIC)
            width = gtk.gdk.screen_width() / 2
            height = gtk.gdk.screen_height() / 2
            self._sample_window.set_size_request(width, height)
            self._sample_window.show()

            store = gtk.ListStore(gtk.gdk.Pixbuf, str)

            icon_view = gtk.IconView()
            icon_view.set_model(store)
            icon_view.set_selection_mode(gtk.SELECTION_SINGLE)
            icon_view.connect('selection-changed', self._sample_selected,
                              store)
            icon_view.set_pixbuf_column(0)
            icon_view.grab_focus()
            self._sample_window.add_with_viewport(icon_view)
            icon_view.show()
            self._fill_samples_list(store)

            width = gtk.gdk.screen_width() / 4
            height = gtk.gdk.screen_height() / 4

            self._sample_box.add(self._sample_window)
            self.fixed.put(self._sample_box, width, height)

        self._sample_window.show()
        self._sample_box.show()

    def _get_selected_path(self, widget, store):
        try:
            iter_ = store.get_iter(widget.get_selected_items()[0])
            image_path = store.get(iter_, 1)[0]

            return image_path, iter_
        except:
            return None

    def _sample_selected(self, widget, store):
        selected = self._get_selected_path(widget, store)

        if selected is None:
            self._selected_sample = None
            self._sample_window.hide()
            return

        image_path, _iter = selected
        iter_ = store.get_iter(widget.get_selected_items()[0])
        image_path = store.get(iter_, 1)[0]

        self._selected_sample = image_path
        self._sample_window.hide()

        self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        gobject.idle_add(self._sample_loader)

    def _sample_loader(self):
        # Convert from thumbnail path to sample path
        basename = os.path.basename(self._selected_sample)[:-4]
        for suffix in ['.ta', '.tb']:
            file_path = os.path.join(activity.get_bundle_path(),
                                     'samples', basename + suffix)
            if os.path.exists(file_path):
                self.tw.load_files(file_path)
                break
        self.tw.load_save_folder = os.path.join(activity.get_bundle_path(),
                                                'samples')
        self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    def _fill_samples_list(self, store):
        '''
        Append images from the artwork_paths to the store.
        '''
        for filepath in self._scan_for_samples():
            pixbuf = None
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                filepath, 100, 100)
            store.append([pixbuf, filepath])

    def _scan_for_samples(self):
        samples = sorted(
            glob.glob(
                os.path.join(
                    activity.get_bundle_path(),
                    'samples',
                    'thumbnails',
                    '*.png')))
        return samples

    def is_toolbar_expanded(self):
        if self.palette_toolbar_button.is_expanded():
            return True
        elif self.edit_toolbar_button.is_expanded():
            return True
        elif self.view_toolbar_button.is_expanded():
            return True
        elif self.activity_toolbar_button.is_expanded():
            return True
        return False
