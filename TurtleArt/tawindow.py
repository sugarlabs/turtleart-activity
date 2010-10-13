# -*- coding: utf-8 -*-
#Copyright (c) 2007, Playful Invention Company
#Copyright (c) 2008-10, Walter Bender
#Copyright (c) 2009-10 Raúl Gutiérrez Segalés

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
import os
import os.path
from math import atan2, pi
DEGTOR = 2 * pi / 360

import locale
from gettext import gettext as _

try:
    from sugar.graphics.objectchooser import ObjectChooser
    from sugar.datastore import datastore
    from sugar import profile
except ImportError:
    pass

from taconstants import HORIZONTAL_PALETTE, VERTICAL_PALETTE, BLOCK_SCALE, \
                        PALETTE_NAMES, TITLEXY, MEDIA_SHAPES, STATUS_SHAPES, \
                        OVERLAY_SHAPES, TOOLBAR_SHAPES, TAB_LAYER, RETURN, \
                        OVERLAY_LAYER, CATEGORY_LAYER, BLOCKS_WITH_SKIN, \
                        ICON_SIZE, PALETTES, PALETTE_SCALE, BOX_STYLE_MEDIA, \
                        PALETTE_WIDTH, MACROS, TOP_LAYER, BLOCK_LAYER, \
                        CONTENT_BLOCKS, DEFAULTS, SPECIAL_NAMES, \
                        HELP_STRINGS, CURSOR, EXPANDABLE, COLLAPSIBLE, \
                        DEAD_DICTS, DEAD_KEYS, TEMPLATES, PYTHON_SKIN, \
                        PALETTE_HEIGHT, STATUS_LAYER, OLD_DOCK, OLD_NAMES, \
                        BOOLEAN_STYLE, BLOCK_NAMES, DEFAULT_TURTLE, \
                        TURTLE_LAYER, EXPANDABLE_BLOCKS, COMPARE_STYLE, \
                        BOOLEAN_STYLE, EXPANDABLE_ARGS, NUMBER_STYLE, \
                        NUMBER_STYLE_PORCH, NUMBER_STYLE_BLOCK, \
                        NUMBER_STYLE_VAR_ARG
from talogo import LogoCode, stop_logo
from tacanvas import TurtleGraphics
from tablock import Blocks, Block
from taturtle import Turtles, Turtle
from tautils import magnitude, get_load_name, get_save_name, data_from_file, \
                    data_to_file, round_int, get_id, get_pixbuf_from_journal, \
                    movie_media_type, audio_media_type, image_media_type, \
                    save_picture, save_svg, calc_image_size, get_path, \
                    reset_stack_arm, grow_stack_arm, find_sandwich_top, \
                    find_sandwich_bottom, restore_stack, collapse_stack, \
                    collapsed, collapsible, hide_button_hit, show_button_hit, \
                    arithmetic_check, xy, find_block_to_run, find_top_block, \
                    find_start_stack, find_group, find_blk_below, olpc_xo_1, \
                    dock_dx_dy, data_to_string, journal_check, chooser
from tasprite_factory import SVG, svg_str_to_pixbuf, svg_from_file
from sprites import Sprites, Sprite

import logging
_logger = logging.getLogger('turtleart-activity')


