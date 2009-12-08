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
import tasetup

# Don't display the label for these blocks 
nolabel = ['audiooff', 'descriptionoff','journal']

def findsprite(tw,pos):
    list = tw.sprites[:]
    list.reverse()
    for s in list:
        if s.hit(pos): return s
    return None

def redrawsprites(tw):
    for s in tw.sprites: s.draw()


class Sprite():

    def __init__(self, tw, x, y, image, altlabel=False):
        self.tw, self.x, self.y = tw,x,y
        self.setimage(image)
        self.label = None
        self.ds_id = None
        if altlabel:
            self.draw_label = self.draw_label2
        else: self.draw_label = self.draw_label1

    '''
    mark block as selected or un-selected 
    FIXME: how we'll we create the images for selected blocks
    '''
    def set_selected(self, selected):
        if selected:
            img = tasetup.load_image(self.tw, self.tw.path, '', 'audioon')
        else:
            img = tasetup.load_image(self.tw, self.tw.path, '', 'audioon')
        self.setimage(img)

    def setimage(self, image):
        self.image = image
        if isinstance(image,gtk.gdk.Pixbuf):
            self.width = image.get_width()
            self.height = image.get_height()
        else: self.width,self.height=image.get_size()

    def move(self, pos):
        self.inval()
        self.x,self.y = pos
        self.inval()

    def inval(self):
        rect = gtk.gdk.Rectangle(self.x, self.y, self.width, self.height)
        self.tw.area.invalidate_rect(rect, False)

    def setshape(self, image):
        self.inval()
        self.setimage(image)
        self.inval()

    def setshapex(self):
        self.inval()

    def setlayer(self, layer):
        sprites = self.tw.sprites
        if self in sprites: sprites.remove(self)
        self.layer = layer
        for i in range(len(sprites)):
            if layer < sprites[i].layer:
                sprites.insert(i, self)
                self.inval()
                return
        sprites.append(self)
        self.inval()

    def hide(self):
        if self not in self.tw.sprites: return
        self.inval()
        self.tw.sprites.remove(self)

    def setlabel(self, label):
        self.label = label
        self.inval()

    def draw(self):
        if isinstance(self.image,gtk.gdk.Pixbuf):
            self.tw.area.draw_pixbuf(self.tw.gc, self.image, 0, 0, self.x, self.y)
        else:
            self.tw.area.draw_drawable(self.tw.gc,self.image,0,0,self.x,self.y,-1,-1)
        if self.label!=None:
            if hasattr(self, 'proto') and hasattr(self.proto, 'name'):
                name = self.proto.name
            else:
                name = ""
            if name not in nolabel:
                self.draw_label1(str(self.label))

    def hit(self, pos):
        x, y = pos
        if x<self.x: return False
        if x>self.x+self.width-1: return False
        if y<self.y: return False
        if y>self.y+self.height-1: return False
        if isinstance(self.image,gtk.gdk.Pixmap): return True
        if hasattr(self, 'proto') and hasattr(self.proto, 'name') and \
            self.proto.name == 'journal':
                return True
        dx, dy = x-self.x, y-self.y
        try:
            return ord(self.image.get_pixels()[(dy*self.width+dx)*4+3]) == 255
        except IndexError:
            if hasattr(spr, 'proto') and hasattr(self.proto, 'name'):
                print self.proto.name
            print "IndexError: string index out of range: " + str(dx) + " " \
                + str(dy) + " " + str(self.width) + " " + str(self.height)
            return True

    def real_draw_label(self, label, myscale, center_flag, truncate_flag):
        fd = pango.FontDescription('Sans')
        fd.set_size(int(myscale*self.tw.scale*pango.SCALE))
        if type(label) == str or type(label) == unicode:
            mylabel = label.replace("\0"," ")
            l = len(mylabel)
            if truncate_flag and l > 8:
                pl = self.tw.window.create_pango_layout("..."+mylabel[l-8:])
            else:
                pl = self.tw.window.create_pango_layout(mylabel)
            pl.set_font_description(fd)
            if center_flag:
                swidth = pl.get_size()[0]/pango.SCALE
                centerx = self.x+self.width/2
                x = int(centerx-swidth/2)
            else:
                x = self.x+70
            sheight = pl.get_size()[1]/pango.SCALE
            centery = self.y+self.height/2
            y = int(centery-sheight/2)
            self.tw.gc.set_foreground(self.tw.msgcolor)
            self.tw.area.draw_layout(self.tw.gc, x, y, pl)
        else:
            print type(label)

    # used for most things
    def draw_label1(self, label):
        self.real_draw_label(label, 7, True, True)
        
    # used for status blocks
    def draw_label2(self, label):
        self.real_draw_label(str(label), 9, False, False)

    # used to get pixel value from mask for category selector
    def getpixel(self, image,x,y):
        array = image.get_pixels()
        offset = (y*image.get_width()+x)*4
        r,g,b,a = ord(array[offset]),ord(array[offset+1]),ord(array[offset+2]), \
            ord(array[offset+3])
        return (a<<24)+(b<<16)+(g<<8)+r


