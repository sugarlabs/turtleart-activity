# -*- coding: utf-8 -*-
#Copyright (c) 2007, Playful Invention Company
#Copyright (c) 2008-9, Walter Bendera
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

import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject
import os
import os.path
import time

# Import from Journal for these blocks 
importblocks = ['audiooff', 'descriptionoff','journal']

class taWindow: pass

from math import atan2, pi
DEGTOR = 2*pi/360

from tasetup import *
from tasprites import *
from talogo import *
from taturtle import *
from taproject import *
try:
    from sugar.graphics.objectchooser import ObjectChooser
except:
    pass

from tahoverhelp import *
from gettext import gettext as _

# dead key dictionaries
dead_grave = {'A':192,'E':200,'I':204,'O':210,'U':217,'a':224,'e':232,'i':236,\
              'o':242,'u':249}
dead_acute = {'A':193,'E':201,'I':205,'O':211,'U':218,'a':225,'e':233,'i':237,\
              'o':243,'u':250}
dead_circumflex = {'A':194,'E':202,'I':206,'O':212,'U':219,'a':226,'e':234,\
                   'i':238,'o':244,'u':251}
dead_tilde = {'A':195,'O':211,'N':209,'U':360,'a':227,'o':245,'n':241,'u':361}
dead_diaeresis = {'A':196,'E':203,'I':207,'O':211,'U':218,'a':228,'e':235,\
                  'i':239,'o':245,'u':252}
dead_abovering = {'A':197,'a':229}

# Time out for triggering help
timeout_tag = [0]


#
# Setup
#

def twNew(win, path, lang, parent=None):
    tw = taWindow()
    tw.window = win
    tw.path = os.path.join(path,'images')
    tw.path_lang = os.path.join(path,'images',lang)
    tw.path_en = os.path.join(path,'images/en') # en as fallback
    tw.load_save_folder = os.path.join(path,'samples')
    tw.save_folder = None
    tw.save_file_name = None
    win.set_flags(gtk.CAN_FOCUS)
    tw.width = gtk.gdk.screen_width()
    tw.height = gtk.gdk.screen_height() 
    # starting from command line
    if parent is None:
        win.set_size_request(tw.width, tw.height)
        win.show_all()
    # starting from Sugar
    else:
        parent.show_all()
    win.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    win.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
    win.add_events(gtk.gdk.POINTER_MOTION_MASK)
    win.add_events(gtk.gdk.KEY_PRESS_MASK)
    win.connect("expose-event", expose_cb, tw)
    win.connect("button-press-event", buttonpress_cb, tw)
    win.connect("button-release-event", buttonrelease_cb, tw)
    win.connect("motion-notify-event", move_cb, tw)
    win.connect("key_press_event", keypress_cb, tw)
    tw.keypress = ""
    tw.keyvalue = 0
    tw.dead_key = ""
    tw.area = win.window
    tw.gc = tw.area.new_gc()
    # tw.window.textentry = gtk.Entry()
    # on an OLPC-XO-1, there is a scaling factor
    if os.path.exists('/sys/power/olpc-pm'):
        tw.lead = 1.6
        tw.scale = 1.0
    else:
        tw.lead = 1.0
        tw.scale = 1.6
    tw.cm = tw.gc.get_colormap()
    tw.rgb = [255,0,0]
    tw.bgcolor = tw.cm.alloc_color('#fff8de')
    tw.msgcolor = tw.cm.alloc_color('black')
    tw.fgcolor = tw.cm.alloc_color('red')
    tw.textcolor = tw.cm.alloc_color('blue')
    tw.textsize = 32
    tw.sprites = []
    tw.selected_block = None
    tw.draggroup = None
    prep_selectors(tw)
    tw.myblock = None
    tw.nop = 'nop'
    tw.loaded = 0
    for s in selectors:
        setup_selectors(tw,s)
    setup_misc(tw)
    tw.step_time = 0
    tw.hide = False
    tw.palette = True
    select_category(tw, tw.selbuttons[0])
    tw.turtle = tNew(tw,tw.width,tw.height)
    tw.lc = lcNew(tw)
    tw.buddies = []
    tw.dx = 0
    tw.dy = 0
    return tw

#
# Button Press
#

