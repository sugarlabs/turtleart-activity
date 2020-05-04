# -*- coding: utf-8 -*-
# Copyright (c) 2007, Playful Invention Company
# Copyright (c) 2008-14, Walter Bender
# Copyright (c) 2009-11 Raúl Gutiérrez Segalés
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

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

import os
import sys
import subprocess
import errno
from gettext import gettext as _

import cairo
import gi
gi.require_version('PangoCairo', '1.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GdkPixbuf
from gi.repository import Pango
from gi.repository import PangoCairo

_GST_AVAILABLE = False


from random import uniform
from math import atan2, pi
DEGTOR = 2 * pi / 360

import locale

from .taconstants import (
    HORIZONTAL_PALETTE,
    BLOCK_SCALE,
    MEDIA_SHAPES,
    STATUS_SHAPES,
    OVERLAY_SHAPES,
    TOOLBAR_SHAPES,
    TAB_LAYER,
    RETURN,
    OVERLAY_LAYER,
    CATEGORY_LAYER,
    BLOCKS_WITH_SKIN,
    ICON_SIZE,
    PALETTE_WIDTH,
    SKIN_PATHS,
    MACROS,
    Color,
    KEY_DICT,
    TOP_LAYER,
    BLOCK_LAYER,
    OLD_NAMES,
    DEFAULT_TURTLE,
    TURTLE_LAYER,
    EXPANDABLE,
    NO_IMPORT,
    TEMPLATES,
    PYTHON_SKIN,
    PALETTE_HEIGHT,
    STATUS_LAYER,
    OLD_DOCK,
    EXPANDABLE_ARGS,
    XO1,
    XO15,
    XO175,
    XO30,
    XO4,
    TITLEXY,
    CONTENT_ARGS,
    CONSTANTS,
    EXPAND_SKIN,
    PROTO_LAYER,
    EXPANDABLE_FLOW,
    SUFFIX,
    TMP_SVG_PATH,
    TMP_ODP_PATH,
    Vector,
    PASTE_OFFSET)
from .tapalette import (palette_names, palette_blocks, expandable_blocks,
                        block_names, content_blocks, default_values,
                        special_names, block_styles, help_strings,
                        string_or_number_args, make_palette,
                        palette_name_to_index, palette_init_on_start,
                        palette_i18n_names)
from .talogo import (LogoCode, logoerror)
from .tacanvas import TurtleGraphics
from .tablock import (Blocks, Block, Media, media_blocks_dictionary)
from .taturtle import (Turtles, Turtle)
from .tautils import (magnitude, get_load_name, get_save_name, data_from_file,
                      data_to_file, round_int, get_id, get_pixbuf_from_journal,
                      movie_media_type, audio_media_type, image_media_type,
                      save_picture, calc_image_size, get_path, hide_button_hit,
                      show_button_hit, chooser_dialog, arithmetic_check, xy,
                      find_block_to_run, find_top_block, journal_check,
                      find_group, find_blk_below, data_to_string,
                      find_start_stack, get_hardware, debug_output,
                      error_output, find_hat, find_bot_block,
                      restore_clamp, collapse_clamp, data_from_string,
                      increment_name, get_screen_dpi, is_writeable)
from .tasprite_factory import (svg_str_to_pixbuf, svg_from_file)
from .tapalette import block_primitives
from .tapaletteview import PaletteView
from .taselector import (Selector, create_toolbar_background)
from .sprites import (Sprites, Sprite)

from .util.menubuilder import make_checkmenu_item

from .tagplay import stop_media

_MOTION_THRESHOLD = 6
_SNAP_THRESHOLD = 200
_NO_DOCK = (100, 100)  # Blocks cannot be docked
_BUTTON_SIZE = 32
_MARGIN = 5
_UNFULLSCREEN_VISIBILITY_TIMEOUT = 2
_PLUGIN_SUBPATH = 'plugins'
_MACROS_SUBPATH = 'macros'

# the global instances of single-instance classes
global_objects = {}
plugins_in_use = []


class TurtleArtWindow():

    ''' TurtleArt Window class abstraction  '''

    def __init__(self, canvas_window, lib_path, share_path, parent=None,
                 activity=None, mycolors=None, mynick=None,
                 turtle_canvas=None, running_sugar=True,
                 running_turtleart=True):
        '''
        parent: the GTK Window that TA runs in
        activity: the object that instantiated this TurtleArtWindow (in
                  GNOME, a TurtleMain instance, in Sugar, the Activity
                  instance)
        running_turtleart: are we running TA or exported python code?
        '''
        self.parent = parent
        self.turtle_canvas = turtle_canvas
        self._default_turtle_name = DEFAULT_TURTLE
        self._loaded_project = ''
        self._sharing = False
        self._timeout_tag = [0]
        self.send_event = None  # method to send events over the network
        self.gst_available = _GST_AVAILABLE
        self.running_sugar = False
        self.nick = None
        self.running_turtleart = running_turtleart
        if isinstance(canvas_window, Gtk.DrawingArea):
            self.interactive_mode = True
            self.window = canvas_window
            self.window.set_can_focus(True)
            self.window.show_all()
            if running_sugar:
                self.parent.show_all()
                self.running_sugar = True

                from sugar3 import profile

                self.nick = profile.get_nick_name()
                self.macros_path = os.path.join(
                    get_path(parent, 'data'), _MACROS_SUBPATH)
            else:
                # Make sure macros_path is somewhere writable
                self.macros_path = os.path.join(
                    os.path.expanduser('~'), 'Activities',
                    os.path.basename(lib_path), _MACROS_SUBPATH)
            self._setup_events()
        else:
            self.interactive_mode = False
            self.window = canvas_window
            self.running_sugar = False

        if activity is not None:
            self.activity = activity
        else:
            self.activity = parent

        # paths
        self.lib_path = lib_path
        self.share_path = share_path
        self.load_save_folder = os.path.join(self.share_path, 'samples')
        self.py_load_save_folder = os.path.join(self.share_path, 'pysamples')
        self.images_path = os.path.join(self.share_path, 'images')

        self._py_cache = {}
        self.used_block_list = []  # Which blocks has the user used?
        self.save_folder = None
        self.save_file_name = None

        # dimensions
        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height()
        self.rect = Gdk.Rectangle()

        self.no_help = False
        self.last_label = None
        self._autohide_shape = True
        self.keypress = ''
        self.keyvalue = 0
        self.keyboard = 0
        self._focus_out_id = None
        self._insert_text_id = None
        self._text_to_check = False
        self.mouse_flag = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.update_counter = 0
        self.running_blocks = False
        self.saving_blocks = False
        self.copying_blocks = False
        self.sharing_blocks = False
        self.deleting_blocks = False

        # find out which character to use as decimal point
        try:
            locale.setlocale(locale.LC_NUMERIC, '')
        except locale.Error:
            debug_output('unsupported locale', self.running_sugar)
        self.decimal_point = locale.localeconv()['decimal_point']
        if self.decimal_point == '' or self.decimal_point is None:
            self.decimal_point = '.'

        # settings that depend on the hardware
        self.orientation = HORIZONTAL_PALETTE
        self.hw = get_hardware()
        self.lead = 1.0
        if self.hw in (XO1, XO15, XO175, XO4):
            self.scale = 1.0
            self.entry_scale = 0.67
            if self.hw == XO1:
                self.color_mode = '565'
            else:
                self.color_mode = '888'
        else:
            self.scale = 1.0
            self.entry_scale = 1.0
            self.color_mode = '888'  # TODO: Read visual mode from gtk image
        self._set_screen_dpi()

        self.block_scale = BLOCK_SCALE[3]
        self.trash_scale = 0.5
        self.myblock = {}
        self.python_code = None
        self.nop = 'nop'
        self.loaded = 0
        self.step_time = 0
        # show/ hide palettes depending on whether we're running in TA or not
        self.hide = not self.running_turtleart
        self.palette = self.running_turtleart
        self.coord_scale = 1
        self.buddies = []
        self._saved_string = ''
        self._saved_action_name = ''
        self._saved_box_name = ''
        self.dx = 0
        self.dy = 0
        self.media_shapes = {}
        self.cartesian = False
        self.polar = False
        self.metric = False
        self.overlay_shapes = {}
        self.toolbar_shapes = {}
        self.toolbar_offset = 0
        self.status_spr = None
        self.status_shapes = {}
        self.toolbar_spr = None
        self.palette_button = []
        self.palette_views = []
        self.trash_stack = []
        self.selected_palette = None
        self.previous_palette = None
        self.selectors = []
        self.selected_selector = None
        self._highlighted_blk = None
        self.selected_blk = None
        self.selected_spr = None
        self.selected_turtle = None
        self.drag_group = None
        self.drag_turtle = 'move', 0, 0
        self.drag_pos = 0, 0
        self.dragging_canvas = [False, 0, 0]
        self.turtle_movement_to_share = None
        # Don't paste on top of where you copied.
        self.paste_offset = PASTE_OFFSET

        # common properties of all blocks (font size, decimal point, ...)
        self.block_list = Blocks(font_scale_factor=self.scale,
                                 decimal_point=self.decimal_point)
        if self.interactive_mode:
            self.sprite_list = Sprites(self.window)
        else:
            self.sprite_list = None

        # canvas object that supports the basic drawing functionality
        self.canvas = TurtleGraphics(self, self.width, self.height)
        if self.hw == XO175 and self.canvas.width == 1024:
            self.hw = XO30
        if self.interactive_mode:
            self.sprite_list.set_cairo_context(self.canvas.canvas)

        self.turtles = Turtles(self)
        if self.nick is not None:
            # FIXME Review assumed code changes here
            self._default_turtle_name = str(self.nick)
            self.turtles._default_turtle_name = str(self.nick)
            self.turtles.set_default_turtle_name(self.nick)
        if mycolors is None:
            Turtle(self.turtles, self.turtles.get_default_turtle_name())
        else:
            Turtle(self.turtles, self.turtles.get_default_turtle_name(),
                   mycolors.split(','))
        self.turtles.set_active_turtle(
            self.turtles.get_turtle(self.turtles.get_default_turtle_name()))
        self.turtles.get_active_turtle().show()

        self.canvas.clearscreen()

        self._configure_cb(None)

        self.icon_paths = [os.path.join(self.share_path, 'icons')]

        self.lc = LogoCode(self)

        self.turtleart_plugins = {}
        self.turtleart_favorites_plugins = []
        # self.turtleart_plugin_list = {}
        self.saved_pictures = []
        self.block_operation = ''

        # only in TA: setup basic palettes
        if self.running_turtleart:
            from .tabasics import Palettes
            self._basic_palettes = Palettes(self)

        global_objects["window"] = self
        global_objects["canvas"] = self.canvas
        global_objects["logo"] = self.lc
        global_objects["turtles"] = self.turtles

        if self.interactive_mode:
            GLib.idle_add(self._lazy_init)
        else:
            self._init_plugins()
            self._setup_plugins()

    def get_global_objects(self):
        return global_objects

    def get_init_complete(self):
        if self.running_turtleart:
            return self.activity.init_complete
        else:
            return True

    def _lazy_init(self):
        self._init_plugins()
        self._setup_plugins()
        self._setup_misc()

        if self.running_turtleart:
            self._basic_palettes.make_trash_palette()
            for name in palette_init_on_start:
                debug_output('initing palette %s' % (name), self.running_sugar)
                self.show_toolbar_palette(palette_names.index(name),
                                          init_only=False,
                                          regenerate=True,
                                          show=False)

            self.show_toolbar_palette(0,
                                      init_only=False,
                                      regenerate=True,
                                      show=True)

            if self.running_sugar:
                self.activity.check_buttons_for_fit()
                self.activity.update_palette_from_metadata()

    def _set_screen_dpi(self):
        dpi = get_screen_dpi()
        if self.hw in (XO1, XO15, XO175, XO4):
            dpi = 133  # Tweek because of XO display peculiarities
        font_map_default = PangoCairo.font_map_get_default()
        font_map_default.set_resolution(dpi)

    def _tablet_mode(self):
        ''' DEPRECATED '''
        return False  # Sugar will autoscroll the window for me

    def _get_plugins_from_plugins_dir(self, paths):
        ''' Look for plugin files in plugin dir. '''
        plugin_files = {}
        for path in paths:
            candidates = os.listdir(path)
            for dirname in candidates:
                pname = os.path.join(path, dirname, dirname + '.py')
                if os.path.exists(pname):
                    plugin_files[dirname] = path
        return plugin_files

    def _init_plugins(self):
        ''' Try importing plugin files from the plugin dir. '''
        paths = set()

        homepath = os.path.join(
            os.path.expanduser('~'),
            'Activities',
            os.path.basename(
                self.lib_path),
            _PLUGIN_SUBPATH)
        if os.path.exists(homepath):
            paths.add(homepath)

        path = os.path.join(self.lib_path, _PLUGIN_SUBPATH)
        if os.path.exists(path):
            sys.path.append(self.lib_path)
            paths.add(path)

        turtleart_plugin_list = self._get_plugins_from_plugins_dir(paths)
        plist = sorted(turtleart_plugin_list.keys())
        for plugin_dir in plist:
            plugin_path = turtleart_plugin_list[plugin_dir]
            # add icons paths of all plugins
            self._add_plugin_icon_dir(os.path.join(plugin_path, plugin_dir))
            status = True
            if not self.running_sugar and hasattr(self.activity, 'client'):
                gconf_path = self.activity._PLUGINS_PATH + plugin_dir
                try:
                    status = (self.activity.client.get_int(gconf_path) == 1)
                except BaseException:
                    pass
                if hasattr(self.activity, '_plugin_menu'):
                    make_checkmenu_item(
                        self.activity._plugin_menu,
                        plugin_dir,
                        self.activity._do_toggle_plugin_cb,
                        status)
            if status:
                self.init_plugin(plugin_dir, plugin_path)
                self.turtleart_favorites_plugins.append(plugin_dir)
        if not self.running_sugar:
            if hasattr(self.activity, '_plugin_menu'):
                self.activity._plugin_menu.show_all()

    def init_plugin(self, plugin_dir, plugin_path):
        ''' Initialize plugin in plugin_dir '''
        plugin_class = plugin_dir.capitalize()
        f = 'def f(self): from plugins.%s.%s import %s; return %s(self)' \
            % (plugin_dir, plugin_dir, plugin_class, plugin_class)
        plugins = {}
        # NOTE: When debugging plugins, it may be useful to not trap errors
        try:
            exec(f, globals(), plugins)
            self.turtleart_plugins[plugin_dir] = list(plugins.values())[
                0](self)
            debug_output('Successfully importing %s' % (plugin_class),
                         self.running_sugar)
            # Add the icon dir to the icon_theme search path
            self._add_plugin_icon_dir(os.path.join(plugin_path, plugin_dir))
            # Add the plugin to the list of global objects
            global_objects[plugin_class] = self.turtleart_plugins[plugin_dir]
        except Exception as e:
            debug_output('Failed to load %s: %s' % (plugin_class, str(e)),
                         self.running_sugar)

    def _add_plugin_icon_dir(self, dirname):
        ''' If there is an icon subdir, add it to the search path. '''
        icon_theme = Gtk.IconTheme.get_default()
        icon_path = os.path.join(dirname, 'icons')
        if os.path.exists(icon_path):
            if icon_path not in self.icon_paths:
                icon_theme.append_search_path(icon_path)
                self.icon_paths.append(icon_path)

    def _get_plugin_instance(self, plugin_name):
        ''' Returns the plugin 'plugin_name' instance '''
        if plugin_name in self.turtleart_plugins:
            return self.turtleart_plugins[plugin_name]
        else:
            return None

    def _setup_plugins(self):
        ''' Initial setup -- called just once. '''
        for plugin in sorted(self.turtleart_plugins.keys()):
            try:
                self.turtleart_plugins[plugin].setup()
            except Exception as e:
                debug_output('Plugin %s failed during setup: %s' %
                             (plugin, str(e)), self.running_sugar)
                # If setup fails, remove the plugin from the list
                self.turtleart_plugins.pop(plugin)

    def start_plugins(self):
        ''' Start is called everytime we execute blocks. '''
        for plugin in list(self.turtleart_plugins.values()):
            if hasattr(plugin, 'start'):
                try:
                    plugin.start()
                except Exception as e:
                    debug_output('Plugin %s failed during start: %s' %
                                 (plugin, str(e)), self.running_sugar)

    def stop_plugins(self):
        ''' Stop is called whenever we stop execution. '''
        for plugin in list(self.turtleart_plugins.values()):
            if hasattr(plugin, 'stop'):
                try:
                    plugin.stop()
                except Exception as e:
                    debug_output('Plugin %s failed during stop: %s' %
                                 (plugin, str(e)), self.running_sugar)

    def clear_plugins(self):
        ''' Clear is called from the clean block and erase button. '''
        for plugin in list(self.turtleart_plugins.values()):
            if hasattr(plugin, 'clear'):
                try:
                    plugin.clear()
                except Exception as e:
                    debug_output('Plugin %s failed during clear: %s' %
                                 (plugin, str(e)), self.running_sugar)

    def background_plugins(self):
        ''' Background is called when we are pushed to the background. '''
        for plugin in list(self.turtleart_plugins.values()):
            if hasattr(plugin, 'goto_background'):
                try:
                    plugin.goto_background()
                except Exception as e:
                    debug_output('Plugin %s failed during background: %s' %
                                 (plugin, str(e)), self.running_sugar)

    def foreground_plugins(self):
        ''' Foreground is called when we are return from the background. '''
        for plugin in list(self.turtleart_plugins.values()):
            if hasattr(plugin, 'return_to_foreground'):
                try:
                    plugin.return_to_foreground()
                except Exception as e:
                    debug_output('Plugin %s failed during foreground: %s' %
                                 (plugin, str(e)), self.running_sugar)

    def quit_plugins(self):
        ''' Quit is called upon program exit. '''
        for plugin in list(self.turtleart_plugins.values()):
            if hasattr(plugin, 'quit'):
                try:
                    plugin.quit()
                except Exception as e:
                    debug_output('Plugin %s failed during quit: %s' %
                                 (plugin, str(e)), self.running_sugar)

    def _setup_events(self):
        ''' Register the events we listen to. '''
        self.window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.window.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.window.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.window.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.window.drag_dest_set(Gtk.DestDefaults.ALL, [],
                                  Gdk.DragAction.COPY)
        self.window.drag_dest_set_target_list(None)
        self.window.drag_dest_add_text_targets()
        self.window.connect('draw', self._draw_cb)
        self.window.connect('button-press-event', self._buttonpress_cb)
        self.window.connect('button-release-event', self._buttonrelease_cb)
        self.window.connect('motion-notify-event', self._move_cb)
        self.window.connect('key-press-event', self._keypress_cb)
        self.window.connect('drag_data_received', self._drag_data_received)

        Gdk.Screen.get_default().connect('size-changed',
                                         self._configure_cb)

    def _show_unfullscreen_button(self):
        if self.activity._is_fullscreen and \
                self.activity.props.enable_fullscreen_mode:
            if not self.activity._unfullscreen_button.props.visible:
                self.activity._unfullscreen_button.show()
        # Reset the timer
        if hasattr(self.activity, '_unfullscreen_button_timeout_id'):
            if self.activity._unfullscreen_button_timeout_id is not None:
                GLib.source_remove(
                    self.activity._unfullscreen_button_timeout_id)
                self.activity._unfullscreen_button_timeout_id = None

            self.activity._unfullscreen_button_timeout_id = \
                GLib.timeout_add_seconds(
                    _UNFULLSCREEN_VISIBILITY_TIMEOUT,
                    self.__unfullscreen_button_timeout_cb)

    def __unfullscreen_button_timeout_cb(self):
        self.activity._unfullscreen_button.hide()
        self.activity._unfullscreen_button_timeout_id = None
        return False

    def _drag_data_received(self, w, context, x, y, data, info, time):
        ''' Handle dragging of block data from clipboard to canvas. '''
        debug_output(data.data, True)
        if data and data.format == 8 and data.data[0:2] == '[[':
            self.process_data(data_from_string(data.data),
                              self.paste_offset)
            self.paste_offset += PASTE_OFFSET
            context.finish(True, False, time)
        elif data and data.format == 8 and \
                self.selected_blk is not None and \
                self.selected_blk.name == 'string':
            bounds = self._text_buffer.get_bounds()
            self._text_buffer.set_text(
                self._text_buffer.get_text(
                    bounds[0], bounds[1]) + data.data, True)
            self._text_entry.set_buffer(self._text_buffer)
            context.finish(True, False, time)
        else:
            context.finish(False, False, time)

    def load_media_shapes(self):
        ''' Media shapes get positioned onto blocks '''
        for name in MEDIA_SHAPES:
            if name in self.media_shapes:
                continue
            if name[0:7] == 'journal' and not self.running_sugar:
                filename = 'file' + name[7:]
            else:
                filename = name
            # Try both images/ and plugins/*/images/
            for path in SKIN_PATHS:
                if os.path.exists(os.path.join(self.share_path, path,
                                               filename + '.svg')):
                    self.media_shapes[name] = svg_str_to_pixbuf(
                        svg_from_file(
                            os.path.join(self.share_path, path,
                                         filename + '.svg')))
                    break

    def _setup_misc(self):
        ''' Misc. sprites for status, overlays, etc. '''
        self.load_media_shapes()
        for i, name in enumerate(STATUS_SHAPES):
            # Temporary hack to use wider shapes
            if name in ['print', 'help', 'status'] and self.width > 1024:
                self.status_shapes[name] = svg_str_to_pixbuf(
                    svg_from_file(
                        os.path.join(self.images_path, name + '1200.svg')))
            else:
                self.status_shapes[name] = svg_str_to_pixbuf(
                    svg_from_file(
                        os.path.join(self.images_path, name + '.svg')))
        self.status_spr = Sprite(self.sprite_list, 0, self.height - 200,
                                 self.status_shapes['status'])
        self.status_spr.hide()
        self.status_spr.type = 'status'
        self._autohide_shape = True

        for name in OVERLAY_SHAPES:
            if name == 'Cartesian':
                continue
            self.overlay_shapes[name] = Sprite(
                self.sprite_list,
                int(self.width / 2 - 600),
                int(self.height / 2 - 450),
                svg_str_to_pixbuf(
                    svg_from_file('%s/%s.svg' % (self.images_path, name))))
            self.overlay_shapes[name].hide()
            self.overlay_shapes[name].type = 'overlay'

        self._create_scaled_cartesian_coordinates()

        if self.running_turtleart and not self.running_sugar:
            # offset = 2 * self.width - 55 * len(TOOLBAR_SHAPES)
            offset = 55 * (1 + len(palette_blocks))
            for i, name in enumerate(TOOLBAR_SHAPES):
                self.toolbar_shapes[name] = Sprite(
                    self.sprite_list, i * 55 + offset, 0,
                    svg_str_to_pixbuf(
                        svg_from_file(
                            os.path.join(
                                self.share_path, 'icons', '%s.svg' % (name)))))
                self.toolbar_shapes[name].set_layer(TAB_LAYER)
                self.toolbar_shapes[name].name = name
                self.toolbar_shapes[name].type = 'toolbar'
            self.toolbar_shapes['stopiton'].hide()

    def _create_scaled_cartesian_coordinates(self):
        # Cartesian overlay has to be scaled to match the coordinate_scale
        # 200 pixels in the graphic == height / 4. (10 units)
        pixbuf = svg_str_to_pixbuf(
            svg_from_file('%s/%s.svg' % (self.images_path, 'Cartesian')))

        if self.running_sugar:
            scale = self.height / 800.
        else:
            scale = self.height / 800.
            # scale = (self.height + ICON_SIZE) / 800.
        self.overlay_shapes['Cartesian'] = Sprite(
            self.sprite_list,
            int(self.width / 2 - 600),
            int(self.height / 2 - 450),
            pixbuf.scale_simple(int(1200 * scale),
                                int(900 * scale),
                                GdkPixbuf.InterpType.BILINEAR))
        self.overlay_shapes['Cartesian'].set_layer(TAB_LAYER)
        self.overlay_shapes['Cartesian'].hide()

    def set_sharing(self, shared):
        self._sharing = shared

    def sharing(self):
        return self._sharing

    def is_project_empty(self):
        ''' Check to see if project has any blocks in use '''
        return len(self.just_blocks()) == 1

    def recalculate_constants(self):
        CONSTANTS['titlex'] = int(-(self.width * TITLEXY[0]
                                    ) / (self.coord_scale * 2))
        CONSTANTS['leftx'] = int(-(self.width * TITLEXY[0]
                                   ) / (self.coord_scale * 2))
        CONSTANTS['rightx'] = 0
        CONSTANTS['titley'] = int(
            (self.height * TITLEXY[1]) / (self.coord_scale * 2))
        CONSTANTS['topy'] = int(
            (self.height * (TITLEXY[1] - 0.125)) / (self.coord_scale * 2))
        CONSTANTS['bottomy'] = 0
        CONSTANTS['leftpos'] = int(-self.width / (self.coord_scale * 2))
        CONSTANTS['toppos'] = int(self.height / (self.coord_scale * 2))
        CONSTANTS['rightpos'] = int(self.width / (self.coord_scale * 2))
        CONSTANTS['bottompos'] = int(-self.height / (self.coord_scale * 2))
        CONSTANTS['width'] = int(self.width / self.coord_scale)
        CONSTANTS['height'] = int(self.height / self.coord_scale)

        # If there are any constant blocks on the canvas, relabel them
        for blk in self.just_blocks():
            if blk.name in ['leftpos', 'toppos', 'rightpos', 'bottompos',
                            'width', 'height']:
                blk.spr.set_label('%s = %d' % (block_names[blk.name][0],
                                               CONSTANTS[blk.name]))
                blk.resize()

    def _configure_cb(self, event):
        ''' Screen size has changed '''
        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height()
        self.recalculate_constants()

        if event is None:
            return

        if self.running_sugar:
            self.activity.check_buttons_for_fit()

    def _draw_cb(self, win, context):
        ''' Repaint '''
        self.do_draw(context)
        return True

    def do_draw(self, cr):
        ''' Handle the expose-event by drawing '''

        # TODO: set global scale
        # find_sprite needs rescaled coordinates
        # sw needs new bounds set
        # cr.scale(self.activity.global_x_scale, self.activity.global_y_scale)

        cr.rectangle(self.rect.x, self.rect.y,
                     self.rect.width, self.rect.height)

        if self.turtle_canvas is not None:
            cr.set_source_surface(self.turtle_canvas)
            cr.paint()

        # Refresh sprite list
        self.sprite_list.redraw_sprites(cr=cr)

    def eraser_button(self):
        ''' Eraser_button (hide status block when clearing the screen.) '''
        if self.status_spr is not None:
            self.status_spr.hide()
        self._autohide_shape = True
        self.lc.find_value_blocks()  # Are there blocks to update?
        self.lc.prim_clear()
        self.display_coordinates()

    def run_button(self, time, running_from_button_push=False):
        ''' Run turtle! '''
        if self.running_sugar:
            self.activity.recenter()
        elif self.interactive_mode:  # autosave in GNOME
            self.activity.autosave()

        # Look for a 'start' block
        for blk in self.just_blocks():
            if find_start_stack(blk):
                self.step_time = time
                if self.running_sugar:
                    debug_output('running stack starting from %s' % (blk.name),
                                 self.running_sugar)

                if running_from_button_push:
                    self.selected_blk = None
                else:
                    self.selected_blk = blk

                # Warn user if running an empty start stack
                grp = find_group(blk)
                if len(grp) == 1:
                    # FIX ME: use graphic
                    self.showlabel('emptystart')
                else:
                    self._run_stack(blk)
                return

        # If there is no 'start' block, run stacks that aren't 'def action'
        for blk in self.just_blocks():
            if find_block_to_run(blk):
                self.step_time = time
                if self.running_sugar:
                    debug_output('running stack starting from %s' % (blk.name),
                                 self.running_sugar)
                if running_from_button_push:
                    self.selected_blk = None
                else:
                    self.selected_blk = blk
                self._run_stack(blk)
        return

    def stop_button(self):
        ''' Stop button '''
        self.lc.stop_logo()

    def set_userdefined(self, blk=None):
        ''' Change icon for user-defined blocks after loading Python code. '''
        if blk is not None:
            if blk.name in PYTHON_SKIN:
                x, y = self.calc_image_offset('pythonon', blk.spr)
                blk.set_image(self.media_shapes['pythonon'], x, y)
                self._resize_skin(blk)

    def set_fullscreen(self):
        ''' Enter fullscreen mode '''
        if self.running_sugar:
            self.activity.fullscreen()
            self.activity.recenter()
            self.activity.vbox.set_size_request(Gdk.Screen.width(),
                                                Gdk.Screen.height())

    def set_cartesian(self, flag):
        ''' Turn on/off Cartesian coordinates '''
        if self.coord_scale == 1:
            self.draw_overlay('Cartesian_labeled')
        else:
            self.draw_overlay('Cartesian')
        return

    def get_coord_scale(self):
        return self.coord_scale

    def set_polar(self, flag):
        ''' Turn on/off polar coordinates '''
        self.draw_overlay('polar')
        return

    def set_metric(self, flag):
        ''' Turn on/off metric coordinates '''
        self.draw_overlay('metric')
        return

    def draw_overlay(self, overlay):
        ''' Draw a coordinate grid onto the canvas. '''
        width = self.overlay_shapes[overlay].rect.width
        height = self.overlay_shapes[overlay].rect.height
        if self.running_sugar:
            y_offset = 0
        else:
            y_offset = 0
            # y_offset = ICON_SIZE
        self.canvas.draw_surface(
            self.overlay_shapes[overlay].cached_surfaces[0],
            (self.canvas.width - width) / 2.0,
            (self.canvas.height - height + y_offset) / 2.0,
            width,
            height)

    def update_overlay_position(self, widget=None, event=None):
        ''' Reposition the overlays when window size changes '''
        # self.width = event.width
        # self.height = event.height
        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height()

        for name in OVERLAY_SHAPES:
            if name not in self.overlay_shapes:
                continue
            shape = self.overlay_shapes[name]
            showing = False
            if shape in shape._sprites.list:
                shape.hide()
                showing = True
            self.overlay_shapes[name].move((int(self.width / 2 - 600),
                                            int(self.height / 2 - 450)))
            '''
            self.overlay_shapes[name] = Sprite(
                self.sprite_list,
                int(self.width / 2 - 600),
                int(self.height / 2 - 450),
                svg_str_to_pixbuf(
                    svg_from_file('%s/%s.svg' % (self.images_path, name))))
            '''
            if showing:
                self.overlay_shapes[name].set_layer(OVERLAY_LAYER)
            else:
                self.overlay_shapes[name].hide()
            '''
            self.overlay_shapes[name].type = 'overlay'
            '''

        self.cartesian = False
        self.polar = False
        self.metric = False
        self.canvas.width = self.width
        self.canvas.height = self.height
        self.turtles.get_active_turtle().move_turtle()

    def hideshow_button(self):
        ''' Hide/show button '''
        if not self.hide:
            for blk in self.just_blocks():
                blk.spr.hide()
            self.hide_palette()
            self.hide = True
        else:
            for blk in self.just_blocks():
                if blk.status != 'collapsed':
                    blk.spr.set_layer(BLOCK_LAYER)
            self.show_palette()
            self.hide = False
            if self.running_sugar:
                self.activity.recenter()
        self.inval_all()

    def inval_all(self):
        ''' Force a refresh '''
        if self.interactive_mode:
            self.window.queue_draw_area(0, 0, self.width, self.height)

    def hideshow_palette(self, state):
        ''' Hide or show palette  '''
        if not state:
            self.palette = False
            if self.running_sugar:
                self.activity.do_hidepalette()
            self.hide_palette()
        else:
            self.palette = True
            if self.running_sugar:
                self.activity.do_showpalette()
                self.activity.recenter()
            self.show_palette()

    def show_palette(self, n=None):
        ''' Show palette. '''
        if n is None:
            if self.selected_palette is None:
                n = 0
            else:
                n = self.selected_palette
        self.show_toolbar_palette(n)
        self.palette_button[self.orientation].set_layer(TAB_LAYER)
        self.palette_button[2].set_layer(TAB_LAYER)
        self.palette_views[n].display_palette_shift_buttons()
        if not self.running_sugar:
            self.toolbar_spr.set_layer(CATEGORY_LAYER)
        self.palette = True
        self._set_coordinates_label(palette_names[n])

    def hide_palette(self):
        ''' Hide the palette. '''
        self._hide_toolbar_palette()
        for button in self.palette_button:
            button.hide()
        if not self.running_sugar:
            self.toolbar_spr.hide()
        self.palette = False

    def move_palettes(self, x, y):
        ''' Move the palettes. '''
        for palette in self.palette_views:
            palette.move(x, y)

        self.status_spr.move((x + self.status_spr.save_xy[0],
                              y + self.status_spr.save_xy[1]))

    def hideblocks(self):
        ''' Callback from 'hide blocks' block '''
        if not self.interactive_mode:
            return
        self.hide = False
        self.hideshow_button()
        if self.running_sugar:
            self.activity.do_hide_blocks()

    def showblocks(self):
        ''' Callback from 'show blocks' block '''
        if not self.interactive_mode:
            return
        self.hide = True
        self.hideshow_button()
        if self.running_sugar:
            self.activity.do_show_blocks()

    def resize_blocks(self, blocks=None):
        ''' Resize blocks or if blocks is None, all of the blocks '''
        if blocks is None:
            blocks = self.just_blocks()

        # Do the resizing.
        for blk in blocks:
            blk.rescale(self.block_scale)
        for blk in blocks:
            self._adjust_dock_positions(blk)

        # Resize the skins on some blocks: media content and Python
        for blk in blocks:
            if blk.name in BLOCKS_WITH_SKIN:
                self._resize_skin(blk)

        # Resize text_entry widget
        if hasattr(self, '_text_entry') and len(blocks) > 0:
            font_desc = Pango.FontDescription('Sans')
            font_desc.set_size(
                int(blocks[0].font_size[0] * Pango.SCALE * self.entry_scale))
            self._text_entry.modify_font(font_desc)

    def _has_selectors(self):
        return not self.running_sugar

    def show_toolbar_palette(self, n, init_only=False, regenerate=False,
                             show=True):
        ''' Show the toolbar palettes, creating them on init_only '''
        # If we are running the 0.86+ toolbar, the selectors are already
        # created, as toolbar buttons. Otherwise, we need to create them.
        if (not self.running_sugar) and self.selectors == []:
            # First, create the selector buttons
            self._create_the_selectors()

        # Create the empty palettes that we'll then populate with prototypes.
        if self.palette_views == []:
            self._create_the_empty_palettes()

        # At initialization of the program, we don't populate the palettes.
        if init_only:
            return

        if show:
            # Hide the previously displayed palette
            self._hide_previous_palette()
        else:
            save_selected = self.selected_palette
            save_previous = self.previous_palette

        self.selected_palette = n
        self.previous_palette = self.selected_palette

        # Make sure all of the selectors are visible.
        if show and self._has_selectors():
            self.selected_selector = n
            self.selectors[n].set_shape(1)
            for i in range(len(palette_blocks)):
                self.selectors[i].set_layer()

            # Show the palette with the current orientation.
            if self.palette_views[n].backgrounds[self.orientation] is not None:
                self.palette_views[n].backgrounds[self.orientation].set_layer(
                    CATEGORY_LAYER)
                self.palette_views[n].display_palette_shift_buttons()

        self.palette_views[n].create(regenerate=regenerate, show=show)

        if not show:
            if not save_selected == n:
                self._hide_previous_palette(palette=n)
            self.selected_palette = save_selected
            self.previous_palette = save_previous

    def regenerate_palette(self, n):
        ''' Regenerate palette (used by some plugins) '''
        if self._has_selectors() and self.selectors == []:
            return
        if self.palette_views == []:
            return

        save_selected = self.selected_palette
        save_previous = self.previous_palette
        self.selected_palette = n
        self.previous_palette = self.selected_palette

        self.palette_views[n].layout(regenerate=True,
                                     show=(save_selected == n))

        if not save_selected == n:
            self._hide_previous_palette(palette=n)
        self.selected_palette = save_selected
        self.previous_palette = save_previous

    def _create_the_selectors(self):
        ''' Create the palette selector buttons: only when running
        old-style Sugar toolbars or from GNOME '''
        for i in range(len(palette_names)):
            self.selectors.append(Selector(self, i))

        # Create the toolbar background for the selectors
        self.toolbar_offset = ICON_SIZE
        self.toolbar_spr = create_toolbar_background(self.sprite_list,
                                                     self.width)

    def _create_the_empty_palettes(self):
        ''' Create the empty palettes to be populated by prototype blocks. '''
        for i in range(len(palette_names)):
            self.palette_views.append(PaletteView(self, i))

        # Create the palette orientation button
        self.palette_button.append(
            Sprite(
                self.sprite_list,
                0,
                self.toolbar_offset,
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettehorizontal.svg' % (self.images_path)))))
        self.palette_button.append(
            Sprite(
                self.sprite_list,
                0,
                self.toolbar_offset,
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettevertical.svg' % (self.images_path)))))
        self.palette_button[0].name = _('orientation')
        self.palette_button[1].name = _('orientation')
        self.palette_button[0].type = 'palette'
        self.palette_button[1].type = 'palette'
        self.palette_button[self.orientation].set_layer(TAB_LAYER)
        self.palette_button[1 - self.orientation].hide()

        # Create the palette next button
        self.palette_button.append(
            Sprite(
                self.sprite_list, 16,
                self.toolbar_offset,
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettenext.svg' % (self.images_path)))))
        self.palette_button[2].name = _('next')
        self.palette_button[2].type = 'palette'
        self.palette_button[2].set_layer(TAB_LAYER)

        # Create the palette shift buttons
        dims = self.palette_button[0].get_dimensions()
        self.palette_button.append(
            Sprite(
                self.sprite_list,
                0,
                self.toolbar_offset + dims[1],
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettehshift.svg' % (self.images_path)))))
        self.palette_button.append(
            Sprite(
                self.sprite_list,
                dims[0],
                self.toolbar_offset,
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettevshift.svg' % (self.images_path)))))
        self.palette_button.append(
            Sprite(
                self.sprite_list,
                0,
                self.toolbar_offset + dims[1],
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettehshift2.svg' % (self.images_path)))))
        self.palette_button.append(
            Sprite(
                self.sprite_list,
                dims[0],
                self.toolbar_offset,
                svg_str_to_pixbuf(
                    svg_from_file(
                        '%s/palettevshift2.svg' % (self.images_path)))))
        for i in range(4):
            self.palette_button[3 + i].name = _('shift')
            self.palette_button[3 + i].type = 'palette'
            self.palette_button[3 + i].hide()

    def _hide_toolbar_palette(self):
        ''' Hide the toolbar palettes '''
        self._hide_previous_palette()
        if not self.running_sugar:
            # Hide the selectors
            for i in range(len(palette_blocks)):
                self.selectors[i].hide()

    def _hide_previous_palette(self, palette=None):
        ''' Hide just the previously viewed toolbar palette '''
        if palette is None:
            palette = self.previous_palette
        # Hide previously selected palette
        if palette is not None:
            self.palette_views[palette].hide()
            if self._has_selectors():
                self.selectors[palette].set_shape(0)

    def _buttonpress_cb(self, win, event):
        ''' Button press '''
        self.window.grab_focus()
        x, y = xy(event)
        self.mouse_flag = 1
        self.mouse_x = x
        self.mouse_y = y
        self.button_press(
            event.get_state() & Gdk.ModifierType.CONTROL_MASK, x, y)
        return True

    def get_mouse_flag(self):
        return self.mouse_flag

    def get_mouse_button(self):
        return self.mouse_flag == 1

    def get_mouse_x(self):
        return int((self.mouse_x - (self.canvas.width / 2)) / self.coord_scale)

    def get_mouse_y(self):
        return int(
            ((self.canvas.height / 2) - self.mouse_y) / self.coord_scale)

    def button_press(self, mask, x, y):
        if self.running_turtleart:
            if self.running_sugar:
                self._show_unfullscreen_button()

            if self.interactive_mode:
                self.activity.hide_store()

        # Find out what was clicked
        spr = self.sprite_list.find_sprite((x, y))

        if self.running_blocks:
            if spr is not None:
                blk = self.block_list.spr_to_block(spr)
                if blk is not None:
                    # Make sure stop button is visible
                    if self.running_sugar and self.running_turtleart:
                        self.activity.stop_turtle_button.set_icon_name(
                            "stopiton")
                        self.activity.stop_turtle_button.set_tooltip(
                            _('Stop turtle'))
                    elif self.interactive_mode:
                        self.toolbar_shapes['stopiton'].set_layer(TAB_LAYER)
                    self.showlabel('status',
                                   label=_('Please hit the Stop Button '
                                           'before making changes to your '
                                           'program'))
                    self._autohide_shape = True
                    return True

        self.block_operation = 'click'

        self._unselect_all_blocks()
        self._hide_status_layer(spr)

        self.dx = 0
        self.dy = 0
        self.dragging_canvas[1] = x
        self.dragging_canvas[2] = y
        if spr is None:
            if not self.running_blocks and self.hw not in [XO1]:
                self.dragging_canvas[0] = True
                self.dragging_counter = 0
                self.dragging_dx = 0
                self.dragging_dy = 0
            return True
        self.dragging_canvas[0] = False
        self.selected_spr = spr

        if self._look_for_a_blk(spr, x, y):
            return True
        elif self._look_for_a_turtle(spr, x, y):
            return True
        elif self._check_for_anything_else(spr, x, y):
            return True

    def _unselect_all_blocks(self):
        # Unselect things that may have been selected earlier
        if self.selected_blk is not None:
            if len(self.selected_blk.spr.labels) > 0:
                label_with_no_returns = \
                    self.selected_blk.spr.labels[0].replace(RETURN, ' ')
            else:
                label_with_no_returns = None
            if self._action_name(self.selected_blk, hat=True):
                self.selected_blk.values[0] = label_with_no_returns
                self.selected_blk.spr.labels[0] = label_with_no_returns
                if self.selected_blk.values[0] == _('action'):
                    self._new_stack_block(label_with_no_returns)
                self._update_action_names(label_with_no_returns)
            elif self._box_name(self.selected_blk, storein=True):
                self.selected_blk.values[0] = label_with_no_returns
                self.selected_blk.spr.labels[0] = label_with_no_returns
                if self.selected_blk.values[0] == _('my box'):
                    self._new_storein_block(label_with_no_returns)
                    self._new_box_block(label_with_no_returns)
                self._update_storein_names(label_with_no_returns)
                self._update_box_names(label_with_no_returns)

            # Un-highlight any blocks in the stack
            grp = find_group(self.selected_blk)
            for blk in grp:
                if hasattr(blk, 'status') and blk.status != 'collapsed':
                    blk.unhighlight()
            self._unselect_block()
            if self.running_sugar and self._sharing and \
               hasattr(self.activity, 'share_button'):
                self.activity.share_button.set_tooltip(
                    _('Select blocks to share'))
        self.selected_turtle = None

    def _hide_status_layer(self, spr):
        # Almost always hide the status layer on a click
        if self._autohide_shape and self.status_spr is not None:
            self.status_spr.hide()
        elif spr == self.status_spr:
            self.status_spr.hide()
            self._autohide_shape = True

    def _look_for_a_blk(self, spr, x, y, blk=None):
        # From the sprite at x, y, look for a corresponding block
        if blk is None:
            blk = self.block_list.spr_to_block(spr)
        ''' If we were copying and didn't click on a block... '''
        if self.copying_blocks or self.sharing_blocks or self.saving_blocks:
            if blk is None or blk.type != 'block':
                self.parent.get_window().set_cursor(
                    Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
                self.copying_blocks = False
                self.sharing_blocks = False
                self.saving_blocks = False
        elif self.deleting_blocks:
            if blk is None or blk.type != 'proto':
                self.parent.get_window().set_cursor(
                    Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
                self.deleting_blocks = False
        if blk is not None:
            if blk.type == 'block':
                self.selected_blk = blk
                self._block_pressed(x, y, blk)
            elif blk.type == 'trash':
                self._restore_from_trash(find_top_block(blk))
            elif blk.type == 'proto':
                if self.deleting_blocks:
                    if 'myblocks' in palette_names and \
                            self.selected_palette == \
                            palette_names.index('myblocks'):
                        self._delete_stack_alert(blk)
                    self.parent.get_window().set_cursor(
                        Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
                    self.deleting_blocks = False
                elif blk.name == 'restoreall':
                    self._restore_all_from_trash()
                elif blk.name == 'restore':
                    self.restore_latest_from_trash()
                elif blk.name == 'empty':
                    self.empty_trash()
                elif blk.name == 'trashall':
                    for b in self.just_blocks():
                        if b.type != 'trash':
                            if b.name == 'start':  # Don't trash start block
                                b1 = b.connections[-1]
                                if b1 is not None:
                                    b.connections[-1] = None
                                    b1.connections[0] = None
                                    self._put_in_trash(b1)
                            else:
                                self._put_in_trash(find_top_block(b))
                    if 'trash' in palette_names:
                        self.show_toolbar_palette(
                            palette_names.index('trash'), regenerate=True)
                elif blk.name in MACROS:
                    self.new_macro(blk.name, x + 20, y + 20)
                else:
                    defaults = None
                    name = blk.name
                    # You can only have one instance of some blocks
                    if blk.name in ['start', 'hat1', 'hat2']:
                        blk_list = self.block_list.get_similar_blocks(
                            'block', blk.name)
                        if len(blk_list) > 0:
                            self.showlabel('dupstack')
                            if blk.name == 'start':
                                # Recenter the screen and move the start
                                # stack to the center of the screen
                                if self.running_sugar:
                                    self.activity.recenter()
                                dx = 200 - blk_list[0].spr.get_xy()[0]
                                dy = 200 - blk_list[0].spr.get_xy()[1]
                                drag_group = find_group(blk_list[0])
                                for dblk in drag_group:
                                    dblk.spr.move_relative((dx, dy))
                            return True
                    # We need to check to see if there is already a
                    # similarly default named stack
                    elif blk.name == 'hat':
                        similars = self.block_list.get_similar_blocks(
                            'block', blk.name)
                        # First look for a hat with _('action') as its label
                        found_the_action_block = False
                        bname = _('action')
                        for sblk in similars:
                            cblk = sblk.connections[1]
                            if cblk is not None:
                                blabel = cblk.spr.labels[0]
                                if bname == blabel:
                                    found_the_action_block = True
                        # If there is an action block in use, change the name
                        if len(similars) > 0 and found_the_action_block:
                            defaults = [_('action')]
                            if self._find_proto_name('stack', defaults[0]):
                                defaults[0] = increment_name(defaults[0])
                                while self._find_proto_name('stack_%s' %
                                                            (defaults[0]),
                                                            defaults[0]):
                                    defaults[0] = increment_name(defaults[0])
                                self._new_stack_block(defaults[0])
                    # If we autogenerated a stack prototype, we need
                    # to change its name from 'stack_foo' to 'stack'
                    elif blk.name[0:6] == 'stack_':
                        defaults = [blk.name[6:]]
                        name = 'stack'
                    # If we autogenerated a box prototype, we need
                    # to change its name from 'box_foo' to 'box'
                    elif blk.name[0:4] == 'box_':
                        defaults = [blk.name[4:]]
                        name = 'box'
                    # If we autogenerated a storein prototype, we need
                    # to change its name from 'storein_foo' to 'foo'
                    # and label[1] from foo to box
                    elif blk.name[0:8] == 'storein_':
                        defaults = [blk.name[8:], 100]
                        name = 'storein'
                    # storein my_box gets incremented
                    elif blk.name == 'storein':
                        defaults = [_('my box'), 100]
                        defaults[0] = increment_name(defaults[0])
                        while self._find_proto_name('storein_%s' %
                                                    (defaults[0]),
                                                    defaults[0]):
                            defaults[0] = increment_name(defaults[0])
                        self._new_storein_block(defaults[0])
                        self._new_box_block(defaults[0])
                        name = 'storein'
                    # You cannot mix and match sensor blocks
                    elif blk.name in ['sound', 'volume', 'pitch']:
                        if len(self.block_list.get_similar_blocks(
                                'block', ['resistance', 'voltage',
                                          'resistance2', 'voltage2'])) > 0:
                            self.showlabel('incompatible')
                            return True
                    elif blk.name in ['resistance', 'voltage',
                                      'resistance2', 'voltage2']:
                        if len(self.block_list.get_similar_blocks(
                                'block', ['sound', 'volume', 'pitch'])) > 0:
                            self.showlabel('incompatible')
                            return True
                        if blk.name in ['resistance', 'resistance2']:
                            if len(self.block_list.get_similar_blocks(
                                    'block', ['voltage', 'voltage2'])) > 0:
                                self.showlabel('incompatible')
                                return True
                        elif blk.name in ['voltage', 'voltage2']:
                            if len(self.block_list.get_similar_blocks(
                                    'block', ['resistance',
                                              'resistance2'])) > 0:
                                self.showlabel('incompatible')
                                return True
                    blk.highlight()
                    self._new_block(name, x, y, defaults=defaults)
                    blk.unhighlight()
            return True
        return False

    def _save_stack_alert(self, name, data, macro_path):
        if self.running_sugar:
            from sugar3.graphics.alert import Alert
            from sugar3.graphics.icon import Icon

            alert = Alert()
            alert.props.title = _('Save stack')
            alert.props.msg = _('Really overwrite stack?')

            cancel_icon = Icon(icon_name='dialog-cancel')
            alert.add_button(Gtk.ResponseType.CANCEL, _('Cancel'),
                             cancel_icon)
            stop_icon = Icon(icon_name='dialog-ok')
            alert.add_button(Gtk.ResponseType.OK, '%s %s' %
                             (_('Overwrite stack'), name), stop_icon)

            self.activity.add_alert(alert)
            alert.connect('response',
                          self._overwrite_stack_dialog_response_cb, data,
                          macro_path)
        else:
            msg = _('Really overwrite stack?')
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.OK_CANCEL, msg)
            dialog.set_title('%s %s' % (_('Overwrite stack'), name))
            answer = dialog.run()
            dialog.destroy()
            if answer == Gtk.ResponseType.OK:
                self._save_stack(data, macro_path)

    def _overwrite_stack_dialog_response_cb(self, alert, response_id,
                                            data, macro_path):
        self.activity.remove_alert(alert)
        if response_id == Gtk.ResponseType.OK:
            self._save_stack(data, macro_path)

    def _save_stack(self, data, macro_path):
        data_to_file(data, macro_path)

    def _delete_stack_alert(self, blk):
        if self.running_sugar:
            from sugar3.graphics.alert import Alert
            from sugar3.graphics.icon import Icon

            alert = Alert()
            alert.props.title = _('Delete stack')
            alert.props.msg = _('Really delete stack?')

            cancel_icon = Icon(icon_name='dialog-cancel')
            alert.add_button(Gtk.ResponseType.CANCEL, _('Cancel'),
                             cancel_icon)
            stop_icon = Icon(icon_name='dialog-ok')
            alert.add_button(Gtk.ResponseType.OK, '%s %s' %
                             (_('Delete stack'), blk.spr.labels[0]), stop_icon)

            self.activity.add_alert(alert)
            alert.connect('response', self._delete_stack_dialog_response_cb,
                          blk)
        else:
            msg = _('Really delete stack?')
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.OK_CANCEL, msg)
            dialog.set_title('%s %s' % (_('Delete stack'), blk.spr.labels[0]))
            answer = dialog.run()
            dialog.destroy()
            if answer == Gtk.ResponseType.OK:
                self._delete_stack(blk)

    def _delete_stack_dialog_response_cb(self, alert, response_id, blk):
        self.activity.remove_alert(alert)
        if response_id == Gtk.ResponseType.OK:
            self._delete_stack(blk)

    def _delete_stack(self, blk):
        name = blk.spr.labels[0]
        error_output('deleting proto: clicked on %s %s' % (blk.name, name),
                     self.running_sugar)
        macro_path = os.path.join(self.macros_path, '%s.tb' % (name))
        if os.path.exists(macro_path):
            try:
                os.remove(macro_path)
            except Exception as e:
                error_output('Could not remove macro %s: %s' %
                             (macro_path, e))
                return
            i = palette_names.index('myblocks')
            palette_blocks[i].remove(blk.name)
            for pblk in self.palette_views[i].blocks:
                if pblk.name == blk.name:
                    pblk.spr.hide()
                    self.palette_views[i].blocks.remove(pblk)
                    break
            self.show_toolbar_palette(i, regenerate=True)

    def _look_for_a_turtle(self, spr, x, y):
        # Next, look for a turtle
        turtle = self.turtles.spr_to_turtle(spr)
        if turtle is not None:
            # If turtle is shared, ignore click
            if self.remote_turtle(turtle.get_name()):
                return True
            self.selected_turtle = turtle
            self.turtles.set_turtle(self.turtles.get_turtle_key(turtle))
            self._turtle_pressed(x, y)
            self.update_counter = 0
            return True
        return False

    def _check_for_anything_else(self, spr, x, y):
        # Finally, check for anything else
        if hasattr(spr, 'type'):
            if spr.type == 'selector':
                self._select_category(spr)
            elif spr.type in ['category', 'category-shift-horizontal',
                              'category-shift-vertical']:
                if hide_button_hit(spr, x, y):
                    self.hideshow_palette(False)
            elif spr.type == 'palette':
                if spr.name == _('next'):
                    i = self.selected_palette + 1
                    if i == len(palette_names):
                        i = 0
                    if not self.running_sugar:
                        self._select_category(self.selectors[i].spr)
                    else:
                        self.activity.palette_buttons[i].set_active(True)
                        self.show_palette(i)
                elif spr.name == _('shift'):
                    self.palette_views[self.selected_palette].shift()
                else:
                    self.set_orientation(1 - self.orientation)
            elif spr.type == 'toolbar':
                self._select_toolbar_button(spr)
        return False

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.palette_button[self.orientation].set_layer(TAB_LAYER)
        self.palette_button[1 - self.orientation].hide()
        o = 1 - self.orientation
        spr = self.palette_views[self.selected_palette].backgrounds[o]
        if spr is not None:
            spr.hide()
        self.palette_views[self.selected_palette].layout()
        self.show_palette(self.selected_palette)

    def _update_action_names(self, name):
        ''' change the label on action blocks of the same name '''
        if isinstance(name, (float, int)):
            return
        for blk in self.just_blocks():
            if self._action_name(blk, hat=False):
                if blk.spr.labels[0] == self._saved_action_name:
                    blk.spr.labels[0] = name
                    blk.values[0] = name
                if blk.status == 'collapsed':
                    blk.spr.hide()
                else:
                    blk.spr.set_layer(BLOCK_LAYER)
        self._update_proto_name(name, 'stack_%s' % (self._saved_action_name),
                                'stack_%s' % (name), 'basic-style-1arg')

    def _update_box_names(self, name):
        ''' change the label on box blocks of the same name '''
        if isinstance(name, (float, int)):
            return
        for blk in self.just_blocks():
            if self._box_name(blk, storein=False):
                if blk.spr.labels[0] == self._saved_box_name:
                    blk.spr.labels[0] = name
                    blk.values[0] = name
                if blk.status == 'collapsed':
                    blk.spr.hide()
                else:
                    blk.spr.set_layer(BLOCK_LAYER)
        self._update_proto_name(name, 'box_%s' % (self._saved_box_name),
                                'box_%s' % (name), 'number-style-1strarg')

    def _update_storein_names(self, name):
        ''' change the label on storin blocks of the same name '''
        if isinstance(name, (float, int)):
            return
        for blk in self.just_blocks():
            if self._box_name(blk, storein=True):
                if blk.spr.labels[0] == self._saved_box_name:
                    blk.spr.labels[0] = name
                    blk.values[0] = name
                if blk.status == 'collapsed':
                    blk.spr.hide()
                else:
                    blk.spr.set_layer(BLOCK_LAYER)
        self._update_proto_name(name, 'storein_%s' % (self._saved_box_name),
                                'storein_%s' % (name), 'basic-style-2arg',
                                label=1)

    def _update_proto_name(self, name, old, new, style, palette='blocks',
                           label=0):
        ''' Change the name of a proto block '''
        # The name change has to happen in multiple places:
        # (1) The proto block itself
        # (2) The list of block styles
        # (3) The list of proto blocks on the palette
        # (4) The list of block names

        if old == new:
            '''
            debug_output('update_proto_name: %s == %s' % (old, new),
                         self.running_sugar)
            '''
            return

        if old in block_styles[style]:
            block_styles[style].remove(old)
        if new not in block_styles[style]:
            block_styles[style].append(new)

        if old in block_names:
            del block_names[old]
        if new not in block_names:
            block_names[new] = name

        i = palette_name_to_index(palette)
        for blk in self.palette_views[i].blocks:
            if blk.name == old:
                blk.name = new
                blk.spr.labels[label] = name
                blk.spr.set_layer(PROTO_LAYER)
                blk.resize()
                break  # Should only be one proto block by this name

        if old in palette_blocks[i]:
            palette_blocks[i].remove(old)
        if new not in palette_blocks[i]:
            palette_blocks[i].append(new)

        self.show_toolbar_palette(i, regenerate=True)

    def _action_name(self, blk, hat=False):
        ''' is this a label for an action block? '''
        if blk is None:
            return False
        if blk.name != 'string':  # Ignoring int/float names
            return False
        if blk.connections is None:
            return False
        if blk.connections[0] is None:
            return False
        if hat and blk.connections[0].name == 'hat':
            return True
        if not hat and blk.connections[0].name == 'stack':
            return True
        return False

    def _box_name(self, blk, storein=False):
        ''' is this a label for a storein block? '''
        if blk is None:
            return False
        if blk.name != 'string':  # Ignoring int names
            return False
        if blk.connections is None:
            return False
        if blk.connections[0] is None:
            return False
        if storein and blk.connections[0].name == 'storein':
            if blk.connections[0].connections[1] == blk:
                return True
            else:
                return False
        if not storein and blk.connections[0].name == 'box':
            return True
        return False

    def _select_category(self, spr):
        ''' Select a category from the toolbar '''
        for i, selector in enumerate(self.selectors):
            if selector.spr == spr:
                break
        self.selectors[i].set_shape(1)

        if i != self.selected_selector:
            self.selectors[self.selected_selector].set_shape(0)
            self.selected_selector = i
            self.show_palette(i)

    def _select_toolbar_button(self, spr):
        ''' Select a toolbar button (Used when not running Sugar). '''
        if not hasattr(spr, 'name'):
            return
        if spr.name == 'run-fastoff':
            self.lc.trace = 0
            self.hideblocks()
            self.display_coordinates(clear=True)
            self.run_button(0)
        elif spr.name == 'run-slowoff':
            self.lc.trace = 1
            self.showblocks()
            self.run_button(3)
        elif spr.name == 'stopiton':
            self.stop_button()
            self.display_coordinates()
            self.showblocks()
            self.toolbar_shapes['stopiton'].hide()
        elif spr.name == 'eraseron':
            self.eraser_button()
        elif spr.name == 'hideshowoff':
            self.hideshow_button()

    def _put_in_trash(self, blk, x=0, y=0):
        ''' Put a group of blocks into the trash. '''
        self.trash_stack.append(blk)
        group = find_group(blk)
        for gblk in group:
            gblk.type = 'trash'
            gblk.rescale(self.trash_scale)
        blk.spr.move((x, y))
        for gblk in group:
            self._adjust_dock_positions(gblk)

        # And resize any skins.
        for gblk in group:
            if gblk.name in BLOCKS_WITH_SKIN:
                self._resize_skin(gblk)

        if 'trash' not in palette_names or \
                self.selected_palette != palette_names.index('trash'):
            for gblk in group:
                gblk.spr.hide()

        # If there was a named hat or storein, remove it from the
        # proto palette, the palette name list, the block name list,
        # and the style list
        for gblk in group:
            if (gblk.name == 'hat' or gblk.name == 'storein') and \
               gblk.connections is not None and \
               gblk.connections[1] is not None and \
               gblk.connections[1].name == 'string':
                if gblk.name == 'hat':
                    self._remove_palette_blocks(
                        'stack_%s' % (gblk.connections[1].values[0]),
                        'basic-style-1arg')
                else:  # Only if it was the only one
                    remove = True
                    similars = self.block_list.get_similar_blocks(
                        'block', 'storein')
                    for blk in similars:
                        if blk.connections is not None and \
                           blk.connections[1] is not None and \
                           blk.connections[1].name == 'string':
                            if blk.connections[1].values[0] == \
                               gblk.connections[1].values[0]:
                                remove = False
                    similars = self.block_list.get_similar_blocks(
                        'block', 'box')
                    for blk in similars:
                        if blk.connections is not None and \
                           blk.connections[1] is not None and \
                           blk.connections[1].name == 'string':
                            if blk.connections[1].values[0] == \
                               gblk.connections[1].values[0]:
                                remove = False
                    if remove:
                        self._remove_palette_blocks(
                            'box_%s' % gblk.connections[1].values[0],
                            'number-style-1strarg')
                        self._remove_palette_blocks(
                            'storein_%s' % gblk.connections[1].values[0],
                            'basic-style-2arg')

    def _remove_palette_blocks(self, name, style, palette='blocks'):
        ''' Remove blocks from palette and block, style lists '''
        i = palette_name_to_index('blocks')
        if name in palette_blocks[i]:
            palette_blocks[i].remove(name)
            for blk in self.palette_views[i].blocks:
                if blk.name == name:
                    blk.spr.hide()
                    self.palette_views[i].blocks.remove(blk)
            self.show_toolbar_palette(i, regenerate=True)
        if name in block_styles[style]:
            block_styles[style].remove(name)
        if name in block_names:
            del block_names[name]

    def _restore_all_from_trash(self):
        ''' Restore all the blocks in the trash can. '''
        for blk in self.block_list.list:
            if blk.type == 'trash':
                top = find_top_block(blk)
                if top.type == 'trash':
                    self._restore_from_trash(blk)

    def restore_latest_from_trash(self):
        ''' Restore most recent blocks from the trash can. '''
        if len(self.trash_stack) == 0:
            return
        self._restore_from_trash(self.trash_stack[len(self.trash_stack) - 1])

    def _restore_from_trash(self, blk):
        blk.type = None
        group = find_group(blk)
        debug_output(group, True)

        # We serialize the data and use the "paste" mechanism to
        # restore blocks. This lets us take advantage of the duplicate
        # block checking mechanism.
        selected_blk = self.selected_blk
        self.selected_blk = blk
        data = self.assemble_data_to_save(False, False)
        self.process_data(data)

        remove_list = []
        for gblk in group:
            gblk.spr.hide()
            remove_list.append(gblk)

        for gblk in remove_list:
            if gblk in self.trash_stack:
                self.trash_stack.remove(gblk)

        if 'trash' in palette_names:
            self.show_toolbar_palette(palette_names.index('trash'),
                                      regenerate=True)

        self.selected_blk = selected_blk

    def empty_trash(self):
        ''' Permanently remove all blocks presently in the trash can. '''
        title = _('empty trash')
        msg = _('Do you really want to empty the trash?')
        if self.running_sugar:
            self.activity.empty_trash_alert(title, msg)
        else:
            dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.OK_CANCEL, msg)
            dialog.set_title(title)
            res = dialog.run()
            dialog.destroy()
            if res == Gtk.ResponseType.OK:
                self._empty_trash()

    def _empty_trash(self):
        remove_list = []
        for blk in self.block_list.list:
            if blk.type == 'trash':
                blk.spr.hide()
                remove_list.append(blk)
        for blk in remove_list:
            if blk in self.block_list.list:
                self.block_list.list.remove(blk)
        self.trash_stack = []
        if 'trash' in palette_names:
            self.show_toolbar_palette(palette_names.index('trash'),
                                      regenerate=True)

    def _in_the_trash(self, x, y):
        ''' Is x, y over a palette? '''
        n = self.selected_palette
        if n is not None:
            spr = self.palette_views[n].backgrounds[self.orientation]
            if spr.hit((x, y)):
                return True
        return False

    def _block_pressed(self, x, y, blk):
        ''' Block pressed '''
        if blk is not None:
            blk.highlight()
            self._disconnect(blk)
            self.drag_group = find_group(blk)
            (sx, sy) = blk.spr.get_xy()
            self.drag_pos = x - sx, y - sy
            for blk in self.drag_group:
                if blk.status != 'collapsed':
                    blk.spr.set_layer(TOP_LAYER)
            if self.copying_blocks or self.sharing_blocks or \
               self.saving_blocks:
                for blk in self.drag_group:
                    if blk.status != 'collapsed':
                        blk.highlight()
                self.block_operation = 'copying'
                data = self.assemble_data_to_save(False, False)

                if data is not []:
                    if self.saving_blocks:
                        i = find_hat(data)
                        if i is not None:
                            name = ''
                            try:
                                name = str(data[data[i][4][1]][1][1])
                            except BaseException:
                                pass
                            if name == '':
                                name = 'stack_%d' % (int(uniform(0, 10000)))
                            debug_output('saving macro %s' % (name),
                                         self.running_sugar)
                            if not os.path.exists(self.macros_path):
                                try:
                                    os.makedirs(self.macros_path)
                                except OSError as exc:
                                    if exc.errno == errno.EEXIST:
                                        pass
                                    else:
                                        raise
                            macro_path = os.path.join(
                                self.macros_path, '%s.tb' % (name))
                            # Make sure name is unique
                            if os.path.exists(macro_path):
                                self._save_stack_alert(name, data, macro_path)
                            else:
                                self._save_stack(data, macro_path)
                            self.drag_group = None
                    elif self.copying_blocks:
                        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
                        text = data_to_string(data)
                        if text is not None:
                            clipboard.set_text(text, -1)
                    elif self.sharing():
                        text = data_to_string(data)
                        self.send_event('B', data_to_string([self.nick, text]))
            self.paste_offset = 20

            self.parent.get_window().set_cursor(
                Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
            self.saving_blocks = False

            if self.running_sugar and self._sharing and \
               hasattr(self.activity, 'share_button'):
                self.activity.share_button.set_tooltip(
                    _('Share selected blocks'))

            if len(blk.spr.labels) > 0:
                self._saved_string = blk.spr.labels[0]
                self._saved_action_name = self._saved_string
                self._saved_box_name = self._saved_string
            else:
                self._saved_string = ''

    def _unselect_block(self):
        ''' Unselect block '''
        # After unselecting a 'number' block, we need to check its value
        if self.selected_blk is None:
            return
        if self.selected_blk.name == 'number':
            if self._text_to_check:
                self._test_number()
        elif self.selected_blk.name == 'string':
            if self._text_to_check:
                self._test_string()
        self._text_to_check = False

        if len(self.selected_blk.spr.labels) > 0:
            label_with_no_returns = \
                self.selected_blk.spr.labels[0].replace(RETURN, ' ')
        else:
            label_with_no_returns = None
        if self._action_name(self.selected_blk, hat=True):
            self.selected_blk.spr.labels[0] = label_with_no_returns
            self.selected_blk.values[0] = label_with_no_returns
            if self._saved_action_name == _('action'):
                self._new_stack_block(label_with_no_returns)
            self._update_action_names(label_with_no_returns)
        elif self._box_name(self.selected_blk, storein=True):
            self.selected_blk.spr.labels[0] = label_with_no_returns
            self.selected_blk.values[0] = label_with_no_returns
            if self._saved_box_name == _('my box'):
                self._new_storein_block(label_with_no_returns)
                self._new_box_block(label_with_no_returns)
            self._update_storein_names(label_with_no_returns)
            self._update_box_names(label_with_no_returns)

        self.selected_blk.unhighlight()
        self.selected_blk = None

    def _new_block(self, name, x, y, defaults=None):
        ''' Make a new block. '''
        x_pos = x - 20
        y_pos = y - 20
        if name in content_blocks:
            if defaults is None:
                defaults = default_values[name]
            newblk = Block(self.block_list, self.sprite_list, name, x_pos,
                           y_pos, 'block', defaults)
            if self.block_scale != BLOCK_SCALE[3]:
                newblk.rescale(self.block_scale)
        else:
            newblk = Block(self.block_list, self.sprite_list, name, x_pos,
                           y_pos, 'block', [])
            if self.block_scale != BLOCK_SCALE[3]:
                newblk.rescale(self.block_scale)

        # Add a 'skin' to some blocks
        if name in PYTHON_SKIN:
            if self.nop == 'pythonloaded':
                self._block_skin('pythonon', newblk)
            else:
                self._block_skin('pythonoff', newblk)
        elif name in block_styles['box-style-media']:
            if name in EXPAND_SKIN:
                if newblk.ex == 0:
                    newblk.expand_in_x(EXPAND_SKIN[name][0])
                if newblk.ey == 0:
                    newblk.expand_in_y(EXPAND_SKIN[name][1])
            self._block_skin(name + 'off', newblk)

        newspr = newblk.spr
        newspr.set_layer(TOP_LAYER)
        self.drag_pos = 20, 20
        newblk.connections = [None] * len(newblk.docks)
        if newblk.name in default_values:
            if defaults is None:
                defaults = default_values[newblk.name]
            for i, argvalue in enumerate(defaults):
                # skip the first dock position since it is always a connector
                dock = newblk.docks[i + 1]
                argname = dock[0]
                if argname == 'unavailable':
                    continue
                if argname == 'media':
                    argname = 'journal'
                elif argname == 'number' and \
                        isinstance(argvalue, str):
                    argname = 'string'
                elif argname == 'string' and \
                        name in block_styles['number-style-1strarg'] and \
                        isinstance(argvalue, (float, int)):
                    argname = 'number'
                elif argname == 'bool':
                    argname = argvalue
                elif argname == 'flow':
                    argname = argvalue
                (sx, sy) = newspr.get_xy()
                if argname is not None:
                    if argname in content_blocks:
                        argblk = Block(self.block_list, self.sprite_list,
                                       argname, 0, 0, 'block', [argvalue])
                        if self.block_scale != BLOCK_SCALE[3]:
                            argblk.rescale(self.block_scale)
                    else:
                        argblk = Block(self.block_list, self.sprite_list,
                                       argname, 0, 0, 'block', [])
                        if self.block_scale != BLOCK_SCALE[3]:
                            argblk.rescale(self.block_scale)
                    argdock = argblk.docks[0]
                    nx = sx + dock[2] - argdock[2]
                    ny = sy + dock[3] - argdock[3]
                    if argname == 'journal':
                        self._block_skin('journaloff', argblk)
                    argblk.spr.move((nx, ny))
                    argblk.spr.set_layer(TOP_LAYER)
                    argblk.connections = [newblk, None]
                    newblk.connections[i + 1] = argblk
        self.drag_group = find_group(newblk)
        self.block_operation = 'new'
        if len(newblk.spr.labels) > 0 and newblk.spr.labels[0] is not None \
                and newblk.name not in ['', 'number', 'string']:
            newblk.refresh()
            if len(self.used_block_list) > 0:
                self.used_block_list.append(', ')
            if newblk.name in special_names:
                self.used_block_list.append(special_names[newblk.name])
            elif newblk.spr.labels[0] not in self.used_block_list:
                self.used_block_list.append(newblk.spr.labels[0])

    def new_macro(self, name, x, y):
        ''' Create a 'macro' (predefined stack of blocks). '''
        macro = MACROS[name]
        macro[0][2] = x
        macro[0][3] = y
        top = self.process_data(macro)
        self.block_operation = 'new'
        self.drag_group = find_group(top)

    def process_data(self, block_data, offset=0):
        ''' Process block_data (from a macro, a file, or the clipboard). '''
        if self.interactive_mode:
            self.sprite_list.set_defer_draw(True)
        self._process_block_data = []
        for blk in block_data:
            if not (self._found_a_turtle(blk) or self._found_font_scale(blk)):
                if len(blk) > 5:
                    self._process_block_data.append(
                        [blk[0], blk[1], blk[2], blk[3], blk[4], blk[5]])
                elif len(blk) == 5:
                    self._process_block_data.append(
                        [blk[0], blk[1], blk[2], blk[3], blk[4]])
                else:
                    return None
        self._extra_block_data = []
        # Create the blocks (or turtle).
        blocks = []
        for i, blk in enumerate(self._process_block_data):
            if not (self._found_a_turtle(blk) or self._found_font_scale(blk)):
                newblk = self.load_block(blk, offset)
                if newblk is not None:
                    blocks.append(newblk)
                    if newblk.spr is not None:
                        newblk.spr.set_layer(TOP_LAYER)
                else:
                    blocks.append(None)
        # Some extra blocks may have been added by load_block
        for blk in self._extra_block_data:
            self._process_block_data.append(blk)
            newblk = self.load_block(blk, offset)
            if newblk is not None:
                blocks.append(newblk)
                if newblk.spr is not None:
                    newblk.spr.set_layer(TOP_LAYER)

        # Make the connections.
        for i, blk in enumerate(blocks):
            if blk is None:
                continue
            cons = []
            # Normally, it is simply a matter of copying the connections.
            if blk.connections is None:
                if self._process_block_data[i][4] is not None:
                    for c in self._process_block_data[i][4]:
                        if c is None or c > (len(blocks) - 1):
                            cons.append(None)
                        else:
                            cons.append(blocks[c])
                else:
                    debug_output('connection error %s' %
                                 (str(self._process_block_data[i])),
                                 self.running_sugar)
                    cons.append(None)
            elif blk.connections == 'check':
                # Convert old-style boolean and arithmetic blocks
                cons.append(None)  # Add an extra connection.
                for c in self._process_block_data[i][4]:
                    if c is None:
                        cons.append(None)
                    else:
                        cons.append(blocks[c])
                # If the boolean op was connected, readjust the plumbing.
                if blk.name in block_styles['boolean-style']:
                    if self._process_block_data[i][4][0] is not None:
                        c = self._process_block_data[i][4][0]
                        cons[0] = blocks[self._process_block_data[c][4][0]]
                        c0 = self._process_block_data[c][4][0]
                        for j, cj \
                                in enumerate(self._process_block_data[c0][4]):
                            if cj == c:
                                blocks[c0].connections[j] = blk
                        if c < i:
                            blocks[c].connections[0] = blk
                            blocks[c].connections[3] = None
                        else:
                            # Connection was to a block we haven't seen yet.
                            debug_output('Warning: dock to the future',
                                         self.running_sugar)
                else:
                    if self._process_block_data[i][4][0] is not None:
                        c = self._process_block_data[i][4][0]
                        cons[0] = blocks[self._process_block_data[c][4][0]]
                        c0 = self._process_block_data[c][4][0]
                        for j, cj \
                                in enumerate(self._process_block_data[c0][4]):
                            if cj == c:
                                blocks[c0].connections[j] = blk
                        if c < i:
                            blocks[c].connections[0] = blk
                            blocks[c].connections[1] = None
                        else:
                            # Connection was to a block we haven't seen yet.
                            debug_output('Warning: dock to the future',
                                         self.running_sugar)
            else:
                debug_output('Warning: unknown connection state %s' %
                             (str(blk.connections)), self.running_sugar)
            blk.connections = cons[:]

        # Block sizes and shapes may have changed.
        for blk in blocks:
            if blk is None:
                continue
            self._adjust_dock_positions(blk)

        # Look for any stacks that need to be collapsed
        for blk in blocks:
            if blk is None:
                continue
            if blk.name == 'sandwichclampcollapsed':
                collapse_clamp(blk, False)

        # process in reverse order
        for i in range(len(blocks)):
            blk = blocks[-i - 1]
            if blk is None:
                continue
            if blk.name in EXPANDABLE_FLOW:
                if blk.name in block_styles['clamp-style-1arg'] or \
                   blk.name in block_styles['clamp-style-boolean'] or \
                   blk.name in block_styles['clamp-style-hat-1arg']:
                    if blk.connections[2] is not None:
                        self._resize_clamp(blk, blk.connections[2])
                elif blk.name in block_styles['clamp-style-until']:
                    if blk.connections[2] is not None:
                        self._resize_clamp(blk, blk.connections[2])
                    if blk.connections[1] is not None:
                        self._resize_clamp(blk, blk.connections[1], dockn=1)
                elif blk.name in block_styles['clamp-style'] or \
                        blk.name in \
                        block_styles['clamp-style-collapsible'] or \
                        blk.name in block_styles['clamp-style-hat']:
                    if blk.connections[1] is not None:
                        self._resize_clamp(blk, blk.connections[1])
                elif blk.name in block_styles['clamp-style-else']:
                    if blk.connections[2] is not None:
                        self._resize_clamp(blk, blk.connections[2], dockn=2)
                    if blk.connections[3] is not None:
                        self._resize_clamp(blk, blk.connections[3], dockn=3)
            elif blk.name in block_styles['basic-style-3arg']:
                if blk.connections[2] is not None:
                    dy = 0
                    drag_group = find_group(blk.connections[2])
                    gblk = drag_group[0]
                    d = int(
                        (gblk.docks[-1][3] - gblk.docks[0][3]) / gblk.scale)
                    if d == 0:
                        dy += 21  # Fixme: don't hardcode size of slot
                    else:
                        dy += d
                    blk.expand_in_y2(dy)
                    if dy > 0:
                        for gblk in drag_group:
                            gblk.spr.move_relative((0, -dy * gblk.scale))

        # Eliminate None blocks from the block list
        blocks_copy = []
        for blk in blocks:
            if blk is not None:
                blocks_copy.append(blk)
        blocks = blocks_copy[:]

        # Resize blocks to current scale and draw
        if self.interactive_mode:
            self.resize_blocks(blocks)

        if self.interactive_mode:
            self.sprite_list.set_defer_draw(False)

        if len(blocks) > 0:
            return blocks[0]
        else:
            return None

    def _adjust_dock_positions(self, blk):
        ''' Adjust the dock x, y positions '''
        if not self.interactive_mode:
            return
        (sx, sy) = blk.spr.get_xy()
        for i, c in enumerate(blk.connections):
            if i > 0 and c is not None and i < len(blk.docks):
                bdock = blk.docks[i]
                for j in range(len(c.docks)):
                    if j < len(c.connections) and c.connections[j] == blk:
                        cdock = c.docks[j]
                        nx = sx + bdock[2] - cdock[2]
                        ny = sy + bdock[3] - cdock[3]
                        c.spr.move((nx, ny))
                self._adjust_dock_positions(c)

    def _turtle_pressed(self, x, y):
        pos = self.selected_turtle.get_xy()
        tpos = self.turtles.turtle_to_screen_coordinates(pos)
        dx = x - tpos[0]
        dy = y - tpos[1]
        if not hasattr(self.lc, 'value_blocks'):
            self.lc.find_value_blocks()
        self.lc.update_values = True
        # Compare distance squared of drag position to sprite radius.
        # If x, y is near the edge, rotate.
        if (dx * dx) + (dy * dy) > self.selected_turtle.get_drag_radius():
            self.drag_turtle = (
                'turn',
                self.selected_turtle.get_heading() - atan2(dy, dx) / DEGTOR,
                0)
        else:
            self.drag_turtle = ('move', x - tpos[0], y - tpos[1])

    def _move_cb(self, win, event):
        x, y = xy(event)
        self.mouse_x = x
        self.mouse_y = y
        self._mouse_move(x, y)
        return True

    def _share_mouse_move(self):
        ''' Share turtle movement and rotation after button up '''
        if self.sharing():
            nick = self.turtle_movement_to_share.get_name()
            event = data_to_string(
                [nick,
                 round_int(self.turtles.get_active_turtle().get_heading())])
            self.send_event('r', event)
            if self.turtles.get_active_turtle().get_pen_state():
                self.send_event('p', data_to_string([nick, False]))
                put_pen_back_down = True
            else:
                put_pen_back_down = False
            event = data_to_string(
                [nick,
                 [round_int(self.turtles.get_active_turtle().get_xy()[0]),
                  round_int(self.turtles.get_active_turtle().get_xy()[1])]])
            self.send_event('x', event)
            if put_pen_back_down:
                self.send_event('p', data_to_string([nick, True]))
        self.turtle_movement_to_share = None

    def _mouse_move(self, x, y):
        ''' Process mouse movements '''

        if self.running_sugar and self.dragging_canvas[0]:
            # Don't adjust with each mouse move or GTK cannot keep pace.
            if self.dragging_counter < 10:
                self.dragging_dx += self.dragging_canvas[1] - x
                self.dragging_dy += self.dragging_canvas[2] - y
                self.dragging_canvas[1] = x
                self.dragging_canvas[2] = y
                self.dragging_counter += 1
            else:
                self.activity.adjust_sw(self.dragging_dx, self.dragging_dy)
                self.dragging_counter = 0
                self.dragging_dx = 0
                self.dragging_dy = 0
            return True

        self.block_operation = 'move'

        # First, check to see if we are dragging or rotating a turtle.
        if self.selected_turtle is not None:
            drag_type, dragx, dragy = self.drag_turtle
            self.update_counter += 1
            if drag_type == 'move':
                dx = x - dragx
                dy = y - dragy
                self.selected_turtle.spr.set_layer(TOP_LAYER)
                pos = self.turtles.screen_to_turtle_coordinates((dx, dy))
                if self.selected_turtle.get_pen_state():
                    self.selected_turtle.set_pen_state(False)
                    self.selected_turtle.set_xy(*pos, share=False,
                                                dragging=True)
                    self.selected_turtle.set_pen_state(True)
                else:
                    self.selected_turtle.set_xy(*pos, share=False,
                                                dragging=True)
                if self.update_counter % 5:
                    self.lc.update_label_value(
                        'xcor', self.selected_turtle.get_xy(
                        )[0] / self.coord_scale)
                    self.lc.update_label_value(
                        'ycor', self.selected_turtle.get_xy(
                        )[1] / self.coord_scale)
            else:
                spos = self.turtles.turtle_to_screen_coordinates(
                    self.selected_turtle.get_xy())
                dx = x - spos[0]
                dy = y - spos[1]
                self.turtles.get_active_turtle().set_heading(
                    int(dragx + atan2(dy, dx) / DEGTOR + 5) / 10 * 10,
                    share=False)
                if self.update_counter % 5:
                    self.lc.update_label_value(
                        'heading', self.selected_turtle.get_heading())
            if self.update_counter % 20:
                self.display_coordinates()
            self.turtle_movement_to_share = self.selected_turtle

        # If we are hoving, show popup help.
        elif self.drag_group is None:
            self._show_popup(x, y)
            return

        # If we have a stack of blocks selected, move them.
        elif self.drag_group[0] is not None:
            blk = self.drag_group[0]

            self.selected_spr = blk.spr
            dragx, dragy = self.drag_pos
            (sx, sy) = blk.spr.get_xy()
            dx = x - dragx - sx
            dy = y - dragy - sy

            # Take no action if there was a move of 0, 0.
            if dx == 0 and dy == 0:
                return

            self.drag_group = find_group(blk)

            # Prevent blocks from ending up with a negative x or y
            for blk in self.drag_group:
                (bx, by) = blk.spr.get_xy()
                if bx + dx < 0:
                    dx = -bx
                if by + dy < 0:
                    dy = -by

            # Calculate a bounding box and only invalidate once.
            minx = blk.spr.rect.x
            miny = blk.spr.rect.y
            maxx = blk.spr.rect.x + blk.spr.rect.width
            maxy = blk.spr.rect.y + blk.spr.rect.height

            for blk in self.drag_group:
                if blk.spr.rect.x < minx:
                    minx = blk.spr.rect.x
                if blk.spr.rect.x + blk.spr.rect.width > maxx:
                    maxx = blk.spr.rect.x + blk.spr.rect.width
                if blk.spr.rect.y < miny:
                    miny = blk.spr.rect.y
                if blk.spr.rect.y + blk.spr.rect.height > maxy:
                    maxy = blk.spr.rect.y + blk.spr.rect.height
                blk.spr.rect.x += dx
                blk.spr.rect.y += dy

            if dx < 0:
                minx += dx
            else:
                maxx += dx
            if dy < 0:
                miny += dy
            else:
                maxy += dy

            self.rect.x = minx
            self.rect.y = miny
            self.rect.width = maxx - minx
            self.rect.height = maxy - miny
            self.window.queue_draw_area(self.rect.x,
                                        self.rect.y,
                                        self.rect.width,
                                        self.rect.height)
        self.dx += dx
        self.dy += dy

    def _show_popup(self, x, y):
        ''' Let's help our users by displaying a little help. '''
        if self.no_help:
            return
        spr = self.sprite_list.find_sprite((x, y))
        blk = self.block_list.spr_to_block(spr)
        if spr and blk is not None:
            if self._timeout_tag[0] == 0:
                self._timeout_tag[0] = self._do_show_popup(blk.name)
                self.selected_spr = spr
            else:
                if self._timeout_tag[0] > 0:
                    try:
                        GLib.source_remove(self._timeout_tag[0])
                        self._timeout_tag[0] = 0
                    except BaseException:
                        self._timeout_tag[0] = 0
        elif spr and hasattr(spr, 'type') and \
                (spr.type == 'selector' or spr.type == 'palette' or spr.type == 'toolbar'):
            if self._timeout_tag[0] == 0 and hasattr(spr, 'name'):
                self._timeout_tag[0] = self._do_show_popup(spr.name)
                self.selected_spr = spr
            else:
                if self._timeout_tag[0] > 0:
                    try:
                        GLib.source_remove(self._timeout_tag[0])
                        self._timeout_tag[0] = 0
                    except BaseException:
                        self._timeout_tag[0] = 0
        else:
            if self._timeout_tag[0] > 0:
                try:
                    GLib.source_remove(self._timeout_tag[0])
                    self._timeout_tag[0] = 0
                except BaseException:
                    self._timeout_tag[0] = 0

    def _do_show_popup(self, block_name):
        ''' Fetch the help text and display it.  '''
        if block_name in special_names:
            special_block_name = special_names[block_name]
        elif block_name in block_names:
            special_block_name = str(block_names[block_name][0])
        elif block_name in TOOLBAR_SHAPES:
            special_block_name = ''
        else:
            special_block_name = _(block_name)
        if block_name in help_strings:
            label = help_strings[block_name]
        else:
            label = special_block_name
        if self.last_label == label:
            return 0
        self.showlabel('help', label=label)
        self.last_label = label
        return 0

    def _buttonrelease_cb(self, win, event):
        ''' Button release '''
        x, y = xy(event)
        self.mouse_flag = 0
        self.mouse_x = x
        self.mouse_y = y
        self.button_release(x, y)
        if self.turtle_movement_to_share is not None:
            self._share_mouse_move()
        return True

    def button_release(self, x, y):
        if self.running_sugar and self.dragging_canvas[0]:
            if self.dragging_counter > 0:
                self.activity.adjust_sw(self.dragging_dx, self.dragging_dy)
            self.dragging_counter = 0
            self.dragging_dx = 0
            self.dragging_dy = 0
            self.dragging_canvas[0] = False
            self.dragging_canvas[1] = x
            self.dragging_canvas[2] = y
            self.activity.adjust_palette()
            return True

        # We may have been moving the turtle
        if self.selected_turtle is not None:
            pos = self.selected_turtle.get_xy()
            spos = self.turtles.turtle_to_screen_coordinates(pos)
            turtle_name = self.turtles.get_turtle_key(self.selected_turtle)
            # Remove turtles by dragging them onto the trash palette.
            if self._in_the_trash(spos[0], spos[1]):
                # If it is the default turtle, just recenter it.
                if turtle_name == self.turtles.get_default_turtle_name():
                    self._move_turtle(0, 0)
                    self.selected_turtle.set_heading(0)
                    self.lc.update_label_value('heading', 0)
                else:
                    self.selected_turtle.hide()
                    self.turtles.remove_from_dict(turtle_name)
                    self.turtles.set_active_turtle(None)
            else:
                self._move_turtle(pos[0], pos[1])

            self.selected_turtle = None
            if self.turtles.get_active_turtle() is None:
                self.turtles.set_turtle(self.turtles.get_default_turtle_name())
            self.display_coordinates()
            return

        # If we don't have a group of blocks, then there is nothing to do.
        if self.drag_group is None:
            return

        blk = self.drag_group[0]
        # Remove blocks by dragging them onto any palette.
        if self.block_operation == 'move' and self._in_the_trash(x, y):
            self._put_in_trash(blk, x, y)
            self.drag_group = None
            return

        # Pull a stack of new blocks off of the category palette.
        if self.block_operation == 'new':
            for gblk in self.drag_group:
                (bx, by) = gblk.spr.get_xy()
                if self.orientation == 0:
                    gblk.spr.move((bx + 20,
                                   by + PALETTE_HEIGHT + self.toolbar_offset))
                else:
                    gblk.spr.move((bx + PALETTE_WIDTH, by + 20))

        # Look to see if we can dock the current stack.
        self._snap_to_dock()
        for gblk in self.drag_group:
            if gblk.status != 'collapsed':
                gblk.spr.set_layer(BLOCK_LAYER)
        self.drag_group = None

        # Find the block we clicked on and process it.
        # Consider a very small move a click (for touch interfaces)
        if self.block_operation == 'click' or (
            self.hw in [
                XO175, XO30, XO4] and self.block_operation == 'move' and (
                abs(
                self.dx) < _MOTION_THRESHOLD and abs(
                    self.dy < _MOTION_THRESHOLD))):
            self._click_block(x, y)
        elif self.block_operation == 'copying':
            GLib.timeout_add(500, self._unhighlight_drag_group, blk)

    def _unhighlight_drag_group(self, blk):
        self.drag_group = find_group(blk)
        for gblk in self.drag_group:
            gblk.unhighlight()
        self.drag_group = None

    def remote_turtle(self, name):
        ''' Is this a remote turtle? '''
        if name == self.nick:
            return False
        if hasattr(self, 'remote_turtle_dictionary') and \
                name in self.remote_turtle_dictionary:
            return True
        return False

    def label_remote_turtle(self, name, colors=['#A0A0A0', '#C0C0C0']):
        ''' Add a label to remote turtles '''
        turtle = self.turtles.get_turtle(name)
        if turtle is not None:
            turtle.label_block = Block(self.block_list,
                                       self.sprite_list,
                                       'turtle-label',
                                       0,
                                       0,
                                       'label',
                                       [],
                                       1.5 / self.scale,
                                       colors)
            turtle.label_block.spr.set_label_attributes(10.0 / self.scale)
            turtle.label_block.spr.set_label(name)
            turtle.set_remote()
            turtle.show()

    def _move_turtle(self, x, y):
        ''' Move the selected turtle to (x, y). '''
        if self.drag_turtle[0] == 'move':
            self.turtles.get_active_turtle().move_turtle((x, y))
        if self.interactive_mode:
            self.display_coordinates()
        if self.running_sugar:
            self.selected_turtle.spr.set_layer(TURTLE_LAYER)
            self.lc.update_label_value(
                'xcor',
                self.turtles.get_active_turtle().get_xy(
                )[0] / self.coord_scale)
            self.lc.update_label_value(
                'ycor',
                self.turtles.get_active_turtle().get_xy(
                )[1] / self.coord_scale)

    def _click_block(self, x, y):
        ''' Click block: lots of special cases to handle... '''
        blk = self.block_list.spr_to_block(self.selected_spr)
        if blk is None:
            return
        self.selected_blk = blk

        if blk.name in ['string', 'number']:
            self._saved_string = blk.spr.labels[0]
            if not hasattr(self, '_text_entry'):
                self._text_entry = Gtk.TextView()
                self._text_entry.set_justification(Gtk.Justification.CENTER)
                self._text_buffer = self._text_entry.get_buffer()
                font_desc = Pango.FontDescription('Sans')
                font_desc.set_size(
                    int(blk.font_size[0] * Pango.SCALE * self.entry_scale))
                self._text_entry.modify_font(font_desc)
                self.activity.fixed.put(self._text_entry, 0, 0)
            self._text_entry.show()
            w = blk.spr.label_safe_width()
            if blk.name == 'string':
                count = self._saved_string.count(RETURN)
                self._text_buffer.set_text(
                    self._saved_string.replace(RETURN, '\n'))
                h = blk.spr.label_safe_height() * (count + 1)
            else:
                self._text_buffer.set_text(self._saved_string)
                h = blk.spr.label_safe_height()
            self._text_entry.set_size_request(w, h)
            bx, by = blk.spr.get_xy()
            if not self.running_sugar:
                by += self.activity.menu_height
            mx, my = blk.spr.label_left_top()
            self._text_entry.set_pixels_above_lines(my)
            bx -= int(self.activity.sw.get_hadjustment().get_value())
            by -= int(self.activity.sw.get_vadjustment().get_value())
            self.activity.fixed.move(self._text_entry, bx + mx, by + my * 2)
            self.activity.fixed.show()
            if blk.name == 'number':
                self._insert_text_id = self._text_buffer.connect(
                    'insert-text', self._insert_text_cb)
            self._focus_out_id = self._text_entry.connect(
                'focus-out-event', self._text_focus_out_cb)
            self._text_entry.grab_focus()

        elif blk.name in block_styles['box-style-media'] and \
                blk.name not in NO_IMPORT:
            self._import_from_journal(self.selected_blk)
            if blk.name == 'journal' and self.running_sugar:
                self._load_description_block(blk)

        elif blk.name == 'identity2' or blk.name == 'hspace':
            group = find_group(blk)
            if hide_button_hit(blk.spr, x, y):
                dx = -20
                blk.contract_in_x(-dx)
                # dx = blk.reset_x()
            elif show_button_hit(blk.spr, x, y):
                dx = 20
                blk.expand_in_x(dx)
            else:
                self._run_stack(blk)
                return
            for gblk in group:
                if gblk != blk:
                    gblk.spr.move_relative((dx * blk.scale, 0))

        elif blk.name == 'vspace':
            group = find_group(blk)
            if hide_button_hit(blk.spr, x, y):
                dy = -20
                blk.contract_in_y(-dy)
                # dy = blk.reset_y()
            elif show_button_hit(blk.spr, x, y):
                dy = 20
                blk.expand_in_y(dy)
            else:
                self._run_stack(blk)
                return
            for gblk in group:
                if gblk != blk:
                    gblk.spr.move_relative((0, dy * blk.scale))
            self._resize_parent_clamps(blk)

        elif blk.name in expandable_blocks:
            # Connection may be lost during expansion, so store it...
            blk0 = blk.connections[0]
            if blk0 is not None:
                dock0 = blk0.connections.index(blk)

            if hide_button_hit(blk.spr, x, y):
                dy = -20
                blk.contract_in_y(-dy)
                # dy = blk.reset_y()
            elif show_button_hit(blk.spr, x, y):
                dy = 20
                blk.expand_in_y(dy)
            else:
                self._run_stack(blk)
                return

            if blk.name in block_styles['boolean-style']:
                self._expand_boolean(blk, blk.connections[2], dy)
            else:
                self._expand_expandable(blk, blk.connections[1], dy)

            # and restore it...
            if blk0 is not None:
                blk.connections[0] = blk0
                blk0.connections[dock0] = blk
                self._cascade_expandable(blk)

            self._resize_parent_clamps(blk)

        elif blk.name in EXPANDABLE_ARGS or blk.name == 'nop':
            if show_button_hit(blk.spr, x, y):
                n = len(blk.connections)
                group = find_group(blk.connections[n - 1])
                if blk.name == 'myfunc1arg':
                    blk.spr.labels[1] = 'f(x, y)'
                    blk.spr.labels[2] = ' '
                    dy = blk.add_arg()
                    blk.primitive = 'myfunction2'
                    blk.name = 'myfunc2arg'
                elif blk.name == 'myfunc2arg':
                    blk.spr.labels[1] = 'f(x, y, z)'
                    dy = blk.add_arg(False)
                    blk.primitive = 'myfunction3'
                    blk.name = 'myfunc3arg'
                elif blk.name == 'userdefined':
                    dy = blk.add_arg()
                    blk.primitive = 'userdefined2'
                    blk.name = 'userdefined2args'
                    self._resize_skin(blk)
                elif blk.name == 'userdefined2args':
                    dy = blk.add_arg(False)
                    blk.primitive = 'userdefined3'
                    blk.name = 'userdefined3args'
                    self._resize_skin(blk)
                elif blk.name == 'loadblock':
                    dy = blk.add_arg()
                    blk.primitive = 'loadblock2'
                    blk.name = 'loadblock2arg'
                    self._resize_skin(blk)
                elif blk.name == 'loadblock2arg':
                    dy = blk.add_arg(False)
                    blk.primitive = 'loadblock3'
                    blk.name = 'loadblock3arg'
                    self._resize_skin(blk)
                else:
                    dy = blk.add_arg()
                for gblk in group:
                    gblk.spr.move_relative((0, dy))
                blk.connections.append(blk.connections[n - 1])
                argname = blk.docks[n - 1][0]
                argvalue = default_values[blk.name][
                    len(default_values[blk.name]) - 1]
                argblk = Block(self.block_list, self.sprite_list, argname,
                               0, 0, 'block', [argvalue])
                if self.block_scale != BLOCK_SCALE[3]:
                    argblk.rescale(self.block_scale)
                argdock = argblk.docks[0]
                (bx, by) = blk.spr.get_xy()
                nx = bx + blk.docks[n - 1][2] - argdock[2]
                ny = by + blk.docks[n - 1][3] - argdock[3]
                argblk.spr.move((nx, ny))
                argblk.spr.set_layer(TOP_LAYER)
                argblk.connections = [blk, None]
                blk.connections[n - 1] = argblk
                if blk.name in block_styles['number-style-var-arg']:
                    self._cascade_expandable(blk)
                self._resize_parent_clamps(blk)
            elif blk.name in PYTHON_SKIN:
                self._import_py()
            else:
                self._run_stack(blk)
        elif blk.name == 'sandwichclampcollapsed':
            restore_clamp(blk)
            if blk.connections[1] is not None:
                self._resize_clamp(blk, blk.connections[1], 1)
            self._resize_parent_clamps(blk)
        elif blk.name == 'sandwichclamp':
            if hide_button_hit(blk.spr, x, y):
                collapse_clamp(blk, True)
                self._resize_parent_clamps(blk)
            else:
                self._run_stack(blk)
        else:
            self._run_stack(blk)

    def _resize_parent_clamps(self, blk):
        ''' If we changed size, we need to let any parent clamps know. '''
        nblk, dockn = self._expandable_flow_above(blk)
        while nblk is not None:
            self._resize_clamp(nblk, nblk.connections[dockn], dockn=dockn)
            nblk, dockn = self._expandable_flow_above(nblk)

    def _expand_boolean(self, blk, blk2, dy):
        ''' Expand a boolean blk if blk2 is too big to fit. '''
        group = find_group(blk2)
        for gblk in find_group(blk):
            if gblk not in group:
                gblk.spr.move_relative((0, -dy * blk.scale))

    def _expand_expandable(self, blk, blk2, dy):
        ''' Expand an expandable blk if blk2 is too big to fit. '''
        if blk2 is None:
            group = [blk]
        else:
            group = find_group(blk2)
            group.append(blk)
        for gblk in find_group(blk):
            if gblk not in group:
                gblk.spr.move_relative((0, dy * blk.scale))
        if blk.name in block_styles['compare-style'] or \
           blk.name in block_styles['compare-porch-style']:
            for gblk in find_group(blk):
                gblk.spr.move_relative((0, -dy * blk.scale))

    def _number_style(self, name):
        if name in block_styles['number-style']:
            return True
        if name in block_styles['number-style-porch']:
            return True
        if name in block_styles['number-style-block']:
            return True
        if name in block_styles['number-style-var-arg']:
            return True
        return False

    def _cascade_expandable(self, blk):
        ''' If expanding/shrinking a block, cascade. '''
        while self._number_style(blk.name):
            if blk.connections[0] is None:
                break
            if blk.connections[0].name in expandable_blocks:
                if blk.connections[0].connections.index(blk) != 1:
                    break
                blk = blk.connections[0]
                if blk.connections[1].name == 'myfunc2arg':
                    dy = 40 + blk.connections[1].ey - blk.ey
                elif blk.connections[1].name == 'myfunc3arg':
                    dy = 60 + blk.connections[1].ey - blk.ey
                else:
                    dy = 20 + blk.connections[1].ey - blk.ey
                blk.expand_in_y(dy)
                if dy != 0:
                    group = find_group(blk.connections[1])
                    group.append(blk)
                    for gblk in find_group(blk):
                        if gblk not in group:
                            gblk.spr.move_relative((0, dy * blk.scale))
                    if blk.name in block_styles['compare-style'] or \
                            blk.name in block_styles['compare-porch-style']:
                        for gblk in find_group(blk):
                            gblk.spr.move_relative((0, -dy * blk.scale))
            else:
                break

    def _run_stack(self, blk):
        ''' Run a stack of blocks. '''
        if not self.interactive_mode:
            # Test for forever block
            if len(self.block_list.get_similar_blocks('block', 'forever')) > 0:
                debug_output('WARNING: Projects with forever blocks \
 may not terminate.', False)
            self.__run_stack(blk)
        else:
            self._hide_text_entry()
            self.parent.get_window().set_cursor(
                Gdk.Cursor.new(Gdk.CursorType.WATCH))
            GLib.idle_add(self.__run_stack, blk)

    def __run_stack(self, blk):
        if self.status_spr is not None:
            self.status_spr.hide()
        self._autohide_shape = True
        if blk is None:
            return
        if not self.interactive_mode:
            self.lc.find_value_blocks()  # Are there blocks to update?
        if self.canvas.cr_svg is None:
            self.canvas.setup_svg_surface()
        self.running_blocks = True
        self.start_plugins()  # Let the plugins know we are running.
        top = find_top_block(blk)
        code = self.lc.generate_code(top, self.just_blocks())
        if self.interactive_mode:
            self.parent.get_window().set_cursor(
                Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
        self.lc.run_blocks(code)
        if self.interactive_mode:
            GLib.idle_add(self.lc.doevalstep)
        else:
            while self.lc.doevalstep():
                pass
        # self.running_blocks = False  # Should be handled in talogo.py

    def _snap_to_dock(self):
        ''' Snap a block (selected_block) to the dock of another block
        (destination_block). '''
        selected_block = self.drag_group[0]
        best_destination = None
        d = _SNAP_THRESHOLD
        self.inserting_block_mid_stack = False
        for selected_block_dockn in range(len(selected_block.docks)):
            for destination_block in self.just_blocks():
                # Don't link to a block that is hidden
                if destination_block.status == 'collapsed':
                    continue
                # Don't link to a block to which you're already connected
                if destination_block in self.drag_group:
                    continue
                # Check each dock of destination for a possible connection
                for destination_dockn in range(len(destination_block.docks)):
                    this_xy = self.dock_dx_dy(
                        destination_block, destination_dockn,
                        selected_block, selected_block_dockn)
                    if magnitude(this_xy) > d:
                        continue
                    d = magnitude(this_xy)
                    best_xy = this_xy
                    best_destination = destination_block
                    best_destination_dockn = destination_dockn
                    best_selected_block_dockn = selected_block_dockn
        if d < _SNAP_THRESHOLD:
            # Some combinations of blocks are not valid
            if not arithmetic_check(selected_block, best_destination,
                                    best_selected_block_dockn,
                                    best_destination_dockn):
                return
            if not journal_check(selected_block, best_destination,
                                 best_selected_block_dockn,
                                 best_destination_dockn):
                return

            # Move the selected blocks into the docked position
            for blk in self.drag_group:
                (sx, sy) = blk.spr.get_xy()
                blk.spr.move((sx + best_xy[0], sy + best_xy[1]))

            blk_in_dock = best_destination.connections[best_destination_dockn]
            if self.inserting_block_mid_stack:
                # If there was already a block docked there, move it
                # to the bottom of the drag group.
                if blk_in_dock is not None and blk_in_dock != selected_block:
                    bot = find_bot_block(self.drag_group[0])
                    if bot is not None:
                        blk_in_dock.connections[0] = None
                        drag_group = find_group(blk_in_dock)
                        blk_in_dock.connections[0] = bot
                        bot.connections[-1] = blk_in_dock
                        dx = bot.spr.get_xy()[0] - \
                            self.drag_group[0].spr.get_xy()[0] + \
                            bot.docks[-1][2] - blk_in_dock.docks[0][2]
                        dy = bot.spr.get_xy()[1] - \
                            self.drag_group[0].spr.get_xy()[1] + \
                            bot.docks[-1][3] - blk_in_dock.docks[0][3]
                        # Move each sprite in the group associated
                        # with the block we are moving.
                        for gblk in drag_group:
                            gblk.spr.move_relative((dx, dy))
            else:
                # If there was already a block docked there, move it
                # to the trash.
                if blk_in_dock is not None and blk_in_dock != selected_block:
                    blk_in_dock.connections[0] = None
                    self._put_in_trash(blk_in_dock)

            # Note the connection in destination dock
            best_destination.connections[best_destination_dockn] = \
                selected_block

            # And in the selected block dock
            if selected_block.connections is not None:
                if best_selected_block_dockn < len(selected_block.connections):
                    selected_block.connections[best_selected_block_dockn] = \
                        best_destination

            # Are we renaming an action or variable?
            if best_destination.name in ['hat', 'storein'] and \
                    selected_block.name == 'string' and \
                    best_destination_dockn == 1:
                name = selected_block.values[0]
                if best_destination.name == 'storein':
                    if not self._find_proto_name('storein_%s' % (name), name):
                        self._new_storein_block(name)
                    if not self._find_proto_name('box_%s' % (name), name):
                        self._new_box_block(name)
                else:  # 'hat'
                    # Check to see if it is unique...
                    unique = True
                    similars = self.block_list.get_similar_blocks(
                        'block', 'hat')
                    for blk in similars:
                        if blk == best_destination:
                            continue
                        if blk.connections is not None and \
                                blk.connections[1] is not None and \
                                blk.connections[1].name == 'string':
                            if blk.connections[1].values[0] == name:
                                unique = False
                    if not unique:
                        while self._find_proto_name('stack_%s' % (name), name):
                            name = increment_name(name)
                        blk.connections[1].values[0] = name
                        blk.connections[1].spr.labels[0] = name
                        blk.resize()
                    self._new_stack_block(name)

            # Some destination blocks expand to accomodate large blocks
            if best_destination.name in block_styles['boolean-style']:
                if best_destination_dockn == 2 and \
                        (selected_block.name in
                         block_styles['boolean-style'] or selected_block.name
                         in block_styles['compare-style'] or selected_block.name
                         in block_styles['compare-porch-style']
                         ):
                    dy = selected_block.ey - best_destination.ey
                    if selected_block.name in block_styles['boolean-style']:
                        # Even without expanding, boolean blocks are
                        # too large to fit in the lower dock position
                        dy += 45
                    best_destination.expand_in_y(dy)
                    self._expand_boolean(best_destination, selected_block, dy)
            elif best_destination.name in EXPANDABLE_FLOW:
                if best_destination.name in \
                        block_styles['clamp-style-1arg'] or \
                        best_destination.name in \
                        block_styles['clamp-style-boolean'] or \
                        best_destination.name in \
                        block_styles['clamp-style-hat-1arg']:
                    if best_destination_dockn == 2:
                        self._resize_clamp(best_destination,
                                           self.drag_group[0])
                elif best_destination.name in \
                        block_styles['clamp-style-until']:
                    if best_destination_dockn == 2:
                        self._resize_clamp(best_destination,
                                           self.drag_group[0])
                    elif best_destination_dockn == 1:
                        self._resize_clamp(best_destination,
                                           self.drag_group[0], dockn=1)
                elif best_destination.name in block_styles['clamp-style'] or \
                        best_destination.name in \
                        block_styles['clamp-style-hat'] or \
                        best_destination.name in \
                        block_styles['clamp-style-collapsible']:
                    if best_destination_dockn == 1:
                        self._resize_clamp(best_destination,
                                           self.drag_group[0])
                elif best_destination.name in block_styles['clamp-style-else']:
                    if best_destination_dockn == 2:
                        self._resize_clamp(
                            best_destination, self.drag_group[0], dockn=2)
                    elif best_destination_dockn == 3:
                        self._resize_clamp(
                            best_destination, self.drag_group[0], dockn=3)
            elif best_destination.name in expandable_blocks and \
                    best_destination_dockn == 1:
                dy = 0
                if (selected_block.name in
                        expandable_blocks or selected_block.name
                        in block_styles[
                        'number-style-var-arg']):
                    if selected_block.name == 'myfunc2arg':
                        dy = 40 + selected_block.ey - best_destination.ey
                    elif selected_block.name == 'myfunc3arg':
                        dy = 60 + selected_block.ey - best_destination.ey
                    else:
                        dy = 20 + selected_block.ey - best_destination.ey
                    best_destination.expand_in_y(dy)
                else:
                    if best_destination.ey > 0:
                        dy = best_destination.reset_y()
                if dy != 0:
                    self._expand_expandable(
                        best_destination, selected_block, dy)
                self._cascade_expandable(best_destination)
            elif best_destination.name in \
                    block_styles['basic-style-3arg'] and \
                    best_destination_dockn == 2:
                dy = 0
                if (selected_block.name in
                        expandable_blocks or selected_block.name
                        in block_styles['number-style-var-arg']):
                    if selected_block.name == 'myfunc2arg':
                        dy = 40 + selected_block.ey - best_destination.ey2
                    elif selected_block.name == 'myfunc3arg':
                        dy = 60 + selected_block.ey - best_destination.ey2
                    else:
                        dy = 20 + selected_block.ey - best_destination.ey2
                    best_destination.expand_in_y2(dy)
                else:
                    if best_destination.ey2 > 0:
                        dy = best_destination.reset_y2()
                if dy != 0:
                    # Move the dock1 contents up
                    if best_destination.connections[1] is not None:
                        drag_group = find_group(
                            best_destination.connections[1])
                        for gblk in drag_group:
                            gblk.spr.move_relative((0, -dy * gblk.scale))
                    self._expand_expandable(
                        best_destination, selected_block, dy)
                self._cascade_expandable(best_destination)

        # If we are in an expandable flow, expand it...
        if best_destination is not None:
            self._resize_parent_clamps(best_destination)
        # Check for while nesting
        if best_destination is not None:
            while_blk = self._while_in_drag_group(self.drag_group[0])
            if while_blk is not None:
                self._check_while_nesting(best_destination,
                                          self.drag_group[0], while_blk)

    def _while_in_drag_group(self, blk):
        ''' Is there a contained while or until block? '''
        if blk.name in ['while', 'until']:
            return blk
        return find_blk_below(blk, ['while', 'until'])

    def _check_while_nesting(self, blk, dock_blk, while_blk):
        ''' Is there a containing while or until block? If so, swap them '''
        if blk.name in ['while', 'until']:
            if blk.connections[2] == dock_blk:
                self._swap_while_blocks(blk, while_blk)
        while blk.connections[-1] is not None:
            blk = blk.connections[-1]
            if blk.name in ['while', 'until']:
                if blk.connections[2] == dock_blk:
                    self._swap_while_blocks(blk, while_blk)
            dock_blk = blk

    def _swap_while_blocks(self, blk1, blk2):
        ''' Swap postion in block list of nested while blocks '''
        # Check to see if blk1 comes before blk2 in the block list.
        # If so, swap them.
        i1 = self.just_blocks().index(blk1)
        i2 = self.just_blocks().index(blk2)
        if i1 < i2:
            self.block_list.swap(blk1, blk2)

    def _disconnect(self, blk):
        ''' Disconnect block from stack above it. '''
        if blk is None:
            return
        if blk.connections is None:
            return
        if blk.connections[0] is None:
            return
        c = None
        blk2 = blk.connections[0]
        if blk in blk2.connections:
            c = blk2.connections.index(blk)
            blk2.connections[c] = None
        blk3, dockn = self._expandable_flow_above(blk)

        if blk2.name in block_styles['boolean-style']:
            if c == 2 and blk2.ey > 0:
                dy = -blk2.ey
                blk2.expand_in_y(dy)
                self._expand_boolean(blk2, blk, dy)
        elif blk2.name in expandable_blocks and c == 1:
            if blk2.ey > 0:
                dy = blk2.reset_y()
                if dy != 0:
                    self._expand_expandable(blk2, blk, dy)
                self._cascade_expandable(blk2)
        elif blk2.name in expandable_blocks and c == 2:
            if blk2.ey2 > 0:
                dy = blk2.reset_y2()
                if dy != 0:
                    # Move the dock1 contents up
                    if blk2.connections[1] is not None:
                        drag_group = find_group(blk2.connections[1])
                        for gblk in drag_group:
                            gblk.spr.move_relative((0, -dy * gblk.scale))
                    self._expand_expandable(blk2, blk, dy)
                self._cascade_expandable(blk2)
        elif c is not None and blk2.name in EXPANDABLE_FLOW:
            if blk2.name in block_styles['clamp-style-1arg'] or \
                    blk2.name in block_styles['clamp-style-boolean'] or \
                    blk2.name in block_styles['clamp-style-hat-1arg']:
                if c == 2:
                    self._resize_clamp(blk2, None, dockn=c)
            elif blk2.name in block_styles['clamp-style-until']:
                if c in [1, 2]:
                    self._resize_clamp(blk2, None, dockn=c)
            elif blk2.name in block_styles['clamp-style'] or \
                    blk2.name in block_styles['clamp-style-hat'] or \
                    blk2.name in block_styles['clamp-style-collapsible']:
                if c == 1:
                    self._resize_clamp(blk2, None)
            elif blk2.name in block_styles['clamp-style-else']:
                if c in [2, 3]:
                    self._resize_clamp(blk2, None, dockn=c)
        while blk3 is not None and blk3.connections[dockn] is not None:
            self._resize_clamp(blk3, blk3.connections[dockn], dockn=dockn)
            blk3, dockn = self._expandable_flow_above(blk3)
        blk.connections[0] = None

    def _resize_clamp(self, blk, gblk, dockn=-2):
        ''' If the content of a clamp changes, resize it '''
        if not self.interactive_mode:
            return
        if dockn < 0:
            dockn = len(blk.docks) + dockn
        y1 = blk.docks[-1][3]
        if blk.name in block_styles['clamp-style-else'] and dockn == 3:
            blk.reset_y2()
        elif blk.name in block_styles['clamp-style-until'] and dockn == 1:
            blk.reset_y2()
        else:
            blk.reset_y()
        dy = 0
        # Calculate height of drag group
        if blk.name in block_styles['clamp-style-until'] and dockn == 1:
            if gblk is not None:
                dy = int(gblk.spr.rect.height / gblk.scale)
                # Room for part of one 'standard' boolean by default
                if dy > 0:
                    dy -= 25  # Fixme: don't hardcode size of slot
                if dy < 0:
                    dy = 0
        else:
            while gblk is not None:
                d = int((gblk.docks[-1][3] - gblk.docks[0][3]) / gblk.scale)
                if d == 0:
                    dy += 21  # Fixme: don't hardcode size of slot
                else:
                    dy += d
                gblk = gblk.connections[-1]
            # Clamp has room for one 'standard' block by default
            if dy > 0:
                dy -= 21  # Fixme: don't hardcode size of slot
        if blk.name in block_styles['clamp-style-else'] and dockn == 3:
            blk.expand_in_y2(dy)
        elif blk.name in block_styles['clamp-style-until'] and dockn == 1:
            blk.expand_in_y2(dy)
        else:
            blk.expand_in_y(dy)
        y2 = blk.docks[-1][3]
        gblk = blk.connections[-1]
        # Move group below clamp up or down
        if blk.connections[-1] is not None:
            drag_group = find_group(blk.connections[-1])
            for gblk in drag_group:
                gblk.spr.move_relative((0, y2 - y1))
        # We may have to move the else clamp group up or down too.
        if blk.name in block_styles['clamp-style-else'] and dockn == 2:
            if blk.connections[3] is not None:
                drag_group = find_group(blk.connections[3])
                for gblk in drag_group:
                    gblk.spr.move_relative((0, y2 - y1))
        # We may have to move the bool group up or down too.
        if blk.name in block_styles['clamp-style-until']:
            if blk.connections[1] is not None:
                drag_group = find_group(blk.connections[1])
                for gblk in drag_group:
                    gblk.spr.move_relative((0, y2 - y1))

    def _expandable_flow_above(self, blk):
        ''' Is there an expandable flow block above this one? '''
        while blk.connections[0] is not None:
            if blk.connections[0].name in EXPANDABLE_FLOW:
                if blk.connections[0].name == 'ifelse':
                    if blk.connections[0].connections[2] == blk:
                        return blk.connections[0], 2
                    elif blk.connections[0].connections[3] == blk:
                        return blk.connections[0], 3
                elif blk.connections[0].name == 'hat':
                    if blk.connections[0].connections[2] == blk:
                        return blk.connections[0], 2
                elif blk.connections[0].name == 'start':
                    if blk.connections[0].connections[1] == blk:
                        return blk.connections[0], 1
                else:
                    if blk.connections[0].connections[-2] == blk:
                        return blk.connections[0], -2
            blk = blk.connections[0]
        return None, None

    def _import_from_journal(self, blk):
        ''' Import a file from the Sugar Journal '''
        # TODO: check blk name to set filter
        if self.running_sugar:
            chooser_dialog(self.parent, '', self._update_media_blk)
        else:
            fname, self.load_save_folder = get_load_name('.*',
                                                         self.load_save_folder)
            if fname is None:
                return
            self._update_media_icon(blk, fname)

    def _load_description_block(self, blk):
        ''' Look for a corresponding description block '''
        if blk is None or blk.name != 'journal' or len(blk.values) == 0 or \
           blk.connections[0] is None:
            return
        _blk = blk.connections[0]
        dblk = find_blk_below(_blk, 'description')
        # Autoupdate the block if it is empty
        if dblk is not None and \
                (len(dblk.values) == 0 or dblk.values[0] is None):
            self._update_media_icon(dblk, None, blk.values[0])

    def _update_media_blk(self, dsobject):
        ''' Called from the chooser to load a media block '''
        if dsobject is not None:
            self._update_media_icon(self.selected_blk, dsobject,
                                    dsobject.object_id)
            dsobject.destroy()

    def _update_media_icon(self, blk, name, value=''):
        ''' Update the icon on a 'loaded' media block. '''
        if blk.name == 'journal':
            self._load_image_thumb(name, blk)
        elif blk.name == 'audio':
            self._block_skin('audioon', blk)
        elif blk.name == 'video':
            self._block_skin('videoon', blk)
        else:
            self._block_skin('descriptionon', blk)
        if value == '':
            value = name
        if len(blk.values) > 0:
            blk.values[0] = value
        else:
            blk.values.append(value)
        blk.spr.set_label(' ')

    def _load_image_thumb(self, media, blk):
        ''' Replace icon with a preview image. '''
        pixbuf = None
        media_path = media

        if self.running_sugar:
            from sugar3.datastore import datastore
            if isinstance(media, datastore.RawObject):
                media_path = media.object_id
            elif isinstance(media, datastore.DSObject):
                media_path = media.file_path

        if movie_media_type(media_path):
            self._block_skin('videoon', blk)
            blk.name = 'video'
        elif audio_media_type(media_path):
            self._block_skin('audioon', blk)
            blk.name = 'audio'
        elif image_media_type(media_path):
            if self.running_sugar:
                w, h = calc_image_size(blk.spr)
                pixbuf = get_pixbuf_from_journal(media, w, h)
            else:
                w, h = calc_image_size(blk.spr)
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    media_path, w, h)
        else:
            blk.name = 'description'
            self._block_skin('descriptionon', blk)

        if pixbuf is not None:
            x, y = self.calc_image_offset('', blk.spr)
            blk.set_image(pixbuf, x, y)
            self._resize_skin(blk)

    def _keypress_cb(self, area, event):
        ''' Keyboard '''
        keyname = Gdk.keyval_name(event.keyval)
        keyunicode = Gdk.keyval_to_unicode(event.keyval)
        if event.get_state() & Gdk.ModifierType.MOD1_MASK:
            alt_mask = True
        else:
            alt_mask = False
        self._key_press(alt_mask, keyname, keyunicode)
        return keyname

    def _key_press(self, alt_mask, keyname, keyunicode):
        if keyname is None:
            return False

        self.keypress = keyname

        if alt_mask:
            if keyname == 'p':
                self.hideshow_button()
            elif keyname == 'q':
                self.quit_plugins()
                if self.gst_available:
                    stop_media(self.lc)
                exit()
            elif keyname == 'g':
                self._align_to_grid()
            elif keyname == 's':
                self.stop_button()
                self.toolbar_shapes['stopiton'].hide()

        elif keyname == 'Tab':
            # For the first pass, just tab through palettes
            if self.selected_palette is None:
                print('selected palette is None')
                return True
            else:
                p = self.palette_views[self.selected_palette].blocks
            i = 0
            if self._highlighted_blk is not None:
                self._highlighted_blk.unhighlight()
                if self._highlighted_blk in p:
                    i = p.index(self._highlighted_blk)
                    if i == len(p) - 1:
                        i = 0
                    else:
                        i += 1
                        while not p[i].get_visibility():
                            i += 1
                            if i >= len(p) - 1:
                                i = 0
            if i < len(p):
                self._highlighted_blk = p[i]
                self._highlighted_blk.highlight()
                self.selected_blk = p[i]

        elif self.selected_blk is not None:
            if self.selected_blk.type == 'proto':
                if keyname == 'Return':
                    (x, y) = self.selected_blk.spr.get_xy()
                    if self.orientation == 0:
                        x += 20
                        y += PALETTE_HEIGHT + self.toolbar_offset
                    else:
                        x += PALETTE_WIDTH
                        y += 20
                    self._look_for_a_blk(None, x, y, blk=self.selected_blk)
                    self._unselect_all_blocks()
                    self.selected_spr = None
                    self.drag_group = None
            else:
                self._process_keyboard_commands(keyname, block_flag=True)

        elif self.turtles.spr_to_turtle(self.selected_spr) is not None:
            self._process_keyboard_commands(keyname, block_flag=False)

        return True

    def get_keyboard_input(self):
        """ Query keyboard and update cached keyboard input """
        self.window.grab_focus()
        if len(self.keypress) == 1:
            self.keyboard = ord(self.keypress[0])
        elif self.keypress in KEY_DICT:
            self.keyboard = KEY_DICT[self.keypress]
        else:
            self.keyboard = 0
        self.keypress = ''

    def get_keyboard(self):
        """ Return cached keyboard input """
        return self.keyboard

    def _process_keyboard_commands(self, keyname, block_flag=True):
        ''' Use the keyboard to move blocks and turtle '''
        mov_dict = {'KP_Up': [0, 20], 'j': [0, 20], 'Up': [0, 20],
                    'KP_Down': [0, -20], 'k': [0, -20], 'Down': [0, -20],
                    'KP_Left': [-20, 0], 'h': [-20, 0], 'Left': [-20, 0],
                    'KP_Right': [20, 0], 'l': [20, 0], 'Right': [20, 0],
                    'KP_Page_Down': [-1, -1], 'Page_Down': [-1, -1],
                    'KP_Page_Up': [-1, -1], 'Page_Up': [-1, -1],
                    'KP_End': [0, 0], 'End': [0, 0],
                    'KP_Home': [0, 0], 'Home': [0, 0], 'space': [0, 0],
                    'Return': [-1, -1], 'Esc': [-1, -1]}

        if keyname not in mov_dict:
            return True

        if keyname in ['KP_End', 'End']:
            self.run_button(self.step_time)
        elif self.selected_spr is not None:
            if not self.lc.running and block_flag:
                blk = self.block_list.spr_to_block(self.selected_spr)
                if keyname in ['Return', 'KP_Page_Up', 'Page_Up', 'Esc']:
                    (x, y) = blk.spr.get_xy()
                    self._click_block(x, y)
                elif keyname in ['KP_Page_Down', 'Page_Down']:
                    if self.drag_group is None:
                        self.drag_group = find_group(blk)
                    self._put_in_trash(blk)
                    self.drag_group = None
                elif keyname in ['KP_Home', 'Home', 'space']:
                    block = self.block_list.spr_to_block(self.selected_spr)
                    if block is None:
                        return True
                    block.unhighlight()
                    block = self.block_list.get_next_block_of_same_type(
                        block)
                    if block is not None:
                        self.selected_spr = block.spr
                        block.highlight()
                elif blk is not None:
                    self._jog_block(blk, mov_dict[keyname][0],
                                    mov_dict[keyname][1])
            elif not block_flag:
                self._jog_turtle(mov_dict[keyname][0], mov_dict[keyname][1])
            # Always exit fullscreen mode if applicable
            if self.running_sugar and self.activity.is_fullscreen:
                self.activity.unfullscreen()
                from sugar3.graphics.style import GRID_CELL_SIZE
                self.activity.vbox.set_size_request(
                    Gdk.Screen.width(),
                    Gdk.Screen.height() - 2 * GRID_CELL_SIZE)
        return True

    def _jog_turtle(self, dx, dy):
        ''' Jog turtle '''
        if dx == -1 and dy == -1:
            x = 0
            y = 0
        else:
            pos = self.turtles.get_active_turtle().get_xy()
            x = pos[0] + dx
            y = pos[1] + dy
        self.turtles.set_active_turtle(
            self.turtles.spr_to_turtle(self.selected_spr))
        self.turtles.get_active_turtle().move_turtle((x, y))
        self.display_coordinates()
        self.selected_turtle = None

    def _align_to_grid(self, grid=20):
        ''' Align blocks at the top of stacks to a grid '''
        for blk in self.block_list.list:
            if blk.type == 'block':
                top = find_top_block(blk)
                if top == blk:
                    x = top.spr.get_xy()[0]
                    y = top.spr.get_xy()[1]
                    if x < 0:
                        dx = -x % grid
                    else:
                        dx = -(x % grid)
                    if y < 0:
                        dy = -y % grid
                    else:
                        dy = -(y % grid)
                    self._jog_block(top, dx, -dy)

    def _jog_block(self, blk, dx, dy):
        ''' Jog block '''
        if blk.type == 'proto':
            return
        if dx == 0 and dy == 0:
            return
        self._disconnect(blk)
        self.drag_group = find_group(blk)

        for blk in self.drag_group:
            (sx, sy) = blk.spr.get_xy()
            if sx + dx < 0:
                dx += -(sx + dx)
            if sy + dy < 0:
                dy += -(sy + dy)

        for blk in self.drag_group:
            (sx, sy) = blk.spr.get_xy()
            blk.spr.move((sx + dx, sy - dy))

        self._snap_to_dock()
        self.drag_group = None

    def _hide_text_entry(self):
        if hasattr(self, '_text_entry'):
            if self._focus_out_id is not None:
                self._text_entry.disconnect(self._focus_out_id)
                self._focus_out_id = None
            if self._insert_text_id is not None:
                self._text_buffer.disconnect(self._insert_text_id)
                self._insert_text_id = None
            self._text_entry.hide()

    def _test_number(self):
        ''' Make sure a 'number' block contains a number. '''
        if hasattr(self, '_text_entry'):
            bounds = self._text_buffer.get_bounds()
            text = self._text_buffer.get_text(bounds[0], bounds[1], True)
            self._hide_text_entry()
        else:
            text = self.selected_blk.spr.labels[0]
        self._number_check(text)

    def _number_check(self, text):
        text = text.strip()  # Ignore any whitespace
        if text == '':
            text = '0'
        if text in ['-', '.', '-.', ',', '-,']:
            num = 0
        elif text is not None:
            try:
                num = float(text.replace(self.decimal_point, '.'))
                if num > 1000000:
                    num = 1
                    self.showlabel('#overflowerror')
                elif num < -1000000:
                    num = -1
                    self.showlabel('#overflowerror')
                if int(num) == num:
                    num = int(num)
            except ValueError:
                num = 0
                self.showlabel('#notanumber')
        else:
            num = 0
        self.selected_blk.spr.set_label(str(num))
        try:
            self.selected_blk.values[0] = \
                float(str(num).replace(self.decimal_point, '.'))
        except ValueError:
            self.selected_blk.values[0] = float(str(num))
        except IndexError:
            self.selected_blk.values[0] = float(str(num))

    def _text_focus_out_cb(self, widget=None, event=None):
        self._text_to_check = True
        self._unselect_block()

    def _insert_text_cb(self, textbuffer, textiter, text, length):
        self._text_to_check = True
        if '\n' in text:
            self._unselect_block()

    def paste_text_in_block_label(self, text):
        # If we paste plain text from the clipboard, try to insert it into
        # a block label
        if self._focus_out_id is not None:
            self._text_entry.get_buffer().insert_at_cursor(text)
        else:
            label = self.selected_blk.spr.labels[0]
            label += text
            self.selected_blk.spr.labels[0] = label

    def _test_string(self):
        if hasattr(self, '_text_entry'):
            bounds = self._text_buffer.get_bounds()
            text = self._text_buffer.get_text(bounds[0], bounds[1], True)
            self._hide_text_entry()
        else:
            text = self.selected_blk.spr.labels[0]
        self.selected_blk.spr.set_label(text.replace('\n', RETURN))
        self.selected_blk.resize()
        self.selected_blk.values[0] = text.replace(RETURN, '\n')
        self._saved_string = self.selected_blk.values[0]

    def load_python_code_from_file(self, fname=None, add_new_block=True):
        ''' Load Python code from a file '''
        id = None
        self.python_code = None
        if fname is None:
            fname, self.py_load_save_folder = get_load_name(
                '.py',
                self.py_load_save_folder)
        if fname is None:
            return id
        try:
            f = open(fname, 'r')
            self.python_code = f.read()
            f.close()
            id = fname
        except IOError:
            error_output('Unable to read Python code from %s' % (fname),
                         self.running_sugar)
            return id

        # if we are running Sugar, copy the file into the Journal
        if self.running_sugar:
            if fname in self._py_cache:
                id = self._py_cache[fname]
            else:
                from sugar3.datastore import datastore
                from sugar3 import profile

                dsobject = datastore.create()
                dsobject.metadata['title'] = os.path.basename(fname)
                dsobject.metadata['icon-color'] = \
                    profile.get_color().to_string()
                dsobject.metadata['mime_type'] = 'text/x-python'
                dsobject.metadata['activity'] = 'org.laptop.Pippy'
                dsobject.set_file_path(fname)
                try:
                    datastore.write(dsobject)
                    id = dsobject.object_id
                    debug_output('Copied %s to the datastore' % (fname),
                                 self.running_sugar)
                    # Don't copy the same file more than once
                    self._py_cache[fname] = id
                except IOError:
                    error_output('Error copying %s to the datastore' % (fname),
                                 self.running_sugar)
                    id = None
                dsobject.destroy()

            if add_new_block:
                # add a new block for this code at turtle position
                pos = self.turtles.get_active_turtle().get_xy()
                self._new_block('userdefined', pos[0], pos[1])
                self.myblock[self.block_list.list.index(self.drag_group[0])] =\
                    self.python_code
                self.set_userdefined(self.drag_group[0])
                self.drag_group[0].values.append(id)
                self.drag_group = None
            # Save object ID in block value
            if self.selected_blk is not None:
                if len(self.selected_blk.values) == 0:
                    self.selected_blk.values.append(id)
                else:
                    self.selected_blk.values[0] = id
        else:
            if len(self.selected_blk.values) == 0:
                self.selected_blk.values.append(fname)
            else:
                self.selected_blk.values[0] = fname

        return id

    def load_python_code_from_journal(self, dsobject, blk=None):
        ''' Read the Python code from the Journal object '''
        self.python_code = None
        if dsobject is None:
            return
        try:
            file_handle = open(dsobject.file_path, 'r')
            self.python_code = file_handle.read()
            file_handle.close()
        except IOError:
            debug_output('Could not open %s' % dsobject.file_path,
                         self.running_sugar)
        # Save the object id as the block value
        if blk is None:
            blk = self.selected_blk
        if blk is not None:
            if len(blk.values) == 0:
                blk.values.append(dsobject.object_id)
            else:
                blk.values[0] = dsobject.object_id

    def _import_py(self):
        ''' Import Python code into a block '''
        if self.running_sugar:
            chooser_dialog(self.parent, 'org.laptop.Pippy',
                           self.load_python_code_from_journal)
        else:
            self.load_python_code_from_file(fname=None, add_new_block=False)

        if self.selected_blk is not None:
            self.myblock[self.block_list.list.index(self.selected_blk)] = \
                self.python_code
            self.set_userdefined(self.selected_blk)

    def new_project(self):
        ''' Start a new project '''
        self.lc.stop_logo()
        self._loaded_project = ''
        # Put current project in the trash.
        while len(self.just_blocks()) > 0:
            blk = self.just_blocks()[0]
            top = find_top_block(blk)
            self._put_in_trash(top)
        self.canvas.clearscreen()
        self.save_file_name = None

    def is_new_project(self):
        ''' Is this a new project or was a old project loaded from a file? '''
        return self._loaded_project == ''

    def project_has_changed(self):
        ''' WARNING: order of JSON serialized data may have changed. '''
        try:
            f = open(self._loaded_project, 'r')
            saved_project_data = f.read()
            f.close()
        except BaseException:
            debug_output('problem loading saved project data from %s' %
                         (self._loaded_project), self.running_sugar)
            saved_project_data = ''
        current_project_data = data_to_string(self.assemble_data_to_save())
        return saved_project_data != current_project_data

    def load_files(self, ta_file, create_new_project=True):
        ''' Load a project from a file '''
        if create_new_project:
            self.new_project()
        self.process_data(data_from_file(ta_file))
        self._loaded_project = ta_file

    def load_file_from_chooser(self, create_new_project=True):
        ''' Load a project from file chooser '''
        file_name, self.load_save_folder = get_load_name(
            '.t[a-b]',
            self.load_save_folder)
        if file_name is None:
            return
        if not file_name.endswith(SUFFIX):
            file_name = file_name + SUFFIX[1]
        self.load_files(file_name, create_new_project)
        if create_new_project:
            self.save_file_name = os.path.basename(file_name)
        if self.running_sugar:
            self.activity.metadata['title'] = os.path.split(file_name)[1]

    def _found_font_scale(self, blk):
        ''' '_saved_font_scale is a reserved name '''
        # [-1, '_saved_font_scale', 2.0]
        if blk[1] == '_saved_font_scale':
            if len(blk) > 4 and isinstance(blk[4], float):
                self.block_scale = blk[4]
            return True
        return False

    def _found_a_turtle(self, blk):
        ''' Either [-1, 'turtle', ...] or [-1, ['turtle', key], ...] '''
        if blk[1] == 'turtle':
            self.load_turtle(blk)
            return True
        elif isinstance(blk[1], (list, tuple)) and blk[1][0] == 'turtle':
            if blk[1][1] == DEFAULT_TURTLE:
                if self.nick is not None and self.nick != '':
                    self.load_turtle(blk, self.nick)
            else:
                self.load_turtle(blk, blk[1][1])
            return True
        return False

    def load_turtle(self, blk, key=1):
        ''' Restore a turtle from its saved state '''
        tid, name, xcor, ycor, heading, color, shade, pensize = blk
        self.turtles.set_turtle(key)
        self.turtles.get_active_turtle().set_xy(xcor, ycor, share=True,
                                                pendown=False)
        self.turtles.get_active_turtle().set_heading(heading)
        self.turtles.get_active_turtle().set_color(color)
        self.turtles.get_active_turtle().set_shade(shade)
        self.turtles.get_active_turtle().set_gray(100)
        self.turtles.get_active_turtle().set_pen_size(pensize)

    def load_block(self, b, offset=0):
        ''' Restore individual blocks from saved state '''
        if self.running_sugar:
            from sugar3.datastore import datastore

        if b[1] == 0:
            return None
        # A block is saved as: (i, (btype, value), x, y, (c0,... cn), private)
        # The x, y position is saved/loaded for backward compatibility
        # private is an optional field
        btype, value = b[1], None
        if isinstance(btype, tuple):
            btype, value = btype
        elif isinstance(btype, list):
            btype, value = btype[0], btype[1]

        # Replace deprecated sandwich blocks
        if btype == 'sandwichtop_no_label':
            btype = 'sandwichclamp'
            docks = []
            for d in b[4]:
                docks.append(d)
            docks.append(None)
            b[4] = docks
        elif btype == 'sandwichtop_no_arm_no_label':
            btype = 'sandwichclampcollapsed'
            docks = []
            for d in b[4]:
                docks.append(d)
            docks.append(None)
            b[4] = docks
        # FIXME: blocks after sandwich bottom must be attached to
        # sandwich top dock[2], currently set to None
        elif btype in ['sandwichbottom', 'sandwichcollapsed']:
            btype = 'vspace'
        # FIXME: blocks after sandwichtop should be in a sandwich clamp
        elif btype in ['sandwichtop', 'sandwichtop_no_arm']:
            btype = 'comment'

        # Optional private data
        if len(b) > 5:
            private = b[5]
        else:
            private = None

        # Some blocks can only appear once...
        if btype in ['start', 'hat1', 'hat2']:
            if self._check_for_duplicate(btype):
                name = block_names[btype][0]
                while self._find_proto_name('stack_%s' % (name), name):
                    name = increment_name(name)
                i = len(self._process_block_data) + len(self._extra_block_data)
                self._extra_block_data.append(
                    [i, ['string', name], 0, 0, [b[0], None]])
                # To do: check for a duplicate name
                self._new_stack_block(name)
                btype = 'hat'
                self._process_block_data[b[0]] = [
                    b[0], b[1], b[2], b[3], [b[4][0], i, b[4][1]]]
        elif btype == 'hat':
            name = None
            if b[4][1] < len(self._process_block_data):
                i = b[4][1]
                if i is not None:
                    name = self._process_block_data[i][1][1]
            else:
                i = b[4][1] - len(self._process_block_data)
                name = self._extra_block_data[i][1][1]
            if name is not None:
                while self._find_proto_name('stack_%s' % (name), name):
                    name = increment_name(name)
                    if b[4][1] < len(self._process_block_data):
                        dblk = self._process_block_data[i]
                        self._process_block_data[i] = [
                            dblk[0], (dblk[1][0], name), dblk[2], dblk[3],
                            dblk[4]]
                    else:
                        dblk = self._extra_block_data[i]
                        self._extra_block_data[i] = [
                            dblk[0], (dblk[1][0], name), dblk[2], dblk[3],
                            dblk[4]]
                self._new_stack_block(name)
        elif btype == 'storein':
            name = None
            if b[4][1] < len(self._process_block_data):
                i = b[4][1]
                if i is not None:
                    name = self._process_block_data[i][1][1]
            else:
                i = b[4][1] - len(self._process_block_data)
                name = self._extra_block_data[i][1][1]
            if name is not None:
                if not self._find_proto_name('storein_%s' % (name), name):
                    self._new_storein_block(name)
                if not self._find_proto_name('box_%s' % (name), name):
                    self._new_box_block(name)

        if btype in content_blocks:
            if btype == 'number':
                try:
                    values = [round_int(value)]
                except ValueError:
                    values = [0]
            else:
                values = [value]
        else:
            values = []

        if btype in OLD_DOCK:
            check_dock = True
        else:
            check_dock = False
        if btype in OLD_NAMES:
            btype = OLD_NAMES[btype]

        blk = Block(self.block_list, self.sprite_list, btype,
                    b[2] + offset, b[3] + offset, 'block', values)

        if private is not None:
            blk.private = private

        if self.block_scale != BLOCK_SCALE[3]:
            blk.rescale(self.block_scale)

        # If it was an unknown block type, we need to match the number
        # of dock items. TODO: Try to infer the dock type from connections
        if blk.unknown and len(b[4]) > len(blk.docks):
            debug_output('%s: dock mismatch %d > %d' %
                         (btype, len(b[4]), len(blk.docks)),
                         self.running_sugar)
            for i in range(len(b[4]) - len(blk.docks)):
                blk.docks.append(['unavailable', True, 0, 0])

        # Some blocks get transformed.
        if btype in block_styles['basic-style-var-arg'] and value is not None:
            # Is there code stored in this userdefined block?
            if value > 0:  # catch deprecated format (#2501)
                self.python_code = None
                if self.running_sugar:
                    # For security reasons, only open files found in
                    # Python samples directory
                    if os.path.exists(
                            os.path.join(self.share_path, value)) and \
                            value[0:9] == 'pysamples':
                        self.selected_blk = blk
                        self.load_python_code_from_file(
                            fname=os.path.join(self.share_path, value),
                            add_new_block=False)
                        self.selected_blk = None
                    else:  # or files from the Journal
                        try:
                            dsobject = datastore.get(value)
                        except BaseException:
                            # Should be IOError, but dbus error is raised
                            dsobject = None
                            debug_output('Could not get dsobject %s' % (value),
                                         self.running_sugar)
                        if dsobject is not None:
                            self.load_python_code_from_journal(dsobject, blk)
                else:
                    self.selected_blk = blk
                    self.load_python_code_from_file(fname=value,
                                                    add_new_block=False)
                    self.selected_blk = None
                if self.python_code is not None:
                    self.myblock[self.block_list.list.index(blk)] = \
                        self.python_code
                    self.set_userdefined(blk)
        if btype == 'string' and blk.spr is not None:
            value = blk.values[0]
            blk.spr.set_label(value.replace('\n', RETURN))
        elif btype in block_styles['box-style-media'] and blk.spr is not None:
            if btype in EXPAND_SKIN:
                if blk.ex == 0:
                    blk.expand_in_x(EXPAND_SKIN[btype][0])
                if blk.ey == 0:
                    blk.expand_in_y(EXPAND_SKIN[btype][1])
            if len(blk.values) == 0 or blk.values[0] == 'None' or \
               blk.values[0] is None or btype in NO_IMPORT:
                self._block_skin(btype + 'off', blk)
            elif btype in ['video', 'audio', 'description']:
                self._block_skin(btype + 'on', blk)
            elif self.running_sugar:
                try:
                    dsobject = datastore.get(blk.values[0])
                    if not movie_media_type(dsobject.file_path[-4:]):
                        w, h, = calc_image_size(blk.spr)
                        pixbuf = get_pixbuf_from_journal(dsobject, w, h)
                        if pixbuf is not None:
                            x, y = self.calc_image_offset('', blk.spr)
                            blk.set_image(pixbuf, x, y)
                        else:
                            self._block_skin('journalon', blk)
                    dsobject.destroy()
                except BaseException:
                    try:
                        w, h, = calc_image_size(blk.spr)
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                            blk.values[0], w, h)
                        x, y = self.calc_image_offset('', blk.spr)
                        blk.set_image(pixbuf, x, y)
                    except BaseException:
                        debug_output('Could not open dsobject (%s)' %
                                     (blk.values[0]), self.running_sugar)
                        self._block_skin('journaloff', blk)
            else:
                if not movie_media_type(blk.values[0][-4:]):
                    try:
                        w, h, = calc_image_size(blk.spr)
                        pixbuf = GdkPixbuf.pixbuf.new_from_file_at_size(
                            blk.values[0], w, h)
                        x, y = self.calc_image_offset('', blk.spr)
                        blk.set_image(pixbuf, x, y)
                    except BaseException:
                        self._block_skin('journaloff', blk)
                else:
                    self._block_skin('journalon', blk)
            blk.spr.set_label(' ')
            blk.resize()
        elif btype in EXPANDABLE or \
                btype in expandable_blocks or \
                btype in EXPANDABLE_FLOW or \
                btype in EXPANDABLE_ARGS or \
                btype == 'nop':
            if btype == 'vspace' or btype in expandable_blocks:
                if value is not None:
                    blk.expand_in_y(value)
            elif btype == 'hspace' or btype == 'identity2':
                if value is not None:
                    blk.expand_in_x(value)
            elif btype in EXPANDABLE_FLOW:
                if value is not None:
                    if isinstance(value, int):
                        blk.expand_in_y(value)
                    elif btype == 'ifelse':
                        blk.expand_in_y(value[0])
                        blk.expand_in_y2(value[1])
            elif btype == 'templatelist' or btype == 'bulletlist':
                for i in range(len(b[4]) - 4):
                    blk.add_arg()
            elif btype == 'myfunc2arg' or \
                    btype == 'myfunc3arg' or \
                    btype == 'userdefined2args' or \
                    btype == 'userdefined3args' or\
                    btype == 'loadblock2arg' or \
                    btype == 'loadblock3arg':
                blk.add_arg()
            if btype == 'myfunc3arg' or \
                    btype == 'userdefined3args' or \
                    btype == 'loadblock3arg':
                blk.add_arg(False)
            if btype in PYTHON_SKIN:
                if self.nop == 'pythonloaded':
                    self._block_skin('pythonon', blk)
                else:
                    self._block_skin('pythonoff', blk)

        if self.interactive_mode:
            blk.spr.set_layer(BLOCK_LAYER)
        if check_dock:
            blk.connections = 'check'

        if self.running_sugar and len(blk.spr.labels) > 0 and \
                blk.name not in ['', ' ', 'number', 'string']:
            if len(self.used_block_list) > 0:
                self.used_block_list.append(', ')
            if blk.name in special_names:
                self.used_block_list.append(special_names[blk.name])
            elif blk.spr.labels[0] not in self.used_block_list:
                self.used_block_list.append(blk.spr.labels[0])
        return blk

    def _check_for_duplicate(self, name):
        ''' Is there already a block of this name? '''
        for blk in self.just_blocks():
            if blk.name == name:
                return True
        return False

    def load_start(self, ta_file=None):
        ''' Start a new project with a 'start' brick '''
        if ta_file is None:
            self.process_data(
                [[0, 'start', PALETTE_WIDTH + 20,
                  self.toolbar_offset + PALETTE_HEIGHT + 20 + ICON_SIZE,
                  [None, None]]])
        else:
            self.process_data(data_from_file(ta_file))
            self._loaded_project = ta_file

    def save_file(self, file_name=None):
        ''' Start a project to a file '''
        if self.save_folder is not None:
            self.load_save_folder = self.save_folder
        if file_name is None:
            file_name, self.load_save_folder = get_save_name(
                '.t[a-b]', self.load_save_folder, self.save_file_name)
        if not is_writeable(self.load_save_folder):
            if self.running_sugar:  # Shouldn't occur in Sugar
                debug_output('Cannot write data to %s.' %
                             self.load_save_folder, self.running_sugar)
            else:
                title = _('Cannot write data to %s.') % self.load_save_folder
                msg = _('Please choose a different save directory.')
                dlg = Gtk.MessageDialog(parent=None, type=Gtk.MessageType.INFO,
                                        buttons=Gtk.ButtonsType.OK_CANCEL,
                                        message_format=title)
                dlg.format_secondary_text(msg)
                dlg.set_title(title)
                dlg.set_property('skip-taskbar-hint', False)

                dlg.run()
                dlg.destroy()
            return
        if file_name is None:
            return
        if not file_name.endswith(SUFFIX):
            file_name = file_name + SUFFIX[1]
        if os.path.exists(file_name) and not is_writeable(file_name):
            if self.running_sugar:  # Shouldn't occur in Sugar
                debug_output('Cannot write data to %s.' % file_name,
                             self.running_sugar)
            else:
                title = _('Cannot write data to %s.') % file_name
                msg = _('Please choose a different file name.')
                dlg = Gtk.MessageDialog(parent=None, type=Gtk.MessageType.INFO,
                                        buttons=Gtk.ButtonsType.CANCEL,
                                        message_format=title)
                dlg.format_secondary_text(msg)
                dlg.set_title(title)
                dlg.set_property('skip-taskbar-hint', False)

                dlg.run()
                dlg.destroy()
            return
        data_to_file(self.assemble_data_to_save(), file_name)
        self.save_file_name = os.path.basename(file_name)
        if not self.running_sugar:
            self.save_folder = self.load_save_folder

    def assemble_data_to_save(self, save_turtle=True, save_project=True):
        ''' Pack the project (or stack) into a datastream to be serialized '''
        data = []
        blks = []

        if save_project:
            blks = self.just_blocks()
        else:
            if self.selected_blk is None:
                return []
            blks = find_group(find_top_block(self.selected_blk))

        for i, blk in enumerate(blks):
            blk.id = i
        for blk in blks:
            if blk.name in content_blocks:
                if len(blk.values) > 0:
                    name = (blk.name, blk.values[0])
                else:
                    name = (blk.name)
            elif blk.name in block_styles['basic-style-var-arg'] and \
                    len(blk.values) > 0:
                name = (blk.name, blk.values[0])
            elif blk.name in EXPANDABLE or blk.name in expandable_blocks or \
                    blk.name in EXPANDABLE_ARGS or blk.name in EXPANDABLE_FLOW:
                ex, ey, ey2 = blk.get_expand_x_y()
                if blk.name in block_styles['clamp-style-else']:
                    name = (blk.name, (ey, ey2))
                elif ex > 0:
                    name = (blk.name, ex)
                elif ey > 0:
                    name = (blk.name, ey)
                else:
                    name = (blk.name, 0)
            else:
                name = (blk.name)
            if hasattr(blk, 'connections') and blk.connections is not None:
                connections = [get_id(cblk) for cblk in blk.connections]
            else:
                connections = None
            (sx, sy) = blk.spr.get_xy()
            # Add a slight offset for copy/paste
            if not save_project:
                sx += 20
                sy += 20
            if blk.private is not None:
                data.append((blk.id, name, sx, sy, connections, blk.private))
            else:
                data.append((blk.id, name, sx, sy, connections))
        if save_turtle:
            for turtle in iter(self.turtles.dict):
                # Don't save remote turtles
                if not self.remote_turtle(turtle):
                    # Save default turtle as 'Yertle'
                    if turtle == self.nick:
                        turtle = DEFAULT_TURTLE
                    pos = self.turtles.get_active_turtle().get_xy()
                    data.append(
                        (-1,
                         ['turtle', turtle],
                         pos[0], pos[1],
                         self.turtles.get_active_turtle().get_heading(),
                         self.turtles.get_active_turtle().get_color(),
                         self.turtles.get_active_turtle().get_shade(),
                         self.turtles.get_active_turtle().get_pen_size()))
            # Also save font scale
            data.append((-1, '_saved_font_scale', 0, 0, self.block_scale))

        return data

    def display_coordinates(self, clear=False):
        ''' Display the coordinates of the current turtle on the toolbar '''
        if not self.interactive_mode:
            return
        if clear:
            self._set_coordinates_label('')
        else:
            x = round_int(
                float(self.turtles.get_active_turtle().get_xy(
                )[0]) / self.coord_scale)
            y = round_int(
                float(
                    self.turtles.get_active_turtle().get_xy(
                    )[1]) / self.coord_scale)
            h = round_int(self.turtles.get_active_turtle().get_heading())
            if self.running_sugar:
                if int(x) == x and int(y) == y and int(h) == h:
                    formatting = '(%d, %d) %d'
                else:
                    formatting = '(%0.2f, %0.2f) %0.2f'
                self._set_coordinates_label(formatting % (x, y, h))
            elif self.interactive_mode:
                if int(x) == x and int(y) == y and int(h) == h:
                    formatting = '%s — %s: %d %s: %d %s: %d'
                else:
                    formatting = '%s — %s: %0.2f %s: %0.2f %s: %0.2f'
                self._set_coordinates_label(
                    formatting % (self.activity.name, _('xcor'), x,
                                  _('ycor'), y, _('heading'), h))
        self.update_counter = 0

    def _set_coordinates_label(self, text):
        if self.running_sugar:
            self.activity.coordinates_label.set_text(text)
            self.activity.coordinates_label.show()
        elif self.interactive_mode:
            self.parent.set_title(text)

    def print_(self, n, flag):
        """ Print object n to the bar at the bottom of the screen """
        if flag and (self.hide or self.step_time == 0):
            return

        # list
        if isinstance(n, list):
            heap_as_string = str(self.lc.heap)
            if len(heap_as_string) > 80:
                self.showlabel('print', str(self.lc.heap)[0:79] + '…')
            else:
                self.showlabel('print', str(self.lc.heap))
        # color
        elif isinstance(n, Color):
            if n.color is None:
                self.showlabel('print', '%s %d, %s %d' %
                               (_('shade'), n.shade,
                                _('gray'), n.gray))
            else:
                self.showlabel('print', '%s %d, %s %d, %s %d' %
                               (_('color'), n.color,
                                _('shade'), n.shade,
                                _('gray'), n.gray))
        # vector
        elif isinstance(n, Vector):
            self.showlabel('print', '%s' % n.get_vector_string())
        # media
        elif isinstance(n, Media):
            if (n.type == 'media' and n.value.lower()
                    not in media_blocks_dictionary):
                try:
                    if self.running_sugar:
                        from sugar3.datastore import datastore
                        try:
                            dsobject = datastore.get(n.value)
                        except BaseException:
                            debug_output("Couldn't open %s" % (n.value),
                                         self.running_sugar)
                        self.showlabel('print', dsobject.metadata['title'])
                        dsobject.destroy()
                    else:
                        self.showlabel('print', n.value)
                except IOError:
                    self.showlabel('print', str(n))
            else:
                self.showlabel('print', str(n))
        # string
        elif isinstance(n, str):
            self.showlabel('print', n)
        # integer
        elif isinstance(n, int):
            self.showlabel('print', n)
        # other number
        else:
            self.showlabel(
                'print',
                str(round_int(n)).replace('.', self.decimal_point))

    def showlabel(self, shp, label=''):
        ''' Display a message on a status block '''
        '''dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "This is an INFO MessageDialog")
        dialog.run()
        dialog.destroy()'''
        if not self.interactive_mode:
            debug_output(label, self.running_sugar)
            return
        # Don't overwrite an error message
        if not self._autohide_shape:
            return
        if shp in ['print', 'info', 'help']:
            self._autohide_shape = True
        else:
            self._autohide_shape = False
        if shp == 'syntaxerror' and str(label) != '':
            if str(label)[1:] in self.status_shapes:
                shp = str(label)[1:]
                label = ''
            else:
                shp = 'status'
        elif shp[0] == '#':
            shp = shp[1:]
            label = ''
        if self.running_sugar and \
           shp not in ['print', 'status', 'info', 'help']:
            self.activity.error_list.append(shp)
        self.status_spr.set_shape(self.status_shapes[shp])
        self.status_spr.set_label_attributes(12.0, rescale=False)
        if shp == 'status':
            # Make sure True and False get added to the POT file
            if label in ['True', 'False', _('True'), _('False')]:
                label = _(label)
            self.status_spr.set_label('"%s"' % (str(label)))
        else:
            self.status_spr.set_label(str(label))
        self.status_spr.set_layer(STATUS_LAYER)
        if shp == 'info':
            self.status_spr.move((PALETTE_WIDTH, self.height - 400))
        else:
            # Adjust vertical position based on scrolled window adjustment
            if self.running_sugar:
                offset_from_bottom = self.activity.label_offset
                if self.activity.toolbox.get_property("visible"):
                    if self.activity.toolbars_expanded():
                        offset_from_bottom *= 3
                    else:
                        offset_from_bottom *= 2
                self.status_spr.move(
                    (0,
                     self.height - offset_from_bottom + self.activity.sw.get_vadjustment().get_value()))
            elif self.interactive_mode:
                self.status_spr.move(
                    (0, self.activity.win.get_window().get_height() - 80))

    def calc_position(self, template):
        ''' Relative placement of portfolio objects (deprecated) '''
        w, h, x, y, dx, dy = TEMPLATES[template]
        x *= self.canvas.width
        y *= self.canvas.height
        w *= (self.canvas.width - x)
        h *= (self.canvas.height - y)
        dx *= w
        dy *= h
        return(w, h, x, y, dx, dy)

    def save_for_upload(self, file_name):
        ''' Grab the current canvas and save it for upload '''
        if not file_name.endswith(SUFFIX):
            ta_file = file_name + SUFFIX[1]
            image_file = file_name + '.png'
        else:
            ta_file = file_name
            image_file = file_name[0:-3] + '.png'

        data_to_file(self.assemble_data_to_save(), ta_file)
        save_picture(self.canvas, image_file)
        return ta_file, image_file

    def save_as_odp(self, name=None):
        from .util.odp import TurtleODP

        path_list = []
        if self.running_sugar:
            from sugar3.datastore import datastore
            from sugar3 import profile
            for ds_id in self.saved_pictures:
                dsobj = datastore.get(ds_id[0])
                path_list.append(dsobj.file_path)
        else:
            for ds_id in self.saved_pictures:
                path_list.append(ds_id[0])
        if len(path_list) < 1:
            debug_output('nothing to save to ODP', self.running_sugar)
            return

        pres = TurtleODP()
        pres.create_presentation(TMP_ODP_PATH, 1024, 768)
        for file_path in path_list:
            pres.add_image(file_path)
        pres.save_presentation()

        if self.running_sugar:
            dsobject = datastore.create()
            if name is None:
                dsobject.metadata['title'] = '%s.odp' % \
                    (self.activity.metadata['title'])
            else:
                dsobject.metadata['title'] = name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = \
                'application/vnd.oasis.opendocument.presentation'
            dsobject.set_file_path(TMP_ODP_PATH)
            datastore.write(dsobject)
            dsobject.destroy()
            os.remove(TMP_ODP_PATH)
        else:
            if self.save_folder is not None:
                self.load_save_folder = self.save_folder
                name, self.load_save_folder = get_save_name(
                    '.odp', self.load_save_folder, 'turtleblocks.odp')
                datapath = self.load_save_folder
            else:
                datapath = os.getcwd()
                if '.odp' not in name:
                    name = name + '.odp'
            if name is not None:
                subprocess.check_output(
                    ['cp', TMP_ODP_PATH, os.path.join(datapath, name)])

    def save_as_icon(self, name=''):
        from .util.sugariconify import SugarIconify

        path = self.canvas.get_svg_path()
        self._ensure_square_svg(path)  # icons are square

        output_dir, basename = os.path.split(path)

        icon = SugarIconify()
        icon.set_use_default_colors(True)
        icon.set_output_path(output_dir)
        icon.set_stroke_color('rgb(0%,0%,0%)')
        icon.set_fill_color('rgb(99.215686%,99.215686%,99.215686%)')
        icon.iconify(path)

        # replace .svg with .sugar.svg
        sugarized_path = os.path.join(output_dir, basename[:-4] + '.sugar.svg')

        if self.running_sugar:
            from sugar3.datastore import datastore
            from sugar3 import profile

            dsobject = datastore.create()
            if len(name) == 0:
                dsobject.metadata['title'] = '%s %s' % \
                    (self.activity.metadata['title'], _('icon'))
            else:
                dsobject.metadata['title'] = name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'image/svg+xml'
            dsobject.set_file_path(sugarized_path)
            datastore.write(dsobject)
            dsobject.destroy()
            self.saved_pictures.append((dsobject.object_id, True))
            os.remove(sugarized_path)
        else:
            if len(name) == 0:
                name = 'turtleblocks-icon.svg'
            if self.save_folder is not None:
                self.load_save_folder = self.save_folder
                name, self.load_save_folder = get_save_name(
                    '.svg', self.load_save_folder, name)
                datapath = self.load_save_folder
            else:
                datapath = os.getcwd()
                if '.svg' not in name:
                    name = name + '.svg'
            subprocess.check_output(
                ['cp', TMP_SVG_PATH, os.path.join(datapath, name)])

    def write_svg_operation(self):
        self.canvas.svg_close()
        self.canvas.svg_reset()

    def _ensure_square_svg(self, path):
        from xml.dom import minidom

        fil = open(path, 'r')
        svg_text = fil.read()
        fil.close()

        svg_xml = minidom.parseString(svg_text)
        svg_element = svg_xml.getElementsByTagName('svg')[0]

        width = int(svg_element.getAttribute('width')[:-2])
        height = int(svg_element.getAttribute('height')[:-2])
        size = min(width, height)

        svg_element.setAttribute('width', str(size) + 'pt')
        svg_element.setAttribute('height', str(size) + 'pt')

        if width > height:
            dx = int((width - size) / 2)
            view_box = '%d 0 %d %d' % (dx, size, size)
        else:
            dy = int((height - size) / 2)
            view_box = '0 %d %d %d' % (dy, size, size)

        svg_element.setAttribute('viewBox', view_box)
        svg_text = svg_xml.toxml()

        fil = open(path, 'w+')
        fil.write(svg_text)
        fil.close()

    def save_blocks_as_image(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                     self.canvas.width, self.canvas.height)
        context = cairo.Context(surface)
        s = Sprites(self.window)
        s.set_cairo_context(context)
        blocks = self.just_blocks()
        for block in blocks:
            s.append_to_list(block.spr)
        s.redraw_sprites(cr=context)

        if self.running_sugar:
            datapath = get_path(self.activity, 'instance')
            filename = _('%s blocks image' % (self.activity.metadata['title']))
            file_path = os.path.join(datapath, filename + '.png')

            surface.write_to_png(file_path)

            from sugar3.datastore import datastore
            from sugar3 import profile

            dsobject = datastore.create()
            dsobject.metadata['title'] = filename
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'image/png'
            dsobject.set_file_path(file_path)
            datastore.write(dsobject)
            dsobject.destroy()
        else:
            datapath = os.getcwd()
            filename = 'turtleblocks'
            if self.save_folder is not None:
                datapath = self.save_folder
            filename, datapath = get_save_name('.png', datapath, filename)
            file_path = os.path.join(datapath, filename)

            surface.write_to_png(file_path)

    def save_as_image(self, name='', svg=False):
        ''' Grab the current canvas and save it. '''
        if svg:
            suffix = '.svg'
        else:
            suffix = '.png'

        # If we are running in non-interactive mode, we save as PNG
        if not self.interactive_mode:
            save_picture(self.canvas, name[:-3] + suffix)
            return

        if self.running_sugar:
            if len(name) == 0:
                filename = 'turtleblocks' + suffix
            else:
                filename = name + suffix
            datapath = get_path(self.activity, 'instance')
        elif len(name) == 0:
            name = 'turtleblocks' + suffix
            if self.save_folder is not None:
                self.load_save_folder = self.save_folder
            filename, self.load_save_folder = get_save_name(
                suffix, self.load_save_folder, name)
            datapath = self.load_save_folder
        else:
            datapath = os.getcwd()
            filename = name + suffix

        if filename is None:
            return

        file_path = os.path.join(datapath, filename)
        if svg:
            if self.canvas.cr_svg is None:
                return
            self.canvas.svg_close()
            self.canvas.svg_reset()
            svg_path = self.canvas.get_svg_path()
        else:
            save_picture(self.canvas, file_path)

        if self.running_sugar:
            from sugar3.datastore import datastore
            from sugar3 import profile

            dsobject = datastore.create()
            if len(name) == 0:
                dsobject.metadata['title'] = '%s %s' % \
                    (self.activity.metadata['title'], _('image'))
            else:
                dsobject.metadata['title'] = name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            if svg:
                dsobject.metadata['mime_type'] = 'image/svg+xml'
                dsobject.set_file_path(svg_path)
            else:
                dsobject.metadata['mime_type'] = 'image/png'
                dsobject.set_file_path(file_path)
            datastore.write(dsobject)
            dsobject.destroy()
            self.saved_pictures.append((dsobject.object_id, svg))
            if svg:
                os.remove(svg_path)
            else:
                os.remove(file_path)
        else:
            if svg:
                subprocess.check_output(
                    ['cp', svg_path, os.path.join(datapath, filename)])
            self.saved_pictures.append((file_path, svg))

    def just_blocks(self):
        ''' Filter out 'proto', 'trash', and 'deleted' blocks '''
        just_blocks_list = []
        for blk in self.block_list.list:
            if blk.type == 'block':
                just_blocks_list.append(blk)
        return just_blocks_list

    def just_protos(self):
        ''' Filter out 'block', 'trash', and 'deleted' blocks '''
        just_protos_list = []
        for blk in self.block_list.list:
            if blk.type == 'proto':
                just_protos_list.append(blk)
        return just_protos_list

    def _width_and_height(self, blk):
        ''' What are the width and height of a stack? '''
        minx = 10000
        miny = 10000
        maxx = -10000
        maxy = -10000
        for gblk in find_group(blk):
            (x, y) = gblk.spr.get_xy()
            w, h = gblk.spr.get_dimensions()
            if x < minx:
                minx = x
            if y < miny:
                miny = y
            if x + w > maxx:
                maxx = x + w
            if y + h > maxy:
                maxy = y + h
        return(maxx - minx, maxy - miny)

    # Utilities related to putting a image 'skin' on a block

    def calc_image_offset(self, name, spr, iw=0, ih=0):
        ''' Calculate the postion for placing an image onto a sprite. '''
        _l, _t = spr.label_left_top()
        if name == '':
            return _l, _t
        _w = spr.label_safe_width()
        _h = spr.label_safe_height()
        if iw == 0:
            iw = self.media_shapes[name].get_width()
            ih = self.media_shapes[name].get_height()
        return int(_l + (_w - iw) / 2), int(_t + (_h - ih) / 2)

    def _calc_w_h(self, name, spr):
        ''' Calculate new image size '''
        target_w = spr.label_safe_width()
        target_h = spr.label_safe_height()
        if name == '':
            return target_w, target_h
        image_w = self.media_shapes[name].get_width()
        image_h = self.media_shapes[name].get_height()
        scale_factor = float(target_w) / image_w
        new_w = target_w
        new_h = image_h * scale_factor
        if new_h > target_h:
            scale_factor = float(target_h) / new_h
            new_h = target_h
            new_w = target_w * scale_factor
        return int(new_w), int(new_h)

    def _block_skin(self, name, blk):
        ''' Some blocks get a skin '''
        x, y = self.calc_image_offset(name, blk.spr)
        blk.set_image(self.media_shapes[name], x, y)
        self._resize_skin(blk)

    def _resize_skin(self, blk):
        ''' Resize the 'skin' when block scale changes. '''
        if blk.name in PYTHON_SKIN:
            w, h = self._calc_w_h('pythonoff', blk.spr)
            x, y = self.calc_image_offset('pythonoff', blk.spr, w, h)
        elif blk.name == 'journal':
            if len(blk.values) == 1 and blk.values[0] is not None:
                w, h = self._calc_w_h('', blk.spr)
                x, y = self.calc_image_offset('journaloff', blk.spr, w, h)
            else:
                w, h = self._calc_w_h('journaloff', blk.spr)
                x, y = self.calc_image_offset('journaloff', blk.spr, w, h)
        else:
            # w, h = self._calc_w_h('descriptionoff', blk.spr)
            w, h = self._calc_w_h('', blk.spr)
            # x, y = self.calc_image_offset('descriptionoff', blk.spr, w, h)
            x, y = self.calc_image_offset('', blk.spr, w, h)
        blk.scale_image(x, y, w, h)

    def _find_proto_name(self, name, label, palette='blocks'):
        ''' Look for a protoblock with this name '''
        if not self.interactive_mode:
            return False
        i = palette_name_to_index(palette)
        for blk in self.palette_views[i].blocks:
            blk_label = blk.spr.labels[0]
            if blk.name == name and blk_label == label:
                return True
            # Check labels[1] too (e.g., store in block)
            if len(blk.spr.labels) > 1:
                blk_label = blk.spr.labels[1]
                if blk.name == name and blk_label == label:
                    return True
        return False

    def _new_stack_block(self, name):
        ''' Add a stack block to the 'blocks' palette '''
        if not self.interactive_mode:
            return
        if isinstance(name, (float, int)):
            return
        if name == _('action'):
            return
        # Choose a palette for the new block.
        palette = make_palette('blocks')

        # Create a new block prototype.
        palette.add_block('stack_%s' % (name),
                          style='basic-style-1arg',
                          label=name,
                          string_or_number=True,
                          prim_name='stack',
                          logo_command='action',
                          default=name,
                          help_string=_('invokes named action stack'))

        # Regenerate the palette, which will now include the new block.
        self.show_toolbar_palette(palette_name_to_index('blocks'),
                                  regenerate=True)

    def _new_box_block(self, name):
        ''' Add a box block to the 'blocks' palette '''
        if not self.interactive_mode:
            return
        if isinstance(name, (float, int)):
            return
        if name == _('my box'):
            return
        # Choose a palette for the new block.
        palette = make_palette('blocks')

        # Create a new block prototype.
        palette.add_block('box_%s' % (name),
                          style='number-style-1strarg',
                          label=name,
                          string_or_number=True,
                          prim_name='box',
                          default=name,
                          logo_command='box',
                          help_string=_('named variable (numeric value)'))

        # Regenerate the palette, which will now include the new block.
        self.show_toolbar_palette(palette_name_to_index('blocks'),
                                  regenerate=True)

    def _new_storein_block(self, name):
        ''' Add a storin block to the 'blocks' palette '''
        if not self.interactive_mode:
            return
        if isinstance(name, (float, int)):
            return
        if name == _('my box'):
            return
        # Choose a palette for the new block.
        palette = make_palette('blocks')

        # Create a new block prototype.
        palette.add_block('storein_%s' % (name),
                          style='basic-style-2arg',
                          label=[_('store in'), name, _('value')],
                          string_or_number=True,
                          prim_name='storeinbox',
                          logo_command='storeinbox',
                          default=[name, 100],
                          help_string=_('stores numeric value in named \
variable'))

        # Regenerate the palette, which will now include the new block.
        self.show_toolbar_palette(palette_name_to_index('blocks'),
                                  regenerate=True)

    def dock_dx_dy(self, block1, dock1n, block2, dock2n):
        ''' Find the distance between the dock points of two blocks. '''
        # Cannot dock a block to itself
        if block1 == block2:
            return _NO_DOCK
        dock1 = block1.docks[dock1n]
        dock2 = block2.docks[dock2n]
        # Dock types include flow, number, string, unavailable
        # Dock directions: Flow: True -> in; False -> out
        # Dock directions: Number: True -> out; False -> in
        # Each dock point as an associated relative x, y position on its block
        d1type, d1dir, d1x, d1y = dock1[0:4]
        d2type, d2dir, d2x, d2y = dock2[0:4]
        # Cannot dock to 'unavailable'
        if 'unavailable' in [d1type, d2type]:
            return _NO_DOCK
        # Cannot connect an innie to an innie or an outie to an outie
        if d1dir == d2dir:
            return _NO_DOCK
        # Flow blocks can be inserted into the middle of a stack
        if d2type == 'flow' and dock2n == 0:
            if block1.connections is not None and \
               dock1n == len(block1.connections) - 1 and \
               block1.connections[dock1n] is not None:
                self.inserting_block_mid_stack = True
            elif block1.connections is not None and \
                    block1.name in EXPANDABLE_FLOW and \
                    block1.connections[dock1n] is not None:
                self.inserting_block_mid_stack = True
        # Only number blocks can be docked when the dock is not empty
        elif d2type != 'number' or dock2n != 0:
            if block1.connections is not None and \
                    dock1n < len(block1.connections) and \
                    block1.connections[dock1n] is not None:
                return _NO_DOCK
            if block2.connections is not None and \
                    dock2n < len(block2.connections) and \
                    block2.connections[dock2n] is not None:
                return _NO_DOCK
        # Only some dock types are interchangeable
        if d1type != d2type:
            # Some blocks will take strings or numbers
            if block1.name in string_or_number_args:
                if d2type == 'number' or d2type == 'string':
                    pass
            # Some blocks will take content blocks
            elif block1.name in CONTENT_ARGS:
                if d2type in content_blocks:
                    pass
            else:
                return _NO_DOCK
        (b1x, b1y) = block1.spr.get_xy()
        (b2x, b2y) = block2.spr.get_xy()
        return ((b1x + d1x) - (b2x + d2x), (b1y + d1y) - (b2y + d2y))

    def prim_load_block(self, *args):
        ''' Load a block on to the canvas '''
        # Place the block at the active turtle (x, y) and move the turtle
        # into position to place the next block in the stack.
        # TODO: Add expandable argument, media block arguments
        name = args[0]
        pos = self.turtles.get_active_turtle().get_xy()
        values = []
        for i in range(len(args) - 1):
            values.append(args[i + 1])
        if len(values) > 0:
            dy = int(self._find_block(name, pos[0], pos[1], values))
        else:
            if name == 'delete':
                for blk in self.just_blocks():
                    if blk.status == 'load block':
                        blk.type = 'trash'
                        blk.spr.hide()
                dy = 0
            else:
                dy = int(self._find_block(name, pos[0], pos[1]))

        # Reposition turtle to end of flow
        pos = self.turtles.get_active_turtle().get_xy()
        pos[1] -= dy
        self.turtles.get_active_turtle().move_turtle(pos)

    def _make_block(self, name, x, y, defaults):
        if defaults is None:
            self._new_block(name, x, y, defaults)
        else:
            for i, v in enumerate(defaults):
                if isinstance(v, float) and int(v) == v:
                    defaults[i] = int(v)
            self._new_block(name, x, y, defaults)

        # Find the block we just created and attach it to a stack.
        self.drag_group = None
        spr = self.sprite_list.find_sprite((x, y))
        if spr is not None:
            blk = self.block_list.spr_to_block(spr)
            if blk is not None:
                self.drag_group = find_group(blk)
                for b in self.drag_group:
                    b.status = 'load block'
                self._snap_to_dock()

        # Disassociate new block from mouse.
        self.drag_group = None
        return blk.docks[-1][3]

    def _find_block(self, blkname, x, y, defaults=None):
        """ Create a new block. It is a bit more work than just calling
        _new_block(). We need to:
        (1) translate the label name into the internal block name;
        (2) 'dock' the block onto a stack where appropriate; and
        (3) disassociate the new block from the mouse. """
        x, y = self.turtles.turtle_to_screen_coordinates((x, y))
        for name in block_names:
            # Translate label name into block/prim name.
            if blkname in block_names[name]:  # block label is an array
                if name in content_blocks or \
                        (name in
                         block_primitives and block_primitives[name] == name):
                    return self._make_block(name, x, y, defaults)
            elif blkname in block_names:
                return self._make_block(blkname, x, y, defaults)
        for name in special_names:
            # Translate label name into block/prim name.
            if blkname in special_names[name]:
                return self._make_block(name, x, y, defaults)
        # Check for a macro
        if blkname in MACROS:
            self.new_macro(blkname, x, y)
            return 0  # Fix me: calculate flow position
        # Block not found
        raise logoerror("#syntaxerror")
        return -1

    def prim_load_palette(self, arg):
        ''' Select a palette '''
        if type(arg) in [int, float]:
            if int(arg) < 0 or int(arg) > len(palette_names):
                raise logoerror("#syntaxerror")
            else:
                self.show_toolbar_palette(int(arg))
        else:
            if arg in palette_names or arg in palette_i18n_names:
                self.show_toolbar_palette(palette_name_to_index(arg))
            else:
                raise logoerror("#syntaxerror")
