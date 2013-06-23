# -*- coding: utf-8 -*-
#Copyright (c) 2010-13 Walter Bender

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

from random import uniform
from math import sin, cos, pi, sqrt
import gtk
import cairo

from taconstants import (TURTLE_LAYER, DEFAULT_TURTLE_COLORS)
from tasprite_factory import (SVG, svg_str_to_pixbuf)
from tacanvas import (wrap100, COLOR_TABLE, COLORDICT)
from sprites import Sprite
from tautils import debug_output, data_to_string, round_int

SHAPES = 36
DEGTOR = pi / 180.
RTODEG = 180. / pi


def generate_turtle_pixbufs(colors):
    """ Generate pixbufs for generic turtles """
    shapes = []
    svg = SVG()
    svg.set_scale(1.0)
    for i in range(SHAPES):
        svg.set_orientation(i * 10)
        shapes.append(svg_str_to_pixbuf(svg.turtle(colors)))
    return shapes


class Turtles:

    def __init__(self, sprite_list):
        """ Class to hold turtles """
        self.dict = dict()
        self.sprite_list = sprite_list
        self.default_pixbufs = []

    def get_turtle(self, k, append=False, colors=None):
        """ Find a turtle """
        if k in self.dict:
            return self.dict[k]
        elif not append:
            return None
        else:
            if colors is None:
                Turtle(self, k)
            elif isinstance(colors, (list, tuple)):
                Turtle(self, k, colors)
            else:
                Turtle(self, k, colors.split(','))
            return self.dict[k]

    def get_turtle_key(self, turtle):
        """ Find a turtle's name """
        for k in iter(self.dict):
            if self.dict[k] == turtle:
                return k
        return None

    def turtle_count(self):
        """ How many turtles are there? """
        return(len(self.dict))

    def add_to_dict(self, k, turtle):
        """ Add a new turtle """
        self.dict[k] = turtle

    def remove_from_dict(self, k):
        """ Delete a turtle """
        if k in self.dict:
            del(self.dict[k])

    def show_all(self):
        """ Make all turtles visible """
        for k in iter(self.dict):
            self.dict[k].show()

    def spr_to_turtle(self, spr):
        """ Find the turtle that corresponds to sprite spr. """
        for k in iter(self.dict):
            if spr == self.dict[k].spr:
                return self.dict[k]
        return None

    def get_pixbufs(self):
        """ Get the pixbufs for the default turtle shapes. """
        if self.default_pixbufs == []:
            self.default_pixbufs = generate_turtle_pixbufs(
                ["#008000", "#00A000"])
        return(self.default_pixbufs)


