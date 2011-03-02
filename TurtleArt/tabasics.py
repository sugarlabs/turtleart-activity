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

        b = Primitive('uturn') 
        b.set_palette('turtle')  # the palette to place it in
        b.set_style('basic-style')  # the block style 
        b.set_label(_('u-turn'))  # the label that will appear on the block
        b.set_prim_name('uturn')  # an intern name for the primitive
        b.set_help(_('turns the turtle 180 degrees'))  # a help message

        # def_prim takes 3 arguments: the primitive name, the number of
        # of arguments, 0 in this case, and the function to call.
        # We are using a special method, 'set', that will update the label
        # of the heading block as well as the heading itself. _prim_set
        # also takes arguments: the name of the block whose label needs to
        # be updated, the function call to change the value, and the new
        # value, in the case, the current heading + 180
        self.tw.lc._def_prim('uturn', 0, 
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'heading', self.tw.canvas.seth, self.tw.canvas.heading + 180))
        b.add_prim()

That's it. When you next run Turtle Art, you will have a 'uturn' block
on the Turtle Palette.

Adding a new palette is simply a matter of:
        p = Palette('turtle', ["#00FF00", "#00A000"])  # assign name and colors
        p.set_help(_('Palette of turtle commands'))  # and a help message
        p.add_palette()

However you will have to create icons for the palette-selector
buttons. These are kept in the icons subdirectory. You need two icons:
yourpalettenameoff.svg and yourpalettenameon.svg, where
yourpalettename is the same string as the entry you added to the
PALETTE_NAMES list. Note that the icons should be the same size
(55x55) as the others. This is the default icon size for Sugar
toolbars.

