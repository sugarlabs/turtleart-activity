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
from tasetup import *
from talogo import *
from taturtle import *
from taproject import *
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
        prep_selectors(self) # i wonder where this method belongs
        for s in selectors:
            setup_selectors(self,s)
        setup_misc(self)
        self._select_category(self.selbuttons[0])

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

        # starting from command line
        if parent is None:
            self.window.show_all()
        # starting from Sugar
        else:
            parent.show_all()

        self._setup_events()

        self.keypress = ""
        self.keyvalue = 0
        self.dead_key = ""
        self.firstkey = True
        self.area = self.window.window
        self.gc = self.area.new_gc()
        # on an OLPC-XO-1, there is a scaling factor
        if self._is_XO_1():
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
        self.selected_spr = None
        self.selected_blk = None
        # self.selected_turtle = None # in anticipation of multiple turtles
        self.draggroup = None
        self.myblock = None
        self.nop = 'nop'
        self.loaded = 0
        self.step_time = 0
        self.hide = False
        self.palette = True
        self.coord_scale = 1
        """
        NEW SVG/BLOCK initializations
        """
        self.sprite_list = sprites.Sprites(self.window, self.area, self.gc)
        self.block_list = block.Blocks()
        self.turtle_list = turtlex.Turtles()
        """
        """
        self.turtle = tNew(self,self.width,self.height)
        self.lc = lcNew(self)
        self.buddies = []
        self.dx = 0
        self.dy = 0
        self.cartesian = False
        self.polar = False
        self.spr = None # "currently selected spr"

    """
    DEPRECATED
    """
    def runtool(self, spr, cmd, *args):
        cmd(*(args))

    """
    eraser_button: hide status block
    """
    def eraser_button(self):
        self.status_spr.set_layer(400)
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
        for blk in self.block_list.list:
            if blk.name == 'nop':
                blk.set_image(self.media_shapes['pythonloaded'])
        self.nop = 'pythonloaded'

    """
    hideshow button
    """
    def hideshow_button(self):
        if self.hide is False: 
            for b in self.block_list.list:
                b.spr.set_layer(HIDE_LAYER)
            self._hide_palette() 
            self.hide = True
        else:
            for b in self.block_list.list:
                b.spr.set_layer(BLOCK_LAYER)
            self.show_palette()
            self.hide = False
        self.turtle.canvas.inval()


    """
    run turtle!
    """
    def run_button(self, time):
        print "you better run, turtle, run!!"
        # look for the start block
        for b in self.block_list.list:
            if self._find_start_stack(b.spr):
                self.step_time = time
                if hasattr(self, 'activity'):
                    self.activity.recenter()
                self._run_stack(b.spr)
                return
        # no start block, so run a stack that isn't a hat
        for b in self.blocks_list.list:
            if self._find_block_to_run(b.spr):
                print "running " + b.name
                self.step_time = time
                self._run_stack(b.spr)
        return

    """
    button_press
    """
    def button_press(self, mask, x, y, verbose=False):
        if verbose:
            print "processing remote button press: " + str(x) + " " + str(y)
        self.block_operation = 'click'
        if self.selected_spr is not None:
            self._unselect()
        else:
            self.status_spr.set_layer(HIDE_LAYER)
        spr = self.sprite_list.find_sprite((x,y))
        blk = self.block_list.spr_to_block(spr)
        print "found %s at (%d,%d)" % (str(spr),x,y)
        self.x, self.y = x,y
        self.dx = 0
        self.dy = 0
        if spr is None:
            return True
        if hasattr(spr, 'type'):
            print "type: %s" % (spr.type)
            if spr.type == "canvas":
                spr.set_layer(CANVAS_LAYER)
                return True
            elif spr.type == 'selbutton':
                self._select_category(spr)
            elif spr.type == 'category':
                self._block_selector_pressed(x,y)
            elif spr.type == 'turtle':
                self._turtle_pressed(x,y)
        elif blk is not None:
            self._block_pressed(mask,x,y,spr)
        self.spr = spr

    """
    hideshow_palette 
    """
    def hideshow_palette(self, state):
        if state is False:
            self.palette == False
            if hasattr(self, 'activity'):
                # Use new toolbar design
                self.activity.do_hidepalette()
            self._hide_palette()
        else:
            self.palette == True
            if hasattr(self, 'activity'):
                # Use new toolbar design
                self.activity.do_showpalette()
            self.show_palette()

    """
    show palette 
    """
    def show_palette(self):
        for i in self.selbuttons: i.set_layer(TAB_LAYER)
        self._select_category(self.selbuttons[0])
        self.palette = True

    def xy(self, event):
        return map(int, event.get_coords())

    """
    unselect
    """
    def _unselect(self):
        if self.selected_spr.labels[0] in ['-', '.', '-.']:
            self.selected_spr.set_label('0')

        # put an upper and lower bound on numbers to prevent OverflowError
        if self.block_list.spr_to_block(self.selected_spr).name == 'number'\
            and self.selected_spr.labels[0] is not None:
            try:
                i = float(self.selected_spr.labels[0])
                if i > 1000000:
                    self.selected_spr.set_label('1')
                    showlabel(self.lc,"#overflowerror")
                elif i < -1000000:
                    self.selected_spr.set_label('-1')
                    showlabel(self.lc,"#overflowerror")
            except ValueError:
                pass

        self.selected_spr.set_shape(
                      self.block_list.spr_to_block(self.selected_spr).shape)
        self.selected_spr = None

    """
    select category 
    """
    def _select_category(self, spr):
        if hasattr(self, 'current_category'):
            self.current_category.set_shape(self.current_category.offshape)
        spr.set_shape(spr.onshape)
        self.current_category = spr
        self.category_spr.set_shape(spr.group)

    """
    hide palette 
    """
    def _hide_palette(self):
        for i in self.selbuttons: i.hide()
        self.category_spr.set_shape(self.hidden_palette_icon)
        self.palette = False

    """
    register the events we listen to 
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
    XO-1 ?
    """
    def _is_XO_1(self):
        return os.path.exists('/etc/olpc-release') or \
               os.path.exists('/sys/power/olpc-pm')

    """
    find a stack to run (any stack without a hat)
    """
    def _find_block_to_run(self, spr):
        top = self._find_top_block(spr)
        if spr == top and self.block_list.spr_to_block(spr).name[0:3] != 'hat':
            return True
        else:
            return False

    """
    find top block
    """
    def _find_top_block(self, spr):
        blk = self.block_list.spr_to_block(spr)
        b = blk.spr
        while blk.connections[0]!=None:
            b=blk.connections[0]
        return b

    """
    find start stack
    """
    def _find_start_stack(self, spr):
        top = self._find_top_block(spr)
        if self.block_list.spr_to_block(top).name == 'start':
            return True
        else:
            return False

    """
    tube available?
    """
    def _sharing(self):
        ret = False
        if hasattr(self, 'activity') and hasattr(self.activity, 'chattube'):
            if self.activity.chattube is not None:
                ret = True
        return ret

    """
    Mouse move
    """
    def _move_cb(self, win, event):
        x,y = self.xy(event)
        self._mouse_move(x, y)
        return True

    def _mouse_move(self, x, y, verbose=False, mdx=0, mdy=0):
        if verbose:
            print "processing remote mouse move: " + str(x) + " " + str(y)
        if self.draggroup is None:
            self._show_popup(x, y)
            return

        self.block_operation = 'move'
        spr = self.draggroup[0]
        blk = self.block_list.spr_to_block(spr)
        if blk is not None:
            self.spr = spr
            dragx, dragy = self.dragpos
            if mdx != 0 or mdy != 0:
                dx,dy = mdx,mdy
            else:
                (sx,sy) = spr.get_xy()
                dx,dy = x-dragx-sx,y-dragy-sy
            # skip if there was a move of 0,0
            if dx == 0 and dy == 0:
                return
            # drag entire stack if moving lock block
            
            if blk.name == 'lock':
                self.draggroup = findgroup(self._find_top_block(spr),
                                           self.block_list)
            else:
                self.draggroup = findgroup(spr, self.block_list)
            # check to see if any block ends up with a negative x
            for b in self.draggroup:
                (bx, by) = b.get_xy()
                if bx+dx < 0:
                    dx += -(bx+dx)
            # move the stack
            for b in self.draggroup:
                (bx, by) = b.get_xy()
                b.move((bx+dx, by+dy))
        if self.turtle_list.spr_to_turtle(spr) is not None:
            type,dragx,dragy = self.dragpos
            (sx,sy) = spr.get_xy()
            if type == 'move':
                if mdx != 0 or mdy != 0:
                    dx,dy = mdx,mdy
                else:
                    dx,dy = x-dragx-sx,y-dragy-sy
                spr.move((sx+dx, sy+dy))
            else:
                if mdx != 0 or mdy != 0:
                    dx,dy = mdx,mdy
                else:
                    dx,dy = x-sx-30,y-sy-30
                seth(self.turtle, int(dragx+atan2(dy,dx)/DEGTOR+5)/10*10)
        if mdx != 0 or mdy != 0:
            dx,dy = 0,0
        else:
            self.dx += dx
            self.dy += dy

    """
    get_proto_from_category
    """
    def _get_proto_from_category(self, x, y):
        (sx,sy) = self.category_spr.get_xy()
        pixel = self.current_category.get_pixel(self.current_category.mask,
                                                x-sx, y-sy)
        index = ((pixel%256)>>3)-1
        if index==0:
            return 'hide'
        index-=1
        if index>len(self.current_category.blockprotos):
            return None
        return self.current_category.blockprotos[index]

    """
    lets help our users by displaying a little help
    """
    def _show_popup(self, x, y):
        spr = self.sprite_list.find_sprite((x,y))
        blk = self.block_list.spr_to_block(spr)
        if spr and blk is not None:
            if self.timeout_tag[0] == 0:
                self.timeout_tag[0] = self._do_show_popup(blk.name)
                self.spr = spr
            else:
                if self.timeout_tag[0] > 0:
                    try:
                        gobject.source_remove(self.timeout_tag[0])
                        self.timeout_tag[0] = 0
                    except:
                        self.timeout_tag[0] = 0
        elif spr and spr.type == 'category':
            proto = self._get_proto_from_category(x, y)
            if proto and proto!='hide':
                if self.timeout_tag[0] == 0:
                    self.timeout_tag[0] = self._do_show_popup(proto.name)
                    self.spr = spr
                    return
            else:
                if self.timeout_tag[0] > 0:
                    try:
                        gobject.source_remove(self.timeout_tag[0])
                        self.timeout_tag[0] = 0
                    except:
                        self.timeout_tag[0] = 0
        elif spr and spr.type == 'selbutton':
            if self.timeout_tag[0] == 0:
                self.timeout_tag[0] = self._do_show_popup(spr.name)
                self.spr = spr
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
    fetch the help text and display it 
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
        if hasattr(self, "activity"):
            self.activity.hover_help_label.set_text(label)
            self.activity.hover_help_label.show()
        elif hasattr(self, "win"):
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
            print "processing remote key press: " + keyname
        self.keypress = keyname
        if alt_mask is True and self.selected_spr==None:
            if keyname=="i" and hasattr(self, 'activity'):
                self.activity.waiting_for_blocks = True
                self.activity._send_event("i") # request sync for sharing
            elif keyname=="p":
                self.hideshow_button()
            elif keyname=='q':
                exit()
            return True
        if self.selected_blk is not None and \
           self.selected_blk.name == 'number':
            if keyname in ['minus', 'period']: 
                keyname = {'minus': '-', 'period': '.'}[keyname]
            oldnum = self.selected_spr.labels[0] 
            if keyname == 'BackSpace':
                if len(oldnum) > 1:
                    newnum = oldnum[:len(oldnum)-1]
                else:
                    newnum = ''
                self.selected_spr.set_label(numcheck(newnum,oldnum))
                if len(newnum) > 0:
                    self.firstkey = False
                else:
                    self.firstkey = True
            if len(keyname)>1:
                return True
        else: # gtk.keysyms.Left ...
            if keyname in ['Escape', 'Return', 'j', 'k', 'h', 'l', 'KP_Page_Up',
                           'Up', 'Down', 'Left', 'Right', 'KP_Home', 'KP_End',
                           'KP_Up', 'KP_Down', 'KP_Left', 'KP_Right',
                           'KP_Page_Down']:
                # move blocks (except number and text blocks only with arrows)
                # or click with Return
                if keyname == 'KP_End':
                    self.run_button(0)
                elif self.spr is not None:
                    if self.spr.type == 'turtle': # jog turtle with arrow keys
                        if keyname == 'KP_Up' or keyname == 'j' \
                                              or keyname == 'Up':
                            self._jog_turtle(0,10)
                        elif keyname == 'KP_Down' or keyname == 'k' or \
                             keyname == 'Down':
                            self._jog_turtle(0,-10)
                        elif keyname == 'KP_Left' or keyname == 'h' or \
                             keyname == 'Left':
                            self._jog_turtle(-10,0)
                        elif keyname == 'KP_Right' or keyname == 'l' or \
                             keyname == 'Right':
                            self._jog_turtle(10,0)
                        elif keyname == 'KP_Home':
                            self._jog_turtle(-1,-1)
                    elif self.spr.type == 'block':
                        if keyname == 'Return' or keyname == 'KP_Page_Up':
                            self._click_block()
                        elif keyname == 'KP_Up' or keyname == 'j' or \
                             keyname == 'Up':
                            self._jog_block(0,10)
                        elif keyname == 'KP_Down' or keyname == 'k' or \
                             keyname == 'Down':
                            self._jog_block(0,-10)
                        elif keyname == 'KP_Left' or keyname == 'h' or \
                             keyname == 'Left':
                            self._jog_block(-10,0)
                        elif keyname == 'KP_Right' or keyname == 'l' or \
                             keyname == 'Right':
                            self._jog_block(10,0)
                        elif keyname == 'KP_Page_Down':
                            if self.draggroup == None:
                                self.draggroup = findgroup(self.spr,
                                                           self.block_list)
                            for b in self.draggroup: b.hide()
                            self.draggroup = None
                    elif self.spr.type == 'selbutton':
                        if keyname == 'Return' or keyname == 'KP_Page_Up':
                            self._select_category(self.spr)
                    elif self.spr.type == 'category':
                        if keyname == 'Return' or keyname == 'KP_Page_Up':
                            (x,y) = self.window.get_pointer()
                            self._block_selector_pressed(x, y)
                            for b in self.draggroup:
                               (bx, by) = b.get_xy()
                               b.move((bx+200, by))
                            self.draggroup = None
                return True
        if self.selected_spr is None:
            return False
        if keyname in ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock', \
                       'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift']:
            keyname = ''
            keyunicode = 0
        # Hack until I sort out input and unicode + dead keys
        if keyname[0:5] == 'dead_':
            self.dead_key = keyname
            keyname = ''
            keyunicode = 0
        if keyname in WHITE_SPACE:
            keyunicode = 32
        oldnum = self.selected_spr.labels[0]
        if keyname == 'BackSpace':
            if len(oldnum) > 1:
                newnum = oldnum[:len(oldnum)-1]
            else:
                newnum = ''
            self.selected_spr.set_label(strcheck(newnum,oldnum))
            if len(newnum) > 0:
                self.firstkey = False
            else:
                self.firstkey = True
        else:
            if self.dead_key is not '':
                keyunicode =\
                    DEAD_DICTS[DEAD_KEYS.index(self.dead_key[5:])][keyname]
                self.dead_key = ""
            if self.firstkey:
                newnum = strcheck(unichr(keyunicode), "")
            elif keyunicode > 0:
                if unichr(keyunicode) is not '\x00':
                    newnum = oldnum+unichr(keyunicode)
                else:
                    newnum = oldnum
            else:
                newnum = ""
            self.selected_spr.set_label(strcheck(newnum,oldnum))
            self.firstkey = False
        return True

    """
    Button release
    """
    def _buttonrelease_cb(self, win, event):
        x,y = self.xy(event)
        self.button_release(x, y)
        if self._sharing():
            # print "sending release button"
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
            print "processing remote button release: " + str(x) + " " + str(y)
        if self.draggroup == None: 
            return
        spr = self.draggroup[0]
        if self.turtle_list.spr_to_turtle(spr) is not None:
            print "clicked on a turtle"
            (tx, ty) = self.turtle.spr.get_xy()
            self.turtle.xcor = tx-self.turtle.cx- \
                self.turtle.canvas._width/2+30
            self.turtle.ycor = self.turtle.canvas._height/2-ty+ \
                self.turtle.cy-30
            move_turtle(self.turtle)
            display_coordinates(self)
            self.draggroup = None
            return
        # remove block by dragging them onto the category palette
        if self.block_operation=='move' and self.category_spr.hit((x,y)):
            for b in self.draggroup: b.hide()
            self.draggroup = None
            return
        if self.block_operation=='new':
            for b in self.draggroup:
                (bx, by) = b.get_xy()
                b.move((bx+200, by))
        self._snap_to_dock()
        for b in self.draggroup: b.set_layer(BLOCK_LAYER)
        self.draggroup = None
        if self.block_operation=='click':
            blk = self.block_list.spr_to_block(self.spr)
            if blk is not None and blk.name=='number':
                self.selected_spr = spr
                self.selected_blk = blk
                self.selected_spr.set_shape(blk.selected_shape)
                self.firstkey = True
            elif blk is not None and self.defdict.has_key(blk.name):
                self.selected_spr = spr
                self.selected_blk = blk
                if blk.name=='string':
                    self.selected_spr.set_shape(blk.selected_shape)
                    self.firstkey = True
                elif blk.name in self.importblocks:
                    self._import_from_journal(spr)
            elif blk is not None and blk.name=='nop' and self.myblock==None:
                self.activity.import_py()
            else:
                # mark block as selected
                self.selected_spr = spr
                self.selected_blk = blk
                if blk is not None:
                    self.selected_spr.set_shape(blk.selected_shape)
                spr.set_selected(True)
                self._run_stack(spr)

    """
    click block
    """
    def _click_block(self):
        blk = self.block_list.spr_to_block(self.spr)
        if blk is not None and blk.name=='number':
            self.selected_spr = self.spr
            self.selected_blk = blk
            self.firstkey = True
        elif blk is not None and self.defdict.has_key(blk.name):
            self.selected_spr = self.spr
            self.selected_blk = blk
            if blk.name=='string':
                self.firstkey = True
            elif blk.name in self.importblocks:
                self._import_from_journal(self.spr)
        elif blk is not None and blk.name=='nop' and self.myblock==None:
            self.activity.import_py()
        else: self._run_stack(self.spr)

    """
    Repaint
    """
    def _expose_cb(self, win, event):
        self.sprite_list.redraw_sprites()
        return True

    """
    Button Press
    """
    def _buttonpress_cb(self, win, event):
        self.window.grab_focus()
        x, y = self.xy(event)
        self.button_press(event.get_state()&gtk.gdk.CONTROL_MASK, x, y)
  
        # if sharing, send button press
        if self._sharing():
            # print "sending button pressed"
            if event.get_state()&gtk.gdk.CONTROL_MASK is True:
                self.activity._send_event("p:"+str(x)+":"+str(y)+":"+'T')
            else:
                self.activity._send_event("p:"+str(x)+":"+str(y)+":"+'F')
        return True

    """
    snap_to_dock
    """
    def _snap_to_dock(self):
        spr = self.draggroup[0]
        my_block = self.block_list.spr_to_block(spr)
        self.block_list.print_list()
        d = 200
        for my_dockn in range(len(my_block.docks)):
            for i, your_block in enumerate(self.block_list.list):
                # don't link to a block to which you're already connected
                if your_block.spr in self.draggroup:
                    continue
                # check each dock of your_block for a possible connection
                for your_dockn in range(len(your_block.docks)):
                    this_xy = self._dock_dx_dy(your_block, your_dockn,
                                              my_block, my_dockn)
                    if self._magnitude(this_xy) > d:
                        continue
                    your_block.spr.set_shape(your_block.selected_shape)
                    d = self._magnitude(this_xy)
                    best_xy = this_xy
                    best_you = your_block
                    best_your_dockn = your_dockn
                    best_my_dockn = my_dockn
        if d<200:
            for b in self.draggroup:
                (bx, by) = b.get_xy()
                b.move((bx+best_xy[0],by+best_xy[1]))
            block_in_dock = best_you.connections[best_your_dockn]
            if block_in_dock is not None:
                for b in findgroup(block_in_dock, self.block_list):
                    b.hide()
            best_you.connections[best_your_dockn] = my_block.spr
            if my_block.connections is not None:
                my_block.connections[best_my_dockn] = best_you.spr

    """
    import from Journal
    """
    def _import_from_journal(self, spr):
        if hasattr(self, "activity"): # this should be a method: _inside_sugar()
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
    run stack
    """
    def _run_stack(self, spr):
        self.lc.ag = None
        top = self._find_top_block(spr)
        run_blocks(self.lc, top, self.block_list.list, True)
        gobject.idle_add(doevalstep, self.lc)

    """
    # phased out
    filter out blocks
    """
    def _blocks(self):
        return [spr for spr in self.sprite_list.list if spr.type == 'block']

    """
    block selector pressed
    """
    def _block_selector_pressed(self, x, y):
        proto = self._get_proto_from_category(x, y)
        if proto==None:
            return
        if proto is not 'hide':
            self._new_block_from_category(proto, x, y)
        else:
            self.hideshow_palette(False)

    """
    new block from category
    """
    def _new_block_from_category(self, proto, x, y):
        if proto is None:
            return True

        #
        # Create new instance of a block
        # 

        # load alternative image of nop block if python code is loaded
        if proto.name == 'nop' and self.nop == 'pythonloaded':
            pass
            # TODO: handle python-loaded case
            # newspr = Sprite(self,x-20,y-20,self.media_shapes['pythonloaded'])
        else:
            newblk = block.Block(self.block_list, self.sprite_list, proto.name,
                                 x-20, y-20, [proto.name])
            newspr = newblk.spr

        newspr.set_layer(TOP_LAYER)
        self.dragpos = 20,20
        newblk.primname = proto.primname
        if self.defdict.has_key(newblk.name):
            newspr.labels[0]=self.defdict[newblk.name]
        newblk.connections = [None]*len(newblk.docks)
        print "%s: %s" % (newblk.name, newblk.connections)
        for i in range(len(newblk.defaults)):
            dock = newblk.docks[i+1]
            argproto = self.protodict[self.valdict[dock[0]]]
            argdock = argproto.docks[0]
            (sx, sy) = newspr.get_xy()
            nx, ny = sx+dock[2]-argdock[2], sy+dock[3]-argdock[3]
            argblk = block.Block(self.block_list, self.sprite_list,
                                 argproto.name, nx, ny)
            argspr = argblk.spr
            argspr.set_label(str(newblk.defaults[i]))
            argspr.set_layer(TOP_LAYER)
            argblk.connections = [newspr,None]
            newblk.connections[i+1] = argspr
            print "%s: %s" % (argblk.name, argblk.connections)
        self.draggroup = findgroup(newspr, self.block_list)
        self.block_operation = 'new' 

    """
    block pressed
    TODO: mark block as selected
    """
    def _block_pressed(self, mask, x, y, spr):
        if spr is not None:
            blk = self.block_list.spr_to_block(spr)
            if blk is not None:
                print "in block_pressed: creating draggroup with %s" % (
                      blk.name)
            self.draggroup = findgroup(spr, self.block_list)
            for b in self.draggroup: b.set_layer(TOP_LAYER)
            if self.block_list.spr_to_block(spr).connections[0] is not None and\
                           self.block_list.spr_to_block(spr).name == 'lock':
                b = self._find_top_block(spr)
                (bx, by) = b.get_xy()
                self.dragpos = x-bx,y-by
            else:
                (sx, sy) = spr.get_xy()
                self.dragpos = x-sx,y-sy
                self._disconnect(spr)

    """
    disconnect block
    """
    def _disconnect(self, b):
        blk = self.block_list.spr_to_block(b)
        if blk.connections[0]==None:
            return
        b2=blk.connections[0]
        blk2 = self.block_list.spr_to_block(b2)
        blk2.connections[blk2.connections.index(b)] = None
        blk.connections[0] = None

    """
    turtle pressed
    """
    def _turtle_pressed(self, x, y):
        (tx, ty) = self.turtle.spr.get_xy()
        dx, dy = x-tx-30, y-ty-30
        if dx*dx+dy*dy > 200:
            self.dragpos = ('turn', self.turtle.heading-atan2(dy,dx)/DEGTOR, 0)
        else:
            self.dragpos = ('move', x-tx, y-ty)
        self.draggroup = [self.turtle.spr]

    """
    Replace Journal block graphic with preview image 
    """
    def _load_image(self, picture, spr):
        from talogo import get_pixbuf_from_journal
        pixbuf = get_pixbuf_from_journal(picture,spr.width,spr.height)
        if pixbuf is not None:
            spr.set_image(pixbuf)
        else:
            spr.set_image(self.media_shapes['texton'])

    """
    dock_dx_dy 
    """
    def _dock_dx_dy(self, block1, dock1n, block2, dock2n):
        dock1 = block1.docks[dock1n]
        dock2 = block2.docks[dock2n]
        d1type, d1dir, d1x, d1y = dock1[0:4]
        d2type, d2dir, d2x, d2y = dock2[0:4]
        if (d2type is not 'num') or (dock2n is not 0):
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
            if block1.name in ('write', 'plus2', 'equal', 'less', 'greater',
                               'template1', 'template2', 'template3',
                               'template4', 'template6', 'template7', 'nop',
                               'print', 'stack'):
                if block1.name == 'write' and d1type == 'string':
                    if d2type == 'num' or d2type == 'string':
                        pass
                else: 
                    if d2type == 'num' or d2type == 'string':
                        pass
            # some blocks can take strings, nums, or Journal
            elif block1.name in ('show', 'push', 'storein', 'storeinbox1',
                                 'storeinbox2'):
                if d2type == 'num' or d2type == 'string' or d2type == 'journal':
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
    magnitude 
    """
    def _magnitude(self, pos):
        x,y = pos
        return x*x+y*y

    """
    jog turtle
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
        self.draggroup = None

    """
    jog block
    """
    def _jog_block(self,dx,dy):
        # drag entire stack if moving lock block
        if self.block_list.spr_to_block(spr).name == 'lock':
            self.draggroup = findgroup(self._find_top_block(self.spr),
                                       self.block_list)
        else:
            self.draggroup = findgroup(self.spr, self.block_list)
        # check to see if any block ends up with a negative x
        for b in self.draggroup:
            (bx, by) = b.get_xy()
            if bx+dx < 0:
                dx += -(bx+dx)
        # move the stack
        for b in self.draggroup:
            (bx, by) = b.get_xy()
            b.move((bx+dx, by-dy))
        self._snap_to_dock()
        self.draggroup = None


#
# utilities used for checking variable validity
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

