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
import gobject
from time import clock
from math import sqrt
from random import uniform
from operator import isNumberType
import audioop
import subprocess
from UserDict import UserDict
try:
    from sugar.datastore import datastore
except:
    pass

from taconstants import PALETTES, PALETTE_NAMES, BOX_STYLE
from tagplay import play_audio, play_movie_from_file, stop_media
from tajail import myfunc, myfunc_import
from tautils import get_pixbuf_from_journal, movie_media_type,\
                    audio_media_type, round_int
from gettext import gettext as _

procstop = False

class noKeyError(UserDict):
    __missing__=lambda x,y: 0

class symbol:
    def __init__(self, name):
        self.name = name
        self.nargs = None
        self.fcn = None

    def __str__(self):
        return self.name
    def __repr__(self):
        return '#'+self.name

class logoerror(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

"""
Utility functions
"""

'''
The strategy for mixing numbers and strings is to first try
converting the string to a float; then if the string is a single
character, try converting it to an ord; finally, just treat it as a
string. Numbers appended to strings are first trreated as ints, then
floats.
'''
def convert(x, fn, try_ord=True):
    try:
        return fn(x)
    except ValueError:
        if try_ord:
            xx, flag = chr_to_ord(x)
            if flag:
                return fn(xx)
        return x

def numtype(x):
    if type(x) == int:
        return True
    if type(x) == float:
        return True
    if type(x) == ord:
        return True
    return False

def strtype(x):
    if type(x) == str:
        return True
    if type(x) == unicode:
        return True
    return False

def str_to_num(x):
    xx = convert(x, float)
    if type(xx) is float:
        return xx
    else:
        xx, xflag = chr_to_ord(x)
        if xflag:
            return xx
        else:
            raise logoerror("#syntaxerror")

def chr_to_ord(x):
    if strtype(x) and len(x) == 1:
        try:
            return ord(x[0]), True
        except ValueError:
            return x, False
    return x, False

def careful_divide(x, y):
    try:
        return x/y
    except ZeroDivisionError:
        raise logoerror("#zerodivide")
    except TypeError:
        try:
            return str_to_num(x) / str_to_num(y)
        except ZeroDivisionError:
            raise logoerror("#zerodivide")
        except ValueError:
            raise logoerror("#syntaxerror")

def taequal(x, y):
    try:
        return float(x)==float(y)
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
    try:
        return float(x)<float(y)
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
            raise logoerror("#syntaxerror")

def tamore(x, y):
    return taless(y, x)

def taplus(x, y):
    if numtype(x) and numtype(y):
        return(x+y)
    else:
        if numtype(x):
            xx = str(round_int(x))
        else:
            xx = x
        if numtype(y):
            yy = str(round_int(y))
        else:
            yy = y
        return(xx+yy)
    
def taminus(x, y):
    if numtype(x) and numtype(y):
        return(x-y)
    try:
        return str_to_num(x) - str_to_num(y)
    except TypeError:
        raise logoerror("#syntaxerror")
    
def taproduct(x, y):
    if numtype(x) and numtype(y):
        return(x*y)
    try:
        return str_to_num(x) * str_to_num(y)
    except TypeError:
        raise logoerror("#syntaxerror")

def tamod(x, y):
    if numtype(x) and numtype(y):
        return(x%y)
    try:
        return str_to_num(x) % str_to_num(y)
    except TypeError:
        raise logoerror("#syntaxerror")
    except ValueError:
        raise logoerror("#syntaxerror")
    
def tasqrt(x):
    if numtype(x):
        if x < 0:
            raise logoerror("#negroot")        
        return sqrt(x)
    try:
        return sqrt(str_to_num(x))
    except ValueError:
        raise logoerror("#negroot")
    except TypeError:
        raise logoerror("#syntaxerror")

def tarandom(x, y):
    if numtype(x) and numtype(y):
        print "trying floats %f, %f" % (x,y)
        return(int(uniform(x,y)))
    xx, xflag = chr_to_ord(x)
    yy, yflag = chr_to_ord(y)
    print xx, xflag, yy, yflag
    if xflag and yflag:
        print "trying chr %d, %d" % (xx,yy)
        return chr(int(uniform(xx,yy)))
    if not xflag:
        xx = str_to_num(x)
    if not yflag:
        yy = str_to_num(y)
    try:
        print "trying str %s, %s" % (str(xx),str(yy))
        return(int(uniform(xx,yy)))
    except TypeError:
        raise logoerror("#syntaxerror")

def identity(x):
    return(x)
    
"""
Stop_logo is called from the Stop button on the toolbar
"""
def stop_logo(tw):
    tw.step_time = 0
    tw.lc.step = just_stop()
    tw.turtles.show_all()

def just_stop():
    yield False

def millis():
    return int(clock()*1000)

"""
A class for parsing Logo Code
"""
class LogoCode:
    def __init__(self, tw):

        self.tw = tw
        self.oblist = {}

        DEFPRIM = {
        '(':[1, lambda self, x: self.prim_opar(x)],
        '/':[None, lambda self,x,y: careful_divide(x,y)],
        '-':[None, lambda self,x,y: x-y],
        '*':[None, lambda self,x,y: x*y],
        '%':[None, lambda self,x,y: x%y],
        '+':[None, lambda self,x,y: x+y],
        'and':[2, lambda self,x,y: x&y],
        'arc':[2, lambda self, x, y: self.tw.canvas.arc(x, y)],
        'back':[1, lambda self,x: self.tw.canvas.forward(-x)],
        'blue':[0, lambda self: 70],
        'bpos':[0, lambda self: -self.tw.canvas.height/(self.tw.coord_scale*2)],
        'boty':[0, lambda self: self.tw.bottomy],
        'box1':[0, lambda self: self.boxes['box1']],
        'box':[1, lambda self,x: self.box(x)],
        'box2':[0, lambda self: self.boxes['box2']],
        'bullet':[1, self.prim_bullet, True],
        'bulletlist':[1, self.prim_list, True],
        'clean':[0, lambda self: self.prim_clear()],
        'clearheap':[0, lambda self: self.empty_heap()],
        'color':[0, lambda self: self.tw.canvas.color],
        'comment':[1, lambda self,x: self.prim_print(x, True)],
        'container':[1, lambda self,x: x],
        'cyan':[0, lambda self: 50],
        'define':[2, self.prim_define],
        'division':[2, lambda self,x,y: careful_divide(x,y)],
        'equal?':[2, lambda self,x,y: taequal(x,y)],
        'fillscreen':[2, lambda self, x, y: self.tw.canvas.fillscreen(x, y)],
        'forever':[1, self.prim_forever, True],
        'forward':[1, lambda self, x: self.tw.canvas.forward(x)],
        'fullscreen':[0, lambda self: self.tw.set_fullscreen()],
        'greater?':[2, lambda self,x,y: tamore(x,y)],
        'green':[0, lambda self: 30],
        'heading':[0, lambda self: self.tw.canvas.heading],
        'hideblocks':[0, lambda self: self.tw.hideblocks()],
        'hres':[0, lambda self: self.tw.canvas.width/self.tw.coord_scale],
        'id':[1, lambda self,x: identity(x)],
        'if':[2, self.prim_if, True],
        'ifelse':[3, self.prim_ifelse, True],
        'insertimage':[1, lambda self,x: self.insert_image(x, False)],
        'kbinput':[0, lambda self: self.prim_kbinput()],
        'keyboard':[0, lambda self: self.keyboard],
        'left':[1, lambda self,x: self.tw.canvas.right(-x)],
        'leftx':[0, lambda self: self.tw.leftx],
        'lpos':[0, lambda self: -self.tw.canvas.width/(self.tw.coord_scale*2)],
        'less?':[2, lambda self,x,y: taless(x,y)],
        'minus':[2, lambda self,x,y: taminus(x,y)],
        'mod':[2, lambda self,x,y: tamod(x,y)],
        'myfunc':[1, self.prim_myfunc, True],
        'myfunction':[1, lambda self, x: self.myfunction(x)],
        'nop':[0, lambda self: None],
        'nop1':[0, lambda self: None],
        'nop2':[0, lambda self: None],
        'nop3':[1, lambda self,x: None],
        'not':[1, lambda self,x:not x],
        'orange':[0, lambda self: 10],
        'or':[2, lambda self,x,y: x|y],
        'pendown':[0, lambda self: self.tw.canvas.setpen(True)],
        'pensize':[0, lambda self: self.tw.canvas.pensize],
        'penup':[0, lambda self: self.tw.canvas.setpen(False)],
        'plus':[2, lambda self,x,y: taplus(x,y)],
        'pop':[0, lambda self: self.prim_pop()],
        'print':[1, lambda self,x: self.prim_print(x, False)],
        'printheap':[0, lambda self: self.prim_print_heap()],
        'product':[2, lambda self,x,y: taproduct(x,y)],
        'purple':[0, lambda self: 90],
        'push':[1, lambda self,x: self.prim_push(x)],
        'random':[2, lambda self,x,y: tarandom(x,y)],
        'red':[0, lambda self: 0],
        'repeat':[2, self.prim_repeat, True],
        'right':[1, lambda self, x: self.tw.canvas.right(x)],
        'rightx':[0, lambda self: self.tw.rightx],
        'rpos':[0, lambda self: self.tw.canvas.width/(self.tw.coord_scale*2)],
        'savepix':[1, lambda self, x: self.save_picture(x)],
        'scale':[0, lambda self: self.scale],
        'setcolor':[1, lambda self, x: self.tw.canvas.setcolor(x)],
        'seth':[1, lambda self, x: self.tw.canvas.seth(x)],
        'setpensize':[1, lambda self, x: self.tw.canvas.setpensize(x)],
        'setscale':[1, lambda self,x: self.set_scale(x)],
        'setshade':[1, lambda self, x: self.tw.canvas.setshade(x)],
        'settextcolor':[1, lambda self, x: self.tw.canvas.settextcolor(x)],
        'settextsize':[1, lambda self, x: self.tw.canvas.settextsize(x)],
        'setxy':[2, lambda self, x, y: self.tw.canvas.setxy(x, y)],
        'shade':[0, lambda self: self.tw.canvas.shade],
        'show':[1,lambda self, x: self.show(x, True)],
        'showaligned':[1,lambda self, x: self.show(x, False)],
        'showblocks':[0, lambda self: self.tw.showblocks()],
        'sound':[1, lambda self,x: self.play_sound(x)],
        'sqrt':[1, lambda self,x: tasqrt(x)],
        'stack1':[0, self.prim_stack1, True],
        'stack':[1, self.prim_stack, True],
        'stack2':[0, self.prim_stack2, True],
        'start':[0, lambda self: self.prim_start()],
        'stopstack':[0, self.prim_stopstack],
        'storeinbox1':[1, lambda self,x: self.prim_setbox('box1', None ,x)],
        'storeinbox2':[1, lambda self,x: self.prim_setbox('box2', None, x)],
        'storeinbox':[2, lambda self,x,y: self.prim_setbox('box3', x, y)],
        't1x1':[2, lambda self,x,y: self.show_template1x1(x, y)],
        't1x1a':[2, lambda self,x,y: self.show_template1x1a(x, y)],
        't1x2':[3, lambda self,x,y,z: self.show_template1x2(x, y, z)],
        't2x1':[3, lambda self,x,y,z: self.show_template2x1(x, y, z)],
        't2x2':[5, lambda self,x,y,z,a,b: self.show_template2x2(x, y, z, a, b)],
        'textcolor':[0, lambda self: self.tw.canvas.textcolor],
        'textsize':[0, lambda self: self.tw.textsize],
        'titlex':[0, lambda self: self.tw.titlex],
        'titley':[0, lambda self: self.tw.titley],
        'topy':[0, lambda self: self.tw.topy],
        'tpos':[0, lambda self: self.tw.canvas.height/(self.tw.coord_scale*2)],
        'turtle':[1, lambda self, x: self.tw.canvas.set_turtle(x)],
        'userdefined':[1, lambda self,x: self.prim_myblock(x)],
        'video':[1, lambda self,x: self.play_movie(x)],
        'vres':[0, lambda self: self.tw.canvas.height/self.tw.coord_scale],
        'wait':[1, self.prim_wait, True],
        'write':[2, lambda self, x,y: self.write(self, x,y)],
        'xcor':[0, lambda self: self.tw.canvas.xcor/self.tw.coord_scale],
        'ycor':[0, lambda self: self.tw.canvas.ycor/self.tw.coord_scale],
        'yellow':[0, lambda self: 20]}

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
    
        self.istack = []
        self.stacks = {}
        self.boxes = {'box1': 0, 'box2': 0}
        self.heap = []

        self.keyboard = 0
        self.trace = 0
        self.gplay = None
        self.ag = None
        self.title_height = int((self.tw.canvas.height/20)*self.tw.scale)
        self.body_height = int((self.tw.canvas.height/40)*self.tw.scale)
        self.bullet_height = int((self.tw.canvas.height/30)*self.tw.scale)
    
        self.scale = 33

    """
    Define the primitives associated with the blocks
    """
    def defprim(self, name, args, fcn, rprim=False):
        sym = self.intern(name)
        sym.nargs, sym.fcn = args, fcn
        sym.rprim = rprim    

    """
    Add any new objects to the symbol list.
    """
    def intern(self, str):
        if str in self.oblist:
            return self.oblist[str]
        sym = symbol(str)
        self.oblist[str] = sym
        return sym
    
    """
    Given a block to run...
    """
    def run_blocks(self, blk, blocks, run_flag):
        for k in self.stacks.keys():
            self.stacks[k] = None
        self.stacks['stack1'] = None
        self.stacks['stack2'] = None

        for b in blocks:
            b.unhighlight()
            if b.name == 'hat1':
                code = self.blocks_to_code(b)
                self.stacks['stack1'] = self.readline(code)
            if b.name=='hat2':
                code = self.blocks_to_code(b)
                self.stacks['stack2'] = self.readline(code)
            if b.name == 'hat':
                if b.connections[1] is not None:
                    code = self.blocks_to_code(b)
                    self.stacks['stack3'+b.connections[1].values[0]] =\
                        self.readline(code)

        code = self.blocks_to_code(blk)
        if run_flag is True:
            print "running code: %s" % (code)
            self.setup_cmd(code)
        else:
            return code

    """
    Convert a stack of blocks to pseudocode.
    Maintains a parallel datastructure for backpointers to blocks.
    """
    def blocks_to_code(self, blk):
        if blk is None:
            return ['%nothing%', '%nothing%']
        code = []
        dock = blk.docks[0]
        if len(dock)>4: # There could be a '(', ')', '[' or ']'.
            code.append(dock[4])
        if blk.primitive is not None: # make a tuple (prim, blk)
            code.append((blk.primitive, self.tw.block_list.list.index(blk)))
        elif len(blk.values)>0:  # Extract the value from content blocks.
            if blk.name=='number':
                try:
                    code.append(float(blk.values[0]))
                except ValueError:
                    code.append(float(ord(blk.values[0][0])))
            elif blk.name=='string' or blk.name=='title':
                if type(blk.values[0]) == float or type(blk.values[0]) == int:
                    if int(blk.values[0]) == blk.values[0]:
                        blk.values[0] = int(blk.values[0])
                    code.append('#s'+str(blk.values[0]))
                else:
                    code.append('#s'+blk.values[0])
            elif blk.name=='journal':
                if blk.values[0] is not None:
                    code.append('#smedia_'+str(blk.values[0]))
                else:
                    code.append('#smedia_None')
            elif blk.name=='description':
                if blk.values[0] is not None:
                    code.append('#sdescr_'+str(blk.values[0]))
                else:
                    code.append('#sdescr_None')
            elif blk.name=='audio':
                if blk.values[0] is not None:
                    code.append('#saudio_'+str(blk.values[0]))
                else:
                    code.append('#saudio_None')
            else:
                print "%s had no primitive." % (blk.name)
                return ['%nothing%']
        else:
            print "%s had no value." % (blk.name)
            return ['%nothing%']
        for i in range(1, len(blk.connections)):
            b = blk.connections[i]        
            dock = blk.docks[i]
            if len(dock)>4: # There could be a '(', ')', '[' or ']'.
                for c in dock[4]:
                    code.append(c)
            if b is not None:
                code.extend(self.blocks_to_code(b))
            elif blk.docks[i][0] not in ['flow', 'unavailable']:
                code.append('%nothing%')
        return code
    
    """
    Execute the psuedocode.
    """
    def setup_cmd(self, str):
        self.tw.active_turtle.hide() # Hide the turtle while we are running.
        self.procstop = False
        list = self.readline(str)
        self.step = self.start_eval(list)

    """
    Convert the pseudocode into a list of commands.
        The block associated with the command is stored as the second element
        in a tuple, e.g., (#forward, 16)
    """
    def readline(self, line):
        res = []
        while line:
            token = line.pop(0)
            btoken = None
            if type(token) == tuple:
                 (token, btoken) = token
            if isNumberType(token):
                res.append(token)
            elif token.isdigit():
                res.append(float(token))
            elif token[0]=='-' and token[1:].isdigit():
                res.append(-float(token[1:]))
            elif token[0] == '"':
                res.append(token[1:])
            elif token[0:2] == "#s":
                res.append(token[2:])
            elif token == '[':
                res.append(self.readline(line))
            elif token == ']':
                return res
            elif btoken is None:
                res.append(self.intern(token))
            else:
                res.append((self.intern(token),btoken))
        return res

    """
    Step through the list.
    """
    def start_eval(self, list):
        self.icall(self.evline, list)
        yield True
        if self.tw.running_sugar:
            self.tw.activity.stop_button.set_icon("stopitoff")
        yield False

    """
    Add a function and its arguments to the program stack.
    """
    def icall(self, fcn, *args):
        self.istack.append(self.step)
        self.step = fcn(*(args))

    """
    Evaluate a line of code from the list.
    """
    def evline(self, list):
        oldiline = self.iline
        self.iline = list[:]
        self.arglist = None
        while self.iline:
            token = self.iline[0]
            btoken = None
            if type(token) == tuple:
                (token, btoken) = self.iline[0]

            if self.tw.hide is False\
               and btoken is not None and type(btoken) is int:
                self.tw.block_list.list[btoken].highlight()

            if self.tw.step_time > 0:
                self.tw.active_turtle.show()
                endtime = millis()+self.an_int(self.tw.step_time)*100
                while millis()<endtime:
                    yield True
                self.tw.active_turtle.hide()

            if token == self.symopar:
                token = self.iline[1]
                if type(token) == tuple:
                    (token, btoken) = self.iline[1]
            self.icall(self.eval)
            yield True

            if self.tw.hide is False\
               and btoken is not None and type(btoken) is int:
                self.tw.block_list.list[btoken].unhighlight()

            if self.procstop:
                break
            if self.iresult == None:
                continue

            if btoken is not None and type(btoken) is int:
                self.tw.block_list.list[btoken].highlight()
            raise logoerror(str(self.iresult))
        self.iline = oldiline
        self.ireturn()
        if self.tw.hide is False:
            self.tw.display_coordinates()
        yield True
    
    """
    Evaluate the next token on the line.
    """
    def eval(self, infixarg=False):
        token = self.iline.pop(0)
        btoken = None
        if type(token) == tuple:
            (token, btoken) = token
        if type(token) == self.symtype:
            if self.tw.hide is False and btoken is not None:
                self.tw.block_list.list[btoken].highlight()
            self.icall(self.evalsym, token)
            yield True
            if self.tw.hide is False and btoken is not None:
                self.tw.block_list.list[btoken].unhighlight()
            res = self.iresult
        else:
            res = token
        if not infixarg:
            while self.infixnext():
                self.icall(self.evalinfix, res)
                yield True
                res = self.iresult
        self.ireturn(res)
        yield True

    """
    Processing flow (vertical)
    """
    def evalsym(self, token):
        btoken = None
        if type(token) == tuple:
            (token, btoken) = token
            print "found a tuple in evalsym (%s, %s)?" % (token, btoken)
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
                self.icall(self.ufuncall, self.cfun.fcn)
                yield True
            else:
                self.icall(self.cfun.fcn, *self.arglist)
                yield True
            result = None
        else:
            # TODO: find out why stopstack args are mismatched
            if token.name == 'stopstack':
                result = self.cfun.fcn()
            else:
                result = self.cfun.fcn(self, *self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        if self.arglist is not None and result == None:
            raise logoerror("%s didn't output to %s (arglist %s, result %s)" % \
                (oldcfun.name, self.cfun.name, str(self.arglist), str(result)))
        self.ireturn(result)
        yield True

    #
    # Processing assignments (horizontal)
    #
    def evalinfix(self, firstarg):
        token = self.iline.pop(0)
        btoken = None
        if type(token) == tuple:
            (token, btoken) = token
        oldcfun, oldarglist = self.cfun, self.arglist
        self.cfun, self.arglist = token, [firstarg]
        no_args_check(self)
        self.icall(self.eval, True)
        yield True
        self.arglist.append(self.iresult)
        result = self.cfun.fcn(self, *self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        self.ireturn(result)
        yield True
    
    def infixnext(self):
        if len(self.iline)==0:
            return False
        if type(self.iline[0]) is not self.symtype:
            return False
        return self.iline[0].name in ['+', '-', '*', '/','%','and','or']

    def ufuncall(self, body):
        ijmp(self.evline, body)
        yield True
    
    def doevalstep(self):
        starttime = millis()
        try:
            while (millis()-starttime)<120:
                try:
                    if self.step is not None:
                        self.step.next()
                    else:
                        print "step is None"
                        return False
                except StopIteration:
                    self.tw.turtles.show_all()
                    return False
        except logoerror, e:
            self.tw.showlabel('syntaxerror', str(e)[1:-1])
            self.tw.turtles.show_all()
            return False
        return True

    def ireturn(self, res=None):
        self.step = self.istack.pop()
        self.iresult = res

    def ijmp(self, fcn, *args):
        self.step = fcn(*(args))

    def debug_trace(self, token):
        if self.trace:
            if token.name in PALETTES[PALETTE_NAMES.index('turtle')]:
                my_string = "%s\n%s=%d\n%s=%d\n%s=%d\n%s=%d" %\
                    (token.name, _('xcor'), int(self.tw.canvas.xcor),
                     _('ycor'), int(self.tw.canvas.ycor), _('heading'),
                     int(self.tw.canvas.heading), _('scale'), int(self.scale))
            elif token.name in PALETTES[PALETTE_NAMES.index('pen')]:
                if self.tw.canvas.pendown:
                    penstatus = _('pen down')
                else:
                    penstatus = _('pen up')
                my_string = "%s\n%s\n%s=%d\n%s=%d\n%s=%.1f" %\
                    (token.name, penstatus, _('color'),
                     int(self.tw.canvas.color), _('shade'),
                     int(self.tw.canvas.shade), _('pen size'),
                     self.tw.canvas.pensize)
            else:
                my_string = "%s\n%s:\n" % (token.name, _('box'))
                for k, v in self.boxes.iteritems():
                    tmp = k +":" + str(v) + "\n"
                    my_string += tmp
            self.tw.showlabel('info',my_string)
        return
    
    def undefined_check(self, token):
        if token.fcn is not None:
            return False
        if token.name == '%nothing%':
            errormsg = ''
        else:
            errormsg = "%s %s" % (_("I don't know how to"), _(token.name))
        raise logoerror(errormsg)
    
    def no_args_check(self):
        if self.iline and self.iline[0] is not self.symnothing:
            return
        raise logoerror("#noinput")
    
    #
    # Primitives
    #

    def prim_clear(self):
        stop_media(self)
        self.tw.canvas.clearscreen()

    def prim_start(self):
        if self.tw.running_sugar:
            self.tw.activity.recenter()

    def prim_wait(self, time):
        self.tw.active_turtle.show()
        endtime = millis()+self.an_int(time*1000)
        while millis()<endtime:
            yield True
        self.tw.active_turtle.hide()
        self.ireturn()
        yield True
    
    def prim_repeat(self, num, list):
        num = self.an_int(num)
        for i in range(num):
            self.icall(self.evline, list[:])
            yield True
            if self.procstop:
                break
        self.ireturn()
        yield True

    def prim_bullet(self, list): # Depreciated block style
        self.show_bullets(list)
        self.ireturn()
        yield True

    def prim_list(self, list):
        self.show_list(list)
        self.ireturn()
        yield True

    def prim_myfunc(self, list):
        new_list = [self.intern('myfunction')]
        new_list.append(list)
        self.icall(self.evline, new_list)
        yield True
        self.ireturn()
        yield True

    def myfunction(self, list):
        y = myfunc(list[0], list[1:])
        if y == None:
            raise logoerror("#syntaxerror")
            stop_logo(self.tw)
        else:
            return y

    def prim_forever(self, list):
        while True:
            self.icall(self.evline, list[:])
            yield True
            if self.procstop:
                break
        self.ireturn()
        yield True

    def prim_if(self, bool, list):
        if bool:
            self.icall(self.evline, list[:])
            yield True
        self.ireturn()
        yield True

    def prim_ifelse(self, bool, list1, list2):
        if bool:
            self.ijmp(self.evline, list1[:])
            yield True
        else:
            self.ijmp(self.evline, list2[:])
            yield True

    def prim_opar(self, val):
        self.iline.pop(0)
        return val

    def prim_define(self, name, body):
        if type(name) is not symtype:
            name = self.intern(name)
        name.nargs, name.fcn = 0, body
        name.rprim = True
    
    def prim_stack(self, str):
        if (not self.stacks.has_key('stack3'+str)) or\
           self.stacks['stack3'+str] is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks['stack3'+str][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def prim_stack1(self):
        if self.stacks['stack1'] is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks['stack1'][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True
    
    def prim_stack2(self):
        if self.stacks['stack2'] is None:
            raise logoerror("#nostack")
        self.icall(self.evline, self.stacks['stack2'][:])
        yield True
        self.procstop = False
        self.ireturn()
        yield True

    def prim_stopstack(self):
        self.procstop = True
    
    def prim_print_heap(self):
        self.tw.showlabel('status', self.heap)

    def an_int(self, n):
        if type(n) == int:
            return n
        elif type(n) == float:
            return int(n)
        elif type(n) == str:
            return int(ord(n[0]))
        else:
            raise logoerror("%s doesn't like %s as input" \
                % (self.cfun.name, str(n)))

    def box(self, x):
        if type(convert(x, float, False)) == float:
            if int(float(x)) == x:
                x = int(x)
        try:
            return self.boxes['box3'+str(x)]
        except:
            raise logoerror("#emptybox")
    
    def prim_myblock(self, x):
        if self.tw.myblock is not None:
            try:
                y = myfunc_import(self, self.tw.myblock, x)
            except:
                raise logoerror("#nocode")
        else:
            raise logoerror("#nocode")
        return
    
    def prim_print(self, n, flag):
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
            self.tw.showlabel('status', round_int(n))
    
    def prim_kbinput(self):
        if len(self.tw.keypress) == 1:
            self.keyboard = ord(self.tw.keypress[0])
        else:
            try:
                self.keyboard = {'Escape': 27, 'space': 32, ' ': 32,
                                 'Return': 13, \
                                 'KP_Up': 2, 'KP_Down': 4, 'KP_Left': 1, \
                                 'KP_Right': 3,}[self.tw.keypress]
            except:
                self.keyboard = 0
        self.tw.keypress = ""

    def prim_setbox(self, name, x, val):
        if x is None:
            self.boxes[name]=val
        else:
            if type(convert(x, float, False)) == type(float):
                if int(float(x)) == x:
                    x = int(x)
            self.boxes[name+str(x)]=val

    def prim_push(self, val):
        self.heap.append(val)

    def prim_pop(self):
        try:
            return self.heap.pop(-1)
        except:
            raise logoerror ("#emptyheap")

    def empty_heap(self):
        self.heap = []

    def save_picture(self, name):
        self.tw.save_as_image(name)

    def show_list(self, sarray):
        x = self.tw.canvas.xcor/self.tw.coord_scale
        y = self.tw.canvas.ycor/self.tw.coord_scale
        for s in sarray:
            self.tw.canvas.setxy(x, y)
            self.show(s)
            y -= int(self.bullet_height*2*self.tw.lead)

    def set_scale(self, x):
        self.scale = x

    # need to fix export logo to map show to write
    def show(self, string, center=False):
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width/2+int(self.tw.canvas.xcor)
        y = self.tw.canvas.height/2-int(self.tw.canvas.ycor)
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
                if center is True:
                    y -= self.tw.textsize
                self.tw.canvas.draw_text(string,x,y,self.tw.textsize,
                          self.tw.canvas.width-x)
        elif type(string) == float or type(string) == int:
            string = round_int(string)
            if center is True:
                y -= self.tw.textsize
            self.tw.canvas.draw_text(string, x, y, self.tw.textsize,
                                     self.tw.canvas.width-x)
    
    def play_sound(self, audio):
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

    def show_picture(self, media, x, y, w, h):
        if media == "" or media[6:] == "":
            pass
        elif media[6:] is not "None":
            pixbuf = None
            if self.tw.running_sugar:
                try:
                    dsobject = datastore.get(media[6:])
                except:
                    self.tw.showlabel('nojournal', media[6:]) 
                    print "Couldn't open Journal object %s" % (media[6:])
                if movie_media_type(dsobject.file_path):
                    play_movie_from_file(self,
                        dsobject.file_path, int(x), int(y), int(w), int(h))
                else:
                    pixbuf = get_pixbuf_from_journal(dsobject, int(w), int(h))
                dsobject.destroy()
            else:
                try:
                    if movie_media_type(media):
                        play_movie_from_file(self, media[6:], int(x), int(y),
                                                              int(w), int(h))
                    else:
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                     media[6:], int(w), int(h))
                except:
                    self.tw.showlabel('nofile', media[6:]) 
                    print "Couldn't open media object %s" % (media[6:])
            if pixbuf is not None:
                self.tw.canvas.draw_pixbuf(pixbuf, 0, 0, int(x), int(y),
                                                         int(w), int(h))

    def show_description(self, media, x, y, w, h):
        if media == "" or media[6:] == "":
            return
        elif media[6:] is not "None":
            text = None
            if self.tw.running_sugar:
                try:
                    dsobject = datastore.get(media[6:])
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
                print "text: %s" % (text)
                self.tw.canvas.draw_text(text, int(x), int(y),
                                         self.body_height, int(w))
    
    def draw_title(self, title, x, y):
        self.tw.canvas.draw_text(title,int(x),int(y),self.title_height,
                                                     self.tw.canvas.width-x)
    # image only (at current x,y)
    def insert_image(self, media, center):
        w = (self.tw.canvas.width * self.scale)/100
        h = (self.tw.canvas.height * self.scale)/100
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width/2+int(self.tw.canvas.xcor)
        y = self.tw.canvas.height/2-int(self.tw.canvas.ycor)
        if center is True:
            x -= w/2
            y -= h/2
        if media[0:5] == 'media':
            self.show_picture(media, x, y, w, h)
    
    # description text only (at current x,y)
    def insert_desc(self, media):
        w = (self.tw.canvas.width * self.scale)/100
        h = (self.tw.canvas.height * self.scale)/100
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width/2+int(self.tw.canvas.xcor)
        y = self.tw.canvas.height/2-int(self.tw.canvas.ycor)
        if media[0:5] == 'descr':
            self.show_description(media, x, y, w, h)

    """
    Depreciated block methods
    """
    # title, one image, and description
    def show_template1x1(self, title, media):
        w,h,xo,yo,dx,dy = self.tw.calc_position('t1x1')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height*2) \
                      / self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        self.tw.canvas.setxy(x, y)
        self.show(media)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y)
            self.show(media.replace("media_","descr_"))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)
    
    # title, two images (horizontal), two descriptions
    def show_template2x1(self, title, media1, media2):
        w,h,xo,yo,dx,dy = self.tw.calc_position('t2x1')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height*2)/\
                  self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        self.tw.canvas.setxy(x, y)
        self.show(media1)
        x = 0
        self.tw.canvas.setxy(x, y)
        self.show(media2)
        y = -self.title_height
        if self.tw.running_sugar:
            self.tw.canvas.setxy(x, y)
            self.show(media2.replace("media_","descr_"))
            x = -(self.tw.canvas.width/2)+xo
            self.tw.canvas.setxy(x, y)
            self.show(media1.replace("media_","descr_"))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    # title and varible number of  bullets
    def show_bullets(self, sarray):
        w,h,xo,yo,dx,dy = self.tw.calc_position('bullet')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(sarray[0])
        # set body text size
        self.tw.canvas.settextsize(self.bullet_height)
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        for s in sarray[1:]:
            self.tw.canvas.setxy(x, y)
            self.show(s)
            y -= int(self.bullet_height*2*self.tw.lead)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)
    
    # title, two images (vertical), two desciptions
    def show_template1x2(self, title, media1, media2):
        w,h,xo,yo,dx,dy = self.tw.calc_position('t1x2')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height*2)/\
                 self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        self.tw.canvas.setxy(x, y)
        self.show(media1)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y)
            self.show(media1.replace("media_","descr_"))
            y = -self.title_height
            self.tw.canvas.setxy(x, y)
            self.show(media2.replace("media_","descr_"))
            x = -(self.tw.canvas.width/2)+xo
            self.tw.canvas.setxy(x, y)
            self.show(media2)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    # title and four images
    def show_template2x2(self, title, media1, media2, media3, media4):
        w,h,xo,yo,dx,dy = self.tw.calc_position('t2x2')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height*2)/\
                  self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        self.tw.canvas.setxy(x, y)
        self.show(media1)
        x = 0
        self.tw.canvas.setxy(x, y)
        self.show(media2)
        y = -self.title_height
        self.tw.canvas.setxy(x, y)
        self.show(media4)
        x = -(self.tw.canvas.width/2)+xo
        self.tw.canvas.setxy(x, y)
        self.show(media3)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    # title, one media object
    def show_template1x1a(self, title, media1):
        w,h,xo,yo,dx,dy = self.tw.calc_position('t1x1a')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # calculate and set scale for media blocks
        myscale = 90 * (self.tw.canvas.height - self.title_height*2) /\
                       self.tw.canvas.height
        self.set_scale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        self.tw.canvas.setxy(x, y)
        self.show(media1)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def write(self, string, fsize):
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width/2+int(self.tw.canvas.xcor)
        y = self.tw.canvas.height/2-int(self.tw.canvas.ycor)
        self.tw.canvas.draw_text(string,x,y-15,int(fsize),self.tw.canvas.width)
