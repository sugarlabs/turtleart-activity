# -*- coding: utf-8 -*-
# Copyright (c) 2007-8, Playful Invention Company.
# Copyright (c) 2008-13, Walter Bender
# Copyright (c) 2008-10, Raúl Gutiérrez Segalés

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

import numbers
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections import UserDict
from os.path import exists as os_path_exists
from time import time, sleep

from gi.repository import GLib
from gi.repository import GdkPixbuf
from sugar3.graphics import style

GRID_CELL_SIZE = style.GRID_CELL_SIZE

USER_HOME = os.path.expanduser('~')

import traceback

from .tablock import (Block, Media, media_blocks_dictionary)
from .taconstants import (TAB_LAYER, DEFAULT_SCALE, ICON_SIZE)
from .tajail import (myfunc, myfunc_import)
from .tapalette import (block_names, value_blocks)
from .tatype import (TATypeError, TYPES_NUMERIC)
from .tautils import (get_pixbuf_from_journal, data_from_file, get_stack_name,
                      movie_media_type, audio_media_type, image_media_type,
                      text_media_type, round_int, debug_output, find_group,
                      get_path, image_to_base64, data_to_string, data_to_file,
                      get_load_name, chooser_dialog)

try:
    from .util.RtfParser import RtfTextOnly

    RTFPARSE = True
except ImportError:
    RTFPARSE = False

from gettext import gettext as _

primitive_dictionary = {}  # new block primitives get added here


class noKeyError(UserDict):

    def __missing__(x, y):
        return 0


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
        # return repr(self.value)
        return str(self.value)


class NegativeRootError(BaseException):
    """ Similar to the ZeroDivisionError, this error is raised at runtime
    when trying to computer the square root of a negative number. """

    DEFAULT_MESSAGE = 'square root of negative number'

    def __init__(self, neg_value=None, message=DEFAULT_MESSAGE):
        self.neg_value = neg_value
        self.message = message

    def __str__(self):
        return str(self.message)


class HiddenBlock(Block):

    def __init__(self, name, value=None):
        self.name = name
        self.values = []
        if value is not None:
            self.values.append(value)
            self.primitive = None
        else:
            self.primitive = name
        self.connections = []
        self.docks = []


# Utility functions


