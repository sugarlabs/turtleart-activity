#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2009-12 Walter Bender

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

import os

from gi.repository import GdkPixbuf
from gi.repository.RB import file

from .taconstants import HIT_RED, HIT_GREEN, HIDE_WHITE, SHOW_WHITE, \
    PALETTE_COLOR, TOOLBAR_COLOR


class SVG:
    """ Interface to the graphical representation of blocks, turtles,
    palettes, etc. on screen

    terms used here:
    docks -- list of connection points of a block to other blocks
    innies -- right hand side docks of a block, argument slots
    outie -- left hand side dock of a block
    slot -- top dock of a block that can be attached to other blocks
    cap -- top dock of a block that cannot be attached to other blocks
    tab -- bottom dock of a block if other blocks can be attached
    tail -- bottom dock of a block if no other blocks can be attached
    arm -- connection point of a branching block (if-then, loops) where
        inner blocks are attached
    else -- optional second `arm' for if-then-else blocks """

    def __init__(self):
        self._x = 0
        self._y = 0
        self._min_x = 10000
        self._min_y = 10000
        self._max_x = -10000
        self._max_y = -10000
        self._width = 0
        self._height = 0
        self.docks = []
        self._scale = 1
        self._orientation = 0
        self._radius = 8
        self._stroke_width = 1
        self._innie = [False]
        self._outie = False
        self._innie_x1 = (9 - self._stroke_width) / 2
        self._innie_y1 = 3
        self._innie_x2 = (9 - self._stroke_width) / 2
        self._innie_y2 = (9 - self._stroke_width) / 2
        self._innie_spacer = 9
        self._slot = True
        self._cap = False
        self._tab = True
        self._bool = False
        self._slot_x = 10
        self._slot_y = 2
        self._tail = False
        self._porch = False
        self._porch_x = self._innie_x1 + self._innie_x2 + \
            4 * self._stroke_width
        self._porch_y = self._innie_y2
        self._expand_x = 0
        self._expand_x2 = 0
        self._expand_y = 0
        self._expand_y2 = 0
        self._second_clamp = False
        self._arm = True
        self._else = False
        self._draw_innies = True
        self._hide = False
        self._show = False
        self._collapsible = False
        self._show_x = 0
        self._show_y = 0
        self._hide_x = 0
        self._hide_y = 0
        self._dot_radius = 8
        self._fill = "#00FF00"
        self._stroke = "#00A000"
        self._gradient_color = "#FFFFFF"
        self._gradient = False
        self.margins = [0, 0, 0, 0]

    """
    The block construction methods typically start on the upper-left side
    of a block and proceed clockwise around the block, first constructing
    a corner (1, -1), a slot or hat on along the top, a corner (1, 1),
    right side connectors ("innie"), possibly a "porch" to suggest an
    order of arguments, another corner (-1, 1), a tab or tail, and the
    fourth corner (-1, -1), and finally, a left-side connector ("outie").
    In addition:
     * Minimum and maximum values are calculated for the SVG bounding box;
     * Docking coordinates are calculated for each innie, outie, tab, and slot.
    """

    def basic_block(self):
        ''' The most common block type: used for 0, 1, 2, or 3
        argument commands, stacks, et al. '''
        self.reset_min_max()
        (x, y) = self._calculate_x_y()
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self.new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
            if i == 0:
                svg += self._rline_to(0, self._expand_y)
            elif i == 1 and self._expand_y2 > 0:
                svg += self._rline_to(0, self._expand_y2)
            if i == 0 and self._porch is True:
                svg += self._do_porch(False)
            elif len(self._innie) - 1 > i:
                svg += self._rline_to(
                    0, 2 * self._innie_y2 + self._innie_spacer)
        svg += self._corner(-1, 1)
        svg += self.line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        if self._tab:
            svg += self._do_tab()
        else:
            svg += self._do_tail()
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self.line_to(
                x, self._radius + self._innie_y2 + self._stroke_width / 2.0)
            svg += self._do_outie()
        self.calc_w_h()
        svg += self._close_path()
        svg += self.style()
        if self._show is True:
            svg += self._show_dot()
        if self._hide is True:
            svg += self._hide_dot()
        svg += self.footer()
        return self.header() + svg

    def invisible(self):
        ''' A block that is invisible but still has connectors: used
        when collapsing stacks. '''
        self.reset_min_max()
        (x, y) = self._calculate_x_y()
        self.margins[2] = 0
        self.margins[3] = 0
        # calculate shape but don't include it in the svg output
        self.new_path(x, y)
        self._corner(1, -1)
        self._do_slot()
        self._corner(1, 1)
        self._corner(-1, 1)
        self._do_tab()
        self._corner(-1, -1)
        self.calc_w_h()
        self._close_path()
        self.style()
        return self.header() + self.footer()

    def basic_flow(self):
        ''' A flow block includes an arm that holds a branch in the flow '''
        self.reset_min_max()
        (x, y) = self._calculate_x_y()
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self.new_path(x, y)
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
                self.margins[2] = \
                    int((self._x - self._stroke_width + 0.5) * self._scale)
        if self._bool is True:
            svg += self._rline_to(0, self._radius / 2.0)
            svg += self._do_boolean()
            svg += self._rline_to(0, self._stroke_width)
        if self._else:
            svg += self._rline_to(self._radius * 3 + self._slot_x * 2, 0)
        else:
            svg += self._rline_to(self._radius + self._slot_x, 0)
        save_y = self._y
        svg += self._corner(1, 1)
        svg += self._rline_to(-self._radius, 0)
        if self._else:
            svg += self._do_tab()
            svg += self._rline_to(-self._radius * 2, 0)
        svg += self._do_tab()
        svg += self._inverse_corner(-1, 1, 90, 0, 0, True, False)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1, 90, 0, 1, False, True)
        svg += self.line_to(xx, self._y)
        if self._tab:
            svg += self._do_tab()
        else:
            svg += self._do_tail()
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self.line_to(
                x, self._radius + self._innie_y2 + self._stroke_width)
        svg += self._close_path()
        self.calc_w_h()
        svg += self.style()
        if self._hide is True:
            svg += self._hide_dot()
        if self._show is True:
            svg += self._show_dot()
        svg += self.footer()
        if self._bool is True:  # move secondary labels to arm
            self.margins[2] = self._radius * 1.5 * self._scale
            self.margins[3] = (
                self._max_y - save_y - self._radius + self._stroke_width) * \
                self._scale
        return self.header() + svg

    def portfolio(self):
        ''' Deprecated block '''
        self.reset_min_max()
        (x, y) = self._calculate_x_y()
        self.margins[0] = int(x + 2 * self._stroke_width + 0.5)
        self.margins[1] = int(y + self._stroke_width + 0.5 + self._slot_y)
        self.margins[2] = 0
        self.margins[3] = 0
        x += self._innie_x1 + self._innie_x2
        svg = self.new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        xx = self._x
        svg += self._rline_to(self._expand_x, 0)
        svg += self._corner(1, 1)
        svg += self._rline_to(0, self._expand_y)
        for i in range(len(self._innie)):
            if self._innie[i] is True and \
                    i > 0 and self._draw_innies:
                svg += self._do_innie()
                svg += self._rline_to(
                    0, 2 * self._innie_y2 + self._innie_spacer)
            else:
                svg += self._rline_to(
                    0, 2 * self._innie_y2 + self._innie_spacer)
        svg += self._corner(-1, 1)
        svg += self.line_to(xx, self._y)
        svg += self._do_tab()
        svg += self._corner(-1, -1)
        for i in range(len(self._innie)):
            if self._innie[len(self._innie) - i - 1] is True:
                svg += self._rline_to(
                    0, -2 * self._innie_y2 - self._innie_spacer)
                svg += self._do_reverse_innie()
            else:
                svg += self._rline_to(
                    0, -2 * self._innie_y2 - self._innie_spacer)
        svg += self._close_path()
        self.calc_w_h()
        svg += self.style()
        svg += self.footer()
        return self.header() + svg

    def basic_box(self):
        ''' Basic argument style used for numbers, text, media '''
        self.reset_min_max()
        self.set_outie(True)
        x = self._stroke_width / 2.0 + self._innie_x1 + self._innie_x2
        self.margins[0] = int((x + self._stroke_width + 0.5) * self._scale)
        self.margins[1] = int((self._stroke_width + 0.5) * self._scale)
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self.new_path(x, self._stroke_width / 2.0)
        svg += self._rline_to(self._expand_x, 0)
        svg += self._rline_to(
            0, 2 * self._radius + self._innie_y2 + self._expand_y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self.line_to(
            x, self._radius + self._innie_y2 + self._stroke_width / 2.0)
        svg += self._do_outie()
        svg += self._close_path()
        self.calc_w_h()
        svg += self.style()
        svg += self.footer()
        return self.header() + svg

    def boolean_and_or(self):
        ''' Booleans are in a class of their own '''
        self.reset_min_max()
        svg = self._start_boolean(self._stroke_width / 2.0,
                                  self._radius * 5.5 + self._stroke_width / 2.0 + self._innie_y2 + self._innie_spacer + self._expand_y)
        svg += self._rline_to(0, -self._radius * 3.5 - self._innie_y2 - self._innie_spacer - self._stroke_width)

        self._hide_x = self._x + self._radius + self._stroke_width
        self._hide_y = self._y
        self._show_x = self._x + self._radius + self._stroke_width

        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius / 2.0 + self._expand_x, 0)
        xx = self._x
        svg += self._rline_to(0, self._radius / 2.0)
        svg += self._do_boolean()
        svg += self._rline_to(
            0, self._radius * 1.5 + self._innie_y2 + self._innie_spacer)

        svg += self._rline_to(0, self._expand_y)

        svg += self._do_boolean()
        svg += self._rline_to(0, self._radius / 2.0)

        self._show_y = self._y
        self._show_y -= (
            self._innie_y1 + self._innie_y2 + self._stroke_width)

        svg += self.line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        self.margins[0] = int((
            self._radius + self._stroke_width + 0.5) * self._scale)
        self.margins[1] = int(self._stroke_width * self._scale)
        self.margins[2] = int(self._stroke_width * self._scale)
        self.margins[3] = int(self._stroke_width * self._scale)
        return self.header() + svg

    def boolean_not(self, notnot):
        ''' Booleans are in a class of their own: not and not not '''
        self.reset_min_max()
        if self._innie[0]:
            svg = self._start_boolean(
                self._stroke_width / 2.0,
                self._radius * 1.25 + self._stroke_width / 2.0)
        elif not notnot:
            svg = self._start_boolean(
                self._stroke_width / 2.0,
                self._radius * 2.0 + self._stroke_width / 2.0)
        else:
            svg = self._start_boolean(
                self._stroke_width / 2.0,
                self._radius + self._stroke_width / 2.0)

        svg += self._rline_to(0, -self._stroke_width)

        if self._innie[0]:
            svg += self._rline_to(0, -self._radius / 4.0)
        elif not notnot:
            svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius / 2.0 + self._expand_x, 0)
        xx = self._x

        if self._innie[0]:
            svg += self._rline_to(0, self._radius)
            svg += self._do_innie()
            svg += self._rline_to(0, self._radius)
        elif not notnot:
            svg += self._rline_to(0, self._radius / 2.0)
            svg += self._do_boolean()
            svg += self._rline_to(0, self._radius / 2.0)
        else:
            svg += self._rline_to(0, self._radius * 2)

        svg += self.line_to(xx, self._y)
        if self._innie[0]:
            svg += self._rline_to(-self._radius / 2.0 - self._expand_x, 0)
            svg += self._rline_to(0, -self._radius / 4.0)
        elif not notnot:
            svg += self._rline_to(-self._expand_x, 0)
        else:
            svg += self._rline_to(-self._radius / 2.0 - self._expand_x, 0)
        svg += self._end_boolean(notnot)
        if notnot:
            self.margins[0] = int(
                (self._radius + self._stroke_width + 0.5) * self._scale)
            self.margins[2] = int(
                (self._radius + self._stroke_width + 0.5) * self._scale)
        else:
            self.margins[0] = int((self._stroke_width + 0.5) * self._scale)
            self.margins[2] = int((self._stroke_width + 0.5) * self._scale)
        self.margins[1] = int(self._stroke_width * self._scale)
        self.margins[3] = int(self._stroke_width * self._scale)
        return self.header() + svg

    def boolean_compare(self):
        ''' Booleans are in a class of their own '''
        self.reset_min_max()
        yoffset = self._radius * 2 + 2 * self._innie_y2 + \
            self._innie_spacer + self._stroke_width / 2.0 + \
            self._expand_y
        svg = self._start_boolean(self._stroke_width / 2.0, yoffset)
        yoffset = -2 * self._innie_y2 - self._innie_spacer - self._stroke_width
        svg += self._rline_to(0, yoffset)

        self._hide_x = self._x + self._radius + self._stroke_width
        self._hide_y = self._y
        self._show_x = self._x + self._radius + self._stroke_width

        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius / 2.0 + self._expand_x, 0)
        svg += self._rline_to(0, self._radius)
        xx = self._x
        svg += self._do_innie()
        svg += self._rline_to(0, self._expand_y)
        if self._porch is True:
            svg += self._do_porch(False)
        else:
            svg += self._rline_to(0, 2 * self._innie_y2 + self._innie_spacer)
        svg += self._do_innie()
        svg += self._rline_to(0, self._radius)
        svg += self.line_to(xx, self._y)

        svg += self._rline_to(-self._expand_x, 0)

        self._show_y = self._y
        self._show_y -= \
            (self._innie_y1 + self._innie_y2 + self._stroke_width * 2)

        svg += self._end_boolean()
        self.margins[0] = int(
            (self._radius + self._stroke_width) * self._scale)
        self.margins[1] = int(self._stroke_width * self._scale)
        self.margins[2] = int(self._stroke_width * self._scale)
        return self.header() + svg

    def triangle_up(self, colors):
        ''' A triangle that points up '''
        self.reset_min_max()
        self._fill, self._stroke = colors[0], colors[1]
        self._width, self._height = 55 * self._scale, 55 * self._scale
        svg = self.new_path(5, 50)
        svg += self._rline_to(22.5, -45)
        svg += self._rline_to(22.5, 45)
        svg += self._close_path()
        svg += self.style()
        svg += self.footer()
        return self.header() + svg

    def triangle_down(self, colors):
        ''' A triangle that points down '''
        self.reset_min_max()
        self._fill, self._stroke = colors[0], colors[1]
        self._width, self._height = 55 * self._scale, 55 * self._scale
        svg = self.new_path(5, 5)
        svg += self._rline_to(22.5, 45)
        svg += self._rline_to(22.5, -45)
        svg += self._close_path()
        svg += self.style()
        svg += self.footer()
        return self.header() + svg

    def turtle(self, colors):
        ''' Turtles are just another block '''
        self.reset_min_max()
        self._fill, self._stroke = colors[1], colors[0]

        # Tail
        svg = '  <path d="M 27.5 48.3 C 26.9 48.3 26.4 48.2 25.9 48.2 \
L 27.2 50.5 L 28.6 48.2 C 28.2 48.2 27.9 48.3 27.5 48.3 Z" \
stroke-width="3.5" fill="%s" stroke="%s" />\n' % (self._fill, self._stroke)
        # Feet x 4
        svg += '   <path d="M 40.2 11.7 C 38.0 11.7 36.2 13.3 35.8 15.3 \
C 37.7 16.7 39.3 18.4 40.5 20.5 C 42.8 20.4 44.6 18.5 44.6 16.2 \
C 44.6 13.7 42.6 11.7 40.2 11.7 Z" stroke-width="3.5" \
fill="%s" stroke="%s" />\n' % (self._fill, self._stroke)
        svg += '   <path d="M 40.7 39.9 C 39.5 42.1 37.9 44.0 35.9 45.4 \
C 36.4 47.3 38.1 48.7 40.2 48.7 C 42.6 48.7 44.6 46.7 44.6 44.3 \
C 44.6 42.0 42.9 40.2 40.7 39.9 Z" stroke-width="3.5" \
fill="%s" stroke="%s" />\n' % (self._fill, self._stroke)
        svg += '   <path d="M 14.3 39.9 C 12.0 40.1 10.2 42.0 10.2 44.3 \
C 10.2 46.7 12.2 48.7 14.7 48.7 C 16.7 48.7 18.5 47.3 18.9 45.4 \
C 17.1 43.9 15.5 42.1 14.3 39.9 Z" stroke-width="3.5" \
fill="%s" stroke="%s" />\n' % (self._fill, self._stroke)
        svg += '   <path d="M 19.0 15.4 C 18.7 13.3 16.9 11.7 14.7 11.7 \
C 12.2 11.7 10.2 13.7 10.2 16.2 C 10.2 18.5 12.1 20.5 14.5 20.6 \
C 15.7 18.5 17.2 16.8 19.0 15.4 Z" stroke-width="3.5" \
fill="%s" stroke="%s" />\n' % (self._fill, self._stroke)
        # Head
        svg += '<path d="m 27.50,12.56 c 1.91,0 3.73,0.41 5.42,1.13 \
C 33.66,12.62 34.83,11.27 34.25,10 32.95,7.24 31.19,2.31 27.5,2.31 \
c -3.69,0 -5.08,4.93 -6.75,7.69 -0.74,1.22 0.44,2.66 1.21,3.74 1.72,-0.75 \
3.60,-1.18 5.54,-1.18 z" style="fill:%s;stroke:%s;stroke-width:3.5" />' % \
               (self._fill, self._stroke)
        # Shell
        svg += '   <path d="M 43.1 30.4 C 43.1 35.2 41.5 39.7 38.5 43.0 \
C 35.6 46.4 31.6 48.3 27.5 48.3 C 23.4 48.3 19.4 46.4 16.5 43.0 \
C 13.5 39.7 11.9 35.2 11.9 30.4 C 11.9 20.6 18.9 12.6 27.5 12.6 \
C 36.1 12.6 43.1 20.6 43.1 30.4 Z" stroke-width="3.5" \
fill="%s" stroke="%s" />\n' % (self._fill, self._stroke)
        svg += '   <path d="M 25.9 33.8 L 24.3 29.1 \
L 27.5 26.5 L 31.1 29.2 L 29.6 33.8 Z" stroke-width="3.5" \
fill="%s" stroke="none" />\n' % (self._stroke)
        svg += '  <path d="M 27.5 41.6 C 23.5 41.4 22.0 39.5 22.0 39.5 \
L 25.5 35.4 L 30.0 35.5 L 33.1 39.7 C 33.1 39.7 30.2 41.7 27.5 41.6 Z" \
stroke-width="3.5" fill="%s" stroke="none" />\n' % (self._stroke)
        svg += '   <path d="M 18.5 33.8 C 17.6 30.9 18.6 27.0 18.6 27.0 \
L 22.6 29.1 L 24.1 33.8 L 20.5 38.0 C 20.5 38.0 19.1 36.0 18.4 33.8 Z" \
stroke-width="3.5" fill="%s" stroke="none" />\n' % (self._stroke)
        svg += '   <path d="M 19.5 25.1 C 19.5 25.1 20.0 23.2 22.5 21.3 \
C 24.7 19.7 27.0 19.6 27.0 19.6 L 26.9 24.6 L 23.4 27.3 L 19.5 25.1 Z" \
stroke-width="3.5" fill="%s" stroke="none" />\n' % (self._stroke)
        svg += '   <path d="M 32.1 27.8 L 28.6 25.0 \
L 29 19.8 C 29 19.8 30.8 19.7 33.0 21.4 C 35.2 23.2 36.3 26.4 36.3 26.4 \
L 32.1 27.8 Z" \
stroke-width="3.5" fill="%s" stroke="none" />\n' % (self._stroke)
        svg += '   <path d="M 31.3 34.0 L 32.6 29.6 L 36.8 28.0 \
C 36.8 28.0 37.5 30.7 36.8 33.7 C 36.2 36.0 34.7 38.1 34.7 38.1 \
L 31.3 34.0 Z" \
stroke-width="3.5" fill="%s" stroke="none" />\n' % (self._stroke)
        self._width, self._height = 55, 55
        svg += self.footer()
        return self.header() + svg

    def palette(self, width, height):
        ''' Just a rectangle with a hide button. '''
        self.reset_min_max()
        self._width, self._height = width, height
        self._fill, self._stroke = PALETTE_COLOR, "none"
        svg = self._rect(width, height, 0, 0)
        self._hide_x = (width - self._radius) / 2
        self._hide_y = (height - self._radius) / 2
        svg += self._hide_dot(noscale=True)
        svg += self.footer()
        return self.header() + svg

    def toolbar(self, width, height):
        ''' Just a rectangle '''
        self.reset_min_max()
        self._width, self._height = width, height
        self._fill, self._stroke = TOOLBAR_COLOR, "none"
        svg = self._rect(width, height, 0, 0)
        svg += self.footer()
        return self.header() + svg

    def clamp(self):
        ''' Special block for collapsible stacks; includes an 'arm"
        that extends down the left side of a stack and a bottom jaw to
        clamp the blocks. '''
        save_cap = self._cap
        save_slot = self._slot
        self.reset_min_max()
        x = self._stroke_width / 2.0
        if self._cap:
            y = self._stroke_width / 2.0 + self._radius + self._slot_y * 3.0
        else:
            y = self._stroke_width / 2.0 + self._radius
        self.margins[0] = int((x + self._stroke_width + 0.5) * self._scale)
        self.margins[1] = int((self._stroke_width + 0.5) * self._scale)
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self.new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        if self._cap:
            # Only one cap
            self._slot = True
            self._cap = False
        svg += self._rline_to(self._radius + self._stroke_width, 0)
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        if self._innie[0] is True:
            svg += self._do_innie()
        else:
            self.margins[2] = \
                int((self._x - self._stroke_width + 0.5) * self._scale)
        if self._bool is True:
            svg += self._do_boolean()
        svg += self._corner(-1, 1)
        svg += self.line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._do_tab()
        svg += self._inverse_corner(-1, 1, 90, 0, 0)
        svg += self._rline_to(0, self._expand_y)
        svg += self._inverse_corner(1, 1, 90, 0, 0)
        svg += self._do_slot()
        xx = self._x
        svg += self._rline_to(self._radius, 0)
        if self._second_clamp:
            svg += self._corner(-1, 1)
            svg += self.line_to(xx, self._y)
            svg += self._do_tab()
            svg += self._inverse_corner(-1, 1, 90, 0, 0)
            svg += self._rline_to(0, self._expand_y2)
            svg += self._inverse_corner(1, 1, 90, 0, 0)
            svg += self._do_slot()
            svg += self._rline_to(self._radius, 0)
        svg += self._corner(-1, 1)
        svg += self._rline_to(-self._radius - self._stroke_width, 0)
        if self._tail:
            svg += self._do_tail()
        else:
            svg += self._do_tab()

        self._cap = save_cap
        self._slot = save_slot

        svg += self._corner(-1, -1)
        svg += self._close_path()
        self.calc_w_h()
        svg += self.style()
        if self._collapsible:
            svg += self._hide_dot()
        svg += self.footer()
        return self.header() + svg

    def clamp_until(self):
        ''' Until block is like clamp but docks are flipped '''
        self.reset_min_max()
        x = self._stroke_width / 2.0
        y = self._stroke_width / 2.0 + self._radius
        self.margins[0] = int((x + self._stroke_width + 0.5) * self._scale)
        self.margins[1] = int((self._stroke_width + 0.5) * self._scale)
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self.new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._radius + self._stroke_width, 0)
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1, skip=True)
        svg += self._corner(-1, 1, skip=True)
        svg += self.line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._do_tab()
        svg += self._inverse_corner(-1, 1, 90, 0, 0)
        svg += self._rline_to(0, self._expand_y)
        svg += self._inverse_corner(1, 1, 90, 0, 0)
        svg += self._do_slot()
        svg += self._rline_to(self._radius, 0)
        if self._innie[0] is True:
            svg += self._do_innie()
        else:
            self.margins[2] = \
                int((self._x - self._stroke_width + 0.5) * self._scale)
        svg += self._rline_to(0, self._radius + self._expand_y2)
        if self._bool is True:
            svg += self._do_boolean()
        svg += self._corner(-1, 1)
        svg += self._rline_to(-self._radius - self._stroke_width, 0)
        svg += self._do_tab()
        svg += self._corner(-1, -1)
        svg += self._close_path()
        self.calc_w_h()
        svg += self.style()
        if self._collapsible:
            svg += self._hide_dot()
        svg += self.footer()
        return self.header() + svg

    def status_block(self, graphic=None):
        ''' Generate a status block '''
        self.reset_min_max()
        (x, y) = self._calculate_x_y()
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self.new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1)
        svg += self.line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        self.calc_w_h()
        svg += self._close_path()
        svg += self.style()
        if self._hide is True:
            svg += self._hide_dot()
        svg += self.footer()
        return self.header() + svg

    #
    # Utility methods
    #
    def set_tail(self, flag=True):
        self._tail = flag

    def set_draw_innies(self, flag=True):
        self._draw_innies = flag

    def set_hide(self, flag=False):
        self._hide = flag

    def set_show(self, flag=False):
        self._show = flag

    def set_collapsible(self, flag=False):
        self._collapsible = flag

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_innie_width(self):
        return (self._innie_x1 + self._innie_x2) * self._scale

    def get_slot_depth(self):
        return self._slot_y * self._scale

    def clear_docks(self):
        self.docks = []

    def set_scale(self, scale=1):
        self._scale = scale

    def set_orientation(self, orientation=0):
        self._orientation = orientation

    def second_clamp(self, flag=False):
        self._second_clamp = flag

    def expand(self, w=0, h=0, w2=0, h2=0):
        self._expand_x = w
        self._expand_y = h
        self._expand_x2 = w2
        self._expand_y2 = h2

    def set_stroke_width(self, stroke_width=1.5):
        self._stroke_width = stroke_width
        self._calc_porch_params()

    def set_colors(self, colors=["#00FF00", "#00A000"]):
        self._fill = colors[0]
        self._stroke = colors[1]

    def set_fill_color(self, color="#00FF00"):
        self._fill = color

    def set_stroke_color(self, color="#00A000"):
        self._stroke = color

    def set_gradient(self, flag=False, color='#FFFFFF'):
        self._gradient = flag
        self._gradient_color = color

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

    def set_arm(self, flag=True):
        self._arm = flag

    def reset_min_max(self):
        self._min_x = 10000
        self._min_y = 10000
        self._max_x = -10000
        self._max_y = -10000

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

    def set_innie_spacer(self, innie_spacer=0):
        self._innie_spacer = innie_spacer

    def set_slot_params(self, x=12, y=4):
        self._slot_x = x
        self._slot_y = y

    def _calc_porch_params(self):
        self._porch_x = self._innie_x1 + self._innie_x2 + \
            4 * self._stroke_width
        self._porch_y = self._innie_y1 + self._innie_y2 + \
            4 * self._stroke_width

    #
    # SVG helper methods
    #
    def header(self, center=False):
        return '<svg\n\
    xmlns:svg="http://www.w3.org/2000/svg"\n\
    xmlns="http://www.w3.org/2000/svg"\n\
    xmlns:xlink="http://www.w3.org/1999/xlink"\n\
    version="1.1"\n\
    width="%.1f"\n\
    height="%.1f">\n' % (self._width, self._height) + \
               self._defs() + self._transform(center)

    def _defs(self):
        if self._gradient is True:
            return '  <defs>\n\
    <linearGradient\n\
    id="linearGradient1234">\n\
          <stop\n\
          style="stop-color:%s;stop-opacity:1;"\n\
          offset="0" />\n\
          <stop\n\
          style="stop-color:%s;stop-opacity:1;"\n\
          offset="1" />\n\
    </linearGradient>\n\
    <linearGradient\n\
          xlink:href="#linearGradient1234"\n\
          id="linearGradient5678"\n\
          x1="0"\n\
          y1="%.1f"\n\
          x2="%.1f"\n\
          y2="%.1f"\n\
          gradientUnits="userSpaceOnUse" />\n\
          </defs>\n' % (self._gradient_color,
                        self._fill,
                        self._height / 2.0,
                        self._width / self._scale,
                        self._height / 2.0)
        else:
            return ""

    def _transform(self, center):
        if self._orientation != 0:
            orientation = "<g\ntransform = \"rotate(%.1f %.1f %.1f)\">\n" % \
                          (self._orientation,
                           self._width / 2.0, self._height / 2.0)
        else:
            orientation = ""
        if center:
            return "<g\ntransform=\"translate(%.1f, %.1f)\">\n" % \
                   (-self._min_x, -self._min_y)
        else:
            return "<g\ntransform=\"scale(%.1f, %.1f)\">\n%s" % \
                   (self._scale, self._scale, orientation)

    def footer(self):
        if self._orientation != 0:
            return "   </g>\n</g>\n</svg>\n"
        else:
            return "   </g>\n</svg>\n"

    def style(self):
        if self._gradient is True:
            fill = "url(#linearGradient5678)"
        else:
            fill = self._fill
        return "%s%s;%s%s;%s%.1f;%s%s" % (
            "       style=\"fill:", fill,
            "fill-opacity:1;stroke:", self._stroke,
            "stroke-width:", self._stroke_width,
            "stroke-linecap:round;",
            "stroke-opacity:1;\" />\n")

    def text(self, x, y, size, width, string):
        self._x = x
        self._y = y
        self._check_min_max()
        self._x = x + width
        self._y = y - size
        self._check_min_max()
        return "        %s%.1f%s%s%s%.1f%s%.1f%s%.1f%s%s%s%s%s" % (
            "<text style=\"font-size:", size, "px;fill:", self._stroke,
            ";font-family:Sans\">\n           <tspan x=\"", x, "\" y=\"", y,
            "\" style=\"font-size:", size, "px;fill:", self._stroke, "\">",
            string, "</tspan>\n        </text>\n")

    def image(self, x, y, w, h, path, image_data=None):
        self._x = x
        self._y = y
        self._check_min_max()
        self._x = x + w
        self._y = y + h
        self._check_min_max()
        if image_data is None:
            return "        %s%.1f%s%.1f%s%.1f%s%.1f%s%s%s" % (
                "<image x=\"", x, "\" y=\"", y,
                "\" width=\"", w, "\" height=\"", h,
                "\" xlink:href=\"file://", path, "\"/>\n")
        else:
            return "        %s%.1f%s%.1f%s%.1f%s%.1f%s%s%s" % (
                "<image x=\"", x, "\" y=\"", y,
                "\" width=\"", w, "\" height=\"", h,
                "\" xlink:href=\"data:image/png;base64,", image_data,
                "\"/>\n")

    def _circle(self, r, cx, cy):
        return "%s%s%s%s%s%f%s%f%s%f%s" % \
               ("<circle style=\"fill:", self._fill, ";stroke:", self._stroke,
                ";\" r=\"", r, "\" cx=\"", cx, "\" cy=\"", cy, "\" />\n")

    def _rect(self, w, h, x, y):
        return "%s%s%s%s%s%f%s%f%s%f%s%f%s" % ("<rect style=\"fill:",
                                               self._fill,
                                               ";stroke:",
                                               self._stroke,
                                               ";\" width=\"",
                                               w,
                                               "\" height=\"",
                                               h,
                                               "\" x=\"",
                                               x,
                                               "\" y=\"",
                                               y,
                                               "\" />\n")

    def background(self, fill):
        return "%s%s%s%s%s%f%s%f%s%f%s%f%s" % ("<rect style=\"fill:",
                                               fill,
                                               ";stroke:",
                                               fill,
                                               ";\" width=\"",
                                               self._max_x - self._min_x,
                                               "\" height=\"",
                                               self._max_y - self._min_y,
                                               "\" x=\"",
                                               self._min_x,
                                               "\" y=\"",
                                               self._min_y,
                                               "\" />\n")

    def _check_min_max(self):
        if self._x < self._min_x:
            self._min_x = self._x
        if self._y < self._min_y:
            self._min_y = self._y
        if self._x > self._max_x:
            self._max_x = self._x
        if self._y > self._max_y:
            self._max_y = self._y

    def line_to(self, x, y):
        self._check_min_max()
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
            return self.line_to(self._x + dx, self._y + dy)

    def arc_to(self, x, y, r, a=90, laf=0, s=1):
        self._check_min_max()
        if r == 0:
            return self.line_to(x, y)
        else:
            self._x = x
            self._y = y
            self._check_min_max()
            return "A %.1f %.1f %.1f %d %d %.1f %.1f " % (
                r, r, a, laf, s, x, y)

    def _rarc_to(self, sign_x, sign_y, a=90, laf=0, s=1):
        if self._radius == 0:
            return ""
        else:
            x = self._x + sign_x * self._radius
            y = self._y + sign_y * self._radius
            return self.arc_to(x, y, self._radius, a, laf, s)

    def _inverse_corner(self, sign_x, sign_y, a=90, laf=0, s=1, start=True,
                        end=True):
        r2 = self._stroke_width + self._radius / 2.0
        if start:
            if sign_x * sign_y == -1:
                svg_str = self._rline_to(sign_x * (r2 - self._stroke_width), 0)
            else:
                svg_str = self._rline_to(0, sign_y * (r2 - self._stroke_width))
        x = self._x + sign_x * r2
        y = self._y + sign_y * r2
        svg_str += self.arc_to(x, y, r2, a, laf, s)
        if end:
            if sign_x * sign_y == -1:
                svg_str += self._rline_to(0,
                                          sign_y * (r2 - self._stroke_width))
            else:
                svg_str += self._rline_to(sign_x * (r2 - self._stroke_width),
                                          0)
        return svg_str

    def _corner(self, sign_x, sign_y, a=90, laf=0, s=1, start=True, end=True,
                skip=False):
        svg_str = ""
        if sign_x == 1 and sign_y == -1:  # Upper-left corner
            self._hide_x = self._x + self._radius + self._stroke_width
            self._show_x = self._x + self._radius + self._stroke_width
            self._hide_y = self._y + self._stroke_width
        elif sign_x == 1 and sign_y == 1:  # Upper-right corner
            if len(self._innie) == 1 and self._innie[0]:
                self._show_x = self._x - self._radius
                self._show_y = self._hide_y
        elif sign_x == -1 and sign_y == 1:  # Lower-right corner
            if not (len(self._innie) == 1 and self._innie[0]):
                self._show_y = \
                    self._y - self._stroke_width

        if self._radius > 0:
            r2 = self._radius / 2.0
            if start:
                if sign_x * sign_y == 1:
                    svg_str += self._rline_to(sign_x * r2, 0)
                elif not skip:
                    svg_str += self._rline_to(0, sign_y * r2)
            x = self._x + sign_x * r2
            y = self._y + sign_y * r2
            svg_str += self.arc_to(x, y, r2, a, laf, s)
            if end:
                if sign_x * sign_y == 1:
                    svg_str += self._rline_to(0, sign_y * r2)
                elif not skip:
                    svg_str += self._rline_to(sign_x * r2, 0)
        return svg_str

    def new_path(self, x, y):
        """
        self._min_x = x
        self._min_y = y
        self._max_x = x
        self._max_y = y
        """
        self._x = x
        self._y = y
        return "      <path d=\"m%.1f %.1f " % (x, y)

    def _close_path(self):
        return "z\"\n"

    def _hide_dot(self, noscale=False):
        _saved_fill, _saved_stroke = self._fill, self._stroke
        self._fill, self._stroke = HIT_RED, HIT_RED
        svg = "</g>/n<g>/n"
        if noscale:
            scale = 2.0
            x = self._hide_x * scale
            y = self._hide_y * scale
            r = self._dot_radius * 2
            scale = 5
            scale2 = 2
            y2 = y - 10
            svg += self._circle(r, x - r / 2, y - r / 2)
            self._fill, self._stroke = HIDE_WHITE, HIDE_WHITE
            svg += self._rect(10 * scale2, scale, x - 9 * scale2, y2)
            self._fill, self._stroke = _saved_fill, _saved_stroke
        else:
            scale = self._scale * 1.75
            scale2 = scale / 2
            x = self._hide_x * self._scale
            y = self._hide_y * self._scale
            r = self._dot_radius * scale2
            y2 = y - scale2
            svg += self._circle(r, x, y)
            self._fill, self._stroke = HIDE_WHITE, HIDE_WHITE
            svg += self._rect(10 * scale2, scale, x - 5 * scale2, y2)
            self._fill, self._stroke = _saved_fill, _saved_stroke
        return svg

    def _show_dot(self):
        _saved_fill, _saved_stroke = self._fill, self._stroke
        self._fill, self._stroke = HIT_GREEN, HIT_GREEN
        svg = "</g>/n<g>/n"
        scale = self._scale * 1.75
        scale2 = scale / 2
        svg += self._circle(self._dot_radius * scale2,
                            self._show_x * self._scale,
                            self._show_y * self._scale)
        self._fill, self._stroke = SHOW_WHITE, SHOW_WHITE
        svg += self._rect(10 * scale2,
                          2 * scale2, self._show_x * self._scale - 5 * scale2,
                          self._show_y * self._scale - scale2 + scale2 / 2)
        svg += self._rect(2 * scale2, 10 * scale2,
                          self._show_x * self._scale - scale2 + scale2 / 2,
                          self._show_y * self._scale - 5 * scale2)
        self._fill, self._stroke = _saved_fill, _saved_stroke
        return svg

    def _do_slot(self):
        if self._slot is True:
            self.docks.append((int(self._x * self._scale),
                               int(self._y * self._scale)))
            return "%s%s%s" % (
                self._rline_to(0, self._slot_y),
                self._rline_to(self._slot_x, 0),
                self._rline_to(0, -self._slot_y))
        elif self._cap is True:
            return "%s%s" % (
                self._rline_to(self._slot_x / 2.0, -self._slot_y * 3.0),
                self._rline_to(self._slot_x / 2.0, self._slot_y * 3.0))
        else:
            return self._rline_to(self._slot_x, 0)

    def _do_tail(self):
        if self._outie is True:
            return self._rline_to(-self._slot_x, 0)
        elif self._tail:
            return "%s%s" % (
                self._rline_to(-self._slot_x / 2.0, self._slot_y * 3.0),
                self._rline_to(-self._slot_x / 2.0, -self._slot_y * 3.0))
        else:
            return self._rline_to(-self._slot_x, 0)

    def _do_tab(self):
        s = "%s%s%s%s%s" % (
            self._rline_to(-self._stroke_width, 0),
            self._rline_to(0, self._slot_y),
            self._rline_to(-self._slot_x + 2 * self._stroke_width, 0),
            self._rline_to(0, -self._slot_y),
            self._rline_to(-self._stroke_width, 0))
        self.docks.append((int(self._x * self._scale),
                           int((self._y + self._stroke_width) * self._scale)))
        return s

    def _do_innie(self):
        self.docks.append((int((self._x + self._stroke_width) * self._scale),
                           int((self._y + self._innie_y2) * self._scale)))
        if self.margins[2] == 0:
            self.margins[1] = int(
                (self._y - self._innie_y1) * self._scale)
            self.margins[2] = int(
                (self._x - self._innie_x1 - self._innie_x2 - self._stroke_width * 2
                 ) * self._scale)
        self.margins[3] = \
            int((self._y + self._innie_y2 + self._innie_y1) * self._scale)
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, -self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, self._innie_y2 + 2 * self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, -self._innie_y1),
            self._rline_to(self._innie_x1, 0))

    def _do_reverse_innie(self):
        self.docks.append((int((self._x + self._stroke_width) * self._scale),
                           int(self._y * self._scale)))
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, -self._innie_y2 - 2 * self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(self._innie_x1, 0))

    def _do_outie(self):
        if self._outie is not True:
            return self._rline_to(0, -self._innie_y2)
        self.docks.append((int(self._x * self._scale),
                           int(self._y * self._scale)))
        return "%s%s%s%s%s%s%s%s%s" % (
            self._rline_to(0, -self._stroke_width),
            self._rline_to(-self._innie_x1 - 2 * self._stroke_width, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(-self._innie_x2 + 2 * self._stroke_width, 0),
            self._rline_to(0,
                           -self._innie_y2 - 2 * self._innie_y1 +
                           2 * self._stroke_width),
            self._rline_to(self._innie_x2 - 2 * self._stroke_width, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(self._innie_x1 + 2 * self._stroke_width, 0),
            self._rline_to(0, -self._stroke_width))

    def _do_porch(self, flag=True):
        if flag:
            return "%s%s%s" % (
                self._rline_to(0, self._porch_y + self._innie_y1),
                self._rline_to(self._porch_x - self._radius, 0),
                self._corner(1, 1))
        else:
            return "%s%s%s" % (
                self._rline_to(
                    0, self._porch_y - self._innie_y1 + self._stroke_width),
                self._rline_to(self._porch_x - self._radius, 0),
                self._corner(1, 1))

    def _start_boolean(self, xoffset, yoffset):
        svg = self.new_path(xoffset, yoffset)
        self._radius -= self._stroke_width
        self.docks.append((int(self._x * self._scale),
                           int(self._y * self._scale)))
        svg += self._rarc_to(1, -1)
        self._radius += self._stroke_width
        svg += self._rline_to(self._stroke_width, 0)
        svg += self._rline_to(0, -self._expand_y)
        return svg

    def _do_boolean(self):
        self.docks.append(
            (int((self._x - self._radius + self._stroke_width) * self._scale),
             int((self._y + self._radius) * self._scale)))
        self.margins[2] = \
            int((self._x - self._radius - self._stroke_width) * self._scale)
        svg = self._rarc_to(-1, 1, 90, 0, 0) + self._rarc_to(1, 1, 90, 0, 0)
        return svg

    def _end_boolean(self, notnot=False):
        if not notnot:
            svg = self._rline_to(-self._radius * 1.5, 0)
        else:
            svg = ''
        svg += self._rline_to(0, -self._stroke_width)
        svg += self._rline_to(-self._stroke_width, 0)
        self._radius -= self._stroke_width
        svg += self._rarc_to(-1, -1)
        self._radius += self._stroke_width
        svg += self._close_path()
        self.calc_w_h()
        svg += self.style()
        if self._show is True:
            svg += self._show_dot()
        if self._hide is True:
            svg += self._hide_dot()
        return svg + self.footer()

    def calc_w_h(self, add_stroke_width=True):
        if add_stroke_width:
            self._width = (self._max_x - self._min_x + self._stroke_width) * \
                self._scale
        else:
            self._width = (self._max_x - self._min_x) * self._scale
        if self.margins[2] == 0:
            self.margins[2] = int((self._stroke_width + 0.5) * self._scale)
        else:
            self.margins[2] = int(self._width - self.margins[2])
        if add_stroke_width:
            self._height = (self._max_y - self._min_y + self._stroke_width) * \
                self._scale
        else:
            self._height = (self._max_y - self._min_y) * self._scale
        if self.margins[3] == 0:
            if self._tab:
                self.margins[3] = int(
                    (self._slot_y + self._stroke_width + 0.5) * self._scale)
            else:
                self.margins[3] = int(
                    (self._slot_y * 2 + self._stroke_width + 0.5
                     ) * self._scale)
        else:
            self.margins[3] = int(self._height - self.margins[3])

    def _calculate_x_y(self):
        x = self._stroke_width / 2.0
        y = self._stroke_width / 2.0 + self._radius
        self.margins[0] = int(x + self._stroke_width + 0.5)
        self.margins[1] = int(self._stroke_width + 0.5)
        if self._outie is True:
            x += self._innie_x1 + self._innie_x2
            self.margins[0] += self._innie_x1 + self._innie_x2
        if self._cap is True:
            y += self._slot_y * 3.0
            self.margins[1] += self._slot_y * 3.0
        elif self._slot is True:
            self.margins[1] += self._slot_y
        self.margins[0] *= self._scale
        self.margins[1] *= self._scale
        return (x, y)


#
# Command-line tools for testing
#


def open_file(datapath, filename):
    return file(os.path.join(datapath, filename), "w")


def close_file(f):
    f.close()


def generator(datapath):
    '''
    svg = SVG()
    f = open_file(datapath, "turtle.svg")
    svg.set_scale(2)
    svg_str = svg.turtle(['#00FF00','#00AA00'])
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "boolean_notnot.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.boolean_not(True)
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "boolean_not.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.boolean_not(False)
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "boolean-arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True])
    svg_str = svg.boolean_not(True)
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "basic.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "blank.svg")
    svg.set_scale(2)
    svg.set_slot(False)
    svg.set_tab(False)
    svg.set_tail(False)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "head.svg")
    svg.set_scale(2)
    svg.set_slot(False)
    svg.set_cap(True)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "head1arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True])
    svg.set_slot(False)
    svg.set_cap(True)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "tail1arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True])
    svg.set_slot(False)
    svg.set_tail(True)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "tail.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_slot(False)
    svg.set_tail(True)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "basic1arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True])
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "basic2arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True, True])
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "basic3arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True, True, True])
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "box.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.basic_box()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "media.svg")
    svg.set_scale(2)
    svg.expand(40, 30, 0, 0)
    svg_str = svg.basic_box()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "number.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True, True])
    svg.set_outie(True)
    svg.set_tab(False)
    svg.set_slot(False)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "number1arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True])
    svg.set_outie(True)
    svg.set_tab(False)
    svg.set_slot(False)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "number3arg.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True, True, True])
    svg.set_outie(True)
    svg.set_tab(False)
    svg.set_slot(False)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "numberp.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_innie([True, True])
    svg.set_outie(True)
    svg.set_tab(False)
    svg.set_slot(False)
    svg.set_porch(True)
    svg_str = svg.basic_block()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "comparep.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_porch(True)
    svg_str = svg.boolean_compare()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "compare.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.boolean_compare()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "andor.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg_str = svg.boolean_and_or()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "clamp.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_slot(True)
    svg.set_tab(True)
    svg.second_clamp(False)
    svg_str = svg.clamp()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "clampn.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_slot(True)
    svg.set_tab(True)
    svg.set_innie([True])
    svg.second_clamp(False)
    svg_str = svg.clamp()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "clampe.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_slot(True)
    svg.set_tab(True)
    svg.set_boolean(True)
    svg.second_clamp(True)
    svg_str = svg.clamp()
    f.write(svg_str)
    close_file(f)
    '''
    svg = SVG()
    f = open_file(datapath, "start.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_slot(False)
    svg.set_cap(True)
    svg.set_tail(True)
    svg.set_tab(True)
    svg.set_boolean(False)
    svg.second_clamp(False)
    svg_str = svg.clamp()
    f.write(svg_str)
    close_file(f)
    '''
    svg = SVG()
    f = open_file(datapath, "clampb.svg")
    svg.set_scale(2)
    svg.expand(0, 30, 0, 0)
    svg.set_slot(True)
    svg.set_tab(True)
    svg.set_boolean(True)
    svg.second_clamp(False)
    svg_str = svg.clamp()
    f.write(svg_str)
    close_file(f)

    svg = SVG()
    f = open_file(datapath, "clampu.svg")
    svg.set_scale(2)
    svg.expand(0, 30, 0, 0)
    svg.set_slot(True)
    svg.set_tab(True)
    svg.set_boolean(True)
    svg.second_clamp(False)
    svg_str = svg.clamp_until()
    f.write(svg_str)
    close_file(f)
    '''


def main():
    return 0


if __name__ == "__main__":
    generator(os.path.abspath('.'))
    main()


def svg_str_to_pixbuf(svg_string):
    """ Load pixbuf from SVG string """
    pl = GdkPixbuf.PixbufLoader()
    pl.write(svg_string.encode())
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf


def svg_str_to_pixmap(svg_string):
    """ Load pixmap from SVG string """
    (pixmap, mask) = svg_str_to_pixbuf(svg_string).render_pixmap_and_mask()
    return pixmap


def svg_from_file(pathname):
    """ Read SVG string from a file """
    f = open(pathname, 'r')
    svg = f.read()
    f.close()
    return (svg)
