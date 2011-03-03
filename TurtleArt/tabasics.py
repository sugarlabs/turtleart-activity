# -*- coding: utf-8 -*-
#Copyright (c) 2011, Walter Bender

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
below. If you want to add a new block to Turtle Art, you could
simply add a block of code to this file or to turtle_block_plugin.py,
which contains additional blocks. (Even better, write your own plugin!!)

For example, if we want to add a new turtle command, 'uturn', we'd
make the following changes:

    make_prim('uturn',  # the name of your block
              palette='turtle',  # the palette to place it in
              style='basic-style',  # the block style
              label=_('u turn'),  # the label for the block
              prim_name='uturn',  # code reference (see below)
              help_string=_('turns the turtle 180 degrees'))

    # Next, you need to define what your block will do:
    # def_prim takes 3 arguments: the primitive name, the number of
    # of arguments, 0 in this case, and the function to call, in this
    # case, the canvas function to set the heading.
    self.tw.lc.def_prim('uturn', 0,
        lambda self, x: self.tw.canvas.seth(self.tw.canvas.heading + 180))

That's it. When you next run Turtle Art, you will have a 'uturn' block
on the Turtle Palette.

Adding a new palette is simply a matter of:
    p = Palette('mypalette', ["#00FF00", "#00A000"])  # assign name and colors
    p.set_help(_('Palette of my custom commands'))  # and a help message
    p.add_palette()

You will have to create icons for the palette-selector buttons. These
are kept in the icons subdirectory. You need two icons:
mypaletteoff.svg and mypaletteon.svg, where 'mypalette' is the same
string as the entry you used in instantiating the Palette class. Note
that the icons should be the same size (55x55) as the others. (This is
the default icon size for Sugar toolbars.)

