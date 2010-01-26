# -*- coding: utf-8 -*-
#Copyright (c) 2009, Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from gettext import gettext as _

#
# sprite layers
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
# block palette categories
#

TURTLE = 0
PEN = 1
NUMBER = 2
FLOW = 3
BLOCKS = 4
EXTRAS = 5
PORTFOLIO = 6
TRASH = 7

PALETTE_NAMES = ['turtle', 'pen', 'number', 'flow', 'blocks', 'extras',
                 'portfolio', 'trash']

PALETTES = [['forward', 'back', 'clean', 'left', 'right', 'show', 
             'setheading', 'setxy', 'heading', 'xcor', 'ycor', 'setscale',
              'arc', 'scale'],
            ['penup','pendown', 'setpensize', 'fillscreen', 'pensize',
             'settextsize', 'setcolor', 'setshade', 'textsize', 'color',
             'shade'],
            ['plus2', 'minus2', 'number', 'product2',
             'division2', 'identity2', 'remainder2', 'sqrt', 
             'random', 'greater', 'less', 'equal', 'not', 'and', 'or'],
            ['wait', 'forever', 'repeat', 'if', 'hspace',
             'vspace', 'stopstack'],
            ['hat1', 'stack1', 'hat', 'hat2', 'stack2', 'stack',
             'storeinbox1', 'storeinbox2', 'string', 'box1', 'box2', 'box',
             'storeinbox', 'start'],
            ['kbinput', 'push', 'printheap', 'keyboard', 'pop', 'clearheap',
             'myfunc',  'nop', 'leftpos', 'toppos', 'width', 'rightpos',
             'bottompos', 'height', 'print'],
            ['hideblocks'],
            []]

#
# block style attributes
#

COLORS = [["#00FF00","#00A000"], ["#00FFFF","#00A0A0"], ["#FF00FF","#A000A0"],
          ["#FFC000","#A08000"], ["#FFFF00","#A0A000"], ["#FF0000","#A0000"],
          ["#0000FF","#0000FF"], ["#000000","#000000"]]


PALETTE_HEIGHT = 175
ICON_SIZE = 55
SELECTED_COLOR = "#0000FF"
SELECTED_STROKE_WIDTH = 1.5
STANDARD_STROKE_WIDTH = 1.0

#
# block style definitions
#
BASIC_STYLE_HEAD = ['start', 'hat1', 'hat2']
BASIC_STYLE_HEAD_1ARG = ['hat']
BASIC_STYLE_TAIL = ['stopstack']
BASIC_STYLE = ['clean', 'penup', 'pendown', 'stack1', 'stack2', 'vspace',
    'hideblocks', 'clearheap', 'printheap', 'kbinput']
BASIC_STYLE_1ARG = ['forward', 'back', 'left', 'right', 'setheading', 'show',
    'setscale', 'setpensize', 'setcolor', 'setshade', 'print',
    'settextsize', 'settextcolor', 'print', 'wait', 'storeinbox1',
    'storeinbox2', 'wait', 'stack', 'push', 'nop']
BASIC_STYLE_2ARG = ['arc', 'setxy', 'fillscreen', 'storeinbox', 'myfunc']
BOX_STYLE = ['number', 'xcor', 'ycor', 'heading', 'pensize', 'color', 'shade',
    'textcolor', 'textsize', 'box1', 'box2', 'string', 'leftpos', 'scale',
    'toppos', 'rightpos', 'bottompos', 'width', 'height', 'pop', 'keyboard']
NUMBER_STYLE = ['plus2', 'product2', 'random']
NUMBER_STYLE_PORCH = ['minus2', 'division2', 'remainder2']
NUMBER_STYLE_1ARG = ['sqrt', 'box', 'identity2']
COMPARE_STYLE = ['greater', 'less', 'equal']
BOOLEAN_STYLE = ['and', 'or']
NOT_STYLE = ['not']
FLOW_STYLE = ['forever', 'hspace']
FLOW_STYLE_1ARG = ['repeat']
FLOW_STYLE_BOOLEAN = ['if']

#
# blocks that contain media
#
CONTENT_BLOCKS = ['number', 'string', 'media', 'audio', 'journal']

#
# block name dictionary
#

