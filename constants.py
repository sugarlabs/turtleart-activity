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

# block to proto tables
BASIC_STYLE_HEAD = ['start', 'action 1', 'action 2']
BASIC_STYLE_TAIL = ['stop action']
BASIC_STYLE = ['clean', 'pen up', 'pen down', 'action 1', 'action 2', 'nop' ]
BASIC_STYLE_1ARG = ['forward', 'back', 'left', 'right', 'seth', 'show',\
    'set scale', 'set pen size', 'set color', 'set shade'\
    'set text size', 'set text color', 'print', 'wait', 'store in box 1',\
    'store in box 2']
BASIC_STYLE_2ARG = ['arc', 'setxy', 'fill screen']
BOX_STYLE = ['number', 'xcor', 'ycor', 'heading', 'pen size', 'color', 'shade'\
    'text color', 'text size', 'box 1', 'box 2', 'string']


TURTLE_PALETTE = ['clean', 'forward', 'back', 'left', 'right', 'seth', 'show',\
    'set_scale', 'xcor', 'ycor', 'heading']
PEN_PALETTE = ['pen up','pen down']
NUMBER_PALETTE = ['number']
BLOCKS_PALETTE = ['string']

TURTLE_COLORS = ["#00FF00","#00A000"]
PEN_COLORS = ["#00FFFF","#00A0A0"]
NUMBER_COLORS = ["#FF00FF","#A000A0"]
BLOCKS_COLORS = ["#FFFF00","#A0A000"]

# 'dead key' Unicode dictionaries
DEAD_KEYS = ['grave','acute','circumflex','tilde','diaeresis','abovering']
DEAD_DICTS = [{'A':192,'E':200,'I':204,'O':210,'U':217,'a':224,'e':232,'i':236,\
               'o':242,'u':249},
              {'A':193,'E':201,'I':205,'O':211,'U':218,'a':225,'e':233,'i':237,\
               'o':243,'u':250},
              {'A':194,'E':202,'I':206,'O':212,'U':219,'a':226,'e':234,\
               'i':238,'o':244,'u':251},
              {'A':195,'O':211,'N':209,'U':360,'a':227,'o':245,'n':241,'u':361},
              {'A':196,'E':203,'I':207,'O':211,'U':218,'a':228,'e':235,\
               'i':239,'o':245,'u':252},
              {'A':197,'a':229}]
NOISE_KEYS = ['Shift_L', 'Shift_R', 'Control_L', 'Caps_Lock', 'Pause',\
              'Alt_L', 'Alt_R', 'KP_Enter', 'ISO_Level3_Shift', 'KP_Divide',\
              'Escape', 'Return', 'KP_Page_Up', 'Up', 'Down', 'Menu',\
              'Left', 'Right', 'KP_Home', 'KP_End', 'KP_Up', 'Super_L',\
              'KP_Down', 'KP_Left', 'KP_Right', 'KP_Page_Down', 'Scroll_Lock',\
              'Page_Down', 'Page_Up']
WHITE_SPACE = ['space','Tab']

