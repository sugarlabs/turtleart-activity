# -*- coding: utf-8 -*-
#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-10, Walter Bender
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
from time import clock
from math import sqrt
from random import uniform
from operator import isNumberType
from UserDict import UserDict

try:
    from sugar.datastore import datastore
except:
    pass

from taconstants import PALETTES, PALETTE_NAMES, TAB_LAYER, BLACK, WHITE, \
    DEFAULT_SCALE, ICON_SIZE
from tagplay import play_audio, play_movie_from_file, stop_media
from tajail import myfunc, myfunc_import
from tautils import get_pixbuf_from_journal, movie_media_type, convert, \
                    audio_media_type, text_media_type, round_int, chr_to_ord, \
                    strtype
from gettext import gettext as _

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


def numtype(x):
    """ Is x a number type? """
    if type(x) == int:
        return True
    if type(x) == float:
        return True
    if type(x) == ord:
        return True
    return False


def str_to_num(x):
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


def taand(x, y):
    """ Logical and """
    return x & y


def taor(x, y):
    """ Logical or """
    return x | y


def careful_divide(x, y):
    """ Raise error on divide by zero """
    try:
        return x / y
    except ZeroDivisionError:
        raise logoerror("#zerodivide")
    except TypeError:
        try:
            return str_to_num(x) / str_to_num(y)
        except ZeroDivisionError:
            raise logoerror("#zerodivide")
        except ValueError:
            raise logoerror("#syntaxerror")
        except TypeError:
            raise logoerror("#notanumber")


def taequal(x, y):
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
            return str_to_num(x) == str_to_num(y)
        except ValueError:
            raise logoerror("#syntaxerror")


def taless(x, y):
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
            return str_to_num(x) < str_to_num(y)
        except TypeError:
            raise logoerror("#notanumber")


def tamore(x, y):
    """ Compare numbers and strings """
    return taless(y, x)


def taplus(x, y):
    """ Add numbers, concat strings """
    if numtype(x) and numtype(y):
        return(x + y)
    else:
        if numtype(x):
            xx = str(round_int(x))
        else:
            xx = str(x)
        if numtype(y):
            yy = str(round_int(y))
        else:
            yy = str(y)
        return(xx + yy)


def taminus(x, y):
    """ Numerical subtraction """
    if numtype(x) and numtype(y):
        return(x - y)
    try:
        return str_to_num(x) - str_to_num(y)
    except TypeError:
        raise logoerror("#notanumber")


def taproduct(x, y):
    """ Numerical multiplication """
    if numtype(x) and numtype(y):
        return(x * y)
    try:
        return str_to_num(x) * str_to_num(y)
    except TypeError:
        raise logoerror("#notanumber")


def tamod(x, y):
    """ Numerical mod """
    if numtype(x) and numtype(y):
        return(x % y)
    try:
        return str_to_num(x) % str_to_num(y)
    except TypeError:
        raise logoerror("#notanumber")
    except ValueError:
        raise logoerror("#syntaxerror")


def tasqrt(x):
    """ Square root """
    if numtype(x):
        if x < 0:
            raise logoerror("#negroot")
        return sqrt(x)
    try:
        return sqrt(str_to_num(x))
    except ValueError:
        raise logoerror("#negroot")
    except TypeError:
        raise logoerror("#notanumber")


def tarandom(x, y):
    """ Random integer """
    if numtype(x) and numtype(y):
        return(int(round(uniform(x, y), 0)))
    xx, xflag = chr_to_ord(x)
    yy, yflag = chr_to_ord(y)
    if xflag and yflag:
        return chr(int(round(uniform(xx, yy), 0)))
    if not xflag:
        xx = str_to_num(x)
    if not yflag:
        yy = str_to_num(y)
    try:
        return(int(round(uniform(xx, yy), 0)))
    except TypeError:
        raise logoerror("#notanumber")


def identity(x):
    """ Identity function """
    return(x)


def stop_logo(tw):
    """ Stop logo is called from the Stop button on the toolbar """
    tw.step_time = 0
    tw.lc.step = just_stop()
    tw.active_turtle.show()


def just_stop():
    """ yield False to stop stack """
    yield False


def millis():
    """ Current time in milliseconds """
    return int(clock() * 1000)


