# -*- coding: utf-8 -*-
# Copyright (c) 2010-14 Walter Bender

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

import os
import tempfile
from random import uniform
from gettext import gettext as _

# Packaging constants
SUFFIX = ('.ta', '.tb')
MAGICNUMBER = 'TB'
MIMETYPE = ['application/x-turtle-art', 'application/vnd.turtleblocks']

# Sprite layers
OVERLAY_LAYER = 400
TURTLE_LAYER = 500
BLOCK_LAYER = 600
CATEGORY_LAYER = 700
TAB_LAYER = 800
PROTO_LAYER = 801
STATUS_LAYER = 900
TOP_LAYER = 1000

# Special-case some block colors
BOX_COLORS = {'red': ["#FF0000", "#A00000"],
              'orange': ["#FFD000", "#AA8000"],
              'yellow': ["#FFFF00", "#A0A000"],
              'blue': ["#0000FF", "#000080"],
              'cyan': ["#00FFFF", "#00A0A0"],
              'green': ["#00FF00", "#008000"],
              'purple': ["#FF00FF", "#A000A0"],
              'white': ["#FFFFFF", "#A0A0A0"],
              'black': ["#000000", "#000000"]}

# Misc. parameters
PALETTE_HEIGHT = 120
PALETTE_WIDTH = 175
SELECTOR_WIDTH = 55
ICON_SIZE = 55
GRADIENT_COLOR = "#FFFFFF"
STANDARD_STROKE_WIDTH = 1.0
BLOCK_SCALE = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
PALETTE_SCALE = 1.5
DEFAULT_TURTLE = 'Yertle'
DEFAULT_TURTLE_COLORS = ['#008000', '#00A000']
PALETTE_COLOR = "#FFD000"
TOOLBAR_COLOR = "#282828"
HORIZONTAL_PALETTE = 0
VERTICAL_PALETTE = 1
BLACK = -9999
WHITE = -9998
HIT_HIDE = 240
HIT_SHOW = 224
HIT_RED = "#F00000"
HIT_GREEN = "#00E000"
HIDE_WHITE = "#F0F0F0"
SHOW_WHITE = "#E0E0E0"
DEFAULT_SCALE = 33
DEFAULT_PEN_COLOR = [255, 0, 0]
DEFAULT_BACKGROUND_COLOR = [153, 204, 255]
DEFAULT_BACKGROUND_COLOR_SHADE_GRAY = [60, 80, 100]
DEFAULT_FONT = 'Sans'
XO1 = 'xo1'
XO15 = 'xo1.5'
XO175 = 'xo1.75'
XO30 = 'xo3.0'
XO4 = 'xo4'
UNKNOWN = 'unknown'
PASTE_OFFSET = 20
TMP_SVG_PATH = os.path.join(
    tempfile.gettempdir(), 'turtle-blocks-%d.svg' % int(uniform(0, 10000)))
TMP_ODP_PATH = os.path.join(
    tempfile.gettempdir(), 'turtle-blocks-%d.odp' % int(uniform(0, 10000)))

ARG_MUST_BE_NUMBER = ['product2', 'minus2', 'random', 'remainder2', 'forward',
                      'back', 'left', 'right', 'arc', 'setxy2', 'setxy',
                      'fillscreen', 'setscale', 'setpensize', 'wait',
                      'setcolor', 'seth', 'setgray', 'setshade', 'string',
                      'fillscreen2']

