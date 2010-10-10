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

from gettext import gettext as _

from taconstants import EXPANDABLE, EXPANDABLE_BLOCKS, EXPANDABLE_ARGS, \
    PRIMITIVES, OLD_NAMES, BLOCK_SCALE, BLOCK_NAMES, CONTENT_BLOCKS, \
    PALETTES, COLORS, BASIC_STYLE_HEAD, BASIC_STYLE_HEAD_1ARG, \
    BASIC_STYLE_TAIL, BASIC_STYLE, BASIC_STYLE_EXTENDED, BASIC_STYLE_1ARG, \
    BASIC_STYLE_VAR_ARG, BULLET_STYLE, BASIC_STYLE_2ARG, BOX_STYLE, \
    BOX_STYLE_MEDIA, NUMBER_STYLE, NUMBER_STYLE_VAR_ARG, NUMBER_STYLE_BLOCK, \
    NUMBER_STYLE_PORCH, NUMBER_STYLE_1ARG, NUMBER_STYLE_1STRARG, \
    COMPARE_STYLE, BOOLEAN_STYLE, NOT_STYLE, FLOW_STYLE, FLOW_STYLE_TAIL, \
    FLOW_STYLE_1ARG, FLOW_STYLE_BOOLEAN, FLOW_STYLE_WHILE, FLOW_STYLE_ELSE, \
    COLLAPSIBLE_TOP, COLLAPSIBLE_TOP_NO_ARM, COLLAPSIBLE_TOP_NO_LABEL, \
    COLLAPSIBLE_TOP_NO_ARM_NO_LABEL, COLLAPSIBLE_BOTTOM, PORTFOLIO_STYLE_2x2, \
    PORTFOLIO_STYLE_1x1, PORTFOLIO_STYLE_2x1, PORTFOLIO_STYLE_1x2, \
    STANDARD_STROKE_WIDTH, SELECTED_STROKE_WIDTH, SELECTED_COLOR, BOX_COLORS, \
    BASIC_STYLE_EXTENDED_VERTICAL
from tasprite_factory import SVG, svg_str_to_pixbuf
import sprites

import logging
_logger = logging.getLogger('turtleart-activity')


class Blocks:
    """ A class for the list of blocks and everything they share in common """

    def __init__(self, font_scale_factor=1, decimal_point='.'):
        self.list = []
        self.font_scale_factor = font_scale_factor
        self.decimal_point = decimal_point

    def get_block(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self, block):
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
                b._font_size[i] *= b.scale * scale / self.font_scale_factor
        self.font_scale_factor = scale

    def spr_to_block(self, spr):
        for b in self.list:
            if spr == b.spr:
                return b
        return None

    def get_next_block(self, block):
        if block is None:
            return None
        try:
            i = self.list.index(block)
        except ValueError:
            return None
        i += 1
        if i < len(self.list):
            return self.list[i]
        else:
            return self.list[0]

    def get_next_block_of_same_type(self, block):
        if block is None:
            return None
        type = block.type
        i = 0
        while block is not None:
            block = self.get_next_block(block)
            if block is not None:
                if block.type == type:
                    return block
            if i == len(self.list):
                break
            i += 1
        return None