class LogoCode:
    """ A class for parsing Logo code """

    def __init__(self, tw):

        self.tw = tw
        self.oblist = {}

        DEFPRIM = {
        '(': [1, lambda self, x: self.prim_opar(x)],
        'and': [2, lambda self, x, y: taand(x, y)],
        'arc': [2, lambda self, x, y: self.tw.canvas.arc(x, y)],
        'back': [1, lambda self, x: self.tw.canvas.forward(-x)],
        'black': [0, lambda self: BLACK],
        'blue': [0, lambda self: 70],
        'bpos': [0, lambda self: -self.tw.canvas.height / \
                    (self.tw.coord_scale * 2)],
        'boty': [0, lambda self: self.tw.bottomy],
        'box1': [0, lambda self: self.boxes['box1']],
        'box': [1, lambda self, x: self.box(x)],
        'box2': [0, lambda self: self.boxes['box2']],
        'bullet': [1, self.prim_bullet, True],
        'bulletlist': [1, self.prim_list, True],
        'cartesian': [0, lambda self: self.tw.set_cartesian(True)],
        'clean': [0, lambda self: self.prim_clear()],
        'clearheap': [0, lambda self: self.empty_heap()],
        'color': [0, lambda self: self.tw.canvas.color],
        'gray': [0, lambda self: self.tw.canvas.gray],
        'comment': [1, lambda self, x: self.prim_print(x, True)],
        'container': [1, lambda self, x: x],
        'cyan': [0, lambda self: 50],
        'define': [2, self.prim_define],
        'division': [2, lambda self, x, y: careful_divide(x, y)],
        'equal?': [2, lambda self,x, y: taequal(x, y)],
        'fillscreen': [2, lambda self, x, y: self.tw.canvas.fillscreen(x, y)],
        'forever': [1, self.prim_forever, True],
        'forward': [1, lambda self, x: self.tw.canvas.forward(x)],
        'fullscreen': [0, lambda self: self.tw.set_fullscreen()],
        'greater?': [2, lambda self, x, y: tamore(x, y)],
        'green': [0, lambda self: 30],
        'heading': [0, lambda self: self.tw.canvas.heading],
        'hideblocks': [0, lambda self: self.tw.hideblocks()],
        'hres': [0, lambda self: self.tw.canvas.width / self.tw.coord_scale],
        'id': [1, lambda self, x: identity(x)],
        'if': [2, self.prim_if, True],
        'ifelse': [3, self.prim_ifelse, True],
        'insertimage': [1, lambda self, x: self.insert_image(x, False)],
        'kbinput': [0, lambda self: self.prim_kbinput()],
        'keyboard': [0, lambda self: self.keyboard],
        'left': [1, lambda self, x: self.tw.canvas.right(-x)],
        'leftx': [0, lambda self: self.tw.leftx],
        'lpos': [0, lambda self: -self.tw.canvas.width / \
                    (self.tw.coord_scale * 2)],
        'less?': [2, lambda self, x, y: taless(x, y)],
        'minus': [2, lambda self, x, y: taminus(x, y)],
        'mod': [2, lambda self, x, y: tamod(x, y)],
        'myfunction': [2, lambda self, f, x: self.myfunction(f, [x])],
        'myfunction2': [3, lambda self, f, x, y: self.myfunction(f, [x, y])],
        'myfunction3': [4, lambda self, f, x, y, z: self.myfunction(
                    f, [x, y, z])],
        'nop': [0, lambda self: None],
        'nop1': [0, lambda self: None],
        'nop2': [0, lambda self: None],
        'nop3': [1, lambda self, x: None],
        'not': [1, lambda self, x: not x],
        'orange': [0, lambda self: 10],
        'or': [2, lambda self, x, y: taor(x, y)],
        'pendown': [0, lambda self: self.tw.canvas.setpen(True)],
        'pensize': [0, lambda self: self.tw.canvas.pensize],
        'penup': [0, lambda self: self.tw.canvas.setpen(False)],
        'plus': [2, lambda self, x, y: taplus(x, y)],
        'polar': [0, lambda self: self.tw.set_polar(True)],
        'pop': [0, lambda self: self.prim_pop()],
        'print': [1, lambda self, x: self.prim_print(x, False)],
        'printheap': [0, lambda self: self.prim_print_heap()],
        'product': [2, lambda self, x, y: taproduct(x, y)],
        'purple': [0, lambda self: 90],
        'push': [1, lambda self, x: self.prim_push(x)],
        'random': [2, lambda self, x, y: tarandom(x, y)],
        'readpixel': [0, lambda self: self.read_pixel()],
        'red': [0, lambda self: 0],
        'repeat': [2, self.prim_repeat, True],
        'right': [1, lambda self, x: self.tw.canvas.right(x)],
        'rightx': [0, lambda self: self.tw.rightx],
        'rpos': [0, lambda self: self.tw.canvas.width / \
                    (self.tw.coord_scale * 2)],
        'savepix': [1, lambda self, x: self.save_picture(x)],
        'savesvg': [1, lambda self, x: self.save_svg(x)],
        'scale': [0, lambda self: self.scale],
        'see': [0, lambda self: self.see()],
        'setcolor': [1, lambda self, x: self.tw.canvas.setcolor(x)],
        'setgray': [1, lambda self, x: self.tw.canvas.setgray(x)],
        'seth': [1, lambda self, x: self.tw.canvas.seth(x)],
        'setpensize': [1, lambda self, x: self.tw.canvas.setpensize(x)],
        'setscale': [1, lambda self, x: self.set_scale(x)],
        'setshade': [1, lambda self, x: self.tw.canvas.setshade(x)],
        'settextcolor': [1, lambda self, x: self.tw.canvas.settextcolor(x)],
        'settextsize': [1, lambda self, x: self.tw.canvas.settextsize(x)],
        'setxy2': [2, lambda self, x, y: self.tw.canvas.setxy(x, y)],
        'setxy': [2, lambda self, x, y: self.tw.canvas.setxy(x, y,
                                            pendown=False)],
        'shade': [0, lambda self: self.tw.canvas.shade],
        'show': [1, lambda self, x: self.show(x, True)],
        'showaligned': [1,lambda self, x: self.show(x, False)],
        'showblocks': [0, lambda self: self.tw.showblocks()],
        'skin': [1, lambda self, x: self.reskin(x)],
        'sound': [1, lambda self, x: self.play_sound(x)],
        'sqrt': [1, lambda self, x: tasqrt(x)],
        'stack1': [0, self.prim_stack1, True],
        'stack': [1, self.prim_stack, True],
        'stack2': [0, self.prim_stack2, True],
        'start': [0, lambda self: self.prim_start()],
        'startfill': [0, lambda self: self.tw.canvas.start_fill()],
        'stopfill': [0, lambda self: self.tw.canvas.stop_fill()],
        'stopstack': [0, lambda self: self.prim_stopstack()],
        'storeinbox1': [1, lambda self, x: self.prim_setbox('box1', None, x)],
        'storeinbox2': [1, lambda self, x: self.prim_setbox('box2', None, x)],
        'storeinbox': [2, lambda self, x, y: self.prim_setbox('box3', x, y)],
        't1x1': [2, lambda self, x, y: self.show_template1x1(x, y)],
        't1x1a': [2, lambda self, x, y: self.show_template1x1a(x, y)],
        't1x2': [3, lambda self, x, y, z: self.show_template1x2(x, y, z)],
        't2x1': [3, lambda self, x, y, z: self.show_template2x1(x, y, z)],
        't2x2': [5, lambda self, x, y, z, a, b: self.show_template2x2(
                                                   x, y, z, a, b)],
        'textcolor': [0, lambda self: self.tw.canvas.textcolor],
        'textsize': [0, lambda self: self.tw.textsize],
        'titlex': [0, lambda self: self.tw.titlex],
        'titley': [0, lambda self: self.tw.titley],
        'topy': [0, lambda self: self.tw.topy],
        'tpos': [0, lambda self: self.tw.canvas.height / \
                    (self.tw.coord_scale * 2)],
        'turtle': [1, lambda self, x: self.tw.canvas.set_turtle(x)],
        'userdefined': [1, lambda self, x: self.prim_myblock([x])],
        'userdefined2': [2, lambda self, x, y: self.prim_myblock([x, y])],
        'userdefined3': [3, lambda self, x, y,
                         z: self.prim_myblock([x, y, z])],
        'video': [1, lambda self, x: self.play_movie(x)],
        'vres': [0, lambda self: self.tw.canvas.height / self.tw.coord_scale],
        'wait': [1, self.prim_wait, True],
        # 'while': [2, self.prim_while, True],
        'white': [0, lambda self: WHITE],
        'write': [2, lambda self, x, y: self.write(self, x, y)],
        'xcor': [0, lambda self: self.tw.canvas.xcor / self.tw.coord_scale],
        'ycor': [0, lambda self: self.tw.canvas.ycor / self.tw.coord_scale],
        'yellow': [0, lambda self: 20]}

        for p in iter(DEFPRIM):
            if len(DEFPRIM[p]) == 2:
                self.defprim(p, DEFPRIM[p][0], DEFPRIM[p][1])
            else:
                self.defprim(p, DEFPRIM[p][0], DEFPRIM[p][1], DEFPRIM[p][2])

        self.symtype = type(self.intern('print'))
        self.listtype = type([])
        self.symnothing = self.intern('%nothing%')
        self.symopar = self.intern('(')
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

        self.hidden_turtle = None

        self.keyboard = 0
        self.trace = 0
        self.gplay = None
        self.ag = None
        self.filepath = None

        # Scale factors for depreciated portfolio blocks
        self.title_height = int((self.tw.canvas.height / 20) * self.tw.scale)
        self.body_height = int((self.tw.canvas.height / 40) * self.tw.scale)
        self.bullet_height = int((self.tw.canvas.height / 30) * self.tw.scale)

        self.scale = DEFAULT_SCALE

    def defprim(self, name, args, fcn, rprim=False):
        """ Define the primitives associated with the blocks """
        sym = self.intern(name)
        sym.nargs, sym.fcn = args, fcn
        sym.rprim = rprim

    def intern(self, string):
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

        for b in blocks:
            b.unhighlight()
            if b.name == 'hat1':
                code = self.blocks_to_code(b)
                self.stacks['stack1'] = self.readline(code)
            if b.name == 'hat2':
                code = self.blocks_to_code(b)
                self.stacks['stack2'] = self.readline(code)
            if b.name == 'hat':
                if b.connections[1] is not None:
                    code = self.blocks_to_code(b)
                    x = b.connections[1].values[0]
                    if type(convert(x, float, False)) == float:
                        if int(float(x)) == x:
                            x = int(x)
                    self.stacks['stack3' + str(x)] = self.readline(code)

        code = self.blocks_to_code(blk)
        if run_flag:
            print "running code: %s" % (code)
            self.setup_cmd(code)
            if not self.tw.hide:
                self.tw.display_coordinates()
        else:
            return code

    def blocks_to_code(self, blk):
        """ Convert a stack of blocks to pseudocode. """
        if blk is None:
            return ['%nothing%', '%nothing%']
        code = []
        dock = blk.docks[0]
        if len(dock) > 4: # There could be a '(', ')', '[' or ']'.
            code.append(dock[4])
        if blk.name == 'savesvg':
            self.tw.saving_svg = True
        if blk.primitive is not None: # make a tuple (prim, blk)
            code.append((blk.primitive, self.tw.block_list.list.index(blk)))
        elif len(blk.values) > 0:  # Extract the value from content blocks.
            if blk.name == 'number':
                try:
                    code.append(float(blk.values[0]))
                except ValueError:
                    code.append(float(ord(blk.values[0][0])))
            elif blk.name == 'string' or blk.name == 'title':
                if type(blk.values[0]) == float or type(blk.values[0]) == int:
                    if int(blk.values[0]) == blk.values[0]:
                        blk.values[0] = int(blk.values[0])
                    code.append('#s' + str(blk.values[0]))
                else:
                    code.append('#s' + blk.values[0])
            elif blk.name == 'journal':
                if blk.values[0] is not None:
                    code.append('#smedia_' + str(blk.values[0]))
                else:
                    code.append('#smedia_None')
            elif blk.name == 'description':
                if blk.values[0] is not None:
                    code.append('#sdescr_' + str(blk.values[0]))
                else:
                    code.append('#sdescr_None')
            elif blk.name == 'audio':
                if blk.values[0] is not None:
                    code.append('#saudio_' + str(blk.values[0]))
                else:
                    code.append('#saudio_None')
            else:
                return ['%nothing%']
        else:
            return ['%nothing%']
        if blk.connections is not None and len(blk.connections) > 0:
            for i in range(1, len(blk.connections)):
                b = blk.connections[i]
                dock = blk.docks[i]
                if len(dock) > 4: # There could be a '(', ')', '[' or ']'.
                    for c in dock[4]:
                        code.append(c)
                if b is not None:
                    code.extend(self.blocks_to_code(b))
                elif blk.docks[i][0] not in ['flow', 'unavailable']:
                    code.append('%nothing%')
        return code

    def setup_cmd(self, string):
        """ Execute the psuedocode. """
        self.hidden_turtle = self.tw.active_turtle
        self.hidden_turtle.hide() # Hide the turtle while we are running.
        self.procstop = False
        blklist = self.readline(string)
        self.step = self.start_eval(blklist)

    def readline(self, line):
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
                res.append(self.readline(line))
            elif token == ']':
                return res
            elif bindex is None or type(bindex) is not int:
                res.append(self.intern(token))
            else:
                res.append((self.intern(token), bindex))
        return res

    def start_eval(self, blklist):
        """ Step through the list. """
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon("stopiton")
        elif self.tw.interactive_mode:
            self.tw.toolbar_shapes['stopiton'].set_layer(TAB_LAYER)
        self.running = True
        self.icall(self.evline, blklist)
        yield True
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon("stopitoff")
        elif self.tw.interactive_mode:
            self.tw.toolbar_shapes['stopiton'].hide()
        yield False
        self.running = False

    def icall(self, fcn, *args):
        """ Add a function and its arguments to the program stack. """
        self.istack.append(self.step)
        self.step = fcn(*(args))

    def evline(self, blklist):
        """ Evaluate a line of code from the list. """
        oldiline = self.iline
        self.iline = blklist[:]
        self.arglist = None
        while self.iline:
            token = self.iline[0]
            bindex = None
            if type(token) == tuple:
                (token, bindex) = self.iline[0]

            # If the blocks are visible, highlight the current block.
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].highlight()

            # In debugging modes, we pause between steps and show the turtle.
            if self.tw.step_time > 0:
                self.tw.active_turtle.show()
                endtime = millis() + self.an_int(self.tw.step_time) * 100
                while millis() < endtime:
                    yield True
                self.tw.active_turtle.hide()

            # 'Stand-alone' booleans are handled here.
            if token == self.symopar:
                token = self.iline[1]
                if type(token) == tuple:
                    (token, bindex) = self.iline[1]

            # Process the token and any arguments.
            self.icall(self.eval)
            yield True

            # Time to unhighlight the current block.
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].unhighlight()

            if self.procstop:
                break
            if self.iresult == None:
                continue

            if bindex is not None:
                self.tw.block_list.list[bindex].highlight()
            raise logoerror(str(self.iresult))
        self.iline = oldiline
        self.ireturn()
        if not self.tw.hide and self.tw.step_time > 0:
            self.tw.display_coordinates()
        yield True

    def eval(self):
        """ Evaluate the next token on the line of code we are processing. """
        token = self.iline.pop(0)
        bindex = None
        if type(token) == tuple:
            (token, bindex) = token

        # Either we are processing a symbol or a value.
        if type(token) == self.symtype:
            # We highlight blocks here in case an error occurs...
            # print "> ", token
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].highlight()
            self.icall(self.evalsym, token)
            yield True
            # and unhighlight if everything was OK.
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].unhighlight()
            res = self.iresult
        else:
            # print ": ", token
            res = token

        self.ireturn(res)
        yield True

    def evalsym(self, token):
        """ Process primitive associated with symbol token """
        self.debug_trace(token)
        self.undefined_check(token)
        oldcfun, oldarglist = self.cfun, self.arglist
        self.cfun, self.arglist = token, []

        if token.nargs == None:
            raise logoerror("#noinput")
        for i in range(token.nargs):
            self.no_args_check()
            self.icall(self.eval)
            yield True
            self.arglist.append(self.iresult)
        if self.cfun.rprim:
            if type(self.cfun.fcn) == self.listtype:
                print "evalsym rprim list: ", token
                self.icall(self.ufuncall, self.cfun.fcn)
                yield True
            else:
                # print "evalsym rprim: ", token
                self.icall(self.cfun.fcn, *self.arglist)
                yield True
            result = None
        else:
            # print "evalsym: ", token
            result = self.cfun.fcn(self, *self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        if self.arglist is not None and result == None:
            raise logoerror("%s %s %s" % \
                (oldcfun.name, _("did not output to"), self.cfun.name))
        self.ireturn(result)
        yield True

    def ufuncall(self, body):
        """ ufuncall """
        self.ijmp(self.evline, body)
        yield True

    def doevalstep(self):
        """ evaluate one step """
        starttime = millis()
        try:
            while (millis() - starttime)<120:
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

    def ireturn(self, res=None):
        """ return value """
        self.step = self.istack.pop()
        self.iresult = res

    def ijmp(self, fcn, *args):
        """ ijmp """
        self.step = fcn(*(args))

    def debug_trace(self, token):
        """ Display debugging information """
        if self.trace:
            if token.name in PALETTES[PALETTE_NAMES.index('turtle')]:
                my_string = "%s\n%s=%d\n%s=%d\n%s=%d\n%s=%d" % \
                    (token.name, _('xcor'), int(self.tw.canvas.xcor),
                     _('ycor'), int(self.tw.canvas.ycor), _('heading'),
                     int(self.tw.canvas.heading), _('scale'), int(self.scale))
            elif token.name in PALETTES[PALETTE_NAMES.index('pen')]:
                if self.tw.canvas.pendown:
                    penstatus = _('pen down')
                else:
                    penstatus = _('pen up')
                my_string = "%s\n%s\n%s=%d\n%s=%d\n%s=%.1f" % \
                    (token.name, penstatus, _('color'),
                     int(self.tw.canvas.color), _('shade'),
                     int(self.tw.canvas.shade), _('pen size'),
                     self.tw.canvas.pensize)
            else:
                my_string = "%s\n" % (token.name)
                for k, v in self.boxes.iteritems():
                    my_string += "%s: %s\n" % (k, str(v))
            self.tw.showlabel('info', my_string)
        return

    def undefined_check(self, token):
        """ Make sure token has a definition """
        if token.fcn is not None:
            return False
        if token.name == '%nothing%':
            errormsg = ''
        else:
            errormsg = "%s %s" % (_("I don't know how to"), _(token.name))
        raise logoerror(errormsg)

    def no_args_check(self):
        """ Missing argument ? """
        if self.iline and self.iline[0] is not self.symnothing:
            return
        raise logoerror("#noinput")

    #
    # Primitives
    #

    def prim_clear(self):
        """ Clear screen """
        stop_media(self)
        self.tw.canvas.clearscreen()
        self.scale = DEFAULT_SCALE
        self.tw.set_polar(False)
        self.tw.set_cartesian(False)
        self.hidden_turtle = None

    def prim_start(self):
        """ Start block: recenter """
        if self.tw.running_sugar:
            self.tw.activity.recenter()

    def prim_wait(self, time):
        """ Show the turtle while we wait """
        self.tw.active_turtle.show()
        endtime = millis() + self.an_int(time * 1000)
        while millis()<endtime:
            yield True
        self.tw.active_turtle.hide()
        self.ireturn()
        yield True

    def prim_repeat(self, num, blklist):
        """ Repeat list num times. """
        num = self.an_int(num)
        for i in range(num):
            self.icall(self.evline, blklist[:])
            yield True
            if self.procstop:
                break
        self.ireturn()
        yield True

    def prim_bullet(self, blklist):
        """ Depreciated bullet-list block style """
        self.show_bullets(blklist)
        self.ireturn()
        yield True

    def prim_list(self, blklist):
        """ Expandable list block """
        self.show_list(blklist)
        self.ireturn()
        yield True

    def myfunction(self, f, x):
        """ Programmable block """
        try:
            y = myfunc(f, x)
            if str(y) == 'nan':
                _logger.debug("python function returned nan")
                stop_logo(self.tw)
                raise logoerror("#notanumber")
            else:
                return y
        except ZeroDivisionError:
            stop_logo(self.tw)
            raise logoerror("#zerodivide")
        except ValueError, e:
            stop_logo(self.tw)
            raise logoerror('#' + str(e))
        except SyntaxError, e:
            stop_logo(self.tw)
            raise logoerror('#' + str(e))
        except NameError, e:
            stop_logo(self.tw)
            raise logoerror('#' + str(e))
        except OverflowError:
            stop_logo(self.tw)
            raise logoerror("#overflowerror")
        except TypeError:
            stop_logo(self.tw)
            raise logoerror("#notanumber")

    def prim_forever(self, blklist):
        """ Do list forever """
        while True:
            self.icall(self.evline, blklist[:])
            yield True
            if self.procstop:
                break
        self.ireturn()
        yield True

    '''
    def prim_while(self, list1, list2):
        list = [self.intern('if')]
        for i in list1:
            list.append(i)
        list.append(list2)
        while self.icall(self.evline, list[:]):
            yield True
        self.ireturn()
        yield True
    '''

    def prim_if(self, boolean, blklist):
        """ If bool, do list """
        if boolean:
            self.icall(self.evline, blklist[:])
            yield True
        self.ireturn()
        yield True

    def prim_ifelse(self, boolean, list1, list2):
        """ If bool, do list1, else do list2 """
        if boolean:
            self.ijmp(self.evline, list1[:])
            yield True
        else:
            self.ijmp(self.evline, list2[:])
            yield True

    def prim_opar(self, val):
        self.iline.pop(0)
        return val

    def prim_define(self, name, body):
        """ Define a primitive """
        if type(name) is not self.symtype:
            name = self.intern(name)
        name.nargs, name.fcn = 0, body
        name.rprim = True

    def prim_stack(self, x):
        """ Process a named stack """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        if 'stack3' + str(x) not in self.stacks or\
           self.stacks['stack3' + str(x)] is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks['stack3' + str(x)][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def prim_stack1(self):
        """ Process Stack 1 """
        if self.stacks['stack1'] is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks['stack1'][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def prim_stack2(self):
        """ Process Stack 2 """
        if self.stacks['stack2'] is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks['stack2'][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def prim_stopstack(self):
        """ Stop execution of a stack """
        self.procstop = True

    def prim_print_heap(self):
        """ Display contents of heap """
        self.tw.showlabel('status', self.heap)

    def an_int(self, n):
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

    def box(self, x):
        """ Retrieve value from named box """
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        try:
            return self.boxes['box3' + str(x)]
        except:
            raise logoerror("#emptybox")

    def prim_myblock(self, x):
        """ Run Python code imported from Journal """
        if self.tw.myblock is not None:
            try:
                if len(x) == 1:
                    y = myfunc_import(self, self.tw.myblock, x[0])
                else:
                    y = myfunc_import(self, self.tw.myblock, x)
            except:
                raise logoerror("#syntaxerror")
        else:
            raise logoerror("#nocode")
        return

    def prim_print(self, n, flag):
        """ Print n """
        if flag and (self.tw.hide or self.tw.step_time == 0):
            return
        if type(n) == str or type(n) == unicode:
            if n[0:6] == 'media_':
                try:
                    if self.tw.running_sugar:
                        dsobject = datastore.get(n[6:])
                        self.tw.showlabel('status', dsobject.metadata['title'])
                        dsobject.destroy()
                    else:
                        self.tw.showlabel('status', n[6:])
                except:
                    self.tw.showlabel('status', n)
            else:
                self.tw.showlabel('status', n)
        elif type(n) == int:
            self.tw.showlabel('status', n)
        else:
            self.tw.showlabel('status',
                str(round_int(n)).replace('.', self.tw.decimal_point))

    def prim_kbinput(self):
        """ Query keyboard """
        if len(self.tw.keypress) == 1:
            self.keyboard = ord(self.tw.keypress[0])
        else:
            try:
                self.keyboard = {'Escape': 27, 'space': 32, ' ': 32,
                                 'Return': 13, \
                                 'KP_Up': 2, 'KP_Down': 4, 'KP_Left': 1, \
                                 'KP_Right': 3}[self.tw.keypress]
            except:
                self.keyboard = 0
        self.tw.keypress = ""

    def prim_setbox(self, name, x, val):
        """ Define value of named box """
        if x is None:
            self.boxes[name] = val
        else:
            if type(convert(x, float, False)) == float:
                if int(float(x)) == x:
                    x = int(x)
            self.boxes[name + str(x)] = val

    def prim_push(self, val):
        """ Push value onto FILO """
        self.heap.append(val)

    def prim_pop(self):
        """ Pop value off of FILO """
        try:
            return self.heap.pop(-1)
        except:
            raise logoerror("#emptyheap")

    def empty_heap(self):
        """ Empty FILO """
        self.heap = []

    def save_picture(self, name):
        """ Save canvas to file as PNG """
        self.tw.save_as_image(name)

    def save_svg(self, name):
        """ Save SVG to file """
        self.tw.canvas.svg_close()
        self.tw.save_as_image(name, True)

    def show_list(self, sarray):
        """ Display list of media objects """
        x = self.tw.canvas.xcor / self.tw.coord_scale
        y = self.tw.canvas.ycor / self.tw.coord_scale
        for s in sarray:
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(s)
            y -= int(self.tw.canvas.textsize * self.tw.lead)

    def set_scale(self, x):
        """ Set scale used by media object display """
        self.scale = x

    def reskin(self, media):
        """ Reskin the turtle with an image from a file """
        scale = int(ICON_SIZE * float(self.scale) / DEFAULT_SCALE)
        pixbuf = self.show_picture(media, 0, 0, scale, scale, False)
        if pixbuf is not None:
            self.tw.active_turtle.set_shapes([pixbuf])
            pen_state = self.tw.active_turtle.get_pen_state()
            if pen_state:
                self.tw.canvas.setpen(False)
            self.tw.canvas.forward(0)
            if pen_state:
                self.tw.canvas.setpen(True)

    def show(self, string, center=False):
        """ Show is the general-purpose media-rendering block. """
        # convert from Turtle coordinates to screen coordinates
        x = int(self.tw.canvas.width / 2) + int(self.tw.canvas.xcor)
        y = int(self.tw.canvas.height / 2) - int(self.tw.canvas.ycor)
        if type(string) == str or type(string) == unicode:
            if string == "media_None":
                pass
            elif string[0:6] == 'media_':
                self.insert_image(string, center)
            elif string[0:6] == 'descr_':
                self.insert_desc(string)
            elif string[0:6] == 'audio_':
                self.play_sound(string)
            else:
                if center:
                    y -= self.tw.canvas.textsize
                self.tw.canvas.draw_text(string, x, y,
                                         int(self.tw.canvas.textsize * \
                                             self.scale / 100.),
                                         self.tw.canvas.width - x)
        elif type(string) == float or type(string) == int:
            string = round_int(string)
            if center:
                y -= self.tw.canvas.textsize
            self.tw.canvas.draw_text(string, x, y,
                                     int(self.tw.canvas.textsize * \
                                         self.scale / 100.),
                                     self.tw.canvas.width - x)

    def insert_image(self, media, center):
        """ Image only (at current x, y) """
        w = int((self.tw.canvas.width * self.scale) / 100.)
        h = int((self.tw.canvas.height * self.scale) / 100.)
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width / 2 + int(self.tw.canvas.xcor)
        y = self.tw.canvas.height / 2 - int(self.tw.canvas.ycor)
        if center:
            x -= int(w / 2.)
            y -= int(h / 2.)
        if media[0:5] == 'media':
            self.show_picture(media, x, y, w, h)

    def insert_desc(self, media):
        """ Description text only (at current x, y) """
        w = int((self.tw.canvas.width * self.scale) / 100.)
        h = int((self.tw.canvas.height * self.scale) / 100.)
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width / 2 + int(self.tw.canvas.xcor)
        y = self.tw.canvas.height / 2 - int(self.tw.canvas.ycor)
        if media[0:5] == 'descr':
            self.show_description(media, x, y, w, h)

    def play_sound(self, audio):
        """ Sound file from Journal """
        if audio == "" or audio[6:] == "":
            raise logoerror("#nomedia")
        if self.tw.running_sugar:
            if audio[6:] != "None":
                try:
                    dsobject = datastore.get(audio[6:])
                    play_audio(self, dsobject.file_path)
                except:
                    print "Couldn't open id: " + str(audio[6:])
        else:
            play_audio(self, audio[6:])

    def show_picture(self, media, x, y, w, h, show=True):
        """ Image file from Journal """
        if w < 1 or h < 1:
            return None
        if media == "" or media[6:] == "":
            return None
        elif media[6:] is not "None":
            self.filepath = None
            pixbuf = None
            if self.tw.running_sugar:
                try:
                    dsobject = datastore.get(media[6:])
                    if movie_media_type(dsobject.file_path):
                        play_movie_from_file(self, dsobject.file_path,
                                             int(x), int(y), int(w), int(h))
                    else:
                        self.filepath = dsobject.file_path
                        pixbuf = get_pixbuf_from_journal(dsobject,
                                                         int(w), int(h))
                    dsobject.destroy()
                except:
                    # Maybe it is a pathname instead.
                    try:
                        self.filepath = media[6:0]
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                                   media[6:], int(w), int(h))
                    except:
                        self.filepath = None
                        self.tw.showlabel('nojournal', media[6:])
                        _logger.debug("Couldn't open Journal object %s" % \
                                         (media[6:]))
            else:
                try:
                    if movie_media_type(media):
                        play_movie_from_file(self, media[6:], int(x), int(y),
                                                              int(w), int(h))
                    else:
                        self.filepath = media[6:]
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                     media[6:], int(w), int(h))
                except:
                    self.filepath = None
                    self.tw.showlabel('nofile', media[6:])
                    _logger.debug("Couldn't open media object %s" % \
                                      (media[6:]))
            if pixbuf is not None and show:
                self.tw.canvas.draw_pixbuf(pixbuf, 0, 0, int(x), int(y),
                                                         int(w), int(h),
                                           self.filepath)
            else:
                return pixbuf

    def show_description(self, media, x, y, w, h):
        """ Description field from Journal """
        if media == "" or media[6:] == "":
            return
        elif media[6:] != "None":
            text = None
            if self.tw.running_sugar:
                try:
                    dsobject = datastore.get(media[6:])
                    # TODO: handle rtf, pdf, etc. (See #893)
                    if text_media_type(dsobject.file_path):
                        f = open(dsobject.file_path, 'r')
                        text = f.read()
                        f.close()
                    else:
                        text = str(dsobject.metadata['description'])
                    dsobject.destroy()
                except:
                    print "no description in %s" % (media[6:])
            else:
                try:
                    f = open(media[6:], 'r')
                    text = f.read()
                    f.close()
                except:
                    print "no text in %s?" % (media[6:])
            if text is not None:
                self.tw.canvas.draw_text(text, int(x), int(y),
                                         self.body_height, int(w))

    def see(self):
        """ Read r, g, b from the canvas and return a corresponding palette
        color """
        r, g, b, a = self.tw.canvas.get_pixel()
        return self.tw.canvas.get_color_index(r, g, b)

    def read_pixel(self):
        """ Read r, g, b, a from the canvas and push b, g, r to the stack """
        r, g, b, a = self.tw.canvas.get_pixel()
        self.heap.append(b)
        self.heap.append(g)
        self.heap.append(r)

    # Depreciated block methods

    def draw_title(self, title, x, y):
        """ slide title """
        self.tw.canvas.draw_text(title, int(x), int(y),
                                 self.title_height,
                                 self.tw.canvas.width - x)

    def show_template1x1(self, title, media):
        """ title, one image, and description """
        xo = self.tw.calc_position('t1x1')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) \
                      / self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(media.replace('media_', 'descr_'))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def show_template2x1(self, title, media1, media2):
        """ title, two images (horizontal), two descriptions """
        xo = self.tw.calc_position('t2x1')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                  self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media1)
        x = 0
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media2)
        y = -self.title_height
        if self.tw.running_sugar:
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(media2.replace('media_', 'descr_'))
            x = -(self.tw.canvas.width / 2) + xo
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(media1.replace('media_', 'descr_'))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def show_bullets(self, sarray):
        """ title and varible number of  bullets """
        xo = self.tw.calc_position('bullet')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(sarray[0])
        # set body text size
        self.tw.canvas.settextsize(self.bullet_height)
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        for s in sarray[1:]:
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(s)
            y -= int(self.bullet_height * 2 * self.tw.lead)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def show_template1x2(self, title, media1, media2):
        """ title, two images (vertical), two desciptions """
        xo = self.tw.calc_position('t1x2')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                 self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media1)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(media1.replace('media_', 'descr_'))
            y = -self.title_height
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(media2.replace('media_', 'descr_'))
            x = -(self.tw.canvas.width / 2) + xo
            self.tw.canvas.setxy(x, y, pendown=False)
            self.show(media2)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def show_template2x2(self, title, media1, media2, media3, media4):
        """ title and four images """
        xo = self.tw.calc_position('t2x2')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                  self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media1)
        x = 0
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media2)
        y = -self.title_height
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media4)
        x = -(self.tw.canvas.width / 2) + xo
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media3)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def show_template1x1a(self, title, media1):
        """ title, one media object """
        xo = self.tw.calc_position('t1x1a')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 90 * (self.tw.canvas.height - self.title_height * 2) / \
                       self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self.show(media1)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def write(self, string, fsize):
        """ Write string at size """
        x = self.tw.canvas.width / 2 + int(self.tw.canvas.xcor)
        y = self.tw.canvas.height / 2 - int(self.tw.canvas.ycor)
        self.tw.canvas.draw_text(string, x, y - 15, int(fsize),
                                 self.tw.canvas.width)