"""

from time import time
from math import sqrt
from random import uniform

from gettext import gettext as _

from taprimitive import Palette, Primitive
from talogo import PLUGIN_DICTIONARY, VALUE_BLOCKS, logoerror
from taconstants import DEFAULT_SCALE, CONSTANTS, BLACK, WHITE
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
    """ a class for storing the palettes of blocks """

    def __init__(self, parent):
        self.tw = parent

        p = Palette('turtle', ["#00FF00", "#00A000"])
        p.set_help(_('Palette of turtle commands'))
        p.add_palette()
        self._turtle_palette()

        p = Palette('pen', ["#00FFFF", "#00A0A0"])
        p.set_help(_('Palette of pen commands'))
        p.add_palette()
        self._pen_palette()

        p = Palette('colors', ["#00FFFF", "#00A0A0"])
        p.set_help(_('Palette of pen colors'))
        p.add_palette()
        self._color_palette()

        p = Palette('numbers', ["#FF00FF", "#A000A0"])
        p.set_help(_('Palette of numeric operators'))
        p.add_palette()
        self._numbers_palette()

        p = Palette('flow', ["#FFC000", "#A08000"])
        p.set_help(_('Palette of flow operators'))
        p.add_palette()
        self._flow_palette()

        p = Palette('blocks', ["#FFFF00", "#A0A000"])
        p.set_help(_('Palette of variable blocks'))
        p.add_palette()
        self._blocks_palette()

        p = Palette('trash', ["#FFFF00", "#A0A000"])
        p.add_palette()
        self._trash_palette()

    # Palette definitions

    def _turtle_palette(self):
        b = Primitive('forward')
        b.set_palette('turtle')
        b.set_style('basic-style-1arg')
        b.set_label(_('forward'))
        b.set_prim_name('forward')
        b.set_default(100)
        b.set_help(_('moves turtle forward'))
        PLUGIN_DICTIONARY['move'] = self._prim_move
        self.tw.lc._def_prim('forward', 1, 
                             lambda self, x: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.forward, x))
        b.add_prim()

        b = Primitive('back')
        b.set_palette('turtle')
        b.set_style('basic-style-1arg')
        b.set_label(_('back'))
        b.set_prim_name('back')
        b.set_default(100)
        b.set_help(_('moves turtle backward'))
        self.tw.lc._def_prim('back', 1,
                             lambda self, x: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.forward, -x))
        b.add_prim()

        b = Primitive('clean')
        b.set_palette('turtle')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('clean'))
        b.set_prim_name('clean')
        b.set_help(_('clears the screen and reset the turtle'))
        PLUGIN_DICTIONARY['clean'] = self._prim_clear
        self.tw.lc._def_prim('clean', 0, 
                             lambda self: PLUGIN_DICTIONARY['clean']())
        b.add_prim()

        b = Primitive('left')
        b.set_palette('turtle')
        b.set_style('basic-style-1arg')
        b.set_label(_('left'))
        b.set_prim_name('left')
        b.set_default(90)
        b.set_help(_('turns turtle counterclockwise (angle in degrees)'))
        PLUGIN_DICTIONARY['right'] = self._prim_right
        self.tw.lc._def_prim('right', 1, 
                             lambda self, x: PLUGIN_DICTIONARY['right'](-x))
        b.add_prim()

        b = Primitive('right')
        b.set_palette('turtle')
        b.set_style('basic-style-1arg')
        b.set_label(_('right'))
        b.set_prim_name('right')
        b.set_default(90)
        b.set_help(_('turns turtle clockwise (angle in degrees)'))
        self.tw.lc._def_prim('right', 1, 
                             lambda self, x: PLUGIN_DICTIONARY['right'](x))
        b.add_prim()

        b = Primitive('arc')
        b.set_palette('turtle')
        b.set_style('basic-style-2arg')
        b.set_label([_('arc'), _('angle'), _('radius')])
        b.set_prim_name('arc')
        b.set_default([90, 100])
        b.set_help(_('moves turtle along an arc'))
        PLUGIN_DICTIONARY['arc'] = self._prim_arc
        self.tw.lc._def_prim('arc', 2, 
                             lambda self, x, y: PLUGIN_DICTIONARY['arc'](
                self.tw.canvas.arc, x, y))
        b.add_prim()

        b = Primitive('setxy2')
        b.set_palette('turtle')
        b.set_style('basic-style-2arg')
        b.set_label([_('set xy'), _('x'), _('y')])
        b.set_prim_name('setxy2')
        b.set_default([0, 0])
        b.set_help(_('moves turtle to position xcor, ycor; (0, 0) is in the center of the screen.'))
        self.tw.lc._def_prim('setxy2', 2, 
                             lambda self, x, y: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.setxy, x, y))
        b.add_prim()

        b = Primitive('setxy')  # Depreciated
        b.set_style('basic-style-2arg')
        b.set_label([_('set xy'), _('x'), _('y')])
        b.set_prim_name('setxy')
        b.set_default([0, 0])
        b.set_help(_('moves turtle to position xcor, ycor; (0, 0) is in the center of the screen.'))
        self.tw.lc._def_prim('setxy', 2, 
                             lambda self, x, y: PLUGIN_DICTIONARY['move'](
                self.tw.canvas.setxy, x, y, pendown=False))
        b.add_prim()

        b = Primitive('seth')
        b.set_palette('turtle')
        b.set_style('basic-style-1arg')
        b.set_label(_('set heading'))
        b.set_prim_name('seth')
        b.set_default(0)
        b.set_help(_('sets the heading of the turtle (0 is towards the top of the screen.)'))
        PLUGIN_DICTIONARY['set'] = self._prim_set
        self.tw.lc._def_prim('seth', 1, 
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'heading', self.tw.canvas.seth, x))
        b.add_prim()

        b = Primitive('xcor')
        b.set_palette('turtle')
        b.set_style('box-style')
        b.set_label(_('xcor'))
        b.set_help(_('holds current x-coordinate value of the turtle (can be used in place of a number block)'))
        b.set_value_block(True)
        b.set_prim_name('xcor')
        self.tw.lc._def_prim(
            'xcor', 0, lambda self: self.tw.canvas.xcor / self.tw.coord_scale)
        b.add_prim()

        b = Primitive('ycor')
        b.set_palette('turtle')
        b.set_style('box-style')
        b.set_label(_('ycor'))
        b.set_help(_('holds current y-coordinate value of the turtle (can be used in place of a number block)'))
        b.set_value_block(True)
        b.set_prim_name('ycor')
        self.tw.lc._def_prim(
            'ycor', 0, lambda self: self.tw.canvas.ycor / self.tw.coord_scale)
        b.add_prim()

        b = Primitive('heading')
        b.set_palette('turtle')
        b.set_style('box-style')
        b.set_label(_('heading'))
        b.set_help(_('holds current heading value of the turtle (can be used in place of a number block)'))
        b.set_value_block(True)
        b.set_prim_name('heading')
        self.tw.lc._def_prim(
            'heading', 0, lambda self: self.tw.canvas.heading)
        b.add_prim()

    def _pen_palette(self):
        b = Primitive('penup')
        b.set_palette('pen')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('pen up'))
        b.set_prim_name('penup')
        b.set_help(_('Turtle will not draw when moved.'))
        self.tw.lc._def_prim('penup', 0, 
                             lambda self: self.tw.canvas.setpen(False))
        b.add_prim()

        b = Primitive('pendown')
        b.set_palette('pen')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('pen down'))
        b.set_prim_name('pendown')
        b.set_help(_('Turtle will draw when moved.'))
        self.tw.lc._def_prim('pendown', 0, 
                             lambda self: self.tw.canvas.setpen(True))
        b.add_prim()

        b = Primitive('setpensize')
        b.set_palette('pen')
        b.set_style('basic-style-1arg')
        b.set_label(_('set pen size'))
        b.set_prim_name('setpensize')
        b.set_default(5)
        b.set_help(_('sets size of the line drawn by the turtle'))
        self.tw.lc._def_prim('setpensize', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'pensize', self.tw.canvas.setpensize, x))
        b.add_prim()

        b = Primitive('fillscreen')
        b.set_palette('pen')
        b.set_style('basic-style-2arg')
        b.set_label([_('fill screen'), _('color'), _('shade')])
        b.set_prim_name('fillscreen')
        b.set_default([60, 80])
        b.set_help(_('fills the background with (color, shade)'))
        self.tw.lc._def_prim('fillscreen', 2, 
                             lambda self, x, y: self.tw.canvas.fillscreen(x, y))
        b.add_prim()

        b = Primitive('pensize')
        b.set_palette('pen')
        b.set_style('box-style')
        b.set_label(_('pen size'))
        b.set_help(_('holds current pen size (can be used in place of a number block)'))
        b.set_value_block(True)
        b.set_prim_name('pensize')
        self.tw.lc._def_prim('pensize', 0, lambda self: self.tw.canvas.pensize)
        b.add_prim()

        b = Primitive('startfill')
        b.set_palette('pen')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('start fill'))
        b.set_prim_name('startfill')
        b.set_help(_('starts filled polygon (used with end fill block)'))
        self.tw.lc._def_prim('startfill', 0, 
                             lambda self: self.tw.canvas.start_fill())
        b.add_prim()

        b = Primitive('stopfill')
        b.set_palette('pen')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('end fill'))
        b.set_prim_name('stopfill')
        b.set_help(_('completes filled polygon (used with start fill block)'))
        self.tw.lc._def_prim('stopfill', 0, 
                             lambda self: self.tw.canvas.stop_fill())
        b.add_prim()

    def _color_palette(self):
        b = Primitive('setcolor')
        b.set_palette('colors')
        b.set_style('basic-style-1arg')
        b.set_label(_('set color'))
        b.set_prim_name('setcolor')
        b.set_default(0)
        b.set_help(_('sets color of the line drawn by the turtle'))
        self.tw.lc._def_prim('setcolor', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'color', self.tw.canvas.setcolor, x))
        b.add_prim()

        b = Primitive('settextcolor')  # depreciated
        b.set_style('basic-style-1arg')
        b.set_label(_('set text color'))
        b.set_prim_name('settextcolor')
        b.set_default(0)
        b.set_help(_('sets color of text drawn by the turtle'))
        self.tw.lc._def_prim('settextcolor', 1,
                             lambda self, x: self.tw.canvas.settextcolor(x))
        b.add_prim()

        b = Primitive('setshade')
        b.set_palette('colors')
        b.set_style('basic-style-1arg')
        b.set_label(_('set shade'))
        b.set_prim_name('setshade')
        b.set_default(50)
        b.set_help(_('sets shade of the line drawn by the turtle'))
        self.tw.lc._def_prim('setshade', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'shade', self.tw.canvas.setshade, x))
        b.add_prim()

        b = Primitive('setgray')
        b.set_palette('colors')
        b.set_style('basic-style-1arg')
        b.set_label(_('set gray'))
        b.set_prim_name('setgray')
        b.set_default(100)
        b.set_help(_('sets gray level of the line drawn by the turtle'))
        self.tw.lc._def_prim('setgray', 1,
                             lambda self, x: PLUGIN_DICTIONARY['set'](
                'gray', self.tw.canvas.setgray, x))
        b.add_prim()

        b = Primitive('color')
        b.set_palette('colors')
        b.set_style('box-style')
        b.set_label(_('color'))
        b.set_help(_('holds current pen color (can be used in place of a number block)'))
        b.set_value_block(True)
        b.set_prim_name('color')
        self.tw.lc._def_prim('color', 0, lambda self: self.tw.canvas.color)
        b.add_prim()

        b = Primitive('shade')
        b.set_palette('colors')
        b.set_style('box-style')
        b.set_label(_('shade'))
        b.set_help(_('holds current pen shade'))
        b.set_value_block(True)
        b.set_prim_name('shade')
        self.tw.lc._def_prim('shade', 0, lambda self: self.tw.canvas.shade)
        b.add_prim()

        b = Primitive('gray')
        b.set_palette('colors')
        b.set_style('box-style')
        b.set_label(_('gray'))
        b.set_help(_('holds current gray level (can be used in place of a number block)'))
        b.set_value_block(True)
        b.set_prim_name('gray')
        self.tw.lc._def_prim('gray', 0, lambda self: self.tw.canvas.gray)
        b.add_prim()

        self._make_constant('red', 'colors', CONSTANTS['red'])
        self._make_constant('orange', 'colors', CONSTANTS['orange'])
        self._make_constant('yellow', 'colors', CONSTANTS['yellow'])
        self._make_constant('green', 'colors', CONSTANTS['green'])
        self._make_constant('cyan', 'colors', CONSTANTS['cyan'])
        self._make_constant('blue', 'colors', CONSTANTS['blue'])
        self._make_constant('purple', 'colors', CONSTANTS['purple'])
        self._make_constant('white', 'colors', WHITE)
        self._make_constant('black', 'colors', BLACK)

    def _numbers_palette(self):
        b = Primitive('plus2')
        b.set_palette('numbers')
        b.set_style('number-style')
        b.set_label('+')
        b.set_special_name(_('plus'))
        b.set_prim_name('plus')
        b.set_help(_('adds two alphanumeric inputs'))
        PLUGIN_DICTIONARY['plus'] = self._prim_plus
        self.tw.lc._def_prim(
            'plus', 2, lambda self, x, y: PLUGIN_DICTIONARY['plus'](x, y))
        b.add_prim()

        b = Primitive('minus2')
        b.set_palette('numbers')
        b.set_style('number-style-porch')
        b.set_label('–')
        b.set_special_name(_('minus'))
        b.set_prim_name('minus')
        b.set_help(_('subtracts bottom numeric input from top numeric input'))
        PLUGIN_DICTIONARY['minus'] = self._prim_minus
        self.tw.lc._def_prim(
            'minus', 2, lambda self, x, y: PLUGIN_DICTIONARY['minus'](x, y))
        b.add_prim()

        b = Primitive('product2')
        b.set_palette('numbers')
        b.set_style('number-style')
        b.set_label('×')
        b.set_special_name(_('multiply'))
        b.set_prim_name('product')
        b.set_help(_('multiplies two numeric inputs'))
        PLUGIN_DICTIONARY['product'] = self._prim_product
        self.tw.lc._def_prim(
            'product', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['product'](x, y))
        b.add_prim()

        b = Primitive('division2')
        b.set_palette('numbers')
        b.set_style('number-style-porch')
        b.set_label('/')
        b.set_special_name(_('divide'))
        b.set_prim_name('division')
        b.set_help(_('divides top numeric input (numerator) by bottom numeric input (denominator)'))
        PLUGIN_DICTIONARY['division'] = self._prim_careful_divide
        self.tw.lc._def_prim(
            'division', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['division'](x, y))
        b.add_prim()

        b = Primitive('identity2')
        b.set_palette('numbers')
        b.set_style('number-style-1strarg')
        b.set_label('←')
        b.set_special_name(_('identity'))
        b.set_prim_name('id')
        b.set_help(_('identity operator used for extending blocks'))
        PLUGIN_DICTIONARY['id'] = self._prim_identity
        self.tw.lc._def_prim('id', 1,
                             lambda self, x: PLUGIN_DICTIONARY['id'](x))
        b.add_prim()

        b = Primitive('remainder2')
        b.set_palette('numbers')
        b.set_style('number-style-porch')
        b.set_label(_('mod'))
        b.set_special_name(_('mod'))
        b.set_prim_name('remainder')
        b.set_help(_('modular (remainder) operator'))
        PLUGIN_DICTIONARY['remainder'] = self._prim_mod
        self.tw.lc._def_prim('remainder', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['remainder'](x, y))
        b.add_prim()

        b = Primitive('sqrt')
        b.set_palette('numbers')
        b.set_style('number-style-1arg')
        b.set_label(_('√'))
        b.set_special_name(_('square root'))
        b.set_prim_name('sqrt')
        b.set_help(_('calculates square root'))
        PLUGIN_DICTIONARY['sqrt'] = self._prim_sqrt
        self.tw.lc._def_prim('sqrt', 1,
                             lambda self, x: PLUGIN_DICTIONARY['sqrt'](x))
        b.add_prim()

        b = Primitive('random')
        b.set_palette('numbers')
        b.set_style('number-style-block')
        b.set_label([_('random'), _('min'), _('max')])
        b.set_default([0, 100])
        b.set_prim_name('random')
        b.set_help(_('returns random number between minimum (top) and maximum (bottom) values'))
        PLUGIN_DICTIONARY['random'] = self._prim_random
        self.tw.lc._def_prim(
            'random', 2, lambda self, x, y: PLUGIN_DICTIONARY['random'](x, y))
        b.add_prim()

        b = Primitive('number')
        b.set_palette('numbers')
        b.set_style('box-style')
        b.set_label('100')
        b.set_default(100)
        b.set_special_name(_('number'))
        b.set_help(_('used as numeric input in mathematic operators'))
        b.add_prim()

        b = Primitive('greater2')
        b.set_palette('numbers')
        b.set_style('compare-porch-style')
        b.set_label('>')
        b.set_special_name(_('greater than'))
        b.set_prim_name('greater?')
        b.set_help(_('logical greater-than operator'))
        PLUGIN_DICTIONARY['more'] = self._prim_more
        self.tw.lc._def_prim(
            'greater?', 2, lambda self, x, y: PLUGIN_DICTIONARY['more'](x, y))
        b.add_prim()

        b = Primitive('less2')
        b.set_palette('numbers')
        b.set_style('compare-porch-style')
        b.set_label('<')
        b.set_special_name(_('less than'))
        b.set_prim_name('less?')
        b.set_help(_('logical less-than operator'))
        PLUGIN_DICTIONARY['less'] = self._prim_less
        self.tw.lc._def_prim(
            'less?', 2, lambda self, x, y: PLUGIN_DICTIONARY['less'](x, y))
        b.add_prim()

        b = Primitive('equal2')
        b.set_palette('numbers')
        b.set_style('compare-style')
        b.set_label('=')
        b.set_special_name(_('equal'))
        b.set_prim_name('equal?')
        b.set_help(_('logical equal-to operator'))
        PLUGIN_DICTIONARY['equal'] = self._prim_equal
        self.tw.lc._def_prim(
            'equal?', 2, lambda self, x, y: PLUGIN_DICTIONARY['equal'](x, y))
        b.add_prim()

        b = Primitive('not')
        b.set_palette('numbers')
        b.set_style('not-style')
        b.set_label(_('not'))
        b.set_prim_name('not')
        b.set_help(_('logical NOT operator'))
        self.tw.lc._def_prim('not', 1, lambda self, x: not x)
        b.add_prim()

        b = Primitive('and2')
        b.set_palette('numbers')
        b.set_style('boolean-style')
        b.set_label(_('and'))
        b.set_prim_name('and')
        b.set_special_name(_('and'))
        b.set_help(_('logical AND operator'))
        self.tw.lc._def_prim('not', 2, lambda self, x, y: x & y)
        b.add_prim()

        b = Primitive('or2')
        b.set_palette('numbers')
        b.set_style('boolean-style')
        b.set_label(_('or'))
        b.set_prim_name('or')
        b.set_special_name(_('or'))
        b.set_help(_('logical OR operator'))
        self.tw.lc._def_prim('not', 2, lambda self, x, y: x | y)
        b.add_prim()

    def _flow_palette(self):
        b = Primitive('wait')
        b.set_palette('flow')
        b.set_style('basic-style-1arg')
        b.set_label(_('wait'))
        b.set_prim_name('wait')
        b.set_default(1)
        b.set_help(_('pauses program execution a specified number of seconds'))
        PLUGIN_DICTIONARY['wait'] = self._prim_wait
        self.tw.lc._def_prim('wait', 1, PLUGIN_DICTIONARY['wait'], True)
        b.add_prim()

        b = Primitive('forever')
        b.set_palette('flow')
        b.set_style('flow-style')
        b.set_label(_('forever'))
        b.set_prim_name('forever')
        b.set_default([None, 'vspace'])
        b.set_help(_('loops forever'))
        PLUGIN_DICTIONARY['forever'] = self._prim_forever
        self.tw.lc._def_prim('forever', 1, PLUGIN_DICTIONARY['forever'], True)
        b.add_prim()

        b = Primitive('repeat')
        b.set_palette('flow')
        b.set_style('flow-style-1arg')
        b.set_label([' ', _('repeat')])
        b.set_prim_name('repeat')
        b.set_default([4, None, 'vspace'])
        b.set_special_name(_('repeat'))
        b.set_help(_('loops specified number of times'))
        PLUGIN_DICTIONARY['repeat'] = self._prim_repeat
        self.tw.lc._def_prim('repeat', 2, PLUGIN_DICTIONARY['repeat'], True)
        b.add_prim()

        b = Primitive('if')
        b.set_palette('flow')
        b.set_style('flow-style-boolean')
        b.set_label([' ', _('if'), _('then')])
        b.set_prim_name('if')
        b.set_default([None, None, 'vspace'])
        b.set_special_name(_('if then'))
        b.set_help(_('if-then operator that uses boolean operators from Numbers palette'))
        PLUGIN_DICTIONARY['if'] = self._prim_if
        self.tw.lc._def_prim('if', 2, PLUGIN_DICTIONARY['if'], True)
        b.add_prim()

        b = Primitive('ifelse')
        b.set_palette('flow')
        b.set_style('flow-style-else')
        b.set_label([' ', _('if'), _('then else')])
        b.set_prim_name('ifelse')
        b.set_default([None, 'vspace', None, 'vspace'])
        b.set_special_name(_('if then else'))
        b.set_help(_('if-then-else operator that uses boolean operators from Numbers palette'))
        PLUGIN_DICTIONARY['ifelse'] = self._prim_ifelse
        self.tw.lc._def_prim('ifelse', 3, PLUGIN_DICTIONARY['ifelse'], True)
        b.add_prim()

        b = Primitive('hspace')
        b.set_palette('flow')
        b.set_style('flow-style-tail')
        b.set_label(' ')
        b.set_prim_name('nop')
        b.set_special_name(_('horizontal space'))
        b.set_help(_('jogs stack right'))
        self.tw.lc._def_prim('nop', 0, lambda self: None)
        b.add_prim()

        b = Primitive('vspace')
        b.set_palette('flow')
        b.set_style('basic-style-extended-vertical')
        b.set_label(' ')
        b.set_prim_name('nop')
        b.set_special_name(_('vertical space'))
        b.set_help(_('jogs stack down'))
        self.tw.lc._def_prim('nop', 0, lambda self: None)
        b.add_prim()

        b = Primitive('stopstack')
        b.set_palette('flow')
        b.set_style('basic-style-tail')
        b.set_label(_('stop action'))
        b.set_prim_name('stopstack')
        b.set_help(_('stops current action'))
        PLUGIN_DICTIONARY['stopstack'] = self._prim_stopstack
        self.tw.lc._def_prim('stopstack', 0,
                             lambda self: PLUGIN_DICTIONARY['stopstack']())
        b.add_prim()

    def _blocks_palette(self):
        b = Primitive('start')
        b.set_palette('blocks')
        b.set_style('basic-style-head')
        b.set_label(_('start'))
        b.set_prim_name('start')
        b.set_help(_('connects action to toolbar run buttons'))
        PLUGIN_DICTIONARY['start'] = self._prim_start
        self.tw.lc._def_prim('start', 0,
                             lambda self: PLUGIN_DICTIONARY['start']())
        b.add_prim()

        b = Primitive('storeinbox1')
        b.set_palette('blocks')
        b.set_style('basic-style-1arg')
        b.set_label(_('store in box 1'))
        b.set_prim_name('storeinbox1')
        b.set_default(100)
        b.set_help(_('stores numeric value in Variable 1'))
        PLUGIN_DICTIONARY['setbox'] = self._prim_setbox
        self.tw.lc._def_prim('storeinbox1', 1,
                             lambda self, x: PLUGIN_DICTIONARY['setbox'](
                'box1', None, x))
        b.add_prim()

        b = Primitive('storeinbox2')
        b.set_palette('blocks')
        b.set_style('basic-style-1arg')
        b.set_label(_('store in box 2'))
        b.set_prim_name('storeinbox2')
        b.set_default(100)
        b.set_help(_('stores numeric value in Variable 2'))
        self.tw.lc._def_prim('storeinbox2', 1,
                             lambda self, x: PLUGIN_DICTIONARY['setbox'](
                'box2', None, x))
        b.add_prim()

        b = Primitive('string')
        b.set_palette('blocks')
        b.set_style('box-style')
        b.set_label(_('text'))
        b.set_default(_('text'))
        b.set_special_name('')
        b.set_help(_('string value'))
        b.add_prim()

        b = Primitive('box1')
        b.set_palette('blocks')
        b.set_style('box-style')
        b.set_label(_('box 1'))
        b.set_prim_name('box1')
        b.set_help(_('Variable 1 (numeric value)'))
        b.set_value_block(True)
        self.tw.lc._def_prim('box1', 0, lambda self: self.tw.lc.boxes['box1'])
        b.add_prim()

        b = Primitive('box2')
        b.set_palette('blocks')
        b.set_style('box-style')
        b.set_label(_('box 2'))
        b.set_prim_name('box2')
        b.set_help(_('Variable 2 (numeric value)'))
        b.set_value_block(True)
        self.tw.lc._def_prim('box2', 0, lambda self: self.tw.lc.boxes['box2'])
        b.add_prim()

        b = Primitive('box')
        b.set_palette('blocks')
        b.set_style('number-style-1strarg')
        b.set_label(_('box'))
        b.set_prim_name('box')
        b.set_default(_('my box'))
        b.set_help(_('named variable (numeric value)'))
        PLUGIN_DICTIONARY['box'] = self._prim_box
        self.tw.lc._def_prim('box', 1,
                             lambda self, x: PLUGIN_DICTIONARY['box'](x))
        b.add_prim()

        b = Primitive('storein')
        b.set_palette('blocks')
        b.set_style('basic-style-2arg')
        b.set_label([_('store in'), _('box'), _('value')])
        b.set_prim_name('storeinbox')
        b.set_default([_('my box'), 100])
        b.set_help(_('stores numeric value in named variable'))
        self.tw.lc._def_prim('storeinbox', 2,
                             lambda self, x, y: PLUGIN_DICTIONARY['setbox'](
                'box3', x, y))
        b.add_prim()

        b = Primitive('hat')
        b.set_palette('blocks')
        b.set_style('basic-style-head-1arg')
        b.set_label(_('action'))
        b.set_prim_name('nop3')
        b.set_default(_('action'))
        b.set_help(_('top of nameable action stack'))
        self.tw.lc._def_prim('nop3', 1, lambda self, x: None)
        b.add_prim()

        b = Primitive('hat1')
        b.set_palette('blocks')
        b.set_style('basic-style-head')
        b.set_label(_('action 1'))
        b.set_prim_name('nop1')
        b.set_default(_('action 1'))
        b.set_help(_('top of Action 1 stack'))
        self.tw.lc._def_prim('nop1', 0, lambda self: None)
        b.add_prim()

        b = Primitive('hat2')
        b.set_palette('blocks')
        b.set_style('basic-style-head')
        b.set_label(_('action 2'))
        b.set_prim_name('nop2')
        b.set_default(_('action 2'))
        b.set_help(_('top of Action 2 stack'))
        self.tw.lc._def_prim('nop2', 0, lambda self: None)
        b.add_prim()

        b = Primitive('stack')
        b.set_palette('blocks')
        b.set_style('basic-style-1arg')
        b.set_label(_('action'))
        b.set_prim_name('stack')
        b.set_default(_('action'))
        b.set_help(_('invokes named action stack'))
        PLUGIN_DICTIONARY['stack'] = self._prim_stack
        self.tw.lc._def_prim('stack', 1, PLUGIN_DICTIONARY['stack'], True)
        b.add_prim()

        b = Primitive('stack1')
        b.set_palette('blocks')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('action 1'))
        b.set_prim_name('stack1')
        b.set_default(_('action 1'))
        b.set_help(_('invokes Action 1 stack'))
        PLUGIN_DICTIONARY['stack1'] = self._prim_stack1
        self.tw.lc._def_prim('stack1', 0, PLUGIN_DICTIONARY['stack1'], True)
        b.add_prim()

        b = Primitive('stack2')
        b.set_palette('blocks')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('action 2'))
        b.set_prim_name('stack2')
        b.set_default(_('action 2'))
        b.set_help(_('invokes Action 2 stack'))
        PLUGIN_DICTIONARY['stack2'] = self._prim_stack2
        self.tw.lc._def_prim('stack2', 0, PLUGIN_DICTIONARY['stack2'], True)
        b.add_prim()

    def _trash_palette(self):
        b = Primitive('empty')
        b.set_palette('trash')
        b.set_style('basic-style-tail')
        b.set_label(_('empty trash'))
        b.set_help(_("permanently deletes items in trash"))
        b.add_prim()

        b = Primitive('restoreall')
        b.set_palette('trash')
        b.set_style('basic-style-head')
        b.set_label(_('restore all'))
        b.set_help(_("restore all blocks from trash"))
        b.add_prim()

    # Block primitives

    def _prim_arc(self, cmd, value1, value2):
        """ Turtle draws an arc of degree, radius """
        cmd(float(value1), float(value2))
        self.tw.lc.update_label_value(
            'xcor', self.tw.canvas.xcor / self.tw.coord_scale)
        self.tw.lc.update_label_value(
            'ycor', self.tw.canvas.ycor / self.tw.coord_scale)
        self.tw.lc.update_label_value('heading', self.tw.canvas.heading)
        if len(self.lc.tw.value_blocks['see']) > 0:
            self.lc.tw.see()

    def _prim_box(self, x):
        """ Retrieve value from named box """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        try:
            return self.tw.lc.boxes['box3' + str(x)]
        except KeyError:
            raise logoerror("#emptybox")

    def _prim_clear(self):
        """ Clear screen """
        if self.tw.gst_available:
            from tagplay import stop_media
            # stop_media(self)  # TODO: gplay variable
        self.tw.canvas.clearscreen()
        self.tw.lc.scale = DEFAULT_SCALE  # TODO: move to lc method
        self.tw.lc.hidden_turtle = None
        self.tw.lc._start_time = time()
        for name in VALUE_BLOCKS:
            self.tw.lc.update_label_value(name)

    def _prim_forever(self, blklist):
        """ Do list forever """
        while True:
            self.tw.lc._icall(self.tw.lc._evline, blklist[:])
            yield True
            if self.tw.lc.procstop:
                break
        self.tw.lc._ireturn()
        yield True

    def _prim_if(self, boolean, blklist):
        """ If bool, do list """
        if boolean:
            self.tw.lc._icall(self.tw.lc._evline, blklist[:])
            yield True
        self.tw.lc._ireturn()
        yield True

    def _prim_ifelse(self, boolean, list1, list2):
        """ If bool, do list1, else do list2 """
        if boolean:
            self.tw.lc._ijmp(self.tw.lc._evline, list1[:])
            yield True
        else:
            self.tw.lc._ijmp(self.tw.lc._evline, list2[:])
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
        if len(self.tw.lc.value_blocks['see']) > 0:
            self.tw.lc.see()

    def _prim_repeat(self, num, blklist):
        """ Repeat list num times. """
        num = self.tw.lc._int(num)
        for i in range(num):
            self.tw.lc._icall(self.tw.lc._evline, blklist[:])
            yield True
            if self.tw.lc.procstop:
                break
        self.tw.lc._ireturn()
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
        self.tw.lc._icall(self.tw.lc._evline,
                          self.tw.lc.stacks['stack3' + str(x)][:])
        yield True
        self.tw.lc.procstop = False
        self.tw.lc._ireturn()
        yield True

    def _prim_stack1(self):
        """ Process Stack 1 """
        if self.tw.lc.stacks['stack1'] is None:
            raise logoerror("#nostack")
        self.tw.lc._icall(self.tw.lc._evline,
                          self.tw.lc.stacks['stack1'][:])
        yield True
        self.tw.lc.procstop = False
        self.tw.lc._ireturn()
        yield True

    def _prim_stack2(self):
        """ Process Stack 2 """
        if self.tw.lc.stacks['stack2'] is None:
            raise logoerror("#nostack")
        self.tw.lc._icall(self.tw.lc._evline, self.tw.lc.stacks['stack2'][:])
        yield True
        self.tw.lc.procstop = False
        self.tw.lc._ireturn()
        yield True

    def _prim_start(self):
        """ Start block: recenter """
        if self.tw.running_sugar:
            self.tw.activity.recenter()

    def _prim_stopstack(self):
        """ Stop execution of a stack """
        self.tw.lc.procstop = True

    def _prim_wait(self, time):
        """ Show the turtle while we wait """
        self.tw.active_turtle.show()
        endtime = _millisecond() + time * 1000.
        while _millisecond() < endtime:
            yield True
        self.tw.active_turtle.hide()
        self.tw.lc._ireturn()
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
        b = Primitive(block_name)
        b.set_palette(palette_name)
        b.set_style('box-style')
        b.set_label(_(block_name))
        b.set_prim_name(block_name)
        self.tw.lc._def_prim(block_name, 0, lambda self: constant)
        b.add_prim()
