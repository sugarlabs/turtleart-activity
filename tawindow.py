# -*- coding: utf-8 -*-
#Copyright (c) 2007-9, Playful Invention Company.

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

class taWindow: pass

from math import atan2, pi
DEGTOR = 2*pi/360

from tasetup import *
from tasprites import *
from talogo import *
from taturtle import *
from taproject import *
from sugar.graphics.objectchooser import ObjectChooser

#
# Setup
#

def twNew(win, path, lang, tboxh, parent=None):
    tw = taWindow()
    tw.window = win
    tw.path = os.path.join(path,'images')
    tw.path_lang = os.path.join(path,'images',lang)
    tw.load_save_folder = os.path.join(path,'samples',lang)
    tw.save_folder = None
    tw.save_file_name = None
    win.set_flags(gtk.CAN_FOCUS)
    tw.width = gtk.gdk.screen_width()
    tw.height = gtk.gdk.screen_height() - tboxh
    win.set_size_request(tw.width, tw.height)
    if parent is None: win.show_all()
    else: parent.show_all()
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
    tw.area = win.window
    tw.gc = tw.area.new_gc()
    # tw.window.textentry = gtk.Entry()
    # on an OLPC-XO-1, there is a scaling factor
    if os.path.exists('/sys/power/olpc-pm'):
        tw.scale = 1
    else: tw.scale = 1.6
    tw.cm = tw.gc.get_colormap()
    tw.rgb = [255,0,0]
    tw.bgcolor = tw.cm.alloc_color('#fff8de')
    tw.msgcolor = tw.cm.alloc_color('black')
    tw.fgcolor = tw.cm.alloc_color('red')
    tw.textcolor = tw.cm.alloc_color('blue')
    tw.sprites = []
    tw.selected_block = None
    tw.draggroup = None
    prep_selectors(tw)
    tw.myblock = None
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
    if hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
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
    if tw.selected_block!=None: unselect(tw)
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
        tw.activity.projectToolbar.do_hidepalette()
        hide_palette(tw)
    else:
        tw.palette == True
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
        if mask is True:
            newspr = clone_stack(tw,x-spr.x-20,y-spr.y-20, spr)
            tw.dragpos = x-newspr.x,y-newspr.y
            tw.draggroup = findgroup(newspr)
        else:
            tw.draggroup = findgroup(spr)
            for b in tw.draggroup: setlayer(b,2000)
            if spr.connections[0] != None and spr.proto.name == 'lock':
                b = find_top_block(spr)
                tw.dragpos = x-b.x,y-b.y
            else:
                tw.dragpos = x-spr.x,y-spr.y
                disconnect(spr)

def clone_stack(tw,dx,dy,spr):
    newspr = sprNew(tw,spr.x+dx,spr.y+dy,spr.proto.image)
    newspr.type = spr.type
    newspr.proto = spr.proto
    newspr.label = spr.label
    newspr.connections = [None]*len(spr.proto.docks)
    for i in range(1,len(spr.connections)):
        if(spr.connections[i]==None): continue
        clonearg=clone_stack(tw,dx,dy,spr.connections[i])
        newspr.connections[i]=clonearg
        clonearg.connections[0]=newspr
    setlayer(newspr,2000)
    return newspr

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
#    if hasattr(tw.activity, 'chattube')and tw.activity.chattube is not None:
#            tw.activity._send_event("m:"+str(x)+":"+str(y))
    return True

def mouse_move(tw, x, y, verbose=False, mdx=0, mdy=0):
    if verbose:
        print "processing remote mouse move: " + str(x) + " " + str(y)
    if tw.draggroup is None:
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
    # print "deltas are " + str(dx) + " " + str(dy)

#
# Button release
#

def buttonrelease_cb(win, event, tw):
    x,y = xy(event)
    button_release(tw, x, y)
    if hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
        # print "sending release button"
        tw.activity._send_event("r:"+str(x)+":"+str(y))
    return True

def button_release(tw, x, y, verbose=False):
    if tw.dx != 0 or tw.dy != 0 and \
        hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
            if verbose:
                print "processing accumulated move: " + str(tw.dx) + " " + str(tw.dy)
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
                move(tw.select_mask_string, (spr.x-5,spr.y-5))
                setlayer(tw.select_mask_string, 660)
                tw.firstkey = True
            elif spr.proto.name == 'journal':
                import_image(tw, spr)
            elif spr.proto.name == 'audiooff':
                import_audio(tw, spr)
        else: run_stack(tw, spr)

def import_audio(tw, spr):
    chooser = ObjectChooser('Choose audio', None, gtk.DIALOG_MODAL | \
        gtk.DIALOG_DESTROY_WITH_PARENT)
    try:
        result = chooser.run()
        if result == gtk.RESPONSE_ACCEPT:
            dsobject = chooser.get_selected_object()
            if dsobject and dsobject.file_path:               
                spr.ds_id = dsobject.object_id
                setimage(spr,tw.media_shapes['audioon'])
            dsobject.destroy()
    finally:
        chooser.destroy()
        del chooser