class Turtle:

    def __init__(self, turtle_window, turtles, key, turtle_colors=None):
        """ The turtle is not a block, just a sprite with an orientation """
        self.tw = turtle_window
        self.x = 0.0
        self.y = 0.0
        self.hidden = False
        self.shapes = []
        self.custom_shapes = False
        self.type = 'turtle'
        self.name = key
        self.heading = 0.0
        self.pen_shade = 50
        self.pen_color = 0
        self.pen_gray = 100
        self.pen_size = 5
        self.pen_state = True
        self.pen_fill = False
        self.pen_poly_points = []
        self.label_block = None

        self._prep_shapes(key, turtles, turtle_colors)

        # Choose a random angle from which to attach the turtle label.
        if turtles.sprite_list is not None:
            self.spr = Sprite(turtles.sprite_list, 0, 0, self.shapes[0])
            angle = uniform(0, pi * 4 / 3.0)  # 240 degrees
            w = self.shapes[0].get_width()
            r = w * 0.67
            # Restrict angle the the sides 30-150; 210-330
            if angle > pi * 2 / 3.0:
                angle += pi / 2.0  # + 90
                self.label_xy = [int(r * sin(angle)),
                                 int(r * cos(angle) + w / 2.0)]
            else:
                angle += pi / 6.0  # + 30
                self.label_xy = [int(r * sin(angle) + w / 2.0),
                                 int(r * cos(angle) + w / 2.0)]
        else:
            self.spr = None
        turtles.add_to_dict(key, self)

    def _prep_shapes(self, name, turtles=None, turtle_colors=None):
        # If the turtle name is an int, we'll use a palette color as the
        # turtle color
        try:
            int_key = int(name)
            use_color_table = True
        except ValueError:
            use_color_table = False

        if turtle_colors is not None:
            self.colors = turtle_colors[:]
            self.shapes = generate_turtle_pixbufs(self.colors)
        elif use_color_table:
            fill = wrap100(int_key)
            stroke = wrap100(fill + 10)
            self.colors = ['#%06x' % (COLOR_TABLE[fill]),
                           '#%06x' % (COLOR_TABLE[stroke])]
            self.shapes = generate_turtle_pixbufs(self.colors)
        else:
            if turtles is not None:
                self.colors = DEFAULT_TURTLE_COLORS
                self.shapes = turtles.get_pixbufs()

    def set_turtle_colors(self, turtle_colors):
        ''' reset the colors of a preloaded turtle '''
        if turtle_colors is not None:
            self.colors = turtle_colors[:]
            self.shapes = generate_turtle_pixbufs(self.colors)
            self.set_heading(self.heading, share=False)

    def set_shapes(self, shapes, i=0):
        """ Reskin the turtle """
        n = len(shapes)
        if n == 1 and i > 0:  # set shape[i]
            if i < len(self.shapes):
                self.shapes[i] = shapes[0]
        elif n == SHAPES:  # all shapes have been precomputed
            self.shapes = shapes[:]
        else:  # rotate shapes
            if n != 1:
                debug_output("%d images passed to set_shapes: ignoring" % (n),
                             self.tw.running_sugar)
            if self.heading == 0.0:  # rotate the shapes
                images = []
                w, h = shapes[0].get_width(), shapes[0].get_height()
                nw = nh = int(sqrt(w * w + h * h))
                for i in range(SHAPES):
                    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, nw, nh)
                    context = cairo.Context(surface)
                    context = gtk.gdk.CairoContext(context)
                    context.translate(nw / 2., nh / 2.)
                    context.rotate(i * 10 * pi / 180.)
                    context.translate(-nw / 2., -nh / 2.)
                    context.set_source_pixbuf(shapes[0], (nw - w) / 2.,
                                              (nh - h) / 2.)
                    context.rectangle(0, 0, nw, nh)
                    context.fill()
                    images.append(surface)
                self.shapes = images[:]
            else:  # associate shape with image at current heading
                j = int(self.heading + 5) % 360 / (360 / SHAPES)
                self.shapes[j] = shapes[0]
        self.custom_shapes = True
        self.show()

    def reset_shapes(self):
        """ Reset the shapes to the standard turtle """
        if self.custom_shapes:
            self.shapes = generate_turtle_pixbufs(self.colors)
            self.custom_shapes = False

    def set_heading(self, heading, share=True):
        """ Set the turtle heading (one shape per 360/SHAPES degrees) """
        try:
            self.heading = heading
        except (TypeError, ValueError):
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.heading %= 360

        i = (int(self.heading + 5) % 360) / (360 / SHAPES)
        if not self.hidden and self.spr is not None:
            try:
                self.spr.set_shape(self.shapes[i])
            except IndexError:
                self.spr.set_shape(self.shapes[0])

        if self.tw.sharing() and share:
            event = 'r|%s' % (data_to_string([self.tw.nick,
                                              round_int(self.heading)]))
            self.tw.send_event(event)

    def set_color(self, color=None, share=True):
        """ Set the pen color for this turtle. """
        # Special case for color blocks
        if color is not None and color in COLORDICT:
            self.set_shade(COLORDICT[color][1], share)
            self.set_gray(COLORDICT[color][2], share)
            if COLORDICT[color][0] is not None:
                self.set_color(COLORDICT[color][0], share)
                color = COLORDICT[color][0]
            else:
                color = self.pen_color

            try:
                self.pen_color = color
            except (TypeError, ValueError):
                debug_output('bad value sent to %s' % (__name__),
                             self.tw.running_sugar)
                return

        self.tw.canvas.set_fgcolor(shade=self.pen_shade,
                                   gray=self.pen_gray,
                                   color=self.pen_color)

        if self.tw.sharing() and share:
            event = 'c|%s' % (data_to_string([self.tw.nick,
                                              round_int(self.pen_color)]))
            self.tw.send_event(event)

    def set_gray(self, gray=None, share=True):
        """ Set the pen gray level for this turtle. """
        if gray is not None:
            try:
                self.pen_gray = gray
            except (TypeError, ValueError):
                debug_output('bad value sent to %s' % (__name__),
                             self.tw.running_sugar)
                return

        if self.pen_gray < 0:
            self.pen_gray = 0
        if self.pen_gray > 100:
            self.pen_gray = 100

        self.tw.canvas.set_fgcolor(shade=self.pen_shade,
                                   gray=self.pen_gray,
                                   color=self.pen_color)

        if self.tw.sharing() and share:
            event = 'g|%s' % (data_to_string([self.tw.nick,
                                              round_int(self.pen_gray)]))
            self.tw.send_event(event)

    def set_shade(self, shade=None, share=True):
        """ Set the pen shade for this turtle. """
        if shade is not None:
            try:
                self.pen_shade = shade
            except (TypeError, ValueError):
                debug_output('bad value sent to %s' % (__name__),
                             self.tw.running_sugar)
                return

        self.tw.canvas.set_fgcolor(shade=self.pen_shade,
                                   gray=self.pen_gray,
                                   color=self.pen_color)

        if self.tw.sharing() and share:
            event = 's|%s' % (data_to_string([self.tw.nick,
                                              round_int(self.pen_shade)]))
            self.tw.send_event(event)

    def set_pen_size(self, pen_size=None, share=True):
        """ Set the pen size for this turtle. """
        if pen_size is not None:
            try:
                self.pen_size = max(0, pen_size)
            except (TypeError, ValueError):
                debug_output('bad value sent to %s' % (__name__),
                             self.tw.running_sugar)
                return

        self.tw.canvas.set_pen_size(self.pen_size)

        if self.tw.sharing() and share:
            event = 'w|%s' % (data_to_string([self.tw.nick,
                                              round_int(self.pen_size)]))
            self.tw.send_event(event)

    def set_pen_state(self, pen_state=None, share=True):
        """ Set the pen state (down==True) for this turtle. """
        if pen_state is not None:
            self.pen_state = pen_state

        self.tw.canvas.set_pen(self.pen_state)

        if self.tw.sharing() and share:
            event = 'p|%s' % (data_to_string([self.tw.nick,
                                              self._pen_state]))
            self.tw.send_event(event)

    def set_fill(self, state=False):
        self.pen_fill = state
        if not self.pen_fill:
            self.poly_points = []

    def set_poly_points(self, poly_points=None):
        if poly_points is not None:
            self.poly_points = poly_points[:]

    def start_fill(self):
        self.pen_fill = True
        self.poly_points = []

    def stop_fill(self, share=True):
        self.pen_fill = False
        if len(self.poly_points) == 0:
            return

        self.tw.canvas.fill_polygon(self.poly_points)

        if self.tw.sharing() and share:
            shared_poly_points = []
            for p in self.poly_points:
                shared_poly_points.append(
                    (self.tw.canvas.screen_to_turtle_coordinates(p[0], p[1])))
                event = 'F|%s' % (data_to_string([self.tw.nick,
                                                  shared_poly_points]))
            self.tw.send_event(event)
        self.poly_points = []

    def hide(self):
        if self.spr is not None:
            self.spr.hide()
        if self.label_block is not None:
            self.label_block.spr.hide()
        self.hidden = True

    def show(self):
        if self.spr is not None:
            self.spr.set_layer(TURTLE_LAYER)
            self.hidden = False
        self.move((self.x, self.y))
        self.set_heading(self.heading)
        if self.label_block is not None:
            self.label_block.spr.set_layer(TURTLE_LAYER + 1)

    def move_turtle(self, pos=None):
        if pos is None:
            x, y = self.tw.canvas.get_xy()
        else:
            x, y = self.tw.canvas.turtle_to_screen_coordinates(pos[0], pos[1])
        if self.tw.interactive_mode:
            self.move((self.tw.canvas.cx + x - self.spr.rect.width / 2.,
                       self.tw.canvas.cy + y - self.spr.rect.height / 2.))
        else:
            self.move((self.tw.canvas.cx + x, self.tw.canvas.cy + y))

    def move(self, pos):
        self.x, self.y = pos[0], pos[1]
        if not self.hidden and self.spr is not None:
            self.spr.move((int(pos[0]), int(pos[1])))
        if self.label_block is not None:
            self.label_block.spr.move((int(pos[0] + self.label_xy[0]),
                                       int(pos[1] + self.label_xy[1])))
        return(self.x, self.y)

    def get_name(self):
        return self.name

    def get_xy(self):
        return(self.x, self.y)

    def get_heading(self):
        return(self.heading)

    def get_color(self):
        return(self.pen_color)

    def get_gray(self):
        return(self.pen_gray)

    def get_shade(self):
        return(self.pen_shade)

    def get_pen_size(self):
        return(self.pen_size)

    def get_pen_state(self):
        return(self.pen_state)

    def get_fill(self):
        return(self.pen_fill)

    def get_poly_points(self):
        return(self.poly_points)

    def right(self, degrees, share=True):
        ''' Rotate turtle clockwise '''
        try:
            self.heading += degrees
        except (TypeError, ValueError):
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return
        self.heading %= 360

        if self.tw.sharing() and share:
            event = 'r|%s' % (data_to_string([self.tw.nick,
                                              round_int(self.heading)]))
            self.tw.send_event(event)

    def forward(self, distance, share=True):
        scaled_distance = distance * self.tw.coord_scale

        self.tw.canvas.set_rgb(self.tw.canvas.fgrgb[0] / 255.,
                               self.tw.canvas.fgrgb[1] / 255.,
                               self.tw.canvas.fgrgb[2] / 255.)

        oldx, oldy = self.tw.canvas.get_xy()
        try:
            xcor = oldx + scaled_distance * sin(self.heading * DEGTOR)
            ycor = oldy + scaled_distance * cos(self.heading * DEGTOR)
        except (TypeError, ValueError):
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return

        self.tw.canvas.set_xy(xcor, ycor)
        if self.pen_state:
            self.tw.canvas.draw_line(oldx, oldy, xcor, ycor)
        if self.pen_fill:
            if self.poly_points == []:
                x, y = self.tw.canvas.turtle_to_screen_coordinates(oldx, oldy)
                self.poly_points.append(('move', x, y))
            x, y = self.tw.canvas.turtle_to_screen_coordinates(xcor, ycor)
            self.poly_points.append(('line', x, y))

        self.move_turtle((xcor, ycor))

        if self.tw.sharing() and share:
            event = 'f|%s' % (data_to_string([self.tw.nick,
                                              int(distance)]))
            self.tw.send_event(event)

    def set_xy(self, x, y, share=True, pendown=True):
        oldx, oldy = self.tw.canvas.get_xy()
        try:
            xcor = x * self.tw.coord_scale
            ycor = y * self.tw.coord_scale
            self.tw.canvas.set_xy(x, y)
        except (TypeError, ValueError):
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return

        if self.pen_state and pendown:
            self.tw.canvas.set_rgb(self.tw.canvas.fgrgb[0] / 255.,
                                   self.tw.canvas.fgrgb[1] / 255.,
                                   self.tw.canvas.fgrgb[2] / 255.)
            self.tw.canvas.draw_line(oldx, oldy, xcor, ycor)
        if self.pen_fill:
            if self.poly_points == []:
                x, y = self.tw.canvas.turtle_to_screen_coordinates(oldx, oldy)
                self.poly_points.append(('move', x, y))
            x, y = self.tw.canvas.turtle_to_screen_coordinates(xcor, ycor)
            self.poly_points.append(('line', x, y))

        self.move_turtle((xcor, ycor))

        if self.tw.sharing() and share:
            event = 'x|%s' % (data_to_string([self.tw.nick,
                                              [round_int(x), round_int(y)]]))
            self.tw.send_event(event)

    def arc(self, a, r, share=True):
        ''' Draw an arc '''
        if self.pen_state:
            self.tw.canvas.set_rgb(self.tw.canvas.fgrgb[0] / 255.,
                                   self.tw.canvas.fgrgb[1] / 255.,
                                   self.tw.canvas.fgrgb[2] / 255.)
        try:
            if a < 0:
                self.larc(-a, r)
            else:
                self.rarc(a, r)
        except (TypeError, ValueError):
            debug_output('bad value sent to %s' % (__name__),
                         self.tw.running_sugar)
            return

        xcor, ycor = self.tw.canvas.get_xy()
        self.move_turtle((xcor, ycor))

        if self.tw.sharing() and share:
            event = 'a|%s' % (data_to_string([self.tw.nick,
                                              [round_int(a), round_int(r)]]))
            self.tw.send_event(event)

    def rarc(self, a, r):
        ''' draw a clockwise arc '''
        r *= self.tw.coord_scale
        if r < 0:
            r = -r
            a = -a
        xcor, ycor = self.tw.canvas.get_xy()
        cx = xcor + r * cos(self.heading * DEGTOR)
        cy = ycor - r * sin(self.heading * DEGTOR)
        if self.pen_state:
            x, y = self.tw.canvas.turtle_to_screen_coordinates(cx, cy)
            self.tw.canvas.rarc(x, y, r, a, self.heading)

        if self.pen_fill:
            x, y = self.tw.canvas.turtle_to_screen_coordinates(x, y)
            if self.poly_points == []:
                self.poly_points.append(('move', x, y))
            self.poly_points.append(('rarc', x, y, r,
                                     (self.heading - 180) * DEGTOR,
                                     (self.heading - 180 + a) * DEGTOR))

        self.right(a, False)
        self.tw.canvas.set_xy(cx - r * cos(self.heading * DEGTOR),
                              cy + r * sin(self.heading * DEGTOR))

    def larc(self, a, r):
        ''' draw a counter-clockwise arc '''
        r *= self.tw.coord_scale
        if r < 0:
            r = -r
            a = -a
        xcor, ycor = self.tw.canvas.get_xy()
        cx = xcor - r * cos(self.heading * DEGTOR)
        cy = ycor + r * sin(self.heading * DEGTOR)
        if self.pen_state:
            x, y = self.tw.canvas.turtle_to_screen_coordinates(cx, cy)
            self.tw.canvas.larc(x, y, r, a, self.heading)

        if self.pen_fill:
            x, y = self.tw.canvas.turtle_to_screen_coordinates(x, y)
            if self.poly_points == []:
                self.poly_points.append(('move', x, y))
            self.poly_points.append(('larc', x, y, r,
                                     (self.heading) * DEGTOR,
                                     (self.heading - a) * DEGTOR))

        self.right(-a, False)
        self.tw.canvas.set_xy(cx + r * cos(self.heading * DEGTOR),
                              cy - r * sin(self.heading * DEGTOR))
