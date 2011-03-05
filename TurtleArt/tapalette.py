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

from taconstants import BLOCK_STYLES, BLOCK_NAMES, HELP_STRINGS, PALETTES, \
    PALETTE_NAMES, CONTENT_BLOCKS, PRIMITIVES, DEFAULTS, SPECIAL_NAMES, \
    COLORS, EXPANDABLE_STYLE, EXPANDABLE_BLOCKS
from talogo import VALUE_BLOCKS
from tautils import debug_output


class Palette():
    """ a class for defining new palettes """

    def __init__(self, name, colors=["#00FF00", "#00A000"], position=None):
        self._name = name
        self._special_name = name
        self._colors = colors
        self._help = None

    def add_palette(self, position=None):
        if self._name is None:
            debug_output('You must specify a name for your palette')
            return

        # Insert new palette just before the trash
        if 'trash' in PALETTE_NAMES:
            i = PALETTE_NAMES.index('trash')
        else:
            i = len(PALETTE_NAMES)

        if position is not None and type(position) is int and position < i:
            i = position

        if self._name not in PALETTE_NAMES:
            PALETTE_NAMES.insert(i, self._name)
            PALETTES.insert(i, [])
            COLORS.insert(i, self._colors)
        else:
            # debug_output('Palette %s already defined' % (self._name))
            return

        # Special name entry is needed for help hover mechanism
        SPECIAL_NAMES[self._name] = self._special_name
        if self._help is not None:
            HELP_STRINGS[self._name] = self._help
        else:
            HELP_STRINGS[self._name] = ''

    def set_help(self, help):
        self._help = help

    def set_special_name(self, name):
        self._special_name = name

    def add_block(self, block_name, style='basic-block', label=None,
                  special_name=None, default=None, prim_name=None,
                  help_string=None, value_block=False, content_block=False,
                  hidden=False):
        """ Add a new block to the palette """
        block = Block(block_name)
        block.set_style(style)
        if label is not None:
            block.set_label(label)
        if special_name is not None:
            block.set_special_name(special_name)
        if default is not None:
            if default == 'None':
                block.set_default(None)
            else:
                block.set_default(default)
        if prim_name is not None:
            block.set_prim_name(prim_name)
        if help_string is not None:
            block.set_help(help_string)
        block.set_value_block(value_block)
        block.set_content_block(content_block)
        if not hidden:
            block.set_palette(self._name)
        block.add_block()


def make_palette(palette_name, colors=None, help_string=None):
    """ Palette helper function """
    if colors is None:
        palette = Palette(palette_name)
    else:
        palette = Palette(palette_name, colors)
    if help_string is not None:
        palette.set_help(help_string)
    palette.add_palette()
    return palette


class Block():
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

    def add_block(self, position=None):
        if self._name is None:
            debug_output('You must specify a name for your block')
            return

        if self._style is None:
            debug_output('You must specify a style for your block')
            return
        else:
            BLOCK_STYLES[self._style].append(self._name)

        if self._label is not None:
            BLOCK_NAMES[self._name] = self._label

        if self._palette is not None:
            i = PALETTE_NAMES.index(self._palette)
            if position is not None and type(position) is int and \
                    position < len(PALETTES[i]):
                PALETTES[i].insert(position, self._name)
            else:
                PALETTES[i].append(self._name)
                if position is not None:
                    debug_output('Ignoring position (%s)' % (str(position)))

        if self._help is not None:
            HELP_STRINGS[self._name] = self._help
        else:
            HELP_STRINGS[self._name] = ''

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

        if self._style in EXPANDABLE_STYLE:
            EXPANDABLE_BLOCKS.append(self._name)

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
        if style not in BLOCK_STYLES:
            debug_output('Unknown style: %s' % (style))
        else:
            self._style = style

    def set_prim_name(self, prim_name):
        self._prim_name = prim_name