def _change_user_path(path):
    ''' If the pathname saved in a project was from a different user, try
    changing it.'''
    # FIXME: Use regex
    if path is None:
        return None
    if len(path) < 7:
        return None
    if '/' not in path[6:]:
        return None
    if path[0:5] == '/home' and '/':
        i = path[6:].index('/')
        new_path = USER_HOME + path[6 + i:]
        if new_path == path:
            return None
        else:
            return new_path


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

        DEFPRIM = {'(': [1, lambda self, x: self._prim_opar(x)],
                   'define': [2, self._prim_define],
                   'nop': [0, lambda self: None]}

        for p in iter(DEFPRIM):
            if len(DEFPRIM[p]) == 2:
                self.def_prim(p, DEFPRIM[p][0], DEFPRIM[p][1])
            else:
                self.def_prim(p, DEFPRIM[p][0], DEFPRIM[p][1], DEFPRIM[p][2])

        self.symtype = type(self._intern('print'))
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
        self.return_values = []
        self.heap = []
        self.iresults = None
        self.step = None
        self.bindex = None

        self.hidden_turtle = None

        self.trace = 0
        self.update_values = False
        self.gplay = None
        self.filepath = None
        self.pixbuf = None
        self.dsobject = None
        self.start_time = None
        self._disable_help = False

        self.body_height = int((self.tw.canvas.height / 40) * self.tw.scale)
        self.scale = DEFAULT_SCALE
        self.value_blocks_to_update = {}

    def stop_logo(self):
        """ Stop logo is called from the Stop button on the toolbar """
        self.step = _just_stop()
        # Clear istack and iline of any code that was not executed due to Stop
        self.istack = []
        self.iline = None
        self.tw.stop_plugins()
        if self.tw.gst_available:
            from .tagplay import stop_media
            stop_media(self)
        self.tw.turtles.get_active_turtle().show()
        self.tw.running_blocks = False
        # If we disabled hover help, reenable it
        if self._disable_help:
            self.tw.no_help = False
            self._disable_help = False

    def def_prim(self, name, args, fcn, rprim=False):
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

    def get_prim_callable(self, name):
        """ Return the callable primitive associated with the given name """
        sym = self.oblist.get(name)
        if sym is not None:
            return sym.fcn
        else:
            return None

    def run_blocks(self, code):
        """Run code generated by generate_code().
        """
        self.start_time = time()
        self._setup_cmd(code)

    def generate_code(self, blk, blocks):
        """ Generate code to be passed to run_blocks() from a stack of blocks.
        """
        self._save_all_connections = []
        for b in blocks:
            tmp = []
            for c in b.connections:
                tmp.append(c)
            self._save_all_connections.append(
                {'blk': b, 'connections': tmp})

        for k in list(self.stacks.keys()):
            self.stacks[k] = None
        self.stacks['stack1'] = None
        self.stacks['stack2'] = None

        # Save state in case there is a hidden macro expansion
        self._save_blocks = None
        self._save_blk = blk
        self._save_while_blocks = []
        # self._save_connections = []

        if self.trace > 0:
            self.update_values = True
        else:
            self.update_values = False
            self.clear_value_blocks()
            # Disabled hover help while program is running
            if not self.tw.no_help:
                self._disable_help = True
                self.tw.no_help = True

        for b in blocks:
            b.unhighlight()

        # Hidden macro expansions
        for b in blocks:
            if b.name in ['returnstack']:
                action_blk, new_blocks = self._expand_return(b, blk, blocks)
                blocks = new_blocks[:]
                if b == blk:
                    blk = action_blk

        for b in blocks:
            if b.name in ['while', 'until']:
                action_blk, new_blocks = self._expand_forever(b, blk, blocks)
                blocks = new_blocks[:]
                if b == blk:
                    blk = action_blk
        for b in blocks:
            if b.name in ['forever']:
                action_blk, new_blocks = self._expand_forever(b, blk, blocks)
                blocks = new_blocks[:]
                if b == blk:
                    blk = action_blk

        for b in blocks:
            if b.name in ('hat', 'hat1', 'hat2'):
                stack_name = get_stack_name(b)
                if stack_name:
                    stack_key = self._get_stack_key(stack_name)
                    code = self._blocks_to_code(b)
                    self.stacks[stack_key] = self._readline(code)
                else:
                    self.tw.showlabel('#nostack')
                    self.tw.showblocks()
                    self.tw.running_blocks = False
                    return None

        code = self._blocks_to_code(blk)

        if self._save_blocks is not None:
            # Undo any hidden macro expansion
            blocks = self._save_blocks[:]
            blk = self._save_blk
            for b in self._save_while_blocks:
                if b[1] is not None:
                    b[0].connections[0].connections[b[1]] = b[0]
                if b[2] is not None:
                    b[0].connections[-1].connections[b[2]] = b[0]
                if b[3] is not None:
                    b[0].connections[-2].connections[b[3]] = b[0]

        if self._save_all_connections is not None:
            # Restore any connections that may have been mangled
            # during macro expansion.
            for entry in self._save_all_connections:
                b = entry['blk']
                connections = entry['connections']
                b.connections = connections[:]

        return code

    def _blocks_to_code(self, blk):
        """ Convert a stack of blocks to pseudocode. """
        if blk is None:
            return ['%nothing%', '%nothing%']
        code = []
        dock = blk.docks[0]
        # There could be a '(', ')', '[' or ']'.
        if len(dock) > 4 and dock[4] in ('[', ']', ']['):
            code.append(dock[4])
        if blk.primitive is not None:  # make a tuple (prim, blk)
            if blk in self.tw.block_list.list:
                code.append((blk.primitive,
                             self.tw.block_list.list.index(blk)))
            else:
                code.append(blk.primitive)  # Hidden block
        elif blk.is_value_block():  # Extract the value from content blocks.
            value = blk.get_value()
            if value is None:
                return ['%nothing%']
            else:
                code.append(value)
        else:
            return ['%nothing%']
        if blk.connections is not None and len(blk.connections) > 0:
            for i in range(1, len(blk.connections)):
                b = blk.connections[i]
                dock = blk.docks[i]
                # There could be a '(', ')', '[' or ']'.
                if len(dock) > 4 and dock[4] in ('[', ']', ']['):
                    for c in dock[4]:
                        code.append(c)
                if b is not None:
                    code.extend(self._blocks_to_code(b))
                elif blk.docks[i][0] not in ['flow', 'unavailable']:
                    code.append('%nothing%')
        return code

    def _setup_cmd(self, string):
        """ Execute the psuedocode. """
        self.hidden_turtle = self.tw.turtles.get_active_turtle()
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
        # debug_output(line, self.tw.running_sugar)
        res = []
        while line:
            token = line.pop(0)
            bindex = None
            if isinstance(token, tuple):
                (token, bindex) = token
            if isinstance(token, Media):
                res.append(token)
            elif isinstance(token, numbers.Number):
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
            elif bindex is None or not isinstance(bindex, int):
                res.append(self._intern(token))
            else:
                res.append((self._intern(token), bindex))
        return res

    def _start_eval(self, blklist):
        """ Step through the list. """
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon_name("stopiton")
            self.tw.activity.stop_turtle_button.set_tooltip(
                _('Stop turtle'))
        elif self.tw.interactive_mode:
            self.tw.toolbar_shapes['stopiton'].set_layer(TAB_LAYER)
        self.running = True
        self.icall(self.evline, blklist)
        yield True
        if self.tw.running_sugar:
            if self.tw.step_time == 0 and self.tw.selected_blk is None:
                self.tw.activity.stop_turtle_button.set_icon_name("hideshowon")
                self.tw.activity.stop_turtle_button.set_tooltip(
                    _('Show blocks'))
            else:
                self.tw.activity.stop_turtle_button.set_icon_name(
                    "hideshowoff")
                self.tw.activity.stop_turtle_button.set_tooltip(
                    _('Hide blocks'))
        elif self.tw.interactive_mode:
            self.tw.toolbar_shapes['stopiton'].hide()
        yield False
        self.running = False
        # If we disabled hover help, reenable it
        if self._disable_help:
            self.tw.no_help = False
            self._disable_help = False
        self.tw.display_coordinates()

    def icall(self, fcn, *args):
        """ Add a function and its arguments to the program stack. """
        self.istack.append(self.step)
        self.step = fcn(*(args))

    def evline(self, blklist, call_me=True):
        """ Evaluate a line of code from the list. """
        oldiline = self.iline
        self.iline = blklist[:]
        self.arglist = None
        while self.iline:
            token = self.iline[0]
            self.bindex = None
            if isinstance(token, tuple):
                (token, self.bindex) = self.iline[0]

            if self.bindex is not None:
                current_block = self.tw.block_list.list[self.bindex]
                # If the blocks are visible, highlight the current block.
                if not self.tw.hide:
                    current_block.highlight()
                # Anything we need to do specific for this block
                # before it is run?
                if current_block.before is not None:
                    current_block.before(self.tw, current_block)

            if not self.tw.hide and self.bindex is not None:
                current_block = self.tw.block_list.list[self.bindex]
                current_block.highlight()
                if current_block.before is not None:
                    current_block.before(current_block)

            # In debugging modes, we pause between steps and show the turtle.
            if self.tw.step_time > 0:
                self.tw.turtles.get_active_turtle().show()
                endtime = _millisecond() + self.tw.step_time * 100.
                while _millisecond() < endtime:
                    sleep(0.1)
                    yield True
                self.tw.turtles.get_active_turtle().hide()

            # 'Stand-alone' booleans are handled here.
            if token == self.symopar:
                token = self.iline[1]
                if isinstance(token, tuple):
                    (token, self.bindex) = self.iline[1]

            # Process the token and any arguments.
            self.icall(self._eval, call_me)
            yield True

            if self.bindex is not None:
                current_block = self.tw.block_list.list[self.bindex]
                # Time to unhighlight the current block.
                if not self.tw.hide:
                    current_block.unhighlight()
                # Anything we need to do specific for this block
                # after it is run?
                if current_block.after is not None:
                    current_block.after(self.tw, current_block)

            if self.procstop:
                break
            if self.iresult is None:
                continue

            if self.bindex is not None:
                self.tw.block_list.list[self.bindex].highlight()
            self.tw.showblocks()
            self.tw.display_coordinates()
            raise logoerror(str(self.iresult))
        self.iline = oldiline
        self.ireturn()
        if not self.tw.hide and self.tw.step_time > 0:
            self.tw.display_coordinates()
        yield True

    def _eval(self, call_me=True):
        """ Evaluate the next token on the line of code we are processing. """
        token = self.iline.pop(0)
        bindex = None
        if isinstance(token, tuple):
            (token, bindex) = token

        # Either we are processing a symbol or a value.
        if isinstance(token, self.symtype):
            # We highlight blocks here in case an error occurs...
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].highlight()
            self.icall(self._evalsym, token, call_me)
            yield True
            # and unhighlight if everything was OK.
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].unhighlight()
            res = self.iresult
        else:
            res = token

        self.ireturn(res)
        yield True

    def _evalsym(self, token, call_me):
        """ Process primitive associated with symbol token """
        self._undefined_check(token)
        oldcfun, oldarglist = self.cfun, self.arglist
        self.cfun, self.arglist = token, []

        if token.nargs is None:
            self.tw.showblocks()
            self.tw.display_coordinates()
            raise logoerror("#noinput")
        is_Primitive = type(self.cfun.fcn).__name__ == 'Primitive'
        is_PrimitiveDisjunction = type(self.cfun.fcn).__name__ == \
            'PrimitiveDisjunction'
        call_args = not (is_Primitive or is_PrimitiveDisjunction)
        for i in range(token.nargs):
            self._no_args_check()
            self.icall(self._eval, call_args)
            yield True
            self.arglist.append(self.iresult)
        need_to_pop_istack = False
        if self.cfun.rprim:
            if isinstance(self.cfun.fcn, list):
                # debug_output('evalsym rprim list: %s' % (str(token)),
                #              self.tw.running_sugar)
                self.icall(self._ufuncall, self.cfun.fcn, call_args)
                yield True
                need_to_pop_istack = True
                result = None
            else:
                if call_me:
                    self.icall(self.cfun.fcn, *self.arglist)
                    yield True
                    need_to_pop_istack = True
                    result = None
                else:
                    result = (self.cfun.fcn,) + tuple(self.arglist)
        else:
            need_to_pop_istack = True
            if call_me:
                result = self.cfun.fcn(self, *self.arglist)
            else:
                result = (self.cfun.fcn, self) + tuple(self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        if self.arglist is not None and result is None:
            self.tw.showblocks()
            raise logoerror("%s %s %s" %
                            (oldcfun.name, _("did not output to"),
                             self.cfun.name))
        if need_to_pop_istack:
            self.ireturn(result)
            yield True
        else:
            self.iresult = result

    def _ufuncall(self, body, call_me):
        """ ufuncall """
        self.ijmp(self.evline, body, call_me)
        yield True

    def doevalstep(self):
        """ evaluate one step """
        starttime = _millisecond()
        try:
            while (_millisecond() - starttime) < 120:
                try:
                    if self.step is None:
                        self.tw.running_blocks = False
                        return False
                    if self.tw.running_turtleart:
                        try:
                            next(self.step)
                        except ValueError:
                            debug_output('generator already executing',
                                         self.tw.running_sugar)
                            self.tw.running_blocks = False
                            return False
                        except TATypeError as tte:
                            # TODO insert the correct block name
                            # (self.cfun.name is only the name of the
                            # outermost block in this statement/ line of code)
                            # use logoerror("#notanumber") when possible
                            if tte.req_type in TYPES_NUMERIC and \
                                    tte.bad_type not in TYPES_NUMERIC:
                                raise logoerror("#notanumber")
                            else:
                                raise logoerror(
                                    "%s %s %s %s" %
                                    (self.cfun.name, _("doesn't like"),
                                     str(tte.bad_value), _("as input")))
                        except ZeroDivisionError:
                            raise logoerror("#zerodivide")
                        except NegativeRootError:
                            raise logoerror("#negroot")
                        except IndexError:
                            raise logoerror("#emptyheap")
                    else:
                        try:
                            next(self.step)
                        except BaseException as error:
                            if isinstance(error, (StopIteration,
                                                  logoerror)):
                                self.tw.running_blocks = False
                                raise error
                            else:
                                traceback.print_exc()
                                self.tw.showlabel(
                                    'status', '%s: %s' %
                                    (type(error).__name__, str(error)))
                                self.tw.running_blocks = False
                                return False
                except StopIteration:
                    if self.tw.running_turtleart:
                        # self.tw.turtles.show_all()
                        if self.hidden_turtle is not None:
                            self.hidden_turtle.show()
                            self.hidden_turtle = None
                        else:
                            self.tw.turtles.get_active_turtle().show()
                        self.tw.running_blocks = False
                        return False
                    else:
                        self.ireturn()
        except logoerror as e:
            if self.tw.running_turtleart:
                self.tw.showblocks()
                self.tw.display_coordinates()
                self.tw.showlabel('syntaxerror', str(e))
                self.tw.turtles.show_all()
            else:
                traceback.print_exc()
                self.tw.showlabel('status', 'logoerror: ' + str(e))
            self.tw.running_blocks = False
            return False
        return True

    def ireturn(self, res=None):
        """ return value """
        self.step = self.istack.pop()
        self.iresult = res

    def ijmp(self, fcn, *args):
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
        self.tw.showblocks()
        raise logoerror(errormsg)

    def _no_args_check(self):
        """ Missing argument ? """
        if self.iline and self.iline[0] is not self.symnothing:
            return
        self.tw.showblocks()
        self.tw.display_coordinates()
        raise logoerror("#noinput")

    #
    # Primitives
    #

    def _prim_opar(self, val):
        self.iline.pop(0)
        return val

    def _prim_define(self, name, body):
        """ Define a primitive """
        if not isinstance(name, self.symtype):
            name = self._intern(name)
        name.nargs, name.fcn = 0, body
        name.rprim = True

    def prim_start(self, *ignored_args):
        ''' Start block: recenter '''
        if self.tw.running_sugar:
            self.tw.activity.recenter()

    def prim_clear(self):
        """ Clear screen """
        self.tw.clear_plugins()
        self.stop_playing_media()
        self.reset_scale()
        # self.reset_timer()  # Only reset timer on 'run'
        self.clear_value_blocks()
        self.tw.canvas.clearscreen()
        self.tw.turtles.reset_turtles()
        self.reset_internals()

    def stop_playing_media(self):
        if self.tw.gst_available:
            from .tagplay import stop_media
            stop_media(self)

    def reset_scale(self):
        self.scale = DEFAULT_SCALE

    def reset_timer(self):
        self.start_time = time()

    def get_start_time(self):
        return self.start_time

    def reset_internals(self):
        self.hidden_turtle = None
        if self.tw.running_turtleart:
            self.tw.activity.restore_state()

    def prim_loop(self, controller, blklist):
        """ Execute a loop
        controller -- iterator that yields True iff the loop should be run
            once more OR a callable that returns such an iterator
        blklist -- list of callables that form the loop body """
        if not hasattr(controller, "__next__"):
            if callable(controller):
                controller = controller()
            else:
                raise TypeError("a loop controller must be either an iterator "
                                "or a callable that returns an iterator")
        while next(controller):
            self.icall(self.evline, blklist[:])
            yield True
            if self.procstop:
                break
        self.ireturn()
        yield True

    def prim_clamp(self, blklist):
        """ Run clamp blklist """
        self.icall(self.evline, blklist[:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def set_scale(self, scale):
        ''' Set scale for media blocks '''
        self.scale = scale

    def get_scale(self):
        ''' Set scale for media blocks '''
        return self.scale

    def prim_stop_stack(self):
        """ Stop execution of a stack """
        self.procstop = True

    def prim_return(self, value):
        """ Stop execution of a stack and sets return value"""
        # self.boxes['__return__'] = value
        self.return_values.append(value)
        self.procstop = True

    def active_turtle(self):
        ''' NOP used to add get_active_turtle to Python export '''
        # turtle = self.tw.turtles.get_turtle()
        pass

    def prim_turtle(self, name):
        self.tw.turtles.set_turtle(name)

    def prim_wait(self, wait_time):
        """ Show the turtle while we wait """
        self.tw.turtles.get_active_turtle().show()
        endtime = _millisecond() + wait_time * 1000.
        while _millisecond() < endtime:
            sleep(wait_time / 10.)
            yield True
        self.tw.turtles.get_active_turtle().hide()
        self.ireturn()
        yield True

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

    def prim_set_box(self, name, value):
        """ Store value in named box """
        (key, is_native) = self._get_box_key(name)
        self.boxes[key] = value
        if is_native:
            if self.update_values:
                self.update_label_value(name, value)
        else:
            if self.update_values:
                self.update_label_value('box', value, label=name)

    def prim_get_box(self, name):
        """ Retrieve value from named box """
        if name == '__return__':
            if len(self.return_values) == 0:
                raise logoerror("#emptybox")
            return self.return_values.pop()

        (key, is_native) = self._get_box_key(name)
        try:
            return self.boxes[key]
        except KeyError:
            # FIXME this looks like a syntax error in the GUI
            raise logoerror("#emptybox")

    def _get_box_key(self, name):
        """ Return the key used for this box in the boxes dictionary and a
        boolean indicating whether it is a 'native' box """
        if name in ('box1', 'box2'):
            return (name, True)
        # elif name == '__return__':
        #     return (name, True)
        else:
            # make sure '5' and '5.0' point to the same box
            if isinstance(name, (str, int)):
                try:
                    name = float(name)
                except ValueError:
                    pass
            return ('box3_' + str(name), False)

    def prim_define_stack(self, name):
        """ Top of a named stack """
        pass

    def prim_invoke_stack(self, name):
        """ Process a named stack """
        key = self._get_stack_key(name)
        if self.stacks.get(key) is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks[key][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def prim_invoke_return_stack(self, name):
        """ Process a named stack and return a value"""
        self.prim_invoke_stack(name)
        return self.boxes['__return__']

    def _get_stack_key(self, name):
        """ Return the key used for this stack in the stacks dictionary """
        if name in ('stack1', 'stack2'):
            return name
        else:
            # make sure '5' and '5.0' point to the same action stack
            if isinstance(name, (int, float)):
                if int(name) == name:
                    name = int(name)
                else:
                    name = float(name)
            return 'stack3' + str(name)

    def load_heap(self, obj):
        """ Load FILO from file """
        if not isinstance(obj, Media):
            user_path = _change_user_path(obj)

        if self.tw.running_sugar:
            # Is the object a dsobject?
            if isinstance(obj, Media) and obj.value:
                from sugar3.datastore import datastore
                try:
                    dsobject = datastore.get(obj.value)
                except BaseException:
                    debug_output("Couldn't find dsobject %s" %
                                 (obj.value), self.tw.running_sugar)
                if dsobject is not None:
                    self.push_file_data_to_heap(dsobject)
            # Or is it a path?
            elif os.path.exists(obj):
                self.push_file_data_to_heap(None, path=obj)
            elif user_path is not None and os.path.exists(user_path):
                self.push_file_data_to_heap(None, path=user_path)
            elif os.path.exists(os.path.join(
                    self.tw.activity.get_bundle_path(), obj)):
                self.push_file_data_to_heap(None, path=obj)
            else:
                # Finally try choosing a datastore object
                chooser_dialog(self.tw.parent, obj,
                               self.push_file_data_to_heap)
        else:
            # If you cannot find the file, open a chooser.
            if os.path.exists(obj):
                self.push_file_data_to_heap(None, path=obj)
            elif user_path is not None and os.path.exists(user_path):
                self.push_file_data_to_heap(None, path=user_path)
            else:
                obj, self.tw.load_save_folder = get_load_name(
                    '.*', self.tw.load_save_folder)
                if obj is not None:
                    self.push_file_data_to_heap(None, path=obj)

    def save_heap(self, obj):
        """ save FILO to file """
        if self.tw.running_sugar:
            from sugar3 import profile
            from sugar3.datastore import datastore
            from sugar3.activity import activity

            # Save JSON-encoded heap to temporary file
            heap_file = os.path.join(get_path(activity, 'instance'),
                                     'heap.txt')
            data_to_file(self.heap, heap_file)

            # Write to an existing or new dsobject
            if isinstance(obj, Media) and obj.value:
                dsobject = datastore.get(obj.value)
            else:
                dsobject = datastore.create()
                dsobject.metadata['title'] = str(obj)
                dsobject.metadata['icon-color'] = \
                    profile.get_color().to_string()
                dsobject.metadata['mime_type'] = 'text/plain'
            dsobject.set_file_path(heap_file)
            datastore.write(dsobject)
            dsobject.destroy()
        else:
            heap_file = obj
            data_to_file(self.heap, heap_file)

    def get_heap(self):
        return self.heap

    def reset_heap(self):
        """ Reset heap to an empty list """
        # empty the list rather than setting it to a new empty list object,
        # so the object references are preserved
        while self.heap:
            self.heap.pop()

    def append_heap(self, arg):
        self.heap.append(arg)

    def pop_heap(self):
        return self.heap.pop()

    def prim_myblock(self, *args):
        """ Run Python code imported from Journal """
        if self.bindex is not None and self.bindex in self.tw.myblock:
            try:
                myfunc_import(self, self.tw.myblock[self.bindex], args)
            except BaseException:
                raise logoerror("#syntaxerror")

    def prim_myfunction(self, f, *args):
        """ Programmable block (Call tajail.myfunc and convert any errors to
        logoerrors) """
        try:
            y = myfunc(f, args)
            if str(y) == 'nan':
                debug_output('Python function returned NAN',
                             self.tw.running_sugar)
                self.stop_logo()
                raise logoerror("#notanumber")
            else:
                return y
        except ZeroDivisionError:
            self.stop_logo()
            raise logoerror("#zerodivide")
        except ValueError as e:
            self.stop_logo()
            raise logoerror('#' + str(e))
        except SyntaxError as e:
            self.stop_logo()
            raise logoerror('#' + str(e))
        except NameError as e:
            self.stop_logo()
            raise logoerror('#' + str(e))
        except OverflowError:
            self.stop_logo()
            raise logoerror("#overflowerror")
        except TypeError:
            self.stop_logo()
            raise logoerror("#notanumber")

    def clear_value_blocks(self):
        if not hasattr(self, 'value_blocks_to_update'):
            return
        for name in value_blocks:
            self.update_label_value(name)

    def find_value_blocks(self):
        """ Find any value blocks that may need label updates """
        self.value_blocks_to_update = {}
        for name in value_blocks:
            self.value_blocks_to_update[name] = \
                self.tw.block_list.get_similar_blocks('block', name)

    def update_label_value(self, name, value=None, label=None):
        """ Update the label of value blocks to reflect current value """
        # If it is a named box, we need to match the label to the box
        if not self.tw.interactive_mode:
            return
        if self.tw.hide:
            return
        self.tw.display_coordinates()
        if value is None:
            if name not in self.value_blocks_to_update:
                return
            for block in self.value_blocks_to_update[name]:
                block.spr.set_label(block_names[name][0])
                if name == 'box':
                    argblk = block.connections[-2]
                    dx = block.dx
                    block.resize()
                    if argblk is not None:
                        # Move connections over...
                        dx = (block.dx - dx) * self.tw.block_scale
                        drag_group = find_group(argblk)
                        for blk in drag_group:
                            blk.spr.move_relative((dx, 0))
                else:
                    block.resize()
        elif self.update_values:
            if isinstance(value, float):
                valstring = str(round_int(value)).replace(
                    '.', self.tw.decimal_point)
            else:
                valstring = str(value)
            if name not in self.value_blocks_to_update:
                return
            for block in self.value_blocks_to_update[name]:
                if label is None:
                    block.spr.set_label(
                        block_names[name][0] + ' = ' + valstring)
                    block.resize()
                else:
                    argblk = block.connections[-2]
                    # Only update if label matches
                    if argblk is not None and argblk.spr.labels[0] == label:
                        block.spr.set_label(
                            block_names[name][0] + ' = ' + valstring)
                        dx = block.dx
                        block.resize()
                        # Move connections over...
                        dx = (block.dx - dx) * self.tw.block_scale
                        drag_group = find_group(argblk)
                        for blk in drag_group:
                            blk.spr.move_relative((dx, 0))

    def reskin(self, obj):
        """ Reskin the turtle with an image from a file """
        scale = int(ICON_SIZE * float(self.scale) / DEFAULT_SCALE)
        if scale < 1:
            return
        self.filepath = None
        self.dsobject = None

        user_path = _change_user_path(obj.value)
        if obj.value is not None and os.path.exists(obj.value):
            self.filepath = obj.value
        elif user_path is not None and os.path.exists(user_path):
            self.filepath = user_path
        elif self.tw.running_sugar:  # datastore object
            from sugar3.datastore import datastore
            try:
                self.dsobject = datastore.get(obj.value)
            except BaseException:
                debug_output("Couldn't find dsobject %s" %
                             (obj.value), self.tw.running_sugar)
            if self.dsobject is not None:
                self.filepath = self.dsobject.file_path

        if self.filepath is None:
            self.tw.showlabel('nojournal', self.filepath)
            return

        pixbuf = None
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.filepath, scale, scale)
        except BaseException:
            self.tw.showlabel('nojournal', self.filepath)
            debug_output("Couldn't open skin %s" % (self.filepath),
                         self.tw.running_sugar)
        if pixbuf is not None:
            self.tw.turtles.get_active_turtle().set_shapes([pixbuf])
            pen_state = self.tw.turtles.get_active_turtle().get_pen_state()
            if pen_state:
                self.tw.turtles.get_active_turtle().set_pen_state(False)
            self.tw.turtles.get_active_turtle().forward(0)
            if pen_state:
                self.tw.turtles.get_active_turtle().set_pen_state(True)

        if self.tw.sharing():
            if self.tw.running_sugar:
                tmp_path = get_path(self.tw.activity, 'instance')
            else:
                tmp_path = tempfile.gettempdir()
            tmp_file = os.path.join(get_path(self.tw.activity, 'instance'),
                                    'tmpfile.png')
            pixbuf.save(tmp_file, 'png', {'quality': '100'})
            data = image_to_base64(tmp_file, tmp_path)
            height = pixbuf.get_height()
            width = pixbuf.get_width()
            event = data_to_string(
                [self.tw.nick, [round_int(width), round_int(height), data]])

            def send_event(p):
                self.tw.send_event('R', event)
                return False

            GLib.idle_add(send_event)
            os.remove(tmp_file)

    def get_from_url(self, url):
        """ Get contents of URL as text or tempfile to image """
        if "://" not in url:  # no protocol
            url = "http://" + url  # assume HTTP

        try:
            req = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            debug_output("Couldn't open %s: %s" % (url, e),
                         self.tw.running_sugar)
            raise logoerror(url + ' [%d]' % (e.code))
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                debug_output("Couldn't open %s: %s" % (url, e),
                             self.tw.running_sugar)
                raise logoerror(url + ' [%d]' % (e.code))
            else:  # elif hasattr(e, 'reason'):
                debug_output("Couldn't reach server: %s" % (e),
                             self.tw.running_sugar)
                raise logoerror('#noconnection')

        mediatype = req.getheader('Content-Type')
        if mediatype[0:5] in ['image', 'audio', 'video']:
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(req.read())
            tmp.flush()
            obj = Media(mediatype[0:5], value=tmp.name)
            return obj
        else:
            return req.read()

    def showlist(self, objects):
        """ Display list of media objects """
        x = (self.tw.turtles.get_active_turtle().get_xy(
        )[0] / self.tw.coord_scale)
        y = (self.tw.turtles.get_active_turtle().get_xy(
        )[1] / self.tw.coord_scale)
        for obj in objects:
            self.tw.turtles.get_active_turtle().set_xy(x, y, pendown=False)
            self.show(obj)
            y -= int(self.tw.canvas.textsize * self.tw.lead)

    def show(self, obj, center=False):
        """ Show is the general-purpose media-rendering block. """
        mediatype = None

        if isinstance(obj, Media) and obj.value:
            self.filepath = None
            self.pixbuf = None  # Camera writes directly to pixbuf
            self.dsobject = None

            user_path = _change_user_path(obj.value)
            if obj.value.lower() in media_blocks_dictionary:
                media_blocks_dictionary[obj.value.lower()]()
                mediatype = 'image'  # camera snapshot
            elif os_path_exists(obj.value):
                self.filepath = obj.value
                mediatype = obj.type
                # If for some reason the obj.type is not set, try guessing.
                if mediatype is None and self.filepath is not None:
                    if movie_media_type(self.filepath):
                        mediatype = 'video'
                    elif audio_media_type(self.filepath):
                        mediatype = 'audio'
                    elif image_media_type(self.filepath):
                        mediatype = 'image'
                    elif text_media_type(self.filepath):
                        mediatype = 'text'
            elif user_path is not None and os_path_exists(user_path):
                self.filepath = user_path
                mediatype = obj.type
                # If for some reason the obj.type is not set, try guessing.
                if mediatype is None and self.filepath is not None:
                    if movie_media_type(self.filepath):
                        mediatype = 'video'
                    elif audio_media_type(self.filepath):
                        mediatype = 'audio'
                    elif image_media_type(self.filepath):
                        mediatype = 'image'
                    elif text_media_type(self.filepath):
                        mediatype = 'text'
            elif self.tw.running_sugar:
                from sugar3.datastore import datastore
                try:
                    self.dsobject = datastore.get(obj.value)
                except BaseException:
                    debug_output("Couldn't find dsobject %s" %
                                 (obj.value), self.tw.running_sugar)

                if self.dsobject is not None:
                    self.filepath = self.dsobject.file_path
                    if 'mime_type' in self.dsobject.metadata:
                        mimetype = self.dsobject.metadata['mime_type']
                        if mimetype[0:5] == 'video':
                            mediatype = 'video'
                        elif mimetype[0:5] == 'audio':
                            mediatype = 'audio'
                        elif mimetype[0:5] == 'image':
                            mediatype = 'image'
                        else:
                            mediatype = 'text'

            if self.pixbuf is not None:
                self.insert_image(center=center, pixbuf=True)
            elif self.filepath is None:
                if self.dsobject is not None:
                    self.tw.showlabel(
                        'nojournal',
                        self.dsobject.metadata['title'])
                else:
                    self.tw.showlabel('nojournal', obj.value)

                debug_output("Couldn't open %s" % (obj.value),
                             self.tw.running_sugar)
            elif obj.type == 'media' or mediatype == 'image':
                self.insert_image(center=center)
            elif mediatype == 'audio':
                self.play_sound()
            elif mediatype == 'video':
                self.play_video()
            elif obj.type == 'descr' or mediatype == 'text':
                mimetype = None
                if self.dsobject is not None and \
                        'mime_type' in self.dsobject.metadata:
                    mimetype = self.dsobject.metadata['mime_type']

                description = None
                if self.dsobject is not None and \
                        'description' in self.dsobject.metadata:
                    description = self.dsobject.metadata[
                        'description']

                self.insert_desc(mimetype, description)

            if self.dsobject is not None:
                self.dsobject.destroy()

        elif isinstance(obj, (str, float, int)):  # text or number
            if isinstance(obj, (float, int)):
                obj = round_int(obj)

            x, y = self.x2tx(), self.y2ty()
            if center:
                y -= self.tw.canvas.textsize

            self.tw.turtles.get_active_turtle().draw_text(
                obj, x, y,
                int(self.tw.canvas.textsize * self.scale / 100.),
                self.tw.canvas.width - x)

    def push_file_data_to_heap(self, dsobject, path=None):
        """ push contents of a data store object (assuming json encoding) """
        if dsobject:
            data = data_from_file(dsobject.file_path)
        elif path is not None:
            data = data_from_file(path)
        else:
            data = None
            debug_output("No file to open", self.tw.running_sugar)
        if data is not None:
            for val in data:
                self.heap.append(val)
            self.update_label_value('pop', self.heap[-1])

    def x2tx(self):
        """ Convert screen coordinates to turtle coordinates """
        return int(self.tw.canvas.width / 2) + \
            int(self.tw.turtles.get_active_turtle().get_xy()[0])

    def y2ty(self):
        """ Convert screen coordinates to turtle coordinates """
        return int(self.tw.canvas.height / 2) - \
            int(self.tw.turtles.get_active_turtle().get_xy()[1])

    def wpercent(self):
        """ width as a percentage of screen coordinates """
        return int((self.tw.canvas.width * self.scale) / 100.)

    def hpercent(self):
        """ height as a percentage of screen coordinates """
        return int((self.tw.canvas.height * self.scale) / 100.)

    def insert_image(self, center=False, filepath=None, resize=True,
                     offset=False, pixbuf=False):
        """ Image only (at current x, y) """
        if filepath is not None:
            self.filepath = filepath
        if not pixbuf:
            self.pixbuf = None
        w, h = self.wpercent(), self.hpercent()
        if w < 1 or h < 1:
            return
        if pixbuf:  # We may have to rescale the picture
            if w != self.pixbuf.get_width() or h != self.pixbuf.get_height():
                self.pixbuf = self.pixbuf.scale_simple(
                    w, h, GdkPixbuf.InterpType.BILINEAR)
        elif self.dsobject is not None:
            try:
                self.pixbuf = get_pixbuf_from_journal(self.dsobject, w, h)
            except BaseException:
                debug_output("Couldn't open dsobject %s" % (self.dsobject),
                             self.tw.running_sugar)
        if self.pixbuf is None and \
                self.filepath is not None and \
                self.filepath != '':
            try:
                if not resize:
                    self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.filepath)
                    w = self.pixbuf.get_width()
                    h = self.pixbuf.get_height()
                else:
                    self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                        self.filepath, w, h)
            except BaseException:
                self.tw.showlabel('nojournal', self.filepath)
                debug_output("Couldn't open filepath %s" % (self.filepath),
                             self.tw.running_sugar)
        if self.pixbuf is not None:
            # w, h are relative to screen size, not coord_scale
            # w *= self.tw.coord_scale
            # h *= self.tw.coord_scale
            if center:
                self.tw.turtles.get_active_turtle().draw_pixbuf(
                    self.pixbuf, 0, 0,
                    self.x2tx() - int(w / 2),
                    self.y2ty() - int(h / 2), w, h,
                    self.filepath)
            elif offset:
                self.tw.turtles.get_active_turtle().draw_pixbuf(
                    self.pixbuf, 0, 0,
                    self.x2tx(),
                    self.y2ty() - h,
                    w, h, self.filepath)
            else:
                self.tw.turtles.get_active_turtle().draw_pixbuf(
                    self.pixbuf, 0, 0,
                    self.x2tx(),
                    self.y2ty(),
                    w, h, self.filepath)

    def insert_desc(self, mimetype=None, description=None):
        """ Description text only (at current x, y) """
        w = self.wpercent()
        if w < 1:
            return
        text = None
        if text_media_type(self.filepath):
            if RTFPARSE and \
                    (mimetype == 'application/rtf' or self.filepath.endswith(
                        'rtf')):
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
                    debug_output("Couldn't open %s" % (self.filepath),
                                 self.tw.running_sugar)
        else:
            if description is not None:
                text = str(description)
            else:
                text = self.filepath
        if text is not None:
            self.tw.turtles.get_active_turtle().draw_text(
                text, self.x2tx(), self.y2ty(), self.body_height, w)

    def media_wait(self):
        """ Wait for media to stop playing """
        if self.tw.gst_available:
            from .tagplay import media_playing
            while (media_playing(self)):
                yield True
        self.ireturn()
        yield True

    def media_stop(self):
        """ Stop playing media"""
        if self.tw.gst_available:
            from .tagplay import stop_media
            stop_media(self)
        self.ireturn()
        yield True

    def media_pause(self):
        """ Pause media"""
        if self.tw.gst_available:
            from .tagplay import pause_media
            pause_media(self)
        self.ireturn()
        yield True

    def media_play(self):
        """ Play media"""
        if self.tw.gst_available:
            from .tagplay import play_media
            play_media(self)
        self.ireturn()
        yield True

    def play_sound(self):
        """ Sound file from Journal """
        if self.tw.gst_available:
            from .tagplay import play_audio_from_file
            play_audio_from_file(self, self.filepath)

    def play_video(self):
        """ Movie file from Journal """
        w, h = self.wpercent(), self.hpercent()
        if w < 1 or h < 1:
            return
        if self.tw.gst_available:
            from .tagplay import play_movie_from_file
            # The video window is an overlay, so we need to know where
            # the canvas is relative to the window, e.g., which
            # toolbars, if any are open.
            yoffset = 0
            if self.tw.running_sugar:
                if not self.tw.activity.is_fullscreen():
                    yoffset += GRID_CELL_SIZE
                    if self.tw.activity.toolbars_expanded():
                        yoffset += GRID_CELL_SIZE
            play_movie_from_file(self, self.filepath, self.x2tx(),
                                 self.y2ty() + yoffset, w, h)

    def _expand_return(self, b, blk, blocks):
        """ Expand a returnstack block into action name, box '__return__'
            Parameters: the repeatstack block, the top block, all blocks.
            Return all blocks."""

        # We'll restore the original blocks when we are finished
        if self._save_blocks is None:
            self._save_blocks = blocks[:]

        # Create an action block and a box
        action_blk = HiddenBlock('stack')
        blocks.append(action_blk)
        box_blk = HiddenBlock('box')
        blocks.append(box_blk)
        box_label_blk = HiddenBlock('string', value='__return__')
        blocks.append(box_label_blk)

        # Make connections to substitute blocks
        inflow = None
        cblk = None

        # FIXME: Need to use a stack for return values
        # Find a flow block to use for adding the action blk.
        tmp = b
        while tmp.connections[0] is not None:
            cblk = tmp.connections[0]
            if cblk.docks[0][0] == 'flow':
                break
            else:
                tmp = cblk

        if cblk is not None:
            if cblk.connections[0] is not None:
                inflow = cblk.connections[0]
                inflow.connections[-1] = action_blk
            cblk.connections[0] = action_blk

        action_blk.connections.append(inflow)
        action_blk.docks.append(['flow', True, 0, 0])
        action_blk.connections.append(b.connections[1])
        b.connections[1].connections[0] = action_blk
        action_blk.docks.append(['string', False, 0, 0])
        action_blk.connections.append(cblk)
        action_blk.docks.append(['flow', False, 0, 0])

        # Replace the returnstack block with a box and label.
        box_label_blk.connections.append(box_blk)
        box_label_blk.docks.append(['string', True, 0, 0])
        box_blk.connections.append(b.connections[0])
        if b.connections[0] is not None:
            for i in range(len(b.connections[0].connections)):
                if b.connections[0].connections[i] == b:
                    b.connections[0].connections[i] = box_blk
        box_blk.docks.append(['number', True, 0, 0])
        box_blk.connections.append(box_label_blk)
        box_blk.docks.append(['string', False, 0, 0])

        return action_blk, blocks

    def _expand_forever(self, b, blk, blocks):
        """ Expand a while or until block into: forever, ifelse, stopstack
            Expand a forever block to run in a separate stack
            Parameters: the loop block, the top block, all blocks.
            Return the start block of the expanded loop, and all blocks."""

        # TODO: create a less brittle way of doing this; having to
        # manage the connections and flows locally means we may run
        # into trouble if any of these block types (forever, while,
        # until. ifelse, stopstack, or stack) is changed in tablock.py

        if b.name == 'while':
            while_blk = True
        else:
            while_blk = False
        if b.name == 'until':
            until_blk = True
        else:
            until_blk = False

        # We'll restore the original blocks when we are finished
        if self._save_blocks is None:
            self._save_blocks = blocks[:]

        # Create an action block that will jump to the new stack
        action_name = '_forever %d' % (len(self._save_while_blocks) + 1)
        action_blk = HiddenBlock('stack')
        action_label_blk = HiddenBlock('string', value=action_name)

        # Create the blocks we'll put in the new stack
        forever_blk = HiddenBlock('forever')
        if while_blk or until_blk:
            ifelse_blk = HiddenBlock('ifelse')
            stopstack_blk = HiddenBlock('stopstack')
        inflow = None
        whileflow = None
        outflow = None
        boolflow = None
        if b.connections is not None:
            inflow = b.connections[0]
            if while_blk or until_blk:
                boolflow = b.connections[1]
            whileflow = b.connections[-2]
            outflow = b.connections[-1]

        # Create action block(s) to run the code inside the forever loop
        if until_blk and whileflow is not None:  # run until flow at least once
            action_flow_name = '_flow %d' % (len(self._save_while_blocks) + 1)
            action_first = HiddenBlock('stack')
            first_label_blk = HiddenBlock('string', value=action_flow_name)

        # Assign new connections and build the docks
        if inflow is not None and b in inflow.connections:
            i = inflow.connections.index(b)
            if until_blk and whileflow is not None:
                inflow.connections[i] = action_first
            else:
                inflow.connections[i] = action_blk
        else:
            i = None
        j = None
        if outflow is not None:
            if b in outflow.connections:
                j = outflow.connections.index(b)
                outflow.connections[j] = action_blk

        if until_blk and whileflow is not None:
            action_first.connections.append(inflow)
            action_first.docks.append(['flow', True, 0, 0])
            action_first.connections.append(first_label_blk)
            action_first.docks.append(['number', False, 0, 0])
            action_first.connections.append(action_blk)
            action_first.docks.append(['flow', False, 0, 0])
            first_label_blk.connections.append(action_first)
            first_label_blk.docks.append(['number', True, 0, 0])
            action_blk.connections.append(action_first)
        else:
            action_blk.connections.append(inflow)
        action_blk.docks.append(['flow', True, 0, 0])
        action_blk.connections.append(action_label_blk)
        action_blk.docks.append(['number', False, 0, 0])
        action_blk.connections.append(outflow)
        action_blk.docks.append(['flow', False, 0, 0])
        action_label_blk.connections.append(action_blk)
        action_label_blk.docks.append(['number', True, 0, 0])

        forever_blk.connections.append(None)
        forever_blk.docks.append(['flow', True, 0, 0])
        if while_blk or until_blk:
            forever_blk.connections.append(ifelse_blk)
        else:
            forever_blk.connections.append(whileflow)
        forever_blk.docks.append(['flow', False, 0, 0, '['])
        forever_blk.connections.append(outflow)
        forever_blk.docks.append(['flow', False, 0, 0, ']'])
        if while_blk or until_blk:
            ifelse_blk.connections.append(forever_blk)
            ifelse_blk.docks.append(['flow', True, 0, 0])
            ifelse_blk.connections.append(boolflow)
            ifelse_blk.docks.append(['bool', False, 0, 0])
            if while_blk:
                ifelse_blk.connections.append(whileflow)
                ifelse_blk.connections.append(stopstack_blk)
            else:  # until
                ifelse_blk.connections.append(stopstack_blk)
                ifelse_blk.connections.append(whileflow)
            ifelse_blk.docks.append(['flow', False, 0, 0, '['])
            ifelse_blk.docks.append(['flow', False, 0, 0, ']['])
            ifelse_blk.connections.append(None)
            ifelse_blk.docks.append(['flow', False, 0, 0, ']'])
            stopstack_blk.connections.append(ifelse_blk)
            stopstack_blk.docks.append(['flow', False, 0, 0])

        if whileflow is not None:
            if while_blk or until_blk:
                whileflow.connections[0] = ifelse_blk
            else:
                whileflow.connections[0] = forever_blk

        # Create a separate stacks for the forever loop and the whileflow
        code = self._blocks_to_code(forever_blk)
        self.stacks[self._get_stack_key(action_name)] = self._readline(code)
        if until_blk and whileflow is not None:
            # Create a stack from the whileflow to be called from
            # action_first, but then reconnect it to the ifelse block
            c = whileflow.connections[0]
            whileflow.connections[0] = None
            code = self._blocks_to_code(whileflow)
            self.stacks[self._get_stack_key(action_flow_name)] = \
                self._readline(code)
            whileflow.connections[0] = c

        # Save the connections so we can restore them later
        if whileflow is not None:
            self._save_while_blocks.append([b, i, j, 0])
        else:
            self._save_while_blocks.append([b, i, j, None])

        # Insert the new blocks into the stack
        i = blocks.index(b)
        if i == 0:
            blocks_left = []
        else:
            blocks_left = blocks[0:i]
        if i == len(blocks) - 1:
            blocks_right = []
        else:
            blocks_right = blocks[i + 1:]
        blocks = blocks_left[:]
        if until_blk and whileflow is not None:
            blocks.append(action_first)
        blocks.append(action_blk)
        blocks.append(forever_blk)
        if while_blk or until_blk:
            blocks.append(ifelse_blk)
            blocks.append(stopstack_blk)
        blocks.extend(blocks_right)

        if until_blk and whileflow is not None:
            return action_first, blocks
        else:
            return action_blk, blocks