def import_image(tw, spr):
#    chooser = ObjectChooser('Choose image', None, gtk.DIALOG_MODAL | \
#        gtk.DIALOG_DESTROY_WITH_PARENT, 'image/png' )
    chooser = ObjectChooser('Choose image', None, gtk.DIALOG_MODAL | \
        gtk.DIALOG_DESTROY_WITH_PARENT)
    try:
        result = chooser.run()
        if result == gtk.RESPONSE_ACCEPT:
            dsobject = chooser.get_selected_object()
            load_image(tw, dsobject, spr)
            spr.ds_id = dsobject.object_id
            dsobject.destroy()
    finally:
        chooser.destroy()
        del chooser

def load_image(tw, picture, spr):
    from talogo import get_pixbuf_from_journal
    pixbuf = get_pixbuf_from_journal(picture,spr.width,spr.height)
    if pixbuf is not None:
        setimage(spr, pixbuf)
    else:
        setimage(spr, tw.media_shapes['texton'])

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
        if block1.proto.name in ('write', 'push', 'plus2', 'equal', \
            'template1', 'template2', 'template3', 'template4', \
            'template6', 'template7', 'nop'):
            if block1.proto.name == 'write' and d1type == 'string':
                if d2type == 'num' or d2type == 'string':
                    pass
            else: 
                if d2type == 'num' or d2type == 'string':
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
    results = key_press(tw, event.get_state()&gtk.gdk.MOD4_MASK, keyname)
#    keyname = unichr(gtk.gdk.keyval_to_unicode(event.keyval))
    if keyname is not None and \
        hasattr(tw.activity, 'chattube') and tw.activity.chattube is not None:
        # print "key press"
        if event.get_state()&gtk.gdk.MOD4_MASK:
            tw.activity._send_event("k:"+'T'+":"+keyname)
        else:
            tw.activity._send_event("k:"+'F'+":"+keyname)
    return results