BLOCK_NAMES = {'clean':[_('clean')], 'forward':[_('forward')],
    'back':[_('back')],
    'left':[_('left')], 'right':[_('right')], 'setheading':[_('set heading')],
    'show':[_('show')], 'setscale':[_('set scale')], 'xcor':[_('xcor')],
    'ycor':[_('ycor')], 'heading':[_('heading')], 'penup':[_('pen up')],
    'pendown':[_('pen down')], 'setpensize':[_('set pen size')],
    'arc':[_('arc'),_('angle'),_('radius')],
    'settextsize':[_('set text size')], 'setcolor':[_('set color')],
    'setshade':[_('set shade')],
    'fillscreen':[_('fill screen'),_('color'),_('shade')],
    'shade':[_('shade')],
    'pensize':[_('pen size')], 'textsize':[_('text size')],
    'color':[_('color')],
    'plus2':['+'], 'minus2':['–'], 'product2':['×'], 'division2':['/'],
    'remainder2':[_('mod')], 'identity2':['←'],
    'random':[_('random'),_('min'),_('max')], 'sqrt':['√'],
    'less':['<'],'greater':[">"], 'equal':['='], 'and':[_('and')],
    'not':[_('not')], 'print':[_('print')], 'wait':[_('wait')], 'or':[_('or')],
    'forever':[_('forever')], 'repeat':[_('repeat')], 'if':[_('if then')],
    'stopstack':[_('stop action')], 'hspace':[' '], 'vspace':[' '],
    'start':[_('start')], 'hat1':[_('action 1')],
    'stack1':[_('action 1')],
    'hat2':[_('action 2')], 'stack2':[_('action 2')],
    'hat':[_('action')], 'stack':[_('action')], 'number':['100'],
    'storeinbox1':[_('store in box 1')], 'box1':[_('box 1')],
    'storeinbox2':[_('store in box 2')], 'box2':[_('box 2')], 
    'storeinbox':[_('store in')], 'box':[_('box')], 'string':[_('string')], 
    'leftpos':[_('left')], 'toppos':[_('top')], 'rightpos':[_('right')], 
    'bottompos':[_('bottom')], 'width':[_('width')], 'height':[_('height')],
    'hideblocks':[_('hide blocks')],
    'setxy':[_('set xy'), _('x'), _('y')],
    'scale':[_('scale')], 'keyboard':[_('keyboard')],
    'push':[_('push')], 'pop':[_('pop')], 'kbinput':[_('query keyboard')],
    'myfunc':[_('python'), _('code'), _('value')], 'nop':[' '],
    'printheap':[_('show heap')],
    'clearheap':[_('empty heap')]}

#
# Legacy names
#
OLD_NAMES = {'product':'product2',
             'division':'division2', 'plus':'plus2',
             'remainder':'remainder2', 'identity':'identity2',
             'division':'division2', 'if else':'if'}

#
# Logo primitives
#

PRIMITIVES = {'clean':'clean', 'forward':'forward', 'back':'back', 'arc':'arc',
    'left':'left', 'right':'right', 'set heading':'seth', 'scale':'scale',
    'show':'show', 'set scale':'setscale', 'xcor':'xcor', 'setxy':'setxy',
    'ycor':'ycor', 'heading':'heading', 'penup':'penup',
    'pendown':'pendown', 'setpensize':'setpensize',
    'settextsize':'settextsize', 'setcolor':'setcolor',
    'setshade':'setshade', 'fillscreen':'fillscreen', 'shade':'shade',
    'pensize':'pensize', 'textsize':'textsize', 'color':'color',
    'plus2':'plus', 'minus2':'minus', 'product2':'product',
     'division2':'division', 'remainder2':'mod', 'identity2':'id',
    'random':'random', 'sqrt':'sqrt', 'less':'less?',
    'greater':'greater?', 'equal':'equal?', 'and':'and', 'or':'or',
    'not':'not', 'print':'print', 'wait':'wait',
    'forever':'forever', 'repeat':'repeat', 'if':'if', 'ifelse':'ifelse',
    'stopstack':'stopstack', 'hspace':'nop', 'vspace':'nop',
    'start':'start', 'hat1':'nop1', 'stack1':'stack1',
    'hat2':'nop2', 'stack2':'stack2',
    'hat':'nop3', 'action':'stack',
    'storeinbox1':'storeinbox1', 'box1':'box1',
    'storeinbox2':'storeinbox2', 'box2':'box2', 
    'storeinbox':'storeinbox', 'box':'box',
    'leftpos':'leftpos', 'toppos':'toppos', 'rightpos':'rightpos', 
    'bottompos':'bottompos', 'width':'hres', 'height':'vres',
    'hideblocks':'hideblocks', 'push':'push', 'pop':'pop',
    'keyboard':'keyboard', 'kbinput':'kbinput', 'myfunc':'myfunc',
    'nop':'nop', 'printheap':'printheap', 'clearheap':'clearheap'}

#
# block default values
#

DEFAULTS = {'forward':[100], 'back':[100], 'left':[90], 'right':[90], 
    'arc':[90,100], 'setheading':[0], 'setscale':[33], 'show':[_('text')],
    'setpensize':[5], 'settextsize':[32], 'setcolor':[0],
    'setshade':[50], 'fillscreen':[60,80], 'number':[100],
    'random':[0,100], 'wait':[1], 'repeat':[4], 'setxy':[0,0], 
    'storeinbox':[_('my box'),100], 'box':[_('my box')],
    'hat':[_('action')], 'stack':[_('action')], 'nop':[100],
    'storeinbox1':[100], 'storeinbox2':[100], 'myfunc':[_('x'),100]}



#
# Status blocks
#
MEDIA_SHAPES = ['audioon', 'texton', 'journalon', 'descon', 'pythonoff',
                'pythonon']

OVERLAY_SHAPES = ['Cartesian', 'polar']

STATUS_SHAPES = ['status', 'info', 'nostack', 'noinput', 'emptyheap',
                 'emptybox', 'nomedia', 'nocode', 'overflowerror',
                 'syntaxerror']

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
WHITE_SPACE = ['space','Tab','Return']

