# -*- coding: utf-8 -*-
#Copyright (c) 2010, Walter Bender

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

"""
This file contains the constants that by-in-large determine the
behavior of Turtle Art. Notably, the block palettes are defined
below. If you want to add a new block to Turtle Art, it is generally a
matter of modifying some tables below and then adding the primitive to
talogo.py. For example, if we want to add a new turtle command,
'uturn', we'd make the following changes:

(1) We'd add 'uturn' to the PALETTES list of lists:

PALETTES = [['forward', 'back', 'clean', 'left', 'right', 'uturn', 'show',
             'seth', 'setxy', 'heading', 'xcor', 'ycor', 'setscale',
              'arc', 'scale'],
            ['penup','pendown', 'setpensize', 'fillscreen', 'pensize',...

(2) Then we'd add it to one of the block-style definitions. Since it takes
no arguments, we'd add it here:

BASIC_STYLE = ['clean', 'penup', 'pendown', 'stack1', 'stack2', 'vspace',
    'hideblocks', 'showblocks', 'clearheap', 'printheap', 'kbinput', 'uturn']

(3) Then we give it a name (Note the syntax _('string to be
translated') used by the language-internationalization system; also
note that the name is an array, as some blocks contain multiple
strings.):

BLOCK_NAMES = {
...
    'uturn':[_('u-turn')],
...
              }

(4) and a help-menu entry:

HELP_STRINGS = {
...
    'uturn':_('change the heading of the turtle 180 degrees'),
...
               }

(5) Next, we need to define it as a primitive for the Logo command
parser (generally just the same name):

PRIMITIVES = {
...
    'uturn':'uturn',
...
             }

(6) Since there are no default arguments, we don't need to do anything
else here. But we do need to define the actual function in talogo.py

DEFPRIM = {
...
    'uturn':[0, lambda self: self.tw.canvas.seth(self.tw.canvas.heading+180)],
...
          }

That's it. When you next run Turtle Art, you will have a 'uturn' block
on the Turtle Palette.

Adding a new palette is simply a matter of: (1) adding an additional
entry to PALETTE_NAMES; (2) new list of blocks to PALETTES; and (3) an
additional entry in COLORS. However you will have to: (4) create icons
for the palette-selector buttons. These are kept in the icons
subdirectory. You need two icons: yourpalettenameoff.svg and
yourpalettenameon.svg, where yourpalettename is the same string as the
entry you added to the PALETTE_NAMES list. Note that the icons should
be the same size (55x55) as the others. This is the default icon size
for Sugar toolbars.

"""

from gettext import gettext as _

#
# Sprite layers
#

HIDE_LAYER = 100
CANVAS_LAYER = 500
OVERLAY_LAYER = 525
TURTLE_LAYER = 550
BLOCK_LAYER = 600
CATEGORY_LAYER = 700
TAB_LAYER = 710
STATUS_LAYER = 900
TOP_LAYER = 1000

#
# Block-palette categories
#

PALETTE_NAMES = ['turtle', 'pen', 'colors', 'numbers', 'flow', 'blocks',
                 'extras', 'portfolio', 'trash']

PALETTES = [['clean', 'forward', 'back', 'show', 'left', 'right',
             'seth', 'setxy2', 'heading', 'xcor', 'ycor', 'setscale',
             'arc', 'scale', 'leftpos', 'toppos', 'rightpos',
             'bottompos'],
            ['penup', 'pendown', 'setpensize', 'fillscreen', 'pensize',
             'setcolor', 'setshade', 'setgray', 'color', 'shade',
             'gray', 'startfill', 'stopfill'],
            ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple',
              'white', 'black'],
            ['plus2', 'minus2', 'product2',
             'division2', 'identity2', 'remainder2', 'sqrt', 'random',
             'number', 'greater2', 'less2', 'equal2', 'not', 'and2', 'or2'],
            ['wait', 'forever', 'repeat', 'if', 'ifelse', 'while', 'until',
             'hspace', 'vspace', 'stopstack'],
            ['hat1', 'stack1', 'hat', 'hat2', 'stack2', 'stack',
             'storeinbox1', 'storeinbox2', 'string', 'box1', 'box2', 'box',
             'storein', 'start'],
            ['kbinput', 'push', 'printheap', 'keyboard', 'pop', 'clearheap',
             'myfunc1arg', 'userdefined', 'addturtle', 'comment', 'print',
             'cartesian', 'width', 'height', 'polar', 'sandwichtop_no_label',
             'sandwichbottom', 'readpixel', 'see', 'reskin'],
            ['journal', 'audio', 'description', 'hideblocks', 'showblocks',
             'fullscreen', 'savepix', 'savesvg', 'picturelist',
             'picture1x1a', 'picture1x1', 'picture2x2', 'picture2x1',
             'picture1x2'],
            ['empty', 'restoreall']]

#
# Block-style attributes
#

COLORS = [["#00FF00", "#00A000"], ["#00FFFF", "#00A0A0"],
          ["#00FFFF", "#00A0A0"], ["#FF00FF", "#A000A0"],
          ["#FFC000", "#A08000"], ["#FFFF00", "#A0A000"],
          ["#FF0000", "#A00000"], ["#0000FF", "#0000A0"],
          ["#FFFF00", "#A0A000"]]