def key_press(tw, mask, keyname, verbose=False):
    if keyname is None:
        return False
    if verbose:
        print "processing remote key press: " + keyname
    tw.keypress = keyname
    if mask is True:
        if keyname=="n": new_project(tw)
        if keyname=="o": load_file(tw)
        if keyname=="s": save_file(tw)
        if keyname=="k": tw.activity.clear_journal()
        if keyname=="i": 
            tw.activity.waiting_for_blocks = True
            tw.activity._send_event("i") # request sync for sharing
        return True
    if tw.selected_block==None:
        if keyname=="i": 
            tw.activity.waiting_for_blocks = True
            tw.activity._send_event("i") # request sync for sharing
        elif keyname=="p":
            if tw.palette is True:
                hideshow_palette(tw,False)
            else:
                hideshow_palette(tw,True)
        elif keyname=="b":
            if tw.hide == False:
                tw.activity.projectToolbar.do_hide()
            else:
                tw.activity.projectToolbar.do_show()
            hideshow_button(tw)
        elif keyname=="r":
            runbutton(tw, 0)
        elif keyname=="w":
            runbutton(tw, 3)
        elif keyname=="s":
            stop_button(tw)
        elif keyname=="e":
            eraser_button(tw)
        return False
    # if and when we use unichr above
    # we need to change this logic (and logic in talogo.py)
    if tw.selected_block.proto.name == 'number':
        if keyname in ['minus', 'period']: 
            keyname = {'minus': '-', 'period': '.'}[keyname]
        if len(keyname)>1:
            return True
    else:
        try: 
            keyname = {
'aacute': 'á', 'Aacute': 'Á', 'acircumflex': 'â', 'Acircumflex': 'Â', \
'adiaeresis': 'ä', 'Adiaeresis': 'Ä', 'ae': 'æ', 'AE': 'Æ', 'agrave': \
'à', 'Agrave': 'À', 'ampersand': '&', 'apostrophe': '\'', 'aring': \
'å', 'Aring': 'Å', 'asciicircum': '^', 'asciitilde': '~', 'asterisk': \
'*', 'at': '@', 'Atilde': 'Â', 'atilde': 'ã', 'backslash': '\\', \
'bar': '|', 'braceleft': '{', 'braceright': '}', 'bracketleft': '[', \
'bracketright': ']', 'ccedilla': 'ç', 'Ccedilla': 'Ç', 'colon': ':', \
'comma': ',', 'dollar': '$', 'eacute': 'é', 'Eacute': 'É', \
'ecircumflex': 'ê', 'Ecircumflex': 'Ê', 'egrave': 'è', 'Egrave': 'È', \
'eng': 'ŋ', 'ENG': 'Ŋ', 'equal': '=', 'eth': 'ð', 'ETH': 'Ð', \
'EuroSign': '€', 'exclam': '!', 'exclamdown': '¡', 'gbreve': 'ğ', \
'Gbreve': 'Ğ', 'grave': '`', 'greater': '>', 'guillemnotleft': '«', \
'guillemotright': '»', 'Iabovedot': 'İ', 'iacute': 'í', 'Iacute': 'Í', \
'icircumflex': 'î', 'Icircumflex': 'Î', 'idotless': 'ı', 'igrave': \
'ì', 'Igrave': 'Ì', 'less': '<', 'minus': '-', 'mu': 'µ', 'ntilde': \
'ñ', 'Ntilde': 'Ñ', 'numbersign': '#', 'oacute': 'ó', 'Oacute': 'Ó', \
'ocircumflex': 'ô', 'Ocircumflex': 'Ô', 'odiaeresis': '', \
'Odiaeresis': 'Ö', 'oe': 'œ', 'OE': 'Œ', 'ograve': 'ò', 'Ograve': 'Ò', \
'Ooblique': 'Ø', 'oslash': 'ø', 'parenleft': '(', 'parenright': ')', \
'percent': '%', 'period': '.', 'plus': '+', 'question': '?', \
'questiondown': '¿', 'quotedbl': '\"', 'scedilla': 'ş', 'Scedilla': \
'Ş', 'schwa': 'ə', 'SCHWA': 'Ə', 'semicolon': ';', 'slash': '/', \
'space': ' ', 'ssharp': 'ß', 'sterling': '£', 'thorn': 'þ', 'THO': \
'Þ', 'uacute': 'ú', 'Uacute': 'Ú', 'ucircumflex': 'û', 'Ucircumflex': \
'Û', 'ugrave': '', 'Ugrave': 'Ù', 'underscore': '_', 'ydiaeresis': \
'ÿ', 'Cyrillic_ie': 'є', 'Cyrillic_IE': 'Е', 'Cyrillic_shcha': 'щ', \
'Cyrillic_SHCHA': 'Щ', 'Cyrillic_ef': 'ф', 'Cyrillic_EF': 'Ф', \
'Cyrillic_tse': 'ц', 'Cyrillic_TSE': 'Ц', 'Cyrillic_u': 'у', \
'Cyrillic_U': 'У', 'Cyrillic_zhe': 'ж', 'Cyrillic_ZHE': 'Ж', \
'Cyrillic_e': 'э', 'Cyrillic_E': 'Э', 'Cyrillic_en': 'н', \
'Cyrillic_EN': 'Н', 'Cyrillic_ghe': 'г', 'Cyrillic_GHE': 'Г', \
'Cyrillic_sha': 'ш', 'Cyrillic_SHA': 'Ш', 'Cyrillic_u_straight': \
'ү','Cyrillic_U_straight': 'Ү', 'Cyrillic_ze': 'з', 'Cyrillic_ZE': \
'З', 'Cyrillic_ka': 'к', 'Cyrillic_KA': 'К', 'Cyrillic_hardsign': 'ъ', \
'Cyrillic_HARDSIGN': 'Ъ', 'Cyrillic_shorti': 'й', 'Cyrillic_SHORTI': \
'Й', 'Cyrillic_yeru': 'ы', 'Cyrillic_YERU': 'Ы', 'Cyrillic_be': 'б', \
'Cyrillic_BE': 'Б', 'Cyrillic_o_bar': 'ө', 'Cyrillic_O_bar': 'Ө', \
'Cyrillic_a': 'а', 'Cyrillic_A': 'А', 'Cyrillic_ha': 'х', \
'Cyrillic_HA': 'Х', 'Cyrillic_er': 'р', 'Cyrillic_ER': 'Р', \
'Cyrillic_o': 'о', 'Cyrillic_O': 'О', 'Cyrillic_el': 'л', \
'Cyrillic_EL': 'Л', 'Cyrillic_de': 'д', 'Cyrillic_DE': 'Д', \
'Cyrillic_pe': 'п', 'Cyrillic_PE': 'П', 'Cyrillic_ya': 'я', \
'Cyrillic_YA': 'Я', 'Cyrillic_che': 'ч', 'Cyrillic_CHE': 'Ч', \
'Cyrillic_io': 'ё', 'Cyrillic_IO': 'Ё', 'Cyrillic_es': 'с', \
'Cyrillic_ES': 'С', 'Cyrillic_em': 'м', 'Cyrillic_EM': 'М', \
'Cyrillic_i': 'и', 'Cyrillic_I': 'И', 'Cyrillic_te': 'т', \
'Cyrillic_TE': 'Т', 'Cyrillic_softsign': 'ь', 'Cyrillic_SOFTSIGN': \
'Ь', 'Cyrillic_ve': 'в', 'Cyrillic_VE': 'В', 'Cyrillic_yu': 'ю', \
'Cyrillic_YU': 'Ю', 'KP_Up': '↑', 'KP_Down': '↓', 'KP_Left': '←', \
'KP_Right': '→'}[keyname]
        except:
            if len(keyname)>1:
                return True

    oldnum = tw.selected_block.label 
    selblock=tw.selected_block.proto
    if tw.firstkey: newnum = selblock.check( \
        keyname,tw.defdict[selblock.name])
    else: newnum = oldnum+keyname
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
    clear(tw.lc)

def stop_button(tw):
    stop_logo(tw)

def runbutton(tw, time):
    print "you better run, turtle, run!!"
    # look for the start block
    for b in blocks(tw):
        if find_start_stack(tw, b):
            tw.step_time = time
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


