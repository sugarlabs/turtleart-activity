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

from operator import isNumberType
from UserDict import UserDict

from taconstants import TAB_LAYER, DEFAULT_SCALE, PREFIX_DICTIONARY
from tapalette import block_names, value_blocks
from tautils import get_pixbuf_from_journal, convert, data_from_file, \
    text_media_type, round_int, debug_output

from util.RtfParser import RtfTextOnly

from gettext import gettext as _

media_blocks_dictionary = {}  # new media blocks get added here
primitive_dictionary = {}  # new block primitives get added here


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

class HiddenBlock:

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
        self.pixbuf = None
        self.dsobject = None
        self.start_time = None

        self.body_height = int((self.tw.canvas.height / 40) * self.tw.scale)

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

    def run_blocks(self, blk, blocks, run_flag):
        """ Given a block to run... """
        for k in self.stacks.keys():
            self.stacks[k] = None
        self.stacks['stack1'] = None
        self.stacks['stack2'] = None
        self.tw.saving_svg = False

        # Save state in case there is a hidden macro expansion
        self.save_blocks = None
        self.save_blk = blk
        self.save_while_blks = []

        if self.trace > 0:
            self.update_values = True
        else:
            self.update_values = False

        for b in blocks:
            b.unhighlight()

        for b in blocks:
            # Hidden macro expansions
            if b.name in ['while', 'until', 'forever']:
                action_blk, new_blocks = self._expand_forever(b, blk, blocks)
                blocks = new_blocks[:]
                if b == blk:
                    blk = action_blk

        for b in blocks:
            if b.name == 'hat1':
                code = self._blocks_to_code(b)
                self.stacks['stack1'] = self._readline(code)
            elif b.name == 'hat2':
                code = self._blocks_to_code(b)
                self.stacks['stack2'] = self._readline(code)
            elif b.name == 'hat':
                if b.connections is not None and len(b.connections) > 1 and \
                   b.connections[1] is not None:
                    code = self._blocks_to_code(b)
                    try:
                        x = b.connections[1].values[0]
                    except IndexError:
                        self.tw.showlabel('#nostack')
                        return None
                    if type(convert(x, float, False)) == float:
                        if int(float(x)) == x:
                            x = int(x)
                    self.stacks['stack3' + str(x)] = self._readline(code)

        code = self._blocks_to_code(blk)

        if self.save_blocks is not None:
            # Undo any hidden macro expansion
            blocks = self.save_blocks[:]
            blk = self.save_blk
            for b in self.save_while_blks:
                if b[1] is not None:
                    b[0].connections[0].connections[b[1]] = b[0]
                if b[2] is not None:
                    b[0].connections[-1].connections[b[2]] = b[0]
                if b[3] is not None:
                    b[0].connections[-2].connections[b[3]] = b[0]

        if run_flag:
            # debug_output("running code: %s" % (code), self.tw.running_sugar)
            self.start_time = time()
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
            # special case: expand 'while' and 'until' primitives
            try:
                code.append((blk.primitive,
                             self.tw.block_list.list.index(blk)))
            except ValueError:
                code.append(blk.primitive)  # Hidden block
        elif len(blk.values) > 0:  # Extract the value from content blocks.
            if blk.name == 'number':
                try:
                    code.append(float(blk.values[0]))
                except ValueError:
                    code.append(float(ord(blk.values[0][0])))
            elif blk.name == 'string' or \
                    blk.name == 'title':  # deprecated block
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
            elif blk.name in media_blocks_dictionary:
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
        # debug_output(line, self.tw.running_sugar)
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
            self.icall(self._eval)
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
        self.ireturn()
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
            self.icall(self._evalsym, token)
            yield True
            # and unhighlight if everything was OK.
            if not self.tw.hide and bindex is not None:
                self.tw.block_list.list[bindex].unhighlight()
            res = self.iresult
        else:
            res = token

        self.ireturn(res)
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
            self.icall(self._eval)
            yield True
            self.arglist.append(self.iresult)
        if self.cfun.rprim:
            if type(self.cfun.fcn) == self.listtype:
                # debug_output('evalsym rprim list: %s' % (str(token)),
                #              self.tw.running_sugar)
                self.icall(self._ufuncall, self.cfun.fcn)
                yield True
            else:
                self.icall(self.cfun.fcn, *self.arglist)
                yield True
            result = None
        else:
            result = self.cfun.fcn(self, *self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        if self.arglist is not None and result == None:
            raise logoerror("%s %s %s" % \
                (oldcfun.name, _("did not output to"), self.cfun.name))
        self.ireturn(result)
        yield True

    def _ufuncall(self, body):
        """ ufuncall """
        self.ijmp(self.evline, body)
        yield True

    def doevalstep(self):
        """ evaluate one step """
        starttime = _millisecond()
        try:
            while (_millisecond() - starttime) < 120:
                try:
                    if self.step is not None:
                        try:
                            self.step.next()
                        except ValueError:
                            debug_output('generator already executing',
                                         self.tw.running_sugar)
                            return False
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

    def _prim_opar(self, val):
        self.iline.pop(0)
        return val

    def _prim_define(self, name, body):
        """ Define a primitive """
        if type(name) is not self.symtype:
            name = self._intern(name)
        name.nargs, name.fcn = 0, body
        name.rprim = True

    def prim_clear(self):
        """ Clear screen """
	self.tw.clear_plugins()
        if self.tw.gst_available:
            from tagplay import stop_media
            # stop_media(self)  # TODO: gplay variable
        self.tw.canvas.clearscreen()
        self.scale = DEFAULT_SCALE
        self.hidden_turtle = None
        self.start_time = time()
        for name in value_blocks:
            self.update_label_value(name)

    def int(self, n):
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

    def find_value_blocks(self):
        """ Find any value blocks that may need label updates """
        self.value_blocks_to_update = {}
        for name in value_blocks:
            self.value_blocks_to_update[name] = \
                self.tw.block_list.get_similar_blocks('block', name)

    def update_label_value(self, name, value=None):
        """ Update the label of value blocks to reflect current value """
        if self.tw.hide or not self.tw.interactive_mode:
            return
        if value is None:
            for block in self.value_blocks_to_update[name]:
                block.spr.set_label(block_names[name][0])
                block.resize()
        elif self.update_values:
            if type(value) == float:
                valstring = str(round_int(value)).replace('.',
                    self.tw.decimal_point)
            else:
                valstring = str(value)
            for block in self.value_blocks_to_update[name]:
                block.spr.set_label(block_names[name][0] + ' = ' + valstring)
                block.resize()

    def push_file_data_to_heap(self, dsobject):
        """ push contents of a data store object (assuming json encoding) """
        data = data_from_file(dsobject.file_path)
        if data is not None:
            for val in data:
                self.heap.append(val)
            self.update_label_value('pop', self.heap[-1])

    def x2tx(self):
        """ Convert screen coordinates to turtle coordinates """
        return int(self.tw.canvas.width / 2) + int(self.tw.canvas.xcor)

    def y2ty(self):
        """ Convert screen coordinates to turtle coordinates """
        return int(self.tw.canvas.height / 2) - int(self.tw.canvas.ycor)

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
                    w, h, gtk.gdk.INTERP_BILINEAR)
        elif self.dsobject is not None:
            try:
                self.pixbuf = get_pixbuf_from_journal(self.dsobject, w, h)
            except:
                debug_output("Couldn't open dsobject %s" % (self.dsobject),
                             self.tw.running_sugar)
        if self.pixbuf is None and \
           self.filepath is not None and \
           self.filepath != '':
            try:
                if not resize:
                    self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.filepath)
                    w = self.pixbuf.get_width()
                    h = self.pixbuf.get_height()
                else:
                    self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                        self.filepath, w, h)
            except:
                self.tw.showlabel('nojournal', self.filepath)
                debug_output("Couldn't open filepath %s" % (self.filepath),
                             self.tw.running_sugar)
        if self.pixbuf is not None:
            x = self.tw.canvas.xcor
            y = self.tw.canvas.ycor
            w *= self.tw.coord_scale
            h *= self.tw.coord_scale
            if center:
                self.tw.canvas.draw_pixbuf(self.pixbuf, 0, 0,
                                           self.x2tx() - int(w / 2),
                                           self.y2ty() - int(h / 2), w, h,
                                           self.filepath)
            elif offset:
                self.tw.canvas.draw_pixbuf(self.pixbuf, 0, 0, self.x2tx(),
                                           self.y2ty() - h, w, h, self.filepath)
            else:
                self.tw.canvas.draw_pixbuf(self.pixbuf, 0, 0,
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
                    debug_output("Couldn't open %s" % (self.filepath),
                                 self.tw.running_sugar)
        else:
            if description is not None:
                text = str(description)
            else:
                text = self.filepath
        if text is not None:
            self.tw.canvas.draw_text(text, self.x2tx(), self.y2ty(),
                                     self.body_height, w)

    def media_wait(self):
        """ Wait for media to stop playing """
        if self.tw.gst_available:
            from tagplay import media_playing
            while(media_playing(self)):
                yield True
        self.ireturn()
        yield True

    def play_sound(self):
        """ Sound file from Journal """
        if self.tw.gst_available:
            from tagplay import play_audio_from_file
            play_audio_from_file(self, self.filepath)

    def play_video(self):
        """ Movie file from Journal """
        w, h = self.wpercent(), self.hpercent()
        if w < 1 or h < 1:
            return
        if self.tw.gst_available:
            from tagplay import play_movie_from_file
            play_movie_from_file(self, self.filepath, self.x2tx(), self.y2ty(),
                                 w, h)

    def _expand_forever(self, b, blk, blocks):
        """ Expand a while or until block into: forever, ifelse, stopstack
            Expand a forever block to run in a separate stack """

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
        if self.save_blocks is None:
            self.save_blocks = blocks[:]

        # Create an action block that will jump to the new stack
        action_name = '#s_forever %d' % (len(self.save_while_blks) + 1)
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
            action_flow_name = '#s_flow %d' % (len(self.save_while_blks) + 1)
            action_first = HiddenBlock('stack')
            first_label_blk = HiddenBlock('string', value=action_flow_name)

        # Assign new connections and build the docks
        if inflow is not None:
            i = inflow.connections.index(b)
            if until_blk and whileflow is not None:
                inflow.connections[i] = action_first
            else:
                inflow.connections[i] = action_blk
        else:
            i = None
        if outflow is not None:
            j = outflow.connections.index(b)
            outflow.connections[j] = action_blk
        else:
            j = None

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
        self.stacks['stack3' + str(action_name)] = self._readline(code)
        if until_blk and whileflow is not None:
            # Create a stack from the whileflow to be called from
            # action_first, but then reconnect it to the ifelse block
            c = whileflow.connections[0]
            whileflow.connections[0] = None
            code = self._blocks_to_code(whileflow)
            self.stacks['stack3' + str(action_flow_name)] = self._readline(code)
            whileflow.connections[0] = c

        # Save the connections so we can restore them later
        if whileflow is not None:
            self.save_while_blks.append([b, i, j, 0])
        else:
            self.save_while_blks.append([b, i, j, None])

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
