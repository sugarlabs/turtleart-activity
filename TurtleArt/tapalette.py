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

palette_names = []
palette_blocks = []
block_colors = []
expandable_blocks = []
block_names = {}
block_primitives = {}
default_values = {}
logo_commands = {}
logo_functions = {}
special_names = {}  # Names for blocks without names for popup help
content_blocks = ['number', 'string', 'description', 'audio', 'video',
                  'journal']
hidden_proto_blocks = [] # proto blocks that are (at least initially) hidden
value_blocks = []  # blocks whose labels are updated get added here
special_block_colors = {}
block_styles = {'basic-style': [],
                'blank-style': [],
                'basic-style-head': [],
                'basic-style-head-1arg': [],
                'basic-style-tail': [],
                'basic-style-extended': [],
                'basic-style-extended-vertical': [],
                'basic-style-1arg': [],
                'basic-style-2arg': [],
                'basic-style-3arg': [],
                'basic-style-var-arg': [],
                'bullet-style': [],
                'invisible': [],
                'box-style': [],
                'box-style-media': [],
                'number-style': [],
                'number-style-var-arg': [],
                'number-style-block': [],
                'number-style-porch': [],
                'number-style-1arg': [],
                'number-style-1strarg': [],
                'compare-style': [],
                'compare-porch-style': [],
                'boolean-style': [],
                'not-style': [],
                'flow-style': [],
                'flow-style-tail': [],
                'flow-style-1arg': [],
                'flow-style-boolean': [],
                'flow-style-while': [],
                'flow-style-else': [],
                'collapsible-top': [],
                'collapsible-top-no-arm': [],
                'collapsible-top-no-label': [],
                'collapsible-top-no-arm-no-label': [],
                'collapsible-bottom': [],
                'portfolio-style-2x2': [],
                'portfolio-style-1x1': [],
                'portfolio-style-2x1': [],
                'portfolio-style-1x2': []}

from taconstants import EXPANDABLE_STYLE
from tautils import debug_output

from gettext import gettext as _

help_strings = {
    'next': _('displays next palette'),
    'orientation': _("changes the orientation of the palette of blocks")
    }


class Palette():
    """ a class for defining new palettes """

    def __init__(self, name, colors=["#00FF00", "#00A000"], position=None):
        self._name = name
        self._special_name = _(name)
        self._colors = colors
        self._help = None

        '''
        self._fd = open('/home/walter/Desktop/turtleblocks/doc/%s-palette.page' % (name), 'a')
        '''

    def add_palette(self, position=None):
        if self._name is None:
            debug_output('You must specify a name for your palette')
            return

        # Insert new palette just before the trash
        if 'trash' in palette_names:
            i = palette_names.index('trash')
        else:
            i = len(palette_names)

        if position is not None and type(position) is int and position < i:
            i = position

        if self._name not in palette_names:
            palette_names.insert(i, self._name)
            palette_blocks.insert(i, [])
            block_colors.insert(i, self._colors)

            '''
            self._fd.write('<page xmlns="http://projectmallard.org/1.0/"\n\
      type="guide"\n\
      id="%s-palette"\n\
      xmlns:its="http://www.w3.org/2005/11/its"\n\
      its:version="1.0">\n\
<info>\n\
  <link type="guide" xref="index"/>\n\
  <link type="topic" xref="palettes"/>\n\
  <its:rules version="1.0">\n\
    <its:translateRule selector="//path | //cmd" translate="no"/>\n\
  </its:rules>\n\
</info>\n\
<title>The %s Palette</title>\n\
<p>\n\
%s\n\
</p>\n\
<terms>\n\
' % (self._name, self._name, self._help))
            '''

        else:
            # debug_output('Palette %s already defined' % (self._name))
            return

        # Special name entry is needed for help hover mechanism
        special_names[self._name] = self._special_name
        if self._help is not None:
            help_strings[self._name] = self._help
        else:
            help_strings[self._name] = ''

    def set_help(self, help):
        self._help = help

    def set_special_name(self, name):
        self._special_name = name

    def add_block(self, block_name, style='basic-block', label=None,
                  special_name=None, default=None, prim_name=None,
                  help_string=None, value_block=False, content_block=False,
                  logo_command=None, hidden=False, colors=None):
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
        if logo_command is not None:
            block.set_logo_command(logo_command)
        if help_string is not None:
            block.set_help(help_string)
        if colors is not None:
            block.set_colors(colors)
        block.set_value_block(value_block)
        block.set_content_block(content_block)
        block.set_palette(self._name)
        if hidden:
            block.set_hidden()
        block.add_block()

        '''
        self._fd.write('  <item>\n\
    <title>%s</title>\n\
    <p>%s</p>\n\
  </item>\n\
' % (block_name, help_string))
        '''

def make_palette(palette_name, colors=None, help_string=None, position=None):
    """ Palette helper function """
    if colors is None:
        palette = Palette(palette_name)
    else:
        palette = Palette(palette_name, colors)
    if help_string is not None:
        palette.set_help(help_string)
    palette.add_palette(position)
    return palette


def palette_name_to_index(palette_name):
    ''' Find the index associated with palette_name. '''
    if palette_name in palette_names:
        return palette_names.index(palette_name)
    else:
        return None


def define_logo_function(key, value):
    ''' Add a logo function to the table (not necessarily associated
    with a block, e.g., color lookup tables) '''
    logo_functions[key] = value    


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
        self._logo_command = None
        self._value_block = False
        self._content_block = False
        self._colors = None
        self._hidden = False

    def add_block(self, position=None):
        if self._name is None:
            debug_output('You must specify a name for your block')
            return

        # FIXME: Does the block already exist? A block can live on
        # multiple palettes, but it can only have one set of
        # atttributes. So if this is a redefinition, remove it from
        # all lists except palettes before regeneration.

        if self._style is None:
            debug_output('You must specify a style for your block')
            return
        else:
            block_styles[self._style].append(self._name)

        if self._label is not None:
            block_names[self._name] = self._label

        if self._palette is not None:
            i = palette_names.index(self._palette)
            if position is not None and type(position) is int and \
                    position < len(palette_blocks[i]):
                palette_blocks[i].insert(position, self._name)
            else:
                palette_blocks[i].append(self._name)
                if position is not None:
                    debug_output('Ignoring position (%s)' % (str(position)))

        if self._help is not None:
            help_strings[self._name] = self._help
        else:
            help_strings[self._name] = ''

        if self._value_block:
            value_blocks.append(self._name)

        if self._content_block:
            content_blocks.append(self._name)

        if self._prim_name is not None:
            block_primitives[self._name] = self._prim_name

        if self._logo_command is not None and self._prim_name is not None:
            logo_commands[self._prim_name] = self._logo_command

        if self._default is not None:
            default_values[self._name] = self._default

        if self._special_name is not None:
            special_names[self._name] = self._special_name

        if self._style in EXPANDABLE_STYLE:
            expandable_blocks.append(self._name)

        if self._colors is not None:
            special_block_colors[self._name] = self._colors

        if self._hidden:
            hidden_proto_blocks.append(self._name)

    def set_hidden(self):
        self._hidden = True

    def set_colors(self, colors=None):
        self._colors = colors

    def set_value_block(self, value=True):
        self._value_block = value

    def set_content_block(self, value=True):
        self._content_block = value

    def set_palette(self, palette):
        if not palette in palette_names:
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
        if style not in block_styles:
            debug_output('Unknown style: %s' % (style))
        else:
            self._style = style

    def set_prim_name(self, prim_name):
        self._prim_name = prim_name

    def set_logo_command(self, logo_command):
        self._logo_command = logo_command