def buttonpress_cb(win, event, tw):
    win.grab_focus()
    x, y = xy(event)
    button_press(tw, event.get_state()&gtk.gdk.CONTROL_MASK, x, y)
    # if sharing, send button press
    if hasattr(tw, 'activity') and \
        hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
        # print "sending button pressed"
        if event.get_state()&gtk.gdk.CONTROL_MASK is True:
            tw.activity._send_event("p:"+str(x)+":"+str(y)+":"+'T')
        else:
            tw.activity._send_event("p:"+str(x)+":"+str(y)+":"+'F')
    return True

def button_press(tw, mask, x, y, verbose=False):
    if verbose:
        print "processing remote button press: " + str(x) + " " + str(y)
    tw.block_operation = 'click'
    if tw.selected_block!=None:
        unselect(tw)
    # hide status block
    setlayer(tw.status_spr,400)
    spr = findsprite(tw,(x,y))
    tw.dx = 0
    tw.dy = 0
    if spr is None:
        # print "no spr found"
        return True
    if spr.type == 'selbutton':
        select_category(tw,spr)
    elif spr.type == 'category':
        block_selector_pressed(tw,x,y)
    elif spr.type == 'block':
        block_pressed(tw,mask,x,y,spr)
    elif spr.type == 'turtle':
        turtle_pressed(tw,x,y)

def block_selector_pressed(tw,x,y):
    proto = get_proto_from_category(tw,x,y)
    if proto==None:
        return
    if proto!='hide':
        new_block_from_category(tw,proto,x,y)
    else:
        hideshow_palette(tw,False)

def hideshow_palette(tw,state):
    if state is False:
        tw.palette == False
        if hasattr(tw,'activity'):
            try:
                # Use new toolbar design
                tw.activity.do_hidepalette()
            except:
                # Use old toolbar design
                tw.activity.projectToolbar.do_hidepalette()                
        hide_palette(tw)
    else:
        tw.palette == True
        if hasattr(tw,'activity'):
            try:
                # Use new toolbar design
                tw.activity.do_showpalette()
            except:
                # Use old toolbar design
                tw.activity.projectToolbar.do_showpalette()                
        show_palette(tw)

def show_palette(tw):
    for i in tw.selbuttons: setlayer(i,800)
    select_category(tw,tw.selbuttons[0])
    tw.palette = True

def hide_palette(tw):
    for i in tw.selbuttons: hide(i)
    setshape(tw.category_spr, tw.hidden_palette_icon)
    tw.palette = False

def get_proto_from_category(tw,x,y):
    dx,dy = x-tw.category_spr.x, y-tw.category_spr.y,
    pixel = getpixel(tw.current_category.mask,dx,dy)
    index = ((pixel%256)>>3)-1
    if index==0:
        return 'hide'
    index-=1
    if index>len(tw.current_category.blockprotos):
        return None
    return tw.current_category.blockprotos[index]

def select_category(tw, spr):
    if hasattr(tw, 'current_category'):
        setshape(tw.current_category, tw.current_category.offshape)
    setshape(spr, spr.onshape)
    tw.current_category = spr
    setshape(tw.category_spr,spr.group)

def new_block_from_category(tw,proto,x,y):
    if proto is None:
        return True
    # load alternative image of nop block if python code is loaded
    if proto.name == 'nop' and tw.nop == 'pythonloaded':
        newspr = sprNew(tw,x-20,y-20,tw.media_shapes['pythonloaded'])
    else:
        newspr = sprNew(tw,x-20,y-20,proto.image)
    setlayer(newspr,2000)
    tw.dragpos = 20,20
    newspr.type = 'block'
    newspr.proto = proto
    if tw.defdict.has_key(newspr.proto.name):
        newspr.label=tw.defdict[newspr.proto.name]
    newspr.connections = [None]*len(proto.docks)
    for i in range(len(proto.defaults)):
        dock = proto.docks[i+1]
        argproto = tw.protodict[tw.valdict[dock[0]]]
        argdock = argproto.docks[0]
        nx,ny = newspr.x+dock[2]-argdock[2],newspr.y+dock[3]-argdock[3]
        argspr = sprNew(tw,nx,ny,argproto.image)
        argspr.type = 'block'
        argspr.proto = argproto
        argspr.label = str(proto.defaults[i])
        setlayer(argspr,2000)
        argspr.connections = [newspr,None]
        newspr.connections[i+1] = argspr
    tw.draggroup = findgroup(newspr)
    tw.block_operation = 'new'