BOX_COLORS = {'red': ["#FF0000", "#A00000"],
              'orange': ["#FFD000", "#AA8000"],
              'yellow': ["#FFFF00", "#A0A000"],
              'blue': ["#0000FF", "#000080"],
              'cyan': ["#00FFFF", "#00A0A0"],
              'green': ["#00FF00", "#008000"],
              'purple': ["#FF00FF", "#A000A0"],
              'white': ["#FFFFFF", "#A0A0A0"],
              'black': ["#000000", "#000000"]}

#
# Misc. parameters
#
PALETTE_HEIGHT = 120
PALETTE_WIDTH = 175
SELECTOR_WIDTH = 55
ICON_SIZE = 55
SELECTED_COLOR = "#0000FF"
SELECTED_STROKE_WIDTH = 1.0
STANDARD_STROKE_WIDTH = 1.0
BLOCK_SCALE = 2.0
PALETTE_SCALE = 1.5
DEFAULT_TURTLE = 'Yertle'
HORIZONTAL_PALETTE = 0
VERTICAL_PALETTE = 1
BLACK = -9999
WHITE = -9998
HIT_HIDE = 248
HIT_SHOW = 240
HIT_RED = "#F80000"
HIT_GREEN = "#00F000"
HIDE_WHITE = "#F8F8F8"
SHOW_WHITE = "#F0F0F0"
DEFAULT_SCALE = 33

#
# Block-style definitions
#
BASIC_STYLE_HEAD = ['start', 'hat1', 'hat2', 'restore', 'restoreall']
BASIC_STYLE_HEAD_1ARG = ['hat']
BASIC_STYLE_TAIL = ['stopstack', 'empty']
BASIC_STYLE = []
BASIC_STYLE_EXTENDED_VERTICAL = ['clean', 'penup', 'pendown', 'stack1',
    'stack2', 'hideblocks', 'showblocks', 'clearheap', 'printheap', 'kbinput',
    'fullscreen', 'sandwichcollapsed', 'cartesian', 'polar', 'startfill',
    'stopfill', 'readpixel', 'vspace']
BASIC_STYLE_EXTENDED = ['picturelist', 'picture1x1', 'picture2x2',
    'picture2x1', 'picture1x2', 'picture1x1a']
BASIC_STYLE_1ARG = ['forward', 'back', 'left', 'right', 'seth', 'show', 'image',
    'setscale', 'setpensize', 'setcolor', 'setshade', 'print', 'showaligned',
    'settextsize', 'settextcolor', 'print', 'wait', 'storeinbox1', 'savepix',
    'storeinbox2', 'wait', 'stack', 'push', 'nop', 'addturtle', 'comment',
    'savesvg', 'setgray', 'skin', 'reskin']
BASIC_STYLE_VAR_ARG = ['userdefined', 'userdefined2args', 'userdefined3args']
BULLET_STYLE = ['templatelist', 'list']
BASIC_STYLE_2ARG = ['arc', 'setxy', 'setxy2', 'fillscreen', 'storein', 'write']
BOX_STYLE = ['number', 'xcor', 'ycor', 'heading', 'pensize', 'color', 'shade',
    'textcolor', 'textsize', 'box1', 'box2', 'string', 'leftpos', 'scale',
    'toppos', 'rightpos', 'bottompos', 'width', 'height', 'pop', 'keyboard',
    'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'white',
    'black', 'titlex', 'titley', 'leftx', 'topy', 'rightx', 'bottomy',
    'volume', 'pitch', 'voltage', 'resistance', 'gray', 'see']
BOX_STYLE_MEDIA = ['description', 'audio', 'journal']
NUMBER_STYLE = ['plus2', 'product2', 'myfunc']
NUMBER_STYLE_VAR_ARG = ['myfunc1arg', 'myfunc2arg', 'myfunc3arg']
NUMBER_STYLE_BLOCK = ['random']
NUMBER_STYLE_PORCH = ['minus2', 'division2', 'remainder2']
NUMBER_STYLE_1ARG = ['sqrt', 'identity2']
NUMBER_STYLE_1STRARG = ['box']
COMPARE_STYLE = ['greater2', 'less2', 'equal2']
BOOLEAN_STYLE = ['and2', 'or2']
NOT_STYLE = ['not']
FLOW_STYLE = ['forever']
FLOW_STYLE_TAIL = ['hspace']
FLOW_STYLE_1ARG = ['repeat']
FLOW_STYLE_BOOLEAN = ['if', 'while', 'until']
FLOW_STYLE_WHILE = ['while2']
FLOW_STYLE_ELSE = ['ifelse']
COLLAPSIBLE_TOP = ['sandwichtop']
COLLAPSIBLE_TOP_NO_ARM = ['sandwichtop_no_arm']
COLLAPSIBLE_TOP_NO_LABEL = ['sandwichtop_no_label']
COLLAPSIBLE_TOP_NO_ARM_NO_LABEL = ['sandwichtop_no_arm_no_label']
COLLAPSIBLE_BOTTOM = ['sandwichbottom']

# Depreciated block styles
PORTFOLIO_STYLE_2x2 = ['template2x2']
PORTFOLIO_STYLE_1x1 = ['template1x1', 'template1x1a']
PORTFOLIO_STYLE_2x1 = ['template2x1']
PORTFOLIO_STYLE_1x2 = ['template1x2']

