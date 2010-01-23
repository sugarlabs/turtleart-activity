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
from sprite_factory import *
import sprites
from gettext import gettext as _

#
# A class for the list of blocks and everything they share in common
#
class Blocks:
    def __init__(self):
        self.list = []

    def get_block(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self,block):
        self.list.append(block)

    def remove_from_list(self, block):
        if block in self.list:
            self.list.remove(block)

    def print_list(self):
        for i, block in enumerate(self.list):
            print "%d: %s" % (i, block.name)


    #
    # sprite utilities
    #
    def spr_to_block(self, spr):
        for b in self.list:
            if spr == b.spr:
                return b
        return None

#
# A class for the individual blocks
#
class Block:
    def __init__(self, block_list, sprite_list, name, x, y, labels=[], 
                 colors=["#00FF00","#00A000"], scale=2.0):
        self.spr = None
        self.shape = None
        self.selected_shape = None
        self.name = name
        self.docks = None
        self.connections = None
        self.defaults = []
        self.content = None
        self.primitive = None
        self._new_block_from_factory(sprite_list, name, labels, colors,
                                       scale, x, y)
        self.type = 'block'

        self._left = 0
        self._right = 0

        if DEFAULTS.has_key(name):
            self.defaults = DEFAULTS[name]

        if name in CONTENT_BLOCKS:
            self.content = name

        if PRIMITIVES.has_key(name):
            self.primitive = PRIMITIVES[name]

        block_list.append_to_list(self)
        #
        # TODO:
        # Logo code
        # HTML code
        # debug code
        # etc.

    def _new_block_from_factory(self, sprite_list, name, labels, colors,
                                scale, x, y):

        print "new block: %s (%d %d)" % (name, x, y)

        svg = SVG()
        svg.set_scale(scale)
        svg.set_gradiant(True)
        svg.set_innie([False])
        svg.set_outie(False)
        svg.set_tab(True)
        svg.set_slot(True)

        self._make_block(name, 0, svg)
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

        self.spr.set_margins(self._left, 0, self._right, 0)

        # if labels were passed, use them
        if len(labels) > 0:
            print labels
            for i, l in enumerate(labels):
                self.spr.set_label(l,i)
                if i == 1: # top
                    self.spr.set_label_attributes(9, True, "right", "top", i)
                elif i == 2: # bottom
                    self.spr.set_label_attributes(9, True, "right", "bottom", i)
        # otherwise use default values
        elif BLOCK_NAMES.has_key(name):
            print BLOCK_NAMES[name]
            for i, l in enumerate(BLOCK_NAMES[name]):
                self.spr.set_label(l,i)
                if i == 1: # top
                    self.spr.set_label_attributes(9, True, "right", "top", i)
                elif i == 2: # bottom
                    self.spr.set_label_attributes(9, True, "right", "bottom", i)

        # make sure the label fits
        lw = self.spr.label_width()        
        lwh = self.spr.label_area_dimensions()
        if lw > lwh[0]:
            e = lw-lwh[0]
            self._make_block(name, e, svg)
            self.spr.set_shape(self.shape)

        """
        Do something with default values?
        """

    def _make_block(self, name, e, svg):
        self._set_colors(name, svg)
        svg.set_stroke_width(STANDARD_STROKE_WIDTH)
        svg.clear_docks()
        if name in BASIC_STYLE:
            self._make_basic_style(e, svg)
        elif name in BASIC_STYLE_HEAD:
            self._make_basic_style_head(e, svg)
        elif name in BASIC_STYLE_HEAD_1ARG:
            self._make_basic_style_head_1arg(e, svg)
        elif name in BASIC_STYLE_TAIL:
            self._make_basic_style_tail(e, svg)
        elif name in BASIC_STYLE_1ARG:
            self._make_basic_style_1arg(e, svg)
        elif name in BASIC_STYLE_2ARG:
            self._make_basic_style_1arg(e, svg)
        elif name in BOX_STYLE:
            self._make_box_style(e, svg)
        elif name in NUMBER_STYLE:
            self._make_number_style(e, svg)
        elif name in NUMBER_STYLE_1ARG:
            self._make_number_style_1arg(e, svg)
        elif name in NUMBER_STYLE_PORCH:
            self._make_number_style_porch(e, svg)
        elif name in COMPARE_STYLE:
            self._make_compare_style(e, svg)
        elif name in BOOLEAN_STYLE:
            self._make_boolean_style(e, svg)
        elif name in NOT_STYLE:
            self._make_not_style(e, svg)
        elif name in FLOW_STYLE:
            self._make_flow_style(e, svg)
        elif name in FLOW_STYLE_1ARG:
            self._make_flow_style_1arg(e, svg)
        elif name in FLOW_STYLE_BOOLEAN:
            self._make_flow_style_boolean(e, svg)
        else:
            self._make_basic_style(e, svg)
            print "don't know how to create a block for %s" % (name)

        print self.docks
        print "w %d h %d" % (svg._width, svg._height)
        print "l %d r %d" % (self._left, self._right)

    def _set_colors(self, name, svg):
        if name in TURTLE_PALETTE:
            svg.set_colors(TURTLE_COLORS)
        elif name in PEN_PALETTE:
            svg.set_colors(PEN_COLORS)
        elif name in NUMBER_PALETTE:
            svg.set_colors(NUMBER_COLORS)
        elif name in BLOCKS_PALETTE:
            svg.set_colors(BLOCKS_COLORS)
        elif name in MISC_PALETTE:
            svg.set_colors(MISC_COLORS)
        elif name in FLOW_PALETTE:
            svg.set_colors(FLOW_COLORS)
        elif name in PORTFOLIO_PALETTE:
            svg.set_colors(PORTFOLIO_COLORS)

    def _make_basic_style(self, e, svg):
        svg.expand(40+e, 0)
        self._make_basic_block(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('flow', False,svg.docks[1][0], svg.docks[1][1]))
        self._left, self._right = 0, 0

    def _make_basic_style_head(self, e, svg):
        svg.expand(40+e, 0)
        svg.set_slot(False)
        svg.set_cap(True)
        self._make_basic_block(svg)
        self.docks = (('start', True, 0, 0),
                      ('flow', False, svg.docks[0][0], svg.docks[0][1]))
        self._left, self._right = 0, 0

    def _make_basic_style_head_1arg(self, e, svg):
        svg.expand(40+e, 0)
        svg.set_innie([True])
        svg.set_slot(False)
        svg.set_cap(True)
        self._make_basic_block(svg)
        self.docks = (('start', True, 0, 0),
                      ('string', False, svg.docks[0][0], svg.docks[0][1]),
                      ('flow', False, svg.docks[1][0], svg.docks[1][1]))
        self._left, self._right = 0, svg.get_innie_size()

    def _make_basic_style_tail(self, e, svg):
        svg.expand(40+e, 0)
        svg.set_tab(False)
        self._make_basic_block(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('unavailable', False, 0, 0))

    def _make_basic_style_1arg(self, e, svg):
        svg.expand(25+e, 0)
        svg.set_innie([True])
        self._make_basic_block(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('number', False, svg.docks[1][0], svg.docks[1][1]),
                      ('flow', False, svg.docks[2][0], svg.docks[2][1]))
        self._left, self._right = 0, svg.get_innie_size()

    def _make_basic_style_2arg(self, e, svg):
        svg.expand(25+e, 0)
        svg.set_innie([True,True])
        self._make_basic_block(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('number', False, svg.docks[1][0], svg.docks[1][1]),
                      ('number', False, svg.docks[2][0], svg.docks[2][1]),
                      ('flow', False, svg.docks[3][0], svg.docks[3][1]))
        self._left, self._right = 0, svg.get_width()-svg.docks[1][0]

    def _make_box_style(self, e, svg):
        svg.expand(60+e, 0)
        self._make_basic_box(svg)
        self.docks = (('number', True, svg.docks[0][0], svg.docks[0][1]),
                      ('unavailable', False, 0, 0))
        self._left, self._right = svg.docks[1][0], 0

    def _make_number_style(self, e, svg):
        svg.expand(e, 0)
        svg.set_innie([True,True])
        svg.set_outie(True)
        svg.set_tab(False)
        svg.set_slot(False)
        self._make_basic_block(svg)
        """
        NOTE:
        The "outie" is added last, so the dock order in the NUMBER_STYLE
        needs to be modified.
        """
        self.docks = (('number', True, svg.docks[2][0], svg.docks[2][1]),
                      ('number', False, svg.docks[0][0], svg.docks[0][1]),
                      ('number', False, svg.docks[1][0], svg.docks[1][1])) 
        self._left, self._right = svg.docks[2][0], 0

    def _make_number_style_1arg(self, e, svg):
        svg.expand(e, 0)
        svg.set_innie([True])
        svg.set_outie(True)
        svg.set_tab(False)
        svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = (('number', True, svg.docks[1][0], svg.docks[1][1]),
                      ('number', False, svg.docks[0][0], svg.docks[0][1]))
        self._left, self._right = svg.docks[1][0], svg.docks[1][0]

    def _make_number_style_porch(self, e, svg):
        svg.expand(e, 0)
        svg.set_innie([True,True])
        svg.set_outie(True)
        svg.set_tab(False)
        svg.set_slot(False)
        svg.set_porch(True)
        self._make_basic_block(svg)
        self.docks = (('number', True, svg.docks[2][0], svg.docks[2][1]),
                      ('number', False, svg.docks[0][0], svg.docks[0][1]),
                      ('number', False, svg.docks[1][0], svg.docks[1][1])) 
        self._left, self._right = svg.docks[2][0], svg.get_width()-svg.docks[0][0]

    def _make_compare_style(self, e, svg):
        svg.expand(10+e,0)
        self._make_boolean_compare(svg)
        self.docks = (('bool', True, svg.docks[0][0], svg.docks[0][1]),
                      ('number', False, svg.docks[1][0], svg.docks[1][1]),
                      ('number', False, svg.docks[2][0], svg.docks[2][1])) 
        self._left, self._right = svg.get_width()-svg.docks[2][0], 0

    def _make_boolean_style(self, e, svg):
        svg.expand(10+e,0)
        self._make_boolean_and_or(svg)
        self.docks = (('bool', True, svg.docks[0][0], svg.docks[0][1]),
                      ('bool', False, svg.docks[1][0], svg.docks[1][1]),
                      ('bool', False, svg.docks[2][0], svg.docks[2][1]))
        self._left, self._right = svg.get_width()-svg.docks[1][0], 0

    def _make_not_style(self, e, svg):
        svg.expand(15+e, 0)
        self._make_boolean_not(svg)
        self.docks = (('bool', True, svg.docks[0][0], svg.docks[0][1]),
                      ('bool', False, svg.docks[1][0], svg.docks[1][1]))
        self._right = svg.get_width()-svg.docks[1][0]
        self._left = self._right

    def _make_flow_style(self, e, svg):
        svg.expand(25+e, 0)
        svg.set_slot(True)
        self._make_basic_flow(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('flow', False, svg.docks[1][0], svg.docks[1][1]))
        self._left, self._right = 0, svg.get_width()-svg.docks[1][0]

    def _make_flow_style_1arg(self, e, svg):
        svg.expand(25+e, 0)
        svg.set_slot(True)
        svg.set_tab(True)
        svg.set_innie([True])
        self._make_basic_flow(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('number', False, svg.docks[1][0], svg.docks[1][1]),
                      ('flow', False, svg.docks[2][0], svg.docks[2][1]),
                      ('flow', False, svg.docks[3][0], svg.docks[3][1]))
        self._left, self._right = 0, svg.get_width()-svg.docks[1][0]

    def _make_flow_style_boolean(self, e, svg):
        svg.expand(25+e, 0)
        svg.set_slot(True)
        svg.set_tab(True)
        svg.set_boolean(True)
        self._make_basic_flow(svg)
        self.docks = (('flow', True, svg.docks[0][0], svg.docks[0][1]),
                      ('bool', False, svg.docks[1][0], svg.docks[1][1]),
                      ('flow', False, svg.docks[2][0], svg.docks[2][1]),
                      ('flow', False, svg.docks[3][0], svg.docks[3][1]))
        self._left, self._right = 0, svg.get_width()-svg.docks[1][0]

    def _make_basic_block(self, svg):
        self.shape = svg_str_to_pixbuf(svg.basic_block())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_block())

    def _make_basic_box(self, svg):
        self.shape = svg_str_to_pixbuf(svg.basic_box())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_box())

    def _make_basic_flow(self, svg):
        self.shape = svg_str_to_pixbuf(svg.basic_flow())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_flow())

    def _make_boolean_compare(self, svg):
        self.shape = svg_str_to_pixbuf(svg.boolean_compare())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.boolean_compare())

    def _make_boolean_and_or(self, svg):
        self.shape = svg_str_to_pixbuf(svg.boolean_and_or())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.boolean_and_or())

    def _make_boolean_not(self, svg):
        self.shape = svg_str_to_pixbuf(svg.boolean_not())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.boolean_not())
