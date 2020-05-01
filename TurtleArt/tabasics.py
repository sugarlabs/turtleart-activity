# -*- coding: utf-8 -*-
# Copyright (c) 2011, 2012 Walter Bender

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

'''
This file contains the constants  that by-in-large determine the
behavior of Turtle Art.  Notably, the block palettes are defined
below.  If you want to add a new block to Turtle Art,  you could
simply add a block of code to this file or to
../plugins/turtle_blocks_extras/turtle_blocks_extras.py ,
which contains additional blocks.  (Even better,  write your own
plugin!!)


Adding a new palette is simply a matter of:

    palette = make_palette('mypalette',  # the name of your palette
                           colors=["#00FF00", "#00A000"],
                           help_string=_('Palette of my custom commands'))

For example,  if we want to add  a new turtle command,  'uturn',
we'd use the `add_block` method in the Palette class.

    palette.add_block('uturn',  # the name of your block
                      style='basic-style',  # the block style
                      label=_('u turn'),  # the label for the block
                      prim_name='uturn',  # code reference (see below)
                      help_string=_('turns the turtle 180 degrees'))

Next, you need to define what your block will do: def_prim takes
3 arguments: the primitive name, the number of arguments  ---  0
in this case  ---  and  a Primitive object.   A Primitive object
represents  the statement  to be  executed   when  the block  is
executed in Turtle Art. For the 'uturn' block, we would like the
statement to look roughly like this:

    Turtle.set_heading(plus(Turtle.get_heading(), 180))

Formally, a Primitive object consists of a function,  its return
type,  and descriptions  of its arguments and keyword arguments.
The return type  is not a Python type,   but a type  from Turtle
Art's internal type system.   All available types are defined as
constants in tatype.py .

In this case,  we know in advance  which arguments each function
gets,   so we can use  ConstantArg objects  as argument descrip-
tions. (For examples where the arguments come from other blocks,
please refer to ../doc/primitives-with-arguments.md .) Note that
Primitive objects  can be arguments  to other Primitive objects.
This leads to the following tree-like structure  for our 'uturn'
block:

    prim_uturn = Primitive(Turtle.set_heading,
        arg_descs=[ConstantArg(Primitive(
            Primitive.plus, return_type=TYPE_NUMBER,
                arg_descs=[ConstantArg(Primitive(
                    Turtle.get_heading, return_type=TYPE_NUMBER)),
                    ConstantArg(180)]))],
        call_afterwards=self.after_uturn)

    self.tw.lc.def_prim('uturn', 0, prim_uturn)

    # somewhere else in the same class:
    def after_uturn(self, value):
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value('heading', value)

The `call_afterwards` attribute  is  a simple function   that is
called  just after executing  the block.   It is often used  for
updating GUI labels.

That's it. When you next run Turtle Art, you will have a 'uturn'
block on the 'mypalette' palette.

You will have to create icons  for the palette-selector buttons.
These are kept in the 'icons' subdirectory.  You need two icons:
mypaletteoff.svg and mypaletteon.svg,   where 'mypalette' is the
same string  as the entry  you used in instantiating the Palette
object.  Note  that the icons should be the same size (55x55) as
the others. (This is the default icon size for Sugar toolbars.)
'''

from time import time
from gettext import gettext as _

from .tapalette import (make_palette, define_logo_function)
from .talogo import primitive_dictionary
from .taconstants import (
    Color,
    CONSTANTS,
    DEFAULT_BACKGROUND_COLOR_SHADE_GRAY)
from .taprimitive import (ArgSlot, ConstantArg, or_, Primitive)
from .tatype import (TYPE_BOOL, TYPE_BOX, TYPE_CHAR, TYPE_COLOR, TYPE_FLOAT,
                     TYPE_INT, TYPE_NUMBER, TYPE_NUMERIC_STRING, TYPE_OBJECT,
                     TYPE_STRING, TYPE_VECTOR)
from .taturtle import Turtle


def _millisecond():
    ''' Current time in milliseconds '''
    return time() * 1000


