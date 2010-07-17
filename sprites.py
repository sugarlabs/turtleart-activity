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

"""

sprites.py is a simple sprites library for managing graphics objects,
'sprites', on a canvas. It manages multiple sprites with methods such
as move, hide, set_layer, etc.

There are two classes:

class Sprites maintains a collection of sprites.
class Sprite manages individual sprites within the collection.

Example usage:
        # Import the classes into your program.
        from sprites import Sprites Sprite

        # In your expose callback event handler, call refresh
        def _expose_cb(self, win, event):
            self.sprite_list.refresh(event)
            return True

        # Create a new sprite collection for a gtk Drawing Area.
        my_drawing_area = gtk.DrawingArea()
        self.sprite_list = Sprites(my_drawing_area)

        # Create a "pixbuf" (in this example, from SVG).
        my_pixbuf = svg_str_to_pixbuf("<svg>...some svg code...</svg>")

        # Create a sprite at position x1, y1.
        my_sprite = sprites.Sprite(self.sprite_list, x1, y1, my_pixbuf)

        # Move the sprite to a new position.
        my_sprite.move((x1+dx, y1+dy))

        # Create another "pixbuf".
        your_pixbuf = svg_str_to_pixbuf("<svg>...some svg code...</svg>")

        # Create a sprite at position x2, y2.
        your_sprite = sprites.Sprite(self.sprite_list, x2, y2, my_pixbuf)

        # Assign the sprites to layers.
        # In this example, your_sprite will be on top of my_sprite.
        my_sprite.set_layer(100)
        your_sprite.set_layer(200)

        # Now put my_sprite on top of your_sprite.
        my_sprite.set_layer(300)

# method for converting SVG to a gtk pixbuf
def svg_str_to_pixbuf(svg_string):
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf
"""

import pygtk
pygtk.require('2.0')
import gtk
import pango


class Sprites:
    """ A class for the list of sprites and everything they share in common """

    def __init__(self, canvas, area=None, gc=None):
        """ Initialize an empty array of sprites """
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
        """ Return a sprint from the array """
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        """ How many sprites are there? """
        return(len(self.list))

    def append_to_list(self, spr):
        """ Append a new sprite to the end of the list. """
        self.list.append(spr)

    def insert_in_list(self, spr, i):
        """ Insert a sprite at position i. """
        if i < 0:
            self.list.insert(0, spr)
        elif i > len(self.list) - 1:
            self.list.append(spr)
        else:
            self.list.insert(i, spr)

    def remove_from_list(self, spr):
        """ Remove a sprite from the list. """
        if spr in self.list:
            self.list.remove(spr)

    def find_sprite(self, pos):
        """ Search based on (x, y) position. Return the 'top/first' one. """
        list = self.list[:]
        list.reverse()
        for spr in list:
            if spr.hit(pos):
                return spr
        return None

    def refresh(self, event):
        """ Handle expose event refresh """
        self.redraw_sprites(event.area)

    def redraw_sprites(self, area=None):
        """ Redraw the sprites that intersect area. """
        for spr in self.list:
            if area == None:
                spr.draw()
            else:
                intersection = spr.rect.intersect(area)
                if intersection.width > 0 or intersection.height > 0:
                    spr.draw()


