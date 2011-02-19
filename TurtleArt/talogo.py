# -*- coding: utf-8 -*-
#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-11, Walter Bender
#Copyright (c) 2008-10, Raúl Gutiérrez Segalés

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

import gtk

from time import time
from math import sqrt
from random import uniform
from operator import isNumberType
import os.path

from UserDict import UserDict

try:
    from sugar.datastore import datastore
except ImportError:
    pass

from taconstants import TAB_LAYER, BLACK, WHITE, DEFAULT_SCALE, ICON_SIZE, \
    BLOCK_NAMES, CONSTANTS, PREFIX_DICTIONARY
from tajail import myfunc, myfunc_import
from tautils import get_pixbuf_from_journal, convert, data_from_file, \
    text_media_type, round_int, chr_to_ord, strtype, get_path

from util.RtfParser import RtfTextOnly

from gettext import gettext as _

VALUE_BLOCKS = ['box1', 'box2', 'color', 'shade', 'gray', 'scale', 'pensize',
                'heading', 'xcor', 'ycor', 'pop', 'time', 'keyboard', 'see']
MEDIA_BLOCKS_DICTIONARY = {}  # new media blocks get added here
PLUGIN_DICTIONARY = {}  # new block primitives get added here

import logging
_logger = logging.getLogger('turtleart-activity')


class noKeyError(UserDict):

    __missing__ = lambda x, y: 0


class symbol:

    def __init__(self, name):
        self.name = name
        self.nargs = None
        self.fcn = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return '#' + self.name