#
# Blocks that are expandable
#
EXPANDABLE = ['vspace', 'hspace', 'identity2']

EXPANDABLE_BLOCKS = ['plus2', 'minus2', 'division2', 'remainder2', 'product2',
                   'random', 'equal2', 'greater2', 'less2', 'and2', 'or2',
                   'arc', 'setxy', 'setxy2', 'fillscreen', 'storein', 'write']

EXPANDABLE_ARGS = ['templatelist', 'list', 'myfunc1arg', 'myfunc2arg',
                   'myfunc3arg', 'userdefined', 'userdefined2args',
                   'userdefined3args']
#
# Blocks that are 'collapsible'
#
COLLAPSIBLE = ['sandwichbottom', 'sandwichcollapsed']

#
# Depreciated block styles that need dock adjustments
#
OLD_DOCK = ['and', 'or', 'plus', 'minus', 'division', 'product', 'remainder']

#
# Blocks that contain media
#
CONTENT_BLOCKS = ['number', 'string', 'description', 'audio', 'journal']

#
# These blocks get a special skin
#
BLOCKS_WITH_SKIN = ['journal', 'audio', 'description', 'nop', 'userdefined',
                    'userdefined2args', 'userdefined3args']

PYTHON_SKIN = ['nop', 'userdefined', 'userdefined2args', 'userdefined3args']

#
# Block-name dictionary used for labels
#
BLOCK_NAMES = {
    'addturtle': [_('turtle')],
    'and2': [_('and')],
    'arc': [_('arc'), _('angle'), _('radius')],
    'audio': [' '],
    'back': [_('back')],
    'black': [_('black')],
    'blocks': [_('blocks')],
    'blue': [_('blue') + ' = 70'],
    'bottompos': [_('bottom')],
    'bottomy': [_('picture bottom')],
    'box': [_('box')],
    'box1': [_('box 1')],
    'box2': [_('box 2')],
    'cartesian': [_('Cartesian')],
    'clean': [_(' clean ')],
    'clearheap': [_('empty heap')],
    'color': [_('color')],
    'colors': [_('colors')],
    'comment': [_('comment')],
    'cyan': [_('cyan') + ' = 50'],
    'decription': [' '],
    'division2': ['/'],
    'empty': [_('empty trash')],
    'equal2': ['='],
    'extras': [_('extras')],
    'fillscreen': [_('fill screen'), _('color'), _('shade')],
    'flow': [_('flow')],
    'forever': [_('forever')],
    'forward': [_('forward')],
    'fullscreen': [_('full screen')],
    'gray': [_('gray')],
    'greater2': [">"],
    'green': [_('green') + ' = 30'],
    'hat': [_('action')],
    'hat1': [_('action 1')],
    'hat2': [_('action 2')],
    'heading': [_('heading')],
    'height': [_('height')],
    'hideblocks': [_('hide blocks')],
    'hspace': [' '],
    'identity2': ['←'],
    'if': [' ', _('if'), _('then')],
    'ifelse': [' ', _('if'), _('then else')],
    'image': [_('show')],
    'journal': [' '],
    'kbinput': [_('query keyboard')],
    'keyboard': [_('keyboard')],
    'left': [_('left')],
    'leftpos': [_('left')],
    'leftx': [_('picture left')],
    'less2': ['<'],
    'list': ['list'],
    'minus2': ['–'],
    'myfunc': [_('Python'), 'f(x)', 'x'],
    'myfunc1arg': [_('Python'), 'f(x)', 'x'],
    'myfunc2arg': [_('Python'), 'f(x,y)', ' '],
    'myfunc3arg': [_('Python'), 'f(x,y,z)', ' '],
    'nop': [_(' ')],
    'not': [_('not')],
    'number': ['100'],
    'numbers': [_('numbers')],
    'orange': [_('orange') + ' = 10'],
    'or2': [_('or')],
    'pen': [_('pen')],
    'pendown': [_('pen down')],
    'pensize': [_('pen size')],
    'penup': [_('pen up')],
    'picturelist': [' '],
    'picture1x1': [' '],
    'picture1x1a': [' '],
    'picture2x2': [' '],
    'picture2x1': [' '],
    'picture1x2': [' '],
    'pitch': [_('pitch')],
    'plus2': [' + '],
    'polar': [_('polar')],
    'pop': [_('pop')],
    'portfolio': [_('portfolio')],
    'printheap': [_('show heap')],
    'print': [_('print')],
    'product2': ['×'],
    'purple': [_('purple') + ' = 90'],
    'push': [_('push')],
    'random': [_('random'), _('min'), _('max')],
    'readpixel': [_('read pixel')],
    'red': [_('red') + ' = 0'],
    'remainder2': [_('mod')],
    'repeat': [' ', _('repeat')],
    'reskin': [_('turtle shell')],
    'resistance': [_('resistance')],
    'restore': [_('restore last')],
    'restoreall': [_('restore all')],
    'right': [_('right')],
    'rightpos': [_('right')],
    'rightx': [_('picture right')],
    'savepix': [_('save picture')],
    'savesvg': [_('save SVG')],
    'sandwichbottom': [' ', ' '],
    'sandwichcollapsed': [' ', _('click to open')],
    'sandwichtop': [_('top of stack')],
    'sandwichtop_no_label': [' '],
    'sandwichtop_no_arm': [_('top of stack')],
    'sandwichtop_no_arm_no_label': [' '],
    'scale': [_('scale')],
    'see': [_('turtle sees')],
    'setcolor': [_('set color')],
    'setgray': [_('set gray')],
    'seth': [_('set heading')],
    'setpensize': [_('set pen size')],
    'setscale': [_('set scale')],
    'setshade': [_('set shade')],
    'settextcolor': [_('set text color')],
    'settextsize': [_('set text size')],
    'setxy': [_('set xy'), _('x'), _('y')],
    'setxy2': [_('set xy'), _('x'), _('y')],
    'shade': [_('shade')],
    'show': [_('show')],
    'showblocks': [_('show blocks')],
    'showaligned': [_('show aligned')],
    'skin': [_('turtle shell')],
    'sqrt': ['√'],
    'stack': [_('action')],
    'stack1': [_('action 1')],
    'stack2': [_('action 2')],
    'start': [_('start')],
    'startfill': [_('start fill')],
    'stopfill': [_('end fill')],
    'stopstack': [_('stop action')],
    'storein': [_('store in'), _('box'), _('value')],
    'storeinbox1': [_('store in box 1')],
    'storeinbox2': [_('store in box 2')],
    'string': [_('text')],
    'template1x1': [' '],
    'template1x1a': [' '],
    'template1x2': [' '],
    'template2x1': [' '],
    'template2x2': [' '],
    'templatelist': [' '],
    'textsize': [_('text size')],
    'titlex': [_('title x')],
    'titley': [_('title y')],
    'toppos': [_('top')],
    'topy': [_('picture top')],
    'trash': [_('trash')],
    'turtle': [_('turtle')],
    'until': [_('until')],
    'userdefined': [_(' ')],
    'userdefined2args': [_(' ')],
    'userdefined3args': [_(' ')],
    'voltage': [_('voltage')],
    'volume': [_('volume')],
    'vspace': [' '],
    'wait': [_('wait')],
    'while': [_('while')],
    'while2': [_('while')],
    'white': [_('white')],
    'width': [_('width')],
    'write': [_('write')],
    'xcor': [_('xcor')],
    'ycor': [_('ycor')],
    'yellow': [_('yellow') + ' = 20']}

