# -*- coding: utf-8 -*-
#Copyright (c) 2010 Walter Bender

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

from taconstants import TURTLE_LAYER
from tasprite_factory import SVG, svg_str_to_pixbuf
from sprites import Sprite

def generate_turtle_pixbufs(colors):
    """ Generate pixbufs for generic turtles """
    shapes = []
    svg = SVG()
    svg.set_scale(1.0)
    for i in range(36):
        svg.set_orientation(i*10)
        shapes.append(svg_str_to_pixbuf(svg.turtle(colors)))
    return shapes

#
# A class for the list of blocks and everything they share in common
#
class Turtles:
    def __init__(self, sprite_list):
        """ Class to hold turtles """
        self.dict = dict()
        self.sprite_list = sprite_list
        self.default_pixbufs = []

    def get_turtle(self, k, append=False, colors=None):
        """ Find a turtle """
        if self.dict.has_key(k):
            return self.dict[k]
        elif append is False:
            return None
        else:
            if colors == None:
                Turtle(self, k)
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
        if self.dict.has_key(k):
            del(self.dict[k])

    def show_all(self):
        """ Make all turtles visible """
        for k in iter(self.dict):
            self.dict[k].show()

    #
    # sprite utilities
    #
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

#
# A class for the individual turtles
#
class Turtle:
    def __init__(self, turtles, key, colors=None):
        """ The turtle is not a block, just a sprite with an orientation """
        self.x = 0
        self.y = 0
        self.hidden = False
        self.shapes = []
        self.type = 'turtle'
        self.heading = 0
        self.pen_shade = 50
        self.pen_color = 0
        self.pen_gray = 100
        self.pen_size = 5
        self.pen_state = True

        if colors is None:
            self.shapes = turtles.get_pixbufs()
        else:
            self.colors = colors[:]
            self.shapes = generate_turtle_pixbufs(self.colors)

        if turtles.sprite_list is not None:
            self.spr = Sprite(turtles.sprite_list, 0, 0, self.shapes[0])
        else:
            self.spr = None
        turtles.add_to_dict(key, self)

    def set_heading(self, heading):
        """ Set the turtle heading (and shape: one per 10 degrees) """
        self.heading = heading        
        i = (int(self.heading+5)%360)/10
        if self.hidden is False and self.spr is not None:
            try:
                self.spr.set_shape(self.shapes[i])
            except IndexError:
                self.spr.set_shape(self.shapes[0])
                print "Turtle shape IndexError %f -> %d" % (heading, i)

    def set_color(self, color):
        """ Set the pen color for this turtle. """
        self.pen_color = color

    def set_gray(self, gray):
        """ Set the pen gray level for this turtle. """
        self.pen_gray = gray

    def set_shade(self, shade):
        """ Set the pen shade for this turtle. """
        self.pen_shade = shade

    def set_pen_size(self, pen_size):
        """ Set the pen size for this turtle. """
        self.pen_size = pen_size

    def set_pen_state(self, pen_state):
        """ Set the pen state (down==True) for this turtle. """
        self.pen_state = pen_state

    def hide(self):
        """ Hide the turtle. """
        if self.spr is not None:
            self.spr.hide()
        self.hidden = True

    def show(self):
        """ Show the turtle. """
        if self.spr is not None:
            self.spr.set_layer(TURTLE_LAYER)
            self.hidden = False
        self.move((self.x, self.y))
        self.set_heading(self.heading)

    def move(self, pos):
        """ Move the turtle. """
        self.x, self.y = pos[0], pos[1]
        if self.hidden is False and self.spr is not None:
            self.spr.move(pos)
        return(self.x, self.y)

    def get_xy(self):
        """ Return the turtle's x, y coordinates. """
        return(self.x, self.y)

    def get_heading(self):
        """ Return the turtle's heading. """
        return(self.heading)

    def get_color(self):
        """ Return the turtle's color. """
        return(self.pen_color)

    def get_gray(self):
        """ Return the turtle's gray level. """
        return(self.pen_gray)

    def get_shade(self):
        """ Return the turtle's shade. """
        return(self.pen_shade)

    def get_pen_size(self):
        """ Return the turtle's pen size. """
        return(self.pen_size)

    def get_pen_state(self):
        """ Return the turtle's pen state. """
        return(self.pen_state)