"""

from time import time
from math import sqrt
from random import uniform

from gettext import gettext as _

from taprimitive import make_palette, make_prim
from talogo import PLUGIN_DICTIONARY, logoerror
from taconstants import CONSTANTS, BLACK, WHITE
from tautils import convert, chr_to_ord, round_int, strtype


def _num_type(x):
    """ Is x a number type? """
    if type(x) == int:
        return True
    if type(x) == float:
        return True
    if type(x) == ord:
        return True
    return False


def _millisecond():
    """ Current time in milliseconds """
    return time() * 1000


class Palettes():
    """ a class for creating the palettes of blocks """

    def __init__(self, parent):
        self.tw = parent

        make_palette('turtle', ["#00FF00", "#00A000"],
                     _('Palette of turtle commands'))
        self._turtle_palette()

        make_palette('pen', ["#00FFFF", "#00A0A0"],
                     _('Palette of pen commands'))
        self._pen_palette()

        make_palette('colors', ["#00FFFF", "#00A0A0"],
                     _('Palette of pen colors'))
        self._color_palette()

        make_palette('numbers', ["#FF00FF", "#A000A0"],
                     _('Palette of numeric operators'))
        self._numbers_palette()

        make_palette('flow', ["#FFC000", "#A08000"],
                     _('Palette of flow operators'))
        self._flow_palette()

        make_palette('blocks', ["#FFFF00", "#A0A000"],
                     _('Palette of variable blocks'))
        self._blocks_palette()

        make_palette('trash', ["#FFFF00", "#A0A000"])
        self._trash_palette()

    # Palette definitions

    def _turtle_palette(self):
        """ The basic Turtle Art turtle palette """

        PLUGIN_DICTIONARY['move'] = self._prim_move
        make_prim('forward',
                  palette='turtle',
                  style='basic-style-1arg',
                  label=_('forward'),
                  default=100,
                  prim_name='forward',
                  help_string=_('moves turtle forward'))
        self.tw.lc.def_prim('forward', 1,
                             lambda self, x: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.forward, x))

        make_prim('back',
                  palette='turtle',
                  style='basic-style-1arg',
                  label=_('back'),
                  prim_name='back',
                  default=100,
                  help_string=_('moves turtle backward'))
        self.tw.lc.def_prim('back', 1,
                             lambda self, x: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.forward, -x))

        PLUGIN_DICTIONARY['clean'] = self.tw.lc.prim_clear
        make_prim('clean',
                  palette='turtle',
                  style='basic-style-extended-vertical',
                  label=_('clean'),
                  prim_name='clean',
                  help_string=_('clears the screen and reset the turtle'))
        self.tw.lc.def_prim('clean', 0,
                             lambda self: PLUGIN_DICTIONARY['clean']())

        PLUGIN_DICTIONARY['right'] = self._prim_right
        make_prim('left',
                  palette='turtle',
                  style='basic-style-1arg',
                  label=_('left'),
                  prim_name='left',
                  default=90,
                  help_string=_('turns turtle counterclockwise (angle in \
degrees)'))
        self.tw.lc.def_prim('right', 1,
                             lambda self, x: PLUGIN_DICTIONARY['right'](-x))

        make_prim('right',
                  palette='turtle',
                  style='basic-style-1arg',
                  label=_('right'),
                  prim_name='right',
                  default=90,
                  help_string=_('turns turtle clockwise (angle in degrees)'))
        self.tw.lc.def_prim('right', 1,
                             lambda self, x: PLUGIN_DICTIONARY['right'](x))

        PLUGIN_DICTIONARY['arc'] = self._prim_arc
        make_prim('arc',
                  palette='turtle',
                  style='basic-style-2arg',
                  label=[_('arc'), _('angle'), _('radius')],
                  prim_name='arc',
                  default=[90, 100],
                  help_string=_('moves turtle along an arc'))
        self.tw.lc.def_prim('arc', 2,
                             lambda self, x, y: PLUGIN_DICTIONARY['arc'](
                self.tw.canvas.arc, x, y))

        make_prim('setxy2',
                  palette='turtle',
                  style='basic-style-2arg',
                  label=[_('set xy'), _('x'), _('y')],
                  prim_name='setxy2',
                  default=[0, 0],
                  help_string=_('moves turtle to position xcor, ycor; (0, 0) \
is in the center of the screen.'))
        self.tw.lc.def_prim('setxy2', 2,
                             lambda self, x, y: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.setxy, x, y))

        PLUGIN_DICTIONARY['set'] = self._prim_set
        make_prim('seth',
                  palette='turtle',
                  style='basic-style-1arg',
                  label=_('set heading'),
                  prim_name='seth',
                  default=0,
                  help_string=_('sets the heading of the turtle (0 is towards \
the top of the screen.)'))
        self.tw.lc.def_prim('seth', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'heading', self.tw.canvas.seth, x))

        make_prim('xcor',
                  palette='turtle',
                  style='box-style',
                  label=_('xcor'),
                  help_string=_('holds current x-coordinate value of the \
turtle (can be used in place of a number block)'),
                  value_block=True,
                  prim_name='xcor')
        self.tw.lc.def_prim(
            'xcor', 0, lambda self: self.tw.canvas.xcor / self.tw.coord_scale)

        make_prim('ycor',
                  palette='turtle',
                  style='box-style',
                  label=_('ycor'),
                  help_string=_('holds current y-coordinate value of the \
turtle (can be used in place of a number block)'),
                  value_block=True,
                  prim_name='ycor')
        self.tw.lc.def_prim(
            'ycor', 0, lambda self: self.tw.canvas.ycor / self.tw.coord_scale)

        make_prim('heading',
                  palette='turtle',
                  style='box-style',
                  label=_('heading'),
                  help_string=_('holds current heading value of the turtle \
(can be used in place of a number block)'),
                  value_block=True,
                  prim_name='heading')
        self.tw.lc.def_prim(
            'heading', 0, lambda self: self.tw.canvas.heading)

        # Depreciated
        make_prim('setxy',
                  style='basic-style-2arg',
                  label=[_('set xy'), _('x'), _('y')],
                  prim_name='setxy',
                  default=[0, 0],
                  help_string=_('moves turtle to position xcor, ycor; (0, 0) \
is in the center of the screen.'))
        self.tw.lc.def_prim('setxy', 2,
                             lambda self, x, y: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.setxy, x, y, pendown=False))

    def _pen_palette(self):
        """ The basic Turtle Art pen palette """

        make_prim('penup',
                  palette='pen',
                  style='basic-style-extended-vertical',
                  label=_('pen up'),
                  prim_name='penup',
                  help_string=_('Turtle will not draw when moved.'))
        self.tw.lc.def_prim('penup', 0,
                             lambda self: self.tw.canvas.setpen(False))

        make_prim('pendown',
                  palette='pen',
                  style='basic-style-extended-vertical',
                  label=_('pen down'),
                  prim_name='pendown',
                  help_string=_('Turtle will draw when moved.'))
        self.tw.lc.def_prim('pendown', 0,
                             lambda self: self.tw.canvas.setpen(True))

        make_prim('setpensize',
                  palette='pen',
                  style='basic-style-1arg',
                  label=_('set pen size'),
                  prim_name='setpensize',
                  default=5,
                  help_string=_('sets size of the line drawn by the turtle'))
        self.tw.lc.def_prim('setpensize', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'pensize', self.tw.canvas.setpensize, x))

        make_prim('fillscreen',
                  palette='pen',
                  style='basic-style-2arg',
                  label=[_('fill screen'), _('color'), _('shade')],
                  prim_name='fillscreen',
                  default=[60, 80],
                  help_string=_('fills the background with (color, shade)'))
        self.tw.lc.def_prim('fillscreen', 2,
            lambda self, x, y: self.tw.canvas.fillscreen(x, y))

        make_prim('pensize',
                  palette='pen',
                  style='box-style',
                  label=_('pen size'),
                  help_string=_('holds current pen size (can be used in place \
of a number block)'),
                  value_block=True,
                  prim_name='pensize')
        self.tw.lc.def_prim('pensize', 0, lambda self: self.tw.canvas.pensize)

        make_prim('startfill',
                  palette='pen',
                  style='basic-style-extended-vertical',
                  label=_('start fill'),
                  prim_name='startfill',
                  help_string=_('starts filled polygon (used with end fill \
block)'))
        self.tw.lc.def_prim('startfill', 0,
                             lambda self: self.tw.canvas.start_fill())

        make_prim('stopfill',
                  palette='pen',
                  style='basic-style-extended-vertical',
                  label=_('end fill'),
                  prim_name='stopfill',
                  help_string=_('completes filled polygon (used with start \
fill block)'))
        self.tw.lc.def_prim('stopfill', 0,
                             lambda self: self.tw.canvas.stop_fill())

    def _color_palette(self):
        """ The basic Turtle Art color palette """

        make_prim('setcolor',
                  palette='colors',
                  style='basic-style-1arg',
                  label=_('set color'),
                  prim_name='setcolor',
                  default=0,
                  help_string=_('sets color of the line drawn by the turtle'))
        self.tw.lc.def_prim('setcolor', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'color', self.tw.canvas.setcolor, x))

        make_prim('setshade',
                  palette='colors',
                  style='basic-style-1arg',
                  label=_('set shade'),
                  prim_name='setshade',
                  default=50,
                  help_string=_('sets shade of the line drawn by the turtle'))
        self.tw.lc.def_prim('setshade', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'shade', self.tw.canvas.setshade, x))

        make_prim('setgray',
                  palette='colors',
                  style='basic-style-1arg',
                  label=_('set gray'),
                  prim_name='setgray',
                  default=100,
                  help_string=_('sets gray level of the line drawn by the \
turtle'))
        self.tw.lc.def_prim('setgray', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'gray', self.tw.canvas.setgray, x))

        make_prim('color',
                  palette='colors',
                  style='box-style',
                  label=_('color'),
                  help_string=_('holds current pen color (can be used in \
place of a number block)'),
                  value_block=True,
                  prim_name='color')
        self.tw.lc.def_prim('color', 0, lambda self: self.tw.canvas.color)

        make_prim('shade',
                  palette='colors',
                  style='box-style',
                  label=_('shade'),
                  help_string=_('holds current pen shade'),
                  value_block=True,
                  prim_name='shade')
        self.tw.lc.def_prim('shade', 0, lambda self: self.tw.canvas.shade)

        make_prim('gray',
                  palette='colors',
                  style='box-style',
                  label=_('gray'),
                  help_string=_('holds current gray level (can be used in \
place of a number block)'),
                  value_block=True,
                  prim_name='gray')
        self.tw.lc.def_prim('gray', 0, lambda self: self.tw.canvas.gray)

        self._make_constant('red', 'colors', CONSTANTS['red'])
        self._make_constant('orange', 'colors', CONSTANTS['orange'])
        self._make_constant('yellow', 'colors', CONSTANTS['yellow'])
        self._make_constant('green', 'colors', CONSTANTS['green'])
        self._make_constant('cyan', 'colors', CONSTANTS['cyan'])
        self._make_constant('blue', 'colors', CONSTANTS['blue'])
        self._make_constant('purple', 'colors', CONSTANTS['purple'])
        self._make_constant('white', 'colors', WHITE)
        self._make_constant('black', 'colors', BLACK)

        # depreciated blocks
        make_prim('settextcolor',
                  style='basic-style-1arg',
                  label=_('set text color'),
                  prim_name='settextcolor',
                  default=0,
                  help_string=_('sets color of text drawn by the turtle'))
        self.tw.lc.def_prim('settextcolor', 1,
                             lambda self, x: self.tw.canvas.settextcolor(x))

        make_prim('settextsize',
                  style='basic-style-1arg',
                  label=_('set text size'),
                  prim_name='settextsize',
                  default=0,
                  help_string=_('sets size of text drawn by the turtle'))
        self.tw.lc.def_prim('settextsize', 1,
                             lambda self, x: self.tw.canvas.settextsize(x))

    def _numbers_palette(self):
        """ The basic Turtle Art numbers palette """

        PLUGIN_DICTIONARY['plus'] = self._prim_plus
        make_prim('plus2',
                  palette='numbers',
                  style='number-style',
                  label='+',
                  special_name=_('plus'),
                  prim_name='plus',
                  help_string=_('adds two alphanumeric inputs'))
        self.tw.lc.def_prim(
            'plus', 2, lambda self, x, y: PLUGIN_DICTIONARY['plus'](x, y))

        PLUGIN_DICTIONARY['minus'] = self._prim_minus
        make_prim('minus2',
                  palette='numbers',
                  style='number-style-porch',
                  label='–',
                  special_name=_('minus'),
                  prim_name='minus',
                  help_string=_('subtracts bottom numeric input from top \
numeric input'))
        self.tw.lc.def_prim(
            'minus', 2, lambda self, x, y: PLUGIN_DICTIONARY['minus'](x, y))

        PLUGIN_DICTIONARY['product'] = self._prim_product
        make_prim('product2',
                  palette='numbers',
                  style='number-style',
                  label='×',
                  special_name=_('multiply'),
                  prim_name='product',
                  help_string=_('multiplies two numeric inputs'))
        self.tw.lc.def_prim(
            'product', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['product'](x, y))

        PLUGIN_DICTIONARY['division'] = self._prim_careful_divide
        make_prim('division2',
                  palette='numbers',
                  style='number-style-porch',
                  label='/',
                  special_name=_('divide'),
                  prim_name='division',
                  help_string=_('divides top numeric input (numerator) by \
bottom numeric input (denominator)'))
        self.tw.lc.def_prim(
            'division', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['division'](x, y))

        PLUGIN_DICTIONARY['id'] = self._prim_identity
        make_prim('identity2',
                  palette='numbers',
                  style='number-style-1strarg',
                  label='←',
                  special_name=_('identity'),
                  prim_name='id',
                  help_string=_('identity operator used for extending blocks'))
        self.tw.lc.def_prim('id', 1,
                             lambda self, x: PLUGIN_DICTIONARY['id'](x))

        PLUGIN_DICTIONARY['remainder'] = self._prim_mod
        make_prim('remainder2',
                  palette='numbers',
                  style='number-style-porch',
                  label=_('mod'),
                  special_name=_('mod'),
                  prim_name='remainder',
                  help_string=_('modular (remainder) operator'))
        self.tw.lc.def_prim('remainder', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['remainder'](x, y))

        PLUGIN_DICTIONARY['sqrt'] = self._prim_sqrt
        make_prim('sqrt',
                  palette='numbers',
                  style='number-style-1arg',
                  label=_('√'),
                  special_name=_('square root'),
                  prim_name='sqrt',
                  help_string=_('calculates square root'))
        self.tw.lc.def_prim('sqrt', 1,
                             lambda self, x: PLUGIN_DICTIONARY['sqrt'](x))

        PLUGIN_DICTIONARY['random'] = self._prim_random
        make_prim('random',
                  palette='numbers',
                  style='number-style-block',
                  label=[_('random'), _('min'), _('max')],
                  default=[0, 100],
                  prim_name='random',
                  help_string=_('returns random number between minimum (top) \
and maximum (bottom) values'))
        self.tw.lc.def_prim(
            'random', 2, lambda self, x, y: PLUGIN_DICTIONARY['random'](x, y))

        make_prim('number',
                  palette='numbers',
                  style='box-style',
                  label='100',
                  default=100,
                  special_name=_('number'),
                  help_string=_('used as numeric input in mathematic \
operators'))

        PLUGIN_DICTIONARY['more'] = self._prim_more
        make_prim('greater2',
                  palette='numbers',
                  style='compare-porch-style',
                  label='>',
                  special_name=_('greater than'),
                  prim_name='greater?',
                  help_string=_('logical greater-than operator'))
        self.tw.lc.def_prim(
            'greater?', 2, lambda self, x, y: PLUGIN_DICTIONARY['more'](x, y))

        PLUGIN_DICTIONARY['less'] = self._prim_less
        make_prim('less2',
                  palette='numbers',
                  style='compare-porch-style',
                  label='<',
                  special_name=_('less than'),
                  prim_name='less?',
                  help_string=_('logical less-than operator'))
        self.tw.lc.def_prim(
            'less?', 2, lambda self, x, y: PLUGIN_DICTIONARY['less'](x, y))

        PLUGIN_DICTIONARY['equal'] = self._prim_equal
        make_prim('equal2',
                  palette='numbers',
                  style='compare-style',
                  label='=',
                  special_name=_('equal'),
                  prim_name='equal?',
                  help_string=_('logical equal-to operator'))
        self.tw.lc.def_prim(
            'equal?', 2, lambda self, x, y: PLUGIN_DICTIONARY['equal'](x, y))

        make_prim('not',
                  palette='numbers',
                  style='not-style',
                  label=_('not'),
                  prim_name='not',
                  help_string=_('logical NOT operator'))
        self.tw.lc.def_prim('not', 1, lambda self, x: not x)

        make_prim('and2',
                  palette='numbers',
                  style='boolean-style',
                  label=_('and'),
                  prim_name='and',
                  special_name=_('and'),
                  help_string=_('logical AND operator'))
        self.tw.lc.def_prim('not', 2, lambda self, x, y: x & y)

        make_prim('or2',
                  palette='numbers',
                  style='boolean-style',
                  label=_('or'),
                  prim_name='or',
                  special_name=_('or'),
                  help_string=_('logical OR operator'))
        self.tw.lc.def_prim('not', 2, lambda self, x, y: x | y)

    def _flow_palette(self):
        """ The basic Turtle Art flow palette """

        PLUGIN_DICTIONARY['wait'] = self._prim_wait
        make_prim('wait',
                  palette='flow',
                  style='basic-style-1arg',
                  label=_('wait'),
                  prim_name='wait',
                  default=1,
                  help_string=_(
                'pauses program execution a specified number of seconds'))
        self.tw.lc.def_prim('wait', 1, PLUGIN_DICTIONARY['wait'], True)

        PLUGIN_DICTIONARY['forever'] = self._prim_forever
        make_prim('forever',
                  palette='flow',
                  style='flow-style',
                  label=_('forever'),
                  prim_name='forever',
                  default=[None, 'vspace'],
                  help_string=_('loops forever'))
        self.tw.lc.def_prim('forever', 1, PLUGIN_DICTIONARY['forever'], True)

        PLUGIN_DICTIONARY['repeat'] = self._prim_repeat
        make_prim('repeat',
                  palette='flow',
                  style='flow-style-1arg',
                  label=[' ', _('repeat')],
                  prim_name='repeat',
                  default=[4, None, 'vspace'],
                  special_name=_('repeat'),
                  help_string=_('loops specified number of times'))
        self.tw.lc.def_prim('repeat', 2, PLUGIN_DICTIONARY['repeat'], True)

        PLUGIN_DICTIONARY['if'] = self._prim_if
        make_prim('if',
                  palette='flow',
                  style='flow-style-boolean',
                  label=[' ', _('if'), _('then')],
                  prim_name='if',
                  default=[None, None, 'vspace'],
                  special_name=_('if then'),
                  help_string=_('if-then operator that uses boolean \
operators from Numbers palette'))
        self.tw.lc.def_prim('if', 2, PLUGIN_DICTIONARY['if'], True)

        PLUGIN_DICTIONARY['ifelse'] = self._prim_ifelse
        make_prim('ifelse',
                  palette='flow',
                  style='flow-style-else',
                  label=[' ', _('if'), _('then else')],
                  prim_name='ifelse',
                  default=[None, 'vspace', None, 'vspace'],
                  special_name=_('if then else'),
                  help_string=_('if-then-else operator that uses boolean \
operators from Numbers palette'))
        self.tw.lc.def_prim('ifelse', 3, PLUGIN_DICTIONARY['ifelse'], True)

        make_prim('hspace',
                  palette='flow',
                  style='flow-style-tail',
                  label=' ',
                  prim_name='nop',
                  special_name=_('horizontal space'),
                  help_string=_('jogs stack right'))
        self.tw.lc.def_prim('nop', 0, lambda self: None)

        make_prim('vspace',
                  palette='flow',
                  style='basic-style-extended-vertical',
                  label=' ',
                  prim_name='nop',
                  special_name=_('vertical space'),
                  help_string=_('jogs stack down'))
        self.tw.lc.def_prim('nop', 0, lambda self: None)

        PLUGIN_DICTIONARY['stopstack'] = self._prim_stopstack
        make_prim('stopstack',
                  palette='flow',
                  style='basic-style-tail',
                  label=_('stop action'),
                  prim_name='stopstack',
                  help_string=_('stops current action'))
        self.tw.lc.def_prim('stopstack', 0,
                             lambda self: PLUGIN_DICTIONARY['stopstack']())

    def _blocks_palette(self):
        """ The basic Turtle Art blocks palette """

        PLUGIN_DICTIONARY['start'] = self._prim_start
        make_prim('start',
                  palette='blocks',
                  style='basic-style-head',
                  label=_('start'),
                  prim_name='start',
                  help_string=_('connects action to toolbar run buttons'))
        self.tw.lc.def_prim('start', 0,
                             lambda self: PLUGIN_DICTIONARY['start']())

        PLUGIN_DICTIONARY['setbox'] = self._prim_setbox
        make_prim('storeinbox1',
                  palette='blocks',
                  style='basic-style-1arg',
                  label=_('store in box 1'),
                  prim_name='storeinbox1',
                  default=100,
                  help_string=_('stores numeric value in Variable 1'))
        self.tw.lc.def_prim('storeinbox1', 1,
                             lambda self, x: PLUGIN_DICTIONARY['setbox'](
                'box1', None, x))

        make_prim('storeinbox2',
                  palette='blocks',
                  style='basic-style-1arg',
                  label=_('store in box 2'),
                  prim_name='storeinbox2',
                  default=100,
                  help_string=_('stores numeric value in Variable 2'))
        self.tw.lc.def_prim('storeinbox2', 1,
                             lambda self, x: PLUGIN_DICTIONARY['setbox'](
                'box2', None, x))

        make_prim('string',
                  palette='blocks',
                  style='box-style',
                  label=_('text'),
                  default=_('text'),
                  special_name='',
                  help_string=_('string value'))

        make_prim('box1',
                  palette='blocks',
                  style='box-style',
                  label=_('box 1'),
                  prim_name='box1',
                  help_string=_('Variable 1 (numeric value)'),
                  value_block=True)
        self.tw.lc.def_prim('box1', 0, lambda self: self.tw.lc.boxes['box1'])

        make_prim('box2',
                  palette='blocks',
                  style='box-style',
                  label=_('box 2'),
                  prim_name='box2',
                  help_string=_('Variable 2 (numeric value)'),
                  value_block=True)
        self.tw.lc.def_prim('box2', 0, lambda self: self.tw.lc.boxes['box2'])

        PLUGIN_DICTIONARY['box'] = self._prim_box
        make_prim('box',
                  palette='blocks',
                  style='number-style-1strarg',
                  label=_('box'),
                  prim_name='box',
                  default=_('my box'),
                  help_string=_('named variable (numeric value)'))
        self.tw.lc.def_prim('box', 1,
                             lambda self, x: PLUGIN_DICTIONARY['box'](x))

        make_prim('storein',
                  palette='blocks',
                  style='basic-style-2arg',
                  label=[_('store in'), _('box'), _('value')],
                  prim_name='storeinbox',
                  default=[_('my box'), 100],
                  help_string=_('stores numeric value in named variable'))
        self.tw.lc.def_prim('storeinbox', 2,
                             lambda self, x, y: PLUGIN_DICTIONARY['setbox'](
                'box3', x, y))

        make_prim('hat',
                  palette='blocks',
                  style='basic-style-head-1arg',
                  label=_('action'),
                  prim_name='nop3',
                  default=_('action'),
                  help_string=_('top of nameable action stack'))
        self.tw.lc.def_prim('nop3', 1, lambda self, x: None)

        make_prim('hat1',
                  palette='blocks',
                  style='basic-style-head',
                  label=_('action 1'),
                  prim_name='nop1',
                  help_string=_('top of Action 1 stack'))
        self.tw.lc.def_prim('nop1', 0, lambda self: None)

        make_prim('hat2',
                  palette='blocks',
                  style='basic-style-head',
                  label=_('action 2'),
                  prim_name='nop2',
                  help_string=_('top of Action 2 stack'))
        self.tw.lc.def_prim('nop2', 0, lambda self: None)

        PLUGIN_DICTIONARY['stack'] = self._prim_stack
        make_prim('stack',
                  palette='blocks',
                  style='basic-style-1arg',
                  label=_('action'),
                  prim_name='stack',
                  default=_('action'),
                  help_string=_('invokes named action stack'))
        self.tw.lc.def_prim('stack', 1, PLUGIN_DICTIONARY['stack'], True)

        PLUGIN_DICTIONARY['stack1'] = self._prim_stack1
        make_prim('stack1',
                  palette='blocks',
                  style='basic-style-extended-vertical',
                  label=_('action 1'),
                  prim_name='stack1',
                  default=_('action 1'),
                  help_string=_('invokes Action 1 stack'))
        self.tw.lc.def_prim('stack1', 0, PLUGIN_DICTIONARY['stack1'], True)

        PLUGIN_DICTIONARY['stack2'] = self._prim_stack2
        make_prim('stack2',
                  palette='blocks',
                  style='basic-style-extended-vertical',
                  label=_('action 2'),
                  prim_name='stack2',
                  default=_('action 2'),
                  help_string=_('invokes Action 2 stack'))
        self.tw.lc.def_prim('stack2', 0, PLUGIN_DICTIONARY['stack2'], True)

    def _trash_palette(self):
        """ The basic Turtle Art turtle palette """

        make_prim('empty',
                  palette='trash',
                  style='basic-style-tail',
                  label=_('empty trash'),
                  help_string=_("permanently deletes items in trash"))

        make_prim('restoreall',
                  palette='trash',
                  style='basic-style-head',
                  label=_('restore all'),
                  help_string=_("restore all blocks from trash"))

    # Block primitives

    def _prim_arc(self, cmd, value1, value2):
        """ Turtle draws an arc of degree, radius """
        cmd(float(value1), float(value2))
        self.tw.lc.update_label_value(
            'xcor', self.tw.canvas.xcor / self.tw.coord_scale)
        self.tw.lc.update_label_value(
            'ycor', self.tw.canvas.ycor / self.tw.coord_scale)
        self.tw.lc.update_label_value('heading', self.tw.canvas.heading)

    def _prim_box(self, x):
        """ Retrieve value from named box """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        try:
            return self.tw.lc.boxes['box3' + str(x)]
        except KeyError:
            raise logoerror("#emptybox")

    def _prim_forever(self, blklist):
        """ Do list forever """
        while True:
            self.tw.lc.icall(self.tw.lc.evline, blklist[:])
            yield True
            if self.tw.lc.procstop:
                break
        self.tw.lc.ireturn()
        yield True

    def _prim_if(self, boolean, blklist):
        """ If bool, do list """
        if boolean:
            self.tw.lc.icall(self.tw.lc.evline, blklist[:])
            yield True
        self.tw.lc.ireturn()
        yield True

    def _prim_ifelse(self, boolean, list1, list2):
        """ If bool, do list1, else do list2 """
        if boolean:
            self.tw.lc.ijmp(self.tw.lc.evline, list1[:])
            yield True
        else:
            self.tw.lc.ijmp(self.tw.lc.evline, list2[:])
            yield True

    def _prim_move(self, cmd, value1, value2=None, pendown=True):
        """ Turtle moves by method specified in value1 """
        if value2 is None:
            cmd(value1)
        else:
            cmd(float(value1), float(value2), pendown=pendown)
        self.tw.lc.update_label_value('xcor',
                           self.tw.canvas.xcor / self.tw.coord_scale)
        self.tw.lc.update_label_value('ycor',
                           self.tw.canvas.ycor / self.tw.coord_scale)

    def _prim_repeat(self, num, blklist):
        """ Repeat list num times. """
        num = self.tw.lc.int(num)
        for i in range(num):
            self.tw.lc.icall(self.tw.lc.evline, blklist[:])
            yield True
            if self.tw.lc.procstop:
                break
        self.tw.lc.ireturn()
        yield True

    def _prim_right(self, value):
        """ Turtle rotates clockwise """
        self.tw.canvas.right(float(value))
        self.tw.lc.update_label_value('heading', self.tw.canvas.heading)

    def _prim_set(self, name, cmd, value=None):
        """ Set a value and update the associated value blocks """
        if value is not None:
            cmd(value)
            self.tw.lc.update_label_value(name, value)

    def _prim_setbox(self, name, x, val):
        """ Define value of named box """
        if x is not None:
            if type(convert(x, float, False)) == float:
                if int(float(x)) == x:
                    x = int(x)
            self.tw.lc.boxes[name + str(x)] = val
            return

        self.tw.lc.boxes[name] = val
        self.tw.lc.update_label_value(name, val)

    def _prim_stack(self, x):
        """ Process a named stack """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        if 'stack3' + str(x) not in self.tw.lc.stacks or \
           self.tw.lc.stacks['stack3' + str(x)] is None:
            raise logoerror("#nostack")
        self.tw.lc.icall(self.tw.lc.evline,
                          self.tw.lc.stacks['stack3' + str(x)][:])
        yield True
        self.tw.lc.procstop = False
        self.tw.lc.ireturn()
        yield True

    def _prim_stack1(self):
        """ Process Stack 1 """
        if self.tw.lc.stacks['stack1'] is None:
            raise logoerror("#nostack")
        self.tw.lc.icall(self.tw.lc.evline,
                          self.tw.lc.stacks['stack1'][:])
        yield True
        self.tw.lc.procstop = False
        self.tw.lc.ireturn()
        yield True

    def _prim_stack2(self):
        """ Process Stack 2 """
        if self.tw.lc.stacks['stack2'] is None:
            raise logoerror("#nostack")
        self.tw.lc.icall(self.tw.lc.evline, self.tw.lc.stacks['stack2'][:])
        yield True
        self.tw.lc.procstop = False
        self.tw.lc.ireturn()
        yield True

    def _prim_start(self):
        """ Start block: recenter """
        if self.tw.running_sugar:
            self.tw.activity.recenter()

    def _prim_stopstack(self):
        """ Stop execution of a stack """
        self.tw.lc.procstop = True

    def _prim_wait(self, wait_time):
        """ Show the turtle while we wait """
        self.tw.active_turtle.show()
        endtime = _millisecond() + wait_time * 1000.
        while _millisecond() < endtime:
            yield True
        self.tw.active_turtle.hide()
        self.tw.lc.ireturn()
        yield True

    # Math primitivies

    def _prim_careful_divide(self, x, y):
        """ Raise error on divide by zero """
        try:
            return x / y
        except ZeroDivisionError:
            raise logoerror("#zerodivide")
        except TypeError:
            try:
                return self._string_to_num(x) / self._string_to_num(y)
            except ZeroDivisionError:
                raise logoerror("#zerodivide")
            except ValueError:
                raise logoerror("#syntaxerror")
            except TypeError:
                raise logoerror("#notanumber")

    def _prim_equal(self, x, y):
        """ Numeric and logical equal """
        try:
            return float(x) == float(y)
        except TypeError:
            typex, typey = False, False
            if strtype(x):
                typex = True
            if strtype(y):
                typey = True
            if typex and typey:
                return x == y
            try:
                return self._string_to_num(x) == self._string_to_num(y)
            except ValueError:
                raise logoerror("#syntaxerror")

    def _prim_less(self, x, y):
        """ Compare numbers and strings """
        try:
            return float(x) < float(y)
        except ValueError:
            typex, typey = False, False
            if strtype(x):
                typex = True
            if strtype(y):
                typey = True
            if typex and typey:
                return x < y
            try:
                return self._string_to_num(x) < self._string_to_num(y)
            except TypeError:
                raise logoerror("#notanumber")

    def _prim_more(self, x, y):
        """ Compare numbers and strings """
        return self._prim_less(y, x)

    def _prim_plus(self, x, y):
        """ Add numbers, concat strings """
        if _num_type(x) and _num_type(y):
            return(x + y)
        else:
            if _num_type(x):
                xx = str(round_int(x))
            else:
                xx = str(x)
            if _num_type(y):
                yy = str(round_int(y))
            else:
                yy = str(y)
            return(xx + yy)

    def _prim_minus(self, x, y):
        """ Numerical subtraction """
        if _num_type(x) and _num_type(y):
            return(x - y)
        try:
            return self._string_to_num(x) - self._string_to_num(y)
        except TypeError:
            raise logoerror("#notanumber")

    def _prim_product(self, x, y):
        """ Numerical multiplication """
        if _num_type(x) and _num_type(y):
            return(x * y)
        try:
            return self._string_to_num(x) * self._string_to_num(y)
        except TypeError:
            raise logoerror("#notanumber")

    def _prim_mod(self, x, y):
        """ Numerical mod """
        if _num_type(x) and _num_type(y):
            return(x % y)
        try:
            return self._string_to_num(x) % self._string_to_num(y)
        except TypeError:
            raise logoerror("#notanumber")
        except ValueError:
            raise logoerror("#syntaxerror")

    def _prim_sqrt(self, x):
        """ Square root """
        if _num_type(x):
            if x < 0:
                raise logoerror("#negroot")
            return sqrt(x)
        try:
            return sqrt(self._string_to_num(x))
        except ValueError:
            raise logoerror("#negroot")
        except TypeError:
            raise logoerror("#notanumber")

    def _prim_random(self, x, y):
        """ Random integer """
        if _num_type(x) and _num_type(y):
            return(int(round(uniform(x, y), 0)))
        xx, xflag = chr_to_ord(x)
        yy, yflag = chr_to_ord(y)
        if xflag and yflag:
            return chr(int(round(uniform(xx, yy), 0)))
        if not xflag:
            xx = self._string_to_num(x)
        if not yflag:
            yy = self._string_to_num(y)
        try:
            return(int(round(uniform(xx, yy), 0)))
        except TypeError:
            raise logoerror("#notanumber")

    def _prim_identity(self, x):
        """ Identity function """
        return(x)

    # Utilities

    def _string_to_num(self, x):
        """ Try to comvert a string to a number """
        if type(x) is float:
            return(x)
        if type(x) is int:
            return(x)
        if type(x) is ord:
            return(int(x))
        xx = convert(x.replace(self.tw.decimal_point, '.'), float)
        if type(xx) is float:
            return xx
        else:
            xx, xflag = chr_to_ord(x)
            if xflag:
                return xx
            else:
                raise logoerror("#syntaxerror")

    def _make_constant(self, block_name, palette_name, constant):
        """ Factory for constant blocks """
        make_prim(block_name, palette=palette_name, style='box-style',
                  label=_(block_name), prim_name=block_name)
        self.tw.lc.def_prim(block_name, 0, lambda self: constant)