#
# Logo primitives
#

PRIMITIVES = {
    'addturtle': 'turtle',
    'and2': 'and',
    'arc': 'arc',
    'back': 'back',
    'black': 'black',
    'blue': 'blue',
    'bottompos': 'bpos',
    'bottomy': 'boty',
    'box1': 'box1',
    'box2': 'box2',
    'box': 'box',
    'cartesian': 'cartesian',
    'clean': 'clean',
    'clearheap': 'clearheap',
    'color': 'color',
    'comment': 'comment',
    'cyan': 'cyan',
    'division2': 'division',
    'equal2': 'equal?',
    'fillscreen': 'fillscreen',
    'forever': 'forever',
    'forward': 'forward',
    'fullscreen': 'fullscreen',
    'gray': 'gray',
    'greater2': 'greater?',
    'green': 'green',
    'hat': 'nop3',
    'hat1': 'nop1',
    'hat2': 'nop2',
    'heading': 'heading',
    'height': 'vres',
    'hideblocks': 'hideblocks',
    'hspace': 'nop',
    'identity2': 'id',
    'if': 'if',
    'ifelse': 'ifelse',
    'image': 'show',
    'kbinput': 'kbinput',
    'keyboard': 'keyboard',
    'left': 'left',
    'leftpos': 'lpos',
    'leftx': 'leftx',
    'less2': 'less?',
    'list': 'bulletlist',
    'minus2': 'minus',
    'myfunc': 'myfunction',
    'myfunc1arg': 'myfunction',
    'myfunc2arg': 'myfunction2',
    'myfunc3arg': 'myfunction3',
    'nop': 'userdefined',
    'not': 'not',
    'orange': 'orange',
    'or2': 'or',
    'pendown': 'pendown',
    'pensize': 'pensize',
    'penup': 'penup',
    'pitch': 'pitch',
    'plus2': 'plus',
    'polar': 'polar',
    'pop': 'pop',
    'printheap': 'printheap',
    'print': 'print',
    'product2': 'product',
    'purple': 'purple',
    'push': 'push',
    'random': 'random',
    'red': 'red',
    'readpixel': 'readpixel',
    'remainder2': 'mod',
    'repeat': 'repeat',
    'resistance': 'resistance',
    'right': 'right',
    'rightpos': 'rpos',
    'rightx': 'rightx',
    'sandwichtop': 'comment',
    'sandwichtop_no_arm': 'comment',
    'sandwichtop_no_label': 'nop',
    'sandwichtop_no_arm_no_label': 'nop',
    'sandwichbottom': 'nop',
    'sandwichcollapsed': 'nop',
    'savepix': 'savepix',
    'savesvg': 'savesvg',
    'see': 'see',
    'scale': 'scale',
    'setcolor': 'setcolor',
    'setgray': 'setgray',
    'seth': 'seth',
    'setpensize': 'setpensize',
    'setscale': 'setscale',
    'setshade': 'setshade',
    'settextsize': 'settextsize',
    'settextcolor': 'settextcolor',
    'setxy': 'setxy',
    'setxy2': 'setxy2',
    'shade': 'shade',
    'show': 'show',
    'showblocks': 'showblocks',
    'showaligned': 'showaligned',
    'skin': 'skin',
    'sqrt': 'sqrt',
    'stack': 'stack',
    'stack1': 'stack1',
    'stack2': 'stack2',
    'start': 'start',
    'startfill': 'startfill',
    'stopfill': 'stopfill',
    'stopstack': 'stopstack',
    'storein': 'storeinbox',
    'storeinbox1': 'storeinbox1',
    'storeinbox2': 'storeinbox2',
    'template1x1': 't1x1',
    'template1x1a': 't1x1a',
    'template1x2': 't1x2',
    'template2x1': 't2x1',
    'template2x2': 't2x2',
    'templatelist': 'bullet',
    'textsize': 'textsize',
    'titlex': 'titlex',
    'titley': 'titley',
    'toppos': 'tpos',
    'topy': 'topy',
    'userdefined': 'userdefined',
    'userdefined2args': 'userdefined2',
    'userdefined3args': 'userdefined3',
    'voltage': 'voltage',
    'volume': 'volume',
    'vspace': 'nop',
    'wait': 'wait',
    'while2': 'while',
    'white': 'white',
    'width': 'hres',
    'write': 'write',
    'xcor': 'xcor',
    'ycor': 'ycor',
    'yellow': 'yellow'}

