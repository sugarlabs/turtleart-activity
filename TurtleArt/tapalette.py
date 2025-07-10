#!/usr/bin/env python3
# Copyright (c) 2011-13 Walter Bender

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

help_palettes = {}
help_windows = {}
palette_names = []
palettes = {}
palette_i18n_names = []
palette_init_on_start = []
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
hidden_proto_blocks = []  # proto blocks that are (at least initially) hidden
value_blocks = []  # blocks whose labels are updated get added here
special_block_colors = {}
string_or_number_args = []
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
                'basic-style-7arg': [],
                'basic-style-var-arg': [],
                'bullet-style': [],
                'box-style': [],
                'box-style-media': [],
                'number-style': [],
                'number-style-var-arg': [],
                'number-style-var-3arg': [],
                'number-style-block': [],
                'number-style-porch': [],
                'number-style-1arg': [],
                'number-style-1strarg': [],
                'compare-style': [],
                'compare-porch-style': [],
                'boolean-style': [],
                'not-style': [],
                'boolean-block-style': [],
                'boolean-1arg-block-style': [],
                'flow-style-tail': [],
                'clamp-style': [],
                'clamp-style-collapsible': [],
                'clamp-style-collapsed': [],
                'clamp-style-1arg': [],
                'clamp-style-hat-1arg': [],
                'clamp-style-hat': [],
                'clamp-style-boolean': [],
                'clamp-style-until': [],
                'clamp-style-else': [],
                'portfolio-style-2x2': [],
                'portfolio-style-1x1': [],
                'portfolio-style-2x1': [],
                'portfolio-style-1x2': []}


from gi.repository import Gtk
from gi.repository import Gdk

try:
    from sugar3.graphics import style
    from .util.helpbutton import (add_section, add_paragraph)
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
    HELP_PALETTE = True
except ImportError:
    GRID_CELL_SIZE = 55
    HELP_PALETTE = False

from .taconstants import (EXPANDABLE_STYLE, EXPANDABLE_FLOW)

from gettext import gettext as _

help_strings = {
    'next': _('displays next palette'),
    'orientation': _("changes the orientation of the palette of blocks")}