class Palettes():

    ''' a class for creating the palettes of blocks '''

    def __init__(self, turtle_window):
        self.tw = turtle_window

        self.prim_cache = {
            "minus": Primitive(Primitive.minus,
                               return_type=TYPE_NUMBER,
                               arg_descs=[ArgSlot(TYPE_NUMBER)]),
            "ord": Primitive(ord,
                             return_type=TYPE_INT,
                             arg_descs=[ArgSlot(TYPE_CHAR)])
        }  # avoid several Primitives of the same function

        self._turtle_palette()

        self._pen_palette()

        self._color_palette()

        self._numbers_palette()

        self._flow_palette()

        self._blocks_palette()

    def make_trash_palette(self):
        self._trash_palette()

    # Palette definitions

    def _turtle_palette(self):
        ''' The basic Turtle Art turtle palette '''

        palette = make_palette('turtle',
                               colors=["#00FF00", "#00A000"],
                               help_string=_('Palette of turtle commands'),
                               translation=_('turtle'))

        palette.add_block('forward',
                          style='basic-style-1arg',
                          label=_('forward'),
                          prim_name='forward',
                          default=100,
                          logo_command='forward',
                          help_string=_('moves turtle forward'))
        self.tw.lc.def_prim(
            'forward', 1,
            Primitive(Turtle.forward,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_move))

        palette.add_block('back',
                          style='basic-style-1arg',
                          label=_('back'),
                          prim_name='back',
                          default=100,
                          logo_command='back',
                          help_string=_('moves turtle backward'))
        self.tw.lc.def_prim(
            'back', 1,
            Primitive(Turtle.backward,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_move))

        palette.add_block('clean',
                          style='basic-style-extended-vertical',
                          label=_('clean'),
                          prim_name='clean',
                          logo_command='clean',
                          help_string=_('clears the screen and reset the \
turtle'))
        self.tw.lc.def_prim('clean', 0,
                            Primitive(Primitive.group, arg_descs=[
                                ConstantArg([
                                    Primitive(self.tw.clear_plugins),
                                    Primitive(self.tw.lc.stop_playing_media),
                                    Primitive(self.tw.lc.reset_scale),
                                    # Primitive(self.tw.lc.reset_timer),
                                    Primitive(self.tw.lc.clear_value_blocks),
                                    Primitive(self.tw.canvas.clearscreen),
                                    Primitive(self.tw.lc.reset_internals),
                                    Primitive(self.tw.turtles.reset_turtles),
                                    Primitive(self.tw.lc.active_turtle)
                                ])]))

        palette.add_block('left',
                          style='basic-style-1arg',
                          label=_('left'),
                          prim_name='left',
                          default=90,
                          logo_command='left',
                          help_string=_('turns turtle counterclockwise (angle \
in degrees)'))
        self.tw.lc.def_prim(
            'left', 1,
            Primitive(Turtle.left,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_right))

        palette.add_block('right',
                          style='basic-style-1arg',
                          label=_('right'),
                          prim_name='right',
                          default=90,
                          logo_command='right',
                          help_string=_('turns turtle clockwise (angle in \
degrees)'))
        self.tw.lc.def_prim(
            'right', 1,
            Primitive(Turtle.right,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_right))

        palette.add_block('arc',
                          style='basic-style-2arg',
                          label=[_('arc'), _('angle'), _('radius')],
                          prim_name='arc',
                          default=[90, 100],
                          logo_command='taarc',
                          help_string=_('moves turtle along an arc'))
        self.tw.lc.def_prim(
            'arc', 2,
            Primitive(Turtle.arc,
                      arg_descs=[ArgSlot(TYPE_NUMBER),
                                 ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_arc))
        define_logo_function('taarc', 'to taarc :a :r\nrepeat round :a \
[right 1 forward (0.0175 * :r)]\nend\n')

        palette.add_block('setxy2',
                          style='basic-style-2arg',
                          label=[_('set xy'), _('x'), _('y')],
                          prim_name='setxy2',
                          logo_command='tasetxy',
                          default=[0, 0],
                          help_string=_('moves turtle to position xcor, ycor; \
(0, 0) is in the center of the screen.'))
        self.tw.lc.def_prim(
            'setxy2', 2,
            Primitive(Turtle.set_xy,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_move))
        define_logo_function('tasetxy', 'to tasetxy :x :y\nsetxy :x :y\nend\n')

        palette.add_block('seth',
                          style='basic-style-1arg',
                          label=_('set heading'),
                          prim_name='seth',
                          default=0,
                          logo_command='seth',
                          help_string=_('sets the heading of the turtle (0 is \
towards the top of the screen.)'))
        self.tw.lc.def_prim(
            'seth', 1,
            Primitive(Turtle.set_heading,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=lambda value: self.after_set(
                          'heading', value)))

        palette.add_block('xcor',
                          style='box-style',
                          label=_('xcor'),
                          help_string=_('holds current x-coordinate value of \
the turtle (can be used in place of a number block)'),
                          value_block=True,
                          prim_name='xcor',
                          logo_command='xcor')
        self.tw.lc.def_prim(
            'xcor', 0,
            Primitive(Primitive.divide, return_type=TYPE_FLOAT,
                      arg_descs=[ConstantArg(Primitive(Turtle.get_x)),
                                 ConstantArg(Primitive(
                                     self.tw.get_coord_scale))]))

        palette.add_block('ycor',
                          style='box-style',
                          label=_('ycor'),
                          help_string=_('holds current y-coordinate value of \
the turtle (can be used in place of a number block)'),
                          value_block=True,
                          prim_name='ycor',
                          logo_command='ycor')
        self.tw.lc.def_prim(
            'ycor', 0,
            Primitive(Primitive.divide, return_type=TYPE_FLOAT,
                      arg_descs=[ConstantArg(Primitive(Turtle.get_y)),
                                 ConstantArg(Primitive(
                                     self.tw.get_coord_scale))]))

        palette.add_block('heading',
                          style='box-style',
                          label=_('heading'),
                          help_string=_('holds current heading value of the \
turtle (can be used in place of a number block)'),
                          value_block=True,
                          prim_name='heading',
                          logo_command='heading')
        self.tw.lc.def_prim('heading', 0,
                            Primitive(
                                Turtle.get_heading, return_type=TYPE_NUMBER))

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
        self.tw.lc.def_prim(
            'setxy', 2,
            Primitive(Turtle.set_xy,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)],
                      kwarg_descs={'pendown': ConstantArg(False)},
                      call_afterwards=self.after_move))
        define_logo_function('tasetxypenup', 'to tasetxypenup :x :y\npenup\n\
setxy :x :y\npendown\nend\n')

    def _pen_palette(self):
        ''' The basic Turtle Art pen palette '''

        palette = make_palette('pen',
                               colors=["#00FFFF", "#00A0A0"],
                               help_string=_('Palette of pen commands'),
                               translation=_('pen'))

        palette.add_block('fillscreen',
                          hidden=True,
                          style='basic-style-2arg',
                          label=[_('fill screen'), _('color'), _('shade')],
                          prim_name='fillscreen',
                          default=DEFAULT_BACKGROUND_COLOR_SHADE_GRAY[0:2],
                          logo_command='tasetbackground',
                          help_string=_('fills the background with (color, \
shade)'))
        self.tw.lc.def_prim(
            'fillscreen', 2,
            Primitive(self.tw.canvas.fillscreen,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)]))

        palette.add_block('fillscreen2',
                          style='basic-style-3arg',
                          label=[_('fill screen') + '\n\n', _('color'),
                                 _('shade'), _('gray')],
                          prim_name='fillscreen2',
                          default=DEFAULT_BACKGROUND_COLOR_SHADE_GRAY,
                          logo_command='tasetbackground',
                          help_string=_('fills the background with (color, \
shade)'))
        self.tw.lc.def_prim(
            'fillscreen2', 3,
            Primitive(self.tw.canvas.fillscreen_with_gray,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER),
                                 ArgSlot(TYPE_NUMBER)]))

        define_logo_function('tasetbackground', 'to tasetbackground :color \
:shade\ntasetshade :shade\nsetbackground :color\nend\n')

        palette.add_block('setcolor',
                          style='basic-style-1arg',
                          label=_('set color'),
                          prim_name='setcolor',
                          default=0,
                          logo_command='tasetpencolor',
                          help_string=_('sets color of the line drawn by the \
turtle'))
        self.tw.lc.def_prim(
            'setcolor', 1,
            Primitive(Turtle.set_color,
                      arg_descs=[or_(ArgSlot(TYPE_COLOR),
                                     ArgSlot(TYPE_NUMBER))],
                      call_afterwards=lambda value: self.after_set(
                          'color', value)))

        palette.add_block('setshade',
                          style='basic-style-1arg',
                          label=_('set shade'),
                          prim_name='setshade',
                          default=50,
                          logo_command='tasetshade',
                          help_string=_('sets shade of the line drawn by the \
turtle'))
        self.tw.lc.def_prim(
            'setshade', 1,
            Primitive(Turtle.set_shade,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=lambda value: self.after_set(
                          'shade', value)))

        palette.add_block('setgray',
                          style='basic-style-1arg',
                          label=_('set gray'),
                          prim_name='setgray',
                          default=100,
                          help_string=_('sets gray level of the line drawn by \
the turtle'))
        self.tw.lc.def_prim(
            'setgray', 1,
            Primitive(Turtle.set_gray,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=lambda value: self.after_set(
                          'gray', value)))

        palette.add_block('color',
                          style='box-style',
                          label=_('color'),
                          help_string=_('holds current pen color (can be used \
in place of a number block)'),
                          value_block=True,
                          prim_name='color',
                          logo_command='pencolor')
        self.tw.lc.def_prim('color', 0,
                            Primitive(
                                Turtle.get_color, return_type=TYPE_NUMBER))

        palette.add_block('shade',
                          style='box-style',
                          label=_('shade'),
                          help_string=_('holds current pen shade'),
                          value_block=True,
                          prim_name='shade',
                          logo_command=':shade')
        self.tw.lc.def_prim(
            'shade',
            0,
            Primitive(
                Turtle.get_shade,
                return_type=TYPE_NUMBER))

        palette.add_block('gray',
                          style='box-style',
                          label=_('gray'),
                          help_string=_('holds current gray level (can be \
used in place of a number block)'),
                          value_block=True,
                          prim_name='gray')
        self.tw.lc.def_prim('gray', 0,
                            Primitive(
                                Turtle.get_gray, return_type=TYPE_NUMBER))

        palette.add_block('penup',
                          style='basic-style-extended-vertical',
                          label=_('pen up'),
                          prim_name='penup',
                          logo_command='penup',
                          help_string=_('Turtle will not draw when moved.'))
        self.tw.lc.def_prim(
            'penup', 0,
            Primitive(Turtle.set_pen_state, arg_descs=[ConstantArg(False)]))

        palette.add_block('pendown',
                          style='basic-style-extended-vertical',
                          label=_('pen down'),
                          prim_name='pendown',
                          logo_command='pendown',
                          help_string=_('Turtle will draw when moved.'))
        self.tw.lc.def_prim(
            'pendown', 0,
            Primitive(Turtle.set_pen_state, arg_descs=[ConstantArg(True)]))

        palette.add_block('penstate',
                          style='boolean-block-style',
                          label=_('pen down?'),
                          prim_name='penstate',
                          help_string=_('returns True if pen is down'))
        self.tw.lc.def_prim(
            'penstate', 0,
            Primitive(Turtle.get_pen_state, return_type=TYPE_BOOL))

        palette.add_block('setpensize',
                          style='basic-style-1arg',
                          label=_('set pen size'),
                          prim_name='setpensize',
                          default=5,
                          logo_command='setpensize',
                          help_string=_('sets size of the line drawn by the \
turtle'))
        self.tw.lc.def_prim(
            'setpensize', 1,
            Primitive(Turtle.set_pen_size,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=lambda val: self.after_set(
                          'pensize', val)))
        define_logo_function('tasetpensize',
                             'to tasetpensize :a\nsetpensize round :a\nend\n')

        palette.add_block('startfill',
                          style='basic-style-extended-vertical',
                          label=_('start fill'),
                          prim_name='startfill',
                          help_string=_('starts filled polygon (used with end \
fill block)'))
        self.tw.lc.def_prim('startfill', 0, Primitive(Turtle.start_fill))

        palette.add_block('stopfill',
                          style='basic-style-extended-vertical',
                          label=_('end fill'),
                          prim_name='stopfill',
                          help_string=_('completes filled polygon (used with \
start fill block)'))
        self.tw.lc.def_prim('stopfill', 0, Primitive(Turtle.stop_fill))

        palette.add_block('pensize',
                          style='box-style',
                          label=_('pen size'),
                          help_string=_('holds current pen size (can be used \
in place of a number block)'),
                          value_block=True,
                          prim_name='pensize',
                          logo_command='pensize')
        self.tw.lc.def_prim(
            'pensize', 0,
            Primitive(Turtle.get_pen_size, return_type=TYPE_NUMBER))
        define_logo_function('tapensize', 'to tapensize\noutput first round \
pensize\nend\n')

    def _rgb_converter(self, r, g, b):
        return float(self.tw.canvas.get_color_index(r, g, b))

    def _color_palette(self):
        ''' The basic Turtle Art color palette '''

        palette = make_palette('colors',
                               colors=["#00FFFF", "#00A0A0"],
                               help_string=_('Palette of pen colors'),
                               translation=_('colors'))

        color_names = ('red', 'orange', 'yellow', 'green', 'cyan', 'blue',
                       'purple', 'white', 'black')
        # Need to make sure color names are included in the PO files
        color_names_i18n = (_('red'), _('orange'), _('yellow'),  # noqa: F841
                            _('green'), _('cyan'), _('blue'),
                            _('purple'), _('white'), _('black'))
        for name in color_names:
            self._make_constant(palette, name, _(name), name)

        palette.add_block('RGB to color',
                          style='number-style-var-3arg',
                          label=[_('RGB to\n\ncolor'), _(
                              'red'), _('green'), _('blue')],
                          default=[0, 0, 0],
                          help_string=_('converter'),
                          prim_name='converter')

        self.tw.lc.def_prim(
            'converter',
            3,
            Primitive(
                self._rgb_converter,
                return_type=TYPE_FLOAT,
                arg_descs=[
                    ArgSlot(TYPE_INT),
                    ArgSlot(TYPE_INT),
                    ArgSlot(TYPE_INT)]))

        # In order to map Turtle Art colors to the standard UCB Logo palette,
        # we need to define a somewhat complex set of functions.
        define_logo_function('tacolor', '\
to tasetpalette :i :r :g :b :myshade \n\
make "s ((:myshade - 50) / 50) \n\
ifelse lessp :s 0 [ \n\
make "s (1 + (:s *0.8)) \n\
make "r (:r * :s) \n\
make "g (:g * :s) \n\
make "b (:b * :s) \n\
] [ \
make "s (:s * 0.9) \n\
make "r (:r + ((99-:r) * :s)) \n\
make "g (:g + ((99-:g) * :s)) \n\
make "b (:b + ((99-:b) * :s)) \n\
] \
setpalette :i (list :r :g :b) \n\
end \n\
\
to rgb :myi :mycolors :myshade \n\
make "myr first :mycolors \n\
make "mycolors butfirst :mycolors \n\
make "myg first :mycolors \n\
make "mycolors butfirst :mycolors \n\
make "myb first :mycolors \n\
make "mycolors butfirst :mycolors \n\
tasetpalette :myi :myr :myg :myb :myshade \n\
output :mycolors \n\
end \n\
\
to processcolor :mycolors :myshade \n\
if emptyp :mycolors [stop] \n\
make "i :i + 1 \n\
processcolor (rgb :i :mycolors :myshade) :myshade \n\
end \n\
\
to tasetshade :shade \n\
make "myshade modulo :shade 200 \n\
if greaterp :myshade 99 [make "myshade (199-:myshade)] \n\
make "i 7 \n\
make "mycolors :colors \n\
processcolor :mycolors :myshade \n\
end \n\
\
to tasetpencolor :c \n\
make "color (modulo (round :c) 100) \n\
setpencolor :color + 8 \n\
end \n\
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
99  0 50 99  0 40 99  0 30 99  0 20 99  0 10] \n\
make "shade  50 \n\
tasetshade :shade \n')

    def _numbers_palette(self):
        ''' The basic Turtle Art numbers palette '''

        palette = make_palette('numbers',
                               colors=["#FF00FF", "#A000A0"],
                               help_string=_('Palette of numeric operators'),
                               translation=_('numbers'))

        palette.add_block('plus2',
                          style='number-style',
                          label='+',
                          special_name=_('plus'),
                          string_or_number=True,
                          prim_name='plus',
                          logo_command='sum',
                          help_string=_('adds two alphanumeric inputs'))
        self.tw.lc.def_prim(
            'plus', 2,
            # add up two numbers ...
            or_(Primitive(Primitive.plus, return_type=TYPE_NUMBER,
                          arg_descs=[ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)]),
                # ... or concatenate two strings
                Primitive(Primitive.plus, return_type=TYPE_STRING,
                          arg_descs=[ArgSlot(TYPE_STRING),
                                     ArgSlot(TYPE_STRING)]),
                # ... or add two vectors
                Primitive(Primitive.plus, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_VECTOR),
                                     ArgSlot(TYPE_VECTOR)])))

        palette.add_block('minus2',
                          style='number-style-porch',
                          label='        –',
                          special_name=_('minus'),
                          prim_name='minus',
                          logo_command='taminus',
                          help_string=_('subtracts bottom numeric input from \
top numeric input'))
        self.tw.lc.def_prim(
            'minus', 2,
            or_(Primitive(Primitive.minus, return_type=TYPE_NUMBER,
                          arg_descs=[ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)]),
                # ... or add two vectors
                Primitive(Primitive.minus, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_VECTOR),
                                     ArgSlot(TYPE_VECTOR)])))

        define_logo_function('taminus', 'to taminus :y :x\noutput sum :x \
minus :y\nend\n')

        palette.add_block('product2',
                          style='number-style',
                          label='×',
                          special_name=_('multiply'),
                          prim_name='product',
                          logo_command='product',
                          help_string=_('multiplies two numeric inputs'))
        self.tw.lc.def_prim(
            'product', 2,
            or_(Primitive(Primitive.multiply, return_type=TYPE_NUMBER,
                          arg_descs=[ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)]),
                Primitive(Primitive.multiply, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_VECTOR),
                                     ArgSlot(TYPE_NUMBER)]),
                Primitive(Primitive.multiply, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_VECTOR)])))

        palette.add_block('division2',
                          style='number-style-porch',
                          label='        /',
                          special_name=_('divide'),
                          prim_name='division',
                          logo_command='quotient',
                          help_string=_('divides top numeric input \
(numerator) by bottom numeric input (denominator)'))
        self.tw.lc.def_prim(
            'division', 2,
            or_(Primitive(Primitive.divide, return_type=TYPE_NUMBER,
                          arg_descs=[ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)]),
                Primitive(Primitive.divide, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_VECTOR),
                                     ArgSlot(TYPE_NUMBER)]),
                Primitive(Primitive.divide, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_VECTOR)])))

        palette.add_block('identity2',
                          style='number-style-1arg',
                          label='←',
                          special_name=_('identity'),
                          prim_name='id',
                          help_string=_('identity operator used for extending \
blocks'))
        self.tw.lc.def_prim(
            'id', 1,
            # preserve the Type of the argument: try less general types first
            or_(Primitive(Primitive.identity, return_type=TYPE_NUMERIC_STRING,
                          arg_descs=[ArgSlot(TYPE_NUMERIC_STRING)]),
                Primitive(Primitive.identity, return_type=TYPE_CHAR,
                          arg_descs=[ArgSlot(TYPE_CHAR)]),
                Primitive(Primitive.identity, return_type=TYPE_COLOR,
                          arg_descs=[ArgSlot(TYPE_COLOR)]),
                Primitive(Primitive.identity, return_type=TYPE_FLOAT,
                          arg_descs=[ArgSlot(TYPE_FLOAT)]),
                Primitive(Primitive.identity, return_type=TYPE_INT,
                          arg_descs=[ArgSlot(TYPE_INT)]),
                Primitive(Primitive.identity, return_type=TYPE_NUMBER,
                          arg_descs=[ArgSlot(TYPE_NUMBER)]),
                Primitive(Primitive.identity, return_type=TYPE_STRING,
                          arg_descs=[ArgSlot(TYPE_STRING)]),
                Primitive(Primitive.identity, return_type=TYPE_VECTOR,
                          arg_descs=[ArgSlot(TYPE_VECTOR)]),
                Primitive(Primitive.identity, return_type=TYPE_OBJECT,
                          arg_descs=[ArgSlot(TYPE_OBJECT)])))

        palette.add_block('remainder2',
                          style='number-style-porch',
                          label=_('mod'),
                          special_name=_('mod'),
                          prim_name='remainder',
                          logo_command='remainder',
                          help_string=_('modular (remainder) operator'))
        self.tw.lc.def_prim(
            'remainder', 2,
            Primitive(Primitive.modulo, return_type=TYPE_NUMBER,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)]))

        palette.add_block('sqrt',
                          style='number-style-1arg',
                          label=_('√'),
                          special_name=_('square root'),
                          prim_name='sqrt',
                          logo_command='tasqrt',
                          help_string=_('calculates square root'))
        self.tw.lc.def_prim(
            'sqrt', 1,
            Primitive(Primitive.square_root, return_type=TYPE_FLOAT,
                      arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('random',
                          style='number-style-block',
                          label=[_('random'), _('min'), _('max')],
                          default=[0, 100],
                          prim_name='random',
                          logo_command='tarandom',
                          help_string=_('returns random number between \
minimum (top) and maximum (bottom) values'))

        self.tw.lc.def_prim(
            'random', 2,
            or_(  # random character ...
                Primitive(Primitive.random_char, return_type=TYPE_CHAR,
                          arg_descs=[
                              ArgSlot(TYPE_INT,
                                      wrapper=self.prim_cache["ord"]),
                              ArgSlot(TYPE_INT,
                                      wrapper=self.prim_cache["ord"])]),
                # ... or random number
                Primitive(Primitive.random_int, return_type=TYPE_INT,
                          arg_descs=[ArgSlot(TYPE_INT), ArgSlot(TYPE_INT)])))
        define_logo_function('tarandom', 'to tarandom :min :max\n \
output (random (:max - :min)) + :min\nend\n')

        palette.add_block('number',
                          style='box-style',
                          label='100',
                          default=100,
                          special_name=_('number'),
                          help_string=_('used as numeric input in mathematic \
operators'))

        palette.add_block('greater2',
                          style='compare-porch-style',
                          label='    >',
                          string_or_number=True,
                          special_name=_('greater than'),
                          prim_name='greater?',
                          logo_command='greater?',
                          help_string=_('logical greater-than operator'))
        self.tw.lc.def_prim(
            'greater?', 2,
            Primitive(Primitive.greater, return_type=TYPE_BOOL,
                      arg_descs=or_([ArgSlot(TYPE_COLOR),
                                     ArgSlot(TYPE_COLOR)],
                                    [ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)],
                                    [ArgSlot(TYPE_STRING),
                                     ArgSlot(TYPE_STRING)],
                                    [ArgSlot(TYPE_OBJECT),
                                     ArgSlot(TYPE_OBJECT)])))

        palette.add_block('less2',
                          style='compare-porch-style',
                          label='    <',
                          special_name=_('less than'),
                          string_or_number=True,
                          prim_name='less?',
                          logo_command='less?',
                          help_string=_('logical less-than operator'))
        self.tw.lc.def_prim(
            'less?', 2,
            Primitive(Primitive.less, return_type=TYPE_BOOL,
                      arg_descs=or_([ArgSlot(TYPE_COLOR),
                                     ArgSlot(TYPE_COLOR)],
                                    [ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)],
                                    [ArgSlot(TYPE_STRING),
                                     ArgSlot(TYPE_STRING)],
                                    [ArgSlot(TYPE_OBJECT),
                                     ArgSlot(TYPE_OBJECT)])))

        palette.add_block('equal2',
                          style='compare-style',
                          label='=',
                          special_name=_('equal'),
                          string_or_number=True,
                          prim_name='equal?',
                          logo_command='equal?',
                          help_string=_('logical equal-to operator'))
        self.tw.lc.def_prim(
            'equal?', 2,
            Primitive(Primitive.equals, return_type=TYPE_BOOL,
                      arg_descs=or_([ArgSlot(TYPE_COLOR),
                                     ArgSlot(TYPE_COLOR)],
                                    [ArgSlot(TYPE_NUMBER),
                                     ArgSlot(TYPE_NUMBER)],
                                    [ArgSlot(TYPE_STRING),
                                     ArgSlot(TYPE_STRING)],
                                    [ArgSlot(TYPE_OBJECT),
                                     ArgSlot(TYPE_OBJECT)])))

        palette.add_block('not',
                          style='not-style',
                          label=_('not'),
                          prim_name='not',
                          logo_command='not',
                          help_string=_('logical NOT operator'))
        self.tw.lc.def_prim(
            'not', 1,
            Primitive(Primitive.not_, return_type=TYPE_BOOL,
                      arg_descs=[ArgSlot(TYPE_BOOL)]))

        palette.add_block('and2',
                          style='boolean-style',
                          label=_('and'),
                          prim_name='and',
                          logo_command='and',
                          special_name=_('and'),
                          help_string=_('logical AND operator'))
        self.tw.lc.def_prim(
            'and', 2,
            Primitive(Primitive.and_, return_type=TYPE_BOOL,
                      arg_descs=[ArgSlot(TYPE_BOOL), ArgSlot(TYPE_BOOL)]))

        palette.add_block('or2',
                          style='boolean-style',
                          label=_('or'),
                          prim_name='or',
                          logo_command='or',
                          special_name=_('or'),
                          help_string=_('logical OR operator'))
        self.tw.lc.def_prim(
            'or', 2,
            Primitive(Primitive.or_, return_type=TYPE_BOOL,
                      arg_descs=[ArgSlot(TYPE_BOOL), ArgSlot(TYPE_BOOL)]))

    def _flow_palette(self):
        ''' The basic Turtle Art flow palette '''

        palette = make_palette('flow',
                               colors=["#FFC000", "#A08000"],
                               help_string=_('Palette of flow operators'),
                               translation=_('flow'))

        palette.add_block('wait',
                          style='basic-style-1arg',
                          label=_('wait'),
                          prim_name='wait',
                          default=1,
                          logo_command='wait',
                          help_string=_('pauses program execution a specified \
number of seconds'))
        self.tw.lc.def_prim(
            'wait', 1,
            Primitive(self.tw.lc.prim_wait, arg_descs=[ArgSlot(TYPE_NUMBER)]),
            True)

        palette.add_block('forever',
                          style='clamp-style',
                          label=_('forever'),
                          prim_name='forever',
                          default=[None],
                          logo_command='forever',
                          help_string=_('loops forever'))
        self.tw.lc.def_prim(
            'forever', 1,
            Primitive(self.tw.lc.prim_loop, arg_descs=[ConstantArg(Primitive(
                Primitive.controller_forever)), ArgSlot(TYPE_OBJECT,
                                                        call_arg=False)]),
            True)

        palette.add_block('repeat',
                          style='clamp-style-1arg',
                          label=_('repeat'),
                          prim_name='repeat',
                          default=[4, None],
                          logo_command='repeat',
                          special_name=_('repeat'),
                          help_string=_('loops specified number of times'))
        self.tw.lc.def_prim(
            'repeat', 2,
            Primitive(self.tw.lc.prim_loop,
                      arg_descs=[ArgSlot(
                          TYPE_OBJECT,
                          wrapper=Primitive(Primitive.controller_repeat,
                                            arg_descs=[ArgSlot(TYPE_INT)])),
                                 ArgSlot(TYPE_OBJECT, call_arg=False)]),
            True)

        palette.add_block('if',
                          style='clamp-style-boolean',
                          label=[_('if'), _('then')],
                          prim_name='if',
                          default=[None, None],
                          special_name=_('if then'),
                          logo_command='if',
                          help_string=_('if-then operator that uses boolean \
operators from Numbers palette'))
        self.tw.lc.def_prim(
            'if', 2,
            Primitive(self.tw.lc.prim_if,
                      arg_descs=[ArgSlot(TYPE_BOOL), ArgSlot(TYPE_OBJECT)]),
            True)

        palette.add_block('ifelse',
                          hidden=True,  # Too big to fit palette
                          style='clamp-style-else',
                          label=[_('if'), _('then'), _('else')],
                          prim_name='ifelse',
                          default=[None, None, None],
                          logo_command='ifelse',
                          special_name=_('if then else'),
                          help_string=_('if-then-else operator that uses \
boolean operators from Numbers palette'))
        self.tw.lc.def_prim(
            'ifelse', 3,
            Primitive(self.tw.lc.prim_ifelse,
                      arg_descs=[ArgSlot(TYPE_BOOL), ArgSlot(TYPE_OBJECT),
                                 ArgSlot(TYPE_OBJECT)]),
            True)

        # macro
        palette.add_block('ifthenelse',
                          style='basic-style-extended-vertical',
                          label=_('if then else'),
                          help_string=_('if-then-else operator that uses \
boolean operators from Numbers palette'))

        # Deprecated
        palette.add_block('hspace',
                          style='flow-style-tail',
                          hidden=True,
                          label='',
                          prim_name='nop',
                          special_name=_('horizontal space'),
                          help_string=_('jogs stack right'))
        self.tw.lc.def_prim(
            'nop', 0,
            Primitive(Primitive.do_nothing, export_me=False))

        palette.add_block('vspace',
                          style='basic-style-extended-vertical',
                          label='',
                          prim_name='nop',
                          special_name=_('vertical space'),
                          help_string=_('jogs stack down'))
        self.tw.lc.def_prim(
            'nop', 0,
            Primitive(Primitive.do_nothing, export_me=False))

        palette.add_block('stopstack',
                          style='basic-style-tail',
                          label=_('stop action'),
                          prim_name='stopstack',
                          logo_command='stop',
                          help_string=_('stops current action'))
        self.tw.lc.def_prim(
            'stopstack', 0,
            Primitive(self.tw.lc.prim_stop_stack))

    def _blocks_palette(self):
        ''' The basic Turtle Art blocks palette '''

        palette = make_palette('blocks',
                               colors=["#FFFF00", "#A0A000"],
                               help_string=_('Palette of variable blocks'),
                               translation=_('blocks'))

        palette.add_block('start',
                          style='clamp-style-hat',
                          label=_('start'),
                          prim_name='start',
                          logo_command='to start\n',
                          help_string=_('connects action to toolbar run \
buttons'))
        self.tw.lc.def_prim(
            'start', 0,
            Primitive(Primitive.group, arg_descs=[ConstantArg([
                Primitive(self.tw.lc.prim_start,
                          export_me=False),
                Primitive(self.tw.lc.prim_define_stack,
                          arg_descs=[ConstantArg('start')])])]))

        palette.add_block('hat',
                          style='clamp-style-hat-1arg',
                          label=_('action'),
                          prim_name='nop3',
                          string_or_number=True,
                          default=_('action'),
                          logo_command='to action',
                          help_string=_('top of nameable action stack'))
        self.tw.lc.def_prim(
            'nop3', 1,
            Primitive(self.tw.lc.prim_define_stack,
                      arg_descs=[ArgSlot(TYPE_OBJECT)]))

        primitive_dictionary['stack'] = Primitive(
            self.tw.lc.prim_invoke_stack,
            arg_descs=[ArgSlot(TYPE_OBJECT)])
        palette.add_block('stack',
                          style='basic-style-1arg',
                          label=_('action'),
                          string_or_number=True,
                          prim_name='stack',
                          logo_command='action',
                          default=_('action'),
                          help_string=_('invokes named action stack'))
        self.tw.lc.def_prim('stack', 1,
                            primitive_dictionary['stack'], True)

        palette.add_block('storeinbox1',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('store in box 1'),
                          prim_name='storeinbox1',
                          default=100,
                          string_or_number=True,
                          logo_command='make "box1',
                          help_string=_('stores numeric value in Variable 1'))
        self.tw.lc.def_prim(
            'storeinbox1', 1,
            Primitive(self.tw.lc.prim_set_box,
                      arg_descs=[ConstantArg('box1'), ArgSlot(TYPE_OBJECT)]))

        palette.add_block('storeinbox2',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('store in box 2'),
                          prim_name='storeinbox2',
                          default=100,
                          string_or_number=True,
                          logo_command='make "box2',
                          help_string=_('stores numeric value in Variable 2'))
        self.tw.lc.def_prim(
            'storeinbox2', 1,
            Primitive(self.tw.lc.prim_set_box,
                      arg_descs=[ConstantArg('box2'), ArgSlot(TYPE_OBJECT)]))

        palette.add_block('box1',
                          hidden=True,
                          style='box-style',
                          label=_('box 1'),
                          prim_name='box1',
                          logo_command=':box1',
                          help_string=_('Variable 1 (numeric value)'),
                          value_block=True)
        self.tw.lc.def_prim(
            'box1', 0,
            Primitive(self.tw.lc.prim_get_box, return_type=TYPE_BOX,
                      arg_descs=[ConstantArg('box1')]))

        palette.add_block('box2',
                          hidden=True,
                          style='box-style',
                          label=_('box 2'),
                          prim_name='box2',
                          logo_command=':box2',
                          help_string=_('Variable 2 (numeric value)'),
                          value_block=True)
        self.tw.lc.def_prim(
            'box2', 0,
            Primitive(self.tw.lc.prim_get_box, return_type=TYPE_BOX,
                      arg_descs=[ConstantArg('box2')]))

        primitive_dictionary['setbox'] = Primitive(
            self.tw.lc.prim_set_box,
            arg_descs=[ArgSlot(TYPE_OBJECT), ArgSlot(TYPE_OBJECT)])
        palette.add_block('storein',
                          style='basic-style-2arg',
                          label=[_('store in'), _('box'), _('value')],
                          string_or_number=True,
                          prim_name='storeinbox',
                          logo_command='storeinbox',
                          default=[_('my box'), 100],
                          help_string=_('stores numeric value in named \
variable'))
        self.tw.lc.def_prim('storeinbox', 2, primitive_dictionary['setbox'])

        primitive_dictionary['box'] = Primitive(
            self.tw.lc.prim_get_box,
            return_type=TYPE_BOX,
            arg_descs=[ArgSlot(TYPE_OBJECT)])
        palette.add_block('box',
                          style='number-style-1strarg',
                          hidden=True,
                          label=_('box'),
                          string_or_number=True,
                          prim_name='box',
                          default=_('my box'),
                          logo_command='box',
                          value_block=True,
                          help_string=_('named variable (numeric value)'))
        self.tw.lc.def_prim('box', 1, primitive_dictionary['box'])

        palette.add_block('hat1',
                          hidden=True,
                          style='basic-style-head',
                          label=_('action 1'),
                          prim_name='nop1',
                          logo_command='to stack1\n',
                          help_string=_('top of Action 1 stack'))
        self.tw.lc.def_prim(
            'nop1', 0,
            Primitive(self.tw.lc.prim_define_stack,
                      arg_descs=[ConstantArg('stack1')]))

        palette.add_block('hat2',
                          hidden=True,
                          style='basic-style-head',
                          label=_('action 2'),
                          prim_name='nop2',
                          logo_command='to stack2\n',
                          help_string=_('top of Action 2 stack'))
        self.tw.lc.def_prim(
            'nop2', 0,
            Primitive(self.tw.lc.prim_define_stack,
                      arg_descs=[ConstantArg('stack2')]))

        palette.add_block('stack1',
                          hidden=True,
                          style='basic-style-extended-vertical',
                          label=_('action 1'),
                          prim_name='stack1',
                          logo_command='stack1',
                          help_string=_('invokes Action 1 stack'))
        self.tw.lc.def_prim(
            'stack1', 0,
            Primitive(self.tw.lc.prim_invoke_stack,
                      arg_descs=[ConstantArg('stack1')]),
            True)

        palette.add_block('stack2',
                          hidden=True,
                          style='basic-style-extended-vertical',
                          label=_('action 2'),
                          prim_name='stack2',
                          logo_command='stack2',
                          help_string=_('invokes Action 2 stack'))
        self.tw.lc.def_prim(
            'stack2', 0,
            Primitive(self.tw.lc.prim_invoke_stack,
                      arg_descs=[ConstantArg('stack2')]),
            True)

        primitive_dictionary['returnstack'] = Primitive(
            self.tw.lc.prim_invoke_return_stack,
            return_type=TYPE_OBJECT,
            arg_descs=[ArgSlot(TYPE_OBJECT)])
        palette.add_block('returnstack',
                          # hidden=True,
                          style='number-style-1arg',
                          label=_('action'),
                          string_or_number=True,
                          prim_name='returnstack',
                          logo_command='action',
                          default=_('action'),
                          help_string=_(
                              'invokes named action stack and returns value'))
        self.tw.lc.def_prim('returnstack', 1,
                            primitive_dictionary['returnstack'], True)

        palette.add_block('return',
                          # hidden=True,
                          style='basic-style-1arg',
                          label=_('return'),
                          prim_name='return',
                          logo_command='stop',
                          help_string=_('returns a value'))
        self.tw.lc.def_prim(
            'return', 1,
            Primitive(self.tw.lc.prim_return,
                      arg_descs=[ArgSlot(TYPE_OBJECT)]))

    def _trash_palette(self):
        ''' The basic Turtle Art turtle palette '''

        palette = make_palette('trash',
                               colors=["#FFFF00", "#A0A000"],
                               help_string=_('trash'),
                               translation=_('trash'))

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

    # Callbacks to update labels after executing a block

    def after_arc(self, *ignored_args):
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value(
                'xcor',
                self.tw.turtles.get_active_turtle(
                ).get_xy()[0] / self.tw.coord_scale)
            self.tw.lc.update_label_value(
                'ycor',
                self.tw.turtles.get_active_turtle().get_xy(
                )[1] / self.tw.coord_scale)
            self.tw.lc.update_label_value(
                'heading',
                self.tw.turtles.get_active_turtle(
                ).get_heading())

    def after_move(self, *ignored_args, **ignored_kwargs):
        ''' Update labels after moving the turtle '''
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value(
                'xcor',
                self.tw.turtles.get_active_turtle().get_xy(
                )[0] / self.tw.coord_scale)
            self.tw.lc.update_label_value(
                'ycor',
                self.tw.turtles.get_active_turtle().get_xy(
                )[1] / self.tw.coord_scale)

    def after_right(self, *ignored_args):
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value(
                'heading',
                self.tw.turtles.get_active_turtle(
                ).get_heading())

    def after_set(self, name, value=None):
        ''' Update the associated value blocks '''
        if value is not None:
            if self.tw.lc.update_values:
                self.tw.lc.update_label_value(name, value)

    # Utilities

    def _make_constant(self, palette, block_name, label, constant_key):
        ''' Factory for constant blocks '''
        constant = CONSTANTS[constant_key]
        if isinstance(constant, Color):
            if constant.color is not None:
                logo_command = str(constant.color)
            else:
                # Black or White
                logo_command = '0 tasetshade %d' % (constant.shade)
            return_type = TYPE_COLOR
        else:
            logo_command = constant
            return_type = TYPE_NUMBER
        palette.add_block(block_name,
                          style='box-style',
                          label=label,
                          prim_name=block_name,
                          logo_command=logo_command)
        self.tw.lc.def_prim(block_name, 0,
                            Primitive(CONSTANTS.get, return_type=return_type,
                                      arg_descs=[ConstantArg(constant_key)]))