#
# block default values
#

DEFAULTS = {
    'addturtle': [1],
    'arc': [90, 100],
    'audio': [None],
    'back': [100],
    'box': [_('my box')],
    'comment': [_('comment')],
    'description': [None],
    'fillscreen': [60, 80],
    'forever': [None, 'vspace'],
    'forward': [100],
    'hat': [_('action')],
    'if': [None, None, 'vspace'],
    'ifelse': [None, 'vspace', None, 'vspace'],
    'journal': [None],
    'left': [90],
    'list': ['∙ ', '∙ '],
    'media': [None],
    'myfunc': ['x', 100],
    'myfunc1arg': ['x', 100],
    'myfunc2arg': ['x+y', 100, 100],
    'myfunc3arg': ['x+y+z', 100, 100, 100],
    'nop': [100],
    'number': [100],
    'random': [0, 100],
    'repeat': [4, None, 'vspace'],
    'right': [90],
    'sandwichtop': [_('label')],
    'sandwichtop_no_arm': [_('label')],
    'savepix': [_('picture name')],
    'savesvg': [_('picture name')],
    'setcolor': [0],
    'setgray': [100],
    'seth': [0],
    'setpensize': [5],
    'setscale': [33],
    'setshade': [50],
    'settextsize': [48],
    'settextcolor': [0],
    'setxy': [0, 0],
    'setxy2': [0, 0],
    'show': [_('text')],
    'showaligned': [_('text')],
    'stack': [_('action')],
    'storeinbox1': [100],
    'storeinbox2': [100],
    'storein': [_('my box'), 100],
    'string': [_('text')],
    'template1x1': [_('Title'), 'None'],
    'template1x1a': [_('Title'), 'None'],
    'template1x2': [_('Title'), 'None', 'None'],
    'template2x1': [_('Title'), 'None', 'None'],
    'template2x2': [_('Title'), 'None', 'None', 'None', 'None'],
    'templatelist': [_('Title'), '∙ '],
    'userdefined': [100],
    'userdefined2args': [100, 100],
    'userdefined3args': [100, 100, 100],
    'wait': [1],
    'write': [_('text'), 32]}

#
# Blocks that can interchange strings and numbers for their arguments
#
STRING_OR_NUMBER_ARGS = ['plus2', 'equal2', 'less2', 'greater2', 'box',
                         'template1x1', 'template1x2', 'template2x1', 'list',
                         'template2x2', 'template1x1a', 'templatelist', 'nop',
                         'print', 'stack', 'hat', 'addturtle', 'myfunc',
                         'myfunc1arg', 'myfunc2arg', 'myfunc3arg', 'comment',
                         'sandwichtop', 'sandwichtop_no_arm', 'userdefined',
                         'userdefined2args', 'userdefined3args', 'storein']

CONTENT_ARGS = ['show', 'showaligned', 'push', 'storein', 'storeinbox1',
                'storeinbox2']

#
# Status blocks
#

MEDIA_SHAPES = ['audiooff', 'audioon', 'audiosmall',
                'journaloff', 'journalon', 'journalsmall',
                'descriptionoff', 'descriptionon', 'descriptionsmall',
                'pythonoff', 'pythonon', 'pythonsmall',
                'list', '1x1', '1x1a', '2x1', '1x2', '2x2']

OVERLAY_SHAPES = ['Cartesian', 'Cartesian_labeled', 'polar']

STATUS_SHAPES = ['status', 'info', 'nostack', 'noinput', 'emptyheap',
                 'emptybox', 'nomedia', 'nocode', 'overflowerror', 'negroot',
                 'syntaxerror', 'nofile', 'nojournal', 'zerodivide',
                 'notanumber']

#
# Emulate Sugar toolbar when running from outside of Sugar
#
TOOLBAR_SHAPES = ['hideshowoff', 'eraseron', 'run-fastoff',
                  'run-slowoff', 'debugoff', 'stopiton']