class logoerror(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Utility functions


def _num_type(x):
    """ Is x a number type? """
    if type(x) == int:
        return True
    if type(x) == float:
        return True
    if type(x) == ord:
        return True
    return False


def _string_to_num(x):
    """ Try to comvert a string to a number """
    xx = convert(x.replace(self.tw.decimal_point, '.'), float)
    if type(xx) is float:
        return xx
    else:
        xx, xflag = chr_to_ord(x)
        if xflag:
            return xx
        else:
            raise logoerror("#syntaxerror")


def _and(x, y):
    """ Logical and """
    return x & y


def _or(x, y):
    """ Logical or """
    return x | y


def _careful_divide(x, y):
    """ Raise error on divide by zero """
    try:
        return x / y
    except ZeroDivisionError:
        raise logoerror("#zerodivide")
    except TypeError:
        try:
            return _string_to_num(x) / _string_to_num(y)
        except ZeroDivisionError:
            raise logoerror("#zerodivide")
        except ValueError:
            raise logoerror("#syntaxerror")
        except TypeError:
            raise logoerror("#notanumber")


def _equal(x, y):
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
            return _string_to_num(x) == _string_to_num(y)
        except ValueError:
            raise logoerror("#syntaxerror")


def _less(x, y):
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
            return _string_to_num(x) < _string_to_num(y)
        except TypeError:
            raise logoerror("#notanumber")


def _more(x, y):
    """ Compare numbers and strings """
    return _less(y, x)


def _plus(x, y):
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


def _minus(x, y):
    """ Numerical subtraction """
    if _num_type(x) and _num_type(y):
        return(x - y)
    try:
        return _string_to_num(x) - _string_to_num(y)
    except TypeError:
        raise logoerror("#notanumber")


def _product(x, y):
    """ Numerical multiplication """
    if _num_type(x) and _num_type(y):
        return(x * y)
    try:
        return _string_to_num(x) * _string_to_num(y)
    except TypeError:
        raise logoerror("#notanumber")


def _mod(x, y):
    """ Numerical mod """
    if _num_type(x) and _num_type(y):
        return(x % y)
    try:
        return _string_to_num(x) % _string_to_num(y)
    except TypeError:
        raise logoerror("#notanumber")
    except ValueError:
        raise logoerror("#syntaxerror")


def _sqrt(x):
    """ Square root """
    if _num_type(x):
        if x < 0:
            raise logoerror("#negroot")
        return sqrt(x)
    try:
        return sqrt(_string_to_num(x))
    except ValueError:
        raise logoerror("#negroot")
    except TypeError:
        raise logoerror("#notanumber")


def _random(x, y):
    """ Random integer """
    if _num_type(x) and _num_type(y):
        return(int(round(uniform(x, y), 0)))
    xx, xflag = chr_to_ord(x)
    yy, yflag = chr_to_ord(y)
    if xflag and yflag:
        return chr(int(round(uniform(xx, yy), 0)))
    if not xflag:
        xx = _string_to_num(x)
    if not yflag:
        yy = _string_to_num(y)
    try:
        return(int(round(uniform(xx, yy), 0)))
    except TypeError:
        raise logoerror("#notanumber")


def _identity(x):
    """ Identity function """
    return(x)


def _just_stop():
    """ yield False to stop stack """
    yield False


def _millisecond():
    """ Current time in milliseconds """
    return time() * 1000


class LogoCode:
    """ A class for parsing Logo code """

    def __init__(self, tw):

        self.tw = tw
        self.oblist = {}

        # TODO: remove plugin blocks
        DEFPRIM = {
        '(': [1, lambda self, x: self._prim_opar(x)],
        'and': [2, lambda self, x, y: _and(x, y)],
        'arc': [2, lambda self, x, y: self._prim_arc(self.tw.canvas.arc, x,
                                                     y)],
        'audio': [1, lambda self, x: self._play_sound(x)],
        'back': [1, lambda self, x: self._prim_move(self.tw.canvas.forward,
                                                    -x)],
        'black': [0, lambda self: BLACK],
        'blue': [0, lambda self: CONSTANTS['blue']],
        'bpos': [0, lambda self: CONSTANTS['bottompos']],
        'boty': [0, lambda self: CONSTANTS['bottomy']],
        'box1': [0, lambda self: self.boxes['box1']],
        'box': [1, lambda self, x: self._box(x)],
        'box2': [0, lambda self: self.boxes['box2']],
        'bullet': [1, self._prim_bullet, True],
        'bulletlist': [1, self._prim_list, True],
        'cartesian': [0, lambda self: self.tw.set_cartesian(True)],
        'clean': [0, lambda self: self.prim_clear()],
        'clearheap': [0, lambda self: self._empty_heap()],
        'color': [0, lambda self: self.tw.canvas.color],
        'gray': [0, lambda self: self.tw.canvas.gray],
        'comment': [1, lambda self, x: self._prim_print(x, True)],
        'container': [1, lambda self, x: x],
        'cyan': [0, lambda self: CONSTANTS['cyan']],
        'define': [2, self._prim_define],
        'division': [2, lambda self, x, y: _careful_divide(x, y)],
        'equal?': [2, lambda self, x, y: _equal(x, y)],
        'fillscreen': [2, lambda self, x, y: self.tw.canvas.fillscreen(x, y)],
        'forever': [1, self._prim_forever, True],
        'forward': [1, lambda self, x: self._prim_move(self.tw.canvas.forward,
                                                      x)],
        'fullscreen': [0, lambda self: self.tw.set_fullscreen()],
        'greater?': [2, lambda self, x, y: _more(x, y)],
        'green': [0, lambda self: CONSTANTS['green']],
        'heading': [0, lambda self: self.tw.canvas.heading],
        'hideblocks': [0, lambda self: self.tw.hideblocks()],
        'hres': [0, lambda self: CONSTANTS['width']],
        'id': [1, lambda self, x: _identity(x)],
        'if': [2, self._prim_if, True],
        'ifelse': [3, self._prim_ifelse, True],
        'insertimage': [1, lambda self, x: self._insert_image(False,
                                                              filepath=x)],
        'kbinput': [0, lambda self: self._prim_kbinput()],
        'keyboard': [0, lambda self: self.keyboard],
        'left': [1, lambda self, x: self._prim_right(-x)],
        'leftx': [0, lambda self: CONSTANTS['leftx']],
        'lpos': [0, lambda self: CONSTANTS['leftpos']],
        'less?': [2, lambda self, x, y: _less(x, y)],
        'mediawait': [0, self._media_wait, True],
        'minus': [2, lambda self, x, y: _minus(x, y)],
        'mod': [2, lambda self, x, y: _mod(x, y)],
        'myfunction': [2, lambda self, f, x: self._myfunction(f, [x])],
        'myfunction2': [3, lambda self, f, x, y: self._myfunction(f, [x, y])],
        'myfunction3': [4, lambda self, f, x, y, z: self._myfunction(
                    f, [x, y, z])],
        'nop': [0, lambda self: None],
        'nop1': [0, lambda self: None],
        'nop2': [0, lambda self: None],
        'nop3': [1, lambda self, x: None],
        'not': [1, lambda self, x: not x],
        'orange': [0, lambda self: CONSTANTS['orange']],
        'or': [2, lambda self, x, y: _or(x, y)],
        'pendown': [0, lambda self: self.tw.canvas.setpen(True)],
        'pensize': [0, lambda self: self.tw.canvas.pensize],
        'penup': [0, lambda self: self.tw.canvas.setpen(False)],
        'plus': [2, lambda self, x, y: _plus(x, y)],
        'polar': [0, lambda self: self.tw.set_polar(True)],
        'pop': [0, lambda self: self._prim_pop()],
        'print': [1, lambda self, x: self._prim_print(x, False)],
        'printheap': [0, lambda self: self._prim_print_heap()],
        'product': [2, lambda self, x, y: _product(x, y)],
        'purple': [0, lambda self: CONSTANTS['purple']],
        'push': [1, lambda self, x: self._prim_push(x)],
        'random': [2, lambda self, x, y: _random(x, y)],
        'readpixel': [0, lambda self: self._read_pixel()],
        'red': [0, lambda self: CONSTANTS['red']],
        'repeat': [2, self._prim_repeat, True],
        'right': [1, lambda self, x: self._prim_right(x)],
        'rightx': [0, lambda self: CONSTANTS['rightx']],
        'rpos': [0, lambda self: CONSTANTS['rightpos']],
        'savepix': [1, lambda self, x: self._save_picture(x)],
        'savesvg': [1, lambda self, x: self._save_svg(x)],
        'scale': [0, lambda self: self.scale],
        'see': [0, lambda self: self.see()],
        'setcolor': [1, lambda self, x: self._prim_set('color',
            self.tw.canvas.setcolor, x)],
        'setgray': [1, lambda self, x: self._prim_set('gray',
            self.tw.canvas.setgray, x)],
        'seth': [1, lambda self, x: self._prim_set('heading',
            self.tw.canvas.seth, x)],
        'setpensize': [1, lambda self, x: self._prim_set('pensize',
            self.tw.canvas.setpensize, x)],
        'setscale': [1, lambda self, x: self._prim_set('scale',
            self._set_scale, x)],
        'setshade': [1, lambda self, x: self._prim_set('shade',
            self.tw.canvas.setshade, x)],
        'settextcolor': [1, lambda self, x: self.tw.canvas.settextcolor(x)],
        'settextsize': [1, lambda self, x: self.tw.canvas.settextsize(x)],
        'setxy2': [2, lambda self, x, y: self._prim_move(self.tw.canvas.setxy,
                                                        x, y)],
        'setxy': [2, lambda self, x, y: self._prim_move(self.tw.canvas.setxy,
                                                        x, y, pendown=False)],
        'shade': [0, lambda self: self.tw.canvas.shade],
        'show': [1, lambda self, x: self._show(x, True)],
        'showaligned': [1, lambda self, x: self._show(x, False)],
        'showblocks': [0, lambda self: self.tw.showblocks()],
        'skin': [1, lambda self, x: self._reskin(x)],
        'sqrt': [1, lambda self, x: _sqrt(x)],
        'stack1': [0, self._prim_stack1, True],
        'stack': [1, self._prim_stack, True],
        'stack2': [0, self._prim_stack2, True],
        'start': [0, lambda self: self._prim_start()],
        'startfill': [0, lambda self: self.tw.canvas.start_fill()],
        'stopfill': [0, lambda self: self.tw.canvas.stop_fill()],
        'stopstack': [0, lambda self: self._prim_stopstack()],
        'storeinbox1': [1, lambda self, x: self._prim_setbox('box1', None, x)],
        'storeinbox2': [1, lambda self, x: self._prim_setbox('box2', None, x)],
        'storeinbox': [2, lambda self, x, y: self._prim_setbox('box3', x, y)],
        't1x1': [2, lambda self, x, y: self._show_template1x1(x, y)],
        't1x1a': [2, lambda self, x, y: self._show_template1x1a(x, y)],
        't1x2': [3, lambda self, x, y, z: self._show_template1x2(x, y, z)],
        't2x1': [3, lambda self, x, y, z: self._show_template2x1(x, y, z)],
        't2x2': [5, lambda self, x, y, z, a, b: self._show_template2x2(
                    x, y, z, a, b)],
        'textcolor': [0, lambda self: self.tw.canvas.textcolor],
        'textsize': [0, lambda self: self.tw.textsize],
        'time': [0, lambda self: self._elapsed_time()],
        'titlex': [0, lambda self: CONSTANTS['titlex']],
        'titley': [0, lambda self: CONSTANTS['titley']],
        'topy': [0, lambda self: CONSTANTS['topy']],
        'tpos': [0, lambda self: CONSTANTS['toppos']],
        'turtle': [1, lambda self, x: self.tw.canvas.set_turtle(x)],
        'userdefined': [1, lambda self, x: self._prim_myblock([x])],
        'userdefined2': [2, lambda self, x, y: self._prim_myblock([x, y])],
        'userdefined3': [3, lambda self, x, y,
                         z: self._prim_myblock([x, y, z])],
        'video': [1, lambda self, x: self._play_video(x)],
        'vres': [0, lambda self: CONSTANTS['height']],
        'wait': [1, self._prim_wait, True],
        'white': [0, lambda self: WHITE],
        'write': [2, lambda self, x, y: self._write(self, x, y)],
        'xcor': [0, lambda self: self.tw.canvas.xcor / self.tw.coord_scale],
        'ycor': [0, lambda self: self.tw.canvas.ycor / self.tw.coord_scale],
        'yellow': [0, lambda self: CONSTANTS['yellow']]}

        for p in iter(DEFPRIM):
            if len(DEFPRIM[p]) == 2:
                self._def_prim(p, DEFPRIM[p][0], DEFPRIM[p][1])
            else:
                self._def_prim(p, DEFPRIM[p][0], DEFPRIM[p][1], DEFPRIM[p][2])

        self.symtype = type(self._intern('print'))
        self.listtype = type([])
        self.symnothing = self._intern('%nothing%')
        self.symopar = self._intern('(')
        self.iline = None
        self.cfun = None
        self.arglist = None
        self.ufun = None
        self.procstop = False
        self.running = False
        self.istack = []
        self.stacks = {}
        self.boxes = {'box1': 0, 'box2': 0}
        self.heap = []
        self.iresults = None
        self.step = None
        self.bindex = None

        self.hidden_turtle = None

        self.keyboard = 0
        self.trace = 0
        self.update_values = False
        self.gplay = None
        self.filepath = None
        self.dsobject = None
        self._start_time = None

        # Scale factors for depreciated portfolio blocks
        self.title_height = int((self.tw.canvas.height / 20) * self.tw.scale)
        self.body_height = int((self.tw.canvas.height / 40) * self.tw.scale)
        self.bullet_height = int((self.tw.canvas.height / 30) * self.tw.scale)

        self.scale = DEFAULT_SCALE

    def stop_logo(self):
        """ Stop logo is called from the Stop button on the toolbar """
        self.tw.step_time = 0
        self.step = _just_stop()
        for plugin in self.tw._plugins:
            plugin.stop()
        if self.tw.gst_available:
            from tagplay import stop_media
            stop_media(self)
        self.tw.active_turtle.show()

    def _def_prim(self, name, args, fcn, rprim=False):
        """ Define the primitives associated with the blocks """
        sym = self._intern(name)
        sym.nargs, sym.fcn = args, fcn
        sym.rprim = rprim

    def _intern(self, string):
        """ Add any new objects to the symbol list. """
        if string in self.oblist:
            return self.oblist[string]
        sym = symbol(string)
        self.oblist[string] = sym
        return sym

    def run_blocks(self, blk, blocks, run_flag):
        """ Given a block to run... """
        for k in self.stacks.keys():
            self.stacks[k] = None
        self.stacks['stack1'] = None
        self.stacks['stack2'] = None
        self.tw.saving_svg = False

        self.find_value_blocks()
        if self.trace > 0:
            self.update_values = True
        else:
            self.update_values = False

        for b in blocks:
            b.unhighlight()
            if b.name == 'hat1':
                code = self._blocks_to_code(b)
                self.stacks['stack1'] = self._readline(code)
            if b.name == 'hat2':
                code = self._blocks_to_code(b)
                self.stacks['stack2'] = self._readline(code)
            if b.name == 'hat':
                if b.connections is not None and len(b.connections) > 1 and \
                   b.connections[1] is not None:
                    code = self._blocks_to_code(b)
                    x = b.connections[1].values[0]
                    if type(convert(x, float, False)) == float:
                        if int(float(x)) == x:
                            x = int(x)
                    self.stacks['stack3' + str(x)] = self._readline(code)

        code = self._blocks_to_code(blk)
        if run_flag:
            _logger.debug("running code: %s" % (code))
            self._start_time = time()
            self._setup_cmd(code)
            if not self.tw.hide:
                self.tw.display_coordinates()
        else:
            return code

    def _blocks_to_code(self, blk):
        """ Convert a stack of blocks to pseudocode. """
        if blk is None:
            return ['%nothing%', '%nothing%']
        code = []
        dock = blk.docks[0]
        if len(dock) > 4:  # There could be a '(', ')', '[' or ']'.
            code.append(dock[4])
        if blk.name == 'savesvg':
            self.tw.saving_svg = True
        if blk.primitive is not None:  # make a tuple (prim, blk)
            code.append((blk.primitive, self.tw.block_list.list.index(blk)))
        elif len(blk.values) > 0:  # Extract the value from content blocks.
            if blk.name == 'number':
                try:
                    code.append(float(blk.values[0]))
                except ValueError:
                    code.append(float(ord(blk.values[0][0])))
            elif blk.name == 'string' or \
                    blk.name == 'title':  # depreciated block
                if type(blk.values[0]) == float or type(blk.values[0]) == int:
                    if int(blk.values[0]) == blk.values[0]:
                        blk.values[0] = int(blk.values[0])
                    code.append('#s' + str(blk.values[0]))
                else:
                    code.append('#s' + blk.values[0])
            elif blk.name in PREFIX_DICTIONARY:
                if blk.values[0] is not None:
                    code.append(PREFIX_DICTIONARY[blk.name] + \
                                    str(blk.values[0]))
                else:
                    code.append(PREFIX_DICTIONARY[blk.name] + 'None')
            elif blk.name in MEDIA_BLOCKS_DICTIONARY:
                code.append('#smedia_' + blk.name.upper())
            else:
                return ['%nothing%']
        else:
            return ['%nothing%']
        if blk.connections is not None and len(blk.connections) > 0:
            for i in range(1, len(blk.connections)):
                b = blk.connections[i]
                dock = blk.docks[i]
                if len(dock) > 4:  # There could be a '(', ')', '[' or ']'.
                    for c in dock[4]:
                        code.append(c)
                if b is not None:
                    code.extend(self._blocks_to_code(b))
                elif blk.docks[i][0] not in ['flow', 'unavailable']:
                    code.append('%nothing%')
        return code

    def _setup_cmd(self, string):
        """ Execute the psuedocode. """
        self.hidden_turtle = self.tw.active_turtle
        self.hidden_turtle.hide()  # Hide the turtle while we are running.
        self.procstop = False
        blklist = self._readline(string)
        self.step = self._start_eval(blklist)

    def _readline(self, line):
        """
        Convert the pseudocode into a list of commands.
        The block associated with the command is stored as the second element
        in a tuple, e.g., (#forward, 16)
        """
        res = []
        while line:
            token = line.pop(0)
            bindex = None
            if type(token) == tuple:
                (token, bindex) = token
            if isNumberType(token):
                res.append(token)
            elif token.isdigit():
                res.append(float(token))
            elif token[0] == '-' and token[1:].isdigit():
                res.append(-float(token[1:]))
            elif token[0] == '"':
                res.append(token[1:])
            elif token[0:2] == "#s":
                res.append(token[2:])
            elif token == '[':
                res.append(self._readline(line))
            elif token == ']':
                return res
            elif bindex is None or type(bindex) is not int:
                res.append(self._intern(token))
            else:
                res.append((self._intern(token), bindex))
        return res

    def _start_eval(self, blklist):
        """ Step through the list. """
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon("stopiton")
        elif self.tw.interactive_mode:
            self.tw.toolbar_shapes['stopiton'].set_layer(TAB_LAYER)
        self.running = True
        self._icall(self._evline, blklist)
        yield True
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon("stopitoff")
        elif self.tw.interactive_mode:
            self.tw.toolbar_shapes['stopiton'].hide()
        yield False
        self.running = False

    def _icall(self, fcn, *args):
        """ Add a function and its arguments to the program stack. """
        self.istack.append(self.step)
        self.step = fcn(*(args))

    def _evline(self, blklist):
        """ Evaluate a line of code from the list. """
        oldiline = self.iline
        self.iline = blklist[:]
        self.arglist = None
        while self.iline:
            token = self.iline[0]
            self.bindex = None
            if type(token) == tuple:
                (token, self.bindex) = self.iline[0]

            # If the blocks are visible, highlight the current block.
            if not self.tw.hide and self.bindex is not None:
                self.tw.block_list.list[self.bindex].highlight()

            # In debugging modes, we pause between steps and show the turtle.
            if self.tw.step_time > 0:
                self.tw.active_turtle.show()
                endtime = _millisecond() + self.tw.step_time * 100.
                while _millisecond() < endtime:
                    yield True
                self.tw.active_turtle.hide()

            # 'Stand-alone' booleans are handled here.
            if token == self.symopar:
                token = self.iline[1]
                if type(token) == tuple:
                    (token, self.bindex) = self.iline[1]

            # Process the token and any arguments.
            self._icall(self._eval)
            yield True

            # Time to unhighlight the current block.
            if not self.tw.hide and self.bindex is not None:
                self.tw.block_list.list[self.bindex].unhighlight()

            if self.procstop:
                break
            if self.iresult == None:
                continue

            if self.bindex is not None:
                self.tw.block_list.list[self.bindex].highlight()
            raise logoerror(str(self.iresult))
        self.iline = oldiline
        self._ireturn()
        if not self.tw.hide and self.tw.step_time > 0:
            self.tw.display_coordinates()
        yield True

    def _eval(self):
        """ Evaluate the next token on the line of code we are processing. """
        token = self.iline.pop(0)
        bindex = None
        if type(token) == tuple:
            (token, bindex) = token

        # Either we are processing a symbol or a value.
        if type(token) == self.symtype:
            # We highlight blocks here in case an error occurs...
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].highlight()
            self._icall(self._evalsym, token)
            yield True
            # and unhighlight if everything was OK.
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].unhighlight()
            res = self.iresult
        else:
            res = token

        self._ireturn(res)
        yield True

    def _evalsym(self, token):
        """ Process primitive associated with symbol token """
        self._undefined_check(token)
        oldcfun, oldarglist = self.cfun, self.arglist
        self.cfun, self.arglist = token, []

        if token.nargs == None:
            raise logoerror("#noinput")
        for i in range(token.nargs):
            self._no_args_check()
            self._icall(self._eval)
            yield True
            self.arglist.append(self.iresult)
        if self.cfun.rprim:
            if type(self.cfun.fcn) == self.listtype:
                _logger.debug("evalsym rprim list: %s" % (str(token)))
                self._icall(self._ufuncall, self.cfun.fcn)
                yield True
            else:
                # print "evalsym rprim: ", token
                self._icall(self.cfun.fcn, *self.arglist)
                yield True
            result = None
        else:
            # print "evalsym: ", token
            result = self.cfun.fcn(self, *self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        if self.arglist is not None and result == None:
            raise logoerror("%s %s %s" % \
                (oldcfun.name, _("did not output to"), self.cfun.name))
        self._ireturn(result)
        yield True

    def _ufuncall(self, body):
        """ ufuncall """
        self._ijmp(self._evline, body)
        yield True

    def doevalstep(self):
        """ evaluate one step """
        starttime = _millisecond()
        try:
            while (_millisecond() - starttime) < 120:
                try:
                    if self.step is not None:
                        self.step.next()
                    else:
                        return False
                except StopIteration:
                    # self.tw.turtles.show_all()
                    if self.hidden_turtle is not None:
                        self.hidden_turtle.show()
                        self.hidden_turtle = None
                    else:
                        self.tw.active_turtle.show()
                    return False
        except logoerror, e:
            self.tw.showlabel('syntaxerror', str(e)[1:-1])
            self.tw.turtles.show_all()
            return False
        return True

    def _ireturn(self, res=None):
        """ return value """
        self.step = self.istack.pop()
        self.iresult = res

    def _ijmp(self, fcn, *args):
        """ ijmp """
        self.step = fcn(*(args))

    def _undefined_check(self, token):
        """ Make sure token has a definition """
        if token.fcn is not None:
            return False
        if token.name == '%nothing%':
            errormsg = ''
        else:
            errormsg = "%s %s" % (_("I don't know how to"), _(token.name))
        raise logoerror(errormsg)

    def _no_args_check(self):
        """ Missing argument ? """
        if self.iline and self.iline[0] is not self.symnothing:
            return
        raise logoerror("#noinput")

    #
    # Primitives
    #

    def prim_clear(self):
        """ Clear screen """
        if self.tw.gst_available:
            from tagplay import stop_media
            stop_media(self)
        self.tw.canvas.clearscreen()
        self.scale = DEFAULT_SCALE
        # Note: users find this "feature" confusing
        # self.tw.set_polar(False)
        # self.tw.set_cartesian(False)
        self.hidden_turtle = None
        self._start_time = time()
        for name in VALUE_BLOCKS:
            self.update_label_value(name)

    def _prim_start(self):
        """ Start block: recenter """
        if self.tw.running_sugar:
            self.tw.activity.recenter()

    def _prim_wait(self, time):
        """ Show the turtle while we wait """
        self.tw.active_turtle.show()
        endtime = _millisecond() + time * 1000.
        while _millisecond() < endtime:
            yield True
        self.tw.active_turtle.hide()
        self._ireturn()
        yield True

    def _prim_repeat(self, num, blklist):
        """ Repeat list num times. """
        num = self._int(num)
        for i in range(num):
            self._icall(self._evline, blklist[:])
            yield True
            if self.procstop:
                break
        self._ireturn()
        yield True

    def _prim_bullet(self, blklist):
        """ Depreciated bullet-list block style """
        self._show_bullets(blklist)
        self._ireturn()
        yield True

    def _prim_list(self, blklist):
        """ Expandable list block """
        self._show_list(blklist)
        self._ireturn()
        yield True

    def _myfunction(self, f, x):
        """ Programmable block """
        try:
            y = myfunc(f, x)
            if str(y) == 'nan':
                _logger.debug("python function returned nan")
                self.stop_logo()
                raise logoerror("#notanumber")
            else:
                return y
        except ZeroDivisionError:
            self.stop_logo()
            raise logoerror("#zerodivide")
        except ValueError, e:
            self.stop_logo()
            raise logoerror('#' + str(e))
        except SyntaxError, e:
            self.stop_logo()
            raise logoerror('#' + str(e))
        except NameError, e:
            self.stop_logo()
            raise logoerror('#' + str(e))
        except OverflowError:
            self.stop_logo()
            raise logoerror("#overflowerror")
        except TypeError:
            self.stop_logo()
            raise logoerror("#notanumber")

    def _prim_forever(self, blklist):
        """ Do list forever """
        while True:
            self._icall(self._evline, blklist[:])
            yield True
            if self.procstop:
                break
        self._ireturn()
        yield True

    '''
    def _prim_while(self, list1, list2):
        list = [self._intern('if')]
        for i in list1:
            list.append(i)
        list.append(list2)
        while self._icall(self._evline, list[:]):
            yield True
        self._ireturn()
        yield True
    '''

    def _prim_if(self, boolean, blklist):
        """ If bool, do list """
        if boolean:
            self._icall(self._evline, blklist[:])
            yield True
        self._ireturn()
        yield True

    def _prim_ifelse(self, boolean, list1, list2):
        """ If bool, do list1, else do list2 """
        if boolean:
            self._ijmp(self._evline, list1[:])
            yield True
        else:
            self._ijmp(self._evline, list2[:])
            yield True

    def _prim_opar(self, val):
        self.iline.pop(0)
        return val

    def _prim_define(self, name, body):
        """ Define a primitive """
        if type(name) is not self.symtype:
            name = self._intern(name)
        name.nargs, name.fcn = 0, body
        name.rprim = True

    def _prim_stack(self, x):
        """ Process a named stack """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        if 'stack3' + str(x) not in self.stacks or\
           self.stacks['stack3' + str(x)] is None:
            raise logoerror("#nostack")
        self._icall(self._evline, self.stacks['stack3' + str(x)][:])
        yield True
        self.procstop = False
        self._ireturn()
        yield True

    def _prim_stack1(self):
        """ Process Stack 1 """
        if self.stacks['stack1'] is None:
            raise logoerror("#nostack")
        self._icall(self._evline, self.stacks['stack1'][:])
        yield True
        self.procstop = False
        self._ireturn()
        yield True

    def _prim_stack2(self):
        """ Process Stack 2 """
        if self.stacks['stack2'] is None:
            raise logoerror("#nostack")
        self._icall(self._evline, self.stacks['stack2'][:])
        yield True
        self.procstop = False
        self._ireturn()
        yield True

    def _prim_stopstack(self):
        """ Stop execution of a stack """
        self.procstop = True

    def _prim_print_heap(self):
        """ Display contents of heap """
        self.tw.showlabel('status', str(self.heap) + '      ')

    def _int(self, n):
        """ Raise an error if n doesn't convert to int. """
        if type(n) == int:
            return n
        elif type(n) == float:
            return int(n)
        elif type(n) == str:
            return int(ord(n[0]))
        else:
            raise logoerror("%s %s %s %s" \
                % (self.cfun.name, _("doesn't like"), str(n), _("as input")))

    def _box(self, x):
        """ Retrieve value from named box """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        try:
            return self.boxes['box3' + str(x)]
        except KeyError:
            raise logoerror("#emptybox")

    def _prim_myblock(self, x):
        """ Run Python code imported from Journal """
        if self.bindex is not None and self.bindex in self.tw.myblock:
            try:
                if len(x) == 1:
                    myfunc_import(self, self.tw.myblock[self.bindex], x[0])
                else:
                    myfunc_import(self, self.tw.myblock[self.bindex], x)
            except:
                raise logoerror("#syntaxerror")

    def _prim_print(self, n, flag):
        """ Print object n """
        if flag and (self.tw.hide or self.tw.step_time == 0):
            return
        if type(n) == str or type(n) == unicode:
            if n[0:6] == 'media_' and \
               n[6:].lower not in MEDIA_BLOCKS_DICTIONARY:
                try:
                    if self.tw.running_sugar:
                        try:
                            dsobject = datastore.get(n[6:])
                        except:
                            _logger.debug("Couldn't open %s" % (n[6:]))
                        self.tw.showlabel('status', dsobject.metadata['title'])
                        dsobject.destroy()
                    else:
                        self.tw.showlabel('status', n[6:])
                except IOError:
                    self.tw.showlabel('status', n)
            else:
                self.tw.showlabel('status', n)
        elif type(n) == int:
            self.tw.showlabel('status', n)
        else:
            self.tw.showlabel('status',
                str(round_int(n)).replace('.', self.tw.decimal_point))

    def _prim_kbinput(self):
        """ Query keyboard """
        if len(self.tw.keypress) == 1:
            self.keyboard = ord(self.tw.keypress[0])
        else:
            try:
                self.keyboard = {'Escape': 27, 'space': 32, ' ': 32,
                                 'Return': 13, 'KP_Up': 2, 'KP_Down': 4,
                                 'KP_Left': 1, 'KP_Right': 3}[self.tw.keypress]
            except KeyError:
                self.keyboard = 0
        self.update_label_value('keyboard', self.keyboard)
        self.tw.keypress = ''

    def find_value_blocks(self):
        """ Find any value blocks that may need label updates """
        self.value_blocks = {}
        for name in VALUE_BLOCKS:
            self.value_blocks[name] = self.tw.block_list.get_similar_blocks(
                'block', name)

    def update_label_value(self, name, value=None):
        """ Update the label of value blocks to reflect current value """
        if self.tw.hide or not self.tw.interactive_mode or \
           not hasattr(self, 'value_blocks'):
            return
        if value is None:
            for block in self.value_blocks[name]:
                block.spr.set_label(BLOCK_NAMES[name][0])
                block.resize()
        elif self.update_values:
            if type(value) == float:
                valstring = str(round_int(value)).replace('.',
                    self.tw.decimal_point)
            else:
                valstring = str(value)
            for block in self.value_blocks[name]:
                block.spr.set_label(BLOCK_NAMES[name][0] + ' = ' + valstring)
                block.resize()

    def _prim_set(self, name, cmd, value=None):
        """ Set a value and update the associated value blocks """
        if value is not None:
            cmd(value)
            self.update_label_value(name, value)

    def _prim_right(self, value):
        """ Turtle rotates clockwise """
        self.tw.canvas.right(float(value))
        self.update_label_value('heading', self.tw.canvas.heading)

    def _prim_move(self, cmd, value1, value2=None, pendown=True):
        """ Turtle moves by method specified in value1 """
        if value2 is None:
            cmd(value1)
        else:
            cmd(float(value1), float(value2), pendown=pendown)
        self.update_label_value('xcor',
                           self.tw.canvas.xcor / self.tw.coord_scale)
        self.update_label_value('ycor',
                           self.tw.canvas.ycor / self.tw.coord_scale)
        if len(self.value_blocks['see']) > 0:
            self.see()

    def _prim_arc(self, cmd, value1, value2):
        """ Turtle draws an arc of degree, radius """
        cmd(float(value1), float(value2))
        self.update_label_value('xcor',
                           self.tw.canvas.xcor / self.tw.coord_scale)
        self.update_label_value('ycor',
                           self.tw.canvas.ycor / self.tw.coord_scale)
        self.update_label_value('heading', self.tw.canvas.heading)
        if len(self.value_blocks['see']) > 0:
            self.see()

    def _prim_setbox(self, name, x, val):
        """ Define value of named box """
        if x is not None:
            if type(convert(x, float, False)) == float:
                if int(float(x)) == x:
                    x = int(x)
            self.boxes[name + str(x)] = val
            return

        self.boxes[name] = val
        self.update_label_value(name, val)

    def _prim_push(self, val):
        """ Push value onto FILO """
        self.heap.append(val)
        self.update_label_value('pop', val)

    def _prim_pop(self):
        """ Pop value off of FILO """
        if len(self.heap) == 0:
            raise logoerror("#emptyheap")
        else:
            if len(self.heap) == 1:
                self.update_label_value('pop')
            else:
                self.update_label_value('pop', self.heap[-2])
            return self.heap.pop(-1)

    def push_file_data_to_heap(self, dsobject):
        """ push contents of a data store object (assuming json encoding) """
        data = data_from_file(dsobject.file_path)
        if data is not None:
            for val in data:
                self.heap.append(val)
            self.update_label_value('pop', self.heap[-1])

    def _empty_heap(self):
        """ Empty FILO """
        self.heap = []

    def _save_picture(self, name):
        """ Save canvas to file as PNG """
        self.tw.save_as_image(name)

    def _save_svg(self, name):
        """ Save SVG to file """
        self.tw.canvas.svg_close()
        self.tw.save_as_image(name, True)

    def _show_list(self, sarray):
        """ Display list of media objects """
        x = self.tw.canvas.xcor / self.tw.coord_scale
        y = self.tw.canvas.ycor / self.tw.coord_scale
        for s in sarray:
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(s)
            y -= int(self.tw.canvas.textsize * self.tw.lead)

    def _set_scale(self, x):
        """ Set scale used by media object display """
        self.scale = x

    def _reskin(self, media):
        """ Reskin the turtle with an image from a file """
        scale = int(ICON_SIZE * float(self.scale) / DEFAULT_SCALE)
        if scale < 1:
            return
        self.filepath = None
        dsobject = None
        if os.path.exists(media[6:]):  # is it a path?
            self.filepath = media[6:]
        elif self.tw.running_sugar:  # is it a datastore object?
            try:
                dsobject = datastore.get(media[6:])
            except:
                _logger.debug("Couldn't open skin %s" % (media[6:]))
            if dsobject is not None:
                self.filepath = dsobject.file_path
        if self.filepath == None:
            self.tw.showlabel('nojournal', self.filepath)
            return
        pixbuf = None
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.filepath, scale,
                                                          scale)
        except:
            self.tw.showlabel('nojournal', self.filepath)
            _logger.debug("Couldn't open skin %s" % (self.filepath))
        if pixbuf is not None:
            self.tw.active_turtle.set_shapes([pixbuf])
            pen_state = self.tw.active_turtle.get_pen_state()
            if pen_state:
                self.tw.canvas.setpen(False)
            self.tw.canvas.forward(0)
            if pen_state:
                self.tw.canvas.setpen(True)

    def _x(self):
        """ Convert screen coordinates to turtle coordinates """
        return int(self.tw.canvas.width / 2) + int(self.tw.canvas.xcor)

    def _y(self):
        """ Convert screen coordinates to turtle coordinates """
        return int(self.tw.canvas.height / 2) - int(self.tw.canvas.ycor)

    def _w(self):
        """ Convert screen coordinates to turtle coordinates """
        return int((self.tw.canvas.width * self.scale) / 100.)

    def _h(self):
        """ Convert screen coordinates to turtle coordinates """
        return int((self.tw.canvas.height * self.scale) / 100.)

    def _show(self, string, center=False):
        """ Show is the general-purpose media-rendering block. """
        if type(string) == str or type(string) == unicode:
            if string in  ['media_', 'descr_', 'audio_', 'video_',
                           'media_None', 'descr_None', 'audio_None',
                           'video_None']:
                pass
            elif string[0:6] in ['media_', 'descr_', 'audio_', 'video_']:
                self.filepath = None
                self.dsobject = None
                print string[6:], MEDIA_BLOCKS_DICTIONARY
                if string[6:].lower() in MEDIA_BLOCKS_DICTIONARY:
                    MEDIA_BLOCKS_DICTIONARY[string[6:].lower()]()
                elif os.path.exists(string[6:]):  # is it a path?
                    self.filepath = string[6:]
                elif self.tw.running_sugar:  # is it a datastore object?
                    try:
                        self.dsobject = datastore.get(string[6:])
                    except:
                        _logger.debug("Couldn't find dsobject %s" % (
                                string[6:]))
                    if self.dsobject is not None:
                        self.filepath = self.dsobject.file_path
                if self.filepath == None:
                    if self.dsobject is not None:
                        self.tw.showlabel('nojournal',
                                          self.dsobject.metadata['title'])
                    else:
                        self.tw.showlabel('nojournal', string[6:])
                    _logger.debug("Couldn't open %s" % (string[6:]))
                elif string[0:6] == 'media_':
                    self._insert_image(center)
                elif string[0:6] == 'descr_':
                    mimetype = None
                    if self.dsobject is not None and \
                       'mime_type' in self.dsobject.metadata:
                        mimetype = self.dsobject.metadata['mime_type']
                    description = None
                    if self.dsobject is not None and \
                       'description' in self.dsobject.metadata:
                        description = self.dsobject.metadata['description']
                    self._insert_desc(mimetype, description)
                elif string[0:6] == 'audio_':
                    self._play_sound()
                elif string[0:6] == 'video_':
                    self._play_video()
                if self.dsobject is not None:
                    self.dsobject.destroy()
            else:  # assume it is text to display
                x, y = self._x(), self._y()
                if center:
                    y -= self.tw.canvas.textsize
                self.tw.canvas.draw_text(string, x, y,
                                         int(self.tw.canvas.textsize * \
                                             self.scale / 100.),
                                         self.tw.canvas.width - x)
        elif type(string) == float or type(string) == int:
            string = round_int(string)
            x, y = self._x(), self._y()
            if center:
                y -= self.tw.canvas.textsize
            self.tw.canvas.draw_text(string, x, y,
                                     int(self.tw.canvas.textsize * \
                                         self.scale / 100.),
                                     self.tw.canvas.width - x)

    def _insert_image(self, center=False, filepath=None):
        """ Image only (at current x, y) """
        if filepath is not None:
            self.filepath = filepath
        pixbuf = None
        w, h = self._w(), self._h()
        if w < 1 or h < 1:
            return
        if self.dsobject is not None:
            try:
                pixbuf = get_pixbuf_from_journal(self.dsobject, w, h)
            except:
                _logger.debug("Couldn't open dsobject %s" % (self.dsobject))
        if pixbuf is None and \
           self.filepath is not None and \
           self.filepath != '':
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.filepath,
                                                              w, h)
            except:
                self.tw.showlabel('nojournal', self.filepath)
                _logger.debug("Couldn't open filepath %s" % (self.filepath))
        if pixbuf is not None:
            if center:
                self.tw.canvas.draw_pixbuf(pixbuf, 0, 0,
                                           self._x() - int(w / 2),
                                           self._y() - int(h / 2), w, h,
                                           self.filepath)
            else:
                self.tw.canvas.draw_pixbuf(pixbuf, 0, 0, self._x(), self._y(),
                                           w, h, self.filepath)

    def _insert_desc(self, mimetype=None, description=None):
        """ Description text only (at current x, y) """
        w = self._w()
        if w < 1:
            return
        text = None
        if text_media_type(self.filepath):
            if mimetype == 'application/rtf' or \
               self.filepath.endswith(('rtf')):
                text_only = RtfTextOnly()
                for line in open(self.filepath, 'r'):
                    text_only.feed(line)
                    text = text_only.output
            else:
                try:
                    f = open(self.filepath, 'r')
                    text = f.read()
                    f.close()
                except IOError:
                    self.tw.showlabel('nojournal', self.filepath)
                    _logger.debug("Couldn't open %s" % (self.filepath))
        else:
            if description is not None:
                text = str(description)
            else:
                text = self.filepath
        if text is not None:
            self.tw.canvas.draw_text(text, self._x(), self._y(),
                                     self.body_height, w)

    def _media_wait(self):
        """ Wait for media to stop playing """
        if self.tw.gst_available:
            from tagplay import media_playing
            while(media_playing(self)):
                yield True
        self._ireturn()
        yield True

    def _play_sound(self):
        """ Sound file from Journal """
        if self.tw.gst_available:
            from tagplay import play_audio_from_file
            play_audio_from_file(self, self.filepath)

    def _play_video(self):
        """ Movie file from Journal """
        w, h = self._w(), self._h()
        if w < 1 or h < 1:
            return
        if self.tw.gst_available:
            from tagplay import play_movie_from_file
            play_movie_from_file(self, self.filepath, self._x(), self._y(),
                                 w, h)

    def _elapsed_time(self):
        """ Number of seconds since program execution has started or
        clean (prim_clear) block encountered """
        elapsed_time = int(time() - self._start_time)
        self.update_label_value('time', elapsed_time)
        return elapsed_time

    def see(self):
        """ Read r, g, b from the canvas and return a corresponding palette
        color """
        r, g, b, a = self.tw.canvas.get_pixel()
        color_index = self.tw.canvas.get_color_index(r, g, b)
        self.update_label_value('see', color_index)
        return color_index

    def _read_pixel(self):
        """ Read r, g, b, a from the canvas and push b, g, r to the stack """
        r, g, b, a = self.tw.canvas.get_pixel()
        self.heap.append(b)
        self.heap.append(g)
        self.heap.append(r)
    # Depreciated block methods

    def _show_template1x1(self, title, media):
        """ title, one image, and description """
        xo = self.tw.calc_position('t1x1')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) \
                      / self.tw.canvas.height
        self._set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(media.replace('media_', 'descr_'))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _show_template2x1(self, title, media1, media2):
        """ title, two images (horizontal), two descriptions """
        xo = self.tw.calc_position('t2x1')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                  self.tw.canvas.height
        self._set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media1)
        x = 0
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media2)
        y = -self.title_height
        if self.tw.running_sugar:
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(media2.replace('media_', 'descr_'))
            x = -(self.tw.canvas.width / 2) + xo
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(media1.replace('media_', 'descr_'))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _show_bullets(self, sarray):
        """ title and varible number of  bullets """
        xo = self.tw.calc_position('bullet')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._show(sarray[0])
        # set body text size
        self.tw.canvas.settextsize(self.bullet_height)
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        for s in sarray[1:]:
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(s)
            y -= int(self.bullet_height * 2 * self.tw.lead)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _show_template1x2(self, title, media1, media2):
        """ title, two images (vertical), two desciptions """
        xo = self.tw.calc_position('t1x2')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                 self.tw.canvas.height
        self._set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media1)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(media1.replace('media_', 'descr_'))
            y = -self.title_height
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(media2.replace('media_', 'descr_'))
            x = -(self.tw.canvas.width / 2) + xo
            self.tw.canvas.setxy(x, y, pendown=False)
            self._show(media2)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _show_template2x2(self, title, media1, media2, media3, media4):
        """ title and four images """
        xo = self.tw.calc_position('t2x2')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                  self.tw.canvas.height
        self._set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media1)
        x = 0
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media2)
        y = -self.title_height
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media4)
        x = -(self.tw.canvas.width / 2) + xo
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media3)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _show_template1x1a(self, title, media1):
        """ title, one media object """
        xo = self.tw.calc_position('t1x1a')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._show(title)
        # calculate and set scale for media blocks
        myscale = 90 * (self.tw.canvas.height - self.title_height * 2) / \
                       self.tw.canvas.height
        self._set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._show(media1)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _write(self, string, fsize):
        """ Write string at size """
        x = self.tw.canvas.width / 2 + int(self.tw.canvas.xcor)
        y = self.tw.canvas.height / 2 - int(self.tw.canvas.ycor)
        self.tw.canvas.draw_text(string, x, y - 15, int(fsize),
                                 self.tw.canvas.width)
