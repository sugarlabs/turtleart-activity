# -*- coding: utf-8 -*-

#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-10 Walter Bender

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

#
# A class for the list of sprites and everything they share in common
#
class Sprites:
    def __init__(self, canvas, area=None, gc=None):
        self.canvas = canvas
        if area == None:
            self.area = self.canvas.window
            self.gc = self.area.new_gc()
        else:
            self.area = area
            self.gc = gc
        self.cm = self.gc.get_colormap()
        self.list = []

    def get_sprite(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self,spr):
        self.list.append(spr)

    def insert_in_list(self,spr,i):
        if i < 0:
            self.list.insert(0, spr)
        elif i > len(self.list)-1:
            self.list.append(spr)
        else:
            self.list.insert(i, spr)

    def remove_from_list(self,spr):
        if spr in self.list:
            self.list.remove(spr)

    def find_sprite(self, pos):
        list = self.list
        list.reverse()
        for spr in list:
            if spr.hit(pos): return spr
        return None

    def redraw_sprites(self):
        for spr in self.list:
            spr.draw()

#
# A class for the individual sprites
#
class Sprite:
    def __init__(self, sprites, x, y, image):
        self.sprites = sprites
        self.x = x
        self.y = y
        self.layer = 100
        self.labels = []
        self.scale = [24]
        self.rescale = [True]
        self.horiz_align = ["center"]
        self.vert_align = ["middle"]
        self.fd = None
        self.bold = False
        self.italic = False
        self.color = None
        self.set_image(image)
        self.sprites.append_to_list(self)

    def set_image(self, image):
        self.image = image
        if isinstance(self.image,gtk.gdk.Pixbuf):
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.width, self.height = self.image.get_size()

    def move(self, pos):
        self.inval()
        self.x,self.y = pos
        self.inval()

    def set_shape(self, image):
        self.inval()
        self.set_image(image)
        self.inval()

    def set_layer(self, layer):
        self.sprites.remove_from_list(self)
        self.layer = layer
        for i in range(self.sprites.length_of_list()):
            if layer < self.sprites.get_sprite(i).layer:
                self.sprites.insert_in_list(self, i)
                self.inval()
                return
        self.sprites.append_to_list(self)
        self.inval()

    def set_label(self, new_label, i=0):
        self._extend_labels_array(i)
        if type(new_label) is str or type(new_label) is unicode:
            # pango doesn't like nulls
            self.labels[i] = new_label.replace("\0"," ")
        else:
            self.labels[i] = str(new_label)
        self.inval()

    def _extend_labels_array(self, i):
        if self.fd is None:
           self.set_font('Sans')
        if self.color is None:
           self.color = self.sprites.cm.alloc_color('black')
        while len(self.labels) < i+1:
           self.labels.append(" ")
           self.scale.append(self.scale[0])
           self.rescale.append(self.rescale[0])
           self.horiz_align.append(self.horiz_align[0])
           self.vert_align.append(self.vert_align[0])

    def set_font(self, font):
        self.fd = pango.FontDescription(font)

    def set_label_color(self, rgb):
        self.color = self.sprites.cm.alloc_color(rgb)

    def set_label_attributes(self, scale, rescale=True, horiz_align="center",
                             vert_align="middle", i=0):
        self._extend_labels_array(i)
        self.scale[i] = scale
        self.rescale[i] = rescale
        self.horiz_align[i] = horiz_align
        self.vert_align[i] = vert_align

    def hide(self):
        self.inval()
        self.sprites.remove_from_list(self)

    def inval(self):
        self.sprites.area.invalidate_rect(
            gtk.gdk.Rectangle(self.x,self.y,self.width,self.height), False)

    def draw(self):
        if isinstance(self.image,gtk.gdk.Pixbuf):
            self.sprites.area.draw_pixbuf(
                self.sprites.gc, self.image, 0, 0, self.x, self.y)
        else:
            self.sprites.area.draw_drawable(
                self.sprites.gc, self.image, 0, 0, self.x, self.y, -1, -1)
        if len(self.labels) > 0:
            self.draw_label()

    def hit(self, pos):
        x, y = pos
        if x < self.x:
            return False
        if x > self.x+self.width:
            return False
        if y < self.y:
            return False
        if y > self.y+self.height:
            return False
        return True

    def draw_label(self):
        for i in range(len(self.labels)):
            pl = self.sprites.canvas.create_pango_layout(self.labels[i])
            self.fd.set_size(int(self.scale[i]*pango.SCALE))
            pl.set_font_description(self.fd)
            w = pl.get_size()[0]/pango.SCALE
            if w > self.width:
                if self.rescale[i] is True:
                    self.fd.set_size(int(self.scale[i]*pango.SCALE*\
                                         self.width/w))
                    pl.set_font_description(self.fd)
                    w = pl.get_size()[0]/pango.SCALE
                else:
                    j = len(self.labels[i])-1
                    while(w > self.width and j > 0):
                        pl = self.sprites.canvas.create_pango_layout(
                                 "…"+self.labels[i][len(self.labels[i])-j:])
                        self.fd.set_size(int(self.scale[i]*pango.SCALE))
                        pl.set_font_description(self.fd)
                        w = pl.get_size()[0]/pango.SCALE        
                        j -= 1
            if self.horiz_align[i] == "center":
                x = int(self.x+(self.width-w)/2)
            elif self.horiz_align[i] == 'left':
                x = self.x
            else: # right
                x = int(self.x+self.width-w)
            h = pl.get_size()[1]/pango.SCALE
            if self.vert_align[i] == "middle":
                y = int(self.y+(self.height-h)/2)
            elif self.vert_align[i] == "top":
                y = self.y
            else: # bottom
                y = int(self.y+self.height-h)
            self.sprites.gc.set_foreground(self.color)
            self.sprites.area.draw_layout(self.sprites.gc, x, y, pl)

    def label_width(self):
        max = 0
        for i in range(len(self.labels)):
            pl = self.sprites.canvas.create_pango_layout(self.labels[i])
            self.fd.set_size(int(self.scale[i]*pango.SCALE))
            pl.set_font_description(self.fd)
            w = pl.get_size()[0]/pango.SCALE
            if w > max:
                max = w
        return max

    def get_pixel(self, image, x, y):
        array = image.get_pixels()
        offset = (y*image.get_width()+x)*4
        r,g,b,a = ord(array[offset]),ord(array[offset+1]),ord(array[offset+2]),\
                  ord(array[offset+3])
        return (a<<24)+(b<<16)+(g<<8)+r
