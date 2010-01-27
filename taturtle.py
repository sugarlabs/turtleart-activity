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
    def __init__(self):
        self.list = []

    def get_turtle(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self, turtle):
        self.list.append(turtle)

    def remove_from_list(self, turtle):
        if block in self.list:
            self.list.remove(turtle)

    #
    # sprite utilities
    #
    def spr_to_turtle(self, spr):
        for b in self.list:
            if spr == b.spr:
                return b
        return None

#
# A class for the individual turtles
#
class Turtle:
    # The turtle is not a block, just a sprite with an orientation
    def __init__(self, turtle_list, sprite_list,
                       colors=["#008000", "#00A000"], scale=1.0):
        self.shapes = []
        self.type = 'turtle'
        _svg = SVG()
        _svg.set_scale(scale)
        self.spr = sprites.Sprite(sprite_list, 0, 0,
                       svg_str_to_pixbuf(_svg.turtle(colors)))
        turtle_list.append_to_list(self)
        for i in range(36):
            _svg.set_orientation(i*10)
            self.shapes.append(svg_str_to_pixbuf(_svg.turtle(colors)))

    def rotate(self, orientation):
        try:
            self.spr.set_shape(self.shapes[orientation])
        except IndexError:
            self.spr.set_shape(self.shapes[0])
            print "Turtle shape IndexError %d" % orientation
