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
    def __init__(self, font_scale_factor = 1):
        self.list = []
        self.font_scale_factor = font_scale_factor

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

    def print_list(self, block_type=None):
        for i, block in enumerate(self.list):
            if block_type is None or block_type == block.type:
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
    #
    # TODO:
    # block data should be stored in block, not in block.spr.label
    # Logo code
    # HTML code
    # debug code
    # etc.
    def __init__(self, block_list, sprite_list, name, x, y, type='block',
                 values=[], scale=2.0, colors=["#00FF00","#00A000"]):
        self.spr = None
        self.shapes = []
        self.name = name
        self.colors = colors
        self.scale = scale
        self.docks = None
        self.connections = None
        self.values = []
        self.content = None
        self.primitive = None
        self.type = type
        self._ex = 0
        self._ey = 0
        self._font_size = [6.0, 4.5]
        self._left = 2
        self._right = 2

        if OLD_NAMES.has_key(self.name):
            self.name = OLD_NAMES[self.name]

        for i in range(len(self._font_size)):
            self._font_size[i] *= self.scale*block_list.font_scale_factor

        self.values = values

        self._new_block_from_factory(sprite_list, x, y)

        # TODO: add media block graphics here
        if name in CONTENT_BLOCKS:
            self.content = self.name

        if PRIMITIVES.has_key(name):
            self.primitive = PRIMITIVES[self.name]

        block_list.append_to_list(self)

    # We need to resize some blocks on the fly.
    def resize(self):
        # make sure the label fits
        lw = self.spr.label_width()        
        lwh = self.spr.label_area_dimensions()
        if lw > lwh[0]:
            e = (lw-lwh[0])
            self._make_block(e, self.svg)
            self.spr.set_shape(self.shapes[0])

    # We may want to rescale blocks as well.
    def rescale(self, scale):
        for i in range(len(self._font_size)):
            self._font_size[i] /= self.scale
        self.scale = scale
        for i in range(len(self._font_size)):
            self._font_size[i] *= self.scale
        self._make_block(e, self.svg)
        self.spr.set_shape(self.shapes[0])

    # We may want to grow a block vertically.
    def expand_in_y(self, dy):
        self._ey += dy
        self._make_block(0, self.svg)
        self.spr.set_shape(self.shapes[0])

    # We may want to grow a block vertically.
    def expand_in_x(self, dx):
        self._ex += dx
        self._make_block(0, self.svg)
        self.spr.set_shape(self.shapes[0])

    def _new_block_from_factory(self, sprite_list, x, y):
        self.svg = SVG()
        self.svg.set_scale(self.scale)
        self.svg.set_gradiant(True)
        self.svg.set_innie([False])
        self.svg.set_outie(False)
        self.svg.set_tab(True)
        self.svg.set_slot(True)

        self._make_block(0, self.svg)
        self.spr = sprites.Sprite(sprite_list, x, y, self.shapes[0])

        self.spr.set_margins(self._left, self.svg.get_slot_depth(), self._right,
                             self.svg.get_slot_depth()*2)

        if self.name in CONTENT_BLOCKS and len(self.values) > 0:
            for i, v in enumerate(self.values):
                self._set_labels(i, str(v))
        elif BLOCK_NAMES.has_key(self.name):
            for i, n in enumerate(BLOCK_NAMES[self.name]):
                self._set_labels(i, n)

        # Make sure the labels fit.
        self.resize()

    def _set_labels(self, i, label):
        if i == 1: # top
            self.spr.set_label_attributes(int(self._font_size[1]+0.5), True,
                                          "right", "top", i)
        elif i == 2: # bottom
            self.spr.set_label_attributes(int(self._font_size[1]+0.5), True,
                                          "right", "bottom", i)
        else:
            self.spr.set_label_attributes(int(self._font_size[0]+0.5), True,
                                          "center", "middle", i)
        self.spr.set_label(label, i)

    def _make_block(self, e, svg):
        self._set_colors(svg)
        self.svg.set_stroke_width(STANDARD_STROKE_WIDTH)
        self.svg.clear_docks()
        self.shapes = []
        if self.name in BASIC_STYLE:
            self._make_basic_style(e, svg)
        elif self.name in BASIC_STYLE_HEAD:
            self._make_basic_style_head(e, svg)
        elif self.name in BASIC_STYLE_HEAD_1ARG:
            self._make_basic_style_head_1arg(e, svg)
        elif self.name in BASIC_STYLE_TAIL:
            self._make_basic_style_tail(e, svg)
        elif self.name in BASIC_STYLE_1ARG:
            self._make_basic_style_1arg(e, svg)
        elif self.name in BASIC_STYLE_2ARG:
            self._make_basic_style_2arg(e, svg)
        elif self.name in BOX_STYLE:
            self._make_box_style(e, svg)
        elif self.name in NUMBER_STYLE:
            self._make_number_style(e, svg)
        elif self.name in NUMBER_STYLE_BLOCK:
            self._make_number_style_block(e, svg)
        elif self.name in NUMBER_STYLE_1ARG:
            self._make_number_style_1arg(e, svg)
        elif self.name in NUMBER_STYLE_PORCH:
            self._make_number_style_porch(e, svg)
        elif self.name in COMPARE_STYLE:
            self._make_compare_style(e, svg)
        elif self.name in BOOLEAN_STYLE:
            self._make_boolean_style(e, svg)
        elif self.name in NOT_STYLE:
            self._make_not_style(e, svg)
        elif self.name in FLOW_STYLE:
            self._make_flow_style(e, svg)
        elif self.name in FLOW_STYLE_1ARG:
            self._make_flow_style_1arg(e, svg)
        elif self.name in FLOW_STYLE_BOOLEAN:
            self._make_flow_style_boolean(e, svg)
        elif self.name in FLOW_STYLE_ELSE:
            self._make_flow_style_else(e, svg)
        else:
            self._make_basic_style(e, svg)
            print ">>>>> I don't know how to create a %s block" % (self.name)

    def _set_colors(self, svg):
        if BOX_COLORS.has_key(self.name):
            self.colors = BOX_COLORS[self.name]
        else:
            for p in range(len(PALETTES)):
                if self.name in PALETTES[p]:
                    self.colors = COLORS[p]
        self.svg.set_colors(self.colors)

    def _make_basic_style(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self._make_basic_block(svg)
        self.docks = (('flow',True,self.svg.docks[0][0],self.svg.docks[0][1]),
                      ('flow',False,self.svg.docks[1][0],self.svg.docks[1][1]))
        self._left, self._right = 2, 2

    def _make_basic_style_head(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self.svg.set_slot(False)
        self.svg.set_cap(True)
        self._make_basic_block(svg)
        self.docks = (('start', True, 0, 0),
                      ('flow', False, self.svg.docks[0][0],
                                      self.svg.docks[0][1]))
        self._left, self._right = 2, 2

    def _make_basic_style_head_1arg(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self.svg.set_innie([True])
        self.svg.set_slot(False)
        self.svg.set_cap(True)
        self._make_basic_block(svg)
        self.docks = (('start', True, 0, 0),
                      ('string', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]),
                      ('flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]))
        self._left, self._right = 2, self.svg.get_innie_width()*1.5

    def _make_basic_style_tail(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self.svg.set_tab(False)
        self._make_basic_block(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('unavailable', False, 0, 0))

    def _make_basic_style_1arg(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self.svg.set_innie([True])
        self._make_basic_block(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]),
                      ('flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]))
        self._left, self._right = 2, self.svg.get_innie_width()*1.5

    def _make_basic_style_2arg(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self.svg.set_innie([True,True])
        self._make_basic_block(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]),
                      ('number', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]),
                      ('flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]))
        self._left, self._right = 2, self.svg.get_innie_width()*1.5

    def _make_box_style(self, e, svg):
        self.svg.expand(60+e+self._ex, self._ey)
        self._make_basic_box(svg)
        self.docks = (('number', True, self.svg.docks[0][0],
                                       self.svg.docks[0][1]),
                      ('unavailable', False, 0, 0))
        self._left, self._right = self.svg.docks[1][0], 1

    def _make_number_style(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_innie([True,True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        """
        NOTE: The "outie" is added last, so the dock order in the NUMBER_STYLE
        needs to be modified.
        """
        self.docks = (('number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1]),
                      ('number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1])) 
        self._left = self.svg.docks[2][0]
        self._right = self.svg.get_innie_width()*1.5

    def _make_number_style_block(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_innie([True,True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = (('number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1], '('),
                      ('number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]),
                      ('unavailable', False, 0, 0, ')'))
        self._left = self.svg.docks[2][0]
        self._right = self.svg.get_innie_width()*1.5

    def _make_number_style_1arg(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_innie([True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = (('number', True, self.svg.docks[1][0],
                                       self.svg.docks[1][1]),
                      ('number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]))
        self._left, self._right = self.svg.docks[1][0], self.svg.docks[1][0]

    def _make_number_style_porch(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_innie([True,True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self.svg.set_porch(True)
        self._make_basic_block(svg)
        self.docks = (('number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1]),
                      ('number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1])) 
        self._left = self.svg.docks[2][0]
        self._right = self.svg.get_width()-self.svg.docks[0][0]

    def _make_compare_style(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self._make_boolean_compare(svg)
        self.docks = (('bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1], '('),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]),
                      ('number', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]),
                      ('unavailable', False, 0, 0, ')'))
        self._left, self._right = self.svg.get_width()-self.svg.docks[2][0], 0

    def _make_boolean_style(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self._make_boolean_and_or(svg)
        self.docks = (('bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]),
                      ('bool', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]))
        self._left, self._right = self.svg.get_width()-self.svg.docks[1][0], 0
 
    def _make_not_style(self, e, svg):
        self.svg.expand(15+e+self._ex, self._ey)
        self._make_boolean_not(svg)
        self.docks = (('bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]))
        self._right = self.svg.get_width()-self.svg.docks[1][0]
        self._left = self._right

    def _make_flow_style(self, e, svg):
        self.svg.expand(10+e+self._ex, self._ey)
        self.svg.set_slot(True)
        self.svg.set_tab(False)
        self._make_basic_flow(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1], '['),
                      ('unavailable', False, 0, 0, ']'))
        self._left, self._right = 0, self.svg.get_width()-self.svg.docks[1][0]

    def _make_flow_style_1arg(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True])
        self._make_basic_flow(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]),
                      ('flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], '['),
                      ('flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']'))
        self._left = 2
        self._right = self.svg.get_width()-self.svg.docks[1][0]+ \
                      self.svg.get_innie_width()*1.5

    def _make_flow_style_boolean(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_boolean(True)
        self._make_basic_flow(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]),
                      ('flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], '['),
                      ('flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']'))
        self._left, self._right = 2, self.svg.get_width()-self.svg.docks[1][0]

    def _make_flow_style_else(self, e, svg):
        self.svg.expand(e+self._ex, self._ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_else(True)
        self.svg.set_boolean(True)
        self._make_basic_flow(svg)
        self.docks = (('flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]),
                      ('bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]),
                      ('flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], '['),
                      ('flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], ']['),
                      ('flow', False, self.svg.docks[4][0],
                                      self.svg.docks[4][1], ']'))
        self._left, self._right = 2, self.svg.get_width()-self.svg.docks[1][0]

    def _make_basic_block(self, svg):
        self.shapes.append(svg_str_to_pixbuf(self.svg.basic_block()))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes.append(svg_str_to_pixbuf(self.svg.basic_block()))

    def _make_basic_box(self, svg):
        self.shapes.append(svg_str_to_pixbuf(self.svg.basic_box()))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes.append(svg_str_to_pixbuf(self.svg.basic_box()))

    def _make_basic_flow(self, svg):
        self.shapes.append(svg_str_to_pixbuf(self.svg.basic_flow()))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes.append(svg_str_to_pixbuf(self.svg.basic_flow()))

    def _make_boolean_compare(self, svg):
        self.shapes.append(svg_str_to_pixbuf(self.svg.boolean_compare()))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes.append(svg_str_to_pixbuf(self.svg.boolean_compare()))

    def _make_boolean_and_or(self, svg):
        self.shapes.append(svg_str_to_pixbuf(self.svg.boolean_and_or()))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes.append(svg_str_to_pixbuf(self.svg.boolean_and_or()))

    def _make_boolean_not(self, svg):
        self.shapes.append(svg_str_to_pixbuf(self.svg.boolean_not()))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes.append(svg_str_to_pixbuf(self.svg.boolean_not()))