def block_pressed(tw,mask,x,y,spr):
    if spr is not None:
        tw.draggroup = findgroup(spr)
        for b in tw.draggroup: setlayer(b,2000)
        if spr.connections[0] != None and spr.proto.name == 'lock':
            b = find_top_block(spr)
            tw.dragpos = x-b.x,y-b.y
        else:
            tw.dragpos = x-spr.x,y-spr.y
            disconnect(spr)

def turtle_pressed(tw,x,y):
    dx,dy = x-tw.turtle.spr.x-30,y-tw.turtle.spr.y-30
    if dx*dx+dy*dy > 200:
        tw.dragpos = ('turn', \
        tw.turtle.heading-atan2(dy,dx)/DEGTOR,0)
    else:
        tw.dragpos = ('move', x-tw.turtle.spr.x,y-tw.turtle.spr.y)
    tw.draggroup = [tw.turtle.spr]

#
# Mouse move
#

def move_cb(win, event, tw):
    x,y = xy(event)
    mouse_move(tw, x, y)
    return True

def mouse_move(tw, x, y, verbose=False, mdx=0, mdy=0):
    if verbose:
        print "processing remote mouse move: " + str(x) + " " + str(y)
    if tw.draggroup is None:
        # popup help from RGS
        spr = findsprite(tw,(x,y))
        if spr and spr.type == 'category':
            proto = get_proto_from_category(tw,x,y)
            if proto and proto!='hide':
                if timeout_tag[0] == 0:
                    timeout_tag[0] = showPopup(proto.name,tw)
                    return
            else:
                if timeout_tag[0] > 0:
                    try:
                        gobject.source_remove(timeout_tag[0])
                        timeout_tag[0] = 0
                    except:
                        timeout_tag[0] = 0
        elif spr and spr.type == 'selbutton':
            if timeout_tag[0] == 0:
                timeout_tag[0] = showPopup(spr.name,tw)
            else:
                if timeout_tag[0] > 0:
                    try:
                        gobject.source_remove(timeout_tag[0])
                        timeout_tag[0] = 0
                    except:
                        timeout_tag[0] = 0
        else:
            if timeout_tag[0] > 0:
                try:
                    gobject.source_remove(timeout_tag[0])
                    timeout_tag[0] = 0
                except:
                    timeout_tag[0] = 0
        return
    tw.block_operation = 'move'
    spr = tw.draggroup[0]
    if spr.type=='block':
        dragx, dragy = tw.dragpos
        if mdx != 0 or mdy != 0:
            dx,dy = mdx,mdy
        else:
            dx,dy = x-dragx-spr.x,y-dragy-spr.y
        # skip if there was a move of 0,0
        if dx == 0 and dy == 0:
            return
        # drag entire stack if moving lock block
        if spr.proto.name == 'lock':
            tw.draggroup = findgroup(find_top_block(spr))
        else:
            tw.draggroup = findgroup(spr)
        for b in tw.draggroup:
            move(b,(b.x+dx, b.y+dy))
    elif spr.type=='turtle':
        type,dragx,dragy = tw.dragpos
        if type == 'move':
            if mdx != 0 or mdy != 0:
                dx,dy = mdx,mdy
            else:
                dx,dy = x-dragx-spr.x,y-dragy-spr.y
            move(spr, (spr.x+dx, spr.y+dy))
        else:
            if mdx != 0 or mdy != 0:
                dx,dy = mdx,mdy
            else:
                dx,dy = x-spr.x-30,y-spr.y-30
            seth(tw.turtle, int(dragx+atan2(dy,dx)/DEGTOR+5)/10*10)
    if mdx != 0 or mdy != 0:
        dx,dy = 0,0
    else:
        tw.dx += dx
        tw.dy += dy

#
# Button release
#

def buttonrelease_cb(win, event, tw):
    x,y = xy(event)
    button_release(tw, x, y)
    if hasattr(tw, 'activity') and \
        hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
        # print "sending release button"
        tw.activity._send_event("r:"+str(x)+":"+str(y))
    return True

