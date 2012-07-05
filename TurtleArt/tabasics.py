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


Adding a new palette is simply a matter of:
    palette = make_palette('mypalette',  # the name of your palette
                           colors=["#00FF00", "#00A000"],
                           help_string=_('Palette of my custom commands'))

For example, if we want to add a new turtle command, 'uturn', we'd use the
add_block method in the Palette class.
    palette.add_block('uturn',  # the name of your block
                      style='basic-style',  # the block style
                      label=_('u turn'),  # the label for the block
                      prim_name='uturn',  # code reference (see below)
                      help_string=_('turns the turtle 180 degrees'))

    # Next, you need to define what your block will do:
    # def_prim takes 3 arguments: the primitive name, the number of
    # arguments -- 0 in this case -- and the function to call -- in this
    # case, the canvas.seth function to set the heading.
    self.tw.lc.def_prim('uturn', 0,
        lambda self: self.tw.canvas.seth(self.tw.canvas.heading + 180))

That's it. When you next run Turtle Art, you will have a 'uturn' block
on the 'mypalette' palette.

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

from tapalette import make_palette, define_logo_function
from talogo import primitive_dictionary, logoerror
from tautils import convert, chr_to_ord, round_int, strtype
from taconstants import BLACK, WHITE, CONSTANTS, XO30


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

        self._turtle_palette()

        self._pen_palette()

        self._color_palette()

        self._numbers_palette()

        self._flow_palette()

        self._blocks_palette()

        self._trash_palette()

    # Palette definitions

    def _turtle_palette(self):
        """ The basic Turtle Art turtle palette """

        palette = make_palette('turtle',
                               colors=["#00FF00", "#00A000"],
                               help_string=_('Palette of turtle commands'))

        primitive_dictionary['move'] = self._prim_move
        palette.add_block('forward',
                          style='basic-style-1arg',
                          label=_('forward'),
                          prim_name='forward',
                          default=100,
                          logo_command='forward',
                          help_string=_('moves turtle forward'))
        self.tw.lc.def_prim('forward', 1,
                             lambda self, x: primitive_dictionary['move'](
                self.tw.canvas.forward, x))

        palette.add_block('back',
                          style='basic-style-1arg',
                          label=_('back'),
                          prim_name='back',
                          default=100,
                          logo_command='back',
                          help_string=_('moves turtle backward'))
        self.tw.lc.def_prim('back', 1,
                             lambda self, x: primitive_dictionary['move'](
                self.tw.canvas.forward, -x))

        primitive_dictionary['clean'] = self.tw.lc.prim_clear
        palette.add_block('clean',
                          style='basic-style-extended-vertical',
                          label=_('clean'),
                          prim_name='clean',
                          logo_command='clean',
                          help_string=_('clears the screen and reset the \
turtle'))
        self.tw.lc.def_prim('clean', 0,
                             lambda self: primitive_dictionary['clean']())

        primitive_dictionary['right'] = self._prim_right
        palette.add_block('left',
                          style='basic-style-1arg',
                          label=_('left'),
                          prim_name='left',
                          default=90,
                          logo_command='left',
                          help_string=_('turns turtle counterclockwise (angle \
in degrees)'))
        self.tw.lc.def_prim('left', 1,
                             lambda self, x: primitive_dictionary['right'](-x))

        palette.add_block('right',
                          style='basic-style-1arg',
                          label=_('right'),
                          prim_name='right',
                          default=90,
                          logo_command='right',
                          help_string=_('turns turtle clockwise (angle in \
degrees)'))
        self.tw.lc.def_prim('right', 1,
                             lambda self, x: primitive_dictionary['right'](x))

        primitive_dictionary['arc'] = self._prim_arc
        palette.add_block('arc',
                          style='basic-style-2arg',
                          label=[_('arc'), _('angle'), _('radius')],
                          prim_name='arc',
                          default=[90, 100],
                          logo_command='taarc',
                          help_string=_('moves turtle along an arc'))
        self.tw.lc.def_prim('arc', 2,
                             lambda self, x, y: primitive_dictionary['arc'](
                self.tw.canvas.arc, x, y))
        define_logo_function('taarc', 'to taarc :a :r\rrepeat round :a \
[right 1 forward (0.0175 * :r)]\rend\r')

        palette.add_block('setxy2',
                          style='basic-style-2arg',
                          label=[_('set xy'), _('x'), _('y')],
                          prim_name='setxy2',
                          logo_command='tasetxy',
                          default=[0, 0],
                          help_string=_('moves turtle to position xcor, ycor; \
(0, 0) is in the center of the screen.'))
        self.tw.lc.def_prim('setxy2', 2,
                             lambda self, x, y: primitive_dictionary['move'](
                self.tw.canvas.setxy, x, y))
        define_logo_function('tasetxy', 'to tasetxy :x :y\rsetxy :x :y\rend\r')

        primitive_dictionary['set'] = self._prim_set
        palette.add_block('seth',
                          style='basic-style-1arg',
                          label=_('set heading'),
                          prim_name='seth',
                          default=0,
                          logo_command='seth',
                          help_string=_('sets the heading of the turtle (0 is \
towards the top of the screen.)'))
        self.tw.lc.def_prim('seth', 1,
                             lambda self, x: primitive_dictionary['set'](
                'heading', self.tw.canvas.seth, x))

        palette.add_block('xcor',
                          style='box-style',
                          label=_('xcor'),
                          help_string=_('holds current x-coordinate value of \
the turtle (can be used in place of a number block)'),
                          value_block=True,
                          prim_name='xcor',
                          logo_command='xcor')
        self.tw.lc.def_prim(
            'xcor', 0, lambda self: self.tw.canvas.xcor / self.tw.coord_scale)

        palette.add_block('ycor',
                          style='box-style',
                          label=_('ycor'),
                          help_string=_('holds current y-coordinate value of \
the turtle (can be used in place of a number block)'),
                          value_block=True,
                          prim_name='ycor',
                          logo_command='ycor')
        self.tw.lc.def_prim(
            'ycor', 0, lambda self: self.tw.canvas.ycor / self.tw.coord_scale)

        palette.add_block('heading',
                          style='box-style',
                          label=_('heading'),
                          help_string=_('holds current heading value of the \
turtle (can be used in place of a number block)'),
                          value_block=True,
                          prim_name='heading',
                          logo_command='heading')
        self.tw.lc.def_prim(
            'heading', 0, lambda self: self.tw.canvas.heading)

        palette.add_block('turtle-label',
                          hidden=True,
                          style='blank-style',
                          label=['turtle'])

        # Deprecated
        palette.add_block('setxy',
                          hidden=True,
                          style='basic-style-2arg',
                          label=[_('set xy'), _('x'), _('y')],
                          prim_name='setxy',
                          default=[0, 0],
                          logo_command='tasetxypenup',
                          help_string=_('moves turtle to position xcor, ycor; \
(0, 0) is in the center of the screen.'))
        self.tw.lc.def_prim('setxy', 2,
                             lambda self, x, y: primitive_dictionary['move'](
                self.tw.canvas.setxy, x, y, pendown=False))
        define_logo_function('tasetxypenup', 'to tasetxypenup :x :y\rpenup\r\
setxy :x :y\rpendown\rend\r')

    def _pen_palette(self):
        """ The basic Turtle Art pen palette """

        palette = make_palette('pen',
                               colors=["#00FFFF", "#00A0A0"],
                               help_string=_('Palette of pen commands'))

        palette.add_block('penup',
                          style='basic-style-extended-vertical',
                          label=_('pen up'),
                          prim_name='penup',
                          logo_command='penup',
                          help_string=_('Turtle will not draw when moved.'))
        self.tw.lc.def_prim('penup', 0,
                             lambda self: self.tw.canvas.setpen(False))

        palette.add_block('pendown',
                          style='basic-style-extended-vertical',
                          label=_('pen down'),
                          prim_name='pendown',
                          logo_command='pendown',
                          help_string=_('Turtle will draw when moved.'))
        self.tw.lc.def_prim('pendown', 0,
                             lambda self: self.tw.canvas.setpen(True))

        palette.add_block('setpensize',
                          style='basic-style-1arg',
                          label=_('set pen size'),
                          prim_name='setpensize',
                          default=5,
                          logo_command='setpensize',
                          help_string=_('sets size of the line drawn by the \
turtle'))
        self.tw.lc.def_prim('setpensize', 1,
                             lambda self, x: primitive_dictionary['set'](
                'pensize', self.tw.canvas.setpensize, x))
        define_logo_function('tasetpensize', 'to tasetpensize :a\rsetpensize \
round :a\rend\r')

        palette.add_block('fillscreen',
                          style='basic-style-2arg',
                          label=[_('fill screen'), _('color'), _('shade')],
                          prim_name='fillscreen',
                          default=[60, 80],
                          logo_command='tasetbackground',
                          help_string=_('fills the background with (color, \
shade)'))
        self.tw.lc.def_prim('fillscreen', 2,
            lambda self, x, y: self.tw.canvas.fillscreen(x, y))
        define_logo_function('tasetbackground', 'to tasetbackground :color \
:shade\rtasetshade :shade\rsetbackground :color\rend\r')

        palette.add_block('pensize',
                          style='box-style',
                          label=_('pen size'),
                          help_string=_('holds current pen size (can be used \
in place of a number block)'),
                          value_block=True,
                          prim_name='pensize',
                          logo_command='pensize')
        self.tw.lc.def_prim('pensize', 0, lambda self: self.tw.canvas.pensize)
        define_logo_function('tapensize', 'to tapensize\routput first round \
pensize\rend\r')

        palette.add_block('setcolor',
                          style='basic-style-1arg',
                          label=_('set color'),
                          prim_name='setcolor',
                          default=0,
                          logo_command='tasetpencolor',
                          help_string=_('sets color of the line drawn by the \
turtle'))
        self.tw.lc.def_prim('setcolor', 1,
                             lambda self, x: primitive_dictionary['set'](
                'color', self.tw.canvas.setcolor, x))

        palette.add_block('setshade',
                          style='basic-style-1arg',
                          label=_('set shade'),
                          prim_name='setshade',
                          default=50,
                          logo_command='tasetshade',
                          help_string=_('sets shade of the line drawn by the \
turtle'))
        self.tw.lc.def_prim('setshade', 1,
                             lambda self, x: primitive_dictionary['set'](
                'shade', self.tw.canvas.setshade, x))

        palette.add_block('setgray',
                          style='basic-style-1arg',
                          label=_('set gray'),
                          prim_name='setgray',
                          default=100,
                          help_string=_('sets gray level of the line drawn by \
the turtle'))
        self.tw.lc.def_prim('setgray', 1,
                             lambda self, x: primitive_dictionary['set'](
                'gray', self.tw.canvas.setgray, x))

        palette.add_block('color',
                          style='box-style',
                          label=_('color'),
                          help_string=_('holds current pen color (can be used \
in place of a number block)'),
                          value_block=True,
                          prim_name='color',
                          logo_command='pencolor')
        self.tw.lc.def_prim('color', 0, lambda self: self.tw.canvas.color)

        palette.add_block('shade',
                          style='box-style',
                          label=_('shade'),
                          help_string=_('holds current pen shade'),
                          value_block=True,
                          prim_name='shade',
                          logo_command=':shade')
        self.tw.lc.def_prim('shade', 0, lambda self: self.tw.canvas.shade)

        palette.add_block('gray',
                          style='box-style',
                          label=_('gray'),
                          help_string=_('holds current gray level (can be \
used in place of a number block)'),
                          value_block=True,
                          prim_name='gray')
        self.tw.lc.def_prim('gray', 0, lambda self: self.tw.canvas.gray)

        palette.add_block('startfill',
                          style='basic-style-extended-vertical',
                          label=_('start fill'),
                          prim_name='startfill',
                          help_string=_('starts filled polygon (used with end \
fill block)'))
        self.tw.lc.def_prim('startfill', 0,
                             lambda self: self.tw.canvas.start_fill())

        palette.add_block('stopfill',
                          style='basic-style-extended-vertical',
                          label=_('end fill'),
                          prim_name='stopfill',
                          help_string=_('completes filled polygon (used with \
start fill block)'))
        self.tw.lc.def_prim('stopfill', 0,
                             lambda self: self.tw.canvas.stop_fill())

    def _color_palette(self):
        """ The basic Turtle Art color palette """

        if self.tw.hw == XO30:
            palette = make_palette('pen',
                                   colors=["#00FFFF", "#00A0A0"],
                                   help_string=_('Palette of pen colors'))
        else:
            palette = make_palette('colors',
                                   colors=["#00FFFF", "#00A0A0"],
                                   help_string=_('Palette of pen colors'))

        self._make_constant(palette, 'red', _('red'), CONSTANTS['red'])
        self._make_constant(palette, 'orange', _('orange'),
                            CONSTANTS['orange'])
        self._make_constant(palette, 'yellow', _('yellow'),
                            CONSTANTS['yellow'])
        self._make_constant(palette, 'green', _('green'), CONSTANTS['green'])
        self._make_constant(palette, 'cyan', _('cyan'), CONSTANTS['cyan'])
        self._make_constant(palette, 'blue', _('blue'), CONSTANTS['blue'])
        self._make_constant(palette, 'purple', _('purple'),
                            CONSTANTS['purple'])
        self._make_constant(palette, 'white', _('white'), WHITE)
        self._make_constant(palette, 'black', _('black'), BLACK)

        # deprecated blocks
        palette.add_block('settextcolor',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('set text color'),
                          prim_name='settextcolor',
                          default=0,
                          help_string=_('sets color of text drawn by the \
turtle'))
        self.tw.lc.def_prim('settextcolor', 1,
                             lambda self, x: self.tw.canvas.settextcolor(x))

        palette.add_block('settextsize',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('set text size'),
                          prim_name='settextsize',
                          default=0,
                          help_string=_('sets size of text drawn by the \
turtle'))
        self.tw.lc.def_prim('settextsize', 1,
                             lambda self, x: self.tw.canvas.settextsize(x))

        # In order to map Turtle Art colors to the standard UCB Logo palette,
        # we need to define a somewhat complex set of functions.
        define_logo_function('tacolor', '\
to tasetpalette :i :r :g :b :myshade \r\
make "s ((:myshade - 50) / 50) \r\
ifelse lessp :s 0 [ \r\
make "s (1 + (:s *0.8)) \r\
make "r (:r * :s) \r\
make "g (:g * :s) \r\
make "b (:b * :s) \r\
] [ \
make "s (:s * 0.9) \r\
make "r (:r + ((99-:r) * :s)) \r\
make "g (:g + ((99-:g) * :s)) \r\
make "b (:b + ((99-:b) * :s)) \r\
] \
setpalette :i (list :r :g :b) \r\
end \r\
\
to rgb :myi :mycolors :myshade \r\
make "myr first :mycolors \r\
make "mycolors butfirst :mycolors \r\
make "myg first :mycolors \r\
make "mycolors butfirst :mycolors \r\
make "myb first :mycolors \r\
make "mycolors butfirst :mycolors \r\
tasetpalette :myi :myr :myg :myb :myshade \r\
output :mycolors \r\
end \r\
\
to processcolor :mycolors :myshade \r\
if emptyp :mycolors [stop] \r\
make "i :i + 1 \r\
processcolor (rgb :i :mycolors :myshade) :myshade \r\
end \r\
\
to tasetshade :shade \r\
make "myshade modulo :shade 200 \r\
if greaterp :myshade 99 [make "myshade (199-:myshade)] \r\
make "i 7 \r\
make "mycolors :colors \r\
processcolor :mycolors :myshade \r\
end \r\
\
to tasetpencolor :c \r\
make "color (modulo (round :c) 100) \r\
setpencolor :color + 8 \r\
end \r\
\
make "colors [ \
99  0  0 99  5  0 99 10  0 99 15  0 99 20  0 \
99 25  0 99 30  0 99 35  0 99 40  0 99 45  0 \
99 50  0 99 55  0 99 60  0 99 65  0 99 70  0 \
99 75  0 99 80  0 99 85  0 99 90  0 99 95  0 \
99 99  0 90 99  0 80 99  0 70 99  0 60 99  0 \
50 99  0 40 99  0 30 99  0 20 99  0 10 99  0 \
 0 99  0  0 99  5  0 99 10  0 99 15  0 99 20 \
 0 99 25  0 99 30  0 99 35  0 99 40  0 99 45 \
 0 99 50  0 99 55  0 99 60  0 99 65  0 99 70 \
 0 99 75  0 99 80  0 99 85  0 99 90  0 99 95 \
 0 99 99  0 95 99  0 90 99  0 85 99  0 80 99 \
 0 75 99  0 70 99  0 65 99  0 60 99  0 55 99 \
 0 50 99  0 45 99  0 40 99  0 35 99  0 30 99 \
 0 25 99  0 20 99  0 15 99  0 10 99  0  5 99 \
 0  0 99  5  0 99 10  0 99 15  0 99 20  0 99 \
25  0 99 30  0 99 35  0 99 40  0 99 45  0 99 \
50  0 99 55  0 99 60  0 99 65  0 99 70  0 99 \
75  0 99 80  0 99 85  0 99 90  0 99 95  0 99 \
99  0 99 99  0 90 99  0 80 99  0 70 99  0 60 \
99  0 50 99  0 40 99  0 30 99  0 20 99  0 10] \r\
make "shade  50 \r\
tasetshade :shade \r')

    def _numbers_palette(self):
        """ The basic Turtle Art numbers palette """

        palette = make_palette('numbers',
                               colors=["#FF00FF", "#A000A0"],
                               help_string=_('Palette of numeric operators'))

        primitive_dictionary['plus'] = self._prim_plus
        palette.add_block('plus2',
                          style='number-style',
                          label='+',
                          special_name=_('plus'),
                          string_or_number=True,
                          prim_name='plus',
                          logo_command='sum',
                          help_string=_('adds two alphanumeric inputs'))
        self.tw.lc.def_prim(
            'plus', 2, lambda self, x, y: primitive_dictionary['plus'](x, y))

        primitive_dictionary['minus'] = self._prim_minus
        palette.add_block('minus2',
                          style='number-style-porch',
                          label='–',
                          special_name=_('minus'),
                          prim_name='minus',
                          logo_command='taminus',
                          help_string=_('subtracts bottom numeric input from \
top numeric input'))
        self.tw.lc.def_prim(
            'minus', 2, lambda self, x, y: primitive_dictionary['minus'](x, y))
        define_logo_function('taminus', 'to taminus :y :x\routput sum :x \
minus :y\rend\r')

        primitive_dictionary['product'] = self._prim_product
        palette.add_block('product2',
                          style='number-style',
                          label='×',
                          special_name=_('multiply'),
                          prim_name='product',
                          logo_command='product',
                          help_string=_('multiplies two numeric inputs'))
        self.tw.lc.def_prim(
            'product', 2,
            lambda self, x, y: primitive_dictionary['product'](x, y))

        primitive_dictionary['division'] = self._prim_careful_divide
        palette.add_block('division2',
                          style='number-style-porch',
                          label='/',
                          special_name=_('divide'),
                          prim_name='division',
                          logo_command='quotient',
                          help_string=_('divides top numeric input \
(numerator) by bottom numeric input (denominator)'))
        self.tw.lc.def_prim(
            'division', 2,
            lambda self, x, y: primitive_dictionary['division'](x, y))

        primitive_dictionary['id'] = self._prim_identity
        palette.add_block('identity2',
                          style='number-style-1arg',
                          label='←',
                          special_name=_('identity'),
                          prim_name='id',
                          help_string=_('identity operator used for extending \
blocks'))
        self.tw.lc.def_prim('id', 1,
                             lambda self, x: primitive_dictionary['id'](x))

        primitive_dictionary['remainder'] = self._prim_mod
        palette.add_block('remainder2',
                          style='number-style-porch',
                          label=_('mod'),
                          special_name=_('mod'),
                          prim_name='remainder',
                          logo_command='remainder',
                          help_string=_('modular (remainder) operator'))
        self.tw.lc.def_prim('remainder', 2,
            lambda self, x, y: primitive_dictionary['remainder'](x, y))

        primitive_dictionary['sqrt'] = self._prim_sqrt
        palette.add_block('sqrt',
                          style='number-style-1arg',
                          label=_('√'),
                          special_name=_('square root'),
                          prim_name='sqrt',
                          logo_command='tasqrt',
                          help_string=_('calculates square root'))
        self.tw.lc.def_prim('sqrt', 1,
                             lambda self, x: primitive_dictionary['sqrt'](x))

        primitive_dictionary['random'] = self._prim_random
        palette.add_block('random',
                          style='number-style-block',
                          label=[_('random'), _('min'), _('max')],
                          default=[0, 100],
                          prim_name='random',
                          logo_command='tarandom',
                          help_string=_('returns random number between \
minimum (top) and maximum (bottom) values'))
        self.tw.lc.def_prim(
            'random', 2, lambda self, x, y: primitive_dictionary['random'](
                x, y))
        define_logo_function('tarandom', 'to tarandom :min :max\r \
output (random (:max - :min)) + :min\rend\r')

        palette.add_block('number',
                          style='box-style',
                          label='100',
                          default=100,
                          special_name=_('number'),
                          help_string=_('used as numeric input in mathematic \
operators'))

        primitive_dictionary['more'] = self._prim_more
        palette.add_block('greater2',
                          style='compare-porch-style',
                          label='>',
                          string_or_number=True,
                          special_name=_('greater than'),
                          prim_name='greater?',
                          logo_command='greater?',
                          help_string=_('logical greater-than operator'))
        self.tw.lc.def_prim(
            'greater?', 2,
            lambda self, x, y: primitive_dictionary['more'](x, y))

        primitive_dictionary['less'] = self._prim_less
        palette.add_block('less2',
                          style='compare-porch-style',
                          label='<',
                          special_name=_('less than'),
                          string_or_number=True,
                          prim_name='less?',
                          logo_command='less?',
                          help_string=_('logical less-than operator'))
        self.tw.lc.def_prim(
            'less?', 2, lambda self, x, y: primitive_dictionary['less'](x, y))

        primitive_dictionary['equal'] = self._prim_equal
        palette.add_block('equal2',
                          style='compare-style',
                          label='=',
                          special_name=_('equal'),
                          string_or_number=True,
                          prim_name='equal?',
                          logo_command='equal?',
                          help_string=_('logical equal-to operator'))
        self.tw.lc.def_prim('equal?', 2,
            lambda self, x, y: primitive_dictionary['equal'](x, y))

        palette.add_block('not',
                          style='not-style',
                          label=_('not'),
                          prim_name='not',
                          logo_command='not',
                          help_string=_('logical NOT operator'))
        self.tw.lc.def_prim('not', 1, lambda self, x: not x)

        primitive_dictionary['and'] = self._prim_and
        palette.add_block('and2',
                          style='boolean-style',
                          label=_('and'),
                          prim_name='and',
                          logo_command='and',
                          special_name=_('and'),
                          help_string=_('logical AND operator'))
        self.tw.lc.def_prim(
            'and', 2, lambda self, x, y: primitive_dictionary['and'](x, y))

        primitive_dictionary['or'] = self._prim_or
        palette.add_block('or2',
                          style='boolean-style',
                          label=_('or'),
                          prim_name='or',
                          logo_command='or',
                          special_name=_('or'),
                          help_string=_('logical OR operator'))
        self.tw.lc.def_prim(
            'or', 2, lambda self, x, y: primitive_dictionary['or'](x, y))

    def _flow_palette(self):
        """ The basic Turtle Art flow palette """

        palette = make_palette('flow',
                               colors=["#FFC000", "#A08000"],
                               help_string=_('Palette of flow operators'))

        primitive_dictionary['wait'] = self._prim_wait
        palette.add_block('wait',
                          style='basic-style-1arg',
                          label=_('wait'),
                          prim_name='wait',
                          default=1,
                          logo_command='wait',
                          help_string=_('pauses program execution a specified \
number of seconds'))
        self.tw.lc.def_prim('wait', 1, primitive_dictionary['wait'], True)

        primitive_dictionary['forever'] = self._prim_forever
        palette.add_block('forever',
                          # style='flow-style',
                          style='clamp-style',
                          label=_('forever'),
                          prim_name='forever',
                          # default=[None, 'vspace'],
                          default=[None, None],
                          logo_command='forever',
                          help_string=_('loops forever'))
        self.tw.lc.def_prim('forever', 1, primitive_dictionary['forever'],
                            True)

        primitive_dictionary['repeat'] = self._prim_repeat
        palette.add_block('repeat',
                          # style='flow-style-1arg',
                          style='clamp-style-1arg',
                          label=_('repeat'),
                          prim_name='repeat',
                          # default=[4, None, 'vspace'],
                          default=[4, None, None],
                          logo_command='repeat',
                          special_name=_('repeat'),
                          help_string=_('loops specified number of times'))
        self.tw.lc.def_prim('repeat', 2, primitive_dictionary['repeat'], True)

        primitive_dictionary['if'] = self._prim_if
        palette.add_block('if',
                          # style='flow-style-boolean',
                          style='clamp-style-boolean',
                          # label=[_('if'), '', _('then')],
                          label=[_('if'), _('then'), ''],
                          prim_name='if',
                          # default=[None, None, 'vspace'],
                          default=[None, None, None],
                          special_name=_('if then'),
                          logo_command='if',
                          help_string=_('if-then operator that uses boolean \
operators from Numbers palette'))
        self.tw.lc.def_prim('if', 2, primitive_dictionary['if'], True)

        primitive_dictionary['ifelse'] = self._prim_ifelse
        palette.add_block('ifelse',
                          hidden=True,  # Too big to fit palette
                          # style='flow-style-else',
                          style='clamp-style-else',
                          label=[_('if'), _('then'), _('else')],
                          prim_name='ifelse',
                          # default=[None, 'vspace', None, 'vspace'],
                          default=[None, None, None, None],
                          logo_command='ifelse',
                          special_name=_('if then else'),
                          help_string=_('if-then-else operator that uses \
boolean operators from Numbers palette'))
        self.tw.lc.def_prim('ifelse', 3, primitive_dictionary['ifelse'], True)

        # macro
        palette.add_block('ifthenelse',
                          style='basic-style-extended-vertical',
                          label=_('if then else'),
                          help_string=_('if-then-else operator that uses \
boolean operators from Numbers palette'))

        palette.add_block('hspace',
                          style='flow-style-tail',
                          hidden=True,
                          label='',
                          prim_name='nop',
                          special_name=_('horizontal space'),
                          help_string=_('jogs stack right'))
        self.tw.lc.def_prim('nop', 0, lambda self: None)

        palette.add_block('vspace',
                          style='basic-style-extended-vertical',
                          label='',
                          prim_name='nop',
                          special_name=_('vertical space'),
                          help_string=_('jogs stack down'))
        self.tw.lc.def_prim('nop', 0, lambda self: None)

        primitive_dictionary['stopstack'] = self._prim_stopstack
        palette.add_block('stopstack',
                          style='basic-style-tail',
                          label=_('stop action'),
                          prim_name='stopstack',
                          logo_command='stop',
                          help_string=_('stops current action'))
        self.tw.lc.def_prim('stopstack', 0,
                             lambda self: primitive_dictionary['stopstack']())

    def _blocks_palette(self):
        """ The basic Turtle Art blocks palette """

        palette = make_palette('blocks',
                               colors=["#FFFF00", "#A0A000"],
                               help_string=_('Palette of variable blocks'))

        primitive_dictionary['start'] = self._prim_start
        palette.add_block('start',
                          style='basic-style-head',
                          label=_('start'),
                          prim_name='start',
                          logo_command='to start\r',
                          help_string=_('connects action to toolbar run \
buttons'))
        self.tw.lc.def_prim('start', 0,
                             lambda self: primitive_dictionary['start']())

        primitive_dictionary['setbox'] = self._prim_setbox
        palette.add_block('storeinbox1',
                          style='basic-style-1arg',
                          label=_('store in box 1'),
                          prim_name='storeinbox1',
                          default=100,
                          string_or_number=True,
                          logo_command='make "box1',
                          help_string=_('stores numeric value in Variable 1'))
        self.tw.lc.def_prim('storeinbox1', 1,
                             lambda self, x: primitive_dictionary['setbox'](
                'box1', None, x))

        palette.add_block('storeinbox2',
                          style='basic-style-1arg',
                          label=_('store in box 2'),
                          prim_name='storeinbox2',
                          default=100,
                          string_or_number=True,
                          logo_command='make "box2',
                          help_string=_('stores numeric value in Variable 2'))
        self.tw.lc.def_prim('storeinbox2', 1,
                             lambda self, x: primitive_dictionary['setbox'](
                'box2', None, x))

        palette.add_block('string',
                          style='box-style',
                          label=_('text'),
                          default=_('text'),
                          special_name=_('text'),
                          help_string=_('string value'))

        palette.add_block('box1',
                          style='box-style',
                          label=_('box 1'),
                          prim_name='box1',
                          logo_command=':box1',
                          help_string=_('Variable 1 (numeric value)'),
                          value_block=True)
        self.tw.lc.def_prim('box1', 0, lambda self: self.tw.lc.boxes['box1'])

        palette.add_block('box2',
                          style='box-style',
                          label=_('box 2'),
                          prim_name='box2',
                          logo_command=':box2',
                          help_string=_('Variable 2 (numeric value)'),
                          value_block=True)
        self.tw.lc.def_prim('box2', 0, lambda self: self.tw.lc.boxes['box2'])

        primitive_dictionary['box'] = self._prim_box
        palette.add_block('box',
                          style='number-style-1strarg',
                          label=_('box'),
                          string_or_number=True,
                          prim_name='box',
                          default=_('my box'),
                          logo_command='box',
                          help_string=_('named variable (numeric value)'))
        self.tw.lc.def_prim('box', 1,
                             lambda self, x: primitive_dictionary['box'](x))

        palette.add_block('storein',
                          style='basic-style-2arg',
                          label=[_('store in'), _('box'), _('value')],
                          string_or_number=True,
                          prim_name='storeinbox',
                          logo_command='storeinbox',
                          default=[_('my box'), 100],
                          help_string=_('stores numeric value in named \
variable'))
        self.tw.lc.def_prim('storeinbox', 2,
                             lambda self, x, y: primitive_dictionary['setbox'](
                'box3', x, y))

        palette.add_block('hat',
                          style='basic-style-head-1arg',
                          label=_('action'),
                          prim_name='nop3',
                          string_or_number=True,
                          default=_('action'),
                          logo_command='to action',
                          help_string=_('top of nameable action stack'))
        self.tw.lc.def_prim('nop3', 1, lambda self, x: None)

        palette.add_block('hat1',
                          style='basic-style-head',
                          label=_('action 1'),
                          prim_name='nop1',
                          logo_command='to stack1\r',
                          help_string=_('top of Action 1 stack'))
        self.tw.lc.def_prim('nop1', 0, lambda self: None)

        palette.add_block('hat2',
                          style='basic-style-head',
                          label=_('action 2'),
                          prim_name='nop2',
                          logo_command='to stack2\r',
                          help_string=_('top of Action 2 stack'))
        self.tw.lc.def_prim('nop2', 0, lambda self: None)

        primitive_dictionary['stack'] = self._prim_stack
        palette.add_block('stack',
                          style='basic-style-1arg',
                          label=_('action'),
                          string_or_number=True,
                          prim_name='stack',
                          logo_command='action',
                          default=_('action'),
                          help_string=_('invokes named action stack'))
        self.tw.lc.def_prim('stack', 1, primitive_dictionary['stack'], True)

        primitive_dictionary['stack1'] = self._prim_stack1
        palette.add_block('stack1',
                          style='basic-style-extended-vertical',
                          label=_('action 1'),
                          prim_name='stack1',
                          logo_command='stack1',
                          help_string=_('invokes Action 1 stack'))
        self.tw.lc.def_prim('stack1', 0, primitive_dictionary['stack1'], True)

        primitive_dictionary['stack2'] = self._prim_stack2
        palette.add_block('stack2',
                          style='basic-style-extended-vertical',
                          label=_('action 2'),
                          prim_name='stack2',
                          logo_command='stack2',
                          help_string=_('invokes Action 2 stack'))
        self.tw.lc.def_prim('stack2', 0, primitive_dictionary['stack2'], True)

    def _trash_palette(self):
        """ The basic Turtle Art turtle palette """

        palette = make_palette('trash',
                               colors=["#FFFF00", "#A0A000"],
                               help_string=_('trash'))

        palette.add_block('empty',
                          style='blank-style',
                          label=_('empty trash'),
                          help_string=_('permanently deletes items in trash'))

        palette.add_block('restoreall',
                          style='blank-style',
                          label=_('restore all'),
                          help_string=_('restore all blocks from trash'))

        palette.add_block('trashall',
                          style='blank-style',
                          label=_('clear all'),
                          help_string=_('move all blocks to trash'))

    # Block primitives

    def _prim_and(self, x, y):
        """ Logical and """
        return x & y

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

    def _prim_or(self, x, y):
        """ Logical or """
        return x | y

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
        if type(x) == list and _num_type(y):
            z = []
            for i in range(len(x)):
                try:
                    z.append(x[i] / y)
                except ZeroDivisionError:
                    raise logoerror("#zerodivide")
            return z
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
        if type(x) == list and type(y) == list:
            for i in range(len(x)):
                if x[i] != y[i]:
                    return False
            return True
        try:
            return float(x) == float(y)
        except ValueError:
            typex, typey = False, False
            if strtype(x):
                typex = True
            if strtype(y):
                typey = True
            if typex and typey:
                return x == y
            try:
                return self._string_to_num(x) == self._string_to_num(y)
            except TypeError:
                raise logoerror("#syntaxerror")

    def _prim_less(self, x, y):
        """ Compare numbers and strings """
        if type(x) == list or type(y) == list:
            raise logoerror("#syntaxerror")
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
        elif type(x) == list and type(y) == list:
            z = []
            for i in range(len(x)):
                z.append(x[i] + y[i])
            return(z)
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
        elif type(x) == list and type(y) == list:
            z = []
            for i in range(len(x)):
                z.append(x[i] - y[i])
            return(z)
        try:
            return self._string_to_num(x) - self._string_to_num(y)
        except TypeError:
            raise logoerror("#notanumber")

    def _prim_product(self, x, y):
        """ Numerical multiplication """
        if _num_type(x) and _num_type(y):
            return(x * y)
        elif type(x) == list and _num_type(y):
            z = []
            for i in range(len(x)):
                z.append(x[i] * y)
            return(z)
        elif type(y) == list and _num_type(x):
            z = []
            for i in range(len(y)):
                z.append(y[i] * x)
            return(z)
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
        if type(x) is list:
            raise logoerror("#syntaxerror")
        xx = convert(x.replace(self.tw.decimal_point, '.'), float)
        if type(xx) is float:
            return xx
        else:
            xx, xflag = chr_to_ord(x)
            if xflag:
                return xx
            else:
                raise logoerror("#syntaxerror")

    def _make_constant(self, palette, block_name, label, constant):
        """ Factory for constant blocks """
        palette.add_block(block_name, style='box-style',
                          label=label, prim_name=block_name,
                          logo_command=block_name)
        self.tw.lc.def_prim(block_name, 0, lambda self: constant)