class Palette():

    """ a class for defining new palettes """

    def __init__(self, name, colors=["#00FF00", "#00A000"], position=None):
        self._name = name
        self._special_name = _(name)
        self._colors = colors
        self._max_text_width = int(Gdk.Screen.width() / 3) - 20

        # Prepare a vbox for the help palette
        if self._name not in help_palettes:
            self._help_box = Gtk.VBox()
            self._help_box.set_homogeneous(False)
            help_palettes[self._name] = self._help_box
            help_windows[self._name] = Gtk.ScrolledWindow()
            help_windows[self._name].set_size_request(
                int(Gdk.Screen.width() / 3),
                Gdk.Screen.height() - GRID_CELL_SIZE * 3)
            help_windows[self._name].set_policy(
                Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            help_windows[self._name].add_with_viewport(
                help_palettes[self._name])
            help_palettes[self._name].show()
            self._help = None
        else:
            self._help_box = help_palettes[self._name]
            self._help = 'deja vu'

    def add_palette(self, position=None, init_on_start=False):
        if self._name is None:
            print('You must specify a name for your palette')
            return

        # Insert new palette just before the trash
        if 'trash' in palette_names:
            i = palette_names.index('trash')
        elif _('trash') in palette_i18n_names:
            i = palette_i18n_names.index(_('trash'))
        else:
            i = len(palette_names)

        if position is not None and isinstance(position, int) and position < i:
            i = position

        if self._name not in palette_names:
            palettes[self._name] = self
            palette_names.insert(i, self._name)
            palette_i18n_names.insert(i, _(self._name))
            palette_blocks.insert(i, [])
            block_colors.insert(i, self._colors)
            if init_on_start:
                if self._name not in palette_init_on_start:
                    palette_init_on_start.append(self._name)
        else:
            return

        # Special name entry is needed for help hover mechanism
        special_names[self._name] = self._special_name
        if self._help is not None:
            help_strings[self._name] = self._help
        else:
            help_strings[self._name] = ''

    def set_help(self, help):
        if self._help is None:
            self._help = help
            if hasattr(self, '_help_box') and HELP_PALETTE:
                add_section(self._help_box, self._help,
                            icon=self._name + 'off')

    def set_special_name(self, name):
        self._special_name = name

    def add_block(self, block_name, style='basic-block', label=None,
                  special_name=None, default=None, prim_name=None,
                  help_string=None, value_block=False, content_block=False,
                  logo_command=None, hidden=False, colors=None,
                  string_or_number=False, before=None, after=None,
                  private=None):
        """ Add a new block to the palette """
        block = _ProtoBlock(block_name)
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
            if not hidden:
                first_arg = None
                if special_name is None:
                    if isinstance(label, list):
                        first_arg = label[0]
                    else:
                        first_arg = label
                else:
                    first_arg = special_name
                if HELP_PALETTE:
                    if first_arg is None or \
                            first_arg == '' or \
                            first_arg == ' ':
                        add_paragraph(self._help_box, '%s' % (help_string))
                    else:
                        add_paragraph(self._help_box, '%s: %s' % (first_arg,
                                                                  help_string))
        if colors is not None:
            block.set_colors(colors)
        if string_or_number:
            block.set_string_or_number()
        if before is not None:
            block.before = before
        if after is not None:
            block.after = after
        if private is not None:
            block.private = private
        block.set_value_block(value_block)
        block.set_content_block(content_block)
        block.set_palette(self._name)
        if hidden:
            block.set_hidden()
        block.add_block()


def make_palette(palette_name, colors=None, help_string=None, position=None,
                 init_on_start=False, translation=None):
    """ Palette helper function """
    if palette_name in palettes:
        return palettes[palette_name]
    else:
        if colors is None:
            palette = Palette(palette_name)
        else:
            palette = Palette(palette_name, colors)
        if help_string is not None:
            palette.set_help(help_string)
        palette.add_palette(position, init_on_start=init_on_start)
        return palette


def palette_name_to_index(palette_name):
    ''' Find the index associated with palette_name. '''
    if palette_name in palette_names:
        return palette_names.index(palette_name)
    elif palette_name in palette_i18n_names:
        return palette_i18n_names.index(palette_name)
    else:
        return None


def define_logo_function(key, value):
    ''' Add a logo function to the table (not necessarily associated
    with a block, e.g., color lookup tables) '''
    logo_functions[key] = value


class _ProtoBlock():

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
        self._string_or_number = False

    def add_block(self, position=None):
        if self._name is None:
            print('You must specify a name for your block')
            return

        # FIXME: Does the block already exist? A block can live on
        # multiple palettes, but it can only have one set of
        # atttributes. So if this is a redefinition, remove it from
        # all lists except palettes before regeneration.

        if self._style is None:
            print('You must specify a style for your block')
            return
        else:
            block_styles[self._style].append(self._name)
        if self._style in ['clamp-style',
                           'clamp-style-hat-1arg',
                           'clamp-style-hat',
                           'clamp-style-collapsible',
                           'clamp-style-1arg',
                           'clamp-style-boolean',
                           'clamp-style-until',
                           'clamp-style-else']:
            EXPANDABLE_FLOW.append(self._name)

        if self._label is not None:
            block_names[self._name] = self._label

        if self._palette is not None:
            i = palette_names.index(self._palette)
            if self._name in palette_blocks[i]:
                print('%s already in palette %s, skipping...' %
                      (self._name, self._palette))
            else:
                if position is not None and isinstance(position, int) and \
                        position < len(palette_blocks[i]):
                    palette_blocks[i].insert(position, self._name)
                else:
                    palette_blocks[i].append(self._name)
                    if position is not None:
                        print('Ignoring position (%s)' % (str(position)))

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

        if self._string_or_number:
            string_or_number_args.append(self._name)

        if self._hidden:
            hidden_proto_blocks.append(self._name)

    def set_hidden(self):
        self._hidden = True

    def set_colors(self, colors=None):
        self._colors = colors

    def set_string_or_number(self, flag=True):
        self._string_or_number = flag

    def set_value_block(self, value=True):
        self._value_block = value

    def set_content_block(self, value=True):
        self._content_block = value

    def set_palette(self, palette):
        if palette not in palette_names:
            print('Could not find palette %s' % (palette))
        else:
            self._palette = palette

    def set_help(self, help):
        self._help = help

    def set_special_name(self, name):
        self._special_name = name

    def set_label(self, label):
        if isinstance(label, list):
            self._label = label[:]
        else:
            self._label = [label]

    def set_default(self, default):
        if isinstance(default, list):
            self._default = default[:]
        else:
            self._default = [default]

    def set_style(self, style):
        if style not in block_styles:
            print('Unknown style: %s' % (style))
        else:
            self._style = style

    def set_prim_name(self, prim_name):
        self._prim_name = prim_name

    def set_logo_command(self, logo_command):
        self._logo_command = logo_command