def button_release(tw, x, y, verbose=False):
    if tw.dx != 0 or tw.dy != 0:
        if hasattr(tw, 'activity') and \
            hasattr(tw.activity, 'chattube') and \
            tw.activity.chattube is not None:
                if verbose:
                    print "processing move: " + str(tw.dx) + " " + str(tw.dy)
                tw.activity._send_event("m:"+str(tw.dx)+":"+str(tw.dy))
                tw.dx = 0
                tw.dy = 0
    if verbose:
        print "processing remote button release: " + str(x) + " " + str(y)
    if tw.draggroup == None: 
        return
    spr = tw.draggroup[0]
    if spr.type == 'turtle':
        tw.turtle.xcor = tw.turtle.spr.x-tw.turtle.canvas.x- \
            tw.turtle.canvas.width/2+30
        tw.turtle.ycor = tw.turtle.canvas.height/2-tw.turtle.spr.y+ \
            tw.turtle.canvas.y-30
        move_turtle(tw.turtle)
        tw.draggroup = None
        return
    if tw.block_operation=='move' and hit(tw.category_spr, (x,y)):
        for b in tw.draggroup: hide(b)
        tw.draggroup = None
        return
    if tw.block_operation=='new':
        for b in tw.draggroup:
            move(b, (b.x+200, b.y))
    snap_to_dock(tw)
    for b in tw.draggroup: setlayer(b,650)
    tw.draggroup = None
    if tw.block_operation=='click':
        if spr.proto.name=='number':
            tw.selected_block = spr
            move(tw.select_mask, (spr.x-5,spr.y-5))
            setlayer(tw.select_mask, 660)
            tw.firstkey = True
        elif tw.defdict.has_key(spr.proto.name):
            tw.selected_block = spr
            if spr.proto.name=='string':
                # entry = gtk.Entry()
                move(tw.select_mask_string, (spr.x-5,spr.y-5))
                setlayer(tw.select_mask_string, 660)
                tw.firstkey = True
            elif spr.proto.name in importblocks:
                import_from_journal(tw, spr)
        else: run_stack(tw, spr)

def import_from_journal(tw, spr):
    chooser = ObjectChooser('Choose image', None, gtk.DIALOG_MODAL | \
        gtk.DIALOG_DESTROY_WITH_PARENT)
    try:
        result = chooser.run()
        if result == gtk.RESPONSE_ACCEPT:
            dsobject = chooser.get_selected_object()
            # change block graphic to indicate that object is "loaded"
            if spr.proto.name == 'journal':
                load_image(tw, dsobject, spr)
            elif spr.proto.name == 'audiooff':
                setimage(spr,tw.media_shapes['audioon'])
            else:
                setimage(spr, tw.media_shapes['decson'])
            spr.ds_id = dsobject.object_id
            dsobject.destroy()
    finally:
        chooser.destroy()
        del chooser

# Replace Journal block graphic with preview image
def load_image(tw, picture, spr):
    from talogo import get_pixbuf_from_journal
    pixbuf = get_pixbuf_from_journal(picture,spr.width,spr.height)
    if pixbuf is not None:
        setimage(spr, pixbuf)
    else:
        setimage(spr, tw.media_shapes['texton'])

# change the icon for user-defined blocks after Python code is loaded
def set_userdefined(tw):
    list = tw.sprites[:]
    for spr in list:
        if hasattr(spr,'proto') and spr.proto.name == 'nop':
            setimage(spr,tw.media_shapes['pythonloaded'])
    tw.nop = 'pythonloaded'

def snap_to_dock(tw):
    d=200
    me = tw.draggroup[0]
    for mydockn in range(len(me.proto.docks)):
        for you in blocks(tw):
            if you in tw.draggroup:
                continue
            for yourdockn in range(len(you.proto.docks)):
                thisxy = dock_dx_dy(you,yourdockn,me,mydockn)
                if magnitude(thisxy)>d:
                    continue
                d=magnitude(thisxy)
                bestxy=thisxy
                bestyou=you
                bestyourdockn=yourdockn
                bestmydockn=mydockn
    if d<200:
        for b in tw.draggroup:
            move(b,(b.x+bestxy[0],b.y+bestxy[1]))
        blockindock=bestyou.connections[bestyourdockn]
        if blockindock!=None:
            for b in findgroup(blockindock):
                hide(b)
        bestyou.connections[bestyourdockn]=me
        me.connections[bestmydockn]=bestyou