KEY_DICT = {
    'Left': 1,
    'KP_Left': 1,
    'Up': 2,
    'KP_Up': 2,
    'Right': 3,
    'KP_Right': 3,
    'Down': 4,
    'KP_Down': 4,
    'BackSpace': 8,
    'Tab': 9,
    'Return': 13,
    'Escape': 27,
    'space': 32,
    ' ': 32,
    'exclam': 33,
    'quotedbl': 34,
    'numbersign': 35,
    'dollar': 36,
    'percent': 37,
    'ampersand': 38,
    'apostrophe': 39,
    'parenleft': 40,
    'parenright': 41,
    'asterisk': 42,
    'plus': 43,
    'comma': 44,
    'minus': 45,
    'period': 46,
    'slash': 47,
    'colon': 58,
    'semicolon': 59,
    'less': 60,
    'equal': 61,
    'greater': 62,
    'question': 63,
    'at': 64,
    'underscore': 95,
    'bracketleft': 91,
    'backslash': 92,
    'bracketright': 93,
    'asciicircum': 94,
    'grave': 96,
    'braceleft': 123,
    'bar': 124,
    'braceright': 125,
    'asciitilde': 126,
    'Delete': 127,
}
REVERSE_KEY_DICT = {
    1: _('left'),
    2: _('up'),
    3: _('right'),
    4: _('down'),
    8: _('backspace'),
    9: _('tab'),
    # TRANS: enter is the name of the enter (or return) key
    13: _('enter'),
    27: 'esc',
    # TRANS: space is the name of the space key
    32: _('space'),
    127: _('delete')
}


class ColorObj(object):

    def __init__(self, color):
        self.color = color

    def __int__(self):
        if hasattr(self.color, 'color'):
            if self.color.color is None:
                return int(self.color.shade)
            else:
                return int(self.color.color)
        else:
            return int(self.color)

    def __float__(self):
        if hasattr(self.color, 'color'):
            return float(int(self))
        else:
            return float(self.color)

    def __str__(self):
        if isinstance(self.color, (float, int, bool)):
            return str(self.color)
        return str(self.color.name)

    def __repr__(self):
        if isinstance(self.color, (float, int, bool)):
            return str(self.color)
        return str(self.color.name)


