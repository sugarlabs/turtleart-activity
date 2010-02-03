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

from constants import *
from sprite_factory import SVG, svg_str_to_pixbuf
import sprites
from gettext import gettext as _

#
# A class for the list of blocks and everything they share in common
#
class Turtles:
    def __init__(self, sprite_list):
        self.list = []
        self.sprite_list = sprite_list

    def get_turtle(self, i, append=False):
        if i < 0:
            print "IndexError: Turtles %d" % (i)
            return self.list[0]
        elif i > len(self.list)-1:
            if append is False:
                print "IndexError: Turtles %d" % (i)
                return self.list[0]
            else:
                for t in range(i-len(self.list)+1):
                    Turtle(self)
                return(self.list[i])
        else:
            return(self.list[i])

    def turtle_count(self):
        return(len(self.list))

    def append_to_list(self, turtle):
        self.list.append(turtle)

    def remove_from_list(self, turtle):
        if turtle in self.list:
            self.list.remove(turtle)

    def show_all(self):
        for turtle in self.list:
            turtle.show()

    #
    # sprite utilities
    #
    def spr_to_turtle(self, spr):
        for turtle in self.list:
            if spr == turtle.spr:
                return turtle
        return None

#
# A class for the individual turtles
#
class Turtle:
    # The turtle is not a block, just a sprite with an orientation
    def __init__(self, turtle_list,
                       colors=["#008000", "#00A000", "#D0D000", "#808000"],
                       scale=1.0):
        self.x = 0
        self.y = 0
        self.hidden = False
        self.shapes = []
        self.type = 'turtle'
        self.heading = 0
        self.pen_shade = 50
        self.pen_color = 0
        self.pen_size = 5
        self.pen_state = True

        if len(colors) == 2:
            _colors = colors[:]
            _colors.append(colors[0])
            _colors.append(colors[1])
        elif len(colors) == 4:
            _colors=colors[:]
        else:
            _colors=["#008000", "#00A000", "#D0D000", "#808000"]

        _svg = SVG()
        _svg.set_scale(scale)
        self.spr = sprites.Sprite(turtle_list.sprite_list, self.x, self.y,
                       svg_str_to_pixbuf(_svg.turtle(_colors)))
        turtle_list.append_to_list(self)
        for i in range(36):
            _svg.set_orientation(i*10)
            self.shapes.append(svg_str_to_pixbuf(_svg.turtle(_colors)))

    def set_heading(self, heading):
        self.heading = heading        
        i = (int(self.heading+5)%360)/10
        try:
            if self.hidden is False:
                self.spr.set_shape(self.shapes[i])
        except IndexError:
            if self.hidden is False:
                self.spr.set_shape(self.shapes[0])
            print "Turtle shape IndexError %f -> %d" % (heading, i)

    def set_color(self, color):
        self.pen_color = color

    def set_shade(self, shade):
        self.pen_shade = shade

    def set_pen_size(self, pen_size):
        self.pen_size = pen_size

    def set_pen_state(self, pen_state):
        self.pen_state = pen_state

    def hide(self):
        self.spr.set_layer(HIDE_LAYER)
        self.hidden = True

    def show(self):
        self.spr.set_layer(TURTLE_LAYER)
        self.hidden = False
        self.move((self.x, self.y))
        self.set_heading(self.heading)

    def move(self, pos):
        self.x, self.y = pos[0], pos[1]
        if self.hidden is False:
            self.spr.move(pos)

    def get_xy(self):
        return(self.x, self.y)

    def get_heading(self):
        return(self.heading)

    def get_color(self):
        return(self.pen_color)

    def get_shade(self):
        return(self.pen_shade)

    def get_pen_size(self):
        return(self.pen_size)

    def get_pen_state(self):
        return(self.pen_state)
