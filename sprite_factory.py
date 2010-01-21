#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright (c) 2009,10 Walter Bender

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
import os
from gettext import gettext as _

class SVG:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0
        self._width = 0
        self._height = 0
        self._scale = 1
        self._orientation = 0
        self._radius = 8
        self._stroke_width = 1
        self._innie = [False]
        self._outie = False
        self._innie_x1 = 4
        self._innie_y1 = 3
        self._innie_x2 = 4
        self._innie_y2 = 4
        self._innie_spacer = 9
        self._slot = True
        self._tab = True
        self._bool = False
        self._slot_x = 12
        self._slot_y = 2
        self._porch = False
        self._porch_x = self._innie_x1+self._innie_x2+4*self._stroke_width
        self._porch_y = self._innie_y1+self._innie_y2+4*self._stroke_width
        self._expand_x = 0
        self._expand_y = 0
        self._fill = "#00FF00"
        self._stroke = "#00A000"
        self._gradiant = False

    def basic_block(self):
        (x, y) = self._calculate_x_y()
        svg = self._new_path(x, y)
        svg += self._rarc_to(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._rarc_to(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
            if i==0 and self._porch is True:
                svg += self._do_porch()
            elif len(self._innie)-1 > i:
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._rline_to(0, self._expand_y)
        svg += self._rarc_to(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._do_tab()
        svg += self._rarc_to(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self._line_to(x,
                                 self._radius+self._innie_y2+self._stroke_width)
            svg += self._do_outie()
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def basic_flow(self):
        (x, y) = self._calculate_x_y()
        svg = self._new_path(x, y)
        svg += self._rarc_to(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._rarc_to(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        if self._bool is True:
            svg += self._rline_to(0,self._radius/2.0)
            svg += self._do_boolean()
            svg += self._rline_to(0,self._radius/2.0)
        svg += self._rline_to(self._radius+self._slot_x, 0)
        svg += self._rarc_to(1,1)
        svg += self._rline_to(-self._radius,0)
        svg += self._do_tab()
        svg += self._rline_to(-self._radius, 0)
        svg += self._rline_to(0, self._expand_y)
        svg += self._rarc_to(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._do_tab()
        svg += self._rarc_to(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self._line_to(x,
                                 self._radius+self._innie_y2+self._stroke_width)
            svg += self._do_outie()
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def basic_box(self):
        self.set_outie(True)
        x = self._stroke_width/2.0+self._innie_x1+self._innie_x2
        svg = self._new_path(x, self._stroke_width/2.0)
        svg += self._rline_to(self._expand_x, 0)
        svg += self._rline_to(0, 2*self._radius+self._innie_y2+self._expand_y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._line_to(x, self._radius+self._innie_y2+\
                                self._stroke_width/2.0)
        svg += self._do_outie()
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def boolean_and_or(self):
        svg = self._start_boolean(self._stroke_width/2.0,
                                  self._radius*5.5+self._stroke_width/2.0+\
                                  self._innie_y2+self._innie_spacer)
        svg += self._rline_to(0,-self._radius*3.5-self._innie_y2-\
                             self._innie_spacer-self._stroke_width)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius*1.5+self._innie_y2+\
                                self._innie_spacer)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._end_boolean()
        return self._header() + svg

    def boolean_not(self):
        svg = self._start_boolean(self._stroke_width/2.0,
                                  self._radius*2.0+self._stroke_width/2.0)
        svg += self._rline_to(0,-self._stroke_width)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._end_boolean()
        return self._header() + svg

    def boolean_compare(self):
        yoffset = self._radius*2+2*self._innie_y2+\
                  self._innie_spacer+self._stroke_width/2.0
        if self._porch is True:
            yoffset += self._porch_y
        svg = self._start_boolean(self._stroke_width/2.0, yoffset)
        yoffset = -2*self._innie_y2-self._innie_spacer-self._stroke_width
        if self._porch is True:
            yoffset -= self._porch_y
        svg += self._rline_to(0, yoffset)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        svg += self._rline_to(0,self._radius)
        xx = self._x
        svg += self._do_innie()
        if self._porch is True:
           svg += self._do_porch()
        else:
           svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._do_innie()
        svg += self._rline_to(0, self._radius)
        svg += self._line_to(xx, self._y)
        svg += self._end_boolean()
        return self._header() + svg

    def turtle(self):
        self._fill, self._stroke = "#D0D000", "none"
        svg = self._rect(21, 21, 19.5, 18)
        self._fill = "#808000"
        svg += self._rect(3, 3, 30, 24)
        svg += self._rect(3, 3, 24, 24)
        svg += self._rect(3, 3, 30, 30)
        svg += self._rect(3, 3, 24, 30)
        svg += self._rect(3, 3, 27, 27)
        svg += self._rect(3, 3, 21, 27)
        svg += self._rect(3, 3, 33, 27)
        svg += self._rect(3, 3, 27, 21)
        svg += self._rect(3, 3, 21, 21)
        svg += self._rect(3, 3, 33, 21)
        svg += self._rect(3, 3, 27, 33)
        svg += self._rect(3, 3, 21, 33)
        svg += self._rect(3, 3, 33, 33)
        svg += self._rect(3, 3, 30, 36)
        svg += self._rect(3, 3, 24, 36)
        svg += self._rect(3, 3, 30, 18)
        svg += self._rect(3, 3, 24, 18)
        svg += self._rect(3, 3, 36, 24)
        svg += self._rect(3, 3, 36, 30)
        svg += self._rect(3, 3, 36, 18)
        svg += self._rect(3, 3, 36, 36)
        self._fill, self._stroke = "#008000", "#008000"
        svg += self._turtle_body()
        self._fill, self._stroke = "#00a000", "#00a000"
        svg += self._turtle_shell()
        self._fill, self._stroke = "#000000", "#000000"
        svg += self._circle(1.25,32.5,8)
        svg += self._circle(1.25,27.5,8)
        svg += self._footer()
        self._width, self._height = 60, 60
        # TODO: Add orientation
        return self._header() + svg

    #
    # Utility methods
    #

    def set_scale(self, scale=1):
        self._scale = scale

    def set_orientation(self, orientation=0):
        self._orientation = orientation

    def expand(self, w=0, h=0):
        self._expand_x = w
        self._expand_y = h

    def set_stroke_width(self, stroke_width=1.5):
        self._stroke_width = stroke_width
        self._calc_porch_params()

    def set_colors(self, colors=["#00FF00","#00A000"]):
        self._fill = colors[0]
        self._stroke = colors[1]

    def set_fill_color(self, color="#00FF00"):
        self._fill = color

    def set_stroke_color(self, color="#00A000"):
        self._stroke = color

    def set_gradiant(self, flag=False):
        self._gradiant = flag

    def set_innie(self, innie_array=[False]):
        self._innie = innie_array

    def set_outie(self, flag=False):
        self._outie = flag

    def set_slot(self, flag=True):
        self._slot = flag

    def set_tab(self, flag=True):
        self._tab = flag

    def set_porch(self, flag=False):
        self._porch = flag

    def set_boolean(self, flag=False):
        self._bool = flag

    #
    # Exotic methods
    #

    def set_radius(self, radius=8):
        self._radius = radius

    def set_innie_params(self, x1=4, y1=3, x2=4, y2=4):
        self._innie_x1 = x1
        self._innie_y1 = y1
        self._innie_x2 = x2
        self._innie_y2 = y2
        self._calc_porch_params()

    def set_innie_spacer(self, innie_spacer = 0):
        self._innie_spacer = innie_spacer

    def set_slot_params(self, x=12, y=4):
        self._slot_x = x
        self._slot_y = y

    def _calc_porch_params(self):
        self._porch_x = self._innie_x1+self._innie_x2+4*self._stroke_width
        self._porch_y = self._innie_y1+self._innie_y2+4*self._stroke_width

    #
    # SVG helper methods
    #

    def _header(self):
        return "%s%s%s%s%s%s%s%s%.1f%s%s%.1f%s%s%s" % (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n",
            "<!-- Created with Python -->\n",
            "<svg\n",
            "   xmlns:svg=\"http://www.w3.org/2000/svg\"\n",
            "   xmlns=\"http://www.w3.org/2000/svg\"\n",
            "   xmlns:xlink=\"http://www.w3.org/1999/xlink\"",
            "   version=\"1.1\"\n",
            "   width=\"", self._width, "\"\n",
            "   height=\"", self._height, "\">\n",
            self._defs(),
            self._transform())

    def _defs(self):
        if self._gradiant is True:
            return "%s%s%s%s%s%s%s%s%s%s%s%s%.1f%s%s%.1f%s%s%.1f%s%s" % (
        "  <defs>\n    <linearGradient\n       id=\"linearGradient1234\">\n",
        "      <stop\n         style=\"stop-color:#ffffff;stop-opacity:1;\"\n",
        "         offset=\"0\" />\n",
        "      <stop\n         style=\"stop-color:", self._fill,
        ";stop-opacity:1;\"\n",
        "         offset=\"1\" />\n",
        "    </linearGradient>\n",
        "    <linearGradient\n       xlink:href=\"#linearGradient1234\"\n",
        "       id=\"linearGradient5678\"\n",
        "       x1=\"0\"\n",
        "       y1=\"", self._height/2.0, "\"\n",
        "       x2=\"", self._width, "\"\n",
        "       y2=\"", self._height/2.0, "\"\n",
        "       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n")
        else:
            return ""

    def _transform(self):
        return "%s%.1f%s%.1f%s" % (
        "<g\n       transform=\"scale(",self._scale,",",self._scale,")\">\n")

    def _footer(self):
        return "   </g>\n</svg>\n"

    def _style(self):
        if self._gradiant is True:
            fill = "url(#linearGradient5678)"
        else:
            fill = self._fill
        return "%s%s;%s%s;%s%.1f;%s%s" % (
               "       style=\"fill:",fill,
               "fill-opacity:1;stroke:",self._stroke,
               "stroke-width:",self._stroke_width,
               "stroke-linecap:square;",
               "stroke-opacity:1;\" />\n")

    def _circle(self, r, cx, cy):
        return "%s%s%s%s%s%f%s%f%s%f%s" % ("<circle style=\"fill:",
             self._fill, ";stroke:", self._stroke, ";\" r=\"", r, "\" cx=\"",
             cx, "\" cy=\"", cy, "\" />")

    def _rect(self, w, h, x, y):
        return "%s%s%s%s%s%f%s%f%s%f%s%f%s" % ("<rect style=\"fill:",
               self._fill, ";stroke:", self._stroke, ";\" width=\"", w,
               "\" height=\"", h,"\" x=\"", x, "\" y=\"", y, "\" />")

    def _turtle_body(self):
        return "%s%s%s%s%s" % ("<path style=\"", self._fill, ";stroke:",
               self._stroke, "\" d=\"M 20,42 C 21,41 23,40 24,40 C 24,39 24,40 26,41 C 28,43 31,43 34,41 C 35,40 35,39 36,40 C 36,40 38,41 39,42 C 41,42 45,43 46,43 C 47,43 46,41 43,39 L 39,36 L 42,34 C 44,30 45,28 43,25 L 41,22 L 46,18 C 48,16 47.5,13.5 47,13 C 46.5,12.5 46,13 45,13 C 44,13 43.5,14 42.5,15 C 39.5,17 40,18 37,17 C 32,16 31.5,15 34.5,12 C 36.5,10 36,7 34,6 C 32,3 28,4 26,6 C 24,8 23,10 25,12 C 28,15 27,16 22,17 C 18,18 19,17 17,15 C 16,14 16,13 15,13 C 14,13 13,13 13,13 C 12,13 11,16 14,18 L 19,22 L 17,25 C 15,28 16,30 18,34 L 20,36 L 16,39 C 13,41 12,43 13,43 C 14,43 18,42 20,42 z M 30,18 C 32,18 36,19 38,20 C 40,22 39.5,25 39.5,28 C 39.5,30 40,32.5 38.5,35 C 37,36.5 36.5,37.5 35,38 C 33.5,38.5 31,39 30,39 C 28,39 26,39 25,38 C 23,37 22.5,37 21.5,35 C 20.5,33 20.5,30 20.5,28 C 20.5,25 20,22 22,20 C 24,19 27,18 30,18 z\" />")

    def _turtle_shell(self):
        return "%s%s%s%s%s" % ("<path style=\"", self._fill, ";stroke:",
               self._stroke, "\" d=\"M 33,10 C 33,11 31.5,12 30,12 C 28,12 27,11 27,10 C 27,9 28,8 30,8 C 31.5,8 33,9 33,10 z\" />")

    def _check_min_max(self):
        if self._x < self._min_x:
            self._min_x = self._x
        if self._y < self._min_y:
            self._min_y = self._y
        if self._x > self._max_x:
            self._max_x = self._x
        if self._y > self._max_y:
            self._max_y = self._y

    def _line_to(self, x, y):
        if self._x == x and self._y == y:
            return ""
        else:
            self._x = x
            self._y = y
            self._check_min_max()
            return "L %.1f %.1f " % (x, y) 

    def _rline_to(self, dx, dy):
        if dx == 0 and dy == 0:
            return ""
        else:
            return self._line_to(self._x+dx, self._y+dy)

    def _arc_to(self, x, y, a=90, l=0, s=1):
        if self._radius == 0:
            return self._line_to(x, y)
        else:
            self._x = x
            self._y = y
            self._check_min_max()
            return "A %.1f %.1f %.1f %d %d %.1f %.1f " % (
                self._radius, self._radius, a, l, s, x, y)

    def _rarc_to(self, sign_x, sign_y, a=90, l=0, s=1):
        if self._radius == 0:
            return ""
        else:
            x = self._x + sign_x*self._radius
            y = self._y + sign_y*self._radius
            return self._arc_to(x, y, a, l, s)

    def _new_path(self, x, y):
        self._min_x = x
        self._min_y = y
        self._max_x = x
        self._max_y = y
        self._x = x
        self._y = y
        return "      <path d=\"m%.1f %.1f " % (x, y)

    def _close_path(self):
        return "z\"\n"

    def _do_slot(self):
        if self._slot is True:
            return "%s%s%s" % (
                self._rline_to(0, self._slot_y),
                self._rline_to(self._slot_x, 0),
                self._rline_to(0, -self._slot_y))
        else:
            return self._rline_to(self._slot_x, 0)

    def _do_tab(self):
        if self._tab is True:
            return "%s%s%s%s%s" % (
                self._rline_to(-self._stroke_width, 0),
                self._rline_to(0, self._slot_y),
                self._rline_to(-self._slot_x+2*self._stroke_width, 0),
                self._rline_to(0, -self._slot_y),
                self._rline_to(-self._stroke_width, 0))
        else:
            return self._rline_to(-self._slot_x, 0)

    def _do_innie(self):
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, -self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, self._innie_y2+2*self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, -self._innie_y1),          
            self._rline_to(self._innie_x1, 0))

    def _do_outie(self):
        if self._outie is not True:
            return self._rline_to(0, -self._innie_y2)
        return "%s%s%s%s%s%s%s%s%s" % (
            self._rline_to(0, -self._stroke_width),
            self._rline_to(-self._innie_x1-2*self._stroke_width, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(-self._innie_x2+2*self._stroke_width, 0),
            self._rline_to(0,
                -self._innie_y2-2*self._innie_y1+2*self._stroke_width),
            self._rline_to(self._innie_x2-2*self._stroke_width, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(self._innie_x1+2*self._stroke_width, 0),
            self._rline_to(0, -self._stroke_width))

    def _do_porch(self):
         return "%s%s%s" % (
            self._rline_to(0, self._porch_y),
            self._rline_to(self._porch_x-self._radius, 0),
            self._rarc_to(1, 1))

    def _start_boolean(self, xoffset, yoffset):
        svg = self._new_path(xoffset, yoffset)
        self._radius -= self._stroke_width
        svg += self._rarc_to(1, -1)
        self._radius += self._stroke_width
        return svg + self._rline_to(self._stroke_width, 0)

    def _do_boolean(self):
        return self._rarc_to(-1, 1, 90, 0, 0) + self._rarc_to(1, 1, 90, 0, 0)

    def _end_boolean(self):
        svg = self._rline_to(-self._radius*1.5,0)
        svg += self._rline_to(0, -self._stroke_width)
        svg += self._rline_to(-self._stroke_width, 0)
        self._radius -= self._stroke_width
        svg += self._rarc_to(-1, -1)
        self._radius += self._stroke_width
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        return svg + self._footer()

    def _calculate_w_h(self):
        self._width = (self._max_x-self._min_x+self._stroke_width)*\
                      self._scale
        self._height = (self._max_y-self._min_y+self._stroke_width)*\
                      self._scale

    def _calculate_x_y(self):
        if self._outie is True:
            return(self._stroke_width/2.0+self._innie_x1+self._innie_x2,
                   self._radius+self._stroke_width/2.0)
        else:
            return(self._stroke_width/2.0, self._radius+self._stroke_width/2.0)

#
# Command-line tools for testing
#

def open_file(datapath, filename):
    return file(os.path.join(datapath, filename), "w")

def close_file(f):
    f.close()

def generator(datapath):
    svg0 = SVG()
    f = open_file(datapath, "flow-test.svg")
    svg0.set_scale(1)
    svg0.expand(20,0)
    # svg0.set_innie([True])
    svg0.set_boolean(True)
    svg0.set_tab(True)
    svg0.set_gradiant(True)
    svg_str = svg0.basic_flow()
    f.write(svg_str)
    close_file(f)

    svg1 = SVG()
    f = open_file(datapath, "blob-test.svg")
    svg1.set_scale(1)
    svg1.expand(20,0)
    svg1.set_innie([True,True])
    svg1.set_tab(False)
    svg1.set_gradiant(True)
    svg_str = svg1.basic_block()
    f.write(svg_str)
    close_file(f)

    svg2 = SVG()
    f = open_file(datapath, "box-test.svg")
    svg2.set_scale(1)
    svg2.expand(40,0)
    svg2.set_colors(["#FFA000","#A08000"])
    svg2.set_gradiant(True)
    svg_str = svg2.basic_box()
    f.write(svg_str)
    close_file(f)

    svg3 = SVG()
    f = open_file(datapath, "compare-text.svg")
    svg3.set_scale(1)
    svg3.set_colors(["#0000FF","#0000A0"])
    svg3.set_gradiant(True)
    # svg3.set_porch(True)
    svg_str = svg3.boolean_compare()
    f.write(svg_str)
    close_file(f)

    svg4 = SVG()
    f = open_file(datapath, "and-or-test.svg")
    svg4.set_scale(1)
    svg4.set_colors(["#00FFFF","#00A0A0"])
    svg4.set_gradiant(True)
    svg_str = svg4.boolean_and_or()
    f.write(svg_str)
    close_file(f)

    svg5 = SVG()
    f = open_file(datapath, "nor-test.svg")
    svg5.set_scale(1)
    svg5.set_colors(["#FF00FF","#A000A0"])
    svg5.set_gradiant(True)
    svg_str = svg5.boolean_not()
    f.write(svg_str)
    close_file(f)

def main():
    return 0

if __name__ == "__main__":
    generator(os.path.abspath('.'))
    main()


#
# Load pixbuf from SVG string
#
def svg_str_to_pixbuf(svg_string):
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf

