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

PALETTE_NAMES = ['turtle', 'pen', 'number', 'flow', 'blocks', 'extras',
                 'portfolio']

PALETTES = [['clean', 'forward', 'back', 'left', 'right', 'arc', 'set xy',
     'show', 'set scale', 'set heading', 'scale', 'xcor', 'ycor', 'heading'],
    ['pen up','pen down', 'set pen size', 'set text size',
     'set color', 'set shade', 'fill screen', 'pen size', 'text size', 'color',
     'shade'],
    ['number', 'plus', 'minus', 'multiply',
     'divide', 'mod', 'square root', 'random', 'greater than', 'less than',
     'equal to', 'and', 'or', 'not'],
    ['wait', 'forever', 'repeat', 'if then', 'stop action', 'hspace',
     'vspace'],
    ['start', 'def action 1', 'action 1', 'def action 2', 
     'action 2', 'def action', 'action', 'store in box 1', 'box 1',
     'store in box 2', 'box 2', 'store in', 'box', 'string'],
    ['print', 'left pos', 'top pos', 'right pos', 'bottom pos', 'width', 
     'height'],
    ['hide blocks']]

#
# block style attributes
#

COLORS = [["#00FF00","#00A000"], ["#00FFFF","#00A0A0"], ["#FF00FF","#A000A0"],
          ["#FFC000","#A08000"], ["#FFFF00","#A0A000"], ["#FF0000","#A0000"],
          ["#0000FF","#0000FF"]]


PALETTE_HEIGHT = 175
ICON_SIZE = 55
SELECTED_COLOR = "#0000FF"
SELECTED_STROKE_WIDTH = 1.5
STANDARD_STROKE_WIDTH = 1.0

#
# block style definitions
#
BASIC_STYLE_HEAD = ['start', 'def action 1', 'def action 2']
BASIC_STYLE_HEAD_1ARG = ['def action']
BASIC_STYLE_TAIL = ['stop action']
BASIC_STYLE = ['clean', 'pen up', 'pen down', 'action 1', 'action 2', 'vspace',
    'hide blocks']
BASIC_STYLE_1ARG = ['forward', 'back', 'left', 'right', 'set heading', 'show',
    'set scale', 'set pen size', 'set color', 'set shade', 'print',
    'set text size', 'set text color', 'print', 'wait', 'store in box 1',
    'store in box 2', 'wait', 'action']
BASIC_STYLE_2ARG = ['arc', 'set xy', 'fill screen', 'store in']
BOX_STYLE = ['number', 'xcor', 'ycor', 'heading', 'pen size', 'color', 'shade',
    'text color', 'text size', 'box 1', 'box 2', 'string', 'left pos', 'scale',
    'top pos', 'right pos', 'bottom pos', 'width', 'height']
NUMBER_STYLE = ['plus', 'multiply', 'random']
NUMBER_STYLE_PORCH = ['minus', 'divide', 'mod']
NUMBER_STYLE_1ARG = ['square root', 'box']
COMPARE_STYLE = ['greater than', 'less than', 'equal to']
BOOLEAN_STYLE = ['and', 'or']
NOT_STYLE = ['not']
FLOW_STYLE = ['forever', 'hspace']
FLOW_STYLE_1ARG = ['repeat']
FLOW_STYLE_BOOLEAN = ['if then']

#
# blocks that contain media
#
CONTENT_BLOCKS = ['number', 'string', 'media', 'audio', 'journal']

#
# block name dictionary
#

BLOCK_NAMES = {'clean':[_('clean')], 'forward':[_('forward')],
    'back':[_('back')],
    'left':[_('left')], 'right':[_('right')], 'set heading':[_('set heading')],
    'show':[_('show')], 'set scale':[_('set scale')], 'xcor':[_('xcor')],
    'ycor':[_('ycor')], 'heading':[_('heading')], 'pen up':[_('pen up')],
    'pen down':[_('pen down')], 'set pen size':[_('set pen size')],
    'arc':[_('arc'),_('angle'),_('radius')],
    'set text size':[_('set text size')], 'set color':[_('set color')],
    'set shade':[_('set shade')],
    'fill screen':[_('fill screen'),_('color'),_('shade')],
    'shade':[_('shade')],
    'pen size':[_('pen size')], 'text size':[_('text size')],
    'color':[_('color')],
    'plus':['+'], 'minus':['–'], 'multiply':['×'], 'divide':['/'],
    'mod':[_('mod')], 
    'random':[_('random'),_('min'),_('max')], 'square root':['√'],
    'less than':['<'],
    'greater than':[">"], 'equal to':['='], 'and':[_('and')], 'or':[_('or')],
    'not':[_('not')], 'print':[_('print')], 'wait':[_('wait')],
    'forever':[_('forever')], 'repeat':[_('repeat')], 'if then':[_('if then')],
    'stop action':[_('stop action')], 'hspace':[' '], 'vspace':[' '],
    'start':[_('start')], 'def action 1':[_('action 1')],
    'action 1':[_('action 1')],
    'def action 2':[_('action 2')], 'action 2':[_('action 2')],
    'def action':[_('action')], 'action':[_('action')], 'number':['100'],
    'store in box 1':[_('store in box 1')], 'box 1':[_('box 1')],
    'store in box 2':[_('store in box 2')], 'box 2':[_('box 2')], 
    'store in':[_('store in')], 'box':[_('box')], 'string':[_('string')], 
    'left pos':[_('left')], 'top pos':[_('top')], 'right pos':[_('right')], 
    'bottom pos':[_('bottom')], 'width':[_('width')], 'height':[_('height')],
    'hide blocks':[_('hide blocks')],
    'set xy':[_('set xy'),_('x'),_('y')],
    'scale':[_('scale')]}

#
# Legacy names
#
OLD_NAMES = {'setxy':'set xy', 'storeinbox1':'store in box 1',
             'setpensize':'set pen size', 'setshade':'set shade',
             'plus2':'plus', 'division2':'divide','box1':'box 1',
             'box2':'box 2', 'storeinbox2':'store in box 2',
             'division':'divide', 'setcolor':'set color'}

#
# Logo primitives
#

PRIMITIVES = {'clean':'clean', 'forward':'forward', 'back':'back', 'arc':'arc',
    'left':'left', 'right':'right', 'set heading':'seth', 'scale':'scale',
    'show':'show', 'set scale':'setscale', 'xcor':'xcor', 'set xy':'setxy',
    'ycor':'ycor', 'heading':'heading', 'pen up':'penup',
    'pen down':'pendown', 'set pen size':'setpensize',
    'set text size':'settextsize', 'set color':'setcolor',
    'set shade':'setshade', 'fill screen':'fillscreen', 'shade':'shade',
    'pen size':'pensize', 'text size':'textsize', 'color':'color',
    'plus':'plus', 'minus':'minus', 'multiply':'product',
     'divide':'division', 'mod':'mod', 
    'random':'random', 'square root':'sqrt', 'less than':'less?',
    'greater than':'greater?', 'equal to':'equal?', 'and':'and', 'or':'or',
    'not':'not', 'print':'print', 'wait':'wait',
    'forever':'forever', 'repeat':'repeat', 'if then':'if', 'if else':'ifelse',
    'stop action':'stopstack', 'hspace':'nop', 'vspace':'nop',
    'start':'start', 'def action 1':'nop1', 'action 1':'stack1',
    'def action 2':'nop2', 'action 2':'stack2',
    'def action':'nop3', 'action':'stack',
    'store in box 1':'storeinbox1', 'box 1':'box1',
    'store in box 2':'storeinbox2', 'box 2':'box2', 
    'store in':'storeinbox', 'box':'box',
    'left pos':'leftpos', 'top pos':'toppos', 'right pos':'rightpos', 
    'bottom pos':'bottompos', 'width':'hres', 'height':'vres',
    'hide blocks':'hideblocks'}

#
# block default values
#

DEFAULTS = {'forward':[100], 'back':[100], 'left':[90], 'right':[90], 
    'arc':[90,100], 'set heading':[0], 'set scale':[33], 'show':[_('text')],
    'set pen size':[5], 'set text size':[32], 'set color':[0],
    'set shade':[50], 'fill screen':[60,80], 'number':[100],
    'random':[0,100], 'wait':[1], 'repeat':[4], 'set xy':[0,0], 
    'store in':[_('my box'),100], 'box':[_('my box')],
    'def action':[_('action')], 'action':[_('action')],
    'store in box 1':[100], 'store in box 2':[100]}

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