def dock_dx_dy(block1,dock1n,block2,dock2n):
    dock1 = block1.proto.docks[dock1n]
    dock2 = block2.proto.docks[dock2n]
    d1type,d1dir,d1x,d1y=dock1[0:4]
    d2type,d2dir,d2x,d2y=dock2[0:4]
    if (d2type!='num') or (dock2n!=0):
        if block1.connections[dock1n] != None:
            return (100,100)
        if block2.connections[dock2n] != None:
            return (100,100)
    if block1==block2: return (100,100)
    if d1type!=d2type:
        # some blocks can take strings or nums
        if block1.proto.name in ('write', 'plus2', 'equal', 'less', 'greater', \
                                 'template1', 'template2', 'template3', \
                                 'template4', 'template6', 'template7', 'nop', \
                                 'print', 'stack'):
            if block1.proto.name == 'write' and d1type == 'string':
                if d2type == 'num' or d2type == 'string':
                    pass
            else: 
                if d2type == 'num' or d2type == 'string':
                    pass
        # some blocks can take strings, nums, or Journal
        elif block1.proto.name in ('show', 'push', 'storein', 'storeinbox1', \
                                   'storeinbox2'):
            if d2type == 'num' or d2type == 'string' or d2type == 'journal':
                pass
        # some blocks can take media, audio, movies, of descriptions
        elif block1.proto.name in ('containter'):
            if d1type == 'audiooff' or d1type == 'journal':
                pass
        else:
            return (100,100)
    if d1dir==d2dir:
        return (100,100)
    return (block1.x+d1x)-(block2.x+d2x),(block1.y+d1y)-(block2.y+d2y)

def magnitude(pos):
    x,y = pos
    return x*x+y*y

#
# Repaint
#

def expose_cb(win, event, tw):
    redrawsprites(tw)
    return True

#
# Keyboard
#

def keypress_cb(area, event, tw):
    keyname = gtk.gdk.keyval_name(event.keyval)
#    keyunicode = unichr(gtk.gdk.keyval_to_unicode(event.keyval)).replace("\x00","")
    keyunicode = gtk.gdk.keyval_to_unicode(event.keyval)
#    print keyname
#    if keyunicode > 0:
#        print unichr(keyunicode)

    if event.get_state()&gtk.gdk.MOD1_MASK:
        alt_mask = True
    else:
        alt_mask = False
    results = key_press(tw, alt_mask, keyname, keyunicode)
    if keyname is not None and hasattr(tw,"activity") and \
        hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
        # print "key press"
        if alt_mask:
            tw.activity._send_event("k:"+'T'+":"+keyname+":"+str(keyunicode))
        else:
            tw.activity._send_event("k:"+'F'+":"+keyname+":"+str(keyunicode))
    return keyname
'''
    if len(keyname)>1:
        # print "(" + keyunicode.encode("utf-8") + ")"
        return keyname
    else:
        # print "[" + keyunicode.encode("utf-8") + "]"
        return keyunicode.encode("utf-8")
'''
def key_press(tw, alt_mask, keyname, keyunicode, verbose=False):
    if keyname is None:
        return False
    if verbose:
        print "processing remote key press: " + keyname
    tw.keypress = keyname
    if alt_mask is True and tw.selected_block==None:
        if keyname=="i" and hasattr(tw, 'activity'):
            tw.activity.waiting_for_blocks = True
            tw.activity._send_event("i") # request sync for sharing
        elif keyname=="p":
            hideshow_button(tw)
        elif keyname=='q':
            exit()
        return True
    if tw.selected_block==None:
        return False
    if tw.selected_block.proto.name == 'number':
        if keyname in ['minus', 'period']: 
            keyname = {'minus': '-', 'period': '.'}[keyname]
        if len(keyname)>1:
            return True
    else: # gtk.keysyms.Left ...
        if keyname in ['Escape', 'Return', \
                       'KP_Up', 'KP_Down', 'KP_Left', 'KP_Right']:
            return True
    if keyname in ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock', \
                   'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift']:
        keyname = ''
        keyunicode = 0
    # Hack until I sort out input and unicode + dead keys
    if keyname[0:5] == 'dead_':
        tw.dead_key = keyname
        keyname = ''
        keyunicode = 0
    if keyname == 'Tab':
        keyunicode = 32 # substitute a space for a tab
    oldnum = tw.selected_block.label 
    selblock=tw.selected_block.proto
    if keyname == 'BackSpace':
        if len(oldnum) > 1:
            newnum = oldnum[:len(oldnum)-1]
        else:
            newnum = ''
        setlabel(tw.selected_block, selblock.check(newnum,oldnum))
        if len(newnum) > 0:
            tw.firstkey = False
    elif keyname is not '':
        # Hack until I sort out input and unicode + dead keys
        if tw.dead_key == 'dead_grave':
            keyunicode = dead_grave[keyname]
        elif tw.dead_key == 'dead_acute':
            keyunicode = dead_acute[keyname]
        elif tw.dead_key == 'dead_circumflex':
            keyunicode = dead_circumflex[keyname]
        elif tw.dead_key == 'dead_tilde':
            keyunicode = dead_tilde[keyname]
        elif tw.dead_key == 'dead_diaeresis':
            keyunicode = dead_diaeresis[keyname]
        elif tw.dead_key == 'dead_abovering':
            keyunicode = dead_abovering[keyname]
        tw.dead_key = ""
        if tw.firstkey:
            newnum = selblock.check(unichr(keyunicode), \
                                    tw.defdict[selblock.name])
        elif keyunicode > 0:
            if unichr(keyunicode) is not '\x00':
                newnum = oldnum+unichr(keyunicode)
            else:
                newnum = oldnum
        else:
            newnum = ""
        setlabel(tw.selected_block, selblock.check(newnum,oldnum))
        tw.firstkey = False
    return True

