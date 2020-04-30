# -*- coding: utf-8 -*-

# Copyright (c) 2007-8, Playful Invention Company.
# Copyright (c) 2008-14 Walter Bender

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''

sprites.py is a simple sprites library for managing graphics objects,
'sprites', on a Gtk.DrawingArea. It manages multiple sprites with
methods such as move, hide, set_layer, etc.

There are two classes:

class Sprites maintains a collection of sprites
class Sprite manages individual sprites within the collection.

Example usage:
        # Import the classes into your program.
        from sprites import Sprites Sprite

        # Create a new sprite collection associated with your widget
        self.sprite_list = Sprites(widget)

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

        cr = self.window.cairo_create()
        # In your activity's do_expose_event, put in a call to redraw_sprites
        self.sprites.redraw_sprites(event.area, cairo_context)

# method for converting SVG to a gtk pixbuf
def svg_str_to_pixbuf(svg_string):
    pl = GdkPixbuf.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf

'''
import cairo

from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Pango
from gi.repository import PangoCairo


class Sprites:

    ''' A class for the list of sprites and everything they share in common '''

    def __init__(self, widget):
        ''' Initialize an empty array of sprites '''
        self.widget = widget
        self.list = []
        self.cr = None
        self.defer_draw = False

    def set_defer_draw(self, state):
        self.defer_draw = state

    def set_cairo_context(self, cr):
        ''' Cairo context may be set or reset after __init__ '''
        self.cr = cr

    def get_sprite(self, i):
        ''' Return a sprint from the array '''
        if i < 0 or i > len(self.list) - 1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        ''' How many sprites are there? '''
        return len(self.list)

    def append_to_list(self, spr):
        ''' Append a new sprite to the end of the list. '''
        self.list.append(spr)

    def insert_in_list(self, spr, i):
        ''' Insert a sprite at position i. '''
        if i < 0:
            self.list.insert(0, spr)
        elif i > len(self.list) - 1:
            self.list.append(spr)
        else:
            self.list.insert(i, spr)

    def find_in_list(self, spr):
        return (spr in self.list)

    def remove_from_list(self, spr):
        ''' Remove a sprite from the list. '''
        if spr in self.list:
            self.list.remove(spr)

    def find_sprite(self, pos, region=False):
        ''' Search based on (x, y) position. Return the 'top/first' one. '''
        list = self.list[:]
        list.reverse()
        for spr in list:
            if spr.hit(pos, readpixel=not region):
                return spr
        return None

    def redraw_sprites(self, area=None, cr=None):
        ''' Redraw the sprites that intersect area. '''
        # I think I need to do this to save Cairo some work
        self.defer_draw = False
        if cr is None:
            cr = self.cr
        else:
            self.cr = cr
        if cr is None:
            print('sprites.redraw_sprites: no Cairo context')
            return
        for spr in self.list:
            if area is None:
                spr.draw(cr=cr)
            else:
                intersection = spr.rect.intersect(area)
                if intersection.width > 0 or intersection.height > 0:
                    spr.draw(cr=cr)


class Sprite:

    ''' A class for the individual sprites '''

    def __init__(self, sprites, x, y, image):
        ''' Initialize an individual sprite '''
        self._sprites = sprites
        self.save_xy = (x, y)  # remember initial (x, y) position
        self.rect = Gdk.Rectangle()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.rect.width = image.get_height()
        self.rect.height = image.get_width()
        self._scale = [12]
        self._rescale = [True]
        self._horiz_align = ['center']
        self._vert_align = ['middle']
        self._x_pos = [None]
        self._y_pos = [None]
        self._fd = None
        self._bold = False
        self._italic = False
        self._color = None
        self._margins = [0, 0, 0, 0]
        self.layer = 100
        self.labels = []
        self.cached_surfaces = []
        self._dx = []  # image offsets
        self._dy = []
        self.type = None
        self.set_image(image)
        self._sprites.append_to_list(self)

    def set_image(self, image, i=0, dx=0, dy=0):
        ''' Add an image to the sprite. '''
        while len(self.cached_surfaces) < i + 1:
            self.cached_surfaces.append(None)
            self._dx.append(0)
            self._dy.append(0)
        self._dx[i] = dx
        self._dy[i] = dy
        if isinstance(image, GdkPixbuf.Pixbuf) or \
           isinstance(image, cairo.ImageSurface):
            w = image.get_width()
            h = image.get_height()
        else:
            w, h = image.get_size()
        if i == 0:  # Always reset width and height when base image changes.
            self.rect.width = w + dx
            self.rect.height = h + dy
        else:
            if w + dx > self.rect.width:
                self.rect.width = w + dx
            if h + dy > self.rect.height:
                self.rect.height = h + dy
        if isinstance(image, cairo.ImageSurface):
            self.cached_surfaces[i] = image
        else:  # Convert to Cairo surface
            surface = cairo.ImageSurface(
                cairo.FORMAT_ARGB32, self.rect.width, self.rect.height)
            context = cairo.Context(surface)
            Gdk.cairo_set_source_pixbuf(context, image, 0, 0)
            context.rectangle(0, 0, self.rect.width, self.rect.height)
            context.fill()
            self.cached_surfaces[i] = surface

    def move(self, pos):
        ''' Move to new (x, y) position '''
        self.inval()
        self.rect.x, self.rect.y = int(pos[0]), int(pos[1])
        self.inval()

    def move_relative(self, pos):
        ''' Move to new (x+dx, y+dy) position '''
        self.inval()
        self.rect.x += int(pos[0])
        self.rect.y += int(pos[1])
        self.inval()

    def get_xy(self):
        ''' Return current (x, y) position '''
        return (self.rect.x, self.rect.y)

    def get_dimensions(self):
        ''' Return current size '''
        return (self.rect.width, self.rect.height)

    def get_layer(self):
        ''' Return current layer '''
        return self.layer

    def set_shape(self, image, i=0):
        ''' Set the current image associated with the sprite '''
        self.inval()
        self.set_image(image, i)
        self.inval()

    def set_layer(self, layer=None):
        ''' Set the layer for a sprite '''
        self._sprites.remove_from_list(self)
        if layer is not None:
            self.layer = layer
        for i in range(self._sprites.length_of_list()):
            spr = self._sprites.get_sprite(i)
            if spr is not None and self.layer < spr.layer:
                self._sprites.insert_in_list(self, i)
                self.inval()
                return
        self._sprites.append_to_list(self)
        self.inval()

    def set_label(self, new_label, i=0):
        ''' Set the label drawn on the sprite '''
        self._extend_labels_array(i)
        if isinstance(new_label, str):
            # pango doesn't like nulls
            self.labels[i] = new_label.replace('\0', ' ')
        else:
            self.labels[i] = str(new_label)
        self.inval()

    def set_margins(self, left=0, top=0, right=0, bottom=0):
        ''' Set the margins for drawing the label '''
        self._margins = [left, top, right, bottom]

    def _extend_labels_array(self, i):
        ''' Append to the labels attribute list '''
        if self._fd is None:
            self.set_font('Sans')
        if self._color is None:
            self._color = (0., 0., 0.)
        while len(self.labels) < i + 1:
            self.labels.append(' ')
            self._scale.append(self._scale[0])
            self._rescale.append(self._rescale[0])
            self._horiz_align.append(self._horiz_align[0])
            self._vert_align.append(self._vert_align[0])
            self._x_pos.append(self._x_pos[0])
            self._y_pos.append(self._y_pos[0])

    def set_font(self, font):
        ''' Set the font for a label '''
        self._fd = Pango.FontDescription(font)

    def set_label_color(self, rgb):
        ''' Set the font color for a label '''
        COLORTABLE = {'black': '#000000', 'white': '#FFFFFF',
                      'red': '#FF0000', 'yellow': '#FFFF00',
                      'green': '#00FF00', 'cyan': '#00FFFF',
                      'blue': '#0000FF', 'purple': '#FF00FF',
                      'gray': '#808080'}
        if rgb.lower() in COLORTABLE:
            rgb = COLORTABLE[rgb.lower()]
        # Convert from '#RRGGBB' to floats
        self._color = (int('0x' + rgb[1:3], 16) / 256.,
                       int('0x' + rgb[3:5], 16) / 256.,
                       int('0x' + rgb[5:7], 16) / 256.)
        return

    def set_label_attributes(self, scale, rescale=True, horiz_align='center',
                             vert_align='middle', x_pos=None, y_pos=None, i=0):
        ''' Set the various label attributes '''
        self._extend_labels_array(i)
        self._scale[i] = scale
        self._rescale[i] = rescale
        self._horiz_align[i] = horiz_align
        self._vert_align[i] = vert_align
        self._x_pos[i] = x_pos
        self._y_pos[i] = y_pos

    def hide(self):
        ''' Hide a sprite '''
        self.inval()
        self._sprites.remove_from_list(self)

    def restore(self):
        ''' Restore a hidden sprite '''
        self.set_layer()

    def inval(self):
        ''' Invalidate a region for gtk '''
        self._sprites.widget.queue_draw_area(self.rect.x,
                                             self.rect.y,
                                             self.rect.width,
                                             self.rect.height)

    def draw(self, cr=None):
        ''' Draw the sprite (and label) '''
        if self._sprites.defer_draw:
            return
        if cr is None:
            print('sprite.draw: no Cairo context.')
            return
        for i, surface in enumerate(self.cached_surfaces):
            cr.set_source_surface(surface,
                                  self.rect.x + self._dx[i],
                                  self.rect.y + self._dy[i])
            cr.rectangle(self.rect.x + self._dx[i],
                         self.rect.y + self._dy[i],
                         self.rect.width,
                         self.rect.height)
            cr.fill()

        if len(self.labels) > 0:
            self.draw_label(cr)

    def hit(self, pos, readpixel=False):
        ''' Is (x, y) on top of the sprite? '''
        x, y = pos
        if x < self.rect.x:
            return False
        if x > self.rect.x + self.rect.width:
            return False
        if y < self.rect.y:
            return False
        if y > self.rect.y + self.rect.height:
            return False
        if readpixel:
            r, g, b, a = self.get_pixel(pos)
            if r == g == b == a == 0:
                return False
            if a == -1:
                return False
        return self._sprites.find_in_list(self)

    def draw_label(self, cr):
        ''' Draw the label based on its attributes '''

        my_width = self.rect.width - self._margins[0] - self._margins[2]
        if my_width < 0:
            my_width = 0
        my_height = self.rect.height - self._margins[1] - self._margins[3]
        for i in range(len(self.labels)):
            pl = PangoCairo.create_layout(cr)
            pl.set_text(self.labels[i], -1)
            self._fd.set_size(int(self._scale[i] * Pango.SCALE))
            pl.set_font_description(self._fd)
            w = pl.get_size()[0] / Pango.SCALE
            if w > my_width:
                if self._rescale[i]:
                    self._fd.set_size(
                        int(self._scale[i] * Pango.SCALE * my_width / w))
                    pl.set_font_description(self._fd)
                    w = pl.get_size()[0] / Pango.SCALE
                else:
                    pl.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
                    self._fd.set_size(int(self._scale[i] * Pango.SCALE))
                    pl.set_font_description(self._fd)
                    w = pl.get_size()[0] / Pango.SCALE
            if self._x_pos[i] is not None:
                x = int(self.rect.x + self._x_pos[i])
            elif self._horiz_align[i] == 'center':
                x = int(self.rect.x + self._margins[0] + (my_width - w) / 2)
            elif self._horiz_align[i] == 'left':
                x = int(self.rect.x + self._margins[0])
            else:  # right
                x = int(self.rect.x + self.rect.width - w - self._margins[2])
            h = pl.get_size()[1] / Pango.SCALE
            if self._y_pos[i] is not None:
                y = int(self.rect.y + self._y_pos[i])
            elif self._vert_align[i] == 'middle':
                y = int(self.rect.y + self._margins[1] + (my_height - h) / 2)
            elif self._vert_align[i] == 'top':
                y = int(self.rect.y + self._margins[1])
            else:  # bottom
                y = int(self.rect.y + self.rect.height - h - self._margins[3])

            cr.save()
            cr.translate(x, y)
            cr.set_source_rgb(self._color[0], self._color[1], self._color[2])
            PangoCairo.update_layout(cr, pl)
            PangoCairo.show_layout(cr, pl)

            cr.restore()

    def label_width(self):
        ''' Calculate the width of a label '''
        cr = self._sprites.cr
        if cr is not None:
            max = 0
            for i in range(len(self.labels)):
                pl = PangoCairo.create_layout(cr)
                pl.set_text(self.labels[i], -1)
                self._fd.set_size(int(self._scale[i] * Pango.SCALE))
                pl.set_font_description(self._fd)
                w = pl.get_size()[0] / Pango.SCALE
                if w > max:
                    max = w
            return max
        else:
            return self.rect.width

    def label_safe_width(self):
        ''' Return maximum width for a label '''
        return self.rect.width - self._margins[0] - self._margins[2]

    def label_safe_height(self):
        ''' Return maximum height for a label '''
        return self.rect.height - self._margins[1] - self._margins[3]

    def label_left_top(self):
        ''' Return the upper-left corner of the label safe zone '''
        return(self._margins[0], self._margins[1])

    def get_pixel(self, pos, i=0):
        ''' Return the pixel at (x, y) '''
        x = int(pos[0] - self.rect.x)
        y = int(pos[1] - self.rect.y)
        if x < 0 or x > (self.rect.width - 1) or \
                y < 0 or y > (self.rect.height - 1):
            return(-1, -1, -1, -1)
        # Create a new 1x1 cairo surface.
        cs = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
        cr = cairo.Context(cs)
        cr.set_source_surface(self.cached_surfaces[i], -x, -y)
        cr.rectangle(0, 0, 1, 1)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.fill()
        cs.flush()  # Ensure all the writing is done.
        pixels = cs.get_data()  # Read the pixel.
        return (pixels[2], pixels[1], pixels[0], 0)
