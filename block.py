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
import sprite_factory
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
    def __init__(self, block_list, sprite_list, proto_name, x, y, labels=[], 
                 colors=["#00FF00","#00A000"], scale=2.0):
        self.spr = None
        self.shape = None
        self.selected_shape = None
        self.name = proto_name
        self.docks = None
        self.connections = None
        self._new_block_from_prototype(sprite_list, proto_name, labels, colors,
                                       scale, x, y)
        block_list.append_to_list(self)
        #
        # TODO:
        # Logo code
        # HTML code
        # debug code
        # etc.

    def _new_block_from_prototype(self, sprite_list, name, labels, colors,
                                  scale, x, y):
        if len(labels) == 0:
            print "new block: %s (%d %d)" % (name, x, y)
        else:
            print "new block: %s %s (%d %d)" % (name, labels[0], x, y)

        svg = sprite_factory.SVG()
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
        svg.set_scale(scale)
        svg.set_gradiant(True)
        svg.set_innie([False])
        svg.set_outie(False)
        svg.set_tab(True)
        svg.set_slot(True)
        if name in BASIC_STYLE:
            svg.expand(40,0)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,37,5),('flow',False,37,39))
        elif name in BASIC_STYLE_HEAD:
            svg.expand(40,0)
            svg.set_slot(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('start',True,37,0), ('flow',False,37,39))
        elif name in BASIC_STYLE_HEAD_1ARG:
            svg.expand(40,0)
            svg.set_slot(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('start',True,37,0), ('string',False,42,12),
                          ('flow',False,37,44))
        elif name in BASIC_STYLE_TAIL:
            svg.expand(40,0)
            svg.set_tab(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,37,5),('unavailable',False,0,0))
        elif name in BASIC_STYLE_1ARG:
            ex = 25
            ey = 0
            svg.expand(ex,ey)
            svg.set_innie([True])
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,37,5), ('num',False,42+ex*scale,12),
                          ('flow',False,37,44+ey))
        elif name in BASIC_STYLE_2ARG:
            ex = 25
            ey = 0
            svg.expand(ex,ey)
            svg.set_innie([True,True])
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,37,5), ('num',False,42+ex*scale,12),
                          ('num',False,42+ex*scale,54), ('flow',False,37,81))
        elif name in BOX_STYLE:
            svg.expand(50,0)
            self._make_basic_box(sprite_list, svg, x, y)
            self.docks = (('num',True,0,12),('unavailable',False,105,12))
        else:
            svg.expand(40,0)
            self._make_basic_block(sprite_list, svg, x, y)
            print "don't know how to create a block for %s" % (name)

        if len(labels) > 0:
            self.spr.set_label(_(labels[0]))
            for label in labels:
                self.spr.set_label(label, labels.index(label))

        self.type = 'block'
        if DEFAULTS.has_key(name):
            self.defaults = DEFAULTS[name]
        else:
            self.defaults = []

    def _make_basic_block(self, sprite_list, svg, x, y):
        self.shape = sprite_factory.svg_str_to_pixbuf(svg.basic_block())
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape =\
                     sprite_factory.svg_str_to_pixbuf(svg.basic_block())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

    def _make_basic_box(self, sprite_list, svg, x, y):
        self.shape = sprite_factory.svg_str_to_pixbuf(svg.basic_box())
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = sprite_factory.svg_str_to_pixbuf(svg.basic_box())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