class Sprite:
    """ A class for the individual sprites """

    def __init__(self, sprites, x, y, image):
        """ Initialize an individual sprite """
        self._sprites = sprites
        self.rect = gtk.gdk.Rectangle(int(x), int(y), 0, 0)
        self._scale = [12]
        self._rescale = [True]
        self._horiz_align = ["center"]
        self._vert_align = ["middle"]
        self._fd = None
        self._bold = False
        self._italic = False
        self._color = None
        self._margins = [0, 0, 0, 0]
        self.layer = 100
        self.labels = []
        self.images = []
        self._dx = []  # image offsets
        self._dy = []
        self.set_image(image)
        self._sprites.append_to_list(self)

    def set_image(self, image, i=0, dx=0, dy=0):
        """ Add an image to the sprite. """
        while len(self.images) < i + 1:
            self.images.append(None)
            self._dx.append(0)
            self._dy.append(0)
        self.images[i] = image
        self._dx[i] = dx
        self._dy[i] = dy
        if isinstance(self.images[i], gtk.gdk.Pixbuf):
            w = self.images[i].get_width()
            h = self.images[i].get_height()
        else:
            w, h = self.images[i].get_size()
        if i == 0:  # Always reset width and height when base image changes.
            self.rect.width = w + dx
            self.rect.height = h + dy
        else:
            if w + dx > self.rect.width:
                self.rect.width = w + dx
            if h + dy > self.rect.height:
                self.rect.height = h + dy

    def move(self, pos):
        """ Move to new (x, y) position """
        self.inval()
        self.rect.x, self.rect.y = int(pos[0]), int(pos[1])
        self.inval()

    def move_relative(self, pos):
        """ Move to new (x+dx, y+dy) position """
        self.inval()
        self.rect.x += int(pos[0])
        self.rect.y += int(pos[1])
        self.inval()

    def get_xy(self):
        """ Return current (x, y) position """
        return (self.rect.x, self.rect.y)

    def get_dimensions(self):
        """ Return current size """
        return (self.rect.width, self.rect.height)

    def get_layer(self):
        """ Return current layer """
        return self.layer

    def set_shape(self, image, i=0):
        """ Set the current image associated with the sprite """
        self.inval()
        self.set_image(image, i)
        self.inval()

    def set_layer(self, layer):
        """ Set the layer for a sprite """
        self._sprites.remove_from_list(self)
        self.layer = layer
        for i in range(self._sprites.length_of_list()):
            if layer < self._sprites.get_sprite(i).layer:
                self._sprites.insert_in_list(self, i)
                self.inval()
                return
        self._sprites.append_to_list(self)
        self.inval()

    def set_label(self, new_label, i=0):
        """ Set the label drawn on the sprite """
        self._extend_labels_array(i)
        if type(new_label) is str or type(new_label) is unicode:
            # pango doesn't like nulls
            self.labels[i] = new_label.replace("\0", " ")
        else:
            self.labels[i] = str(new_label)
        self.inval()

    def set_margins(self, l=0, t=0, r=0, b=0):
        """ Set the margins for drawing the label """
        self._margins = [l, t, r, b]

    def _extend_labels_array(self, i):
        """ Append to the labels attribute list """
        if self._fd is None:
            self.set_font('Sans')
        if self._color is None:
            self._color = self._sprites.cm.alloc_color('black')
        while len(self.labels) < i + 1:
            self.labels.append(" ")
            self._scale.append(self._scale[0])
            self._rescale.append(self._rescale[0])
            self._horiz_align.append(self._horiz_align[0])
            self._vert_align.append(self._vert_align[0])

    def set_font(self, font):
        """ Set the font for a label """
        self._fd = pango.FontDescription(font)

    def set_label_color(self, rgb):
        """ Set the font color for a label """
        self._color = self._sprites.cm.alloc_color(rgb)

    def set_label_attributes(self, scale, rescale=True, horiz_align="center",
                             vert_align="middle", i=0):
        """ Set the various label attributes """
        self._extend_labels_array(i)
        self._scale[i] = scale
        self._rescale[i] = rescale
        self._horiz_align[i] = horiz_align
        self._vert_align[i] = vert_align

    def hide(self):
        """ Hide a sprite """
        self.inval()
        self._sprites.remove_from_list(self)

    def inval(self):
        """ Force a region redraw by gtk """
        self._sprites.area.invalidate_rect(self.rect, False)

    def draw(self):
        """ Draw the sprite (and label) """
        for i, img in enumerate(self.images):
            if isinstance(img, gtk.gdk.Pixbuf):
                self._sprites.area.draw_pixbuf(self._sprites.gc, img, 0, 0,
                                               self.rect.x + self._dx[i],
                                               self.rect.y + self._dy[i])
            elif img is not None:
                self._sprites.area.draw_drawable(self._sprites.gc, img, 0, 0,
                                                 self.rect.x + self._dx[i],
                                                 self.rect.y + self._dy[i],
                                                 -1, -1)
        if len(self.labels) > 0:
            self.draw_label()

    def hit(self, pos):
        """ Is (x, y) on top of the sprite? """
        x, y = pos
        if x < self.rect.x:
            return False
        if x > self.rect.x + self.rect.width:
            return False
        if y < self.rect.y:
            return False
        if y > self.rect.y + self.rect.height:
            return False
        return True

    def draw_label(self):
        """ Draw the label based on its attributes """
        my_width = self.rect.width - self._margins[0] - self._margins[2]
        if my_width < 0:
            my_width = 0
        my_height = self.rect.height - self._margins[1] - self._margins[3]
        for i in range(len(self.labels)):
            pl = self._sprites.canvas.create_pango_layout(str(self.labels[i]))
            self._fd.set_size(int(self._scale[i] * pango.SCALE))
            pl.set_font_description(self._fd)
            w = pl.get_size()[0] / pango.SCALE
            if w > my_width:
                if self._rescale[i]:
                    self._fd.set_size(
                            int(self._scale[i] * pango.SCALE * my_width / w))
                    pl.set_font_description(self._fd)
                    w = pl.get_size()[0] / pango.SCALE
                else:
                    j = len(self.labels[i]) - 1
                    while(w > my_width and j > 0):
                        pl = self._sprites.canvas.create_pango_layout(
                              "…" + self.labels[i][len(self.labels[i]) - j:])
                        self._fd.set_size(int(self._scale[i] * pango.SCALE))
                        pl.set_font_description(self._fd)
                        w = pl.get_size()[0] / pango.SCALE
                        j -= 1
            if self._horiz_align[i] == "center":
                x = int(self.rect.x + self._margins[0] + (my_width - w) / 2)
            elif self._horiz_align[i] == 'left':
                x = int(self.rect.x + self._margins[0])
            else: # right
                x = int(self.rect.x + self.rect.width - w - self._margins[2])
            h = pl.get_size()[1] / pango.SCALE
            if self._vert_align[i] == "middle":
                y = int(self.rect.y + self._margins[1] + (my_height - h) / 2)
            elif self._vert_align[i] == "top":
                y = int(self.rect.y + self._margins[1])
            else: # bottom
                y = int(self.rect.y + self.rect.height - h - self._margins[3])
            self._sprites.gc.set_foreground(self._color)
            self._sprites.area.draw_layout(self._sprites.gc, x, y, pl)

    def label_width(self):
        """ Calculate the width of a label """
        max = 0
        for i in range(len(self.labels)):
            pl = self._sprites.canvas.create_pango_layout(self.labels[i])
            self._fd.set_size(int(self._scale[i] * pango.SCALE))
            pl.set_font_description(self._fd)
            w = pl.get_size()[0] / pango.SCALE
            if w > max:
                max = w
        return max

    def label_safe_width(self):
        """ Return maximum width for a label """
        return self.rect.width - self._margins[0] - self._margins[2]

    def label_safe_height(self):
        """ Return maximum height for a label """
        return self.rect.height - self._margins[1] - self._margins[3]

    def label_left_top(self):
        """ Return the upper-left corner of the label safe zone """
        return(self._margins[0], self._margins[1])

    def get_pixel(self, pos, i=0):
        """ Return the pixl at (x, y) """
        x, y = pos
        x = x - self.rect.x
        y = y - self.rect.y
        if y > self.images[i].get_height() - 1:
            return(-1, -1, -1, -1)
        try:
            array = self.images[i].get_pixels()
            if array is not None:
                offset = (y * self.images[i].get_width() + x) * 4
                r, g, b, a = ord(array[offset]), ord(array[offset + 1]),\
                             ord(array[offset + 2]), ord(array[offset + 3])
                return(r, g, b, a)
            else:
                return(-1, -1, -1, -1)
        except IndexError:
            print "Index Error: %d %d" % (len(array), offset)
            return(-1, -1, -1, -1)