def unselect(tw):
    if tw.selected_block.label in ['-', '.', '-.']:
        select_block.setlabel('0')
    hide(tw.select_mask)
    hide(tw.select_mask_string)
    tw.selected_block = None

#
# Block utilities
#

def disconnect(b):
    if b.connections[0]==None:
        return
    b2=b.connections[0]
    b2.connections[b2.connections.index(b)] = None
    b.connections[0] = None

def run_stack(tw,spr):
    tw.lc.ag = None
    top = find_top_block(spr)
    run_blocks(tw.lc, top, blocks(tw), True)
    gobject.idle_add(doevalstep, tw.lc)

def findgroup(b):
    group=[b]
    for b2 in b.connections[1:]:
        if b2!=None: group.extend(findgroup(b2))
    return group

def find_top_block(spr):
    b = spr
    while b.connections[0]!=None:
        b=b.connections[0]
    return b

def runtool(tw, spr, cmd, *args):
    cmd(*(args))

def eraser_button(tw):
    # hide status block
    setlayer(tw.status_spr,400)
    clear(tw.lc)

def stop_button(tw):
    stop_logo(tw)

def runbutton(tw, time):
    print "you better run, turtle, run!!"
    # look for the start block
    for b in blocks(tw):
        if find_start_stack(tw, b):
            tw.step_time = time
            if hasattr(tw,'activity'):
                tw.activity.recenter()
            run_stack(tw, b)
            return
    # no start block, so run a stack that isn't a hat
    for b in blocks(tw):
        if find_block_to_run(tw, b):
            print "running " + b.proto.name
            tw.step_time = time
            run_stack(tw, b)
    return

def hideshow_button(tw):
    if tw.hide is False:
        for b in blocks(tw): setlayer(b,100)
        hide_palette(tw)
        hide(tw.select_mask)
        hide(tw.select_mask_string)
        tw.hide = True
    else:
        for b in blocks(tw): setlayer(b,650)
        show_palette(tw)
        tw.hide = False
    inval(tw.turtle.canvas)

# find start stack
def find_start_stack(tw, spr):
    top = find_top_block(spr)
    if spr.proto.name == 'start':
        return True
    else:
        return False

# find a stack to run (any stack without a hat)
def find_block_to_run(tw, spr):
    top = find_top_block(spr)
    if spr == top and spr.proto.name[0:3] != 'hat':
        return True
    else:
        return False

def blocks(tw):
    return [spr for spr in tw.sprites if spr.type == 'block']

def xy(event):
    return map(int, event.get_coords())

def showPopup(block_name,tw):
    if hasattr(tw,"activity"):
        if block_name in blocks_dict:
            block_name_s = _(blocks_dict[block_name])
        else:
            block_name_s = _(block_name)
        
        try:
            label = block_name_s + ": " + hover_dict[block_name]
        except:
            label = block_name_s
        try:
            # Use new toolbar
            tw.activity.hover_help_label.set_text(label)
            tw.activity.hover_help_label.show()
        except:
            # Use old toolbar
            tw.activity.helpToolbar.hover_help_label.set_text(label)
            tw.activity.helpToolbar.hover_help_label.show()
    return 0
