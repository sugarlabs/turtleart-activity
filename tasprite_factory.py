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
        self.docks = []
        self._scale = 1
        self._orientation = 0
        self._radius = 8
        self._stroke_width = 1
        self._innie = [False]
        self._outie = False
        self._innie_x1 = (9-self._stroke_width)/2
        self._innie_y1 = 3
        self._innie_x2 = (9-self._stroke_width)/2
        self._innie_y2 = (9-self._stroke_width)/2
        self._innie_spacer = 9
        self._slot = True
        self._cap = False
        self._tab = True
        self._bool = False
        self._slot_x = 10
        self._slot_y = 2
        self._porch = False
        self._porch_x = self._innie_x1+self._innie_x2+4*self._stroke_width
        self._porch_y = self._innie_y1+self._innie_y2+4*self._stroke_width
        self._expand_x = 0
        self._expand_y = 0
        self._else = False
        self._draw_innies = True
        self._hide = False
        self._show = False
        self._show_x = 0
        self._show_y = 0
        self._hide_x = 0
        self._hide_y = 0
        self._dot_radius = 8
        self._fill = "#00FF00"
        self._stroke = "#00A000"
        self._gradiant = False
        self.margins = [0, 0, 0, 0]

    def basic_block(self):
        (x, y) = self._calculate_x_y()
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
            if i==0 and self._porch is True:
                svg += self._do_porch()
            elif len(self._innie)-1 > i:
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        if self._tab:
            svg += self._do_tab()
        else:
            svg += self._do_tail()
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self._line_to(x, self._radius+self._innie_y2+\
                                    self._stroke_width/2.0)
            svg += self._do_outie()
        self._calculate_w_h()
        svg += self._close_path()
        svg += self._style()
        if self._show is True:
            svg += self._show_dot()
        if self._hide is True:
            svg += self._hide_dot()

        svg += self._footer()
        return self._header() + svg

    def basic_flow(self):
        (x, y) = self._calculate_x_y()
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        xx = self._x
        svg += self._rline_to(self._expand_x, 0)
        if self._bool:
            svg += self._corner(1, 1, 90, 0, 1, True, False)
        elif True in self._innie:
            svg += self._corner(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
                svg += self._rline_to(0, self._innie_spacer)
            else:
                self.margins[2] =\
                    int((self._x-self._stroke_width+0.5)*self._scale)
        if self._bool is True:
            svg += self._rline_to(0,self._radius/2.0)
            svg += self._do_boolean()
            svg += self._rline_to(0,self._stroke_width)
        if self._else:
            svg += self._rline_to(self._radius*3+self._slot_x*2, 0)
        else:
            svg += self._rline_to(self._radius+self._slot_x, 0)
        hh = self._x
        svg += self._corner(1, 1)
        svg += self._rline_to(-self._radius,0)
        if self._else:
            svg += self._do_tab()
            svg += self._rline_to(-self._radius*2, 0)
        svg += self._do_tab()
        svg += self._inverse_corner(-1, 1, 90, 0, 0, True, False)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1, 90, 0, 1, False, True)
        svg += self._line_to(xx, self._y)
        if self._tab:
            svg += self._do_tab()
        else:
            svg += self._do_tail()
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self._line_to(x, self._radius+self._innie_y2+\
                                    self._stroke_width)
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        if self._hide is True:
            svg += self._hide_dot()
        if self._show is True:
            svg += self._show_dot()
        svg += self._footer()
        return self._header() + svg

    def portfolio(self):
        (x, y) = self._calculate_x_y()
        self.margins[0] = int(x+2*self._stroke_width+0.5)
        self.margins[1] = int(y+self._stroke_width+0.5+self._slot_y)
        self.margins[2] = 0
        self.margins[3] = 0
        x += self._innie_x1+self._innie_x2
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        xx = self._x
        svg += self._rline_to(self._expand_x, 0)
        svg += self._corner(1, 1)
        svg += self._rline_to(0, self._expand_y)
        for i in range(len(self._innie)):
            if self._innie[i] is True and i > 0 and self._draw_innies:
                svg += self._do_innie()
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
            else:
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._corner(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._do_tab()
        svg += self._corner(-1, -1)
        for i in range(len(self._innie)):
            if self._innie[len(self._innie)-i-1] is True:
                svg += self._rline_to(0, -2*self._innie_y2-self._innie_spacer)
                svg += self._do_reverse_innie()
            else:
                svg += self._rline_to(0, -2*self._innie_y2-self._innie_spacer)
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def basic_box(self):
        self.set_outie(True)
        x = self._stroke_width/2.0+self._innie_x1+self._innie_x2
        self.margins[0] = int((x+self._stroke_width+0.5)*self._scale)
        self.margins[1] = int((self._stroke_width+0.5)*self._scale)
        self.margins[2] = 0
        self.margins[3] = 0
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
        xx = self._x
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius*1.5+self._innie_y2+\
                                self._innie_spacer)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        self.margins[0] = int((self._radius+self._stroke_width+0.5)*self._scale)
        self.margins[1] = int(self._stroke_width*self._scale)
        self.margins[2] = int(self._stroke_width*self._scale)
        self.margins[3] = int(self._stroke_width*self._scale)
        return self._header() + svg

    def boolean_not(self):
        svg = self._start_boolean(self._stroke_width/2.0,
                                  self._radius*2.0+self._stroke_width/2.0)
        svg += self._rline_to(0,-self._stroke_width)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        xx = self._x
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        self.margins[0] = int((self._radius+self._stroke_width+0.5)*self._scale)
        self.margins[1] = int(self._stroke_width*self._scale)
        self.margins[2] = int((self._radius+self._stroke_width+0.5)*self._scale)
        self.margins[3] = int(self._stroke_width*self._scale)
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
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        self.margins[0] = int((self._radius+self._stroke_width)*self._scale)
        self.margins[1] = int(self._stroke_width*self._scale)
        self.margins[2] = int(self._stroke_width*self._scale)
        self.margins[3] = int(self._stroke_width*self._scale)
        return self._header() + svg

    def turtle(self, colors):
        self._fill, self._stroke = colors[0], colors[1]
        svg = "  <path d=\"M 27.497 48.279 C 26.944 48.279 26.398 48.244 25.86 48.179 L 27.248 50.528 L 28.616 48.215 C 28.245 48.245 27.875 48.279 27.497 48.279 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "   <path d=\"M 40.16 11.726 C 37.996 11.726 36.202 13.281 35.817 15.333 C 37.676 16.678 39.274 18.448 40.492 20.541 C 42.777 20.369 44.586 18.48 44.586 16.151 C 44.586 13.707 42.604 11.726 40.16 11.726 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "   <path d=\"M 40.713 39.887 C 39.489 42.119 37.853 44.018 35.916 45.443 C 36.437 47.307 38.129 48.682 40.16 48.682 C 42.603 48.682 44.586 46.702 44.586 44.258 C 44.586 42.003 42.893 40.162 40.713 39.887 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "   <path d=\"M 14.273 39.871 C 12.02 40.077 10.249 41.95 10.249 44.258 C 10.249 46.701 12.229 48.682 14.673 48.682 C 16.737 48.682 18.457 47.262 18.945 45.35 C 17.062 43.934 15.47 42.061 14.273 39.871 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "   <path d=\"M 19.026 15.437 C 18.683 13.334 16.872 11.726 14.673 11.726 C 12.229 11.726 10.249 13.707 10.249 16.15 C 10.249 18.532 12.135 20.46 14.494 20.556 C 15.68 18.513 17.226 16.772 19.026 15.437 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "  <path d=\"M 27.497 12.563 C 29.405 12.563 31.225 12.974 32.915 13.691 C 33.656 12.615 34.093 11.314 34.093 9.908 C 34.093 6.221 31.104 3.231 27.416 3.231 C 23.729 3.231 20.74 6.221 20.74 9.908 C 20.74 11.336 21.192 12.657 21.956 13.742 C 23.68 12.993 25.543 12.563 27.497 12.563 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "   <path d=\"M 43.102 30.421 C 43.102 35.1554 41.4568 39.7008 38.5314 43.0485 C 35.606 46.3963 31.6341 48.279 27.497 48.279 C 23.3599 48.279 19.388 46.3963 16.4626 43.0485 C 13.5372 39.7008 11.892 35.1554 11.892 30.421 C 11.892 20.6244 18.9364 12.563 27.497 12.563 C 36.0576 12.563 43.102 20.6244 43.102 30.421 Z\" stroke_width=\"3.5\" fill=\"" + self._fill + ";\" stroke=\"" + self._stroke + "\" />\n"
        svg += "   <path d=\"M 25.875 33.75 L 24.333 29.125 L 27.497 26.538 L 31.112 29.164 L 29.625 33.833 Z\" stroke_width=\"3.5\" fill=\"" + self._stroke + ";\" stroke=\"none\" />\n"
        svg += "   <path d=\"M 27.501 41.551 C 23.533 41.391 21.958 39.542 21.958 39.542 L 25.528 35.379 L 29.993 35.547 L 33.125 39.667 C 33.125 39.667 30.235 41.661 27.501 41.551 Z\" stroke_width=\"3.5\" fill=\"" + self._stroke + ";\" stroke=\"none\" />\n"
        svg += "   <path d=\"M 18.453 33.843 C 17.604 30.875 18.625 26.959 18.625 26.959 L 22.625 29.126 L 24.118 33.755 L 20.536 37.988 C 20.536 37.987 19.071 35.998 18.453 33.843 Z\" stroke_width=\"3.5\" fill=\"" + self._stroke + ";\" stroke=\"none\" />\n"
        svg += "   <path d=\"M 19.458 25.125 C 19.458 25.125 19.958 23.167 22.497 21.303 C 24.734 19.66 26.962 19.583 26.962 19.583 L 26.925 24.564 L 23.404 27.314 L 19.458 25.125 Z\" stroke_width=\"3.5\" fill=\"" + self._stroke + ";\" stroke=\"none\" />\n"
        svg += "   <path d=\"M 32.084 27.834 L 28.625 24.959 L 29 19.75 C 29 19.75 30.834 19.708 32.959 21.417 C 35.187 23.208 36.321 26.4 36.321 26.4 L 32.084 27.834 Z\" stroke_width=\"3.5\" fill=\"" + self._stroke + ";\" stroke=\"none\" />\n"
        svg += "   <path d=\"M 31.292 34.042 L 32.605 29.578 L 36.792 28.042 C 36.792 28.042 37.469 30.705 36.75 33.709 C 36.21 35.965 34.666 38.07 34.666 38.07 L 31.292 34.042 Z\" stroke_width=\"3.5\" fill=\"" + self._stroke + ";\" stroke=\"none\" />\n"
        self._width, self._height = 55, 55
        svg += self._footer()
        return self._header() + svg

    def palette(self, width, height):
        self._width, self._height = width, height
        self._fill, self._stroke = "#FFD000", "none"
        svg = self._rect(width, height, 0, 0)
        self._hide_x = (width-self._radius*1.5)/2
        self._hide_y = (height-self._radius*1.5)/2
        svg += self._hide_dot(True)
        svg += self._footer()
        return self._header() + svg

    def toolbar(self, width, height):
        self._width, self._height = width, height
        self._fill, self._stroke = "#282828", "none"
        svg = self._rect(width, height, 0, 0)
        svg += self._footer()
        return self._header() + svg

    def sandwich_top(self):
        x = self._stroke_width/2.0
        y = self._stroke_width/2.0+self._radius
        self.margins[0] = int((x+self._stroke_width+0.5)*self._scale)
        self.margins[1] = int((self._stroke_width+0.5)*self._scale)
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._rline_to(self._radius+self._stroke_width, 0)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        svg += self._do_innie()
        svg += self._corner(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._do_tab()
        svg += self._inverse_corner(-1, 1, 90, 0, 0)
        svg += self._rline_to(0, self._expand_y)
        svg += self._rline_to(-self._radius, 0)
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def sandwich_bottom(self):
        x = self._stroke_width/2.0
        y = self._stroke_width/2.0
        self.margins[0] = int((x+self._stroke_width+0.5)*self._scale)
        self.margins[1] = int((self._stroke_width+0.5)*self._scale)
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._rline_to(self._radius, 0)
        svg += self._rline_to(0, self._expand_y)
        svg += self._inverse_corner(1, 1, 90, 0, 0)
        svg += self._do_slot()
        svg += self._rline_to(self._radius, 0)
        svg += self._corner(-1, 1)
        svg += self._do_tab()
        svg += self._rline_to(-self._radius-self._stroke_width,0)
        svg += self._corner(-1, -1)
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        self._hide_x = x + self._radius/2
        self._hide_y = y + self._radius/2
        if self._hide is True:
            svg += self._hide_dot()
        if self._show is True:
            svg += self._show_dot()
        svg += self._footer()
        return self._header() + svg

    #
    # Utility methods
    #
    def set_draw_innies(self, flag=True):
        self._draw_innies = flag

    def set_hide(self, flag=False):
        self._hide = flag

    def set_show(self, flag=False):
        self._show = flag

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_innie_width(self):
        return (self._innie_x1+self._innie_x2)*self._scale

    def get_slot_depth(self):
        return self._slot_y*self._scale

    def clear_docks(self):
        self.docks = []

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
        if self._slot is True:
            self._cap = False

    def set_cap(self, flag=False):
        self._cap = flag
        if self._cap is True:
            self._slot = False

    def set_tab(self, flag=True):
        self._tab = flag

    def set_porch(self, flag=False):
        self._porch = flag

    def set_boolean(self, flag=False):
        self._bool = flag

    def set_else(self, flag=False):
        self._else = flag

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
            "   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n",
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
        "       x2=\"", self._width/self._scale, "\"\n",
        "       y2=\"", self._height/2.0, "\"\n",
        "       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n")
        else:
            return ""

    def _transform(self):
        if self._orientation != 0:
            orientation = "<g\ntransform = \"rotate(%.1f %.1f %.1f)\">\n" % (
                self._orientation, self._width/2.0, self._height/2.0)
        else:
            orientation = ""
        return "<g\ntransform=\"scale(%.1f, %.1f)\">\n%s" % (
                self._scale, self._scale, orientation )

    def _footer(self):
        if self._orientation != 0:
            return "   </g>\n</g>\n</svg>\n"
        else:
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
             cx, "\" cy=\"", cy, "\" />\n")

    def _rect(self, w, h, x, y):
        return "%s%s%s%s%s%f%s%f%s%f%s%f%s" % ("<rect style=\"fill:",
               self._fill, ";stroke:", self._stroke, ";\" width=\"", w,
               "\" height=\"", h,"\" x=\"", x, "\" y=\"", y, "\" />\n")

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

    def _arc_to(self, x, y, r, a=90, l=0, s=1):
        if r == 0:
            return self._line_to(x, y)
        else:
            self._x = x
            self._y = y
            self._check_min_max()
            return "A %.1f %.1f %.1f %d %d %.1f %.1f " % (
                r, r, a, l, s, x, y)

    def _rarc_to(self, sign_x, sign_y, a=90, l=0, s=1):
        if self._radius == 0:
            return ""
        else:
            x = self._x + sign_x*self._radius
            y = self._y + sign_y*self._radius
            return self._arc_to(x, y, self._radius, a, l, s)

    def _inverse_corner(self, sign_x, sign_y, a=90, l=0, s=1, start=True,
                                                                 end=True):
        r2 = self._stroke_width+self._radius/2.0
        if start:
            if sign_x*sign_y == -1:
                svg_str =self._rline_to(sign_x*(r2-self._stroke_width), 0)
            else:
                svg_str =self._rline_to(0, sign_y*+(r2-self._stroke_width))
        x = self._x + sign_x*r2
        y = self._y + sign_y*r2
        svg_str += self._arc_to(x, y, r2, a, l, s)
        if end:
            if sign_x*sign_y == -1:
                svg_str +=self._rline_to(0, sign_y*(r2-self._stroke_width))
            else:
                svg_str +=self._rline_to(sign_x*(r2-self._stroke_width), 0)
        return svg_str

    def _corner(self, sign_x, sign_y, a=90, l=0, s=1, start=True, end=True):
        svg_str = ""
        if sign_x == 1 and sign_y == -1:
            self._hide_x = self._x + self._radius/2
            self._hide_y = self._y - self._radius/2
        if sign_x == -1 and sign_y == 1:
            self._show_x = self._x - self._radius/2
            self._show_y = self._y + self._radius/2
            if True in self._innie:
                self._show_x -= (self._innie_x1+self._innie_x2)
                self._show_y -= (self._innie_y1+self._innie_y2)
        if self._radius > 0:
            r2 = self._radius/2.0
            if start:
                if sign_x*sign_y == 1:
                    svg_str +=self._rline_to(sign_x*r2, 0)
                else:
                    svg_str +=self._rline_to(0, sign_y*r2)
            x = self._x + sign_x*r2
            y = self._y + sign_y*r2
            svg_str += self._arc_to(x, y, r2, a, l, s)
            if end:
                if sign_x*sign_y == 1:
                    svg_str +=self._rline_to(0, sign_y*r2)
                else:
                    svg_str +=self._rline_to(sign_x*r2, 0)
        return svg_str

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

    def _hide_dot(self, noscale=False):
        _saved_fill, _saved_stroke = self._fill, self._stroke
        self._fill, self._stroke = "#FF0000", "#FF0000"
        svg = "</g>/n<g>/n"
        if noscale:
            scale = 2.0
        else:
            scale = self._scale
        scale2 = scale/2
        svg += self._circle(self._dot_radius*scale2, self._hide_x*scale,
                                                    self._hide_y*scale)
        self._fill, self._stroke = "#FFFFFF", "#FFFFFF"
        svg += self._rect(10*scale2, 2*scale2, self._hide_x*scale-5*scale2,
                                             self._hide_y*scale-scale+scale2)
        self._fill, self._stroke = _saved_fill, _saved_stroke
        return svg

    def _show_dot(self, noscale=False):
        _saved_fill, _saved_stroke = self._fill, self._stroke
        self._fill, self._stroke = "#00FE00", "#00FE00"
        svg = "</g>/n<g>/n"
        if noscale:
            scale = 2.0
        else:
            scale = self._scale
        scale2 = scale/2
        svg += self._circle(self._dot_radius*scale2, self._show_x*scale,
                                                    self._show_y*scale)
        self._fill, self._stroke = "#FEFEFE", "#FEFEFE"
        svg += self._rect(10*scale2, 2*scale2, self._show_x*scale-5*scale2,
                                             self._show_y*scale-scale+scale2)
        svg += self._rect(2*scale2, 10*scale2, self._show_x*scale-scale+scale2,
                                             self._show_y*scale-5*scale2)
        self._fill, self._stroke = _saved_fill, _saved_stroke
        return svg

    def _do_slot(self):
        if self._slot is True:
            self.docks.append((int(self._x*self._scale),
                               int(self._y*self._scale)))
            return "%s%s%s" % (
                self._rline_to(0, self._slot_y),
                self._rline_to(self._slot_x, 0),
                self._rline_to(0, -self._slot_y))
        elif self._cap is True:
            return "%s%s" % (
                self._rline_to(self._slot_x/2.0, -self._slot_y*2.0),
                self._rline_to(self._slot_x/2.0, self._slot_y*2.0))
        else:
            return self._rline_to(self._slot_x, 0)

    def _do_tail(self):
        if self._outie is True:
            return self._rline_to(-self._slot_x, 0)
        else:
            return "%s%s" % (
                self._rline_to(-self._slot_x/2.0, self._slot_y*2.0),
                self._rline_to(-self._slot_x/2.0, -self._slot_y*2.0))

    def _do_tab(self):
        s = "%s%s%s%s%s" % (
            self._rline_to(-self._stroke_width, 0),
            self._rline_to(0, self._slot_y),
            self._rline_to(-self._slot_x+2*self._stroke_width, 0),
            self._rline_to(0, -self._slot_y),
            self._rline_to(-self._stroke_width, 0))
        self.docks.append((int(self._x*self._scale),
                           int((self._y+self._stroke_width)*self._scale)))
        return s

    def _do_innie(self):
        self.docks.append((int((self._x+self._stroke_width)*self._scale),
                           int((self._y+self._innie_y2)*self._scale)))
        if self.margins[2] == 0:
            self.margins[1] = int((self._y-self._innie_y1)*self._scale)
            self.margins[2] = int((self._x-self._innie_x1-self._innie_x2-\
                                  self._stroke_width*2)*self._scale)
        self.margins[3] =\
            int((self._y+self._innie_y2+self._innie_y1)*self._scale)
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, -self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, self._innie_y2+2*self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, -self._innie_y1),          
            self._rline_to(self._innie_x1, 0))

    def _do_reverse_innie(self):
        self.docks.append((int((self._x+self._stroke_width)*self._scale),
                           int((self._y)*self._scale)))
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, -self._innie_y2-2*self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, self._innie_y1),          
            self._rline_to(self._innie_x1, 0))

    def _do_outie(self):
        if self._outie is not True:
            return self._rline_to(0, -self._innie_y2)
        self.docks.append((int(self._x*self._scale), int(self._y*self._scale)))
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
            self._corner(1, 1))

    def _start_boolean(self, xoffset, yoffset):
        svg = self._new_path(xoffset, yoffset)
        self._radius -= self._stroke_width
        self.docks.append((int(self._x*self._scale), int(self._y*self._scale)))
        svg += self._rarc_to(1, -1)
        self._radius += self._stroke_width
        return svg + self._rline_to(self._stroke_width, 0)

    def _do_boolean(self):
        self.docks.append(
            (int((self._x-self._radius+self._stroke_width)*self._scale),
                           int((self._y+self._radius)*self._scale)))
        self.margins[2] =\
            int((self._x-self._radius-self._stroke_width)*self._scale)
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
        if self.margins[2] == 0:
            self.margins[2] = int((self._stroke_width+0.5)*self._scale)
        else:
            self.margins[2] = int(self._width - self.margins[2])
        self._height = (self._max_y-self._min_y+self._stroke_width)*\
                      self._scale
        if self.margins[3] == 0:
            if self._tab:
                self.margins[3] =\
                    int((self._slot_y+self._stroke_width+0.5)*self._scale)
            else:
                self.margins[3] =\
                    int((self._slot_y*2+self._stroke_width+0.5)*self._scale)
        else:
            self.margins[3] = int(self._height - self.margins[3])

    def _calculate_x_y(self):
        x = self._stroke_width/2.0
        y = self._stroke_width/2.0+self._radius
        self.margins[0] = int(x+self._stroke_width+0.5)
        self.margins[1] = int(self._stroke_width+0.5)
        if self._outie is True:
            x += self._innie_x1+self._innie_x2
            self.margins[0] += self._innie_x1+self._innie_x2
        if self._cap is True:
            y += self._slot_y*2.0
            self.margins[1] += self._slot_y*2.0
        elif self._slot is True:
            self.margins[1] += self._slot_y
        self.margins[0] *= self._scale
        self.margins[1] *= self._scale
        return(x, y)

#
# Command-line tools for testing
#

def open_file(datapath, filename):
    return file(os.path.join(datapath, filename), "w")

def close_file(f):
    f.close()

def generator(datapath):

    svgt = SVG()
    svgt.set_orientation(180)
    f = open_file(datapath, "turtle180.svg")
    svg_str = svgt.turtle(["#FF0000","#00FF00"])
    f.write(svg_str)
    close_file(f)

    """
    svg0 = SVG()
    f = open_file(datapath, "basic.svg")
    svg0.set_scale(2)
    svg0.set_tab(True)
    svg0.set_slot(True)
    svg_str = svg0.basic_block()
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

    svg2 = SVG()
    f = open_file(datapath, "box-test2.svg")
    svg2.set_scale(4)
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
    """

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


#
# Read SVG string from a file
#
def svg_from_file(pathname):
    f = file(pathname, 'r')
    svg = f.read()
    f.close()
    return(svg)