class TurtleArtWindow():
    """ TurtleArt Window class abstraction  """
    timeout_tag = [0]

    def __init__(self, win, path, parent=None, mycolors=None, mynick=None):
        self._loaded_project = ''
        self.win = None
        self.parent = parent
        if type(win) == gtk.DrawingArea:
            self.interactive_mode = True
            self.window = win
            self.window.set_flags(gtk.CAN_FOCUS)
            if self.parent is not None:
                self.parent.show_all()
                self.running_sugar = True
            else:
                self.window.show_all()
                self.running_sugar = False
            self.area = self.window.window
            self.gc = self.area.new_gc()
            self._setup_events()
        elif type(win) == gtk.gdk.Pixmap:
            self.interactive_mode = False
            self.window = win
            self.running_sugar = False
            self.gc = self.window.new_gc()
        else:
            _logger.debug("bad win type %s" % (type(win)))

        if self.running_sugar:
            self.activity = parent
            self.nick = profile.get_nick_name()
        else:
            self.activity = None
            self.nick = None

        self.path = path
        self.load_save_folder = os.path.join(path, 'samples')
        self.save_folder = None
        self.save_file_name = None
        self.width = gtk.gdk.screen_width()
        self.height = gtk.gdk.screen_height()
        self.rect = gtk.gdk.Rectangle(0, 0, 0, 0)

        self.keypress = ''
        self.keyvalue = 0
        self.dead_key = ''
        self.mouse_flag = 0
        self.mouse_x = 0
        self.mouse_y = 0

        locale.setlocale(locale.LC_NUMERIC, '')
        self.decimal_point = locale.localeconv()['decimal_point']
        if self.decimal_point == '' or self.decimal_point is None:
            self.decimal_point = '.'

        self.orientation = HORIZONTAL_PALETTE
        if olpc_xo_1():
            self.lead = 1.0
            self.scale = 0.67
            self.color_mode = '565'
            if self.running_sugar and not self.activity.new_sugar_system:
                self.orientation = VERTICAL_PALETTE
        else:
            self.lead = 1.0
            self.scale = 1.0
            self.color_mode = '888' # TODO: Read visual mode from gtk image

        self.block_scale = BLOCK_SCALE
        self.trash_scale = 0.5
        self.myblock = None
        self.nop = 'nop'
        self.loaded = 0
        self.step_time = 0
        self.hide = False
        self.palette = True
        self.coord_scale = 1
        self.buddies = []
        self.saved_string = ''
        self.dx = 0
        self.dy = 0
        self.media_shapes = {}
        self.cartesian = False
        self.polar = False
        self.overlay_shapes = {}
        self.toolbar_shapes = {}
        self.toolbar_offset = 0
        self.status_spr = None
        self.status_shapes = {}
        self.toolbar_spr = None
        self.palette_sprs = []
        self.palettes = []
        self.palette_button = []
        self.trash_index = PALETTE_NAMES.index('trash')
        self.trash_stack = []
        self.selected_palette = None
        self.previous_palette = None
        self.selectors = []
        self.selected_selector = None
        self.previous_selector = None
        self.selector_shapes = []
        self.selected_blk = None
        self.selected_spr = None
        self.drag_group = None
        self.drag_turtle = 'move', 0, 0
        self.drag_pos = 0, 0
        self.paste_offset = 20

        self.block_list = Blocks(font_scale_factor=self.scale,
                                 decimal_point=self.decimal_point)
        if self.interactive_mode:
            self.sprite_list = Sprites(self.window, self.area, self.gc)
        else:
            self.sprite_list = None

        self.turtles = Turtles(self.sprite_list)
        if mynick is None:
            self.default_turtle_name = DEFAULT_TURTLE
        else:
            self.default_turtle_name = mynick
        if mycolors is None:
            Turtle(self.turtles, self.default_turtle_name)
        else:
            Turtle(self.turtles, self.default_turtle_name, mycolors.split(','))
        self.active_turtle = self.turtles.get_turtle(self.default_turtle_name)

        self.saving_svg = False
        self.svg_string = ''
        self.selected_turtle = None
        self.canvas = TurtleGraphics(self, self.width, self.height)

        self.titlex = -(self.canvas.width * TITLEXY[0]) / \
            (self.coord_scale * 2)
        self.leftx = -(self.canvas.width * TITLEXY[0]) / \
            (self.coord_scale * 2)
        self.rightx = 0
        self.titley = (self.canvas.height * TITLEXY[1]) / \
            (self.coord_scale * 2)
        self.topy = (self.canvas.height * (TITLEXY[1] - 0.125)) / \
            (self.coord_scale * 2)
        self.bottomy = 0

        self.lc = LogoCode(self)
        self.saved_pictures = []

        if self.interactive_mode:
            self._setup_misc()
            self._show_toolbar_palette(0, False)

        self.block_operation = ''

    def _setup_events(self):
        """ Register the events we listen to. """
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.connect("expose-event", self._expose_cb)
        self.window.connect("button-press-event", self._buttonpress_cb)
        self.window.connect("button-release-event", self._buttonrelease_cb)
        self.window.connect("motion-notify-event", self._move_cb)
        self.window.connect("key_press_event", self._keypress_cb)

    def _setup_misc(self):
        """ Misc. sprites for status, overlays, etc. """
        # media blocks get positioned into other blocks
        for _name in MEDIA_SHAPES:
            if _name[0:7] == 'journal' and not self.running_sugar:
                file_name = 'file' + _name[7:]
            else:
                file_name = _name
            self.media_shapes[_name] = svg_str_to_pixbuf(svg_from_file(
                    "%s/images/%s.svg" % (self.path, file_name)))

        for i, _name in enumerate(STATUS_SHAPES):
            self.status_shapes[_name] = svg_str_to_pixbuf(svg_from_file(
                    "%s/images/%s.svg" % (self.path, _name)))
        self.status_spr = Sprite(self.sprite_list, 0, self.height - 200,
                                 self.status_shapes['status'])
        self.status_spr.hide()
        self.status_spr.type = 'status'

        for _name in OVERLAY_SHAPES:
            self.overlay_shapes[_name] = Sprite(self.sprite_list,
                                                int(self.width / 2 - 600),
                                                int(self.height / 2 - 450),
                                                svg_str_to_pixbuf(
                    svg_from_file("%s/images/%s.svg" % (self.path, _name))))
            self.overlay_shapes[_name].hide()
            self.overlay_shapes[_name].type = 'overlay'

        if not self.running_sugar:
            offset = self.width - 55 * len(TOOLBAR_SHAPES)
            for i, _name in enumerate(TOOLBAR_SHAPES):
                self.toolbar_shapes[_name] = Sprite(self.sprite_list,
                                                    i * 55 + offset, 0,
                                                    svg_str_to_pixbuf(
                        svg_from_file("%s/icons/%s.svg" % (self.path, _name))))
                self.toolbar_shapes[_name].set_layer(TAB_LAYER)
                self.toolbar_shapes[_name].name = _name
                self.toolbar_shapes[_name].type = 'toolbar'
            self.toolbar_shapes['stopiton'].hide()

    def sharing(self):
        """ Is a chattube available for share? """
        if self.running_sugar and hasattr(self.activity, 'chattube') and\
           self.activity.chattube is not None:
            return True
        return False

    def is_project_empty(self):
        """ Check to see if project has any blocks in use """
        return len(self.just_blocks()) == 1

    def _expose_cb(self, win, event):
        """ Repaint """
        self.sprite_list.refresh(event)
        return True

    def eraser_button(self):
        """ Eraser_button (hide status block when clearing the screen.) """
        if self.status_spr is not None:
            self.status_spr.hide()
        self.lc.prim_clear()
        self.display_coordinates()

    def run_button(self, time):
        """ Run turtle! """
        if self.running_sugar:
            self.activity.recenter()

        # Look for a 'start' block
        for blk in self.just_blocks():
            if find_start_stack(blk):
                self.step_time = time
                _logger.debug("running stack starting from %s" % (blk.name))
                self._run_stack(blk)
                return

        # If there is no 'start' block, run stacks that aren't 'def action'
        for blk in self.just_blocks():
            if find_block_to_run(blk):
                self.step_time = time
                _logger.debug("running stack starting from %s" % (blk.name))
                self._run_stack(blk)
        return

    def stop_button(self):
        """ Stop button """
        stop_logo(self)

    def set_userdefined(self):
        """ Change icon for user-defined blocks after loading Python code. """
        for blk in self.just_blocks():
            if blk.name in PYTHON_SKIN:
                x, y = self._calc_image_offset('pythonon', blk.spr)
                blk.set_image(self.media_shapes['pythonon'], x, y)
                self._resize_skin(blk)
        self.nop = 'pythonloaded'

    def set_fullscreen(self):
        """ Enter fullscreen mode """
        if self.running_sugar:
            self.activity.fullscreen()
            self.activity.recenter()

    def set_cartesian(self, flag):
        """ Turn on/off Cartesian coordinates """
        if flag:
            if self.coord_scale == 1:
                self.overlay_shapes['Cartesian_labeled'].set_layer(
                    OVERLAY_LAYER)
            else:
                self.overlay_shapes['Cartesian'].set_layer(OVERLAY_LAYER)
            self.cartesian = True
        else:
            if self.coord_scale == 1:
                self.overlay_shapes['Cartesian_labeled'].hide()
            else:
                self.overlay_shapes['Cartesian'].hide()
            self.cartesian = False

    def set_polar(self, flag):
        """ Turn on/off polar coordinates """
        if flag:
            self.overlay_shapes['polar'].set_layer(OVERLAY_LAYER)
            self.polar = True
        else:
            self.overlay_shapes['polar'].hide()
            self.polar = False

    def update_overlay_position(self, widget, event):
        """ Reposition the overlays when window size changes """
        self.width = event.width
        self.height = event.height
        for _name in OVERLAY_SHAPES:
            shape = self.overlay_shapes[_name]
            showing = False
            if shape in shape._sprites.list:
                shape.hide()
                showing = True
            self.overlay_shapes[_name] = Sprite(self.sprite_list,
                                                int(self.width / 2 - 600),
                                                int(self.height / 2 - 450),
                                                svg_str_to_pixbuf(
                    svg_from_file("%s/images/%s.svg" % (self.path, _name))))
            if showing:
                self.overlay_shapes[_name].set_layer(OVERLAY_LAYER)
            else:
                self.overlay_shapes[_name].hide()
            self.overlay_shapes[_name].type = 'overlay'
        self.cartesian = False
        self.polar = False
        self.canvas.width = self.width
        self.canvas.height = self.height
        self.canvas.move_turtle()

    def hideshow_button(self):
        """ Hide/show button """
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
            if self.activity is not None and self.activity.new_sugar_system:
                self.activity.palette_buttons[0].set_icon(
                                                       PALETTE_NAMES[0] + 'on')
            self.hide = False
            if self.running_sugar:
                self.activity.recenter()

        self.canvas.canvas.inval()

    def hideshow_palette(self, state):
        """ Hide or show palette  """
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

    def show_palette(self, n=0):
        """ Show palette  """
        self._show_toolbar_palette(n)
        self.palette_button[self.orientation].set_layer(TAB_LAYER)
        self.palette_button[2].set_layer(TAB_LAYER)
        if self.activity is None or not self.activity.new_sugar_system:
            self.toolbar_spr.set_layer(CATEGORY_LAYER)
        self.palette = True

    def hide_palette(self):
        """ Hide the palette. """
        self._hide_toolbar_palette()
        self.palette_button[self.orientation].hide()
        self.palette_button[2].hide()
        if self.activity is None or not self.activity.new_sugar_system:
            self.toolbar_spr.hide()
        self.palette = False

    def hideblocks(self):
        """ Callback from 'hide blocks' block """
        if not self.interactive_mode:
            return
        self.hide = False
        self.hideshow_button()
        if self.running_sugar:
            self.activity.do_hide()

    def showblocks(self):
        """ Callback from 'show blocks' block """
        if not self.interactive_mode:
            return
        self.hide = True
        self.hideshow_button()
        if self.running_sugar:
            self.activity.do_show()

    def resize_blocks(self, blocks=None):
        """ Resize blocks or if blocks is None, all of the blocks """
        if blocks is None:
            blocks = self.just_blocks()

        # We need to restore collapsed stacks before resizing.
        for blk in blocks:
            if blk.status == 'collapsed':
                bot = find_sandwich_bottom(blk)
                if collapsed(bot):
                    dy = bot.values[0]
                    restore_stack(find_sandwich_top(blk))
                    bot.values[0] = dy

        # Do the resizing.
        for blk in blocks:
            blk.rescale(self.block_scale)
        for blk in blocks:
            self._adjust_dock_positions(blk)

        # Re-collapsed stacks after resizing.
        for blk in blocks:
            if collapsed(blk):
                collapse_stack(find_sandwich_top(blk))
        for blk in blocks:
            if blk.name in ['sandwichtop', 'sandwichtop_no_label']:
                grow_stack_arm(blk)

        # Resize the skins on some blocks: media content and Python
        for blk in blocks:
            if blk.name in BLOCKS_WITH_SKIN:
                self._resize_skin(blk)

    def _show_toolbar_palette(self, n, init_only=False):
        """ Show the toolbar palettes, creating them on init_only """
        if (self.activity is None or not self.activity.new_sugar_system) and\
           self.selectors == []:
            # Create the selectors
            svg = SVG()
            x, y = 50, 0
            for i, name in enumerate(PALETTE_NAMES):
                a = svg_str_to_pixbuf(svg_from_file("%s/icons/%soff.svg" % (
                                                    self.path, name)))
                b = svg_str_to_pixbuf(svg_from_file("%s/icons/%son.svg" % (
                                                    self.path, name)))
                self.selector_shapes.append([a, b])
                self.selectors.append(Sprite(self.sprite_list, x, y, a))
                self.selectors[i].type = 'selector'
                self.selectors[i].name = name
                self.selectors[i].set_layer(TAB_LAYER)
                w = self.selectors[i].get_dimensions()[0]
                x += int(w)

            # Create the toolbar background
            self.toolbar_offset = ICON_SIZE
            self.toolbar_spr = Sprite(self.sprite_list, 0, 0,
                svg_str_to_pixbuf(svg.toolbar(self.width, ICON_SIZE)))
            self.toolbar_spr.type = 'toolbar'
            self.toolbar_spr.set_layer(CATEGORY_LAYER)


        if self.palette_sprs == []:
            # Create the empty palettes
            if len(self.palettes) == 0:
                for i in range(len(PALETTES)):
                    self.palettes.append([])

            # Create empty palette backgrounds
            for i in PALETTE_NAMES:
                self.palette_sprs.append([None, None])

            # Create the palette orientation button
            self.palette_button.append(Sprite(self.sprite_list, 0,
                self.toolbar_offset, svg_str_to_pixbuf(svg_from_file(
                            "%s/images/palettehorizontal.svg" % (self.path)))))
            self.palette_button.append(Sprite(self.sprite_list, 0,
                self.toolbar_offset, svg_str_to_pixbuf(svg_from_file(
                            "%s/images/palettevertical.svg" % (self.path)))))
            self.palette_button[0].name = _('orientation')
            self.palette_button[1].name = _('orientation')
            self.palette_button[0].type = 'palette'
            self.palette_button[1].type = 'palette'
            self.palette_button[self.orientation].set_layer(TAB_LAYER)
            self.palette_button[1 - self.orientation].hide()

            # Create the palette next button
            self.palette_button.append(Sprite(self.sprite_list, 16,
                self.toolbar_offset, svg_str_to_pixbuf(svg_from_file(
                            "%s/images/palettenext.svg" % (self.path)))))
            self.palette_button[2].name = _('next')
            self.palette_button[2].type = 'palette'
            self.palette_button[2].set_layer(TAB_LAYER)

        if init_only:
            return

        # Hide the previously displayed palette
        self._hide_previous_palette()

        self.selected_palette = n
        self.previous_palette = self.selected_palette

        if self.activity is None or not self.activity.new_sugar_system:
            self.selected_selector = self.selectors[n]
            # Make sure all of the selectors are visible.
            self.selectors[n].set_shape(self.selector_shapes[n][1])
            for i in range(len(PALETTES)):
                self.selectors[i].set_layer(TAB_LAYER)

        # Show the palette with the current orientation.
        if self.palette_sprs[n][self.orientation] is not None:
            self.palette_sprs[n][self.orientation].set_layer(CATEGORY_LAYER)

        if self.palettes[n] == []:
            # Create 'proto' blocks for each palette entry
            for i, name in enumerate(PALETTES[n]):
                self.palettes[n].append(Block(self.block_list,
                    self.sprite_list, name, 0, 0, 'proto', [], PALETTE_SCALE))
                self.palettes[n][i].spr.set_layer(TAB_LAYER)
                self.palettes[n][i].unhighlight()

                # Some proto blocks get a skin.
                if name in BOX_STYLE_MEDIA:
                    self._proto_skin(name + 'small', n, i)
                elif name[:8] == 'template':
                    self._proto_skin(name[8:], n, i)
                elif name[:7] == 'picture':
                    self._proto_skin(name[7:], n, i)
                elif name in PYTHON_SKIN:
                    self._proto_skin('pythonsmall', n, i)

        self._layout_palette(n)
        for blk in self.palettes[n]:
            blk.spr.set_layer(TAB_LAYER)
        if n == self.trash_index:
            for blk in self.trash_stack:
                for gblk in find_group(blk):
                    if gblk.status != 'collapsed':
                        gblk.spr.set_layer(TAB_LAYER)

    def _hide_toolbar_palette(self):
        """ Hide the toolbar palettes """
        self._hide_previous_palette()
        if self.activity is None or not self.activity.new_sugar_system:
            # Hide the selectors
            for i in range(len(PALETTES)):
                self.selectors[i].hide()
        elif self.selected_palette is not None:
            self.activity.palette_buttons[self.selected_palette].set_icon(
                PALETTE_NAMES[self.selected_palette] + 'off')
        self.selected_palette = None
        self.previous_palette = None

    def _hide_previous_palette(self):
        """ Hide just the previously viewed toolbar palette """
        # Hide previous palette
        if self.previous_palette is not None:
            for i in range(len(PALETTES[self.previous_palette])):
                self.palettes[self.previous_palette][i].spr.hide()
            self.palette_sprs[self.previous_palette][
                              self.orientation].hide()
            if self.activity is None or not self.activity.new_sugar_system:
                self.selectors[self.previous_palette].set_shape(
                    self.selector_shapes[self.previous_palette][0])
            elif self.previous_palette is not None and \
                 self.previous_palette != self.selected_palette:
                self.activity.palette_buttons[self.previous_palette].set_icon(
                    PALETTE_NAMES[self.previous_palette] + 'off')
            if self.previous_palette == self.trash_index:
                for blk in self.trash_stack:
                    for gblk in find_group(blk):
                        gblk.spr.hide()

    def _horizontal_layout(self, x, y, blocks):
        """ Position prototypes in a horizontal palette. """
        _max_w = 0
        for blk in blocks:
            _w, _h = self._width_and_height(blk)
            if y + _h > PALETTE_HEIGHT + self.toolbar_offset:
                x += int(_max_w + 3)
                y = self.toolbar_offset + 3
                _max_w = 0
            (_bx, _by) = blk.spr.get_xy()
            _dx = x - _bx
            _dy = y - _by
            for g in find_group(blk):
                g.spr.move_relative((int(_dx), int(_dy)))
            y += int(_h + 3)
            if _w > _max_w:
                _max_w = _w
        return x, y, _max_w

    def _vertical_layout(self, x, y, blocks):
        """ Position prototypes in a vertical palette. """
        _row = []
        _row_w = 0
        _max_h = 0
        for _b in blocks:
            _w, _h = self._width_and_height(_b)
            if x + _w > PALETTE_WIDTH:
                # Recenter row.
                _dx = int((PALETTE_WIDTH - _row_w) / 2)
                for _r in _row:
                    for _g in find_group(_r):
                        _g.spr.move_relative((_dx, 0))
                _row = []
                _row_w = 0
                x = 4
                y += int(_max_h + 3)
                _max_h = 0
            _row.append(_b)
            _row_w += (4 + _w)
            (_bx, _by) = _b.spr.get_xy()
            _dx = int(x - _bx)
            _dy = int(y - _by)
            for _g in find_group(_b):
                _g.spr.move_relative((_dx, _dy))
            x += int(_w + 4)
            if _h > _max_h:
                _max_h = _h
        # Recenter last row.
        _dx = int((PALETTE_WIDTH - _row_w) / 2)
        for _r in _row:
            for _g in find_group(_r):
                _g.spr.move_relative((_dx, 0))
        return x, y, _max_h

    def _layout_palette(self, n):
        """ Layout prototypes in a palette. """
        if n is not None:
            if self.orientation == HORIZONTAL_PALETTE:
                _x, _y = 20, self.toolbar_offset + 5
                _x, _y, _max = self._horizontal_layout(_x, _y,
                                                       self.palettes[n])
                if n == self.trash_index:
                    _x, _y, _max = self._horizontal_layout(_x + _max, _y,
                                                           self.trash_stack)
                _w = _x + _max + 25
                if self.palette_sprs[n][self.orientation] is None:
                    svg = SVG()
                    self.palette_sprs[n][self.orientation] = Sprite(
                            self.sprite_list, 0, self.toolbar_offset,
                            svg_str_to_pixbuf(svg.palette(_w, PALETTE_HEIGHT)))
                    self.palette_sprs[n][self.orientation].type = 'category'
                if n == PALETTE_NAMES.index('trash'):
                    svg = SVG()
                    self.palette_sprs[n][self.orientation].set_shape(
                        svg_str_to_pixbuf(svg.palette(_w, PALETTE_HEIGHT)))
                self.palette_button[2].move((_w - 20, self.toolbar_offset))
            else:
                _x, _y = 5, self.toolbar_offset + 15
                _x, _y, _max = self._vertical_layout(_x, _y, self.palettes[n])
                if n == PALETTE_NAMES.index('trash'):
                    _x, _y, _max = self._vertical_layout(_x, _y + _max,
                                                         self.trash_stack)
                _h = _y + _max + 25 - self.toolbar_offset
                if self.palette_sprs[n][self.orientation] is None:
                    svg = SVG()
                    self.palette_sprs[n][self.orientation] = \
                        Sprite(self.sprite_list, 0, self.toolbar_offset,
                            svg_str_to_pixbuf(svg.palette(PALETTE_WIDTH, _h)))
                    self.palette_sprs[n][self.orientation].type = 'category'
                if n == PALETTE_NAMES.index('trash'):
                    svg = SVG()
                    self.palette_sprs[n][self.orientation].set_shape(
                        svg_str_to_pixbuf(svg.palette(PALETTE_WIDTH, _h)))
                self.palette_button[2].move((PALETTE_WIDTH - 20,
                                             self.toolbar_offset))
            self.palette_sprs[n][self.orientation].set_layer(CATEGORY_LAYER)

    def _buttonpress_cb(self, win, event):
        """ Button press """
        self.window.grab_focus()
        x, y = xy(event)
        self.mouse_flag = 1
        self.mouse_x = x
        self.mouse_y = y
        self.button_press(event.get_state() & gtk.gdk.CONTROL_MASK, x, y)
        return True

    def button_press(self, mask, x, y):
        self.block_operation = 'click'

        # Unselect things that may have been selected earlier
        if self.selected_blk is not None:
            self._unselect_block()
        self.selected_turtle = None

        # Always hide the status layer on a click
        if self.status_spr is not None:
            self.status_spr.hide()

        # Find out what was clicked
        spr = self.sprite_list.find_sprite((x, y))
        self.dx = 0
        self.dy = 0
        if spr is None:
            return True
        self.selected_spr = spr

        # From the sprite at x, y, look for a corresponding block
        blk = self.block_list.spr_to_block(spr)
        if blk is not None:
            if blk.type == 'block':
                self.selected_blk = blk
                self._block_pressed(x, y, blk)
            elif blk.type == 'trash':
                self._restore_from_trash(find_top_block(blk))
            elif blk.type == 'proto':
                if blk.name == 'restoreall':
                    self._restore_all_from_trash()
                elif blk.name == 'restore':
                    self._restore_latest_from_trash()
                elif blk.name == 'empty':
                    self._empty_trash()
                elif blk.name in MACROS:
                    self._new_macro(blk.name, x + 20, y + 20)
                else:
                    blk.highlight()
                    self._new_block(blk.name, x, y)
                    blk.unhighlight()
            return True

        # Next, look for a turtle
        t = self.turtles.spr_to_turtle(spr)
        if t is not None:
            self.selected_turtle = t
            self.canvas.set_turtle(self.turtles.get_turtle_key(t))
            self._turtle_pressed(x, y)
            return True

        # Finally, check for anything else
        if hasattr(spr, 'type'):
            if spr.type == "canvas":
                pass
                # spr.set_layer(CANVAS_LAYER)
            elif spr.type == 'selector':
                self._select_category(spr)
            elif spr.type == 'category':
                if hide_button_hit(spr, x, y):
                    self.hideshow_palette(False)
            elif spr.type == 'palette':
                if spr.name == _('next'):
                    i = self.selected_palette + 1
                    if i == len(PALETTE_NAMES):
                        i = 0
                    if self.activity is None or \
                       not self.activity.new_sugar_system:
                        self._select_category(self.selectors[i])
                    else:
                        if self.selected_palette is not None:
                            self.activity.palette_buttons[
                                self.selected_palette].set_icon(
                                PALETTE_NAMES[self.selected_palette] + 'off')
                        self.activity.palette_buttons[i].set_icon(
                            PALETTE_NAMES[i] + 'on')
                        self.show_palette(i)
                else:
                    self.orientation = 1 - self.orientation
                    self.palette_button[self.orientation].set_layer(TAB_LAYER)
                    self.palette_button[1 - self.orientation].hide()
                    self.palette_sprs[self.selected_palette][
                        1 - self.orientation].hide()
                    self._layout_palette(self.selected_palette)
                    self.show_palette(self.selected_palette)
            elif spr.type == 'toolbar':
                self._select_toolbar_button(spr)
            return True

    def _select_category(self, spr):
        """ Select a category from the toolbar (old Sugar systems only). """
        i = self.selectors.index(spr)
        spr.set_shape(self.selector_shapes[i][1])
        if self.selected_selector is not None:
            j = self.selectors.index(self.selected_selector)
            if i == j:
                return
            self.selected_selector.set_shape(self.selector_shapes[j][0])
        self.previous_selector = self.selected_selector
        self.selected_selector = spr
        self.show_palette(i)

    def _select_toolbar_button(self, spr):
        """ Select a toolbar button (Used when not running Sugar). """
        if not hasattr(spr, 'name'):
            return
        if spr.name == 'run-fastoff':
            self.lc.trace = 0
            self.run_button(0)
        elif spr.name == 'run-slowoff':
            self.lc.trace = 0
            self.run_button(3)
        elif spr.name == 'debugoff':
            self.lc.trace = 1
            self.run_button(6)
        elif spr.name == 'stopiton':
            self.stop_button()
            self.toolbar_shapes['stopiton'].hide()
        elif spr.name == 'eraseron':
            self.eraser_button()
        elif spr.name == 'hideshowoff':
            self.hideshow_button()

    def _put_in_trash(self, blk, x=0, y=0):
        """ Put a group of blocks into the trash. """
        self.trash_stack.append(blk)
        group = find_group(blk)
        for gblk in group:
            if gblk.status == 'collapsed':
                # Collapsed stacks are restored for rescaling
                # and then recollapsed after they are moved to the trash.
                bot = find_sandwich_bottom(gblk)
                if collapsed(bot):
                    dy = bot.values[0]
                    restore_stack(find_sandwich_top(gblk))
                    bot.values[0] = dy
            gblk.type = 'trash'
            gblk.rescale(self.trash_scale)
        blk.spr.move((x, y))
        for gblk in group:
            self._adjust_dock_positions(gblk)

        # Re-collapsing any stacks we had restored for scaling
        for gblk in group:
            if collapsed(gblk):
                collapse_stack(find_sandwich_top(gblk))

        # And resize any skins.
        for gblk in group:
            if gblk.name in BLOCKS_WITH_SKIN:
                self._resize_skin(gblk)

        # self.show_palette(self.trash_index)
        if self.selected_palette != self.trash_index:
            for gblk in group:
                gblk.spr.hide()

    def _restore_all_from_trash(self):
        """ Restore all the blocks in the trash can. """
        for blk in self.block_list.list:
            if blk.type == 'trash':
                self._restore_from_trash(blk)

    def _restore_latest_from_trash(self):
        """ Restore most recent blocks from the trash can. """
        if len(self.trash_stack) == 0:
            return
        self._restore_from_trash(self.trash_stack[len(self.trash_stack) - 1])

    def _restore_from_trash(self, blk):
        group = find_group(blk)
        for gblk in group:
            gblk.rescale(self.block_scale)
            gblk.spr.set_layer(BLOCK_LAYER)
            x, y = gblk.spr.get_xy()
            if self.orientation == 0:
                gblk.spr.move((x, y + PALETTE_HEIGHT + self.toolbar_offset))
            else:
                gblk.spr.move((x + PALETTE_WIDTH, y))
            gblk.type = 'block'
        for gblk in group:
            self._adjust_dock_positions(gblk)
        # If the stack had been collapsed before going into the trash,
        # collapse it again now.
        for gblk in group:
            if collapsed(gblk):
                collapse_stack(find_sandwich_top(gblk))
        # And resize any skins.
        for gblk in group:
            if gblk.name in BLOCKS_WITH_SKIN:
                self._resize_skin(gblk)

        self.trash_stack.remove(blk)

    def _empty_trash(self):
        """ Permanently remove all blocks presently in the trash can. """
        for blk in self.block_list.list:
            if blk.type == 'trash':
                blk.type = 'deleted'
                blk.spr.hide()
        self.trash_stack = []

    def _in_the_trash(self, x, y):
        """ Is x, y over the trash can? """
        """
        if self.selected_palette == self.trash_index and \
           self.palette_sprs[self.trash_index][self.orientation].hit((x, y)):
            return True
        """
        if self.selected_palette is not None and \
           self.palette_sprs[self.selected_palette][self.orientation].hit(
            (x, y)):
            return True
        return False

    def _block_pressed(self, x, y, blk):
        """ Block pressed """
        if blk is not None:
            blk.highlight()
            self._disconnect(blk)
            self.drag_group = find_group(blk)
            (sx, sy) = blk.spr.get_xy()
            self.drag_pos = x - sx, y - sy
            for blk in self.drag_group:
                if blk.status != 'collapsed':
                    blk.spr.set_layer(TOP_LAYER)
            self.saved_string = blk.spr.labels[0]

    def _unselect_block(self):
        """ Unselect block """
        # After unselecting a 'number' block, we need to check its value
        if self.selected_blk.name == 'number':
            self._number_check()
        elif self.selected_blk.name == 'string':
            self._string_check()
        self.selected_blk.unhighlight()
        self.selected_blk = None

    def _new_block(self, name, x, y):
        """ Make a new block. """
        if name in CONTENT_BLOCKS:
            newblk = Block(self.block_list, self.sprite_list, name, x - 20,
                           y - 20, 'block', DEFAULTS[name], self.block_scale)
        else:
            newblk = Block(self.block_list, self.sprite_list, name, x - 20,
                           y - 20, 'block', [], self.block_scale)

        # Add a 'skin' to some blocks
        if name in PYTHON_SKIN:
            if self.nop == 'pythonloaded':
                self._block_skin('pythonon', newblk)
            else:
                self._block_skin('pythonoff', newblk)
        elif name in BOX_STYLE_MEDIA:
            self._block_skin(name + 'off', newblk)

        newspr = newblk.spr
        newspr.set_layer(TOP_LAYER)
        self.drag_pos = 20, 20
        newblk.connections = [None] * len(newblk.docks)
        if newblk.name in DEFAULTS:
            for i, argvalue in enumerate(DEFAULTS[newblk.name]):
                # skip the first dock position since it is always a connector
                dock = newblk.docks[i + 1]
                argname = dock[0]
                if argname == 'unavailable':
                    continue
                if argname == 'media':
                    argname = 'journal'
                elif argname == 'number' and \
                     (type(argvalue) is str or type(argvalue) is unicode):
                    argname = 'string'
                elif argname == 'bool':
                    argname = argvalue
                elif argname == 'flow':
                    argname = argvalue
                (sx, sy) = newspr.get_xy()
                if argname is not None:
                    if argname in CONTENT_BLOCKS:
                        argblk = Block(self.block_list, self.sprite_list,
                                       argname, 0, 0, 'block', [argvalue],
                                       self.block_scale)
                    else:
                        argblk = Block(self.block_list, self.sprite_list,
                                       argname, 0, 0, 'block', [],
                                       self.block_scale)
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

    def _new_macro(self, name, x, y):
        """ Create a "macro" (predefined stack of blocks). """
        macro = MACROS[name]
        macro[0][2] = x
        macro[0][3] = y
        top = self.process_data(macro)
        self.block_operation = 'new'
        self._check_collapsibles(top)
        self.drag_group = find_group(top)

    def process_data(self, block_data, offset=0):
        """ Process block_data (from a macro, a file, or the clipboard). """
        if offset != 0:
            _logger.debug("offset is %d" % (offset))
        # Create the blocks (or turtle).
        blocks = []
        for blk in block_data:
            if not self._found_a_turtle(blk):
                blocks.append(self.load_block(blk, offset))

        # Make the connections.
        for i in range(len(blocks)):
            cons = []
            # Normally, it is simply a matter of copying the connections.
            if blocks[i].connections is None:
                for c in block_data[i][4]:
                    if c is None:
                        cons.append(None)
                    else:
                        cons.append(blocks[c])
            elif blocks[i].connections == 'check':
                # Convert old-style boolean and arithmetic blocks
                cons.append(None) # Add an extra connection.
                for c in block_data[i][4]:
                    if c is None:
                        cons.append(None)
                    else:
                        cons.append(blocks[c])
                # If the boolean op was connected, readjust the plumbing.
                if blocks[i].name in BOOLEAN_STYLE:
                    if block_data[i][4][0] is not None:
                        c = block_data[i][4][0]
                        cons[0] = blocks[block_data[c][4][0]]
                        c0 = block_data[c][4][0]
                        for j, cj in enumerate(block_data[c0][4]):
                            if cj == c:
                                blocks[c0].connections[j] = blocks[i]
                        if c < i:
                            blocks[c].connections[0] = blocks[i]
                            blocks[c].connections[3] = None
                        else:
                            # Connection was to a block we haven't seen yet.
                            _logger.debug("Warning: dock to the future")
                else:
                    if block_data[i][4][0] is not None:
                        c = block_data[i][4][0]
                        cons[0] = blocks[block_data[c][4][0]]
                        c0 = block_data[c][4][0]
                        for j, cj in enumerate(block_data[c0][4]):
                            if cj == c:
                                blocks[c0].connections[j] = blocks[i]
                        if c < i:
                            blocks[c].connections[0] = blocks[i]
                            blocks[c].connections[1] = None
                        else:
                            # Connection was to a block we haven't seen yet.
                            _logger.debug("Warning: dock to the future")
            else:
                _logger.debug("Warning: unknown connection state %s" % \
                                  (str(blocks[i].connections)))
            blocks[i].connections = cons[:]

        # Block sizes and shapes may have changed.
        for blk in blocks:
            self._adjust_dock_positions(blk)

        # Look for any stacks that need to be collapsed or sandwiched
        for blk in blocks:
            if collapsed(blk):
                collapse_stack(find_sandwich_top(blk))
            elif blk.name == 'sandwichbottom' and collapsible(blk):
                blk.svg.set_hide(True)
                blk.svg.set_show(False)
                blk.refresh()
                grow_stack_arm(find_sandwich_top(blk))

        # Resize blocks to current scale
        self.resize_blocks(blocks)

        if len(blocks) > 0:
            return blocks[0]
        else:
            return None

    def _adjust_dock_positions(self, blk):
        """ Adjust the dock x, y positions """
        if not self.interactive_mode:
            return
        (sx, sy) = blk.spr.get_xy()
        for i, c in enumerate(blk.connections):
            if i > 0 and c is not None:
                bdock = blk.docks[i]
                for j in range(len(c.docks)):
                    if c.connections[j] == blk:
                        cdock = c.docks[j]
                        nx = sx + bdock[2] - cdock[2]
                        ny = sy + bdock[3] - cdock[3]
                        c.spr.move((nx, ny))
                self._adjust_dock_positions(c)

    def _turtle_pressed(self, x, y):
        (tx, ty) = self.selected_turtle.get_xy()
        w = self.active_turtle.spr.rect.width / 2
        h = self.active_turtle.spr.rect.height / 2
        dx = x - tx - w
        dy = y - ty - h
        # if x, y is near the edge, rotate
        if (dx * dx) + (dy * dy) > ((w * w) + (h * h)) / 6:
            self.drag_turtle = ('turn',
                self.canvas.heading - atan2(dy, dx) / DEGTOR, 0)
        else:
            self.drag_turtle = ('move', x - tx, y - ty)

    def _move_cb(self, win, event):
        x, y = xy(event)
        self._mouse_move(x, y)
        return True

    def _mouse_move(self, x, y):
        """ Process mouse movements """
        self.block_operation = 'move'

        # First, check to see if we are dragging or rotating a turtle.
        if self.selected_turtle is not None:
            dtype, dragx, dragy = self.drag_turtle
            (sx, sy) = self.selected_turtle.get_xy()
            if dtype == 'move':
                dx = x - dragx - sx
                dy = y - dragy - sy
                self.selected_turtle.spr.set_layer(TOP_LAYER)
                self.selected_turtle.move((sx + dx, sy + dy))
            else:
                dx = x - sx - self.active_turtle.spr.rect.width / 2
                dy = y - sy - self.active_turtle.spr.rect.height / 2
                self.canvas.seth(int(dragx + atan2(dy, dx) / DEGTOR + 5) / \
                                     10 * 10)

        # If we are hoving, show popup help.
        elif self.drag_group is None:
            self._show_popup(x, y)
            return

        # If we have a stack of blocks selected, move them.
        elif self.drag_group[0] is not None:
            blk = self.drag_group[0]

            # Don't move a bottom blk if the stack is collapsed
            if collapsed(blk):
                return

            self.selected_spr = blk.spr
            dragx, dragy = self.drag_pos
            (sx, sy) = blk.spr.get_xy()
            dx = x - dragx - sx
            dy = y - dragy - sy

            # Take no action if there was a move of 0,0.
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
            self.sprite_list.area.invalidate_rect(self.rect, False)

        self.dx += dx
        self.dy += dy

    def _show_popup(self, x, y):
        """ Let's help our users by displaying a little help. """
        spr = self.sprite_list.find_sprite((x, y))
        blk = self.block_list.spr_to_block(spr)
        if spr and blk is not None:
            if self.timeout_tag[0] == 0:
                self.timeout_tag[0] = self._do_show_popup(blk.name)
                self.selected_spr = spr
            else:
                if self.timeout_tag[0] > 0:
                    try:
                        gobject.source_remove(self.timeout_tag[0])
                        self.timeout_tag[0] = 0
                    except:
                        self.timeout_tag[0] = 0
        elif spr and hasattr(spr, 'type') and (spr.type == 'selector' or \
                                               spr.type == 'palette' or \
                                               spr.type == 'toolbar'):
            if self.timeout_tag[0] == 0 and hasattr(spr, 'name'):
                self.timeout_tag[0] = self._do_show_popup(spr.name)
                self.selected_spr = spr
            else:
                if self.timeout_tag[0] > 0:
                    try:
                        gobject.source_remove(self.timeout_tag[0])
                        self.timeout_tag[0] = 0
                    except:
                        self.timeout_tag[0] = 0
        else:
            if self.timeout_tag[0] > 0:
                try:
                    gobject.source_remove(self.timeout_tag[0])
                    self.timeout_tag[0] = 0
                except:
                    self.timeout_tag[0] = 0

    def _do_show_popup(self, block_name):
        """ Fetch the help text and display it.  """
        if block_name in SPECIAL_NAMES:
            block_name_s = SPECIAL_NAMES[block_name]
        elif block_name in BLOCK_NAMES:
            block_name_s = BLOCK_NAMES[block_name][0]
        elif block_name in TOOLBAR_SHAPES:
            block_name_s = ''
        else:
            block_name_s = _(block_name)
        if block_name in HELP_STRINGS:
            if block_name_s == '':
                label = HELP_STRINGS[block_name]
            else:
                label = block_name_s + ": " + HELP_STRINGS[block_name]
        else:
            label = block_name_s
        if self.running_sugar:
            self.activity.hover_help_label.set_text(label)
            self.activity.hover_help_label.show()
        else:
            if self.interactive_mode:
                self.win.set_title(_("Turtle Art") + " — " + label)
        return 0

    def _buttonrelease_cb(self, win, event):
        """ Button release """
        x, y = xy(event)
        self.button_release(x, y)
        return True

    def button_release(self, x, y):
        # We may have been moving the turtle
        if self.selected_turtle is not None:
            (tx, ty) = self.selected_turtle.get_xy()
            k = self.turtles.get_turtle_key(self.selected_turtle)

            # Remove turtles by dragging them onto the trash palette.
            if self._in_the_trash(tx, ty):
                # If it is the default turtle, just recenter it.
                if k == self.default_turtle_name:
                    self._move_turtle(0, 0)
                    self.canvas.heading = 0
                    self.canvas.turn_turtle()
                else:
                    self.selected_turtle.hide()
                    self.turtles.remove_from_dict(k)
            else:
                self._move_turtle(tx - self.canvas.width / 2 + \
                                      self.active_turtle.spr.rect.width / 2,
                                  self.canvas.height / 2 - ty - \
                                      self.active_turtle.spr.rect.height / 2)
            self.selected_turtle = None
            self.active_turtle = self.turtles.get_turtle(
                self.default_turtle_name)
            return

        # If we don't have a group of blocks, then there is nothing to do.
        if self.drag_group is None:
            return

        blk = self.drag_group[0]
        # Remove blocks by dragging them onto the trash palette.
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
        self._check_collapsibles(blk)
        for gblk in self.drag_group:
            if gblk.status != 'collapsed':
                gblk.spr.set_layer(BLOCK_LAYER)
        self.drag_group = None

        # Find the block we clicked on and process it.
        if self.block_operation == 'click':
            self._click_block(x, y)

    def _move_turtle(self, x, y):
        """ Move the selected turtle to (x, y). """
        (cx, cy) = self.canvas.canvas.get_xy()
        self.canvas.xcor = x - cx
        self.canvas.ycor = y + cy
        self.canvas.move_turtle()
        if self.running_sugar:
            self.display_coordinates()
            self.selected_turtle.spr.set_layer(TURTLE_LAYER)

    def _click_block(self, x, y):
        """ Click block: lots of special cases to handle... """
        blk = self.block_list.spr_to_block(self.selected_spr)
        if blk is None:
            return
        self.selected_blk = blk
        if  blk.name == 'number' or blk.name == 'string':
            self.saved_string = blk.spr.labels[0]
            blk.spr.labels[0] += CURSOR
        elif blk.name in BOX_STYLE_MEDIA:
            self._import_from_journal(self.selected_blk)
            if blk.name == 'journal' and self.running_sugar:
                self._load_description_block(blk)
        elif blk.name == 'identity2' or blk.name == 'hspace':
            group = find_group(blk)
            if hide_button_hit(blk.spr, x, y):
                dx = blk.reset_x()
            elif show_button_hit(blk.spr, x, y):
                dx = 20
                blk.expand_in_x(dx)
            else:
                dx = 0
            for gblk in group:
                if gblk != blk:
                    gblk.spr.move_relative((dx * blk.scale, 0))
        elif blk.name == 'vspace':
            group = find_group(blk)
            if hide_button_hit(blk.spr, x, y):
                dy = blk.reset_y()
            elif show_button_hit(blk.spr, x, y):
                dy = 20
                blk.expand_in_y(dy)
            else:
                dy = 0
            for gblk in group:
                if gblk != blk:
                    gblk.spr.move_relative((0, dy * blk.scale))
            grow_stack_arm(find_sandwich_top(blk))
        elif blk.name in EXPANDABLE_BLOCKS:
            # Connection may be lost during expansion, so store it...
            blk0 = blk.connections[0]
            if blk0 is not None:
                dock0 = blk0.connections.index(blk)

            if hide_button_hit(blk.spr, x, y):
                dy = blk.reset_y()
            elif show_button_hit(blk.spr, x, y):
                dy = 20
                blk.expand_in_y(dy)
            else:
                self._run_stack(blk)
                return

            if blk.name in BOOLEAN_STYLE:
                self._expand_boolean(blk, blk.connections[1], dy)
            else:
                self._expand_expandable(blk, blk.connections[1], dy)

            # and restore it...
            if blk0 is not None:
                blk.connections[0] = blk0
                blk0.connections[dock0] = blk
                self._cascade_expandable(blk)

            grow_stack_arm(find_sandwich_top(blk))

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
                elif blk.name == 'userdefined2args':
                    dy = blk.add_arg(False)
                    blk.primitive = 'userdefined3'
                    blk.name = 'userdefined3args'
                else:
                    dy = blk.add_arg()
                for gblk in group:
                    gblk.spr.move_relative((0, dy))
                blk.connections.append(blk.connections[n - 1])
                argname = blk.docks[n - 1][0]
                argvalue = DEFAULTS[blk.name][len(DEFAULTS[blk.name]) - 1]
                argblk = Block(self.block_list, self.sprite_list, argname,
                               0, 0, 'block', [argvalue], self.block_scale)
                argdock = argblk.docks[0]
                (bx, by) = blk.spr.get_xy()
                nx = bx + blk.docks[n - 1][2] - argdock[2]
                ny = by + blk.docks[n - 1][3] - argdock[3]
                argblk.spr.move((nx, ny))
                argblk.spr.set_layer(TOP_LAYER)
                argblk.connections = [blk, None]
                blk.connections[n - 1] = argblk
                if blk.name in NUMBER_STYLE_VAR_ARG:
                    self._cascade_expandable(blk)
                grow_stack_arm(find_sandwich_top(blk))
            elif blk.name in PYTHON_SKIN and self.myblock is None:
                self._import_py()
            else:
                self._run_stack(blk)
        elif blk.name in COLLAPSIBLE:
            top = find_sandwich_top(blk)
            if collapsed(blk):
                restore_stack(top)
            elif top is not None:
                collapse_stack(top)
        else:
            self._run_stack(blk)

    def _expand_boolean(self, blk, blk2, dy):
        """ Expand a boolean blk if blk2 is too big to fit. """
        group = find_group(blk2)
        for gblk in find_group(blk):
            if gblk not in group:
                gblk.spr.move_relative((0, -dy * blk.scale))

    def _expand_expandable(self, blk, blk2, dy):
        """ Expand an expandable blk if blk2 is too big to fit. """
        if blk2 is None:
            group = [blk]
        else:
            group = find_group(blk2)
            group.append(blk)
        for gblk in find_group(blk):
            if gblk not in group:
                gblk.spr.move_relative((0, dy * blk.scale))
        if blk.name in COMPARE_STYLE:
            for gblk in find_group(blk):
                gblk.spr.move_relative((0, -dy * blk.scale))

    def _cascade_expandable(self, blk):
        """ If expanding/shrinking a block, cascade. """
        while blk.name in NUMBER_STYLE or \
                blk.name in NUMBER_STYLE_PORCH or \
                blk.name in NUMBER_STYLE_BLOCK or \
                blk.name in NUMBER_STYLE_VAR_ARG:
            if blk.connections[0] is None:
                break
            if blk.connections[0].name in EXPANDABLE_BLOCKS:
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
                    if blk.name in COMPARE_STYLE:
                        for gblk in find_group(blk):
                            gblk.spr.move_relative((0, -dy * blk.scale))
            else:
                break

    def _check_collapsibles(self, blk):
        """ Check state of collapsible blocks upon change in dock state. """
        group = find_group(blk)
        for gblk in group:
            if gblk.name in COLLAPSIBLE:
                if collapsed(gblk):
                    gblk.svg.set_show(True)
                    gblk.svg.set_hide(False)
                    reset_stack_arm(find_sandwich_top(gblk))
                elif collapsible(gblk):
                    gblk.svg.set_hide(True)
                    gblk.svg.set_show(False)
                    grow_stack_arm(find_sandwich_top(gblk))
                else:
                    gblk.svg.set_hide(False)
                    gblk.svg.set_show(False)
                    # Ouch: When you tear off the sandwich bottom, you
                    # no longer have access to the group with the sandwich top
                    # so check them all.
                    for b in self.just_blocks():
                        if b.name  in ['sandwichtop', 'sandwichtop_no_label']:
                            if find_sandwich_bottom(b) is None:
                                reset_stack_arm(b)
                gblk.refresh()

    def _run_stack(self, blk):
        """ Run a stack of blocks. """
        if blk is None:
            return
        self.lc.ag = None
        top = find_top_block(blk)
        self.lc.run_blocks(top, self.just_blocks(), True)
        if self.interactive_mode:
            gobject.idle_add(self.lc.doevalstep)
        else:
            while self.lc.doevalstep():
                pass

    def _snap_to_dock(self):
        """ Snap a block (selected_block) to the dock of another block
            (destination_block).
        """
        selected_block = self.drag_group[0]
        best_destination = None
        d = 200
        for selected_block_dockn in range(len(selected_block.docks)):
            for destination_block in self.just_blocks():
                # Don't link to a block to which you're already connected
                if destination_block in self.drag_group:
                    continue
                # Check each dock of destination for a possible connection
                for destination_dockn in range(len(destination_block.docks)):
                    this_xy = dock_dx_dy(destination_block, destination_dockn,
                                          selected_block, selected_block_dockn)
                    if magnitude(this_xy) > d:
                        continue
                    d = magnitude(this_xy)
                    best_xy = this_xy
                    best_destination = destination_block
                    best_destination_dockn = destination_dockn
                    best_selected_block_dockn = selected_block_dockn
        if d < 200:
            if not arithmetic_check(selected_block, best_destination,
                                    best_selected_block_dockn,
                                    best_destination_dockn):
                return
            if not journal_check(selected_block, best_destination,
                                    best_selected_block_dockn,
                                    best_destination_dockn):
                return
            for blk in self.drag_group:
                (sx, sy) = blk.spr.get_xy()
                blk.spr.move((sx + best_xy[0], sy + best_xy[1]))

            # If there was already a block docked there, move it to the trash.
            blk_in_dock = best_destination.connections[best_destination_dockn]
            if blk_in_dock is not None and blk_in_dock != selected_block:
                blk_in_dock.connections[0] = None
                self._put_in_trash(blk_in_dock)

            best_destination.connections[best_destination_dockn] = \
                selected_block
            if selected_block.connections is not None:
                selected_block.connections[best_selected_block_dockn] = \
                    best_destination

            if best_destination.name in BOOLEAN_STYLE:
                if best_destination_dockn == 2 and \
                   selected_block.name in COMPARE_STYLE:
                    dy = selected_block.ey - best_destination.ey
                    best_destination.expand_in_y(dy)
                    self._expand_boolean(best_destination, selected_block, dy)
            elif best_destination.name in EXPANDABLE_BLOCKS and \
                 best_destination_dockn == 1:
                dy = 0
                if (selected_block.name in EXPANDABLE_BLOCKS or
                    selected_block.name in NUMBER_STYLE_VAR_ARG):
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
                    self._expand_expandable(best_destination, selected_block,
                                            dy)
                self._cascade_expandable(best_destination)
                grow_stack_arm(find_sandwich_top(best_destination))

    def _disconnect(self, blk):
        """ Disconnect block from stack above it. """
        if blk.connections[0] is None:
            return
        if collapsed(blk):
            return
        blk2 = blk.connections[0]
        c = blk2.connections.index(blk)
        blk2.connections[c] = None

        if blk2.name in BOOLEAN_STYLE:
            if c == 2 and blk2.ey > 0:
                dy = -blk2.ey
                blk2.expand_in_y(dy)
                self._expand_boolean(blk2, blk, dy)
        elif blk2.name in EXPANDABLE_BLOCKS and c == 1:
            if blk2.ey > 0:
                dy = blk2.reset_y()
                if dy != 0:
                    self._expand_expandable(blk2, blk, dy)
                self._cascade_expandable(blk2)
                grow_stack_arm(find_sandwich_top(blk2))

        blk.connections[0] = None

    def _import_from_journal(self, blk):
        """ Import a file from the Sugar Journal """
        if self.running_sugar:
            chooser(self.parent, '', self._update_media_blk)
        else:
            fname, self.load_save_folder = get_load_name('.*',
                                                         self.load_save_folder)
            if fname is None:
                return
            self._update_media_icon(blk, fname)

    def _load_description_block(self, blk):
        """ Look for a corresponding description block """
        if blk is None or blk.name != 'journal' or len(blk.values) == 0 or \
           blk.connections[0] is None:
            return
        _blk = blk.connections[0]
        dblk = find_blk_below(_blk, 'description')
        # Autoupdate the block if it is empty
        if dblk != None and (len(dblk.values) == 0 or dblk.values[0] is None):
            self._update_media_icon(dblk, None, blk.values[0])

    def _update_media_blk(self, dsobject):
        """ Called from the chooser to load a media block """
        self._update_media_icon(self.selected_blk, dsobject,
                                dsobject.object_id)

    def _update_media_icon(self, blk, name, value=''):
        """ Update the icon on a 'loaded' media block. """
        if blk.name == 'journal':
            self._load_image_thumb(name, blk)
        elif blk.name == 'audio':
            self._block_skin('audioon', blk)
        else:
            self._block_skin('descriptionon', blk)
        if value == '':
            value = name
        if len(blk.values) > 0:
            blk.values[0] = value
        else:
            blk.values.append(value)
        blk.spr.set_label(' ')

    def _load_image_thumb(self, picture, blk):
        """ Replace icon with a preview image. """
        pixbuf = None
        self._block_skin('descriptionon', blk)

        if self.running_sugar:
            w, h = calc_image_size(blk.spr)
            pixbuf = get_pixbuf_from_journal(picture, w, h)
        else:
            if movie_media_type(picture):
                self._block_skin('journalon', blk)
            elif audio_media_type(picture):
                self._block_skin('audioon', blk)
                blk.name = 'audio'
            elif image_media_type(picture):
                w, h = calc_image_size(blk.spr)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(picture, w, h)
            else:
                blk.name = 'description'
        if pixbuf is not None:
            x, y = self._calc_image_offset('', blk.spr)
            blk.set_image(pixbuf, x, y)
            self._resize_skin(blk)

    def _keypress_cb(self, area, event):
        """ Keyboard """
        keyname = gtk.gdk.keyval_name(event.keyval)
        keyunicode = gtk.gdk.keyval_to_unicode(event.keyval)

        if event.get_state() & gtk.gdk.MOD1_MASK:
            alt_mask = True
            alt_flag = 'T'
        else:
            alt_mask = False
            alt_flag = 'F'
        self._key_press(alt_mask, keyname, keyunicode)
        return keyname

    def _key_press(self, alt_mask, keyname, keyunicode):
        if keyname is None:
            return False

        self.keypress = keyname

        if alt_mask:
            if keyname == "p":
                self.hideshow_button()
            elif keyname == 'q':
                exit()

        elif self.selected_blk is not None:
            if self.selected_blk.name == 'number':
                self._process_numeric_input(keyname)
            elif self.selected_blk.name == 'string':
                self.process_alphanumeric_input(keyname, keyunicode)
                if self.selected_blk is not None:
                    self.selected_blk.resize()
            elif self.selected_blk.name != 'proto':
                self._process_keyboard_commands(keyname, block_flag=True)

        elif self.turtles.spr_to_turtle(self.selected_spr) is not None:
            self._process_keyboard_commands(keyname, block_flag=False)

        return True

    def _process_numeric_input(self, keyname):
        ''' Make sure numeric input is valid. '''
        oldnum = self.selected_blk.spr.labels[0].replace(CURSOR, '')
        if len(oldnum) == 0:
            oldnum = '0'
        if keyname == 'minus':
            if oldnum == '0':
                newnum = '-'
            elif oldnum[0] != '-':
                newnum = '-' + oldnum
            else:
                newnum = oldnum
        elif keyname == 'comma' and self.decimal_point == ',' and \
                ',' not in oldnum:
            newnum = oldnum + ','
        elif keyname == 'period' and self.decimal_point == '.' and \
                '.' not in oldnum:
            newnum = oldnum + '.'
        elif keyname == 'BackSpace':
            if len(oldnum) > 0:
                newnum = oldnum[:len(oldnum)-1]
            else:
                newnum = ''
        elif keyname in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if oldnum == '0':
                newnum = keyname
            else:
                newnum = oldnum + keyname
        elif keyname == 'Return':
            self._unselect_block()
            return
        else:
            newnum = oldnum
        if newnum == '.':
            newnum = '0.'
        if newnum == ',':
            newnum = '0,'
        if len(newnum) > 0 and newnum != '-':
            try:
                float(newnum.replace(self.decimal_point, '.'))
            except ValueError, e:
                newnum = oldnum
        self.selected_blk.spr.set_label(newnum + CURSOR)

    def process_alphanumeric_input(self, keyname, keyunicode):
        """ Make sure alphanumeric input is properly parsed. """
        if len(self.selected_blk.spr.labels[0]) > 0:
            c = self.selected_blk.spr.labels[0].count(CURSOR)
            if c == 0:
                oldleft = self.selected_blk.spr.labels[0]
                oldright = ''
            elif len(self.selected_blk.spr.labels[0]) == 1:
                oldleft = ''
                oldright = ''
            else:
                try:  # Why are getting a ValueError on occasion?
                    oldleft, oldright = \
                        self.selected_blk.spr.labels[0].split(CURSOR)
                except ValueError:
                    _logger.debug("[%s]" % self.selected_blk.spr.labels[0])
                    oldleft = self.selected_blk.spr.labels[0]
                    oldright = ''
        else:
            oldleft = ''
            oldright = ''
        newleft = oldleft
        if keyname in ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock', \
                       'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift']:
            keyname = ''
            keyunicode = 0
        # Hack until I sort out input and unicode and dead keys,
        if keyname[0:5] == 'dead_':
            self.dead_key = keyname
            keyname = ''
            keyunicode = 0
        if keyname == 'space':
            keyunicode = 32
        elif keyname == 'Tab':
            keyunicode = 9
        if keyname == 'BackSpace':
            if len(oldleft) > 1:
                newleft = oldleft[:len(oldleft)-1]
            else:
                newleft = ''
        elif keyname == 'Home':
            oldright = oldleft + oldright
            newleft = ''
        elif keyname == 'Left':
            if len(oldleft) > 0:
                oldright = oldleft[len(oldleft) - 1:] + oldright
                newleft = oldleft[:len(oldleft) - 1]
        elif keyname == 'Right':
            if len(oldright) > 0:
                newleft = oldleft + oldright[0]
                oldright = oldright[1:]
        elif keyname == 'End':
            newleft = oldleft + oldright
            oldright = ''
        elif keyname == 'Return':
            newleft = oldleft + RETURN
        elif keyname == 'Down':
            self._unselect_block()
            return
        elif keyname == 'Up' or keyname == 'Escape': # Restore previous state
            self.selected_blk.spr.set_label(self.saved_string)
            self._unselect_block()
            return
        else:
            if self.dead_key is not '':
                keyunicode = \
                    DEAD_DICTS[DEAD_KEYS.index(self.dead_key[5:])][keyname]
                self.dead_key = ''
            if keyunicode > 0:
                if unichr(keyunicode) != '\x00':
                    newleft = oldleft + unichr(keyunicode)
                else:
                    newleft = oldleft
            elif keyunicode == -1: # clipboard text
                if keyname == '\n':
                    newleft = oldleft + RETURN
                else:
                    newleft = oldleft + keyname
        self.selected_blk.spr.set_label("%s%s%s" % (newleft, CURSOR, oldright))

    def _process_keyboard_commands(self, keyname, block_flag=True):
        """ Use the keyboard to move blocks and turtle """
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
            self.run_button(0)
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
                else:
                    self._jog_block(blk, mov_dict[keyname][0],
                                         mov_dict[keyname][1])
            elif not block_flag:
                self._jog_turtle(mov_dict[keyname][0], mov_dict[keyname][1])
        return True

    def _jog_turtle(self, dx, dy):
        """ Jog turtle """
        if dx == -1 and dy == -1:
            self.canvas.xcor = 0
            self.canvas.ycor = 0
        else:
            self.canvas.xcor += dx
            self.canvas.ycor += dy
        self.active_turtle = self.turtles.spr_to_turtle(self.selected_spr)
        self.canvas.move_turtle()
        self.display_coordinates()
        self.selected_turtle = None

    def _jog_block(self, blk, dx, dy):
        """ Jog block """
        if blk.type == 'proto':
            return
        if collapsed(blk):
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

    def _number_check(self):
        """ Make sure a 'number' block contains a number. """
        n = self.selected_blk.spr.labels[0].replace(CURSOR, '')
        if n in ['-', '.', '-.', ',', '-,']:
            n = 0
        elif n is not None:
            try:
                f = float(n.replace(self.decimal_point, '.'))
                if f > 1000000:
                    n = 1
                    self.showlabel("#overflowerror")
                elif f < -1000000:
                    n = -1
                    self.showlabel("#overflowerror")
            except ValueError:
                n = 0
                self.showlabel("#notanumber")
        else:
            n = 0
        self.selected_blk.spr.set_label(n)
        self.selected_blk.values[0] = n.replace(self.decimal_point, '.')

    def _string_check(self):
        s = self.selected_blk.spr.labels[0].replace(CURSOR, '')
        self.selected_blk.spr.set_label(s)
        self.selected_blk.values[0] = s.replace(RETURN, "\12")

    def load_python_code(self):
        """ Load Python code from a file """
        fname, self.load_save_folder = get_load_name('.py',
                                                     self.load_save_folder)
        if fname is None:
            return
        f = open(fname, 'r')
        self.myblock = f.read()
        f.close()

    def _import_py(self):
        """ Import Python code into a block """
        if self.running_sugar:
            self.activity.import_py()
        else:
            self.load_python_code()
            self.set_userdefined()

    def new_project(self):
        """ Start a new project """
        stop_logo(self)
        self._loaded_project = ""
        # Put current project in the trash.
        while len(self.just_blocks()) > 0:
            blk = self.just_blocks()[0]
            top = find_top_block(blk)
            self._put_in_trash(top)
        self.canvas.clearscreen()
        self.save_file_name = None

    def is_new_project(self):
        """ Is this a new project or was a old project loaded from a file? """
        return self._loaded_project == ""

    def project_has_changed(self):
        """ WARNING: order of JSON serialized data may have changed. """
        try:
            f = open(self._loaded_project, 'r')
            saved_project_data = f.read()
            f.close()
        except:
            _logger.debug("problem loading saved project data from %s" % \
                              (self._loaded_project))
            saved_project_data = ""
        current_project_data = data_to_string(self.assemble_data_to_save())

        return saved_project_data != current_project_data

    def load_files(self, ta_file, create_new_project=True):
        """ Load a project from a file """
        if create_new_project:
            self.new_project()
        self._check_collapsibles(self.process_data(data_from_file(ta_file)))
        self._loaded_prokect = ta_file

    def load_file(self, create_new_project=True):
        _file_name, self.load_save_folder = get_load_name('.ta',
                                                     self.load_save_folder)
        if _file_name is None:
            return
        if _file_name[-3:] == '.ta':
            _file_name = _file_name[0: -3]
        self.load_files(_file_name + '.ta', create_new_project)
        if create_new_project:
            self.save_file_name = os.path.basename(_file_name)
        if self.running_sugar:
            self.activity.metadata['title'] = os.path.split(_file_name)[1]

    def _found_a_turtle(self, blk):
        """ Either [-1, 'turtle', ...] or [-1, ['turtle', key], ...] """
        if blk[1] == 'turtle':
            self.load_turtle(blk)
            return True
        elif type(blk[1]) == list and blk[1][0] == 'turtle':
            self.load_turtle(blk, blk[1][1])
            return True
        elif type(blk[1]) == tuple:
            _btype, _key = blk[1]
            if _btype == 'turtle':
                self.load_turtle(blk, _key)
                return True
        return False

    def load_turtle(self, blk, key=1):
        """ Restore a turtle from its saved state """
        tid, name, xcor, ycor, heading, color, shade, pensize = blk
        self.canvas.set_turtle(key)
        self.canvas.setxy(xcor, ycor, pendown=False)
        self.canvas.seth(heading)
        self.canvas.setcolor(color)
        self.canvas.setshade(shade)
        self.canvas.setpensize(pensize)

    def load_block(self, b, offset=0):
        """ Restore individual blocks from saved state """
        # A block is saved as: (i, (btype, value), x, y, (c0,... cn))
        # The x, y position is saved/loaded for backward compatibility
        btype, value = b[1], None
        if type(btype) == tuple:
            btype, value = btype
        elif type(btype) == list:
            btype, value = btype[0], btype[1]
        if btype in CONTENT_BLOCKS or btype in COLLAPSIBLE:
            if btype == 'number':
                try:
                    values = [round_int(value)]
                except ValueError:
                    values = [0]
            elif btype in COLLAPSIBLE:
                if value is not None:
                    values = [int(value)]
                else:
                    values = []
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
                    b[2] + self.canvas.cx + offset,
                    b[3] + self.canvas.cy + offset,
                    'block', values, self.block_scale)

        # Some blocks get transformed.
        if btype == 'string' and blk.spr is not None:
            blk.spr.set_label(blk.values[0].replace('\n', RETURN))
        elif btype == 'start': # block size is saved in start block
            if value is not None:
                self.block_scale = value
        elif btype in EXPANDABLE or btype in EXPANDABLE_BLOCKS or \
             btype in EXPANDABLE_ARGS or btype == 'nop':
            if btype == 'vspace' or btype in EXPANDABLE_BLOCKS:
                if value is not None:
                    blk.expand_in_y(value)
            elif btype == 'hspace' or btype == 'identity2':
                if value is not None:
                    blk.expand_in_x(value)
            elif btype == 'templatelist' or btype == 'list':
                for i in range(len(b[4])-4):
                    blk.add_arg()
            elif btype == 'myfunc2arg' or btype == 'myfunc3arg' or\
                 btype == 'userdefined2args' or btype == 'userdefined3args':
                blk.add_arg()
            if btype == 'myfunc3arg' or btype == 'userdefined3args':
                blk.add_arg(False)
            if btype in PYTHON_SKIN:
                if self.nop == 'pythonloaded':
                    self._block_skin('pythonon', blk)
                else:
                    self._block_skin('pythonoff', blk)
        elif btype in BOX_STYLE_MEDIA and blk.spr is not None:
            if len(blk.values) == 0 or blk.values[0] == 'None' or \
               blk.values[0] is None:
                self._block_skin(btype + 'off', blk)
            elif btype == 'audio' or btype == 'description':
                self._block_skin(btype + 'on', blk)
            elif self.running_sugar:
                try:
                    dsobject = datastore.get(blk.values[0])
                    if not movie_media_type(dsobject.file_path[-4:]):
                        w, h, = calc_image_size(blk.spr)
                        pixbuf = get_pixbuf_from_journal(dsobject, w, h)
                        if pixbuf is not None:
                            x, y = self._calc_image_offset('', blk.spr)
                            blk.set_image(pixbuf, x, y)
                        else:
                            self._block_skin('journalon', blk)
                    dsobject.destroy()
                except:
                    try:
                        w, h, = calc_image_size(blk.spr)
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                     blk.values[0], w, h)
                        x, y = self._calc_image_offset('', blk.spr)
                        blk.set_image(pixbuf, x, y)
                    except:
                        _logger.debug("Couldn't open dsobject (%s)" % \
                              (blk.values[0]))
                        self._block_skin('journaloff', blk)
            else:
                if not movie_media_type(blk.values[0][-4:]):
                    try:
                        w, h, = calc_image_size(blk.spr)
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                     blk.values[0], w, h)
                        x, y = self._calc_image_offset('', blk.spr)
                        blk.set_image(pixbuf, x, y)
                    except:
                        self._block_skin('journaloff', blk)
                else:
                    self._block_skin('journalon', blk)
            blk.spr.set_label(' ')
            blk.resize()

        if self.interactive_mode:
            blk.spr.set_layer(BLOCK_LAYER)
        if check_dock:
            blk.connections = 'check'
        return blk

    def load_start(self, ta_file=None):
        """ Start a new project with a 'start' brick """
        if ta_file is None:
            self.process_data([[0, "start", PALETTE_WIDTH + 20,
                                self.toolbar_offset + PALETTE_HEIGHT + 20,
                                [None, None]]])
        else:
            self.process_data(data_from_file(ta_file))

    def save_file(self, _file_name=None):
        """ Start a project to a file """
        if self.save_folder is not None:
            self.load_save_folder = self.save_folder
        if _file_name is None:
            _file_name, self.load_save_folder = get_save_name('.ta',
                self.load_save_folder, self.save_file_name)
        if _file_name is None:
            return
        if _file_name[-3:] == '.ta':
            _file_name = _file_name[0: -3]
        data_to_file(self.assemble_data_to_save(), _file_name + '.ta')
        self.save_file_name = os.path.basename(_file_name)
        if not self.running_sugar:
            self.save_folder = self.load_save_folder

    def assemble_data_to_save(self, save_turtle=True, save_project=True):
        """ Pack the project (or stack) into a data stream to be serialized """
        _data = []
        _blks = []

        if save_project:
            _blks = self.just_blocks()
        else:
            if self.selected_blk is None:
                return []
            _blks = find_group(find_top_block(self.selected_blk))

        for _i, _blk in enumerate(_blks):
            _blk.id = _i
        for _blk in _blks:
            if _blk.name in CONTENT_BLOCKS or _blk.name in COLLAPSIBLE:
                if len(_blk.values) > 0:
                    _name = (_blk.name, _blk.values[0])
                else:
                    _name = (_blk.name)
            elif _blk.name in EXPANDABLE or _blk.name in EXPANDABLE_BLOCKS or \
                 _blk.name in EXPANDABLE_ARGS:
                _ex, _ey = _blk.get_expand_x_y()
                if _ex > 0:
                    _name = (_blk.name, _ex)
                elif _ey > 0:
                    _name = (_blk.name, _ey)
                else:
                    _name = (_blk.name, 0)
            elif _blk.name == 'start': # save block_size in start block
                _name = (_blk.name, self.block_scale)
            else:
                _name = (_blk.name)
            if hasattr(_blk, 'connections'):
                connections = [get_id(_cblk) for _cblk in _blk.connections]
            else:
                connections = None
            (_sx, _sy) = _blk.spr.get_xy()
            # Add a slight offset for copy/paste
            if not save_project:
                _sx += 20
                _sy += 20
            _data.append((_blk.id, _name, _sx - self.canvas.cx,
                          _sy - self.canvas.cy, connections))
        if save_turtle:
            for _turtle in iter(self.turtles.dict):
                self.canvas.set_turtle(_turtle)
                _data.append((-1, ['turtle', _turtle],
                             self.canvas.xcor, self.canvas.ycor,
                             self.canvas.heading, self.canvas.color,
                             self.canvas.shade, self.canvas.pensize))
        return _data

    def display_coordinates(self):
        """ Display the coordinates of the current turtle on the toolbar """
        x = round_int(self.canvas.xcor / self.coord_scale)
        y = round_int(self.canvas.ycor / self.coord_scale)
        h = round_int(self.canvas.heading)
        if self.running_sugar:
            self.activity.coordinates_label.set_text("%s: %d %s: %d %s: %d" % \
                (_("xcor"), x, _("ycor"), y, _("heading"), h))
            self.activity.coordinates_label.show()
        elif self.interactive_mode:
            self.win.set_title("%s — %s: %d %s: %d %s: %d" % \
                (_("Turtle Art"), _("xcor"), x, _("ycor"), y, _("heading"), h))

    def showlabel(self, shp, label=''):
        """ Display a message on a status block """
        if not self.interactive_mode:
            _logger.debug(label)
            return
        if shp == 'syntaxerror' and str(label) != '':
            if str(label)[1:] in self.status_shapes:
                shp = str(label)[1:]
                label = ''
            else:
                shp = 'status'
        elif shp[0] == '#':
            shp = shp[1:]
            label = ''
        self.status_spr.set_shape(self.status_shapes[shp])
        self.status_spr.set_label(str(label))
        self.status_spr.set_layer(STATUS_LAYER)
        if shp == 'info':
            self.status_spr.move((PALETTE_WIDTH, self.height - 400))
        else:
            self.status_spr.move((PALETTE_WIDTH, self.height - 200))

    def calc_position(self, template):
        """ Relative placement of portfolio objects (depreciated) """
        w, h, x, y, dx, dy = TEMPLATES[template]
        x *= self.canvas.width
        y *= self.canvas.height
        w *= (self.canvas.width - x)
        h *= (self.canvas.height - y)
        dx *= w
        dy *= h
        return(w, h, x, y, dx, dy)

    def save_for_upload(self, _file_name):
        """ Grab the current canvas and save it for upload """
        if _file_name[-3:] == '.ta':
            _file_name = _file_name[0: -3]
        data_to_file(self.assemble_data_to_save(), _file_name + '.ta')
        save_picture(self.canvas, _file_name + '.png')
        ta_file = _file_name + '.ta'
        image_file = _file_name + '.png'
        return ta_file, image_file

    def save_as_image(self, name="", svg=False, pixbuf=None):
        """ Grab the current canvas and save it. """

        if not self.interactive_mode:
            save_picture(self.canvas, name[:-3] + ".png")
            return
            """
            self.color_map = self.window.get_colormap()
            new_pix = pixbuf.get_from_drawable(self.window, self.color_map,
                                               0, 0, 0, 0,
                                               self.width, self.height)
            new_pix.save(name[:-3] + ".png", "png")
            """

        if self.running_sugar:
            if svg:
                if len(name) == 0:
                    filename = "ta.svg"
                else:
                    filename = name + ".svg"
            else:
                if len(name) == 0:
                    filename = "ta.png"
                else:
                    filename = name + ".png"
            datapath = get_path(self.activity, 'instance')
        elif len(name) == 0:
            name = "ta"
            if self.save_folder is not None:
                self.load_save_folder = self.save_folder
            if svg:
                filename, self.load_save_folder = get_save_name('.svg',
                                                     self.load_save_folder,
                                                     name)
            else:
                filename, self.load_save_folder = get_save_name('.png',
                                                     self.load_save_folder,
                                                     name)
            datapath = self.load_save_folder
        else:
            datapath = os.getcwd()
            if svg:
                filename = name + ".svg"
            else:
                filename = name + ".png"
        if filename is None:
            return

        file_path = os.path.join(datapath, filename)
        if svg:
            if self.svg_string == '':
                return
            save_svg(self.svg_string, file_path)
            self.svg_string = ''
        else:
            save_picture(self.canvas, file_path)

        # keep a log of the saved pictures for export to HTML
        self.saved_pictures.append(file_path)

        if self.running_sugar:
            dsobject = datastore.create()
            if len(name) == 0:
                dsobject.metadata['title'] = "%s %s" % \
                    (self.activity.metadata['title'], _("image"))
            else:
                dsobject.metadata['title'] = name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            if svg:
                dsobject.metadata['mime_type'] = 'image/svg+xml'
            else:
                dsobject.metadata['mime_type'] = 'image/png'
            dsobject.set_file_path(file_path)
            datastore.write(dsobject)
            dsobject.destroy()

    def just_blocks(self):
        """ Filter out 'proto', 'trash', and 'deleted' blocks """
        just_blocks_list = []
        for _blk in self.block_list.list:
            if _blk.type == 'block':
                just_blocks_list.append(_blk)
        return just_blocks_list

    def _width_and_height(self, blk):
        """ What are the width and height of a stack? """
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

    def _calc_image_offset(self, name, spr, iw=0, ih=0):
        """ Calculate the postion for placing an image onto a sprite. """
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
        """ Calculate new image size """
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

    def _proto_skin(self, name, n, i):
        """ Utility for calculating proto skin images """
        x, y = self._calc_image_offset(name, self.palettes[n][i].spr)
        self.palettes[n][i].spr.set_image(self.media_shapes[name], 1, x, y)

    def _block_skin(self, name, blk):
        """ Some blocks get a skin """
        x, y = self._calc_image_offset(name, blk.spr)
        blk.set_image(self.media_shapes[name], x, y)
        self._resize_skin(blk)

    def _resize_skin(self, blk):
        """ Resize the 'skin' when block scale changes. """
        if blk.name in PYTHON_SKIN:
            w, h = self._calc_w_h('pythonoff', blk.spr)
            x, y = self._calc_image_offset('pythonoff', blk.spr, w, h)
        elif blk.name == 'journal':
            if len(blk.values) == 1 and blk.values[0] is not None:
                w, h = self._calc_w_h('', blk.spr)
                x, y = self._calc_image_offset('journaloff', blk.spr, w, h)
            else:
                w, h = self._calc_w_h('journaloff', blk.spr)
                x, y = self._calc_image_offset('journaloff', blk.spr, w, h)
        else:
            w, h = self._calc_w_h('descriptionoff', blk.spr)
            x, y = self._calc_image_offset('descriptionoff', blk.spr, w, h)
        blk.scale_image(x, y, w, h)
