# -*- coding: utf-8 -*-
#Copyright (c) 2007, Playful Invention Company
#Copyright (c) 2008-9, Walter Bender
#Copyright (c) 2009, Raúl Gutiérrez Segalés

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
# - we need a method to know if we are running inside Sugar (vs. stand-alone)
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
from constants import *
from talogo import *
from taturtle import *
from taproject import *
import sprite_factory
try:
    from sugar.graphics.objectchooser import ObjectChooser
except:
    pass

from tahoverhelp import *
from gettext import gettext as _


import sprites
import block
import turtlex

"""
TurtleArt Window class abstraction 
"""
class TurtleArtWindow():

    # Import from Journal for these blocks 
    importblocks = ['audiooff', 'descriptionoff','journal']

    # Time out for triggering help
    timeout_tag = [0]


    def __init__(self, win, path, lang, parent=None):
        self._setup_initial_values(win, path, lang, parent)
        # TODO: most of this goes away
        self._setup_misc()
        # the new palette
        self.show_toolbar_palette(0, False)

    def _setup_initial_values(self, win, path, lang, parent):
        self.window = win
        self.path = os.path.join(path,'images')
        self.path_lang = os.path.join(path,'images',lang)
        self.path_en = os.path.join(path,'images/en') # en as fallback
        self.load_save_folder = os.path.join(path,'samples')
        self.save_folder = None
        self.save_file_name = None
        self.window.set_flags(gtk.CAN_FOCUS)
        self.width = gtk.gdk.screen_width()
        self.height = gtk.gdk.screen_height() 

        # Starting from command line
        if parent is None:
            self.window.show_all()
        # Starting from Sugar
        else:
            parent.show_all()

        self._setup_events()

        self.keypress = ""
        self.keyvalue = 0
        self.dead_key = ""
        self.area = self.window.window
        self.gc = self.area.new_gc()
        if self._OLPC_XO_1():
            self.lead = 1.6
            self.scale = 1.0
        else:
            self.lead = 1.0
            self.scale = 1.6
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
        self.dx = 0
        self.dy = 0
        self.media_shapes = {}
        self.cartesian = False
        self.polar = False
        self.overlay_shapes = {}
        self.status_spr = None
        self.status_shapes = {}
        self.palette_spr = None
        self.palettes = []
        self.selected_palette = None
        self.selectors = []
        self.selected_selector = None
        self.selector_shapes = []
        self.selected_blk = None
        self.selected_spr = None
        self.drag_group = None
        self.block_list = block.Blocks()
        self.sprite_list = sprites.Sprites(self.window, self.area, self.gc)
        self.turtle_list = turtlex.Turtles()
        self.selected_turtle = None
        self.turtle = tNew(self,self.width,self.height)
        self.lc = lcNew(self)

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
    Repaint
    """
    def _expose_cb(self, win, event):
        self.sprite_list.redraw_sprites()
        return True

    """
    Are we running from within Sugar?
    """
    def _running_sugar(self): 
        if hasattr(self, 'activity'):
            return True
        return False

    """
    Is the an OLPC XO-1?
    """
    def _OLPC_XO_1(self):
        return os.path.exists('/etc/olpc-release') or \
               os.path.exists('/sys/power/olpc-pm')

    """
    eraser_button: hide status block
    """
    def eraser_button(self):
        self.status_spr.set_layer(HIDE_LAYER)
        clear(self.lc)
        display_coordinates(self)

    """
    stop button
    """
    def stop_button(self):
        stop_logo(self)

    """
    change the icon for user-defined blocks after Python code is loaded
    """
    def set_userdefined(self):
        for blk in self._just_blocks():
            if blk.name == 'nop':
                blk.set_image(self.media_shapes['pythonloaded'])
        self.nop = 'pythonloaded'

    """
    hideshow button
    """
    def hideshow_button(self):
        if self.hide is False: 
            for blk in self._just_blocks():
                blk.spr.set_layer(HIDE_LAYER)
            self._hide_palette() 
            self.hide = True
        else:
            for blk in self._just_blocks():
                blk.spr.set_layer(BLOCK_LAYER)
            self.show_palette()
            self.hide = False
        self.turtle.canvas.inval()

    """
    hideshow_palette 
    """
    def hideshow_palette(self, state):
        if state is False:
            self.palette == False
            if self._running_sugar():
                self.activity.do_hidepalette()
            self._hide_palette()
        else:
            self.palette == True
            if self._running_sugar():
                self.activity.do_showpalette()
            self.show_palette()

    """
    show palette 
    """
    def show_palette(self):
        self.show_toolbar_palette(0)
        self.palette = True

    """
    Hide the palette.
    """
    def _hide_palette(self):
        self.hide_toolbar_palette()
        self.palette = False

    """
    Where is the mouse event?
    """
    def xy(self, event):
        return map(int, event.get_coords())

    """
    run turtle!
    """
    def run_button(self, time):
        if self._running_sugar():
            self.activity.recenter()
        # Look for a 'start' block
        for blk in self._just_blocks():
            if self._find_start_stack(blk):
                self.step_time = time
                print "running stack starting from %s" % (blk.name)
                self._run_stack(blk)
                return
        # If there is no 'start' block, run stacks that aren't 'def action'
        for blk in self._just_blocks():
            if self._find_block_to_run(blk):
                self.step_time = time
                print "running stack starting from %s" % (blk.name)
                self._run_stack(blk)
        return

    """
    Misc. sprites for status, overlays, etc.
    """
    def _setup_misc(self):
        # media blocks get positioned into other blocks
        for i, name in enumerate(MEDIA_SHAPES):
            self.media_shapes[i] = sprites.Sprite(self.sprite_list, 0, 0,
                self._load_sprite_from_file("%s/%s.svg" % (self.path, name)))
            self.media_shapes[i].set_layer(HIDE_LAYER)
            self.media_shapes[i].type = 'media'
        for i, name in enumerate(STATUS_SHAPES):
            self.status_shapes[i] = sprites.Sprite(self.sprite_list,
                self.height-75, 0,
                self._load_sprite_from_file("%s/%s.svg" % (self.path, name)))
            self.status_shapes[i].set_layer(HIDE_LAYER)
            self.status_shapes[i].type = 'status'
        for i in enumerate(OVERLAY_SHAPES):
            self.overlay_shapes[i] = sprites.Sprite(self.sprite_list, 0, 0,
                self._load_sprite_from_file("%s/%s.svg" % (self.path, name)))
            self.overlay_shapes[i].set_layer(HIDE_LAYER)
            self.overlay_shapes[i].type = 'overlay'

    def _load_sprite_from_file(self, name):
        svg = sprite_factory.SVG()
        return sprite_factory.svg_str_to_pixbuf(svg.from_file(name))

    """
    Show/hide turtle palettes
    """
    def hide_toolbar_palette(self, hide_palette_spr=True):
        for i in range(len(PALETTES[self.selected_palette])):        
            self.palettes[self.selected_palette][i].spr.set_layer(HIDE_LAYER)
        if hide_palette_spr is True:
            self.palette_spr.set_layer(HIDE_LAYER)
            self.selected_palette = None
        for i in range(len(PALETTES)):
            self.selectors[i].set_layer(HIDE_LAYER)

    def show_toolbar_palette(self, n, init_only=False):
        if self.selectors == []:
            svg = sprite_factory.SVG()
            x, y = 5, 0
            for i, name in enumerate(PALETTE_NAMES):
                a = self._load_sprite_from_file("%s/%soff.svg" % (self.path,
                                                         name))
                b = self._load_sprite_from_file("%s/%son.svg" % (self.path,
                                                         name))
                self.selector_shapes.append([a,b])
                self.selectors.append(sprites.Sprite(self.sprite_list, x, y, a))
                self.selectors[i].type = 'selector'
                self.selectors[i].name = name
                self.selectors[i].set_layer(TAB_LAYER)
                w, h = self.selectors[i].get_dimensions()
                x += int(w+5) 
        if self.palette_spr is None:
            svg = sprite_factory.SVG()
            self.palette_spr = sprites.Sprite(self.sprite_list, 0, 0,
                sprite_factory.svg_str_to_pixbuf(svg.palette(self.width,
                                                             PALETTE_HEIGHT)))
            self.palette_spr.type = 'category'
        self.palette_spr.set_layer(CATEGORY_LAYER)
        if len(self.palettes) == 0:
            for i in range(len(PALETTES)):
                self.palettes.append([])

        if init_only is True:
            return

        if self.selected_palette is not None:
            self.hide_toolbar_palette(False)

        for i in range(len(PALETTES)):
            self.selectors[i].set_layer(TAB_LAYER)
        
        self.selected_palette = n
        self.selectors[n].set_shape(self.selector_shapes[n][1])
        self.selected_selector = self.selectors[n]

        if self.palettes[n] == []:
            for i, name in enumerate(PALETTES[n]):
                self.palettes[n].append(block.Block(self.block_list,
                                                    self.sprite_list, name,
                                                    0, 0, 'proto', [], 1.5))
                self.palettes[n][i].spr.set_layer(TAB_LAYER)
                self.palettes[n][i].spr.set_shape(self.palettes[n][i].shapes[0])
            # simple packing algorithm
            x, y, max_width = 5, ICON_SIZE+5, 0
            for i in range(len(PALETTES[n])):
                w, h = self.palettes[n][i].spr.get_dimensions()
                if y+h > PALETTE_HEIGHT:
                    y = ICON_SIZE+5
                    x += int(max_width+5)
                    max_width = 0
                self.palettes[n][i].spr.move((int(x), int(y)))
                y += int(h+5)
                if w > max_width:
                    max_width = w
        else:
            for blk in self.palettes[n]:
                blk.spr.set_layer(CATEGORY_LAYER)

    """
    Select a category.
    """
    def _select_category(self, spr):
        i = self.selectors.index(spr)
        spr.set_shape(self.selector_shapes[i][1])
        if self.selected_selector is not None:
            j = self.selectors.index(self.selected_selector)
            self.selected_selector.set_shape(self.selector_shapes[j][0])
        self.selected_selector = spr
        self.show_toolbar_palette(i)

    """
    Find a stack to run (any stack without a 'def action'on the top).
    """
    def _find_block_to_run(self, blk):
        top = self._find_top_block(blk)
        if blk == top and blk.name[0:3] is not 'def':
            return True
        else:
            return False

    """
    Find the top block in a stack.
    """
    def _find_top_block(self, blk):
        while blk.connections[0] is not None:
            blk = blk.connections[0]
        return blk

    """
    Find a stack with a 'start' block on top.
    """
    def _find_start_stack(self, blk):
        top = self._find_top_block(blk)
        if top.name == 'start':
            return True
        else:
            return False

    """
    Find the connected group of block in a stack.
    """
    def _find_group(self, blk):
        group=[blk]
        for blk2 in blk.connections[1:]:
            if blk2 is not None:
                group.extend(self._find_group(blk2))
        return group

    """
    Is a chattube available for sharing?
    """
    def _sharing(self):
        if self._running_sugar() and hasattr(self.activity, 'chattube') and\
            self.activity.chattube is not None:
                return True
        return False

    """
    Mouse move
    """
    def _move_cb(self, win, event):
        x, y = self.xy(event)
        self._mouse_move(x, y)
        return True

    def _mouse_move(self, x, y, verbose=False, mdx=0, mdy=0):
        if verbose:
            print "processing remote mouse move: %d, %d" % (x, y)

        self.block_operation = 'move'
        # First, check to see if we are dragging or rotating a turtle.
        if self.selected_turtle is not None:
            type, dragx, dragy = self.dragpos
            (sx, sy) = self.selected_turtle.spr.get_xy()
            if type == 'move':
                if mdx != 0 or mdy != 0:
                    dx, dy = mdx, mdy
                else:
                    dx, dy = x-dragx-sx, y-dragy-sy
                self.selected_turtle.spr.move((sx+dx, sy+dy))
            else:
                if mdx != 0 or mdy != 0:
                    dx, dy = mdx, mdy
                else:
                    dx, dy = x-sx-30, y-sy-30
                seth(self.turtle, int(dragx+atan2(dy,dx)/DEGTOR+5)/10*10)
        # If we are hoving, show popup help.
        elif self.drag_group is None:
            self._show_popup(x, y)
            return
        # If we have a stack of blocks selected, move them.
        elif self.drag_group[0] is not None:
            blk = self.drag_group[0]
            self.selected_spr = blk.spr
            dragx, dragy = self.dragpos
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
        elif spr and hasattr(spr,'type') and spr.type == 'selector':
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
        if blocks_dict.has_key(block_name):
            block_name_s = _(blocks_dict[block_name])
        else:
            block_name_s = _(block_name)
        if hover_dict.has_key(block_name):
            label = block_name_s + ": " + hover_dict[block_name]
        else:
            label = block_name_s
        if self._running_sugar():
            self.activity.hover_help_label.set_text(label)
            self.activity.hover_help_label.show()
        else:
            self.win.set_title(_("Turtle Art") + " — " + label)
        return 0

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
            self._process_alphanumeric_input(keyname, keyunicode)
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
        oldnum = self.selected_blk.spr.labels[0] 
        if len(oldnum) == 0:
            oldnum = '0'
        if keyname == 'minus':
            if oldnum == '0':
                newnum = '-'
            elif oldnum[0] != '-':
                newnum = '-' + oldnum
        elif keyname == 'period' and '.' not in oldnum:
            newnum = oldnum + '.'
        elif keyname == 'BackSpace':
            if len(oldnum) > 1:
                newnum = oldnum[:len(oldnum)-1]
            else:
                newnum = ''
        elif keyname in ['0','1','2','3','4','5','6','7','8','9']:
            if oldnum == '0':
                newnum = keyname
            else:
                newnum = oldnum + keyname
        else:
            newnum = oldnum
        self.selected_blk.spr.set_label(numcheck(newnum,oldnum))

    """
    Make sure alphanumeric input is properly parsed.
    """
    def _process_alphanumeric_input(self, keyname, keyunicode):
        oldstr = self.selected_blk.spr.labels[0]
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
            if len(oldstr) > 1:
                newstr = oldstr[:len(oldstr)-1]
            else:
                newstr = ''
        else:
            if self.dead_key is not '':
                keyunicode =\
                    DEAD_DICTS[DEAD_KEYS.index(self.dead_key[5:])][keyname]
                self.dead_key = ''
            if keyunicode > 0:
                if unichr(keyunicode) is not '\x00':
                    newstr = oldstr+unichr(keyunicode)
                else:
                    newstr = oldstr
            else:
                newstr = ''
        self.selected_blk.spr.set_label(strcheck(newstr,oldstr))

    """
    Use the keyboard to move blocks and turtle
    """
    def _process_keyboard_commands(self, keyname):
        mov_dict = {'KP_Up':[0,10],'j':[0,10],'Up':[0,10],
                    'KP_Down':[0,-10],'k':[0,-10],'Down':[0,-10],
                    'KP_Left':[-10,0],'h':[-10,0],'Left':[-10,0],
                    'KP_Right':[-10,0],'l':[-10,0],'Right':[-10,0],
                    'KP_Page_Down':[0,0], 'KP_Page_Up':[0,0], 'KP_End':[0,0],
                    'KP_Home':[-1,-1],'Return':[-1,-1], 'Esc':[0,0]}
        if not mov_dict.has_key(keyname):
            return
        if keyname == 'KP_End':
            self.run_button(0)
        elif self.selected_spr is not None:
            blk = self.block_list.spr_to_block(self.selected_spr)
            tur = self.turtle_list.spr_to_turtle(self.selected_spr)
            if blk is not None:
                if keyname == 'Return' or keyname == 'KP_Page_Up':
                    self._click_block()
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
            """
            elif self.selected_spr.type == 'selector':
                if keyname == 'Return' or keyname == 'KP_Page_Up':
                    self._select_category(self.selected_spr)
            """
        return True

    """
    button_press
    """
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
            self.status_spr.set_layer(HIDE_LAYER)

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
            elif blk.type == 'proto':
                if blk.name == 'restore':
                    self._restore_from_trash()
                else:
                    blk.spr.set_shape(blk.shapes[1])
                    self._new_block_from_category(blk.name, x, y+PALETTE_HEIGHT)
                    blk.spr.set_shape(blk.shapes[0])
            return True

        # Next, look for a turtle
        tur = self.turtle_list.spr_to_turtle(spr)
        if tur is not None:
            self.selected_turtle = tur
            self._turtle_pressed(x, y)
            return True

        # Finally, check for anything else
        if hasattr(spr, 'type'):
            if spr.type == "canvas":
                spr.set_layer(CANVAS_LAYER)
                return True
            elif spr.type == 'selector':
                self._select_category(spr)

    """
    Block pressed
    """
    def _block_pressed(self, mask, x, y, blk):
        if blk is not None:
            blk.spr.set_shape(blk.shapes[1])
            self._disconnect(blk)
            self.drag_group = self._find_group(blk)
            (sx, sy) = blk.spr.get_xy()
            self.dragpos = x-sx, y-sy
            for blk in self.drag_group:
                blk.spr.set_layer(TOP_LAYER)

    """
    Unselect block
    """
    def _unselect_block(self):
        # After unselecting a 'number' block, we need to check its value
        if self.selected_blk.name == 'number':
            self._number_check()
        # Reset shape of the selected block
        self.selected_blk.spr.set_shape(self.selected_blk.shapes[0])
        self.selected_blk = None

    """
    Button Press
    """
    def _buttonpress_cb(self, win, event):
        self.window.grab_focus()
        x, y = self.xy(event)
        self.button_press(event.get_state()&gtk.gdk.CONTROL_MASK, x, y)
        if self._sharing():
            if event.get_state()&gtk.gdk.CONTROL_MASK is True:
                self.activity._send_event("p:%d:%d:T" % (x, y))
            else:
                self.activity._send_event("p:%d:%d:F" % (x, y))
        return True

    """
    Button release
    """
    def _buttonrelease_cb(self, win, event):
        x, y = self.xy(event)
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
            (tx, ty) = self.turtle.spr.get_xy()
            self.turtle.xcor = tx-self.turtle.cx- \
                self.turtle.canvas._width/2+30
            self.turtle.ycor = self.turtle.canvas._height/2-ty+ \
                self.turtle.cy-30
            move_turtle(self.turtle)
            display_coordinates(self)
            self.selected_turtle = None
            return

        # If we don't have a group of blocks, then there is nothing to do.
        if self.drag_group == None: 
            return

        blk = self.drag_group[0]
        # Remove blocks by dragging them onto the trash palette
        if self.block_operation=='move' and self._in_the_trash(x, y):
            for b in self.drag_group:
                b.type = 'trash'
                b.spr.hide()
            self.drag_group = None
            return

        # Pull a stack of new blocks off of the category palette.
        if self.block_operation=='new':
            for b in self.drag_group:
                (bx, by) = b.spr.get_xy()
                b.spr.move((bx+200, by))

        # Look to see if we can dock the current stack.
        self._snap_to_dock()
        for b in self.drag_group:
            b.spr.set_layer(BLOCK_LAYER)
        self.drag_group = None

        # Find the block we clicked on and process it.
        if self.block_operation=='click':
            self._click_block()

    """
    click block
    """
    def _click_block(self):
        blk = self.block_list.spr_to_block(self.selected_spr)
        if blk is None:
            return
        self.selected_blk = blk
        if  blk.name=='number' or blk.name=='string':
            pass
            '''
            elif blk.name in self.importblocks:
                self._import_from_journal(self.selected_spr)
            '''
        elif blk.name=='nop' and self.myblock==None:
            self.activity.import_py()
        else:
            self._run_stack(blk)

    """
    snap_to_dock
    """
    def _snap_to_dock(self):
        my_block = self.drag_group[0]
        d = 200
        for my_dockn in range(len(my_block.docks)):
            for i, your_block in enumerate(self._just_blocks()):
                # don't link to a block to which you're already connected
                if your_block in self.drag_group:
                    continue
                # check each dock of your_block for a possible connection
                for your_dockn in range(len(your_block.docks)):
                    this_xy = self._dock_dx_dy(your_block, your_dockn,
                                              my_block, my_dockn)
                    if self._magnitude(this_xy) > d:
                        continue
                    d = self._magnitude(this_xy)
                    best_xy = this_xy
                    best_you = your_block
                    best_your_dockn = your_dockn
                    best_my_dockn = my_dockn
        if d<200:
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
    import from Journal
    """
    def _import_from_journal(self, spr):
        if self._running_sugar():
            chooser = ObjectChooser('Choose image', None,\
                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
            try:
                result = chooser.run()
                if result == gtk.RESPONSE_ACCEPT:
                    dsobject = chooser.get_selected_object()
                    # change block graphic to indicate that object is "loaded"
                    blk = self.block_list.spr_to_block(spr)
                    if blk.name == 'journal':
                        self._load_image(dsobject, spr)
                    elif blk.name == 'audiooff':
                        spr.set_image(self.media_shapes['audioon'])
                    else:
                        spr.set_image(self.media_shapes['decson'])
                    spr.ds_id = dsobject.object_id
                    dsobject.destroy()
            finally:
                chooser.destroy()
                del chooser
        else:
            print "Journal Object Chooser unavailable from outside of Sugar"

    """
    Run stack
    """
    def _run_stack(self, blk):
        if blk is None:
            return
        self.lc.ag = None
        top = self._find_top_block(blk)
        run_blocks(self.lc, top, self._just_blocks(), True)
        gobject.idle_add(doevalstep, self.lc)

    """
    Restore all the blocks in the trash can
    """
    def _restore_from_trash(self):
        for b in self.block_list.list:
            if b.type == 'trash':
                b.spr.set_layer(BLOCK_LAYER)
                x,y = b.spr.get_xy()
                b.spr.move((x,y+200))
                b.type = 'block'

    """
    Is x,y over the trash can?
    """
    def _in_the_trash(self, x, y):
        if self.selected_palette == TRASH and self.palette_spr.hit((x,y)):
            return True
        return False

    """
    Filter out 'proto' blocks
    """
    def _just_blocks(self):
        just_blocks_list = []
        for b in self.block_list.list:
            if b.type == 'block':
                just_blocks_list.append(b)
        return just_blocks_list

    """
    Make a new block.
    """
    def _new_block_from_category(self, name, x, y):
        # load alternative image of nop block if python code is loaded
        if name == 'nop' and self.nop == 'pythonloaded':
            pass
            # TODO: handle python-loaded case
            # newspr = Sprite(self,x-20,y-20,self.media_shapes['pythonloaded'])
        else:
            newblk = block.Block(self.block_list, self.sprite_list, name,
                                 x-20, y-20, 'block', [])
            newspr = newblk.spr
        newspr.set_layer(TOP_LAYER)
        self.dragpos = 20, 20
        newblk.connections = [None]*len(newblk.docks)
        for i, argvalue in enumerate(newblk.defaults):
            # skip the first dock position--it is always a connector
            dock = newblk.docks[i+1]
            argname = dock[0]
            if argname == 'unavailable':
                continue
            if (type(argvalue) is str or type(argvalue) is unicode) and\
               argname == 'number':
                argname = 'string'
            (sx, sy) = newspr.get_xy()
            argblk = block.Block(self.block_list, self.sprite_list,
                                 argname, 0, 0)
            argdock = argblk.docks[0]
            nx, ny = sx+dock[2]-argdock[2], sy+dock[3]-argdock[3]
            argblk.spr.move((nx, ny))
            argblk.spr.set_label(str(argvalue))
            argblk.spr.set_layer(TOP_LAYER)
            argblk.connections = [newblk, None]
            newblk.connections[i+1] = argblk
        self.drag_group = self._find_group(newblk)
        self.block_operation = 'new' 

    """
    Debugging tools
    """
    def _print_spr_list(self, spr_list):
        s = ""
        for spr in spr_list:
            if spr == None:
                s+="None"
            else:
                s+=self.block_list.spr_to_block(spr).name
            s += " "
        return s

    def _print_blk_list(self, blk_list):
        s = ""
        for blk in blk_list:
            if blk == None:
                s+="None"
            else:
                s+=blk.name
            s += " "
        return s

    """
    Disconnect block from stack above it.
    """
    def _disconnect(self, blk):
        if blk.connections[0]==None:
            return
        blk2=blk.connections[0]
        blk2.connections[blk2.connections.index(blk)] = None
        blk.connections[0] = None

    """
    Turtle pressed
    """
    def _turtle_pressed(self, x, y):
        (tx, ty) = self.turtle.spr.get_xy()
        dx, dy = x-tx-30, y-ty-30
        if dx*dx+dy*dy > 200:
            self.dragpos = ('turn', self.turtle.heading-atan2(dy,dx)/DEGTOR, 0)
        else:
            self.dragpos = ('move', x-tx, y-ty)

    """
    Replace Journal block graphic with preview image 
    TODO: move to block
    """
    def _load_image(self, picture, spr):
        from talogo import get_pixbuf_from_journal
        pixbuf = get_pixbuf_from_journal(picture,spr.width,spr.height)
        if pixbuf is not None:
            spr.set_image(pixbuf)
        else:
            spr.set_image(self.media_shapes['texton'])

    """
    Find the distance between the dock points of two blocks.
    """
    def _dock_dx_dy(self, block1, dock1n, block2, dock2n):
        dock1 = block1.docks[dock1n]
        dock2 = block2.docks[dock2n]
        d1type, d1dir, d1x, d1y = dock1[0:4]
        d2type, d2dir, d2x, d2y = dock2[0:4]
        if (d2type is not 'number') or (dock2n is not 0):
            if block1.connections is not None and dock1n < block1.connections\
                and block1.connections[dock1n] is not None:
                    return (100,100)
            if block2.connections is not None and dock2n < block2.connections\
                and block2.connections[dock2n] is not None:
                    return (100,100)
        if block1 == block2:
            return (100,100)
        if d1type != d2type:
            # some blocks can take strings or nums
            if block1.name in ('write', 'plus', 'equal', 'less', 'greater',
                               'template1', 'template2', 'template3',
                               'template4', 'template6', 'template7', 'nop',
                               'print', 'stack'):
                if block1.name == 'write' and d1type == 'string':
                    if d2type == 'number' or d2type == 'string':
                        pass
                else: 
                    if d2type == 'number' or d2type == 'string':
                        pass
            # some blocks can take strings, nums, or Journal
            elif block1.name in ('show', 'push', 'storein', 'storeinbox1',
                                 'storeinbox2'):
                if d2type in CONTENT_BLOCKS:
                    pass
            # some blocks can take media, audio, movies, of descriptions
            elif block1.name in ('containter'):
                if d1type == 'audiooff' or d1type == 'journal':
                    pass
            else:
                return (100,100)
        if d1dir == d2dir:
            return (100,100)
        (b1x, b1y) = block1.spr.get_xy()
        (b2x, b2y) = block2.spr.get_xy()
        return ((b1x+d1x)-(b2x+d2x), (b1y+d1y)-(b2y+d2y))

    """
    Magnitude 
    """
    def _magnitude(self, pos):
        x,y = pos
        return x*x+y*y

    """
    Jog turtle
    """
    def _jog_turtle(self, dx, dy):
        if dx == -1 and dy == -1:
            self.turtle.xcor = 0
            self.turtle.ycor = 0
        else:
            self.turtle.xcor += dx
            self.turtle.ycor += dy
        move_turtle(self.turtle)
        display_coordinates(self)
        self.selected_turtle = None

    """
    Jog block
    """
    def _jog_block(self, blk, dx, dy):
        # drag entire stack if moving lock block
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
        if self.selected_blk.spr.labels[0] in ['-', '.', '-.']:
            self.selected_blk.spr.set_label('0')
        if self.selected_blk.spr.labels[0] is not None:
            try:
                n = float(self.selected_blk.spr.labels[0])
                if n > 1000000:
                    self.selected_blk.spr.set_label('1')
                    showlabel(self.lc, "#overflowerror")
                elif n < -1000000:
                    self.selected_blk.spr.set_label('-1')
                    showlabel(self.lc, "#overflowerror")
            except ValueError:
                self.selected_blk.spr.set_label('0')
                showlabel(self.lc, "#notanumber")

#
# Utilities used for checking variable validity
#

def numcheck(new, old):
    if new is '': return "0"
    if new in ['-', '.', '-.']: return new
    if new=='.': return '0.'
    try: float(new); return new
    except ValueError,e : return old

def strcheck(new, old):
    try: str(new); return new
    except ValueError,e : return old

