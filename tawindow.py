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


# TODO:
# - better comments! 
# - many methods could have their logic simplified! 
# - verbose flag should be in the scope of the object instance


import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject
import os
import os.path
import time
from math import atan2, pi
DEGTOR = 2*pi/360
from gettext import gettext as _

try:
    from sugar.graphics.objectchooser import ObjectChooser
    from sugar.datastore import datastore
    from sugar import profile
except ImportError:
    pass

from taconstants import *
from talogo import LogoCode, stop_logo
from tacanvas import TurtleGraphics
from tablock import Blocks, Block
from taturtle import Turtles, Turtle
from tautils import magnitude, get_load_name, get_save_name, data_from_file,\
                    data_to_file, round_int, get_id, get_pixbuf_from_journal,\
                    movie_media_type, audio_media_type, image_media_type,\
                    save_picture
from tasprite_factory import SVG, svg_str_to_pixbuf, svg_from_file
from sprites import Sprites, Sprite

"""
TurtleArt Window class abstraction 
"""
class TurtleArtWindow():

    # Time out for triggering help
    timeout_tag = [0]

    def __init__(self, win, path, lang, parent=None, mycolors=None):
        self._setup_initial_values(win, path, lang, parent, mycolors)
        self._setup_misc()
        self._show_toolbar_palette(0, False)

    def _setup_initial_values(self, win, path, lang, parent, mycolors):
        self.window = win
        self.path = os.path.join(path, 'images')
        self.load_save_folder = os.path.join(path, 'samples')
        self.save_folder = None
        self.save_file_name = None
        self.window.set_flags(gtk.CAN_FOCUS)
        self.width = gtk.gdk.screen_width()
        self.height = gtk.gdk.screen_height() 
        if parent is not None:
            parent.show_all()
            self.running_sugar = True
        else:
            self.window.show_all()
            self.running_sugar = False
        self._setup_events()
        self.keypress = ""
        self.keyvalue = 0
        self.dead_key = ""
        self.area = self.window.window
        self.gc = self.area.new_gc()
        if self._OLPC_XO_1():
            self.lead = 1.0
            self.scale = 0.67
        else:
            self.lead = 1.0
            self.scale = 1.0
        self.block_scale = BLOCK_SCALE
        self.trash_scale = 0.5
        self.cm = self.gc.get_colormap()
        self.rgb = [255,0,0]
        self.bgcolor = self.cm.alloc_color('#fff8de')
        self.msgcolor = self.cm.alloc_color('black')
        self.fgcolor = self.cm.alloc_color('red')
        self.textcolor = self.cm.alloc_color('blue')
        self.textsize = 32
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
        self.status_spr = None
        self.status_shapes = {}
        self.toolbar_spr = None
        self.palette_sprs = []
        self.palettes = []
        self.palette_button = []
        self.orientation = 0
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
        self.block_list = Blocks(self.scale)
        self.sprite_list = Sprites(self.window, self.area, self.gc)
        self.turtles = Turtles(self.sprite_list)
        if mycolors == None:
            Turtle(self.turtles, 1)
        else:
            Turtle(self.turtles, 1, mycolors.split(','))
        self.active_turtle = self.turtles.get_turtle(1)
        self.selected_turtle = None
        self.canvas = TurtleGraphics(self, self.width, self.height)
        self.titlex = -(self.canvas.width*TITLEXY[0])/(self.coord_scale*2)
        self.leftx = -(self.canvas.width*TITLEXY[0])/(self.coord_scale*2)
        self.rightx = 0
        self.titley = (self.canvas.height*TITLEXY[1])/(self.coord_scale*2)
        self.topy = (self.canvas.height*(TITLEXY[1]-0.125))/(self.coord_scale*2)
        self.bottomy = 0
        self.lc = LogoCode(self)

    """
    Register the events we listen to.
    """
    def _setup_events(self):
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.connect("expose-event", self._expose_cb)
        self.window.connect("button-press-event", self._buttonpress_cb)
        self.window.connect("button-release-event", self._buttonrelease_cb)
        self.window.connect("motion-notify-event", self._move_cb)
        self.window.connect("key_press_event", self._keypress_cb)

    """
    Misc. sprites for status, overlays, etc.
    """
    def _setup_misc(self):
        # media blocks get positioned into other blocks
        for name in MEDIA_SHAPES:
            if name[0:7] == 'journal' and not self.running_sugar:
                filename = 'file'+name[7:]
            else:
                filename = name
            self.media_shapes[name] = \
                svg_str_to_pixbuf(svg_from_file("%s/%s.svg" % (
                                                self.path, filename)))

        for i, name in enumerate(STATUS_SHAPES):
            self.status_shapes[name] = svg_str_to_pixbuf(svg_from_file(
                                               "%s/%s.svg" % (self.path, name)))
        self.status_spr = Sprite(self.sprite_list, 0, self.height-200,
                                         self.status_shapes['status'])
        self.status_spr.hide()
        self.status_spr.type = 'status'

        for name in OVERLAY_SHAPES:
            self.overlay_shapes[name] = Sprite(self.sprite_list,
                int(self.width/2-600), int(self.height/2-450),
                svg_str_to_pixbuf(svg_from_file(
                                              "%s/%s.svg" % (self.path, name))))
            self.overlay_shapes[name].hide()
            self.overlay_shapes[name].type = 'overlay'

    """
    Is a chattube available for sharing?
    """
    def _sharing(self):
        if self.running_sugar and hasattr(self.activity, 'chattube') and\
            self.activity.chattube is not None:
                return True
        return False

    """
    Is the an OLPC XO-1?
    """
    def _OLPC_XO_1(self):
        return os.path.exists('/etc/olpc-release') or \
               os.path.exists('/sys/power/olpc-pm')

    """
    Repaint
    """
    def _expose_cb(self, win, event):
        self.sprite_list.redraw_sprites()
        return True


    """
    Eraser_button (Always hide status block when clearing the screen.)
    """
    def eraser_button(self):
        if self.status_spr is not None:
            self.status_spr.hide()
        self.lc.prim_clear()
        self.display_coordinates()

    """
    Run turtle!
    """
    def run_button(self, time):
        if self.running_sugar:
            self.activity.recenter()
        # Look for a 'start' block
        for blk in self.just_blocks():
            if self._find_start_stack(blk):
                self.step_time = time
                print "running stack starting from %s" % (blk.name)
                self._run_stack(blk)
                return
        # If there is no 'start' block, run stacks that aren't 'def action'
        for blk in self.just_blocks():
            if self._find_block_to_run(blk):
                self.step_time = time
                print "running stack starting from %s" % (blk.name)
                self._run_stack(blk)
        return

    """
    Stop button
    """
    def stop_button(self):
        stop_logo(self)

    """
    Change the icon for user-defined blocks after Python code is loaded.
    """
    def set_userdefined(self):
        for blk in self.just_blocks():
            if blk.name == 'nop':
                x, y = self._calc_image_offset('pythonon', blk.spr)
                blk.spr.set_image(self.media_shapes['pythonon'], 1, x, y)
        self.nop = 'pythonloaded'

    """
    Enter fulscreen mode
    """
    def set_fullscreen(self):
        if self.running_sugar:
            self.activity.fullscreen()
            self.activity.recenter()

    """
    Hide/show button
    """
    def hideshow_button(self):
        if self.hide is False: 
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
        self.canvas.canvas.inval()

    """
    Hide or show palette 
    """
    def hideshow_palette(self, state):
        if state is False:
            self.palette == False
            if self.running_sugar:
                self.activity.do_hidepalette()
            self.hide_palette()
        else:
            self.palette == True
            if self.running_sugar:
                self.activity.do_showpalette()
            self.show_palette()

    """
    Show palette 
    """
    def show_palette(self, n=0):
        self._show_toolbar_palette(n)
        self.palette_button[self.orientation].set_layer(TAB_LAYER)
        self.toolbar_spr.set_layer(CATEGORY_LAYER)
        self.palette = True

    """
    Hide the palette.
    """
    def hide_palette(self):
        self._hide_toolbar_palette()
        self.palette_button[self.orientation].hide()
        self.toolbar_spr.hide()
        self.palette = False

    """
    Callback from 'hide blocks' block
    """
    def hideblocks(self):
        self.hide = False
        self.hideshow_button()
        if self.running_sugar:
            self.activity.do_hide()

    """
    Callback from 'show blocks' block
    """
    def showblocks(self):
        self.hide = True
        self.hideshow_button()
        if self.running_sugar:
            self.activity.do_show()

    """
    Resize all of the blocks
    """
    def resize_blocks(self):
        # We need to restore collapsed stacks before resizing.
        for b in self.just_blocks():
            if b.status == 'collapsed':
                bot = self._find_sandwich_bottom(b)
                if self._collapsed(bot):
                    dy = bot.values[0]
                    self._restore_stack(self._find_sandwich_top(b))
                    bot.values[0] = dy
        for b in self.just_blocks():
            b.rescale(self.block_scale)
        for b in self.just_blocks():
            self._adjust_dock_positions(b)
        # We need to re-collapsed stacks after resizing.
        for b in self.just_blocks():
            if self._collapsed(b):
                self._collapse_stack(self._find_sandwich_top(b))
        for b in self.just_blocks():
            if b.name == 'sandwichtop':
                self._grow_stack_arm(b)

    """
    Show the toolbar palettes, creating them on init_only
    """
    def _show_toolbar_palette(self, n, init_only=False):
        # Create the selectors the first time through.
        if self.selectors == []:
            svg = SVG()
            x, y = 50, 0
            for i, name in enumerate(PALETTE_NAMES):
                a = svg_str_to_pixbuf(svg_from_file("%s/%soff.svg" % (
                                                    self.path, name)))
                b = svg_str_to_pixbuf(svg_from_file("%s/%son.svg" % (
                                                    self.path, name)))
                self.selector_shapes.append([a,b])
                self.selectors.append(Sprite(self.sprite_list, x, y, a))
                self.selectors[i].type = 'selector'
                self.selectors[i].name = name
                self.selectors[i].set_layer(TAB_LAYER)
                w, h = self.selectors[i].get_dimensions()
                x += int(w) 
                self.palette_sprs.append([None,None])

            # Create the palette orientation button
            self.palette_button.append(Sprite(self.sprite_list, 0, 0,
                                      svg_str_to_pixbuf(svg_from_file(
                                     "%s/palettehorizontal.svg" %(self.path)))))
            self.palette_button.append(Sprite(self.sprite_list, 0, 0,
                                      svg_str_to_pixbuf(svg_from_file(
                                     "%s/palettevertical.svg" % (self.path)))))
            self.palette_button[0].name = 'orientation'
            self.palette_button[1].name = 'orientation'
            self.palette_button[0].type = 'palette'
            self.palette_button[1].type = 'palette'
            self.palette_button[self.orientation].set_layer(TAB_LAYER)
            self.palette_button[1-self.orientation].hide()
            # Create the toolbar background
            self.toolbar_spr = Sprite(self.sprite_list, 0, 0,
                svg_str_to_pixbuf(svg.toolbar(self.width, ICON_SIZE)))
            self.toolbar_spr.type = 'toolbar'
            self.toolbar_spr.set_layer(CATEGORY_LAYER)

            # Create the empty palettes
            if len(self.palettes) == 0:
                for i in range(len(PALETTES)):
                    self.palettes.append([]);

        if init_only is True:
            return

        # Hide the previously displayed palette
        self._hide_previous_palette()

        self.selected_palette = n
        self.previous_palette = self.selected_palette        
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
                                              self.sprite_list, name,
                                              0, 0, 'proto', [], PALETTE_SCALE))
                self.palettes[n][i].spr.set_layer(TAB_LAYER)
                self.palettes[n][i].unhighlight()
                # Some blocks get a skin.
                if name in BOX_STYLE_MEDIA:
                    x, y = self._calc_image_offset(name+'small',
                                                   self.palettes[n][i].spr)
                    self.palettes[n][i].spr.set_image(self.media_shapes[
                                                      name+'small'], 1, x, y)
                elif name[:8] == 'template':
                    x, y = self._calc_image_offset(name[8:],
                                                   self.palettes[n][i].spr)
                    self.palettes[n][i].spr.set_image(self.media_shapes[
                                                      name[8:]], 1, x, y)
                elif name[:7] == 'picture':
                    x, y = self._calc_image_offset(name[7:],
                                                   self.palettes[n][i].spr)
                    self.palettes[n][i].spr.set_image(self.media_shapes[
                                                      name[7:]], 1, x, y)
                elif name == 'nop':
                    x, y = self._calc_image_offset('pythonsmall',
                                                   self.palettes[n][i].spr)
                    self.palettes[n][i].spr.set_image(self.media_shapes[
                                                      'pythonsmall'], 1, x, y)

        self._layout_palette(n)
        for blk in self.palettes[n]:
            blk.spr.set_layer(TAB_LAYER)
        if n == PALETTE_NAMES.index('trash'):
            for blk in self.trash_stack:
                for b in self._find_group(blk):
                    if b.status != 'collapsed':
                        b.spr.set_layer(TAB_LAYER)

    """
    Hide the toolbar palettes
    """
    def _hide_toolbar_palette(self):
        self._hide_previous_palette()
        # Hide the selectors
        for i in range(len(PALETTES)):
            self.selectors[i].hide()
        self.selected_palette = None
        self.previous_palette = None

    """
    Hide just the previously viewed toolbar palette
    """
    def _hide_previous_palette(self):
        # Hide previous palette
        if self.previous_palette is not None:
            for i in range(len(PALETTES[self.previous_palette])):        
                self.palettes[self.previous_palette][i].spr.hide()
            self.palette_sprs[self.previous_palette][
                              self.orientation].hide()
            self.selectors[self.previous_palette].set_shape(
                self.selector_shapes[self.previous_palette][0])
            if self.previous_palette == PALETTE_NAMES.index('trash'):
                for b in self.trash_stack:
                    for bb in self._find_group(b):
                        bb.spr.hide()

    """
    Position prototypes in a horizontal palette.
    """
    def _horizontal_layout(self, x, y, blocks):
        _max_w = 0
        for b in blocks:
            _w, _h = self._width_and_height(b)
            if y+_h > PALETTE_HEIGHT+ICON_SIZE:
                x += int(_max_w+5)
                y = ICON_SIZE+5
                _max_w = 0
            (_bx, _by) = b.spr.get_xy()
            _dx = x-_bx
            _dy = y-_by
            for g in self._find_group(b):
                g.spr.move_relative((int(_dx), int(_dy)))
            y += int(_h+5)
            if _w > _max_w:
                _max_w = _w
        return x, y, _max_w

    """
    Position prototypes in a vertical palette.
    """
    def _vertical_layout(self, x, y, blocks):
        _row = []
        _row_w = 0
        _max_h = 0
        for _b in blocks:
            _w, _h = self._width_and_height(_b)
            if x+_w > PALETTE_WIDTH:
                # Recenter row.
                _dx = int((PALETTE_WIDTH-_row_w)/2)
                for _r in _row:
                    for _g in self._find_group(_r):
                       _g.spr.move_relative((_dx, 0))
                _row = []
                _row_w = 0
                x = 5
                y += int(_max_h+5)
                _max_h = 0
            _row.append(_b)
            _row_w += (5+_w)
            (_bx, _by) = _b.spr.get_xy()
            _dx = int(x-_bx)
            _dy = int(y-_by)
            for _g in self._find_group(_b):
                _g.spr.move_relative((_dx, _dy))
            x += int(_w+5)
            if _h > _max_h:
                _max_h = _h
        # Recenter last row.
        _dx = int((PALETTE_WIDTH-_row_w)/2)
        for _r in _row:
            for _g in self._find_group(_r):
                _g.spr.move_relative((_dx, 0))
        return x, y, _max_h

    """
    Layout prototypes in a palette.
    """
    def _layout_palette(self, n):
        if n is not None:
            _x, _y = 5, ICON_SIZE+5
            if self.orientation == 0:
                _x, _y, _max = self._horizontal_layout(_x, _y, self.palettes[n])
                if n == PALETTE_NAMES.index('trash'):
                    _x, _y, _max = self._horizontal_layout(_x+_max, _y,
                                                           self.trash_stack)
                _w = _x+_max+25
                if self.palette_sprs[n][self.orientation] is None:
                    svg = SVG()
                    self.palette_sprs[n][self.orientation] = Sprite(
                            self.sprite_list, 0, ICON_SIZE,
                            svg_str_to_pixbuf(svg.palette(_w, PALETTE_HEIGHT)))
                    self.palette_sprs[n][self.orientation].type = 'category'
                if n == PALETTE_NAMES.index('trash'):
                    svg = SVG()
                    self.palette_sprs[n][self.orientation].set_shape(
                        svg_str_to_pixbuf(svg.palette(_w, PALETTE_HEIGHT)))
            else:
                _x, _y, _max = self._vertical_layout(_x, _y, self.palettes[n])
                if n == PALETTE_NAMES.index('trash'):
                    _x, _y, _max = self._vertical_layout(_x, _y+_max,
                                                         self.trash_stack)
                _h = _y+_max+25-ICON_SIZE
                if self.palette_sprs[n][self.orientation] is None:
                    svg = SVG()
                    self.palette_sprs[n][self.orientation] =\
                        Sprite(self.sprite_list, 0, ICON_SIZE,
                            svg_str_to_pixbuf(svg.palette(PALETTE_WIDTH, _h)))
                    self.palette_sprs[n][self.orientation].type = 'category'
                if n == PALETTE_NAMES.index('trash'):
                    svg = SVG()
                    self.palette_sprs[n][self.orientation].set_shape(
                        svg_str_to_pixbuf(svg.palette(PALETTE_WIDTH, _h)))
            self.palette_sprs[n][self.orientation].set_layer(CATEGORY_LAYER)

    """
    Button press
    """
    def _buttonpress_cb(self, win, event):
        self.window.grab_focus()
        x, y = self._xy(event)
        self.button_press(event.get_state()&gtk.gdk.CONTROL_MASK, x, y)
        if self._sharing():
            if event.get_state()&gtk.gdk.CONTROL_MASK is True:
                self.activity._send_event("p:%d:%d:T" % (x, y))
            else:
                self.activity._send_event("p:%d:%d:F" % (x, y))
        return True

    def button_press(self, mask, x, y, verbose=False):
        if verbose:
            print "processing remote button press: %d, %d" % (x, y)
        self.block_operation = 'click'

        # Unselect things that may have been selected earlier
        if self.selected_blk is not None:
            self._unselect_block()
        self.selected_turtle = None
        # Always hide the status layer on a click
        if self.status_spr is not None:
            self.status_spr.hide()

        # Find out what was clicked
        spr = self.sprite_list.find_sprite((x,y))
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
                self._block_pressed(mask, x, y, blk)
            elif blk.type == 'trash':
                self._restore_from_trash(self.find_top_block(blk))
            elif blk.type == 'proto':
                if blk.name == 'restoreall':
                    self._restore_all_from_trash()
                elif blk.name == 'restore':
                    self._restore_latest_from_trash()
                elif blk.name == 'empty':
                    self._empty_trash()
                elif MACROS.has_key(blk.name):
                    self._new_macro(blk.name, x+100, y+100)
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
                if self._hide_button_hit(spr, x, y):
                    self.hideshow_palette(False)
            elif spr.type == 'palette':
               self.orientation = 1-self.orientation
               self.palette_button[self.orientation].set_layer(TAB_LAYER)
               self.palette_button[1-self.orientation].hide()
               self.palette_sprs[self.selected_palette][
                               1-self.orientation].hide()
               self._layout_palette(self.selected_palette)
               self.show_palette(self.selected_palette)
            return True

    """
    Select a category from the toolbar.
    """
    def _select_category(self, spr):
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

    """
    Restore all the blocks in the trash can
    """
    def _restore_all_from_trash(self):
        for b in self.block_list.list:
            if b.type == 'trash':
                self._restore_from_trash(b)

    """
    Restore latest blocks from the trash can
    """
    def _restore_latest_from_trash(self):
        if len(self.trash_stack) == 0:
            return
        self._restore_from_trash(self.trash_stack[len(self.trash_stack)-1])

    def _restore_from_trash(self, blk):
        group = self._find_group(blk)
        for b in group:
            b.rescale(self.block_scale)
            b.spr.set_layer(BLOCK_LAYER)
            x,y = b.spr.get_xy()
            b.spr.move((x+PALETTE_WIDTH,y+PALETTE_HEIGHT))
            b.type = 'block'
        for b in group:
            self._adjust_dock_positions(b)
        for b in group:
            if self._collapsed(b):
                # If the stack had been collapsed before going into the trash,
                # collapse it again now.
                self._collapse_stack(self._find_sandwich_top(b))
        self.trash_stack.remove(blk)

    """
    Permanently remove blocks in the trash can
    """
    def _empty_trash(self):
        for b in self.block_list.list:
            if b.type == 'trash':
                b.type = 'deleted'
                b.spr.hide()
        self.trash_stack = []

    """
    Is x,y over the trash can?
    """
    def _in_the_trash(self, x, y):
        if self.selected_palette == self.trash_index and \
           self.palette_sprs[self.trash_index][self.orientation].hit((x,y)):
            return True
        return False

    """
    Block pressed
    """
    def _block_pressed(self, mask, x, y, blk):
        if blk is not None:
            blk.highlight()
            self._disconnect(blk)
            self.drag_group = self._find_group(blk)
            (sx, sy) = blk.spr.get_xy()
            self.drag_pos = x-sx, y-sy
            for blk in self.drag_group:
                if blk.status != 'collapsed':
                    blk.spr.set_layer(TOP_LAYER)
            self.saved_string = blk.spr.labels[0]

    """
    Unselect block
    """
    def _unselect_block(self):
        # After unselecting a 'number' block, we need to check its value
        if self.selected_blk.name == 'number':
            self._number_check()
        elif self.selected_blk.name == 'string':
            self._string_check()
        self.selected_blk.unhighlight()
        self.selected_blk = None

    """
    Make a new block.
    """
    def _new_block(self, name, x, y):
        if name in CONTENT_BLOCKS:
            newblk = Block(self.block_list, self.sprite_list, name, x-20, y-20,
                           'block', DEFAULTS[name], self.block_scale)
        else:
            newblk = Block(self.block_list, self.sprite_list, name, x-20, y-20,
                           'block', [], self.block_scale)
        # Add special skin to some blocks
        if name == 'nop':
            if self.nop == 'pythonloaded':
                x, y = self._calc_image_offset('pythonon',newblk.spr)
                newblk.spr.set_image(self.media_shapes['pythonon'], 1, x, y)
            else:
                x, y = self._calc_image_offset('pythonoff',newblk.spr)
                newblk.spr.set_image(self.media_shapes['pythonoff'], 1, x, y)
        elif name in BOX_STYLE_MEDIA:
            x, y = self._calc_image_offset(name+'off',newblk.spr)
            newblk.spr.set_image(self.media_shapes[name+'off'], 1, x, y)
            newblk.spr.set_label(' ')
        newspr = newblk.spr
        newspr.set_layer(TOP_LAYER)
        self.drag_pos = 20, 20
        newblk.connections = [None]*len(newblk.docks)
        if DEFAULTS.has_key(newblk.name):
            for i, argvalue in enumerate(DEFAULTS[newblk.name]):
                # skip the first dock position since it is always a connector
                dock = newblk.docks[i+1]
                argname = dock[0]
                if argname == 'unavailable':
                    continue
                if argname == 'media':
                    argname = 'journal'
                elif argname == 'number' and\
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
                    nx, ny = sx+dock[2]-argdock[2], sy+dock[3]-argdock[3]
                    if argname == 'journal':
                        x, y = self._calc_image_offset('journaloff',argblk.spr)
                        argblk.spr.set_image(self.media_shapes['journaloff'],
                                             1, x, y)
                        argblk.spr.set_label(' ')
                    argblk.spr.move((nx, ny))
                    argblk.spr.set_layer(TOP_LAYER)
                    argblk.connections = [newblk, None]
                    newblk.connections[i+1] = argblk
        self.drag_group = self._find_group(newblk)
        self.block_operation = 'new' 

    """
    Create a "macro" (predefined stack of blocks)
    """
    def _new_macro(self, name, x, y):
        macro = MACROS[name]
        macro[0][2] = x
        macro[0][3] = y
        top = self.process_data(macro)
        self.block_operation = 'new' 
        self._check_collapsibles(top)
        self.drag_group = self._find_group(top)

    """
    Process data (from a macro, a file, or the clipboard) into blocks.
    """
    def process_data(self, data):
        # Create the blocks (or turtle).
        blocks = []
        for b in data:
            if self._found_a_turtle(b) is False:
                blk = self.load_block(b)
                blocks.append(blk)
        # Make the connections.
        for i in range(len(blocks)):
            cons=[]
            # Normally, it is simply a matter of copying the connections.
            if blocks[i].connections == None:
                for c in data[i][4]:
                    if c is None:
                        cons.append(None)
                    else:
                        cons.append(blocks[c])
            elif blocks[i].connections == 'check':
                # Corner case to convert old-style boolean and arithmetic blocks
                cons.append(None) # Add an extra connection.
                for c in data[i][4]:
                    if c is None:
                        cons.append(None)
                    else:
                        cons.append(blocks[c])
                # If the boolean op was connected, readjust the plumbing.
                if blocks[i].name in BOOLEAN_STYLE:
                    if data[i][4][0] is not None:
                        c = data[i][4][0]
                        cons[0] = blocks[data[c][4][0]]
                        c0 = data[c][4][0]
                        for j, cj in enumerate(data[c0][4]):
                            if cj == c:
                                blocks[c0].connections[j] = blocks[i]
                        if c<i:
                            blocks[c].connections[0] = blocks[i]
                            blocks[c].connections[3] = None
                        else:
                            # Connection was to a block we haven't seen yet.
                            print "WARNING: dock check couldn't see the future"
                else:
                    if data[i][4][0] is not None:
                        c = data[i][4][0]
                        cons[0] = blocks[data[c][4][0]]
                        c0 = data[c][4][0]
                        for j, cj in enumerate(data[c0][4]):
                            if cj == c:
                                blocks[c0].connections[j] = blocks[i]
                        if c<i:
                            blocks[c].connections[0] = blocks[i]
                            blocks[c].connections[1] = None
                        else:
                            # Connection was to a block we haven't seen yet.
                            print "WARNING: dock check couldn't see the future"
            else:
                print "WARNING: unknown connection state %s" %\
                      (str(blocks[i].connections))
            blocks[i].connections = cons[:]
        # Block sizes and shapes may have changed.
        for b in blocks:
            self._adjust_dock_positions(b)
        # Look for any stacks that need to be collapsed.
        for b in blocks:
            if self._collapsed(b):
                self._collapse_stack(self._find_sandwich_top(b))
        return blocks[0]

    """
    Adjust the dock x,y positions
    """
    def _adjust_dock_positions(self, blk):
        (sx, sy) = blk.spr.get_xy()
        for i, c in enumerate(blk.connections):
            if i>0 and c is not None:
                bdock = blk.docks[i]
                for j in range(len(c.docks)):
                    if c.connections[j] == blk:
                        cdock = c.docks[j]
                        nx, ny = sx+bdock[2]-cdock[2], sy+bdock[3]-cdock[3]
                        c.spr.move((nx, ny))
                self._adjust_dock_positions(c)

    """
    Turtle pressed
    """
    def _turtle_pressed(self, x, y):
        (tx, ty) = self.selected_turtle.get_xy()
        dx, dy = x-tx-30, y-ty-30
        if dx*dx+dy*dy > 200:
            self.drag_turtle = ('turn',
                                self.canvas.heading-atan2(dy,dx)/DEGTOR, 0)
        else:
            self.drag_turtle = ('move', x-tx, y-ty)

    """
    Mouse move
    """
    def _move_cb(self, win, event):
        x, y = self._xy(event)
        self._mouse_move(x, y)
        return True

    def _mouse_move(self, x, y, verbose=False, mdx=0, mdy=0):
        if verbose:
            print "processing remote mouse move: %d, %d" % (x, y)

        self.block_operation = 'move'
        # First, check to see if we are dragging or rotating a turtle.
        if self.selected_turtle is not None:
            dtype, dragx, dragy = self.drag_turtle
            (sx, sy) = self.selected_turtle.get_xy()
            if dtype == 'move':
                if mdx != 0 or mdy != 0:
                    dx, dy = mdx, mdy
                else:
                    dx, dy = x-dragx-sx, y-dragy-sy
                self.selected_turtle.move((sx+dx, sy+dy))
            else:
                if mdx != 0 or mdy != 0:
                    dx, dy = mdx, mdy
                else:
                    dx, dy = x-sx-30, y-sy-30
                self.canvas.seth(int(dragx+atan2(dy,dx)/DEGTOR+5)/10*10)
        # If we are hoving, show popup help.
        elif self.drag_group is None:
            self._show_popup(x, y)
            return
        # If we have a stack of blocks selected, move them.
        elif self.drag_group[0] is not None:
            blk = self.drag_group[0]
            # Don't move a bottom blk is the stack is collapsed
            if self._collapsed(blk):
                return

            self.selected_spr = blk.spr
            dragx, dragy = self.drag_pos
            if mdx != 0 or mdy != 0:
                dx, dy = mdx, mdy
            else:
                (sx,sy) = blk.spr.get_xy()
                dx, dy = x-dragx-sx, y-dragy-sy
            # Take no action if there was a move of 0,0.
            if dx == 0 and dy == 0:
                return
            self.drag_group = self._find_group(blk)
            # Check to see if any block ends up with a negative x.
            for b in self.drag_group:
                (bx, by) = b.spr.get_xy()
                if bx+dx < 0:
                    dx += -(bx+dx)
            # Move the stack.
            for b in self.drag_group:
                (bx, by) = b.spr.get_xy()
                b.spr.move((bx+dx, by+dy))
        if mdx != 0 or mdy != 0:
            dx, dy = 0, 0
        else:
            self.dx += dx
            self.dy += dy

    """
    Let's help our users by displaying a little help.
    """
    def _show_popup(self, x, y):
        spr = self.sprite_list.find_sprite((x,y))
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
        elif spr and hasattr(spr,'type') and (spr.type == 'selector' or\
                                              spr.type == 'palette'):
            if self.timeout_tag[0] == 0:
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

    """
    Fetch the help text and display it. 
    """
    def _do_show_popup(self, block_name):
        if SPECIAL_NAMES.has_key(block_name):
            block_name_s = SPECIAL_NAMES[block_name]
        elif BLOCK_NAMES.has_key(block_name):
            block_name_s = BLOCK_NAMES[block_name][0]
        else:
            block_name_s = _(block_name)
        if HELP_STRINGS.has_key(block_name):
            label = block_name_s + ": " + HELP_STRINGS[block_name]
        else:
            label = block_name_s
        if self.running_sugar:
            self.activity.hover_help_label.set_text(label)
            self.activity.hover_help_label.show()
        else:
            self.win.set_title(_("Turtle Art") + " — " + label)
        return 0

    """
    Button release
    """
    def _buttonrelease_cb(self, win, event):
        x, y = self._xy(event)
        self.button_release(x, y)
        if self._sharing():
            self.activity._send_event("r:"+str(x)+":"+str(y))
        return True

    def button_release(self, x, y, verbose=False):
        if self.dx != 0 or self.dy != 0:
            if self._sharing():
                if verbose:
                    print "processing move: %d %d" % (self.dx, self.dy)
                self.activity._send_event("m:%d:%d" % (self.dx, self.dy))
                self.dx = 0
                self.dy = 0
        if verbose:
            print "processing remote button release: %d, %d" % (x, y)

        # We may have been moving the turtle
        if self.selected_turtle is not None:
            (tx, ty) = self.selected_turtle.get_xy()
            (cx, cy) = self.canvas.canvas.get_xy()
            self.canvas.xcor = tx-self.canvas.canvas._width/2+30-cx
            self.canvas.ycor = self.canvas.canvas._height/2-ty-30+cy
            self.canvas.move_turtle()
            if self.running_sugar:
                self.display_coordinates()
            self.selected_turtle = None
            return

        # If we don't have a group of blocks, then there is nothing to do.
        if self.drag_group == None: 
            return

        blk = self.drag_group[0]
        # Remove blocks by dragging them onto the trash palette.
        if self.block_operation=='move' and self._in_the_trash(x, y):
            self.trash_stack.append(blk)
            for b in self.drag_group:
                if b.status == 'collapsed':
                    # Collapsed stacks are restored for rescaling
                    # and then recollapsed after they are moved to the trash.
                    bot = self._find_sandwich_bottom(b)
                    if self._collapsed(bot):
                        dy = bot.values[0]
                        self._restore_stack(self._find_sandwich_top(b))
                        bot.values[0] = dy
                b.type = 'trash'
                b.rescale(self.trash_scale)
            blk.spr.move((x,y))
            for b in self.drag_group:
                self._adjust_dock_positions(b)
            # Re-collapsing any stacks we had restored for scaling
            for b in self.drag_group:
                if self._collapsed(b):
                    self._collapse_stack(self._find_sandwich_top(b))

            self.drag_group = None
            self.show_palette(PALETTE_NAMES.index('trash'))
            return

        # Pull a stack of new blocks off of the category palette.
        if self.block_operation=='new':
            for b in self.drag_group:
                (bx, by) = b.spr.get_xy()
                b.spr.move((bx+100, by+100))

        # Look to see if we can dock the current stack.
        self._snap_to_dock()
        self._check_collapsibles(blk)
        for b in self.drag_group:
            if b.status != 'collapsed':
                b.spr.set_layer(BLOCK_LAYER)
        self.drag_group = None

        # Find the block we clicked on and process it.
        if self.block_operation=='click':
            self._click_block(x, y)

    """
    Click block
    """
    def _click_block(self, x, y):
        blk = self.block_list.spr_to_block(self.selected_spr)
        if blk is None:
            return
        self.selected_blk = blk
        if  blk.name=='number' or blk.name=='string':
            self.saved_string = blk.spr.labels[0]
            blk.spr.labels[0] += CURSOR
        elif blk.name in BOX_STYLE_MEDIA:
            self._import_from_journal(self.selected_blk)
        elif blk.name=='identity2' or blk.name=='hspace':
            group = self._find_group(blk)
            if self._hide_button_hit(blk.spr, x, y):
                dx = blk.reset_x()
            elif self._show_button_hit(blk.spr, x, y):
                dx = 20
                blk.expand_in_x(dx)
            for b in group:
                if b != blk:
                    b.spr.move_relative((dx*blk.scale, 0))
        elif blk.name=='vspace':
            group = self._find_group(blk)
            if self._hide_button_hit(blk.spr, x, y):
                dy = blk.reset_y()
            elif self._show_button_hit(blk.spr, x, y):
                dy = 20
                blk.expand_in_y(dy)
            else:
                dy = 0
            for b in group:
                if b != blk:
                    b.spr.move_relative((0, dy*blk.scale))
            self._grow_stack_arm(self._find_sandwich_top(blk))
        elif blk.name in EXPANDABLE:
            if self._show_button_hit(blk.spr, x, y):
                n = len(blk.connections)
                group = self._find_group(blk.connections[n-1])
                if blk.name == 'myfunc' and n == 4:
                    blk.spr.labels[1] = 'f(x,y)'
                    blk.spr.labels[2] = ' '
                if blk.name == 'myfunc' and n == 5:
                    blk.spr.labels[1] = 'f(x,y,z)'
                    dy = blk.add_arg(False)
                else:
                    dy = blk.add_arg()
                for b in group:
                    b.spr.move_relative((0, dy))
                blk.connections.append(blk.connections[n-1])
                argname = blk.docks[n-1][0]
                argvalue = DEFAULTS[blk.name][len(DEFAULTS[blk.name])-1]
                argblk = Block(self.block_list, self.sprite_list, argname,
                               0, 0, 'block', [argvalue], self.block_scale)
                argdock = argblk.docks[0]
                (bx, by) = blk.spr.get_xy()
                nx = bx+blk.docks[n-1][2]-argdock[2]
                ny = by+blk.docks[n-1][3]-argdock[3]
                argblk.spr.move((nx, ny))
                argblk.spr.set_layer(TOP_LAYER)
                argblk.connections = [blk, None]
                blk.connections[n-1] = argblk
                self._grow_stack_arm(self._find_sandwich_top(blk))
            else:
                self._run_stack(blk)
        elif blk.name in COLLAPSIBLE:
            top = self._find_sandwich_top(blk)
            if self._collapsed(blk):
                self._restore_stack(top)
            elif top is not None:
                self._collapse_stack(top)
        elif blk.name=='nop' and self.myblock==None:
            self._import_py()
        else:
            self._run_stack(blk)

    """
    Find the sandwich top above this block.
    """
    def _find_sandwich_top(self, blk):
        b = blk.connections[0]
        while b is not None:
            if b.name in COLLAPSIBLE:
                return None
            if b.name in ['repeat', 'if', 'ifelse']:
                if blk != b.connections[len(b.connections)-1]:
                    return None
            if b.name == 'sandwichtop':
                return b
            blk = b
            b = b.connections[0]
        return None

    """
    Find the sandwich bottom below this block.
    """
    def _find_sandwich_bottom(self, blk):
        b = blk.connections[len(blk.connections)-1]
        while b is not None:
            if b.name == 'sandwichtop':
                return None
            if b.name in COLLAPSIBLE:
                return b
            b = b.connections[len(b.connections)-1]
        return None

    """
    Hide all the blocks between the sandwich top and sandwich bottom.
    """
    def _collapse_stack(self, top):
        hit_bottom = False
        group = self._find_group(top.connections[len(top.connections)-1])
        if group[0].name in COLLAPSIBLE:
            return
        for b in group:
            if not hit_bottom and b.name in COLLAPSIBLE:
                hit_bottom = True

                # Replace 'sandwichbottom' shape with 'sandwichcollapsed' shape
                if len(b.values) == 0:
                    b.values.append(1)
                else:
                    b.values[0] = 1
                olddx = b.docks[1][2]
                olddy = b.docks[1][3]
                b.name = 'sandwichcollapsed'
                b.svg.set_show(True)
                b.svg.set_hide(False)
                b._dx = 0
                b._ey = 0
                b.spr.set_label(_('click to open'))
                b.resize()

                # Redock to sandwich top in group
                you = self._find_sandwich_top(b)
                (yx, yy) = you.spr.get_xy()
                yd = you.docks[len(you.docks)-1]
                (bx, by) = b.spr.get_xy()
                dx = yx+yd[2]-b.docks[0][2]-bx
                dy = yy+yd[3]-b.docks[0][3]-by
                b.spr.move_relative((dx, dy))

                # Since the shapes have changed, the dock positions have too.
                newdx = b.docks[1][2]
                newdy = b.docks[1][3]
                dx += newdx-olddx
                dy += newdy-olddy
            else:
                if not hit_bottom:
                    b.spr.set_layer(HIDE_LAYER)
                    b.status = 'collapsed'
                else:
                    b.spr.move_relative((dx, dy))
        self._reset_stack_arm(top)

    """
    Restore all the blocks between the sandwich top and sandwich bottom.
    """
    def _restore_stack(self, top):
        group = self._find_group(top.connections[len(top.connections)-1])
        hit_bottom = False
        for b in group:
            if not hit_bottom and b.name in COLLAPSIBLE:
                hit_bottom = True

                b.values[0] = 0
                olddx = b.docks[1][2]
                olddy = b.docks[1][3]
                # Replace 'sandwichcollapsed' shape with 'sandwichbottom' shape
                b.name = 'sandwichbottom'
                b.spr.set_label(' ')
                b.svg.set_show(False)
                b.svg.set_hide(True)
                b.refresh()

                # Redock to previous block in group
                you = b.connections[0]
                (yx, yy) = you.spr.get_xy()
                yd = you.docks[len(you.docks)-1]
                (bx, by) = b.spr.get_xy()
                dx = yx+yd[2]-b.docks[0][2]-bx
                dy = yy+yd[3]-b.docks[0][3]-by
                b.spr.move_relative((dx, dy))

                # Since the shapes have changed, the dock positions have too.
                newdx = b.docks[1][2]
                newdy = b.docks[1][3]
                dx += newdx-olddx
                dy += newdy-olddy
            else:
                if not hit_bottom:
                    b.spr.set_layer(BLOCK_LAYER)
                    b.status = None
                else:
                    b.spr.move_relative((dx, dy))
        self._grow_stack_arm(top)

    """
    When we undock, retract the 'arm' that extends down from 'sandwichtop'.
    """
    def _reset_stack_arm(self, top):
        if top is not None and top.name == 'sandwichtop':
            if top.ey > 0:
                top.reset_y()

    """
    When we dock, grow an 'arm' the length of the stack from 'sandwichtop'.
    """
    def _grow_stack_arm(self, top):
        if top is not None and top.name == 'sandwichtop':
            bot = self._find_sandwich_bottom(top)
            if bot is None:
                return
            if top.ey > 0:
                top.reset_y()
            (tx, ty) = top.spr.get_xy()
            (tw, th) = top.spr.get_dimensions()
            (bx, by) = bot.spr.get_xy()
            dy = by-(ty+th)
            if dy > 0:
                top.expand_in_y(dy/top.scale)

    """
    Check the state of collapsible blocks upon change in dock state.
    """
    def _check_collapsibles(self, blk):
        group = self._find_group(blk)
        for b in group:
            if b.name in COLLAPSIBLE:
                if self._collapsed(b):
                    b.svg.set_show(True)
                    b.svg.set_hide(False)
                    self._reset_stack_arm(self._find_sandwich_top(b))
                elif self._collapsible(b):
                    b.svg.set_hide(True)
                    b.svg.set_show(False)
                    self._grow_stack_arm(self._find_sandwich_top(b))
                else:
                    b.svg.set_hide(False)
                    b.svg.set_show(False)
                    # Ouch: When you tear off the sandwich bottom, you
                    # no longer have access to the group with the sandwich top
                    # so check them all.
                    for bb in self.just_blocks():
                        if bb.name == 'sandwichtop':
                            if self._find_sandwich_bottom(bb) is None:
                                self._reset_stack_arm(bb)
                b.refresh()

    """
    Is this stack collapsed?
    """
    def _collapsed(self, blk):
        if blk is not None and blk.name in COLLAPSIBLE and\
           len(blk.values) == 1 and blk.values[0] != 0:
            return True
        return False

    """
    Can this stack be collapsed?
    """
    def _collapsible(self, blk):
        if blk is None or blk.name not in COLLAPSIBLE:
            return False
        if self._find_sandwich_top(blk) is None:
            return False
        return True

    """
    Run a stack of blocks.
    """
    def _run_stack(self, blk):
        if blk is None:
            return
        self.lc.ag = None
        top = self.find_top_block(blk)
        self.lc.run_blocks(top, self.just_blocks(), True)
        gobject.idle_add(self.lc.doevalstep)

    """
    Did the sprite's hide (contract) button get hit?
    """
    def _hide_button_hit(self, spr, x, y):
        r,g,b,a = spr.get_pixel((x, y))
        if (r == 255 and g == 0) or g == 255:
            return True
        else:
            return False

    """
    Did the sprite's show (expand) button get hit?
    """
    def _show_button_hit(self, spr, x, y):
        r,g,b,a = spr.get_pixel((x, y))
        if g == 254:
            return True
        else:
            return False

    """
    Snap a block to the dock of another block.
    """
    def _snap_to_dock(self):
        my_block = self.drag_group[0]
        d = 200
        for my_dockn in range(len(my_block.docks)):
            for i, your_block in enumerate(self.just_blocks()):
                # don't link to a block to which you're already connected
                if your_block in self.drag_group:
                    continue
                # check each dock of your_block for a possible connection
                for your_dockn in range(len(your_block.docks)):
                    this_xy = self._dock_dx_dy(your_block, your_dockn,
                                              my_block, my_dockn)
                    if magnitude(this_xy) > d:
                        continue
                    d = magnitude(this_xy)
                    best_xy = this_xy
                    best_you = your_block
                    best_your_dockn = your_dockn
                    best_my_dockn = my_dockn
        if d<200:
            if self._arithmetic_check(my_block, best_you, best_my_dockn,
                                      best_your_dockn) is False:
                return
            for blk in self.drag_group:
                (sx, sy) = blk.spr.get_xy()
                blk.spr.move((sx+best_xy[0], sy+best_xy[1]))
            blk_in_dock = best_you.connections[best_your_dockn]
            if blk_in_dock is not None:
                for blk in self._find_group(blk_in_dock):
                    blk.spr.hide()
            best_you.connections[best_your_dockn] = my_block
            if my_block.connections is not None:
                my_block.connections[best_my_dockn] = best_you

    """
    Additional docking check for arithmetic blocks
    """
    def _arithmetic_check(self, b1, b2, d1, d2):
        if b1 == None or b2 == None:
            return True
        if b1.name in ['sqrt', 'number'] and b2.name in ['sqrt', 'number']:
            if b1.name == 'number' and float(b1.values[0]) < 0:
                return False
            elif b2.name == 'number' and float(b2.values[0]) < 0:
                return False
        elif b1.name in ['division2', 'number'] and\
             b2.name in ['division2', 'number']:
            if b1.name == 'number' and float(b1.values[0]) == 0 and d2 == 2:
                return False
            elif b2.name == 'number' and float(b2.values[0]) == 0 and d1 == 2:
                return False
        elif b1.name in ['product2', 'minus2', 'sqrt', 'division2', 'random',
                         'remainder2', 'string'] and\
             b2.name in ['product2', 'minus2', 'sqrt', 'division2', 'random',
                         'remainder2', 'string']:
            if b1.name == 'string' and len(b1.values[0]) != 1:
                try:
                    float(b1.values[0])
                except ValueError:
                    return False
            elif b2.name == 'string' and len(b2.values[0]) != 1:
                try:
                    float(b2.values[0])
                except ValueError:
                    return False
        return True

    """
    Import a file from the Sugar Journal
    """
    def _import_from_journal(self, blk):
        if self.running_sugar:
            chooser = ObjectChooser('Choose image', None,
                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
            try:
                result = chooser.run()
                if result == gtk.RESPONSE_ACCEPT:
                    dsobject = chooser.get_selected_object()
                    self._update_media_icon(blk, dsobject, dsobject.object_id)
                    dsobject.destroy()
            finally:
                chooser.destroy()
                del chooser
        else:
            fname, self.load_save_folder = \
                             get_load_name('.*', self.load_save_folder)
            if fname is None:
                return
            self._update_media_icon(blk, fname)

    """
    Update the icon on a 'loaded' media block.
    """
    def _update_media_icon(self, blk, name, value=''):
        if blk.name == 'journal':
            self._load_image_thumb(name, blk)
        elif blk.name == 'audio':
            x, y = self._calc_image_offset('audioon', blk.spr)
            blk.spr.set_image(self.media_shapes['audioon'], 1, x, y)
        else:
            x, y = self._calc_image_offset('descriptionon', blk.spr)
            blk.spr.set_image(self.media_shapes['descriptionon'], 1, x, y)
        if value == '':
            value = name
        if len(blk.values)>0:
            blk.values[0] = value
        else:
            blk.values.append(value)
        blk.spr.set_label(' ')

    """
    Replace icon with a preview image.
    """
    def _load_image_thumb(self, picture, blk):
        pixbuf = None
        x, y = self._calc_image_offset('descriptionon', blk.spr)
        blk.spr.set_image(self.media_shapes['descriptionon'], 1, x, y)
        if self.running_sugar:
            w, h = self._calc_image_size(blk.spr)
            pixbuf = get_pixbuf_from_journal(picture, w, h)
        else:
            if movie_media_type(picture):
                x, y = self._calc_image_offset('journalon', blk.spr)
                blk.spr.set_image(self.media_shapes['journalon'], 1, x, y)
            elif audio_media_type(picture):
                x, y = self._calc_image_offset('audioon', blk.spr)
                blk.spr.set_image(self.media_shapes['audioon'], 1, x, y)
                blk.name = 'audio'
            elif image_media_type(picture):
                w, h = self._calc_image_size(blk.spr)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(picture, w, h)
            else:
                blk.name = 'description'
        if pixbuf is not None:
            x, y = self._calc_image_offset('', blk.spr)
            blk.spr.set_image(pixbuf, 1, x, y)

    """
    Disconnect block from stack above it.
    """
    def _disconnect(self, blk):
        if blk.connections[0]==None:
            return
        if self._collapsed(blk):
            return
        blk2=blk.connections[0]
        blk2.connections[blk2.connections.index(blk)] = None
        blk.connections[0] = None

    """
    Find the distance between the dock points of two blocks.
    """
    def _dock_dx_dy(self, block1, dock1n, block2, dock2n):
        dock1 = block1.docks[dock1n]
        dock2 = block2.docks[dock2n]
        d1type, d1dir, d1x, d1y = dock1[0:4]
        d2type, d2dir, d2x, d2y = dock2[0:4]
        if block1 == block2:
            return (100,100)
        if d1dir == d2dir:
            return (100,100)
        if (d2type is not 'number') or (dock2n is not 0):
            if block1.connections is not None and \
                dock1n < len(block1.connections) and \
                block1.connections[dock1n] is not None:
                    return (100,100)
            if block2.connections is not None and \
                dock2n < len(block2.connections) and \
                block2.connections[dock2n] is not None:
                    return (100,100)
        if d1type != d2type:
            if block1.name in STRING_OR_NUMBER_ARGS:
                if d2type == 'number' or d2type == 'string':
                    pass
            elif block1.name in CONTENT_ARGS:
                if d2type in CONTENT_BLOCKS:
                    pass
            else:
                return (100,100)
        (b1x, b1y) = block1.spr.get_xy()
        (b2x, b2y) = block2.spr.get_xy()
        return ((b1x+d1x)-(b2x+d2x), (b1y+d1y)-(b2y+d2y))


    """
    Keyboard
    """
    def _keypress_cb(self, area, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        keyunicode = gtk.gdk.keyval_to_unicode(event.keyval)

        if event.get_state()&gtk.gdk.MOD1_MASK:
            alt_mask = True
            alt_flag = 'T'
        else:
            alt_mask = False
            alt_flag = 'F'
        results = self._key_press(alt_mask, keyname, keyunicode)
        if keyname is not None and self._sharing():
            self.activity._send_event("k:%s:%s:%s" % (alt_flag, keyname,
                                                      str(keyunicode)))
        return keyname

    def _key_press(self, alt_mask, keyname, keyunicode, verbose=False):
        if keyname is None:
            return False
        if verbose:
            print "processing remote key press: %s" % (keyname)

        self.keypress = keyname

        # First, process Alt keys.
        if alt_mask is True and self.selected_blk==None:
            if keyname=="i" and self._sharing():
                self.activity.waiting_for_blocks = True
                self.activity._send_event("i") # request sync for sharing
            elif keyname=="p":
                self.hideshow_button()
            elif keyname=='q':
                exit()
            return True
        # Process keyboard input for 'number' blocks
        if self.selected_blk is not None and\
           self.selected_blk.name == 'number':
            self._process_numeric_input(keyname)
            return True
        # Process keyboard input for 'string' blocks
        elif self.selected_blk is not None and\
             self.selected_blk.name == 'string':
            self.process_alphanumeric_input(keyname, keyunicode)
            if self.selected_blk is not None:
                self.selected_blk.resize()
            return True
        # Otherwise, use keyboard input to move blocks or turtles
        else:
            self._process_keyboard_commands(keyname)
        if self.selected_blk is None:
            return False

    '''
    Make sure numeric input is valid.
    '''
    def _process_numeric_input(self, keyname):
        oldnum = self.selected_blk.spr.labels[0].replace(CURSOR,'')
        if len(oldnum) == 0:
            oldnum = '0'
        if keyname == 'minus':
            if oldnum == '0':
                newnum = '-'
            elif oldnum[0] != '-':
                newnum = '-' + oldnum
            else:
                newnum = oldnum
        elif keyname == 'period' and '.' not in oldnum:
            newnum = oldnum + '.'
        elif keyname == 'BackSpace':
            if len(oldnum) > 0:
                newnum = oldnum[:len(oldnum)-1]
            else:
                newnum = ''
        elif keyname in ['0','1','2','3','4','5','6','7','8','9']:
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
        if len(newnum) > 0 and newnum != '-':
            try:
                float(newnum)
            except ValueError,e:
                newnum = oldnum
        self.selected_blk.spr.set_label(newnum + CURSOR)

    """
    Make sure alphanumeric input is properly parsed.
    """
    def process_alphanumeric_input(self, keyname, keyunicode):
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
                    oldleft, oldright =\
                        self.selected_blk.spr.labels[0].split(CURSOR)
                except ValueError:
                    print "[%s]" % self.selected_blk.spr.labels[0]
                    oldleft = self.selected_blk.spr.labels[0]
                    oldright = ''
        else:
            oldleft = ''
            oldright = ''
        newleft = oldleft
        if keyname in ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock',\
                       'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift']:
            keyname = ''
            keyunicode = 0
        # Hack until I sort out input and unicode and dead keys,
        if keyname[0:5] == 'dead_':
            self.dead_key = keyname
            keyname = ''
            keyunicode = 0
        if keyname in WHITE_SPACE:
            keyunicode = 32
        if keyname == 'BackSpace':
            if len(oldleft) > 1:
                newleft = oldleft[:len(oldleft)-1]
            else:
                newleft = ''
        elif keyname == 'Home':
            oldright = oldleft+oldright
            newleft = ''
        elif keyname == 'Left':
            if len(oldleft) > 0:
                oldright = oldleft[len(oldleft)-1:]+oldright
                newleft = oldleft[:len(oldleft)-1]
        elif keyname == 'Right':
            if len(oldright) > 0:
                newleft = oldleft + oldright[0]
                oldright = oldright[1:]
        elif keyname == 'End':
            newleft = oldleft+oldright
            oldright = ''
        elif keyname == 'Return' or keyname == 'Down':
            self._unselect_block()
            return
        elif keyname == 'Up' or keyname == 'Escape': # Restore previous state
            self.selected_blk.spr.set_label(self.saved_string)
            self._unselect_block()
            return
        else:
            if self.dead_key is not '':
                keyunicode =\
                    DEAD_DICTS[DEAD_KEYS.index(self.dead_key[5:])][keyname]
                self.dead_key = ''
            if keyunicode > 0:
                if unichr(keyunicode) is not '\x00':
                    newleft = oldleft+unichr(keyunicode)
                else:
                    newleft = oldleft
            elif keyunicode == -1: # clipboard text
                newleft = oldleft+keyname
        self.selected_blk.spr.set_label("%s%s%s" % \
                                        (newleft, CURSOR, oldright))

    """
    Use the keyboard to move blocks and turtle
    """
    def _process_keyboard_commands(self, keyname):
        mov_dict = {'KP_Up':[0,10],'j':[0,10],'Up':[0,10],
                    'KP_Down':[0,-10],'k':[0,-10],'Down':[0,-10],
                    'KP_Left':[-10,0],'h':[-10,0],'Left':[-10,0],
                    'KP_Right':[10,0],'l':[10,0],'Right':[10,0],
                    'KP_Page_Down':[0,0], 'KP_Page_Up':[0,0], 'KP_End':[0,0],
                    'KP_Home':[-1,-1],'Return':[-1,-1], 'Esc':[0,0]}
        if not mov_dict.has_key(keyname):
            return
        if keyname == 'KP_End':
            self.run_button(0)
        elif self.selected_spr is not None:
            blk = self.block_list.spr_to_block(self.selected_spr)
            tur = self.turtles.spr_to_turtle(self.selected_spr)
            if blk is not None:
                if keyname == 'Return' or keyname == 'KP_Page_Up':
                    (x, y) = blk.spr.get_xy()
                    self._click_block(x, y)
                elif keyname == 'KP_Page_Down':
                    if self.drag_group == None:
                        self.drag_group = self._find_group(blk)
                    for b in self.drag_group: b.spr.hide()
                    self.drag_group = None
                else:
                    self._jog_block(blk, mov_dict[keyname][0],
                                         mov_dict[keyname][1])
            elif tur is not None:
                self._jog_turtle(mov_dict[keyname][0], mov_dict[keyname][1])
        return True

    """
    Jog turtle
    """
    def _jog_turtle(self, dx, dy):
        if dx == -1 and dy == -1:
            self.canvas.xcor = 0
            self.canvas.ycor = 0
        else:
            self.canvas.xcor += dx
            self.canvas.ycor += dy
        self.canvas.move_turtle()
        self.display_coordinates()
        self.selected_turtle = None

    """
    Jog block
    """
    def _jog_block(self, blk, dx, dy):
        if self._collapsed(blk):
            return
        self.drag_group = self._find_group(blk)
        # check to see if any block ends up with a negative x
        for blk in self.drag_group:
            (sx, sy) = blk.spr.get_xy()
            if sx+dx < 0:
                dx += -(sx+dx)
        # move the stack
        for blk in self.drag_group:
            (sx, sy) = blk.spr.get_xy()
            blk.spr.move((sx+dx, sy-dy))
        self._snap_to_dock()
        self.drag_group = None

    """
    Make sure a 'number' block contains a number.
    """
    def _number_check(self):
        n = self.selected_blk.spr.labels[0].replace(CURSOR,'')
        if n in ['-', '.', '-.']:
            n = 0
        if n is not None:
            try:
                f = float(n)
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
        self.selected_blk.values[0] = n

    def _string_check(self):
        s = self.selected_blk.spr.labels[0].replace(CURSOR,'')
        self.selected_blk.spr.set_label(s)
        self.selected_blk.values[0] = s

    """
    Load Python code from a file
    """
    def load_python_code(self):
        fname, self.load_save_folder = get_load_name('.py',
                                                     self.load_save_folder)
        if fname==None:
            return
        f = open(fname, 'r')
        self.myblock = f.read()
        f.close()
    
    """
    Import Python code into a block
    """
    def _import_py(self):
        if self.running_sugar:
            self.activity.import_py()
        else:
            self.load_python_code()
            self.set_userdefined()

    """
    Start a new project
    """
    def new_project(self):
        stop_logo(self)
        # Put current project in the trash.
        while len(self.just_blocks()) > 0:
            b = self.just_blocks()[0]
            top = self.find_top_block(b)
            self.trash_stack.append(top)
            for b in self._find_group(top):
                b.type = 'trash'
                b.spr.hide()
        self.canvas.clearscreen()
        self.save_file_name = None
    
    """
    Load a project from a file
    """
    def load_files(self, ta_file, create_new_project=True):
        if create_new_project is True:
            self.new_project()
        top = self.process_data(data_from_file(ta_file))
        self._check_collapsibles(top)
    
    def load_file(self, create_new_project=True):
        fname, self.load_save_folder = get_load_name('.ta',
                                                     self.load_save_folder)
        if fname==None:
            return
        if fname[-3:] == '.ta':
            fname=fname[0:-3]
        self.load_files(fname+'.ta', create_new_project)
        if create_new_project is True:
            self.save_file_name = os.path.basename(fname)

    """
    Turtles are either [-1, 'turtle', ...] or [-1, ['turtle', key], ...]
    """
    def _found_a_turtle(self, b):
        if b[1] == 'turtle':
            self.load_turtle(b)
            return True
        elif type(b[1]) == list and b[1][0] == 'turtle': 
            self.load_turtle(b, b[1][1])
            return True
        elif type(b[1]) == tuple:
            btype, key = b[1]
            if btype == 'turtle':
                self.load_turtle(b, key)
                return True
        return False

    """
    Restore a turtle from its saved state
    """
    def load_turtle(self, b, key=1):
        id, name, xcor, ycor, heading, color, shade, pensize = b
        self.canvas.set_turtle(key)
        self.canvas.setxy(xcor, ycor)
        self.canvas.seth(heading)
        self.canvas.setcolor(color)
        self.canvas.setshade(shade)
        self.canvas.setpensize(pensize)

    """
    Restore individual blocks from saved state
    """
    def load_block(self, b):
        # A block is saved as: (i, (btype, value), x, y, (c0,... cn))
        # The x,y position is saved/loaded for backward compatibility
        btype, value = b[1], None
        if type(btype) == tuple: 
            btype, value = btype
        elif type(btype) == list:
            btype, value = btype[0], btype[1]
        if btype in CONTENT_BLOCKS or btype in COLLAPSIBLE:
            if btype == 'number':
                try:
                    values = [int(value)]
                except ValueError:
                    values = [float(value)]
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
        if OLD_NAMES.has_key(btype):
            btype = OLD_NAMES[btype]
        blk = Block(self.block_list, self.sprite_list, 
                    btype, b[2]+self.canvas.cx, b[3]+self.canvas.cy, 'block',
                    values, self.block_scale)
        # Some blocks get transformed.
        if btype == 'nop': 
            if self.nop == 'pythonloaded':
                x, y = self._calc_image_offset('pythonon', blk.spr)
                blk.spr.set_image(self.media_shapes['pythonon'], 1, x, y)
            else:
                x, y = self._calc_image_offset('pythonoff', blk.spr)
                blk.spr.set_image(self.media_shapes['pythonoff'], 1, x, y)
            blk.spr.set_label(' ')
        elif btype in EXPANDABLE:
            if btype == 'vspace':
                if value is not None:
                    blk.expand_in_y(value)
            elif btype == 'hspace' or btype == 'identity2':
                if value is not None:
                    blk.expand_in_x(value)
            elif btype == 'templatelist' or btype == 'list':
                for i in range(len(b[4])-4):
                    dy = blk.add_arg()
        elif btype in BOX_STYLE_MEDIA and len(blk.values)>0:
            if blk.values[0] == 'None' or blk.values[0] == None:
                x, y = self._calc_image_offset(btype+'off', blk.spr)
                blk.spr.set_image(self.media_shapes[btype+'off'], 1, x, y)
            elif btype == 'audio' or btype == 'description':
                x, y = self._calc_image_offset(btype+'on', blk.spr)
                blk.spr.set_image(self.media_shapes[btype+'on'], 1, x, y)
            elif self.running_sugar:
                try:
                    dsobject = datastore.get(blk.values[0])
                    if not movie_media_type(dsobject.file_path[-4:]):
                        w, h, = self._calc_image_size(blk.spr)
                        pixbuf = get_pixbuf_from_journal(dsobject, w, h)
                        if pixbuf is not None:
                            x, y = self._calc_image_offset('', blk.spr)
                            blk.spr.set_image(pixbuf, 1, x, y)
                        else:
                            x, y = self._calc_image_offset('journalon', blk.spr)
                            blk.spr.set_image(self.media_shapes['journalon'], 1,
                                              x, y)
                    dsobject.destroy()
                except:
                    print "Warning: Couldn't open dsobject (%s)" %\
                          (blk.values[0])
                    x, y = self._calc_image_offset('journaloff', blk.spr)
                    blk.spr.set_image(self.media_shapes['journaloff'], 1, x, y)
            else:
                if not movie_media_type(blk.values[0][-4:]):
                    try:
                        w, h, = self._calc_image_size(blk.spr)
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                     blk.values[0], w, h)
                        x, y = self._calc_image_offset('', blk.spr)
                        blk.spr.set_image(pixbuf, 1, x, y)
                    except:
                        x, y = self._calc_image_offset('journaloff', blk.spr)
                        blk.spr.set_image(self.media_shapes['journaloff'],1,x,y)
                else:
                    x, y = self._calc_image_offset('journalon', blk.spr)
                    blk.spr.set_image(self.media_shapes['journalon'], 1, x, y)
            blk.spr.set_label(' ')
            blk.resize()
        elif btype in BOX_STYLE_MEDIA:
            blk.spr.set_label(' ')
            x, y = self._calc_image_offset(btype+'off', blk.spr)
            blk.spr.set_image(self.media_shapes[btype+'off'], 1, x, y)
    
        blk.spr.set_layer(BLOCK_LAYER)
        if check_dock is True:
            blk.connections = 'check'
        return blk
    
    """
    Start a new project with a 'start' brick
    """
    def load_start(self): 
       top = self.process_data([[0, "start", 218, 224, [None, None]]])
    
    """
    Start a project to a file
    """
    def save_file(self):
        if self.save_folder is not None:
            self.load_save_folder = self.save_folder
        fname, self.load_save_folder = get_save_name('.ta',
                                                     self.load_save_folder,
                                                     self.save_file_name)
        if fname is None:
            return
        if fname[-3:]=='.ta':
            fname=fname[0:-3]
        data = self.assemble_data_to_save()
        data_to_file(data, fname+'.ta')
        self.save_file_name = os.path.basename(fname)

    """
    Pack the project (or stack) into a data stream to be serialized
    """
    def assemble_data_to_save(self, save_turtle=True, save_project=True):
        data = []
        blks = []

        if save_project is True:
            blks = self.just_blocks()
        else:
            blks = self._find_group(self.find_top_block(self.selected_blk))
        
        for i, b in enumerate(blks):
             b.id = i
        for b in blks:
            if b.name in CONTENT_BLOCKS or b.name in COLLAPSIBLE:
                if len(b.values)>0:
                    name = (b.name, b.values[0])
                else:
                    name = (b.name)
            elif b.name in EXPANDABLE:
                ex, ey = b.get_expand_x_y()
                if ex > 0:
                    name = (b.name, ex)
                elif ey > 0:
                    name = (b.name, ey)
                else:
                    name = (b.name, 0)
            else:
                name = (b.name)
            if hasattr(b, 'connections'):
                connections = [get_id(c) for c in b.connections]
            else:
                connections = None
            (sx, sy) = b.spr.get_xy()
            # Add a slight offset for copy/paste
            if save_project is False:
                sx+=20
                sy+=20
            data.append((b.id, name, sx-self.canvas.cx, sy-self.canvas.cy,
                         connections))
        if save_turtle is True:
            for k in iter(self.turtles.dict):
                self.canvas.set_turtle(k)
                data.append((-1,['turtle', k],
                             self.canvas.xcor, self.canvas.ycor,
                             self.canvas.heading,
                             self.canvas.color, self.canvas.shade,
                             self.canvas.pensize))
        return data

    """
    Display the coordinates of the current turtle on the toolbar
    """
    def display_coordinates(self):
        x = round_int(self.canvas.xcor/self.coord_scale)
        y = round_int(self.canvas.ycor/self.coord_scale)
        h = round_int(self.canvas.heading)
        if self.running_sugar:
            self.activity.coordinates_label.set_text("%s: %d %s: %d %s: %d" % (
                                   _("xcor"), x, _("ycor"), y, _("heading"), h))
            self.activity.coordinates_label.show()
        else:
            self.win.set_title("%s — %s: %d %s: %d %s: %d" % (_("Turtle Art"),
                                   _("xcor"), x, _("ycor"), y, _("heading"), h))

    """
    Display a message on a status block
    """
    def showlabel(self, shp, label=''):
        if shp == 'syntaxerror' and str(label) != '':
            if self.status_shapes.has_key(str(label)[1:]):
                shp = str(label)[1:]
                label = ''
            else:
                shp = 'status'
        elif shp[0] == '#':
            shp = shp[1:]
            label = ''
        if shp=='notanumber':
            shp = 'overflowerror'
        self.status_spr.set_shape(self.status_shapes[shp])
        self.status_spr.set_label(str(label))
        self.status_spr.set_layer(STATUS_LAYER)
        if shp == 'info':
            self.status_spr.move((PALETTE_WIDTH, self.height-300))
        else:
            self.status_spr.move((PALETTE_WIDTH, self.height-200))

    """
    Relative placement of portfolio objects (used by depreciated blocks)
    """
    def calc_position(self, t):
        w,h,x,y,dx,dy = TEMPLATES[t]
        x *= self.canvas.width
        y *= self.canvas.height
        w *= (self.canvas.width-x)
        h *= (self.canvas.height-y)
        dx *= w
        dy *= h
        return(w,h,x,y,dx,dy)

    """
    Where is the mouse event?
    """
    def _xy(self, event):
        return map(int, event.get_coords())

    """
    Find a stack to run (any stack without a 'def action'on the top).
    """
    def _find_block_to_run(self, blk):
        top = self.find_top_block(blk)
        if blk == top and blk.name[0:3] is not 'def':
            return True
        else:
            return False

    """
    Find the top block in a stack.
    """
    def find_top_block(self, blk):
        if len(blk.connections) == 0:
            return blk
        while blk.connections[0] is not None:
            blk = blk.connections[0]
        return blk

    """
    Find a stack with a 'start' block on top.
    """
    def _find_start_stack(self, blk):
        top = self.find_top_block(blk)
        if top.name == 'start':
            return True
        else:
            return False

    """
    Find the connected group of block in a stack.
    """
    def _find_group(self, blk):
        if blk is None:
            return []
        group=[blk]
        if blk.connections is not None:
            for blk2 in blk.connections[1:]:
                if blk2 is not None:
                    group.extend(self._find_group(blk2))
        return group

    """
    Filter out 'proto', 'trash', and 'deleted' blocks
    """
    def just_blocks(self):
        just_blocks_list = []
        for b in self.block_list.list:
            if b.type == 'block':
                just_blocks_list.append(b)
        return just_blocks_list


    """
    What are the width and height of a stack?
    """
    def _width_and_height(self, blk):
        minx = 10000
        miny = 10000
        maxx = -10000
        maxy = -10000
        for b in self._find_group(blk):
            (x, y) = b.spr.get_xy()
            w, h = b.spr.get_dimensions()
            if x<minx:
                minx = x
            if y<miny:
                miny = y
            if x+w>maxx:
                maxx = x+w
            if y+h>maxy:
                maxy = y+h
        return(maxx-minx, maxy-miny)

    """
    Grab the current canvas and save it.
    """
    def save_as_image(self, name=""):
        if len(name) == 0:
            filename = "ta.png"
        else:
            filename = name+".png"

        if self.running_sugar:
            datapath = os.path.join(self.activity.get_activity_root(),
                                    "instance")
        else:
            datapath = os.getcwd()
        file_path = os.path.join(datapath, filename)
        save_picture(self.canvas, file_path)

        if self.running_sugar:
            dsobject = datastore.create()
            if len(name) == 0:
                dsobject.metadata['title'] = "%s %s" % (self.metadata['title'],
                                                        _("image"))
            else:
                dsobject.metadata['title'] = name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'image/png'
            dsobject.set_file_path(file_path)
            datastore.write(dsobject)
            dsobject.destroy()

    """
    Calculate the postion for placing an image onto a sprite.
    TODO: Rescale images?
        # if iw > w or ih > h:
        #    print "WARNING: need to recale image"
    """
    def _calc_image_offset(self, name, spr, iw=0, ih=0):
        l, t = spr.label_left_top()
        if name == '':
            return (l, t)
        w = spr.label_safe_width()
        h = spr.label_safe_height()
        if iw == 0:
            iw = self.media_shapes[name].get_width()
            ih = self.media_shapes[name].get_height()
        return int(l+(w-iw)/2), int(t+(h-ih)/2)

    """
    Calculate the maximum size for placing an image onto a sprite.
    """
    def _calc_image_size(self, spr):
        w = spr.label_safe_width()
        h = spr.label_safe_height()
        return (w, h)
