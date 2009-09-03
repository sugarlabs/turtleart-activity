# -*- coding: utf-8 -*-

#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-9, Walter Bender

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
import pango
class taSprite: pass

# Don't display the label for these blocks 
nolabel = ['audiooff', 'descriptionoff','journal']

def findsprite(tw,pos):
    list = tw.sprites[:]
    list.reverse()
    for s in list:
        if hit(s,pos): return s
    return None

def redrawsprites(tw):
    for s in tw.sprites: draw(s)

def sprNew(tw,x,y,image,altlabel=False):
    spr = taSprite()
    spr.tw, spr.x, spr.y = tw,x,y
    setimage(spr,image)
    spr.label = None
    spr.ds_id = None
    if altlabel:
        spr.draw_label = draw_label2
    else: spr.draw_label = draw_label1
    return spr

def setimage(spr,image):
    spr.image = image
    if isinstance(image,gtk.gdk.Pixbuf):
        spr.width = image.get_width()
        spr.height = image.get_height()
    else: spr.width,spr.height=image.get_size()

def move(spr,pos):
    inval(spr)
    spr.x,spr.y = pos
    inval(spr)

def setshape(spr,image):
    inval(spr)
    setimage(spr,image)
    inval(spr)

def setshapex(spr):
    inval(spr)

def setlayer(spr, layer):
    sprites = spr.tw.sprites
    if spr in sprites: sprites.remove(spr)
    spr.layer = layer
    for i in range(len(sprites)):
        if layer < sprites[i].layer:
            sprites.insert(i, spr)
            inval(spr)
            return
    sprites.append(spr)
    inval(spr)

def hide(spr):
    if spr not in spr.tw.sprites: return
    inval(spr)
    spr.tw.sprites.remove(spr)

def setlabel(spr,label):
    spr.label = label
    inval(spr)

def inval(spr):
    spr.tw.area.invalidate_rect(gtk.gdk.Rectangle(spr.x,spr.y,spr.width, \
                                                  spr.height), False)

def draw(spr):
    if isinstance(spr.image,gtk.gdk.Pixbuf):
        spr.tw.area.draw_pixbuf(spr.tw.gc, spr.image, 0, 0, spr.x, spr.y)
    else:
        spr.tw.area.draw_drawable(spr.tw.gc,spr.image,0,0,spr.x,spr.y,-1,-1)
    if spr.label!=None:
        if hasattr(spr, 'proto') and hasattr(spr.proto, 'name'):
            name = spr.proto.name
        else:
            name = ""
        if name not in nolabel:
            spr.draw_label(spr,str(spr.label))

def hit(spr,pos):
    x,y = pos
    if x<spr.x: return False
    if x>spr.x+spr.width: return False
    if y<spr.y: return False
    if y>spr.y+spr.height: return False
    if isinstance(spr.image,gtk.gdk.Pixmap): return True
    if hasattr(spr, 'proto') and hasattr(spr.proto, 'name') and \
        spr.proto.name == 'journal':
            return True
    dx,dy = x-spr.x, y-spr.y
    try:
        return ord(spr.image.get_pixels()[(dy*spr.width+dx)*4+3]) == 255
    except IndexError:
        if hasattr(spr, 'proto') and hasattr(spr.proto, 'name'):
            print spr.proto.name
        print "IndexError: string index out of range" + str(dx) + " " \
            + str(dy) + " " + str(spr.width) + " " + str(spr.height)
        return True

def draw_label(spr, label, myscale, center_flag, truncate_flag):
    fd = pango.FontDescription('Sans')
    fd.set_size(int(myscale*spr.tw.scale*pango.SCALE))
    if type(label) == str or type(label) == unicode:
        mylabel = label.replace("\0"," ")
        l = len(mylabel)
        if truncate_flag and l > 8:
            pl = spr.tw.window.create_pango_layout("..."+mylabel[l-8:])
        else:
            pl = spr.tw.window.create_pango_layout(mylabel)
        pl.set_font_description(fd)
        if center_flag:
            swidth = pl.get_size()[0]/pango.SCALE
            centerx = spr.x+spr.width/2
            x = int(centerx-swidth/2)
        else:
            x = spr.x+70
        sheight = pl.get_size()[1]/pango.SCALE
        centery = spr.y+spr.height/2
        y = int(centery-sheight/2)
        spr.tw.gc.set_foreground(spr.tw.msgcolor)
        spr.tw.area.draw_layout(spr.tw.gc, x, y, pl)
    else:
        print type(label)

# used for most things
def draw_label1(spr, label):
    draw_label(spr, label, 7, True, True)

# used for status blocks
def draw_label2(spr, label):
    draw_label(spr, str(label), 9, False, False)

# used to get pixel value from mask for category selector
def getpixel(image,x,y):
    array = image.get_pixels()
    offset = (y*image.get_width()+x)*4
    r,g,b,a = ord(array[offset]),ord(array[offset+1]),ord(array[offset+2]), \
        ord(array[offset+3])
    return (a<<24)+(b<<16)+(g<<8)+r