#
# Legacy names
#
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
             'sandwichtop2': 'sandwichtop'}

#
# Define the relative size and postion of media objects
#                    (w, h, x, y, dx, dy)
#
TITLEXY = (0.9375, 0.875)

#
# Relative placement of portfolio objects (used by depreciated blocks)
#
TEMPLATES = {'t1x1': (0.5, 0.5, 0.0625, 0.125, 1.05, 0),
             't2z1': (0.5, 0.5, 0.0625, 0.125, 1.05, 1.05),
             't1x2': (0.45, 0.45, 0.0625, 0.125, 1.05, 1.05),
             't2x2': (0.45, 0.45, 0.0625, 0.125, 1.05, 1.05),
             't1x1a': (0.9, 0.9, 0.0625, 0.125, 0, 0),
             'bullet': (1, 1, 0.0625, 0.125, 0, 0.1),
             'insertimage': (0.333, 0.333)}

#
# Names for blocks without names for popup help
#
SPECIAL_NAMES = {
    'audio': _('audio'),
    'division2': _('divide'),
    'equal2': _('equal'),
    'greater2': _('greater than'),
    'hspace': _('horizontal space'),
    'identity2': _('identity'),
    'if': _('if then'),
    'ifelse': _('if then else'),
    'journal': _('journal'),
    'less2': _('less than'),
    'minus2': _('minus'),
    'nop': _('Python code'),
    'number': _('number'),
    'plus2': _('plus'),
    'product2': _('multiply'),
    'sqrt': _('square root'),
    'template1x1': _('presentation 1x1'),
    'template1x1a': _('presentation 1x1'),
    'template1x2': _('presentation 1x2'),
    'template2x1': _('presentation 2x1'),
    'template2x2': _('presentation 2x2'),
    'templatelist': _('presentation bulleted list'),
    'textsize': _('text size'),
    'vspace': _('vertical space')}

#
# Help messages
#
HELP_STRINGS = {
    'addturtle': _("chooses which turtle to command"),
    'and2': _("logical AND operator"),
    'arc': _("moves turtle along an arc"),
    'audio': _("Sugar Journal audio object"),
    'back': _("moves turtle backward"),
    'blocks': _("Palette of variable blocks"),
    'bottompos': _("ycor of bottom of screen"),
    'box1': _("Variable 1 (numeric value)"),
    'box2': _("Variable 2 (numeric value)"),
    'box': _("named variable (numeric value)"),
    'cartesian': _("displays Cartesian coordinates"),
    'clean': _("clears the screen and reset the turtle"),
    'clearheap': _("emptys FILO (first-in-last-out heap)"),
    'color': _("holds current pen color (can be used in place of a number block)"),
    'colors': _("Palette of pen colors"),
    'comment': _("places a comment in your code"),
    'debugoff': _("Debug"),
    'description': _("Sugar Journal description field"),
    'division2': _("divides top numeric input (numerator) by bottom numeric input (denominator)"),
    'empty': _("permanently deletes items in trash"),
    'eraseron': _("Clean"),
    'equal2': _("logical equal-to operator"),
    'extras': _("Palette of extra options"),
    'fillscreen': _("fills the background with (color, shade)"),
    'flow': _("Palette of flow operators"),
    'forever': _("loops forever"),
    'forward': _("moves turtle forward"),
    'fullscreen': _("hides the Sugar toolbars"),
    'gray': _("holds current gray level (can be used in place of a number block)"),
    'greater2': _("logical greater-than operator"),
    'hat1': _("top of Action 1 stack"),
    'hat2': _("top of Action 2 stack"),
    'hat': _("top of nameable action stack"),
    'heading': _("holds current heading value of the turtle (can be used in place of a number block)"),
    'height': _("the canvas height"),
    'hideblocks': _("declutters canvas by hiding blocks"),
    'hideshowoff': _("Hide blocks"),
    'hspace': _("jogs stack right"),
    'identity2': _("identity operator used for extending blocks"),
    'ifelse': _("if-then-else operator that uses boolean operators from Numbers palette"),
    'if': _("if-then operator that uses boolean operators from Numbers palette"),
    'journal': _("Sugar Journal media object"),
    'kbinput': _("query for keyboard input (results stored in keyboard block)"),
    'keyboard': _("holds results of query-keyboard block"),
    'leftpos': _("xcor of left of screen"),
    'left': _("turns turtle counterclockwise (angle in degrees)"),
    'less2': _("logical less-than operator"),
    'minus2': _("subtracts bottom numeric input from top numeric input"),
    'myfunc': _("a programmable block: used to add advanced math equations, e.g., sin(x)"),
    'myfunc1arg': _("a programmable block: used to add advanced single-variable math equations, e.g., sin(x)"),
    'myfunc2arg': _("a programmable block: used to add advanced multi-variable math equations, e.g., sqrt(x*x+y*y)"),
    'myfunc3arg': _("a programmable block: used to add advanced multi-variable math equations, e.g., sin(x+y+z)"),
    'next': _('displays next palette'),
    'nop': _("runs code found in the tamyblock.py module found in the Journal"),
    'not': _("logical NOT operator"),
    'numbers': _("Palette of numeric operators"),
    'number': _("used as numeric input in mathematic operators"),
    'or': _("logical OR operator"),
    'orientation': _("changes the orientation of the palette of blocks"),
    'pendown': _("Turtle will draw when moved."),
    'pen': _("Palette of pen commands"),
    'pensize': _("holds current pen size (can be used in place of a number block)"),
    'penup': _("Turtle will not draw when moved."),
    'picture1x1': _("presentation template: select Journal object (with description)"),
    'picture1x1a': _("presentation template: select Journal object (no description)"),
    'picture1x2': _("presentation template: select two Journal objects"),
    'picture2x1': _("presentation template: select two Journal objects"),
    'picture2x2': _("presentation template: select four Journal objects"),
    'picturelist': _("presentation template: list of bullets"),
    'pitch': _('microphone input pitch'),
    'plus2': _("adds two alphanumeric inputs"),
    'polar': _("displays polar coordinates"),
    'pop': _("pops value off FILO (first-in last-out heap)"),
    'portfolio': _("Palette of presentation templates"),
    'print': _("prints value in status block at bottom of the screen"),
    'printheap': _("shows values in FILO (first-in last-out heap)"),
    'product2': _("multiplies two numeric inputs"),
    'push': _("pushes value onto FILO (first-in last-out heap)"),
    'random': _("returns random number between minimum (top) and maximum (bottom) values"),
    'readpixel': _("RGB color under the turtle is pushed to the stack"),
    'remainder2': _("modular (remainder) operator"),
    'repeat': _("loops specified number of times"),
    'resistance': _("sensor input resistance"),
    'reskin': _("put a custom 'shell' on the turtle"),
    'restore': _("restores most recent blocks from trash"),
    'restoreall': _("restore all blocks from trash"),
    'rightpos': _("xcor of right of screen"),
    'right': _("turns turtle clockwise (angle in degrees)"),
    'run-fastoff': _("Run"),
    'run-slowoff': _("Step"),
    'sandwichbottom': _("bottom block in a collapsibe stack: click to collapse"),
    'sandwichcollapsed': _("bottom block in a collapsed stack: click to open"),
    'sandwichtop': _("top of a collapsible stack"),
    'sandwichtop_no_label': _("top of a collapsed stack"),
    'sandwichtop_no_arm': _("top of a collapsible stack"),
    'sandwichtop_no_arm_no_label': _("top of a collapsed stack"),
    'savepix': _("saves a picture to the Sugar Journal"),
    'savesvg': _("saves turtle graphics as an SVG file in the Sugar Journal"),
    'scale': _("holds current scale value"),
    'see': _('returns the color that the turtle "sees"'),
    'setcolor': _("sets color of the line drawn by the turtle"),
    'setgray': _("sets gray level of the line drawn by the turtle"),
    'seth': _("sets the heading of the turtle (0 is towards the top of the screen.)"),
    'setpensize': _("sets size of the line drawn by the turtle"),
    'setscale': _("sets the scale of media"),
    'setshade': _("sets shade of the line drawn by the turtle"),
    'settextcolor': _("sets color of text drawn by the turtle"),
    'settextsize': _("sets size of text drawn by turtle"),
    'setxy': _("moves turtle to position xcor, ycor; (0, 0) is in the center of the screen."),
    'setxy2': _("moves turtle to position xcor, ycor; (0, 0) is in the center of the screen."),
    'shade': _("holds current pen shade"),
    'show': _("draws text or show media from the Journal"),
    'showblocks': _("restores hidden blocks"),
    'skin': _("put a custom 'shell' on the turtle"),
    'sqrt': _("calculates square root"),
    'stack1': _("invokes Action 1 stack"),
    'stack2': _("invokes Action 2 stack"),
    'stack': _("invokes named action stack"),
    'start': _("connects action to toolbar run buttons"),
    'startfill': _("starts filled polygon (used with end fill block)"),
    'stopfill': _("completes filled polygon (used with start fill block)"),
    'stopiton': _("Stop turtle"),
    'stopstack': _("stops current action"),
    'storeinbox1': _("stores numeric value in Variable 1"),
    'storeinbox2': _("stores numeric value in Variable 2"),
    'storein': _("stores numeric value in named variable"),
    'string': _("string value"),
    'template1x1': _("presentation template: select Journal object (with description)"),
    'template1x1a': _("presentation template: select Journal object (no description)"),
    'template1x2': _("presentation template: select two Journal objects"),
    'template2x1': _("presentation template: select two Journal objects"),
    'template2x2': _("presentation template: select four Journal objects"),
    'templatelist': _("presentation template: list of bullets"),
    'textcolor': _("holds current text color (can be used in place of a number block)"),
    'textsize': _("holds current text size (can be used in place of a number block)"),
    'toppos': _("ycor of top of screen"),
    'trash': _("Trashcan"),
    'turtle': _("Palette of turtle commands"),
    'until': _("do-until-True operator that uses boolean operators from Numbers palette"),
    'userdefined': _("runs code found in the tamyblock.py module found in the Journal"),
    'userdefined2args': _("runs code found in the tamyblock.py module found in the Journal"),
    'userdefined3args': _("runs code found in the tamyblock.py module found in the Journal"),
    'voltage': _("sensor voltage"),
    'volume': _("microphone input volume"),
    'vspace': _("jogs stack down"),
    'wait': _("pauses program execution a specified number of seconds"),
    'while': _("do-while-True operator that uses boolean operators from Numbers palette"),
    'width': _("the canvas width"),
    'xcor': _("holds current x-coordinate value of the turtle (can be used in place of a number block)"),
    'ycor': _("holds current y-coordinate value of the turtle (can be used in place of a number block)")}

#
# 'dead key' Unicode dictionaries
#

DEAD_KEYS = ['grave', 'acute', 'circumflex', 'tilde', 'diaeresis', 'abovering']
DEAD_DICTS = [{'A':192, 'E':200, 'I':204, 'O':210, 'U':217, 'a':224, 'e':232,
               'i':236, 'o':242, 'u':249},
              {'A':193, 'E':201, 'I':205, 'O':211, 'U':218, 'a':225, 'e':233,
               'i':237, 'o':243, 'u':250},
              {'A':194, 'E':202, 'I':206, 'O':212, 'U':219, 'a':226, 'e':234,
               'i':238, 'o':244, 'u':251},
              {'A':195, 'O':211, 'N':209, 'U':360, 'a':227, 'o':245, 'n':241,
               'u':361},
              {'A':196, 'E':203, 'I':207, 'O':211, 'U':218, 'a':228, 'e':235,
               'i':239, 'o':245, 'u':252},
              {'A':197, 'a':229}]
NOISE_KEYS = ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock', 'Pause',
              'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift', 'KP_Divide',
              'Escape', 'Return', 'KP_Page_Up', 'Up', 'Down', 'Menu',
              'Left', 'Right', 'KP_Home', 'KP_End', 'KP_Up', 'Super_L',
              'KP_Down', 'KP_Left', 'KP_Right', 'KP_Page_Down', 'Scroll_Lock',
              'Page_Down', 'Page_Up']
WHITE_SPACE = ['space', 'Tab']

CURSOR = '█'
RETURN = '⏎'


#
# Macros (groups of blocks)
#
MACROS = {
    'until':
              [[0, 'forever', 0, 0, [None, 2, 1]],
               [1, 'vspace', 0, 0, [0, None]],
               [2, 'ifelse', 0, 0, [0, None, 3, None, None]],
               [3, 'vspace', 0, 0, [2, 4]],
               [4, 'stopstack', 0, 0, [3, None]]],
    'while':
              [[0, 'forever', 0, 0, [None, 2, 1]],
               [1, 'vspace', 0, 0, [0, None]],
               [2, 'ifelse', 0, 0, [0, None, 3, 4, None]],
               [3, 'vspace', 0, 0, [2, None]],
               [4, 'stopstack', 0, 0, [2, None]]],
    'kbinput':
              [[0, 'forever', 0, 0, [None, 1, None]],
               [1, 'kbinput', 0, 0, [0, 2]],
               [2, 'vspace', 0, 0, [1, 3]],
               [3, 'if', 0, 0, [2, 4, 7, 8]],
               [4, 'greater2', 0, 0, [3, 5, 6, None]],
               [5, 'keyboard', 0, 0, [4, None]],
               [6, ['number', '0'], 0, 0, [4, None]],
               [7, 'stopstack', 0, 0, [3, None]],
               [8, 'vspace', 0, 0, [3, 9]],
               [9, 'wait', 0, 0, [8, 10, None]],
               [10, ['number', '1'], 0, 0, [9, None]]],
    'picturelist':
              [[0, 'sandwichtop_no_label', 0, 0, [None, 1]],
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
               [17, 'list', 0, 0, [15, 18, 19, 20]],
               [18, ['string', '∙ '], 0, 0, [17, None]],
               [19, ['string', '∙ '], 0, 0, [17, None]],
               [20, 'sandwichbottom', 0, 0, [17, None]]],
    'picture1x1a':
              [[0, 'sandwichtop_no_label', 0, 0, [None, 1]],
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
               [17, 'showaligned', 0, 0, [15, 18, 19]],
               [18, 'journal', 0, 0, [17, None]],
               [19, 'sandwichbottom', 0, 0, [17, None]]],
    'picture2x2':
              [[0, 'sandwichtop_no_label', 0, 0, [None, 1]],
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
               [38, 'showaligned', 0, 0, [37, 39, 40]],
               [39, 'journal', 0, 0, [38, None]],
               [40, 'sandwichbottom', 0, 0, [38, None]]],
    'picture1x2':
              [[0, 'sandwichtop_no_label', 0, 0, [None, 1]],
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
               [38, 'showaligned', 0, 0, [37, 39, 40]],
               [39, 'description', 0, 0, [38, None]],
               [40, 'sandwichbottom', 0, 0, [38, None]]],
    'picture2x1':
              [[0, 'sandwichtop_no_label', 0, 0, [None, 1]],
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
               [38, 'showaligned', 0, 0, [37, 39, 40]],
               [39, 'description', 0, 0, [38, None]],
               [40, 'sandwichbottom', 0, 0, [38, None]]],
    'picture1x1':
              [[0, 'sandwichtop_no_label', 0, 0, [None, 1]],
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
               [26, 'sandwichbottom', 0, 0, [24, None]]],
    'reskin':
              [[0, 'skin', 0, 0, [None, 1, None]],
               [1, 'journal', 0, 0, [0, None]]]}
