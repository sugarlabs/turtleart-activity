#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-11, Walter Bender
#Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

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

import gtk
from math import sin, cos, atan, pi, sqrt
import os
import pango
import cairo
import pangocairo
import base64
from gettext import gettext as _

from sprites import Sprite
from tasprite_factory import SVG
from tautils import image_to_base64, get_path, data_to_string, round_int, \
    debug_output
from taconstants import BLACK, WHITE


def wrap100(n):
    ''' A variant on mod... 101 -> 99; 199 -> 1 '''
    n = int(n)
    n %= 200
    if n > 99:
        n = 199 - n
    return n


def calc_shade(c, s, invert=False):
    ''' Convert a color to the current shade (lightness/darkness). '''
    # Assumes 16 bit input values
    if invert:
        if s < 0:
            return int(c / (1 + s * 0.8))
        return int((c - 65536 * s * 0.9) / (1 - (s * 0.9)))
    else:
        if s < 0:
            return int(c * (1 + s * 0.8))
        return int(c + (65536 - c) * s * 0.9)


def calc_gray(c, g, invert=False):
    ''' Gray is a psuedo saturation calculation. '''
    # Assumes 16 bit input values
    if g == 100:
        return c
    if invert:
        if g == 0:
            return c
        else:
            return int(((c * 100) - (32768 * (100 - g))) / g)
    else:
        return int(((c * g) + (32768 * (100 - g))) / 100)


colors = {}
DEGTOR = 2 * pi / 360

COLOR_TABLE = (
    0xFF0000, 0xFF0D00, 0xFF1A00, 0xFF2600, 0xFF3300,
    0xFF4000, 0xFF4D00, 0xFF5900, 0xFF6600, 0xFF7300,
    0xFF8000, 0xFF8C00, 0xFF9900, 0xFFA600, 0xFFB300,
    0xFFBF00, 0xFFCC00, 0xFFD900, 0xFFE600, 0xFFF200,
    0xFFFF00, 0xE6FF00, 0xCCFF00, 0xB3FF00, 0x99FF00,
    0x80FF00, 0x66FF00, 0x4DFF00, 0x33FF00, 0x1AFF00,
    0x00FF00, 0x00FF0D, 0x00FF1A, 0x00FF26, 0x00FF33,
    0x00FF40, 0x00FF4D, 0x00FF59, 0x00FF66, 0x00FF73,
    0x00FF80, 0x00FF8C, 0x00FF99, 0x00FFA6, 0x00FFB3,
    0x00FFBF, 0x00FFCC, 0x00FFD9, 0x00FFE6, 0x00FFF2,
    0x00FFFF, 0x00F2FF, 0x00E6FF, 0x00D9FF, 0x00CCFF,
    0x00BFFF, 0x00B3FF, 0x00A6FF, 0x0099FF, 0x008CFF,
    0x0080FF, 0x0073FF, 0x0066FF, 0x0059FF, 0x004DFF,
    0x0040FF, 0x0033FF, 0x0026FF, 0x001AFF, 0x000DFF,
    0x0000FF, 0x0D00FF, 0x1A00FF, 0x2600FF, 0x3300FF,
    0x4000FF, 0x4D00FF, 0x5900FF, 0x6600FF, 0x7300FF,
    0x8000FF, 0x8C00FF, 0x9900FF, 0xA600FF, 0xB300FF,
    0xBF00FF, 0xCC00FF, 0xD900FF, 0xE600FF, 0xF200FF,
    0xFF00FF, 0xFF00E6, 0xFF00CC, 0xFF00B3, 0xFF0099,
    0xFF0080, 0xFF0066, 0xFF004D, 0xFF0033, 0xFF001A)