class Block:
    """ A class for the individual blocks """

    def __init__(self, block_list, sprite_list, name, x, y, type='block',
                 values=[], scale=BLOCK_SCALE, colors=["#FF0000", "#A00000"]):
        self.block_list = block_list
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

        if self.name in OLD_NAMES:
            self.name = OLD_NAMES[self.name]

        for i in range(len(self._font_size)):
            self._font_size[i] *= self.scale * \
                self.block_list.font_scale_factor

        for v in (values):
            self.values.append(v)

        # If there is already a block with the same name, reuse it
        copy_block = None
        if self.name not in EXPANDABLE and \
           self.name not in EXPANDABLE_BLOCKS and \
           self.name not in EXPANDABLE_ARGS and \
           self.name not in ['string', 'sandwichtop', 'sandwichtop_no_label']:
            for b in self.block_list.list:
                if b.scale == self.scale and b.name == self.name:
                    copy_block = b
                    break
        self._new_block_from_factory(sprite_list, x, y, copy_block)

        if name in PRIMITIVES:
            self.primitive = PRIMITIVES[self.name]

        self.block_list.append_to_list(self)

    def highlight(self):
        """ We may want to highlight a block... """
        if self.spr is not None:
            self.spr.set_shape(self.shapes[1])

    def unhighlight(self):
        """ Or unhighlight it. """
        if self.spr is not None:
            self.spr.set_shape(self.shapes[0])

    def resize(self):
        """ We need to resize some blocks on the fly so the labels fit. """
        if self.spr is None:
            return
        dx = (self.spr.label_width() - self.spr.label_safe_width()) / \
            self.scale
        if dx !=0:
            self.dx += dx
            if self.dx < 0:
                self.dx = 0
            self.refresh()

    def set_image(self, image, x, y):
        """ Some blocks get a skin. """
        if self.spr is None:
            return
        self._image = image
        self.spr.set_image(image, 1, x, y)

    def scale_image(self, x, y, w, h):
        """ The skin might need scaling. """
        if self.spr is None:
            return
        if self._image is not None:
            tmp = self._image.scale_simple(w, h, gtk.gdk.INTERP_NEAREST)
            self.spr.set_image(tmp, 1, x, y)

    def rescale(self, scale):
        """ We may want to rescale blocks as well. """
        if self.spr is None:
            return
        for i in range(len(self._font_size)):
            self._font_size[i] /= self.scale
        self.scale = scale
        for i in range(len(self._font_size)):
            self._font_size[i] *= self.scale
        self._set_label_attributes()
        self.svg.set_scale(self.scale)
        self.refresh()
        self.spr.draw()

    def refresh(self):
        if self.spr is None:
            return
        self._make_block(self.svg)
        self._set_margins()
        self.spr.set_shape(self.shapes[0])

    def add_arg(self, keep_expanding=True):
        """ We may want to add additional slots for arguments ("innies"). """
        if self.spr is None:
            return
        h = self.svg.get_height()
        self._ei += 1
        if self.type == 'block' and keep_expanding:
            self.svg.set_show(True)
        else:
            self.svg.set_show(False)
        self.refresh()
        return self.svg.get_height() - h

    def expand_in_y(self, dy):
        """ We may want to grow a block vertically. """
        if self.spr is None:
            return
        self.ey += dy
        if self.type == 'block':
            if self.ey > 0:
                self.svg.set_hide(True)
            else:
                self.svg.set_hide(False)
            self.svg.set_show(True)
        else:
            self.svg.set_hide(False)
            self.svg.set_show(False)
        self.refresh()

    def expand_in_x(self, dx):
        """ We may want to grow a block horizontally. """
        if self.spr is None:
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
        if self.spr is None:
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
        if self.spr is None:
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
        if self.spr is None:
            return(0, 0)
        return (self.ex, self.ey)

    def _new_block_from_factory(self, sprite_list, x, y, copy_block=None):

        self.svg = SVG()
        self.svg.set_scale(self.scale)
        self.svg.set_gradiant(True)
        self.svg.set_innie([False])
        self.svg.set_outie(False)
        self.svg.set_tab(True)
        self.svg.set_slot(True)

        if copy_block is not None:
            self._left = copy_block._left
            self._top = copy_block._top
            self._right = copy_block._right
            self._bottom = copy_block._bottom
            self.dx = copy_block.dx
            self.ex = copy_block.ex
            self.ey = copy_block.ey
            self.width = copy_block.width
            self.height = copy_block.height
            self.shapes[0] = copy_block.shapes[0]
            self.spr = sprites.Sprite(sprite_list, x, y, self.shapes[0])
            self.spr._margins = copy_block.spr._margins[:]
            if len(copy_block.shapes) > 1:
                self.shapes[1] = copy_block.shapes[1]
            self.docks = copy_block.docks[:]
        else:
            if (self.name in EXPANDABLE or \
                self.name in EXPANDABLE_BLOCKS or \
                self.name in EXPANDABLE_ARGS) and \
               self.type == 'block':
                self.svg.set_show(True)

            self._make_block(self.svg)

            if sprite_list is not None:
                self.spr = sprites.Sprite(sprite_list, x, y, self.shapes[0])
                self._set_margins()

        self._set_label_attributes()
        if (self.name == 'number' or self.name == 'string') and \
                len(self.values) > 0:
            for i, v in enumerate(self.values):
                if v is not None:
                    if self.name == 'number':
                        self._set_labels(i,
                           str(v).replace('.', self.block_list.decimal_point))
                    else:
                        self._set_labels(i, str(v))
        elif self.name in BLOCK_NAMES:
            for i, n in enumerate(BLOCK_NAMES[self.name]):
                self._set_labels(i, n)

        if copy_block is None:
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
                self.spr.set_label_attributes(int(self._font_size[1] + 0.5),
                                              True, 'right', 'top', i)
            elif i == 2: # bottom
                self.spr.set_label_attributes(int(self._font_size[1] + 0.5),
                                              True, 'right', 'bottom', i)
            else:
                self.spr.set_label_attributes(int(self._font_size[0] + 0.5),
                                              True, 'center', 'middle', i)

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
            self._make_basic_style(svg, 16, 16)
        elif self.name in BASIC_STYLE_EXTENDED_VERTICAL:
            self._make_basic_style(svg, 0, 4)
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
            self._make_collapsible_style_top(svg, arm=True, label=True)
        elif self.name in COLLAPSIBLE_TOP_NO_ARM:
            self._make_collapsible_style_top(svg, arm=False, label=True)
        elif self.name in COLLAPSIBLE_TOP_NO_LABEL:
            self._make_collapsible_style_top(svg, arm=True, label=False)
        elif self.name in COLLAPSIBLE_TOP_NO_ARM_NO_LABEL:
            self._make_collapsible_style_top(svg, arm=False, label=False)
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
            _logger.debug("WARNING: I don't know how to create a %s block" % \
                              (self.name))

    def _set_colors(self, svg):
        if self.name in BOX_COLORS:
            self.colors = BOX_COLORS[self.name]
        else:
            for p in range(len(PALETTES)):
                if self.name in PALETTES[p]:
                    self.colors = COLORS[p]
        self.svg.set_colors(self.colors)

    def _make_basic_style(self, svg, extend_x=0, extend_y=0):
        self.svg.expand(self.dx + self.ex + extend_x, self.ey + extend_y)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['flow', True, self.svg.docks[0][0],
                       self.svg.docks[0][1]], ['flow',
                       False, self.svg.docks[1][0], self.svg.docks[1][1]]]

    def _make_basic_style_head(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_slot(False)
        self.svg.set_cap(True)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['unavailable', False, 0, 0],
                      ['flow', False, self.svg.docks[0][0],
                                      self.svg.docks[0][1]]]

    def _make_basic_style_head_1arg(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_innie([True])
        self.svg.set_slot(False)
        self.svg.set_cap(True)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['unavailable', False, 0, 0],
                      ['string', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_basic_style_tail(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_tab(False)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_basic_style_1arg(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_innie([True])
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]]]

    def _make_basic_style_2arg(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_innie([True, True])
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['number', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]]]

    def _make_basic_style_var_arg(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        innie = [True]
        for i in range(self._ei):
            innie.append(True)
        self.svg.set_innie(innie)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]]]
        for i in range(self._ei):
            self.docks.append(['number', False, self.svg.docks[i + 2][0],
                                                self.svg.docks[i + 2][1]])
        self.docks.append(['flow', False, self.svg.docks[self._ei + 2][0],
                                      self.svg.docks[self._ei + 2][1]])

    def _make_bullet_style(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        innie = [True, True]
        for i in range(self._ei):
            innie.append(True)
        self.svg.set_innie(innie)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1], '['],
                      ['string', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]]]
        for i in range(self._ei):
            self.docks.append(['string', False, self.svg.docks[i + 3][0],
                                                self.svg.docks[i + 3][1]])
        self.docks.append(['flow', False, self.svg.docks[self._ei + 3][0],
                                      self.svg.docks[self._ei + 3][1], ']'])

    def _make_box_style(self, svg):
        self.svg.expand(60 + self.dx + self.ex, self.ey)
        self._make_block_graphics(svg, self.svg.basic_box)
        self.docks = [['number', True, self.svg.docks[0][0],
                                       self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_media_style(self, svg):
        self.svg.expand(40 + self.dx + self.ex, 10 + self.ey)
        self._make_block_graphics(svg, self.svg.basic_box)
        self.docks = [['number', True, self.svg.docks[0][0],
                                       self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_number_style(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_innie([True, True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_block_graphics(svg, self.svg.basic_block)
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
        self.svg.expand(self.dx + self.ex, self.ey)
        innie = [True]
        for i in range(self._ei + 1):
            innie.append(True)
        self.svg.set_innie(innie)
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['number', True, self.svg.docks[2 + self._ei][0],
                                       self.svg.docks[2 + self._ei][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]]]
        for i in range(self._ei + 1):
            self.docks.append(['number', False, self.svg.docks[i + 1][0],
                                                self.svg.docks[i + 1][1]])
        self.docks.append(['unavailable', False, 0, 0])

    def _make_number_style_block(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_innie([True, True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1], '('],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['unavailable', False, 0, 0, ')']]

    def _make_number_style_1arg(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_innie([True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['number', True, self.svg.docks[1][0],
                                       self.svg.docks[1][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]]]

    def _make_number_style_1strarg(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_innie([True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['number', True, self.svg.docks[1][0],
                                       self.svg.docks[1][1]],
                      ['string', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['unavailable', False, 0, 0]]

    def _make_number_style_porch(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_innie([True, True])
        self.svg.set_outie(True)
        self.svg.set_tab(False)
        self.svg.set_slot(False)
        self.svg.set_porch(True)
        self._make_block_graphics(svg, self.svg.basic_block)
        self.docks = [['number', True, self.svg.docks[2][0],
                                       self.svg.docks[2][1]],
                      ['number', False, self.svg.docks[0][0],
                                        self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]]]

    def _make_compare_style(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self._make_block_graphics(svg, self.svg.boolean_compare)
        self.docks = [['bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1], '('],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['number', False, self.svg.docks[2][0],
                                        self.svg.docks[2][1]],
                      ['unavailable', False, 0, 0, ')']]

    def _make_boolean_style(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self._make_block_graphics(svg, self.svg.boolean_and_or)
        self.docks = [['bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['bool', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]]]

    def _make_not_style(self, svg):
        self.svg.expand(15 + self.dx + self.ex, self.ey)
        self._make_block_graphics(svg, self.svg.boolean_not)
        self.docks = [['bool', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_flow_style(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self._make_block_graphics(svg, self.svg.basic_flow)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1], '['],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], ']']]

    def _make_flow_style_tail(self, svg):
        self.svg.expand(10 + self.dx + self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(False)
        self._make_block_graphics(svg, self.svg.basic_flow)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_flow_style_1arg(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True])
        self._make_block_graphics(svg, self.svg.basic_flow)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['number', False, self.svg.docks[1][0],
                                        self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], '['],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']']]

    def _make_flow_style_boolean(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_boolean(True)
        self._make_block_graphics(svg, self.svg.basic_flow)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], '['],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']']]

    def _make_flow_style_while(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_boolean(True)
        self._make_block_graphics(svg, self.svg.basic_flow)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['bool', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1], '['],
                      ['flow', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1], ']['],
                      ['flow', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1], ']']]

    def _make_flow_style_else(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_else(True)
        self.svg.set_boolean(True)
        self._make_block_graphics(svg, self.svg.basic_flow)
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

    def _make_collapsible_style_top(self, svg, arm=True, label=True):
        self.svg.expand(self.dx + self.ex, self.ey)
        self.svg.set_arm(arm)
        self._make_block_graphics(svg, self.svg.sandwich_top, label)
        if label:
            self.docks = [['flow', True, self.svg.docks[0][0],
                           self.svg.docks[0][1]],
                          ['number', False, self.svg.docks[1][0],
                           self.svg.docks[1][1]],
                          ['flow', False, self.svg.docks[2][0],
                           self.svg.docks[2][1]]]
        else:
            self.docks = [['flow', True, self.svg.docks[0][0],
                           self.svg.docks[0][1]],
                          ['flow', False, self.svg.docks[1][0],
                           self.svg.docks[1][1]]]

    def _make_collapsible_style_bottom(self, svg):
        self.svg.expand(self.dx + self.ex, self.ey)
        self._make_block_graphics(svg, self.svg.sandwich_bottom)
        self.docks = [['flow', True, self.svg.docks[0][0],
                       self.svg.docks[0][1]], ['flow', False,
                       self.svg.docks[1][0], self.svg.docks[1][1]]]

    # Depreciated block styles

    def _make_portfolio_style_2x2(self, svg):
        self.svg.expand(30 + self.dx + self.ex, 10 + self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True, False, True])
        self._make_block_graphics(svg, self.svg.portfolio)
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
        self.svg.expand(30 + self.dx + self.ex, 10 + self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True])
        self._make_block_graphics(svg, self.svg.portfolio)
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
        self.svg.expand(30 + self.dx + self.ex, 15 + self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True, False, True])
        self.svg.set_draw_innies(False)
        self._make_block_graphics(svg, self.svg.portfolio)
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
        self.svg.expand(30 + self.dx + self.ex, 15 + self.ey)
        self.svg.set_slot(True)
        self.svg.set_tab(True)
        self.svg.set_innie([True, True])
        self.svg.set_draw_innies(False)
        self._make_block_graphics(svg, self.svg.portfolio)
        self.docks = [['flow', True, self.svg.docks[0][0],
                                     self.svg.docks[0][1]],
                      ['string', False, self.svg.docks[3][0],
                                      self.svg.docks[3][1]],
                      ['media', False, self.svg.docks[2][0],
                                      self.svg.docks[2][1]],
                      ['flow', False, self.svg.docks[1][0],
                                      self.svg.docks[1][1]]]

    def _make_block_graphics(self, svg, function, arg=None):
        if arg is None:
            self.shapes[0] = svg_str_to_pixbuf(function())
        else:
            self.shapes[0] = svg_str_to_pixbuf(function(arg))
        self.width = self.svg.get_width()
        self.height = self.svg.get_height()
        self.svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        self.svg.set_stroke_color(SELECTED_COLOR)
        if arg is None:
            self.shapes[1] = svg_str_to_pixbuf(function())
        else:
            self.shapes[1] = svg_str_to_pixbuf(function(arg))
