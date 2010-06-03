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

import gtk
from taconstants import *
from tasprite_factory import SVG, svg_str_to_pixbuf
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

    def set_scale(self, scale):
        for b in self.list:
            for i in range(len(b._font_size)):
                b._font_size[i] *= b.scale*scale/self.font_scale_factor
        self.font_scale_factor = scale

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
    def __init__(self, block_list, sprite_list, name, x, y, type='block',
                 values=[], scale=BLOCK_SCALE, colors=["#FF0000","#A00000"]):
        self.spr = None
        self.shapes = [None, None]
        self.name = name
        self.colors = colors
        self.scale = scale
        self.docks = None
        self.connections = None
        self.status = None
        self.values = []
        self.primitive = None
        self.type = type
        self.dx = 0
        self.ex = 0
        self.ey = 0
        self._ei = 0
        self._font_size = [6.0, 4.5]
        self._image = None

        if OLD_NAMES.has_key(self.name):
            self.name = OLD_NAMES[self.name]

        for i in range(len(self._font_size)):
            self._font_size[i] *= self.scale*block_list.font_scale_factor

        for v in (values):
            self.values.append(v)

        self._new_block_from_factory(sprite_list, x, y)

        if PRIMITIVES.has_key(name):
            self.primitive = PRIMITIVES[self.name]

        block_list.append_to_list(self)

    # We may want to highlight a block...
    def highlight(self):
        if self.spr is not None:
            self.spr.set_shape(self.shapes[1])

    # Or unhighlight it.
    def unhighlight(self):
        if self.spr is not None:
            self.spr.set_shape(self.shapes[0])

    # We need to resize some blocks on the fly so that the labels fit.
    def resize(self):
        if not self.spr is not None:
            return
        dx = (self.spr.label_width()-self.spr.label_safe_width())/self.scale
        if dx !=0:
            self.dx += dx
            if self.dx < 0:
                self.dx = 0
            self.refresh()

    # Some blocks get a skin.
    def set_image(self, image, x, y):
        if not self.spr is not None:
            return
        self._image = image
        self.spr.set_image(image, 1, x, y)

    # The skin might need scaling.
    # Keep the original here, the scaled version stays with the sprite.
    def scale_image(self, x, y, w, h):
        if not self.spr is not None:
            return
        if self._image is not None:
            tmp = self._image.scale_simple(w, h,
                                   gtk.gdk.INTERP_NEAREST)
            self.spr.set_image(tmp, 1, x, y)

    # We may want to rescale blocks as well.
    def rescale(self, scale):
        if not self.spr is not None:
            return
        for i in range(len(self._font_size)):
            self._font_size[i] /= self.scale
        self.dx /= self.scale
        self.ex /= self.scale
        self.ey /= self.scale
        self.scale = scale
        for i in range(len(self._font_size)):
            self._font_size[i] *= self.scale
        self.dx *= self.scale
        self.ex *= self.scale
        self.ey *= self.scale
        self._set_label_attributes()
        self.svg.set_scale(self.scale)
        self.refresh()
        self.spr.draw()

    def refresh(self):
        if not self.spr is not None:
            return
        self._make_block(self.svg)
        self._set_margins()
        self.spr.set_shape(self.shapes[0])

    # We may want to add additional slots for arguments ("innies").
    def add_arg(self, keep_expanding=True):
        if not self.spr is not None:
            return
        h = self.svg.get_height()
        self._ei += 1
        if self.type == 'block' and keep_expanding:
            self.svg.set_show(True)
        else:
            self.svg.set_show(False)
        self.refresh()
        return self.svg.get_height()-h

    # We may want to grow a block vertically.
    def expand_in_y(self, dy):
        if not self.spr is not None:
            return
        self.ey += dy
        if self.type == 'block':
            self.svg.set_hide(True)
            self.svg.set_show(True)
        else:
            self.svg.set_hide(False)
            self.svg.set_show(False)
        self.refresh()

    # We may want to grow a block horizontally.
    def expand_in_x(self, dx):
        if not self.spr is not None:
            return
        self.ex += dx
        if self.type == 'block':
            self.svg.set_hide(True)
            self.svg.set_show(True)
        else:
            self.svg.set_hide(False)
            self.svg.set_show(False)
        self.refresh()

    def reset_x(self):
        if not self.spr is not None:
            return 0
        dx = -self.ex
        self.ex = 0
        self.svg.set_hide(False)
        if self.type == 'block':
            self.svg.set_show(True)
        else:
            self.svg.set_show(False)
        self.refresh()
        return dx

    def reset_y(self):
        if not self.spr is not None:
            return 0
        dy = -self.ey
        self.ey = 0
        self.svg.set_hide(False)
        if self.type == 'block':
            self.svg.set_show(True)
        else: # 'proto'
            self.svg.set_show(False)
        self.refresh()
        return dy

    def get_expand_x_y(self):
        if not self.spr is not None:
            return(0, 0)
        return (self.ex, self.ey)

    def _new_block_from_factory(self, sprite_list, x, y):
        self.svg = SVG()
        self.svg.set_scale(self.scale)
        self.svg.set_gradiant(True)
        self.svg.set_innie([False])
        self.svg.set_outie(False)
        self.svg.set_tab(True)
        self.svg.set_slot(True)

        if self.name in EXPANDABLE and self.type == 'block':
            self.svg.set_show(True)

        self._make_block(self.svg)
        if sprite_list is not None:
            self.spr = sprites.Sprite(sprite_list, x, y, self.shapes[0])
            self._set_margins()
            self._set_label_attributes()

            if (self.name == 'number' or self.name == 'string') and\
               len(self.values) > 0:
                for i, v in enumerate(self.values):
                    if v is not None:
                        self._set_labels(i, str(v))
            elif BLOCK_NAMES.has_key(self.name):
                for i, n in enumerate(BLOCK_NAMES[self.name]):
                    self._set_labels(i, n)

            # Make sure the labels fit.
            if self.spr.label_width() > self.spr.label_safe_width():
                self.resize()

    def _set_margins(self):
        self.spr.set_margins(self.svg.margins[0], self.svg.margins[1],
                             self.svg.margins[2], self.svg.margins[3])

    def _set_label_attributes(self):
        if self.name in CONTENT_BLOCKS:
            n = len(self.values)
            if n == 0:
                n = 1 # Force a scale to be set, even if there is no value.
        else:
            n = len(BLOCK_NAMES[self.name])
        for i in range(n):
            if i == 1: # top
                self.spr.set_label_attributes(int(self._font_size[1]+0.5), True,
                                              "right", "top", i)
            elif i == 2: # bottom
                self.spr.set_label_attributes(int(self._font_size[1]+0.5), True,
                                              "right", "bottom", i)
            else:
                self.spr.set_label_attributes(int(self._font_size[0]+0.5), True,
                                              "center", "middle", i)

    def _set_labels(self, i, label):
        self.spr.set_label(label, i)

    def _make_block(self, svg):
        self._left = 0
        self._top = 0
        self._right = 0
        self._bottom = 0
        self._set_colors(svg)
        self.svg.set_stroke_width(STANDARD_STROKE_WIDTH)
        self.svg.clear_docks()
        if self.name in BASIC_STYLE:
            self._make_basic_style(svg)
        elif self.name in BASIC_STYLE_HEAD:
            self._make_basic_style_head(svg)
        elif self.name in BASIC_STYLE_EXTENDED:
            self._make_basic_style(svg, 16)
        elif self.name in BASIC_STYLE_HEAD_1ARG:
            self._make_basic_style_head_1arg(svg)
        elif self.name in BASIC_STYLE_TAIL:
            self._make_basic_style_tail(svg)
        elif self.name in BASIC_STYLE_1ARG:
            self._make_basic_style_1arg(svg)
        elif self.name in BASIC_STYLE_2ARG:
            self._make_basic_style_2arg(svg)
        elif self.name in BASIC_STYLE_VAR_ARG:
            self._make_basic_style_var_arg(svg)
        elif self.name in BULLET_STYLE:
            self._make_bullet_style(svg)
        elif self.name in BOX_STYLE:
            self._make_box_style(svg)
        elif self.name in BOX_STYLE_MEDIA:
            self._make_media_style(svg)
        elif self.name in NUMBER_STYLE:
            self._make_number_style(svg)
        elif self.name in NUMBER_STYLE_BLOCK:
            self._make_number_style_block(svg)
        elif self.name in NUMBER_STYLE_VAR_ARG:
            self._make_number_style_var_arg(svg)
        elif self.name in NUMBER_STYLE_1ARG:
            self._make_number_style_1arg(svg)
        elif self.name in NUMBER_STYLE_1STRARG:
            self._make_number_style_1strarg(svg)
        elif self.name in NUMBER_STYLE_PORCH:
            self._make_number_style_porch(svg)
        elif self.name in COMPARE_STYLE:
            self._make_compare_style(svg)
        elif self.name in BOOLEAN_STYLE:
            self._make_boolean_style(svg)
        elif self.name in NOT_STYLE:
            self._make_not_style(svg)
        elif self.name in FLOW_STYLE:
            self._make_flow_style(svg)
        elif self.name in FLOW_STYLE_TAIL:
            self._make_flow_style_tail(svg)
        elif self.name in FLOW_STYLE_1ARG:
            self._make_flow_style_1arg(svg)
        elif self.name in FLOW_STYLE_BOOLEAN:
            self._make_flow_style_boolean(svg)
        elif self.name in FLOW_STYLE_WHILE:
            self._make_flow_style_while(svg)
        elif self.name in FLOW_STYLE_ELSE:
            self._make_flow_style_else(svg)
        elif self.name in COLLAPSIBLE_TOP:
            self._make_collapsible_style_top(svg)
        elif self.name in COLLAPSIBLE_TOP_NO_ARM:
            self._make_collapsible_style_top(svg, True)
        elif self.name in COLLAPSIBLE_BOTTOM:
            self._make_collapsible_style_bottom(svg)
        elif self.name in PORTFOLIO_STYLE_2x2:
            self._make_portfolio_style_2x2(svg)
        elif self.name in PORTFOLIO_STYLE_2x1:
            self._make_portfolio_style_2x1(svg)
        elif self.name in PORTFOLIO_STYLE_1x1:
            self._make_portfolio_style_1x1(svg)
        elif self.name in PORTFOLIO_STYLE_1x2:
            self._make_portfolio_style_1x2(svg)
        else:
            self._make_basic_style(svg)
            print "WARNING: I don't know how to create a %s block" % (self.name)

    def _set_colors(self, svg):
        if BOX_COLORS.has_key(self.name):
            self.colors = BOX_COLORS[self.name]
        else:
            for p in range(len(PALETTES)):
                if self.name in PALETTES[p]:
                    self.colors = COLORS[p]
        self.svg.set_colors(self.colors)

    def _make_basic_style(self, svg, extension=0):
        self.svg.expand(self.dx+self.ex+extension, self.ey+extension)
        self._make_basic_block(svg)
        self.docks = [['flow',True,self.svg.docks[0][0],self.svg.docks[0][1]],
                      ['flow',False,self.svg.docks[1][0],self.svg.docks[1][1]]]

    def _make_basic_style_head(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_slot(False)
        self.svg.set_cap(True)
        self._make_basic_block(svg)
        self.docks = [['unavailable', False, 0, 0],
                      ['flow', False, self.svg.docks[0][0],
                                      self.svg.docks[0][1]]]

    def _make_basic_style_head_1arg(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_innie([True])
        self.svg.set_slot(False)
        self.svg.set_cap(True)
        self._make_basic_block(svg)
        self.docks = [['unavailable', False, 0, 0],
                      ['string', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_basic_style_tail(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_tab(False)
        self._make_basic_block(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_basic_style_1arg(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_innie([True])
        self._make_basic_block(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]]]

    def _make_basic_style_2arg(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_innie([True,True])
        self._make_basic_block(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['number', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]]]

    def _make_basic_style_var_arg(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        innie = [True]
        for i in range(self._ei):
            innie.append(True)
        self.svg.set_innie(innie)
        self._make_basic_block(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]]]
        for i in range(self._ei):
            self.docks.append(['number', False, self.svg.docks[i+2][0],
                                                self.svg.docks[i+2][1]])
        self.docks.append(['flow', False, self.svg.docks[self._ei+2][0],
                                      self.svg.docks[self._ei+2][1]])

    def _make_bullet_style(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        innie = [True, True]
        for i in range(self._ei):
            innie.append(True)
        self.svg.set_innie(innie)
        self._make_basic_block(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1], '['],
                      ['string', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]]]
        for i in range(self._ei):
            self.docks.append(['string', False, self.svg.docks[i+3][0],
                                                self.svg.docks[i+3][1]])
        self.docks.append(['flow', False, self.svg.docks[self._ei+3][0],
                                      self.svg.docks[self._ei+3][1], ']'])

    def _make_box_style(self, svg):
        self.svg.expand(60+self.dx+self.ex, self.ey)
        self._make_basic_box(svg)
        self.docks = [['number', True, self.svg.docks[0][0],
                                       self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_media_style(self, svg):
        self.svg.expand(40+self.dx+self.ex, 10+self.ey)
        self._make_basic_box(svg)
        self.docks = [['number', True, self.svg.docks[0][0],
                                       self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_number_style(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_innie([True,True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        """
        NOTE: The "outie" is added last, so the dock order in NUMBER_STYLE
              blocks needs to be modified.
        """
        self.docks = [['number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]]] 

    def _make_number_style_var_arg(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        innie = [True]
        for i in range(self._ei+1):
            innie.append(True)
        self.svg.set_innie(innie)
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = [['number', True, self.svg.docks[2+self._ei][0],
                                       self.svg.docks[2+self._ei][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]]]
        for i in range(self._ei+1):
            self.docks.append(['number', False, self.svg.docks[i+1][0],
                                                self.svg.docks[i+1][1]])
        self.docks.append(['unavailable', False, 0, 0])

    def _make_number_style_block(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_innie([True,True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = [['number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1], '('],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['unavailable', False, 0, 0, ')']]

    def _make_number_style_1arg(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_innie([True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = [['number', True, self.svg.docks[1][0],
                                       self.svg.docks[1][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]]]

    def _make_number_style_1strarg(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_innie([True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_basic_block(svg)
        self.docks = [['number', True, self.svg.docks[1][0],
                                       self.svg.docks[1][1]],
                      ['string', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_number_style_porch(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_innie([True,True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self.svg.set_porch(True)
        self._make_basic_block(svg)
        self.docks = [['number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]]] 

    def _make_compare_style(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self._make_boolean_compare(svg)
        self.docks = [['bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1], '('],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['number', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]],
                      ['unavailable', False, 0, 0, ')']]

    def _make_boolean_style(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self._make_boolean_and_or(svg)
        self.docks = [['bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['bool', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]]]
 
    def _make_not_style(self, svg):
        self.svg.expand(15+self.dx+self.ex, self.ey)
        self._make_boolean_not(svg)
        self.docks = [['bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_flow_style(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self._make_basic_flow(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1], '['],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], ']']]

    def _make_flow_style_tail(self, svg):
        self.svg.expand(10+self.dx+self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(False)
        self._make_basic_flow(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_flow_style_1arg(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True])
        self._make_basic_flow(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], '['],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']']]

    def _make_flow_style_boolean(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_boolean(True)
        self._make_basic_flow(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], '['],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']']]

    def _make_flow_style_while(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_boolean(True)
        self._make_basic_flow(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1], '['],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], ']['],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']']]

    def _make_flow_style_else(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_else(True)
        self.svg.set_boolean(True)
        self._make_basic_flow(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], '['],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], ']['],
                      ['flow', False, self.svg.docks[4][0],
                                      self.svg.docks[4][1], ']']]

    def _make_collapsible_style_top(self, svg, no_arm=False):
        self.svg.expand(self.dx+self.ex, self.ey)
        self.svg.set_no_arm(no_arm)
        self._make_collapsible_top_block(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]]]

    def _make_collapsible_style_bottom(self, svg):
        self.svg.expand(self.dx+self.ex, self.ey)
        self._make_collapsible_bottom_block(svg)
        self.docks = [['flow',True,self.svg.docks[0][0],self.svg.docks[0][1]],
                      ['flow',False,self.svg.docks[1][0],self.svg.docks[1][1]]]

    # Depreciated block styles
    def _make_portfolio_style_2x2(self, svg):
        self.svg.expand(30+self.dx+self.ex, 10+self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True, False, True])        
        self._make_portfolio(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[6][0],
                                      self.svg.docks[6][1]],
                      ['media', False, self.svg.docks[5][0],
                                      self.svg.docks[5][1]],
                      ['media', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['media', False, self.svg.docks[4][0],
                                      self.svg.docks[4][1]],
                      ['media', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]]]

    def _make_portfolio_style_2x1(self, svg):
        self.svg.expand(30+self.dx+self.ex, 10+self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True])        
        self._make_portfolio(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[4][0],
                                      self.svg.docks[4][1]],
                      ['media', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]],
                      ['media', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]]]

    def _make_portfolio_style_1x2(self, svg):
        self.svg.expand(30+self.dx+self.ex, 15+self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True, False, True])
        self.svg.set_draw_innies(False)
        self._make_portfolio(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[4][0],
                                      self.svg.docks[4][1]],
                      ['media', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]],
                      ['media', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_portfolio_style_1x1(self, svg):
        self.svg.expand(30+self.dx+self.ex, 15+self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True])  
        self.svg.set_draw_innies(False)
        self._make_portfolio(svg)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]],
                      ['media', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_basic_block(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.basic_block())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.basic_block())

    def _make_collapsible_top_block(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.sandwich_top())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.sandwich_top())

    def _make_collapsible_bottom_block(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.sandwich_bottom())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.sandwich_bottom())

    def _make_basic_box(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.basic_box())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.basic_box())

    def _make_portfolio(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.portfolio())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.portfolio())

    def _make_basic_flow(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.basic_flow())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.basic_flow())

    def _make_boolean_compare(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.boolean_compare())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.boolean_compare())

    def _make_boolean_and_or(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.boolean_and_or())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.boolean_and_or())

    def _make_boolean_not(self, svg):
        self.shapes[0] = svg_str_to_pixbuf(self.svg.boolean_not())
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        self.shapes[1] = svg_str_to_pixbuf(self.svg.boolean_not())