class TurtleGraphics:
    ''' A class for the Turtle graphics canvas '''

    def __init__(self, tw, width, height):
        ''' Create a sprite to hold the canvas. '''
        self.tw = tw
        self.width = width
        self.height = height
        
        # Build a cairo.Context from a cairo.XlibSurface
        self.canvas = cairo.Context(self.tw.turtle_canvas)
        cr = gtk.gdk.CairoContext(self.canvas)
        cr.set_line_cap(1)  # Set the line cap to be round

        self.cx = 0
        self.cy = 0
        self.fgrgb = [255, 0, 0]
        self.bgrgb = [255, 248, 222]
        self.textsize = 48  # deprecated
        self.shade = 0
        self.pendown = False
        self.xcor = 0
        self.ycor = 0
        self.heading = 0
        self.pensize = 5
        self.color = 0
        self.gray = 100
        self.fill = False
        self.poly_points = []
        self.svg = SVG()
        self.svg.set_fill_color('none')
        self.tw.svg_string = ''

    def start_fill(self):
        ''' Start accumulating points of a polygon to fill. '''
        self.fill = True
        self.poly_points = []
        if self.tw.saving_svg:
            self.tw.svg_string += '<g>'

    def stop_fill(self):
        ''' Fill the polygon. '''
        self.fill = False
        if len(self.poly_points) == 0:
            return
        self.fill_polygon(self.poly_points)
        if self.tw.sharing():
            shared_poly_points = []
            for p in self.poly_points:
                shared_poly_points.append((self.screen_to_turtle_coordinates(
                            p[0], p[1])))
                event = 'F|%s' % (data_to_string([self._get_my_nick(),
                                                  shared_poly_points]))
            self.tw.send_event(event)
        self.poly_points = []
        if self.tw.saving_svg:
            self.tw.svg_string += '</g>'

    def fill_polygon(self, poly_points):
        ''' Draw the polygon... '''
        self.canvas.new_path()
        for i, p in enumerate(poly_points):
            if p[0] == 'move':
                self.canvas.move_to(p[1], p[2])
            elif p[0] == 'rarc':
                self.canvas.arc(p[1], p[2], p[3], p[4], p[5])
            elif p[0] == 'larc':
                self.canvas.arc_negative(p[1], p[2], p[3], p[4], p[5])
            else:  # line
                self.canvas.line_to(p[1], p[2])
        self.canvas.close_path()
        self.canvas.fill()
        if self.tw.saving_svg and self.pendown:
            self.svg.set_fill_color('#%02x%02x%02x' % (self.fgrgb[0],
                                                       self.fgrgb[1],
                                                       self.fgrgb[2]))
            self.tw.svg_string += self.svg.new_path(poly_points[0][0],
                                                    poly_points[0][1])
            for p in range(len(poly_points)):
                if p > 0:
                    self.tw.svg_string += self.svg.line_to(poly_points[p][0],
                                                           poly_points[p][1])
            self.tw.svg_string += '"\n'
            self.tw.svg_string += self.svg.style()
            self.svg.set_fill_color('none')

    def clearscreen(self, share=True):
        '''Clear the canvas and reset most graphics attributes to defaults.'''
        self.canvas.move_to(0, 0)
        self.canvas.set_source_rgb(self.bgrgb[0] / 255.,
                                   self.bgrgb[1] / 255.,
                                   self.bgrgb[2] / 255.)
        self.canvas.rectangle(0, 0, self.width * 2, self.height * 2)
        self.canvas.fill()
        self.inval()
        self.setpensize(5, share)
        self.setgray(100, share)
        self.setcolor(0, share)
        self.setshade(50, share)
        self.tw.svg_string = ''
        self.svg.reset_min_max()
        self.fill = False
        self.poly_points = []
        for turtle_key in iter(self.tw.turtles.dict):
            # Don't reset remote turtles
            if not self.tw.remote_turtle(turtle_key):
                self.set_turtle(turtle_key)
                self.tw.active_turtle.set_color(0)
                self.tw.active_turtle.set_shade(50)
                self.tw.active_turtle.set_gray(100)
                self.tw.active_turtle.set_pen_size(5)
                self.tw.active_turtle.reset_shapes()
                self.seth(0, share)
                self.setpen(False, share)
                self.setxy(0, 0, share)
                self.setpen(True, share)
                self.tw.active_turtle.hide()
        self.set_turtle(self.tw.default_turtle_name)

    def forward(self, n, share=True):
        ''' Move the turtle forward.'''
        nn = n * self.tw.coord_scale
        self.canvas.set_source_rgb(self.fgrgb[0] / 255., self.fgrgb[1] / 255.,
                                   self.fgrgb[2] / 255.)
        oldx, oldy = self.xcor, self.ycor
        try:
            self.xcor += nn * sin(self.heading * DEGTOR)
            self.ycor += nn * cos(self.heading * DEGTOR)
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        if self.pendown:
            self.draw_line(oldx, oldy, self.xcor, self.ycor)

        self.move_turtle()

        if self.tw.sharing() and share:
            event = 'f|%s' % (data_to_string([self._get_my_nick(), int(n)]))
            self.tw.send_event(event)
        self.inval()

    def seth(self, n, share=True):
        ''' Set the turtle heading. '''
        try:
            self.heading = n
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.heading %= 360
        self.turn_turtle()
        if self.tw.sharing() and share:
            event = 'r|%s' % (data_to_string([self._get_my_nick(),
                                              round_int(self.heading)]))
            self.tw.send_event(event)

    def right(self, n, share=True):
        ''' Rotate turtle clockwise '''
        try:
            self.heading += n
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.heading %= 360
        self.turn_turtle()
        if self.tw.sharing() and share:
            event = 'r|%s' % (data_to_string([self._get_my_nick(),
                                              round_int(self.heading)]))
            self.tw.send_event(event)

    def arc(self, a, r, share=True):
        ''' Draw an arc '''
        self.canvas.set_source_rgb(self.fgrgb[0] / 255., self.fgrgb[1] / 255.,
                                   self.fgrgb[2] / 255.)
        try:
            if a < 0:
                self.larc(-a, r)
            else:
                self.rarc(a, r)
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.move_turtle()
        if self.tw.sharing() and share:
            event = 'a|%s' % (data_to_string([self._get_my_nick(),
                                              [round_int(a), round_int(r)]]))
            self.tw.send_event(event)

    def rarc(self, a, r):
        ''' draw a clockwise arc '''
        r *= self.tw.coord_scale
        if r < 0:
            r = -r
            a = -a
            s = 0
        else:
            s = 1
        oldx, oldy = self.xcor, self.ycor
        cx = self.xcor + r * cos(self.heading * DEGTOR)
        cy = self.ycor - r * sin(self.heading * DEGTOR)
        if self.pendown:
            x, y = self.turtle_to_screen_coordinates(cx, cy)
            self.canvas.arc(x, y, r,
                            (self.heading - 180) * DEGTOR,
                            (self.heading - 180 + a) * DEGTOR)
            self.canvas.stroke()
            self.inval()

        if self.fill:
            if self.poly_points == []:
                self.poly_points.append(('move', x, y))
            self.poly_points.append(('rarc', x, y, r,
                                     (self.heading - 180) * DEGTOR,
                                     (self.heading - 180 + a) * DEGTOR))

        self.right(a, False)
        self.xcor = cx - r * cos(self.heading * DEGTOR)
        self.ycor = cy + r * sin(self.heading * DEGTOR)
        if self.tw.saving_svg and self.pendown:
            x, y = self.turtle_to_screen_coordinates(oldx, oldy)
            self.tw.svg_string += self.svg.new_path(x, y)
            x, y = self.turtle_to_screen_coordinates(self.xcor, self.ycor)
            self.tw.svg_string += self.svg.arc_to(x, y, r, a, 0, s)
            self.tw.svg_string += '"\n'
            self.tw.svg_string += self.svg.style()

    def larc(self, a, r):
        ''' draw a counter-clockwise arc '''
        r *= self.tw.coord_scale
        if r < 0:
            r = -r
            a = -a
            s = 1
        else:
            s = 0
        oldx, oldy = self.xcor, self.ycor
        cx = self.xcor - r * cos(self.heading * DEGTOR)
        cy = self.ycor + r * sin(self.heading * DEGTOR)
        if self.pendown:
            x, y = self.turtle_to_screen_coordinates(cx, cy)
            self.canvas.arc_negative(x, y, r,
                                     (self.heading) * DEGTOR,
                                     (self.heading - a) * DEGTOR)
            self.canvas.stroke()
            self.inval()

        if self.fill:
            if self.poly_points == []:
                self.poly_points.append(('move', x, y))
            self.poly_points.append(('larc', x, y, r,
                                     (self.heading) * DEGTOR,
                                     (self.heading - a) * DEGTOR))

        self.right(-a, False)
        self.xcor = cx + r * cos(self.heading * DEGTOR)
        self.ycor = cy - r * sin(self.heading * DEGTOR)
        if self.tw.saving_svg and self.pendown:
            x, y = self.turtle_to_screen_coordinates(oldx, oldy)
            self.tw.svg_string += self.svg.new_path(x, y)
            x, y = self.turtle_to_screen_coordinates(self.xcor, self.ycor)
            self.tw.svg_string += self.svg.arc_to(x, y, r, a, 0, s)
            self.tw.svg_string += '"\n'
            self.tw.svg_string += self.svg.style()

    def setxy(self, x, y, share=True, pendown=True):
        ''' Move turtle to position x,y '''
        oldx, oldy = self.xcor, self.ycor
        x *= self.tw.coord_scale
        y *= self.tw.coord_scale
        try:
            self.xcor, self.ycor = x, y
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return

        if self.pendown and pendown:
            self.canvas.set_source_rgb(self.fgrgb[0] / 255.,
                                       self.fgrgb[1] / 255.,
                                       self.fgrgb[2] / 255.)
            self.draw_line(oldx, oldy, self.xcor, self.ycor)
            self.inval()
        self.move_turtle()

        if self.tw.sharing() and share:
            event = 'x|%s' % (data_to_string([self._get_my_nick(),
                                              [round_int(x), round_int(y)]]))
            self.tw.send_event(event)

    def setpensize(self, ps, share=True):
        ''' Set the pen size '''
        try:
            if ps < 0:
                ps = 0
            self.pensize = ps
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.tw.active_turtle.set_pen_size(ps)
        self.canvas.set_line_width(ps)
        self.svg.set_stroke_width(self.pensize)
        if self.tw.sharing() and share:
            event = 'w|%s' % (data_to_string([self._get_my_nick(),
                                              round_int(ps)]))
            self.tw.send_event(event)

    def setcolor(self, c, share=True):
        ''' Set the pen color '''
        try:
            self.color = c
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.tw.active_turtle.set_color(c)
        self.set_fgcolor()
        if self.tw.sharing() and share:
            event = 'c|%s' % (data_to_string([self._get_my_nick(),
                                              round_int(c)]))
            self.tw.send_event(event)

    def setgray(self, g, share=True):
        ''' Set the gray level '''
        try:
            self.gray = g
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        if self.gray < 0:
            self.gray = 0
        if self.gray > 100:
            self.gray = 100
        self.set_fgcolor()
        self.tw.active_turtle.set_gray(self.gray)
        if self.tw.sharing() and share:
            event = 'g|%s' % (data_to_string([self._get_my_nick(),
                                              round_int(self.gray)]))
            self.tw.send_event(event)

    def set_textcolor(self):
        ''' Deprecated: Set the text color to foreground color. '''
        return

    def settextcolor(self, c):  # deprecated
        ''' Set the text color '''
        return

    def settextsize(self, c):  # deprecated
        ''' Set the text size '''
        try:
            self.tw.textsize = c
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)

    def setshade(self, s, share=True):
        ''' Set the color shade '''
        try:
            self.shade = s
        except TypeError, ValueError:
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.tw.active_turtle.set_shade(s)
        self.set_fgcolor()
        if self.tw.sharing() and share:
            event = 's|%s' % (data_to_string([self._get_my_nick(),
                                              round_int(s)]))
            self.tw.send_event(event)

    def fillscreen(self, c, s):
        ''' Fill screen with color/shade and reset to defaults '''
        oldc, olds = self.color, self.shade
        self.setcolor(c, False)
        self.setshade(s, False)
        self.canvas.set_source_rgb(self.fgrgb[0] / 255.,
                                   self.fgrgb[1] / 255.,
                                   self.fgrgb[2] / 255.)
        self.bgrgb = self.fgrgb[:]
        self.canvas.rectangle(0, 0, self.width * 2, self.height * 2)
        self.canvas.fill()
        self.inval()
        self.setcolor(oldc, False)
        self.setshade(olds, False)
        self.tw.svg_string = ''
        self.svg.reset_min_max()
        self.fill = False
        self.poly_points = []

    def set_fgcolor(self):
        ''' Set the foreground color '''
        if self.color == WHITE or self.shade == WHITE:
            r = 0xFF00
            g = 0xFF00
            b = 0xFF00
        elif self.color == BLACK or self.shade == BLACK:
            r = 0x0000
            g = 0x0000
            b = 0x0000
        else:
            sh = (wrap100(self.shade) - 50) / 50.0
            rgb = COLOR_TABLE[wrap100(self.color)]
            r = (rgb >> 8) & 0xff00
            r = calc_gray(r, self.gray)
            r = calc_shade(r, sh)
            g = rgb & 0xff00
            g = calc_gray(g, self.gray)
            g = calc_shade(g, sh)
            b = (rgb << 8) & 0xff00
            b = calc_gray(b, self.gray)
            b = calc_shade(b, sh)
        self.fgrgb = [r >> 8, g >> 8, b >> 8]
        self.svg.set_stroke_color('#%02x%02x%02x' % (self.fgrgb[0],
                                                     self.fgrgb[1],
                                                     self.fgrgb[2]))

    def setpen(self, bool, share=True):
        ''' Lower or raise the pen '''
        self.pendown = bool
        self.tw.active_turtle.set_pen_state(bool)
        if self.tw.sharing() and share:
            event = 'p|%s' % (data_to_string([self._get_my_nick(), bool]))
            self.tw.send_event(event)

    def draw_surface(self, surface, x, y, w, h):
        ''' Draw a surface '''
        cr = gtk.gdk.CairoContext(self.canvas)
        cr.set_source_surface(surface, x, y)
        cr.rectangle(x, y, w, h)
        cr.fill()
        self.inval()

    def draw_pixbuf(self, pixbuf, a, b, x, y, w, h, path, share=True):
        ''' Draw a pixbuf '''
        # Build a gtk.gdk.CairoContext from a cairo.Context to access
        # the set_source_pixbuf attribute.
        cr = gtk.gdk.CairoContext(self.canvas)
        cr.save()
        # center the rotation on the center of the image
        cr.translate(x + w / 2., y + h / 2.)
        cr.rotate(self.heading * DEGTOR)
        cr.translate(-x - w / 2., -y - h / 2.)
        cr.set_source_pixbuf(pixbuf, x, y)
        cr.rectangle(x, y, w, h)
        cr.fill()
        cr.restore()
        self.inval()
        if self.tw.saving_svg:
            if self.tw.running_sugar:
                # In Sugar, we embed the images inside the SVG
                tmp_file = os.path.join(get_path(self.tw.activity, 'instance'),
                                       'tmpfile.png')
                pixbuf.save(tmp_file, 'png', {'quality': '100'})
                self.tw.svg_string += self.svg.image(
                    x, y, w, h, path,
                    image_to_base64(tmp_file,
                                    get_path(self.tw.activity, 'instance')))
                os.remove(tmp_file)
            else:
                # In GNOME, we embed a path
                self.tw.svg_string += self.svg.image(
                    x - self.width / 2, y, w, h, path)
        if self.tw.sharing() and share:
            if self.tw.running_sugar:
                tmp_path = get_path(self.tw.activity, 'instance')
            else:
                tmp_path = '/tmp'
            tmp_file = os.path.join(get_path(self.tw.activity, 'instance'),
                                   'tmpfile.png')
            pixbuf.save(tmp_file, 'png', {'quality': '100'})
            data = image_to_base64(tmp_file, tmp_path)
            height = pixbuf.get_height()
            width = pixbuf.get_width()
            x, y = self.screen_to_turtle_coordinates(x, y)
            event = 'P|%s' % (data_to_string([self._get_my_nick(),
                                              [round_int(a), round_int(b),
                                               round_int(x), round_int(y),
                                               round_int(w), round_int(h),
                                               round_int(width),
                                               round_int(height),
                                               data]]))
            self.tw.send_event(event)
            os.remove(tmp_file)

    def draw_text(self, label, x, y, size, w, share=True):
        ''' Draw text '''
        w *= self.tw.coord_scale
        cr = pangocairo.CairoContext(self.canvas)
        pl = cr.create_layout()
        fd = pango.FontDescription('Sans')
        fd.set_size(int(size * self.tw.coord_scale) * pango.SCALE)
        pl.set_font_description(fd)
        if type(label) == str or type(label) == unicode:
            pl.set_text(label.replace('\0', ' '))
        elif type(label) == float or type(label) == int:
            pl.set_text(str(label))
        else:
            pl.set_text(str(label))
        pl.set_width(int(w) * pango.SCALE)
        cr.save()
        cr.translate(x, y)
        cr.rotate(self.heading * DEGTOR)
        self.canvas.set_source_rgb(self.fgrgb[0] / 255.,
                                   self.fgrgb[1] / 255.,
                                   self.fgrgb[2] / 255.)
        cr.update_layout(pl)
        cr.show_layout(pl)
        cr.restore()
        self.inval()
        if self.tw.saving_svg:  # and self.pendown:
            self.tw.svg_string += self.svg.text(x, # - self.width / 2,
                                                y + size, size, w, label)
        if self.tw.sharing() and share:
            event = 'W|%s' % (data_to_string([self._get_my_nick(),
                                              [label, round_int(x),
                                               round_int(y), round_int(size),
                                               round_int(w)]]))
            self.tw.send_event(event)

    def turtle_to_screen_coordinates(self, x, y):
        ''' The origin of turtle coordinates is the center of the screen '''
        return self.width / 2. + x, self.invert_y_coordinate(y)

    def screen_to_turtle_coordinates(self, x, y):
        ''' The origin of the screen coordinates is the upper left corner '''
        return x - self.width / 2., self.invert_y_coordinate(y)

    def invert_y_coordinate(self, y):
        ''' Positive y goes up in turtle coordinates, down in sceeen
        coordinates '''
        return self.height / 2. - y

    def draw_line(self, x1, y1, x2, y2):
        ''' Draw a line '''
        x1, y1 = self.turtle_to_screen_coordinates(x1, y1)
        x2, y2 = self.turtle_to_screen_coordinates(x2, y2)

        self.canvas.move_to(x1, y1)
        self.canvas.line_to(x2, y2)
        self.canvas.stroke()

        if self.fill:
            if self.poly_points == []:
                self.poly_points.append(('move', x1, y1))
            self.poly_points.append(('line', x2, y2))

        if self.tw.saving_svg and self.pendown:
            self.tw.svg_string += self.svg.new_path(x1, y1)
            self.tw.svg_string += self.svg.line_to(x2, y2)
            self.tw.svg_string += '"\n'
            self.tw.svg_string += self.svg.style()

    def turn_turtle(self):
        ''' Change the orientation of the turtle '''
        self.tw.active_turtle.set_heading(self.heading)

    def move_turtle(self):
        ''' Move the turtle '''
        x, y = self.turtle_to_screen_coordinates(self.xcor, self.ycor)
        if self.tw.interactive_mode:
            self.tw.active_turtle.move(
                (int(self.cx + x - self.tw.active_turtle.spr.rect.width / 2.),
                 int(self.cy + y - self.tw.active_turtle.spr.rect.height / 2.)))
        else:
            self.tw.active_turtle.move((int(self.cx + x), int(self.cy + y)))

    def get_color_index(self, r, g, b, a=0):
        ''' Find the closest palette entry to the rgb triplet '''
        if self.shade != 50 or self.gray != 100:
            r <<= 8
            g <<= 8
            b <<= 8
            if self.shade != 50:
                sh = (wrap100(self.shade) - 50) / 50.
                r = calc_shade(r, sh, True)
                g = calc_shade(g, sh, True)
                b = calc_shade(b, sh, True)
            if self.gray != 100:
                r = calc_gray(r, self.gray, True)
                g = calc_gray(g, self.gray, True)
                b = calc_gray(b, self.gray, True)
            r >>= 8
            g >>= 8
            b >>= 8
        min_distance = 1000000
        closest_color = -1
        for i, c in enumerate(COLOR_TABLE):
            cr = int((c & 0xff0000) >> 16)
            cg = int((c & 0x00ff00) >> 8)
            cb = int((c & 0x0000ff))
            distance_squared = \
                ((cr - r) ** 2) + ((cg - g) ** 2) + ((cb - b) ** 2)
            if distance_squared == 0:
                return i
            if distance_squared < min_distance:
                min_distance = distance_squared
                closest_color = i
        return closest_color

    def get_pixel(self):
        ''' Read the pixel at x, y '''
        if self.tw.interactive_mode:
            x, y = self.turtle_to_screen_coordinates(self.xcor, self.ycor)
            x = int(x)
            y = int(y)
            w = self.tw.turtle_canvas.get_width()
            h = self.tw.turtle_canvas.get_height()
            if x < 0 or x > (w - 1) or y < 0 or y > (h - 1):
                return(-1, -1, -1, -1)
            # create a new 1x1 cairo surface
            cs = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1);
            cr = cairo.Context(cs)
            cr.set_source_surface(self.tw.turtle_canvas, -x, -y)
            cr.rectangle(0,0,1,1)
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.fill()
            cs.flush() # ensure all writing is done
            # Read the pixel
            pixels = cs.get_data()
            return (ord(pixels[2]), ord(pixels[1]), ord(pixels[0]), 0)
        else:
            return(-1, -1, -1, -1)

    def set_turtle(self, k, colors=None):
        ''' Select the current turtle and associated pen status '''
        if k not in self.tw.turtles.dict:
            # if it is a new turtle, start it in the center of the screen
            self.tw.active_turtle = self.tw.turtles.get_turtle(k, True, colors)
            self.seth(0, False)
            self.setxy(0, 0, False, pendown=False)
            self.tw.active_turtle.set_pen_state(True)
        elif colors is not None:
            self.tw.active_turtle = self.tw.turtles.get_turtle(k, False)
            self.tw.active_turtle.set_turtle_colors(colors)
        else:
            self.tw.active_turtle = self.tw.turtles.get_turtle(k, False)
        self.tw.active_turtle.show()
        tx, ty = self.tw.active_turtle.get_xy()
        self.xcor, self.ycor = self.screen_to_turtle_coordinates(tx, ty)
        if self.tw.interactive_mode:
            self.xcor += self.tw.active_turtle.spr.rect.width / 2.
            self.ycor -= self.tw.active_turtle.spr.rect.height / 2.
        self.heading = self.tw.active_turtle.get_heading()
        self.setcolor(self.tw.active_turtle.get_color(), False)
        self.setgray(self.tw.active_turtle.get_gray(), False)
        self.setshade(self.tw.active_turtle.get_shade(), False)
        self.setpensize(self.tw.active_turtle.get_pen_size(), False)
        self.setpen(self.tw.active_turtle.get_pen_state(), False)

    def svg_close(self):
        ''' Close current SVG graphic '''
        if self.tw.svg_string == '':
            return
        self.svg.calc_w_h(False)
        self.tw.svg_string = '%s %s %s %s' % (
            self.svg.header(True),
            self.svg.background('#%02x%02x%02x' % (
                    self.bgrgb[0], self.bgrgb[1], self.bgrgb[2])),
            self.tw.svg_string, self.svg.footer())

    def _get_my_nick(self):
        return self.tw.nick

    def inval(self):
        ''' Invalidate a region for gtk '''
        self.tw.inval_all()
