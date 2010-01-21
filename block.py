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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
from constants import *
import sprite_factory
import sprites

#
# A class for the list of blocks and everything they share in common
#
class Blocks:
    def __init__(self, sprite_list):
        self.list = []
        self.sprites = sprite_list

    def get_block(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self,block):
        self.list.append(block)

    def insert_in_list(self,block,i):
        if i < 0:
            self.list.insert(0, block)
        elif i > len(self.list)-1:
            self.list.append(block)
        else:
            self.list.insert(i, block)

    def remove_from_list(self, block):
        if block in self.list:
            self.list.remove(block)

    #
    # block and spr utilities
    #
    def spr_to_block(self, spr):
        for b in self.list:
            if spr == b.spr:
                return b

#
# A class for the individual blocks
#
class Block:
    def __init__(self, blocks, proto_name, x, y, labels=[], 
                 colors=["#00FF00","#00A000"], scale=2.0):
        self.blocks = blocks
        self.spr = None
        self.shape = None
        self.selected_shape = None
        self._new_block_from_prototype(proto_name, labels, colors, scale, x, y)
        self.blocks.append_to_list(self)
        #
        # TODO:
        # save arguments
        # dock and connection info
        # highlight image
        # Logo code
        # HTML code
        # debug code
        # etc.

    def _new_block_from_prototype(self, name, labels, colors, scale, x, y):
        if len(labels) == 0:
            print "%s (%d %d)" % (name, x, y)
        else:
            print "%s %s (%d %d)" % (name, labels[0], x, y)

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
            self._make_basic_block(svg, x, y)
            self.docks = (('flow',True,37,5),('flow',False,37,44))
            print "created new basic block: %s" % (str(self.spr))
        elif name in BASIC_STYLE_HEAD:
            svg.expand(40,0)
            svg.set_slot(False)
            self._make_basic_block(svg, x, y)
            self.docks = (('start',True,50,0), ('flow',False,49,55))
            print "created new basic block head: %s" % (str(self.spr))
        elif name in BASIC_STYLE_HEAD_1ARG:
            svg.expand(40,0)
            svg.set_slot(False)
            self._make_basic_block(svg, x, y)
            self.docks = (('start',True,50,0), ('string',False,21,38),
                          ('flow',False,75,75))
            print "created new basic block head: %s" % (str(self.spr))
        elif name in BASIC_STYLE_TAIL:
            svg.expand(40,0)
            svg.set_tab(False)
            self._make_basic_block(svg, x, y)
            self.docks = (('flow',True,37,5),('unavailable',False,0,0))
            print "created new basic block tail: %s" % (str(self.spr))
        elif name in BASIC_STYLE_1ARG:
            svg.expand(20,0)
            svg.set_innie([True])
            self._make_basic_block(svg, x, y)
            self.docks = (('flow',True,37,5), ('num',False,74,21),
                          ('flow',False,37,44))
            print "created new basic block 1 arg: %s" % (str(self.spr))
        elif name in BASIC_STYLE_2ARG:
            svg.expand(20,0)
            svg.set_innie([True,True])
            self._make_basic_block(svg, x, y)
            self.docks = (('flow',True,37,5), ('num',False,74,21),
                          ('num',False,74,58), ('flow',False,37,81))
            print "created new basic block 2 args: %s" % (str(self.spr))
        elif name in BOX_STYLE:
            svg.expand(50,0)
            self._make_basic_box(svg, x, y)
            self.docks = (('num',True,0,12),('numend',False,105,12))
            print "created new box block: %s" % (str(self.spr))
        else:
            svg.expand(40,0)
            self._make_basic_block(svg, x, y)
            print "don't know how to create a block for %s" % (name)

        if len(labels) > 0:
            self.spr.set_label(labels[0])
            for label in labels:
                self.spr.set_label(label, labels.index(label))

        self.type = 'block'

    def _make_basic_block(self, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.basic_block())
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_block())
        self.spr = sprites.Sprite(self.blocks.sprites, x, y, self.shape)

    def _make_basic_box(self, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.basic_box())
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_box())
        self.spr = sprites.Sprite(self.blocks.sprites, x, y, self.shape)

class Turtle:
    def __init__(self, blocks, orientation=0, scale=1.0):
        self.blocks = blocks
        self.spr = None
        self._new_turtle_from_prototype(orientation, scale)
        self.blocks.append_to_list(self)
        self.orientation = orientation

    def _new_turtle_from_prototype(self, orientation, scale):
        svg = sprite_factory.SVG()
        svg.set_scale(scale)
        svg.set_orientation(orientation)
        self.spr = sprites.Sprite(self.blocks.sprites, 0, 0,
                                  svg_str_to_pixbuf(svg.turtle()))
        self.type = 'turtle'

#
# Load pixbuf from SVG string
#
def svg_str_to_pixbuf(svg_string):
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf

