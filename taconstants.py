# -*- coding: utf-8 -*-
#Copyright (c) 2010, Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""
This file contains the constants that by-in-large determine the
behavior of Turtle Art. Noteably, the block palettes are defined
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
for the palette-selector buttons. These are kept in the images
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
             'seth', 'setxy', 'heading', 'xcor', 'ycor', 'setscale',
             'arc', 'scale', 'leftpos', 'toppos', 'rightpos',
             'bottompos'],
            ['penup','pendown', 'setpensize', 'fillscreen', 'pensize',
             'settextsize', 'setcolor', 'setshade', 'textsize', 'color',
             'shade'],
            [ 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'],
            ['plus2', 'minus2', 'product2',
             'division2', 'identity2', 'remainder2', 'sqrt', 'random',
             'number', 'greater2', 'less2', 'equal2', 'not', 'and2', 'or2'],
            ['wait', 'forever', 'repeat', 'if', 'ifelse', 'hspace',
             'vspace', 'stopstack'],
            ['hat1', 'stack1', 'hat', 'hat2', 'stack2', 'stack',
             'storeinbox1', 'storeinbox2', 'string', 'box1', 'box2', 'box',
             'storein', 'start'],
            ['kbinput', 'push', 'printheap', 'keyboard', 'pop', 'clearheap',
             'myfunc',  'nop', 'sandwichtop', 'sandwichbottom',
             'addturtle', 'print', 'comment', 'width', 'height'],
            ['journal', 'audio', 'description', 'savepix', 'hideblocks',
             'showblocks', 'fullscreen', 'picturelist', 'picture1x1a',
             'picture1x1', 'picture2x2', 'picture2x1', 'picture1x2'],
            ['empty', 'restoreall']]

#
# Block-style attributes
#

COLORS = [["#00FF00","#00A000"], ["#00FFFF","#00A0A0"], ["#00FFFF","#00A0A0"],
          ["#FF00FF","#A000A0"], ["#FFC000","#A08000"], ["#FFFF00","#A0A000"],
          ["#FF0000","#A00000"], ["#0000FF","#0000A0"], ["#FFFF00","#A0A000"]]

BOX_COLORS = {'red':["#FF0000","#A00000"],'orange':["#FFD000","#AA8000"],
              'yellow':["#FFFF00","#A0A000"],'green':["#00FF00","#008000"],
              'cyan':["#00FFFF","#00A0A0"],'blue':["#0000FF","#000080"],
              'purple':["#FF00FF","#A000A0"]}

PALETTE_HEIGHT = 120
PALETTE_WIDTH = 175
SELECTOR_WIDTH = 55
ICON_SIZE = 55
SELECTED_COLOR = "#0000FF"
SELECTED_STROKE_WIDTH = 1.0
STANDARD_STROKE_WIDTH = 1.0
BLOCK_SCALE = 2.0
PALETTE_SCALE = 1.5

#
# Block-style definitions
#
BASIC_STYLE_HEAD = ['start', 'hat1', 'hat2', 'restore', 'restoreall']
BASIC_STYLE_HEAD_1ARG = ['hat']
BASIC_STYLE_TAIL = ['stopstack', 'empty']
BASIC_STYLE = ['clean', 'penup', 'pendown', 'stack1', 'stack2', 'vspace',
    'hideblocks', 'showblocks', 'clearheap', 'printheap', 'kbinput',
    'fullscreen', 'sandwichcollapsed']
BASIC_STYLE_EXTENDED = ['picturelist', 'picture1x1', 'picture2x2',
    'picture2x1', 'picture1x2', 'picture1x1a']
BASIC_STYLE_1ARG = ['forward', 'back', 'left', 'right', 'seth', 'show',
    'setscale', 'setpensize', 'setcolor', 'setshade', 'print', 'showaligned',
    'settextsize', 'settextcolor', 'print', 'wait', 'storeinbox1', 'savepix',
    'storeinbox2', 'wait', 'stack', 'push', 'nop', 'addturtle', 'comment']
BASIC_STYLE_2ARG = ['arc', 'setxy', 'fillscreen', 'storein', 'write']
BOX_STYLE = ['number', 'xcor', 'ycor', 'heading', 'pensize', 'color', 'shade',
    'textcolor', 'textsize', 'box1', 'box2', 'string', 'leftpos', 'scale',
    'toppos', 'rightpos', 'bottompos', 'width', 'height', 'pop', 'keyboard',
    'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple',
    'titlex', 'titley', 'leftx', 'topy', 'rightx', 'bottomy']
BOX_STYLE_MEDIA =  ['description', 'audio', 'journal']
NUMBER_STYLE = ['plus2', 'product2']
NUMBER_STYLE_VAR_ARG = ['myfunc']
NUMBER_STYLE_BLOCK = ['random']
NUMBER_STYLE_PORCH = ['minus2', 'division2', 'remainder2']
NUMBER_STYLE_1ARG = ['sqrt', 'identity2']
NUMBER_STYLE_1STRARG = ['box']
COMPARE_STYLE = ['greater2', 'less2', 'equal2']
BOOLEAN_STYLE = ['and2', 'or2']
NOT_STYLE = ['not']
FLOW_STYLE = ['forever', 'hspace']
FLOW_STYLE_1ARG = ['repeat']
FLOW_STYLE_BOOLEAN = ['if']
FLOW_STYLE_ELSE = ['ifelse']
COLLAPSIBLE_TOP = ['sandwichtop']
COLLAPSIBLE_BOTTOM = ['sandwichbottom']

# Depreciated block styles
PORTFOLIO_STYLE_2x2 = ['template2x2']
BULLET_STYLE = ['templatelist', 'list']
PORTFOLIO_STYLE_1x1 = ['template1x1', 'template1x1a']
PORTFOLIO_STYLE_2x1 = ['template2x1']
PORTFOLIO_STYLE_1x2 = ['template1x2']


#
# Macros (groups of blocks)
#
MACROS = {
    'kbinput':[[0, 'forever', 0, 0, [None, 1, None]],
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
              [[0, 'sandwichtop', 0, 0, [None, 1, 2]],
               [1, ['string', _('bulleted list')], 0, 0, [0, None]],
               [2, 'setxy', 0, 0, [0, 3, 4, 5]],
               [3, 'titlex', 0, 0, [2, None]],
               [4, 'titley', 0, 0, [2, None]],
               [5, 'show', 0, 0, [2, 6, 7]],
               [6, ['string',_('Title')], 0, 0, [5, None]],
               [7, 'setxy', 0, 0, [5, 8, 9, 10]],
               [8, 'leftx', 0, 0, [7, None]],
               [9, 'topy', 0, 0, [7, None]],
               [10, 'list', 0, 0, [7, 11, 12, 13]],
               [11, ['string','∙ '], 0, 0, [10, None]],
               [12, ['string','∙ '], 0, 0, [10, None]],
               [13, 'sandwichbottom', 0, 0, [10, None]]],
    'picture1x1a':
              [[0, 'sandwichtop', 0, 0, [None, 1, 2]],
               [1, ['string', _('picture')], 0, 0, [0, None]],
               [2, 'setxy', 0, 0, [0, 3, 4, 5]],
               [3, 'titlex', 0, 0, [2, None]],
               [4, 'titley', 0, 0, [2, None]],
               [5, 'show', 0, 0, [2, 6, 7]],
               [6, ['string',_('Title')], 0, 0, [5, None]],
               [7, 'setscale', 0, 0, [5, 8, 9]],
               [8, ['number', '90'], 0, 0, [7, None]],
               [9, 'setxy', 0, 0, [7, 10, 11, 12]],
               [10, 'leftx', 0, 0, [9, None]],
               [11, 'topy', 0, 0, [9, None]],
               [12, 'showaligned', 0, 0, [9, 13, 14]],
               [13, 'journal', 0, 0, [12, None]],
               [14, 'sandwichbottom', 0, 0, [12, None]]],
    'picture2x2':
              [[0, 'sandwichtop', 0, 0, [None, 1, 2]],
               [1, ['string', _('2×2 pictures')], 0, 0, [0, None]],
               [2, 'setxy', 0, 0, [0, 3, 4, 5]],
               [3, 'titlex', 0, 0, [2, None]],
               [4, 'titley', 0, 0, [2, None]],
               [5, 'show', 0, 0, [2, 6, 7]],
               [6, ['string',_('Title')], 0, 0, [5, None]],
               [7, 'setscale', 0, 0, [5, 8, 9]],
               [8, ['number', '45'], 0, 0, [7, None]],
               [9, 'setxy', 0, 0, [7, 10, 11, 12]],
               [10, 'leftx', 0, 0, [9, None]],
               [11, 'topy', 0, 0, [9, None]],
               [12, 'showaligned', 0, 0, [9, 13, 14]],
               [13, 'journal', 0, 0, [12, None]],
               [14, 'setxy', 0, 0, [12, 15, 16, 17]],
               [15, 'rightx', 0, 0, [14, None]],
               [16, 'topy', 0, 0, [14, None]],
               [17, 'showaligned', 0, 0, [14, 18, 19]],
               [18, 'journal', 0, 0, [17, None]],
               [19, 'setxy', 0, 0, [17, 20, 21, 22]],
               [20, 'leftx', 0, 0, [19, None]],
               [21, 'bottomy', 0, 0, [19, None]],
               [22, 'showaligned', 0, 0, [19, 23, 24]],
               [23, 'journal', 0, 0, [22, None]],
               [24, 'setxy', 0, 0, [22, 25, 26, 27]],
               [25, 'rightx', 0, 0, [24, None]],
               [26, 'bottomy', 0, 0, [24, None]],
               [27, 'showaligned', 0, 0, [24, 28, 29]],
               [28, 'journal', 0, 0, [27, None]],
               [29, 'sandwichbottom', 0, 0, [27, None]]],
    'picture2x1':
              [[0, 'sandwichtop', 0, 0, [None, 1, 2]],
               [1, ['string', _('2×1 pictures')], 0, 0, [0, None]],
               [2, 'setxy', 0, 0, [0, 3, 4, 5]],
               [3, 'titlex', 0, 0, [2, None]],
               [4, 'titley', 0, 0, [2, None]],
               [5, 'show', 0, 0, [2, 6, 7]],
               [6, ['string',_('Title')], 0, 0, [5, None]],
               [7, 'setscale', 0, 0, [5, 8, 9]],
               [8, ['number', '45'], 0, 0, [7, None]],
               [9, 'setxy', 0, 0, [7, 10, 11, 12]],
               [10, 'leftx', 0, 0, [9, None]],
               [11, 'topy', 0, 0, [9, None]],
               [12, 'showaligned', 0, 0, [9, 13, 14]],
               [13, 'journal', 0, 0, [12, None]],
               [14, 'setxy', 0, 0, [12, 15, 16, 17]],
               [15, 'rightx', 0, 0, [14, None]],
               [16, 'topy', 0, 0, [14, None]],
               [17, 'showaligned', 0, 0, [14, 18, 19]],
               [18, 'journal', 0, 0, [17, None]],
               [19, 'setxy', 0, 0, [17, 20, 21, 22]],
               [20, 'leftx', 0, 0, [19, None]],
               [21, 'bottomy', 0, 0, [19, None]],
               [22, 'showaligned', 0, 0, [19, 23, 24]],
               [23, 'description', 0, 0, [22, None]],
               [24, 'setxy', 0, 0, [22, 25, 26, 27]],
               [25, 'rightx', 0, 0, [24, None]],
               [26, 'bottomy', 0, 0, [24, None]],
               [27, 'showaligned', 0, 0, [24, 28, 29]],
               [28, 'description', 0, 0, [27, None]],
               [29, 'sandwichbottom', 0, 0, [27, None]]],
    'picture1x2':
              [[0, 'sandwichtop', 0, 0, [None, 1, 2]],
               [1, ['string', _('1×2 pictures')], 0, 0, [0, None]],
               [2, 'setxy', 0, 0, [0, 3, 4, 5]],
               [3, 'titlex', 0, 0, [2, None]],
               [4, 'titley', 0, 0, [2, None]],
               [5, 'show', 0, 0, [2, 6, 7]],
               [6, ['string',_('Title')], 0, 0, [5, None]],
               [7, 'setscale', 0, 0, [5, 8, 9]],
               [8, ['number', '45'], 0, 0, [7, None]],
               [9, 'setxy', 0, 0, [7, 10, 11, 12]],
               [10, 'leftx', 0, 0, [9, None]],
               [11, 'topy', 0, 0, [9, None]],
               [12, 'showaligned', 0, 0, [9, 13, 14]],
               [13, 'journal', 0, 0, [12, None]],
               [14, 'setxy', 0, 0, [12, 15, 16, 17]],
               [15, 'rightx', 0, 0, [14, None]],
               [16, 'topy', 0, 0, [14, None]],
               [17, 'showaligned', 0, 0, [14, 18, 19]],
               [18, 'description', 0, 0, [17, None]],
               [19, 'setxy', 0, 0, [17, 20, 21, 22]],
               [20, 'leftx', 0, 0, [19, None]],
               [21, 'bottomy', 0, 0, [19, None]],
               [22, 'showaligned', 0, 0, [19, 23, 24]],
               [23, 'journal', 0, 0, [22, None]],
               [24, 'setxy', 0, 0, [22, 25, 26, 27]],
               [25, 'rightx', 0, 0, [24, None]],
               [26, 'bottomy', 0, 0, [24, None]],
               [27, 'showaligned', 0, 0, [24, 28, 29]],
               [28, 'description', 0, 0, [27, None]],
               [29, 'sandwichbottom', 0, 0, [27, None]]],
    'picture1x1':
              [[0, 'sandwichtop', 0, 0, [None, 1, 2]],
               [1, ['string', _('1×1 picture')], 0, 0, [0, None]],
               [2, 'setxy', 0, 0, [0, 3, 4, 5]],
               [3, 'titlex', 0, 0, [2, None]],
               [4, 'titley', 0, 0, [2, None]],
               [5, 'show', 0, 0, [2, 6, 7]],
               [6, ['string',_('Title')], 0, 0, [5, None]],
               [7, 'setscale', 0, 0, [5, 8, 9]],
               [8, ['number', '45'], 0, 0, [7, None]],
               [9, 'setxy', 0, 0, [7, 10, 11, 12]],
               [10, 'leftx', 0, 0, [9, None]],
               [11, 'topy', 0, 0, [9, None]],
               [12, 'showaligned', 0, 0, [9, 13, 14]],
               [13, 'journal', 0, 0, [12, None]],
               [14, 'setxy', 0, 0, [12, 15, 16, 17]],
               [15, 'rightx', 0, 0, [14, None]],
               [16, 'topy', 0, 0, [14, None]],
               [17, 'showaligned', 0, 0, [14, 18, 19]],
               [18, 'description', 0, 0, [17, None]],
               [19, 'sandwichbottom', 0, 0, [17, None]]]
         }

#
# Blocks that are expandable
#
EXPANDABLE = ['vspace', 'hspace', 'templatelist', 'list', 'identity2', 'myfunc']

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
# Block-name dictionary used for labels
#
BLOCK_NAMES = {
    'addturtle':[_('turtle')],
    'and2':[_('and')],
    'arc':[_('arc'),_('angle'),_('radius')],
    'audio':[' '],
    'back':[_('back')],
    'blue':[_('blue')],
    'bottompos':[_('bottom')],
    'bottomy':[_('picture bottom')],
    'box':[_('box')],
    'box1':[_('box 1')],
    'box2':[_('box 2')],
    'clean':[_(' clean ')],
    'clearheap':[_('empty heap')],
    'color':[_('color')],
    'comment':[_('comment')],
    'cyan':[_('cyan')],
    'division2':['/'],
    'empty':[_('empty trash')],
    'equal2':['='],
    'fillscreen':[_('fill screen'),_('color'),_('shade')],
    'forever':[_('forever')],
    'forward':[_('forward')],
    'fullscreen':[_('full screen')],
    'greater2':[">"],
    'green':[_('green')],
    'hat':[_('action')],
    'hat1':[_('action 1')],
    'hat2':[_('action 2')],
    'heading':[_('heading')],
    'height':[_('height')],
    'hideblocks':[_('hide blocks')],
    'hspace':[' '],
    'identity2':['←'],
    'if':[' ',_('if'),_('then')],
    'ifelse':[' ',_('if'),_('then else')],
    'journal':[' '],
    'kbinput':[_('query keyboard')],
    'keyboard':[_('keyboard')],
    'left':[_('left')],
    'leftpos':[_('left')],
    'leftx':[_('picture left')],
    'less2':['<'],
    'list':['list'],
    'minus2':['–'],
    'myfunc':[_('Python'),'f(x)','x'],
    'nop':[_(' ')],
    'not':[_('not')],
    'number':['100'],
    'orange':[_('orange')],
    'or2':[_('or')],
    'pendown':[_('pen down')],
    'pensize':[_('pen size')],
    'penup':[_('pen up')],
    'picturelist':[' '],
    'picture1x1':[' '],
    'picture1x1a':[' '],
    'picture2x2':[' '],
    'picture2x1':[' '],
    'picture1x2':[' '],
    'plus2':['+'],
    'pop':[_('pop')],
    'printheap':[_('show heap')],
    'print':[_('print')],
    'product2':['×'],
    'purple':[_('purple')],
    'push':[_('push')],
    'random':[_('random'),_('min'),_('max')],
    'red':[_('red')],
    'remainder2':[_('mod')],
    'repeat':[' ',_('repeat')],
    'restore':[_('restore last')],
    'restoreall':[_('restore all')],
    'right':[_('right')],
    'rightpos':[_('right')],
    'rightx':[_('picture right')],
    'savepix':[_('save picture')],
    'scale':[_('scale')],
    'sandwichbottom':[''],
    'sandwichcollapsed':[_('click to open')],
    'sandwichtop':['top of stack'],
    'setcolor':[_('set color')],
    'seth':[_('set heading')],
    'setpensize':[_('set pen size')],
    'setscale':[_('set scale')],
    'setshade':[_('set shade')],
    'settextcolor':[_('set text color')],
    'settextsize':[_('set text size')],
    'setxy':[_('set xy'),_('x'),_('y')],
    'shade':[_('shade')],
    'show':[_('show')],
    'showblocks':[_('show blocks')],
    'showaligned':[_('show aligned')],
    'sqrt':['√'],
    'stack':[_('action')],
    'stack1':[_('action 1')],
    'stack2':[_('action 2')],
    'start':[_('start')],
    'stopstack':[_('stop action')],
    'storein':[_('store in'),_('box'),_('value')],
    'storeinbox1':[_('store in box 1')],
    'storeinbox2':[_('store in box 2')],
    'string':[_('text')],
    'template1x1':[' '],
    'template1x1a':[' '],
    'template1x2':[' '],
    'template2x1':[' '],
    'template2x2':[' '],
    'templatelist':[' '],
    'textsize':[_('text size')],
    'titlex':[_('title x')],
    'titley':[_('title y')],
    'toppos':[_('top')],
    'topy':[_('picture top')],
    'turtle':[_('turtle')],
    'vspace':[' '],
    'wait':[_('wait')],
    'width':[_('width')],
    'xcor':[_('xcor')],
    'ycor':[_('ycor')],
    'yellow':[_('yellow')]}

#
# Logo primitives
#

PRIMITIVES = {
    'addturtle':'turtle',
    'and2':'and',
    'arc':'arc',
    'back':'back',
    'blue':'blue',
    'bottompos':'bpos',
    'bottomy':'boty',
    'box1':'box1',
    'box2':'box2',
    'box':'box',
    'clean':'clean',
    'clearheap':'clearheap',
    'color':'color',
    'comment':'comment',
    'cyan':'cyan',
    'division2':'division',
    'equal2':'equal?',
    'fillscreen':'fillscreen',
    'forever':'forever',
    'forward':'forward',
    'fullscreen':'fullscreen',
    'greater2':'greater?',
    'green':'green',
    'hat':'nop3',
    'hat1':'nop1',
    'hat2':'nop2',
    'heading':'heading',
    'height':'vres',
    'hideblocks':'hideblocks',
    'hspace':'nop',
    'identity2':'id',
    'if':'if',
    'ifelse':'ifelse',
    'kbinput':'kbinput',
    'keyboard':'keyboard',
    'left':'left',
    'leftpos':'lpos',
    'leftx':'leftx',
    'less2':'less?',
    'list':'bulletlist',
    'minus2':'minus',
    'myfunc':'myfunc',
    'nop':'userdefined',
    'not':'not',
    'orange':'orange',
    'or2':'or',
    'pendown':'pendown',
    'pensize':'pensize',
    'penup':'penup',
    'plus2':'plus',
    'pop':'pop',
    'printheap':'printheap',
    'print':'print',
    'product2':'product',
    'purple':'purple',
    'push':'push',
    'random':'random',
    'red':'red',
    'remainder2':'mod',
    'repeat':'repeat',
    'right':'right',
    'rightpos':'rpos',
    'rightx':'rightx',
    'sandwichtop':'comment',
    'sandwichbottom':'nop',
    'sandwichcollapsed':'nop',
    'savepix':'savepix',
    'scale':'scale',
    'setcolor':'setcolor',
    'seth':'seth',
    'setpensize':'setpensize',
    'setscale':'setscale',
    'setshade':'setshade',
    'settextsize':'settextsize',
    'settextcolor':'settextcolor',
    'setxy':'setxy',
    'shade':'shade',
    'show':'show',
    'showblocks':'showblocks',
    'showaligned':'showaligned',
    'sqrt':'sqrt',
    'stack':'stack',
    'stack1':'stack1',
    'stack2':'stack2',
    'start':'start',
    'stopstack':'stopstack',
    'storein':'storeinbox',
    'storeinbox1':'storeinbox1',
    'storeinbox2':'storeinbox2',
    'template1x1':'t1x1',
    'template1x1a':'t1x1a',
    'template1x2':'t1x2',
    'template2x1':'t2x1',
    'template2x2':'t2x2',
    'templatelist':'bullet',
    'textsize':'textsize',
    'titlex':'titlex',
    'titley':'titley',
    'toppos':'tpos',
    'topy':'topy',
    'vspace':'nop',
    'wait':'wait',
    'width':'hres',
    'write':'write',
    'xcor':'xcor',
    'ycor':'ycor',
    'yellow':'yellow'}

#
# block default values
#

DEFAULTS = {
    'addturtle':[1],
    'arc':[90, 100],
    'audio':[None],
    'back':[100],
    'box':[_('my box')],
    'comment':[_('comment')],
    'description':[None],
    'fillscreen':[60, 80],
    'forward':[100],
    'hat':[_('action')],
    'if':[None, None, 'vspace'],
    'ifelse':[None, 'vspace', None, 'vspace'],
    'journal':[None],
    'left':[90],
    'list':['∙ ', '∙ '],
    'media':[None],
    'myfunc':[_('x'), 100],
    'nop':[100],
    'number':[100],
    'random':[0, 100],
    'repeat':[4, None, 'vspace'],
    'right':[90],
    'sandwichtop':[_('label')],
    'savepix':[_('picture name')],
    'setcolor':[0],
    'seth':[0],
    'setpensize':[5],
    'setscale':[33],
    'setshade':[50],
    'settextsize':[32],
    'settextcolor':[0],
    'setxy':[0, 0],
    'show':[_('text')],
    'showaligned':[_('text')],
    'stack':[_('action')],
    'storeinbox1':[100],
    'storeinbox2':[100],
    'storein':[_('my box'), 100],
    'string':[_('text')],
    'template1x1':[_('Title'), 'None'],
    'template1x1a':[_('Title'), 'None'],
    'template1x2':[_('Title'), 'None', 'None'],
    'template2x1':[_('Title'), 'None', 'None'],
    'template2x2':[_('Title'), 'None', 'None', 'None', 'None'],
    'templatelist':[_('Title'), '∙ '],
    'wait':[1],
    'write':[_('text'), 32]}

#
# Blocks that can interchange strings and numbers for their arguments
#
STRING_OR_NUMBER_ARGS = ['plus2', 'equal2', 'less2', 'greater2', 'box',
                         'template1x1', 'template1x2', 'template2x1', 'list',
                         'template2x2', 'template1x1a', 'templatelist', 'nop',
                         'print', 'stack', 'hat', 'addturtle']

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
                 'emptybox', 'nomedia', 'nocode', 'overflowerror',
                 'syntaxerror', 'nofile', 'nojournal']

#
# Legacy names
#
OLD_NAMES = {'product':'product2', 'storeinbox':'storein', 'minus':'minus2',
             'division':'division2', 'plus':'plus2', 'and':'and2', 'or':'or2',
             'less':'less2', 'greater':'greater2', 'equal':'equal2',
             'remainder':'remainder2', 'identity':'identity2',
             'division':'division2', 'audiooff':'audio',
             'descriptionoff':'description','template3':'templatelist',
             'template1':'template1x1', 'template2':'template2x1',
             'template6':'template1x2', 'template7':'template2x2', 
             'template4':'template1x1a', 'hres':'width', 'vres':'height' }

#
# Define the relative size and postion of media objects
#                    (w,   h,   x,      y,     dx, dy)
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
    'audio':_('audio'),
    'division2':_('divide'),
    'equal2':_('equal'),
    'greater2':_('greater than'),
    'hspace':_('horizontal space'),
    'identity2':_('identity'),
    'if':_('if then'),
    'ifelse':_('if then else'),
    'journal':_('journal'),
    'less2':_('less than'),
    'minus2':_('minus'),
    'myfunc':_('Python code'),
    'nop':_('Python code'),
    'number':_('number'),
    'plus2':_('plus'),
    'product2':_('multiply'),
    'sqrt':_('square root'),
    'template1x1':_('presentation 1x1'),
    'template1x1a':_('presentation 1x1'),
    'template1x2':_('presentation 1x2'),
    'template2x1':_('presentation 2x1'),
    'template2x2':_('presentation 2x2'),
    'templatelist':_('presentation bulleted list'),
    'textsize':_('text size'),
    'vspace':_('vertical space')}

#
# Help messages
#
HELP_STRINGS = {
    'addturtle':_("chooses which turtle to command"),
    'and2':_("logical AND operator"),
    'arc':_("moves turtle along an arc"),
    'audio':_("Sugar Journal audio object"),
    'back':_("moves turtle backward"),
    'blocks':_("palette of variable blocks"),
    'bottompos':_("ycor of bottom of screen"),
    'box1':_("Variable 1 (numeric value)"),
    'box2':_("Variable 2 (numeric value)"),
    'box':_("named variable (numeric value)"),
    'clean':_("clears the screen and reset the turtle"),
    'clearheap':_("emptys FILO (first-in-last-out heap)"),
    'color':_("holds current pen color (can be used in place of a number block)"),
    'colors':_("a palette of pen colors"),
    'comment':_("places a comment in your code"),
    'description':_("Sugar Journal description field"),
    'division2':_("divides top numeric input (numerator) by bottom numeric input (denominator)"),
    'empty':_("permanently deletes items in trash"),
    'equal2':_("logical equal-to operator"),
    'extras':_("palette of extra options"),
    'fillscreen':_("fills the background with (color, shade)"),
    'flow':_("palette of flow operators"),
    'forever':_("loops forever"),
    'forward':_("moves turtle forward"),
    'fullscreen':_("hides the Sugar toolbars"),
    'greater2':_("logical greater-than operator"),
    'hat1':_("top of Action 1 stack"),
    'hat2':_("top of Action 2 stack"),
    'hat':_("top of nameable action stack"),
    'heading':_("holds current heading value of the turtle (can be used in place of a number block)"),
    'hideblocks':_("declutters canvas by hiding blocks"),
    'width':_("the canvas width"),
    'hspace':_("jogs stack right"),
    'identity2':_("identity operator used for extending blocks"),
    'ifelse':_("if-then-else operator that uses boolean operators from Numbers palette"),
    'if':_("if-then operator that uses boolean operators from Numbers palette"),
    'journal':_("Sugar Journal media object"),
    'kbinput':_("query for keyboard input (results stored in keyboard block)"),
    'keyboard':_("holds results of query-keyboard block"),
    'leftpos':_("xcor of left of screen"),
    'left':_("turns turtle counterclockwise (angle in degrees)"),
    'less2':_("logical less-than operator"),
    'minus2':_("subtracts bottom numeric input from top numeric input"),
    'myfunc':_("a programmable block: used to add advanced math equations, e.g., sin(x)"),
    'nop':_("runs code found in the tamyblock.py module found in the Journal"),
    'not':_("logical NOT operator"),
    'numbers':_("palette of numeric operators"),
    'number':_("used as numeric input in mathematic operators"),
    'or':_("logical OR operator"),
    'orientation':_("changes the orientation of the palette of blocks"),
    'pendown':_("Turtle will draw when moved."),
    'pen':_("palette of pen commands"),
    'pensize':_("holds current pen size (can be used in place of a number block)"),
    'penup':_("Turtle will not draw when moved."),
    'picture1x1':_("presentation template: select Journal object (with description)"),
    'picture1x1a':_("presentation template: select Journal object (no description)"),
    'picture1x2':_("presentation template: select two Journal objects"),
    'picture2x1':_("presentation template: select two Journal objects"),
    'picture2x2':_("presentation template: select four Journal objects"),
    'picturelist':_("presentation template: list of bullets"),
    'plus2':_("adds two alphanumeric inputs"),
    'pop':_("pops value off FILO (first-in last-out heap)"),
    'portfolio':_("palette of presentation templates"),
    'print':_("prints value in status block at bottom of the screen"),
    'printheap':_("shows values in FILO (first-in last-out heap)"),
    'product2':_("multiplies two numeric inputs"),
    'push':_("pushes value onto FILO (first-in last-out heap)"),
    'random':_("returns random number between minimum (top) and maximum (bottom) values"),
    'remainder2':_("modular (remainder) operator"),
    'repeat':_("loops specified number of times"),
    'restore':_("restores most recent blocks from trash"),
    'restoreall':_("restore all blocks from trash"),
    'rightpos':_("xcor of right of screen"),
    'right':_("turns turtle clockwise (angle in degrees)"),
    'savepix':_("saves a picture to the Sugar Journal"),
    'scale':_("holds current scale value"),
    'setcolor':_("sets color of the line drawn by the turtle"),
    'seth':_("sets the heading of the turtle (0 is towards the top of the screen.)"),
    'setpensize':_("sets size of the line drawn by the turtle"),
    'setscale':_("sets the scale of media"),
    'setshade':_("sets shade of the line drawn by the turtle"),
    'settextcolor':_("sets color of text drawn by the turtle"),
    'settextsize':_("sets size of text drawn by turtle"),
    'setxy':_("moves turtle to position xcor, ycor; (0, 0) is in the center of the screen."),
    'shade':_("holds current pen shade"),
    'show':_("draws text or show media from the Journal"),
    'showblocks':_("restores hidden blocks"),
    'sqrt':_("calculates square root"),
    'stack1':_("invokes Action 1 stack"),
    'stack2':_("invokes Action 2 stack"),
    'stack':_("invokes named action stack"),
    'start':_("connects action to toolbar run buttons"),
    'stopstack':_("stops current action"),
    'storeinbox1':_("stores numeric value in Variable 1"),
    'storeinbox2':_("stores numeric value in Variable 2"),
    'storein':_("stores numeric value in named variable"),
    'string':_("string value"),
    'template1x1':_("presentation template: select Journal object (with description)"),
    'template1x1a':_("presentation template: select Journal object (no description)"),
    'template1x2':_("presentation template: select two Journal objects"),
    'template2x1':_("presentation template: select two Journal objects"),
    'template2x2':_("presentation template: select four Journal objects"),
    'templatelist':_("presentation template: list of bullets"),
    'textcolor':_("holds current text color (can be used in place of a number block)"),
    'textsize':_("holds current text size (can be used in place of a number block)"),
    'toppos':_("ycor of top of screen"),
    'trash':_("a place to throw away blocks"),
    'turtle':_("palette of turtle commands"),
    'height':_("the canvas height"),
    'vspace':_("jogs stack down"),
    'wait':_("pauses program execution a specified number of seconds"),
    'xcor':_("holds current x-coordinate value of the turtle (can be used in place of a number block)"),
    'ycor':_("holds current y-coordinate value of the turtle (can be used in place of a number block)")}


#
# 'dead key' Unicode dictionaries
#

DEAD_KEYS = ['grave','acute','circumflex','tilde','diaeresis','abovering']
DEAD_DICTS = [{'A':192,'E':200,'I':204,'O':210,'U':217,'a':224,'e':232,'i':236,
               'o':242,'u':249},
              {'A':193,'E':201,'I':205,'O':211,'U':218,'a':225,'e':233,'i':237,
               'o':243,'u':250},
              {'A':194,'E':202,'I':206,'O':212,'U':219,'a':226,'e':234,
               'i':238,'o':244,'u':251},
              {'A':195,'O':211,'N':209,'U':360,'a':227,'o':245,'n':241,'u':361},
              {'A':196,'E':203,'I':207,'O':211,'U':218,'a':228,'e':235,
               'i':239,'o':245,'u':252},
              {'A':197,'a':229}]
NOISE_KEYS = ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock', 'Pause',
              'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift', 'KP_Divide',
              'Escape', 'Return', 'KP_Page_Up', 'Up', 'Down', 'Menu',
              'Left', 'Right', 'KP_Home', 'KP_End', 'KP_Up', 'Super_L',
              'KP_Down', 'KP_Left', 'KP_Right', 'KP_Page_Down', 'Scroll_Lock',
              'Page_Down', 'Page_Up']
WHITE_SPACE = ['space','Tab']

CURSOR = '█'