class Color(object):

    """ A color used in block programs (e.g., as pen color). """

    def __init__(self, name, color=0, shade=50, gray=100):
        """ name -- a string with the name of the color, e.g., 'red'
        color -- the hue (0-100, or None for white, gray, and black)
        shade -- the lightness (0 is black, 100 is white)
        gray -- the saturation (0 is gray, 100 is fully saturated) """
        self.name = name
        self.color = color
        self.shade = shade
        self.gray = gray

    def __int__(self):
        if self.color is None:
            return int(self.shade)
        else:
            return int(self.color)

    def __float__(self):
        return float(int(self))

    def get_number_string(self):
        return str(int(self))

    def get_number_name(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return '%s (%s/%d/%d)' % (str(self.name), str(self.color),
                                  self.shade, self.gray)

    def __eq__(self, other):
        """ A Color is equivalent to
        * another Color with the same color, shade, and gray values
        * an integer, float, or long that equals int(self) """
        if isinstance(other, Color):
            return self.color == other.color and \
                self.shade == other.shade and \
                self.gray == other.gray
        elif isinstance(other, (int, float)):
            return int(self) == other
        # * a basestring that equals str(self)
        # elif isinstance(other, basestring):
        #    return str(self) == other
        else:
            return False

    def __lt__(self, other):
        """ A Color is less than
        * another Color whose name appears earlier in the alphabet
        * a number that is less than int(self)
        * a string that appears before the underscore in the ASCII table """
        if isinstance(other, Color):
            return str(self) < str(other)
        elif isinstance(other, (int, float)):
            return int(self) < other
        elif isinstance(other, str):
            return '_' + str(self) < other
        else:
            return False

    def __gt__(self, other):
        """ A Color is greater than
        * another Color whose name appears later in the alphabet
        * a number that is greater than int(self)
        * a string that appears after the underscore in the ASCII table """
        if isinstance(other, Color):
            return str(self) > str(other)
        elif isinstance(other, (int, float)):
            return int(self) > other
        elif isinstance(other, str):
            return '_' + str(self) > other
        else:
            return False

    def is_gray(self):
        """ Return True iff this color is white, gray, or black, i.e. if its
        hue is not set or its saturation is zero. """
        return self.color is None or not self.gray


class Vector(object):

    """ A vector object used in block programs (e.g., as food object). """

    def __init__(self, name, vector):
        """ name -- a string with the name of the vector, e.g., 'banana'
        vector -- a list of values, e.g., [105, 1, 27, 3, 0] """
        self.name = name
        self.vector = vector

    '''
    def __int__(self):
        return 0

    def __float__(self):
        return 0.0
    '''

    def __str__(self):
        return self.get_vector_string()

    def get_vector_string(self):
        string = '%s [' % str(self.name)
        for s in self.vector:
            string += '%d' % s
            if self.vector.index(s) < len(self.vector) - 1:
                string += ', '
        string += ']'
        return string

    def __eq__(self, other):
        """ A Vector is equivalent to
        * another Vector with the same vector values """
        if isinstance(other, Vector):
            return self.vector == other.vector
        else:
            return False

    def __lt__(self, other):
        """ A Vector is less than
        * another Vector whose name appears earlier in the alphabet
        * a number that is less than int(self)
        * a string that appears before the underscore in the ASCII table """
        if isinstance(other, Vector):
            return str(self.vector) < str(other.vector)
        else:
            return False

    def __gt__(self, other):
        """ A Vector is greater than
        * another Vector whose name appears later in the alphabet
        * a number that is greater than int(self)
        * a string that appears after the underscore in the ASCII table """
        if isinstance(other, Vector):
            return str(self.vector) > str(other.vector)
        else:
            return False


CONSTANTS = {'leftpos': None, 'toppos': None, 'rightpos': None,
             'bottompos': None, 'width': None, 'height': None,
             'black': Color('black', None, 0, 0),
             'white': Color('white', None, 100, 0),
             'red': Color('red', 0, 50, 100),
             'orange': Color('orange', 10, 50, 100),
             'yellow': Color('yellow', 20, 50, 100),
             'green': Color('green', 40, 50, 100),
             'cyan': Color('cyan', 50, 50, 100),
             'blue': Color('blue', 70, 50, 100),
             'purple': Color('purple', 90, 50, 100),
             'titlex': None, 'titley': None, 'leftx': None,
             'topy': None, 'rightx': None, 'bottomy': None}

# Blocks that are expandable
EXPANDABLE_STYLE = ['boolean-style', 'compare-porch-style', 'compare-style',
                    'number-style-porch', 'number-style', 'basic-style-2arg',
                    'basic-style-3arg', 'number-style-block',
                    'box-style-media']

# These are defined in add_block based on block style
EXPANDABLE_FLOW = []

EXPANDABLE = ['vspace', 'hspace', 'identity2']

EXPANDABLE_ARGS = ['bulletlist', 'myfunc1arg', 'myfunc2arg', 'myfunc3arg',
                   'userdefined', 'userdefined2args', 'userdefined3args',
                   'loadblock', 'loadblock2arg', 'loadblock3arg']

# Deprecated block styles that need dock adjustments
OLD_DOCK = ['and', 'or', 'plus', 'minus', 'division', 'product', 'remainder']

CONTENT_ARGS = ['show', 'showaligned', 'push', 'storein', 'storeinbox1',
                'storeinbox2']

MEDIA_BLOCK2TYPE = {}  # map media blocks to media types


BLOCKS_WITH_SKIN = []  # These blocks get a special skin

PYTHON_SKIN = []

SKIN_PATHS = ['images']

MEDIA_SHAPES = []

NO_IMPORT = []

EXPAND_SKIN = {}

# Status blocks
OVERLAY_SHAPES = ['Cartesian', 'Cartesian_labeled', 'polar', 'metric']

STATUS_SHAPES = ['status', 'info', 'nostack', 'dupstack', 'noinput',
                 'emptyheap', 'emptybox', 'nomedia', 'nocode', 'overflowerror',
                 'negroot', 'syntaxerror', 'nofile', 'nojournal', 'zerodivide',
                 'notanumber', 'incompatible', 'help', 'print', 'noconnection',
                 'emptystart']

# Emulate Sugar toolbar when running from outside of Sugar
TOOLBAR_SHAPES = ['hideshowoff', 'eraseron', 'run-fastoff',
                  'run-slowoff', 'stopiton']

# Legacy names
OLD_NAMES = {'product': 'product2', 'storeinbox': 'storein', 'minus': 'minus2',
             'division': 'division2', 'plus': 'plus2', 'and': 'and2',
             'or': 'or2', 'less': 'less2', 'greater': 'greater2',
             'equal': 'equal2', 'remainder': 'remainder2',
             'identity': 'identity2', 'division': 'division2',
             'audiooff': 'audio', 'endfill': 'stopfill',
             'descriptionoff': 'description', 'template3': 'templatelist',
             'template1': 'template1x1', 'template2': 'template2x1',
             'template6': 'template1x2', 'template7': 'template2x2',
             'template4': 'template1x1a', 'hres': 'width', 'vres': 'height',
             'sandwichtop2': 'sandwichtop', 'image': 'show',
             'container': 'indentity2', 'insertimage': 'show'}

# Define the relative size and postion of media objects
#                    (w, h, x, y, dx, dy)
#
TITLEXY = (0.9375, 0.875)

# Relative placement of portfolio objects (used by deprecated blocks)
TEMPLATES = {'t1x1': (0.5, 0.5, 0.0625, 0.125, 1.05, 0),
             't2z1': (0.5, 0.5, 0.0625, 0.125, 1.05, 1.05),
             't1x2': (0.45, 0.45, 0.0625, 0.125, 1.05, 1.05),
             't2x2': (0.45, 0.45, 0.0625, 0.125, 1.05, 1.05),
             't1x1a': (0.9, 0.9, 0.0625, 0.125, 0, 0),
             'bullet': (1, 1, 0.0625, 0.125, 0, 0.1),
             'insertimage': (0.333, 0.333)}

RETURN = '⏎'

VOICES = {'af': 'afrikaans', 'cy': 'welsh-test', 'el': 'greek',
          'es': 'spanish', 'hi': 'hindi-test', 'hy': 'armenian',
          'ku': 'kurdish', 'mk': 'macedonian-test', 'pt': 'brazil',
          'sk': 'slovak', 'sw': 'swahili', 'bs': 'bosnian',
          'da': 'danish', 'en': 'english', 'fi': 'finnish',
          'hr': 'croatian', 'id': 'indonesian-test', 'la': 'latin',
          'nl': 'dutch-test', 'sq': 'albanian', 'ta': 'tamil',
          'vi': 'vietnam-test', 'ca': 'catalan', 'de': 'german',
          'eo': 'esperanto', 'fr': 'french', 'hu': 'hungarian',
          'is': 'icelandic-test', 'lv': 'latvian', 'no': 'norwegian',
          'ro': 'romanian', 'sr': 'serbian', 'zh': 'Mandarin',
          'cs': 'czech', 'it': 'italian', 'pl': 'polish',
          'ru': 'russian_test', 'sv': 'swedish', 'tr': 'turkish'}

# Macros (groups of blocks)
MACROS = {
    'ifthenelse':  # Because it is too big to fit on the palette
    [[0, 'ifelse', 0, 0, [None, None, None, None, None]]],
    'indexblock':
    [[0, 'index', 0, 0, [None, 1, 2, 3]],
     [1, ['string', _('text')], 0, 0, [0, None]],
     [2, ['number', 0], 0, 0, [0, None]],
     [3, ['number', 1], 0, 0, [0, None]]],
    'kbinput':
    [[0, 'until', 0, 0, [None, 1, 4, None]],
     [1, 'greater2', 0, 0, [0, 2, 3, None]],
     [2, 'keyboard', 0, 0, [1, None]],
     [3, ['number', '0'], 0, 0, [1, None]],
     [4, 'wait', 0, 0, [0, 5, 6]],
     [5, ['number', '0.1'], 0, 0, [4, None]],
     [6, 'kbinput', 0, 0, [4, None]]],
    'list':
    [[0, ['sandwichclamp', 252], 0, 0, [None, 1, None]],
     [1, 'penup', 0, 0, [0, 2]],
     [2, 'setxy2', 0, 0, [1, 3, 4, 5]],
     [3, 'titlex', 0, 0, [2, None]],
     [4, 'titley', 0, 0, [2, None]],
     [5, 'pendown', 0, 0, [2, 6]],
     [6, 'setscale', 0, 0, [5, 7, 8]],
     [7, ['number', '100'], 0, 0, [6, None]],
     [8, 'show', 0, 0, [6, 9, 10]],
     [9, ['string', _('Title')], 0, 0, [8, None]],
     [10, 'penup', 0, 0, [8, 11]],
     [11, 'setxy2', 0, 0, [10, 12, 13, 14]],
     [12, 'leftx', 0, 0, [11, None]],
     [13, 'topy', 0, 0, [11, None]],
     [14, 'pendown', 0, 0, [11, 15]],
     [15, 'setscale', 0, 0, [14, 16, 17]],
     [16, ['number', '67'], 0, 0, [15, None]],
     [17, 'bulletlist', 0, 0, [15, 18, 19, None]],
     [18, ['string', '∙ '], 0, 0, [17, None]],
     [19, ['string', '∙ '], 0, 0, [17, None]]],
    '1x1a':
    [[0, ['sandwichclamp', 231], 0, 0, [None, 1, None]],
     [1, 'penup', 0, 0, [0, 2]],
     [2, 'setxy2', 0, 0, [1, 3, 4, 5]],
     [3, 'titlex', 0, 0, [2, None]],
     [4, 'titley', 0, 0, [2, None]],
     [5, 'pendown', 0, 0, [2, 6]],
     [6, 'setscale', 0, 0, [5, 7, 8]],
     [7, ['number', '100'], 0, 0, [6, None]],
     [8, 'show', 0, 0, [6, 9, 10]],
     [9, ['string', _('Title')], 0, 0, [8, None]],
     [10, 'penup', 0, 0, [8, 11]],
     [11, 'setxy2', 0, 0, [10, 12, 13, 14]],
     [12, 'leftx', 0, 0, [11, None]],
     [13, 'topy', 0, 0, [11, None]],
     [14, 'pendown', 0, 0, [11, 15]],
     [15, 'setscale', 0, 0, [14, 16, 17]],
     [16, ['number', '90'], 0, 0, [15, None]],
     [17, 'showaligned', 0, 0, [15, 18, None]],
     [18, 'journal', 0, 0, [17, None]]],
    '2x2':
    [[0, ['sandwichclamp', 546], 0, 0, [None, 1, None]],
     [1, 'penup', 0, 0, [0, 2]],
     [2, 'setxy2', 0, 0, [1, 3, 4, 5]],
     [3, 'titlex', 0, 0, [2, None]],
     [4, 'titley', 0, 0, [2, None]],
     [5, 'pendown', 0, 0, [2, 6]],
     [6, 'setscale', 0, 0, [5, 7, 8]],
     [7, ['number', '100'], 0, 0, [6, None]],
     [8, 'show', 0, 0, [6, 9, 10]],
     [9, ['string', _('Title')], 0, 0, [8, None]],
     [10, 'setscale', 0, 0, [8, 11, 12]],
     [11, ['number', '35'], 0, 0, [10, None]],
     [12, 'penup', 0, 0, [10, 13]],
     [13, 'setxy2', 0, 0, [12, 14, 15, 16]],
     [14, 'leftx', 0, 0, [13, None]],
     [15, 'topy', 0, 0, [13, None]],
     [16, 'pendown', 0, 0, [13, 17]],
     [17, 'showaligned', 0, 0, [16, 18, 19]],
     [18, 'journal', 0, 0, [17, None]],
     [19, 'penup', 0, 0, [17, 20]],
     [20, 'setxy2', 0, 0, [19, 21, 22, 23]],
     [21, 'rightx', 0, 0, [20, None]],
     [22, 'topy', 0, 0, [20, None]],
     [23, 'pendown', 0, 0, [20, 24]],
     [24, 'showaligned', 0, 0, [23, 25, 26]],
     [25, 'journal', 0, 0, [24, None]],
     [26, 'penup', 0, 0, [24, 27]],
     [27, 'setxy2', 0, 0, [26, 28, 29, 30]],
     [28, 'leftx', 0, 0, [27, None]],
     [29, 'bottomy', 0, 0, [27, None]],
     [30, 'pendown', 0, 0, [27, 31]],
     [31, 'showaligned', 0, 0, [30, 32, 33]],
     [32, 'journal', 0, 0, [31, None]],
     [33, 'penup', 0, 0, [31, 34]],
     [34, 'setxy2', 0, 0, [33, 35, 36, 37]],
     [35, 'rightx', 0, 0, [34, None]],
     [36, 'bottomy', 0, 0, [34, None]],
     [37, 'pendown', 0, 0, [34, 38]],
     [38, 'showaligned', 0, 0, [37, 39, None]],
     [39, 'journal', 0, 0, [38, None]]],
    '1x2':
    [[0, ['sandwichclamp', 546], 0, 0, [None, 1, None]],
     [1, 'penup', 0, 0, [0, 2]],
     [2, 'setxy2', 0, 0, [1, 3, 4, 5]],
     [3, 'titlex', 0, 0, [2, None]],
     [4, 'titley', 0, 0, [2, None]],
     [5, 'pendown', 0, 0, [2, 6]],
     [6, 'setscale', 0, 0, [5, 7, 8]],
     [7, ['number', '100'], 0, 0, [6, None]],
     [8, 'show', 0, 0, [6, 9, 10]],
     [9, ['string', _('Title')], 0, 0, [8, None]],
     [10, 'setscale', 0, 0, [8, 11, 12]],
     [11, ['number', '35'], 0, 0, [10, None]],
     [12, 'penup', 0, 0, [10, 13]],
     [13, 'setxy2', 0, 0, [12, 14, 15, 16]],
     [14, 'leftx', 0, 0, [13, None]],
     [15, 'topy', 0, 0, [13, None]],
     [16, 'pendown', 0, 0, [13, 17]],
     [17, 'showaligned', 0, 0, [16, 18, 19]],
     [18, 'journal', 0, 0, [17, None]],
     [19, 'penup', 0, 0, [17, 20]],
     [20, 'setxy2', 0, 0, [19, 21, 22, 23]],
     [21, 'rightx', 0, 0, [20, None]],
     [22, 'topy', 0, 0, [20, None]],
     [23, 'pendown', 0, 0, [20, 24]],
     [24, 'showaligned', 0, 0, [23, 25, 26]],
     [25, 'description', 0, 0, [24, None]],
     [26, 'penup', 0, 0, [24, 27]],
     [27, 'setxy2', 0, 0, [26, 28, 29, 30]],
     [28, 'leftx', 0, 0, [27, None]],
     [29, 'bottomy', 0, 0, [27, None]],
     [30, 'pendown', 0, 0, [27, 31]],
     [31, 'showaligned', 0, 0, [30, 32, 33]],
     [32, 'journal', 0, 0, [31, None]],
     [33, 'penup', 0, 0, [31, 34]],
     [34, 'setxy2', 0, 0, [33, 35, 36, 37]],
     [35, 'rightx', 0, 0, [34, None]],
     [36, 'bottomy', 0, 0, [34, None]],
     [37, 'pendown', 0, 0, [34, 38]],
     [38, 'showaligned', 0, 0, [37, 39, None]],
     [39, 'description', 0, 0, [38, None]]],
    '2x1':
    [[0, ['sandwichclamp', 546], 0, 0, [None, 1, None]],
     [1, 'penup', 0, 0, [0, 2]],
     [2, 'setxy2', 0, 0, [1, 3, 4, 5]],
     [3, 'titlex', 0, 0, [2, None]],
     [4, 'titley', 0, 0, [2, None]],
     [5, 'pendown', 0, 0, [2, 6]],
     [6, 'setscale', 0, 0, [5, 7, 8]],
     [7, ['number', '100'], 0, 0, [6, None]],
     [8, 'show', 0, 0, [6, 9, 10]],
     [9, ['string', _('Title')], 0, 0, [8, None]],
     [10, 'setscale', 0, 0, [8, 11, 12]],
     [11, ['number', '35'], 0, 0, [10, None]],
     [12, 'penup', 0, 0, [10, 13]],
     [13, 'setxy2', 0, 0, [12, 14, 15, 16]],
     [14, 'leftx', 0, 0, [13, None]],
     [15, 'topy', 0, 0, [13, None]],
     [16, 'pendown', 0, 0, [13, 17]],
     [17, 'showaligned', 0, 0, [16, 18, 19]],
     [18, 'journal', 0, 0, [17, None]],
     [19, 'penup', 0, 0, [17, 20]],
     [20, 'setxy2', 0, 0, [19, 21, 22, 23]],
     [21, 'rightx', 0, 0, [20, None]],
     [22, 'topy', 0, 0, [20, None]],
     [23, 'pendown', 0, 0, [20, 24]],
     [24, 'showaligned', 0, 0, [23, 25, 26]],
     [25, 'journal', 0, 0, [24, None]],
     [26, 'penup', 0, 0, [24, 27]],
     [27, 'setxy2', 0, 0, [26, 28, 29, 30]],
     [28, 'leftx', 0, 0, [27, None]],
     [29, 'bottomy', 0, 0, [27, None]],
     [30, 'pendown', 0, 0, [27, 31]],
     [31, 'showaligned', 0, 0, [30, 32, 33]],
     [32, 'description', 0, 0, [31, None]],
     [33, 'penup', 0, 0, [31, 34]],
     [34, 'setxy2', 0, 0, [33, 35, 36, 37]],
     [35, 'rightx', 0, 0, [34, None]],
     [36, 'bottomy', 0, 0, [34, None]],
     [37, 'pendown', 0, 0, [34, 38]],
     [38, 'showaligned', 0, 0, [37, 39, None]],
     [39, 'description', 0, 0, [38, None]]],
    '1x1':
    [[0, ['sandwichclamp', 336], 0, 0, [None, 1, None]],
     [1, 'penup', 0, 0, [0, 2]],
     [2, 'setxy2', 0, 0, [1, 3, 4, 5]],
     [3, 'titlex', 0, 0, [2, None]],
     [4, 'titley', 0, 0, [2, None]],
     [5, 'pendown', 0, 0, [2, 6]],
     [6, 'setscale', 0, 0, [5, 7, 8]],
     [7, ['number', '100'], 0, 0, [6, None]],
     [8, 'show', 0, 0, [6, 9, 10]],
     [9, ['string', _('Title')], 0, 0, [8, None]],
     [10, 'setscale', 0, 0, [8, 11, 12]],
     [11, ['number', '35'], 0, 0, [10, None]],
     [12, 'penup', 0, 0, [10, 13]],
     [13, 'setxy2', 0, 0, [12, 14, 15, 16]],
     [14, 'leftx', 0, 0, [13, None]],
     [15, 'topy', 0, 0, [13, None]],
     [16, 'pendown', 0, 0, [13, 17]],
     [17, 'showaligned', 0, 0, [16, 18, 19]],
     [18, 'journal', 0, 0, [17, None]],
     [19, 'penup', 0, 0, [17, 20]],
     [20, 'setxy2', 0, 0, [19, 21, 22, 23]],
     [21, 'rightx', 0, 0, [20, None]],
     [22, 'topy', 0, 0, [20, None]],
     [23, 'pendown', 0, 0, [20, 24]],
     [24, 'showaligned', 0, 0, [23, 25, None]],
     [25, 'description', 0, 0, [24, None]]],
    'reskin':
    [[0, 'skin', 0, 0, [None, 1, None]],
     [1, 'journal', 0, 0, [0, None]]],
    'newfood':
    [[0, 'add_food', 0, 0, [None, 1, 2, 3, 4, 5, 6, 7, None]],
     [1, ['string', _('banana')], 0, 0, [0, None]],
     [2, 'journal', 0, 0, [0, None]],
     [3, ['number', '105'], 0, 0, [0, None]],
     [4, ['number', '1'], 0, 0, [0, None]],
     [5, ['number', '27'], 0, 0, [0, None]],
     [6, ['number', '3'], 0, 0, [0, None]],
     [7, ['number', '0'], 0, 0, [0, None]]],
    'loadheapfromjournal':
    [[0, 'loadheap', 0, 0, [None, 1, None]],
     [1, 'journal', 0, 0, [0, None]]]}
