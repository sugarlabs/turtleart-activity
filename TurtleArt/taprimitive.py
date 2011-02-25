#!/usr/bin/env python
#Copyright (c) 2011 Walter Bender

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
    STANDARD_STROKE_WIDTH, BOX_COLORS, GRADIENT_COLOR, COMPARE_PORCH_STYLE, \
    BASIC_STYLE_EXTENDED_VERTICAL, CONSTANTS, INVISIBLE, PALETTE_NAMES, \
    HELP_STRINGS, DEFAULTS, SPECIAL_NAMES

from talogo import VALUE_BLOCKS
from tautils import debug_output


class Primitive():
    """ a class for defining new block primitives """

    def __init__(self, name):
        self._name = name
        self._special_name = None
        self._palette = None
        self._style = None
        self._label = None
        self._default = None
        self._help = None
        self._prim_name = None
        self._value_block = False
        self._content_block = False

    def add_prim(self):
        if self._name is None:
            debug_output('You must specify a name for your block')
            return

        if self._style is None:
            debug_output('You must specify a style for your block')
            return
        else:
            self._style.append(self._name)

        if self._label is not None:
            BLOCK_NAMES[self._name] = self._label

        if self._palette is not None:
            PALETTES[PALETTE_NAMES.index(self._palette)].append(self._name)

        if self._help is not None:
            HELP_STRINGS[self._name] = self._help

        if self._value_block:
            VALUE_BLOCKS.append(self._name)

        if self._content_block:
            CONTENT_BLOCKS.append(self._name)

        if self._prim_name is not None:
            PRIMITIVES[self._name] = self._prim_name

        if self._default is not None:
            DEFAULTS[self._name] = self._default

        if self._special_name is not None:
            SPECIAL_NAMES[self._name] = self._special_name

    def set_value_block(self, value=True):
        self._value_block = value

    def set_content_block(self, value=True):
        self._content_block = value

    def set_palette(self, palette):
        if not palette in PALETTE_NAMES:
            debug_output('Could not find palette %s' % (palette))
        else:
            self._palette = palette

    def set_help(self, help):
        self._help = help

    def set_special_name(self, name):
        self._special_name = name

    def set_label(self, label):
        if type(label) == type([]):
            self._label = label[:]
        else:
            self._label = [label]

    def set_default(self, default):
        if type(default) == type([]):
            self._default = default[:]
        else:
            self._default = [default]

    def set_style(self, style):
        self._style = style

    def set_prim_name(self, prim_name):
        self._prim_name = prim_name

