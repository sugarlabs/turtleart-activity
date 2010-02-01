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

import re
from time import *
import gobject
from operator import isNumberType
import random
import audioop
from math import *
import subprocess
from UserDict import UserDict
try:
    from sugar.datastore import datastore
except:
    pass

from constants import *
from tacanvas import *
from tagplay import play_audio, play_movie_from_file, stop_media
from tajail import myfunc, myfunc_import

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

#
# Utility functions
#
def movie_media_type(suffix):
    if suffix.replace('.','') in ['ogv','vob','mp4','wmv','mov', 'mpeg']:
        return True
    return False

def audio_media_type(suffix):
    if suffix.replace('.','') in ['ogg', 'oga', 'm4a']:
        return True
    return False

def careful_divide(x,y):
    try:
        if y==0:
            return 0
        return x/y
    except:
        return 0

def taequal(x,y):
    try:
        return float(x)==float(y)
    except:
        if type(x) == str or type(x) == unicode:
            xx = ord(x[0])
        else:
            xx = x
        if type(y) == str or type(y) == unicode:
            yy = ord(y[0])
        else:
            yy = y
        return xx==yy
    
def taless(x, y):
    try:
        return float(x)<float(y)
    except:
        if type(x) == str or type(x) == unicode:
            xx = ord(x[0])
        else:
            xx = x
        if type(y) == str or type(y) == unicode:
            yy = ord(y[0])
        else:
            yy = y
        return xx<yy
    
def tamore(x, y):
    return taless(y, x)

def taplus(x, y):
    if (type(x) == int or type(x) == float) and \
        (type(y) == int or type(y) == float):
        return(x+y)
    else:
        return(str(x) + str(y))
    
def taminus(x, y):
    try:
        return(x-y)
    except:
        raise logoerror("#syntaxerror")
    
def taproduct(x, y):
    try:
        return(x*y)
    except:
        raise logoerror("#syntaxerror")
    
def tamod(x, y):
    try:
        return(x%y)
    except:
        raise logoerror("#syntaxerror")
    
def tasqrt(x):
    try:
        return sqrt(x)
    except:
        raise logoerror("#syntaxerror")
    
def identity(x):
    return(x)

def display_coordinates(tw, a=-1, b=-1, d=-1):
    if a==-1 and b==-1 and d == -1:
        x = round_int(tw.canvas.xcor/tw.coord_scale)
        y = round_int(tw.canvas.ycor/tw.coord_scale)
        h = round_int(tw.canvas.heading)
    else:
        x = a
        y = b
        h = d
    if tw.running_sugar():
        tw.activity.coordinates_label.set_text("%s: %d %s: %d %s: %d" % (
                                   _("xcor"), x, _("ycor"), y, _("heading"), h))
        tw.activity.coordinates_label.show()
    
def round_int(n):
    if int(float(n)) == n:
        return int(n)
    else:
        nn = int(float(n+0.05)*10)/10.
        if int(float(nn)) == nn:
            return int(nn)
        return nn

def get_pixbuf_from_journal(dsobject, w, h):
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(dsobject.file_path,
                                                      int(w),int(h))
    except:
        try:
            pixbufloader = \
                gtk.gdk.pixbuf_loader_new_with_mime_type('image/png')
            pixbufloader.set_size(min(300,int(w)),min(225,int(h)))
            pixbufloader.write(dsobject.metadata['preview'])
            pixbufloader.close()
            pixbuf = pixbufloader.get_pixbuf()
        except:
            pixbuf = None
    return pixbuf

def calc_position(tw, t):
    w,h,x,y,dx,dy = TEMPLATES[t]
    x *= tw.canvas.width
    y *= tw.canvas.height
    w *= (tw.canvas.width-x)
    h *= (tw.canvas.height-y)
    dx *= w
    dy *= h
    return(w,h,x,y,dx,dy)
    
def stop_logo(tw):
    tw.step_time = 0
    tw.lc.step = just_stop()
    
def just_stop():
    yield False

def millis():
    return int(clock()*1000)

"""
def parseline(str):
    split = re.split(r"\s|([\[\]()])", str)
    return [x for x in split if x and x != ""]
"""
 
#
# A class for parsing Logo Code
#
class LogoCode:
    def __init__(self, tw):

        self.tw = tw
        self.oblist = {}

        # math primitives
        self.defprim('print', 1, lambda self,x: self.status_print(x))
        self.defprim('+', None, lambda self,x,y: x+y)
        self.defprim('plus', 2, lambda self,x,y: taplus(x,y))
        self.defprim('-', None, lambda self,x,y: x-y)
        self.defprim('minus', 2, lambda self,x,y: taminus(x,y))
        self.defprim('*', None, lambda self,x,y: x*y)
        self.defprim('product', 2, lambda self,x,y: taproduct(x,y))
        self.defprim('/', None, lambda self,x,y: careful_divide(x,y))
        self.defprim('division', 2, lambda self,x,y: careful_divide(x,y))
        self.defprim('random', 2, lambda self,x,y: int(random.uniform(x,y)))
        self.defprim('greater?', 2, lambda self,x,y: tamore(x,y))
        self.defprim('less?', 2, lambda self,x,y: taless(x,y))
        self.defprim('equal?', 2, lambda self,x,y: taequal(x,y))
        self.defprim('and', None, lambda self,x,y: x&y)
        self.defprim('or', None, lambda self,x,y: x|y)
        self.defprim('not', 1, lambda self,x:not x)
        self.defprim('%', None, lambda self,x,y: x%y)
        self.defprim('mod', 2, lambda self,x,y: tamod(x,y))
        self.defprim('sqrt', 1, lambda self,x: sqrt(x))
        self.defprim('id',1, lambda self,x: identity(x))
        
        # keyboard, sensor, and misc. primitives
        self.defprim('kbinput', 0, lambda self: self.kbinput())
        self.defprim('keyboard', 0, lambda self: self.keyboard)
        self.defprim('userdefined', 1, lambda self,x: self.loadmyblock(x))
        self.defprim('myfunc', 2, lambda self,f,x: self.callmyfunc(f, x))
        self.defprim('hres', 0,
                lambda self: self.tw.canvas.width/self.tw.coord_scale)
        self.defprim('vres', 0,
                lambda self: self.tw.canvas.height/self.tw.coord_scale)
        self.defprim('leftpos', 0,
                lambda self: -(self.tw.canvas.width/(self.tw.coord_scale*2)))
        self.defprim('toppos', 0,
                lambda self: self.tw.canvas.height/(self.tw.coord_scale*2))
        self.defprim('rightpos', 0,
                lambda self: self.tw.canvas.width/(self.tw.coord_scale*2)) 
        self.defprim('bottompos', 0,
                lambda self: -(self.tw.canvas.height/(self.tw.coord_scale*2)))

        # turtle primitives
        self.defprim('clean', 0, lambda self: self.clear())
        self.defprim('forward', 1, lambda self, x: self.tw.canvas.forward(x))
        self.defprim('back', 1, lambda self,x: self.tw.canvas.forward(-x))
        self.defprim('seth', 1, lambda self, x: self.tw.canvas.seth(x))
        self.defprim('right', 1, lambda self, x: self.tw.canvas.right(x))
        self.defprim('left', 1, lambda self,x: self.tw.canvas.right(-x))
        self.defprim('heading', 0, lambda self: self.tw.canvas.heading)
        self.defprim('setxy', 2, lambda self, x, y: self.tw.canvas.setxy(x, y))
        self.defprim('show',1,lambda self, x: self.show(x, True))
        self.defprim('setscale', 1, lambda self,x: self.set_scale(x))
        self.defprim('scale', 0, lambda self: self.scale)
        self.defprim('write', 2, lambda self, x,y: self.write(self, x,y))
        self.defprim('insertimage', 1,
                lambda self,x: self.insert_image(x, False))
        self.defprim('arc', 2, lambda self, x, y: self.tw.canvas.arc(x, y))
        self.defprim('xcor', 0,
                lambda self: self.tw.canvas.xcor/self.tw.coord_scale)
        self.defprim('ycor', 0,
                lambda self: self.tw.canvas.ycor/self.tw.coord_scale)
        self.defprim('turtle', 1,
                lambda self, x: self.tw.canvas.set_turtle(int(x-1)))
    
        # pen primitives
        self.defprim('pendown', 0, lambda self: self.tw.canvas.setpen(True))
        self.defprim('penup', 0, lambda self: self.tw.canvas.setpen(False))
        self.defprim('(', 1, lambda self, x: self.prim_opar(x))
        self.defprim('setcolor', 1, lambda self, x: self.tw.canvas.setcolor(x))
        self.defprim('settextcolor', 1,
                lambda self, x: self.tw.canvas.settextcolor(x))
        self.defprim('settextsize', 1,
                lambda self, x: self.tw.canvas.settextsize(x))
        self.defprim('setshade', 1, lambda self, x: self.tw.canvas.setshade(x))
        self.defprim('setpensize', 1,
                lambda self, x: self.tw.canvas.setpensize(x))
        self.defprim('fillscreen', 2,
                lambda self, x, y: self.tw.canvas.fillscreen(x, y))
        self.defprim('color', 0, lambda self: self.tw.canvas.color)
        self.defprim('shade', 0, lambda self: self.tw.canvas.shade)
        self.defprim('pensize', 0, lambda self: self.tw.canvas.pensize)
        self.defprim('textcolor', 0, lambda self: self.tw.canvas.textcolor)
        self.defprim('textsize', 0, lambda self: self.tw.textsize)
        self.defprim('red', 0, lambda self: 0)
        self.defprim('orange', 0, lambda self: 10)
        self.defprim('yellow', 0, lambda self: 20)
        self.defprim('green', 0, lambda self: 30)
        self.defprim('cyan', 0, lambda self: 50)
        self.defprim('blue', 0, lambda self: 70)
        self.defprim('purple', 0, lambda self: 90)

        # flow primitives
        self.defprim('wait', 1, self.prim_wait, True)
        self.defprim('repeat', 2, self.prim_repeat, True)
        self.defprim('forever', 1, self.prim_forever, True)
        self.defprim('if', 2, self.prim_if, True)
        self.defprim('ifelse', 3, self.prim_ifelse, True)
        self.defprim('stopstack', 0, self.prim_stopstack)

        # blocks primitives
        self.defprim('stack1', 0, self.prim_stack1, True)
        self.defprim('stack2', 0, self.prim_stack2, True)
        self.defprim('stack', 1, self.prim_stack, True)
        self.defprim('box1', 0, lambda self: self.boxes['box1'])
        self.defprim('box2', 0, lambda self: self.boxes['box2'])
        self.defprim('box', 1, lambda self,x: self.box(x))
        self.defprim('storeinbox1', 1, lambda self,x: self.setbox('box1',x))
        self.defprim('storeinbox2', 1, lambda self,x: self.setbox('box2',x))
        self.defprim('storeinbox', 2,
                lambda self,x,y: self.setbox('box3'+str(x),y))
        self.defprim('push', 1, lambda self,x: self.push_heap(x))
        self.defprim('pop', 0, lambda self: self.pop_heap())
        self.defprim('heap', 0, lambda self: self.heap_print())
        self.defprim('emptyheap', 0, lambda self: self.empty_heap())
        self.defprim('start', 0, lambda self: self.start_stack())
        self.defprim('define', 2, self.prim_define)
        self.defprim('nop', 0, lambda self: None)
        self.defprim('nop1', 0, lambda self: None)
        self.defprim('nop2', 0, lambda self: None)
        self.defprim('nop3', 1, lambda self,x: None)
    
        # templates primitives
        self.defprim('container', 1, lambda self,x: x)
        self.defprim('t1x1', 2, lambda self,x,y: self.show_template1x1(x, y))
        self.defprim('t1x1a', 2, lambda self,x,y: self.show_template1x1a(x, y))
        self.defprim('t2x1', 3,
                lambda self,x,y,z: self.show_template2x1(x, y, z))
        self.defprim('bullet', 2, self.prim_bullet, True)
        self.defprim('sound', 1, lambda self,x: self.play_sound(x))
        self.defprim('video', 1, lambda self,x: self.play_movie(x))
        self.defprim('t1x2', 3,
                lambda self,x,y,z: self.show_template1x2(x, y, z))
        self.defprim('t2x2', 5,
                lambda self,x,y,z,a,b: self.show_template2x2(x, y, z, a, b))
        self.defprim('hideblocks', 0, lambda self: self.hideblocks())
    
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
        self.nobox = ""
        self.title_height = int((self.tw.canvas.height/20)*self.tw.scale)
        self.body_height = int((self.tw.canvas.height/40)*self.tw.scale)
        self.bullet_height = int((self.tw.canvas.height/30)*self.tw.scale)
    
        self.scale = 33

    def run_blocks(self, blk, blocks, run_flag):
        for x in self.stacks.keys():
            self.stacks[x] = None
        self.stacks['stack1'] = None
        self.stacks['stack2'] = None
        for b in blocks:
            if b.name == 'hat1':
                self.stacks['stack1'] = self.readline(self.blocks_to_code(b))
            if b.name=='hat2':
                self.stacks['stack2'] = self.readline(self.blocks_to_code(b))
            if b.name == 'hat':
                if (b.connections[1] is not None):
                    text = b.connections[1].values[0]
                    self.stacks['stack3'+text] =\
                        self.readline(self.blocks_to_code(b))
        code = self.blocks_to_code(blk)
        if run_flag is True:
            print "code: %s" % (code)
            self.setup_cmd(code)
        else: return code

    def blocks_to_code(self, blk):
        if blk is None:
            return ['%nothing%']
        code = []
        dock = blk.docks[0]
        if len(dock)>4:
            code.append(dock[4])
        if blk.primitive is not None:
            code.append(blk.primitive)
        else:
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
                return ['%nothing%']
        for i in range(1,len(blk.connections)):
            b = blk.connections[i]        
            dock = blk.docks[i]
            if len(dock)>4:
                for c in dock[4]:
                    code.append(c)
            if b is not None:
                code.extend(self.blocks_to_code(b))
            elif blk.docks[i][0] not in ['flow', 'unavailable']:
                code.append('%nothing%')
        return code
    
    def intern(self, str):
        if str in self.oblist: return self.oblist[str]
        sym = symbol(str)
        self.oblist[str] = sym
        return sym
    
    def readline(self, line):
        res = []
        while line:
            token = line.pop(0)
            if isNumberType(token): res.append(token)
            elif token.isdigit(): res.append(float(token))
            elif token[0]=='-' and token[1:].isdigit():
                res.append(-float(token[1:]))
            elif token[0] == '"': res.append(token[1:])
            elif token[0:2] == "#s": res.append(token[2:])
            elif token == '[': res.append(self.readline(line))
            elif token == ']': return res
            else: res.append(self.intern(token))
        return res

    def setup_cmd(self, str):
        self.tw.active_turtle.hide()
        self.procstop=False
        list = self.readline(str)
        self.step = self.start_eval(list)

    def start_eval(self, list):
        self.icall(self.evline, list)
        yield True
        if self.tw.running_sugar():
            self.tw.activity.stop_button.set_icon("stopitoff")
        yield False

    def evline(self, list):
        oldiline = self.iline
        self.iline = list[:]
        self.arglist = None
        while self.iline:
            if self.tw.step_time > 0:
                self.tw.active_turtle.show()
                endtime = millis()+self.an_int(self.tw.step_time)*100
                while millis()<endtime:
                    yield True
                self.tw.active_turtle.hide()
            token = self.iline[0]
            if token == self.symopar:
                token = self.iline[1]
            self.icall(self.eval)
            yield True
            if self.procstop:
                break
            if self.iresult == None:
                continue
            raise logoerror(str(self.iresult))
        self.iline = oldiline
        self.ireturn()
        display_coordinates(self.tw)
        yield True
    
    def eval(self, infixarg=False):
        token = self.iline.pop(0)
        if type(token) == self.symtype:
            self.icall(self.evalsym, token); yield True
            res = self.iresult
        else: res = token
        if not infixarg:
            while self.infixnext():
                self.icall(self.evalinfix, res); yield True
                res = self.iresult
        self.ireturn(res)
        yield True

    def evalsym(self, token):
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
                print "%s: %d" % (token.name, len(self.arglist))
                result = self.cfun.fcn()
            else:
                result = self.cfun.fcn(self, *self.arglist)
        self.cfun, self.arglist = oldcfun, oldarglist
        if self.arglist is not None and result == None:
            raise logoerror("%s didn't output to %s (arglist %s, result %s)" % \
                (oldcfun.name, self.cfun.name, str(self.arglist), str(result)))
        self.ireturn(result)
        yield True

    def evalinfix(self, firstarg):
        token = self.iline.pop(0)
        oldcfun, oldarglist = self.cfun, self.arglist
        self.cfun, self.arglist = token, [firstarg]
        no_args_check(self)
        self.icall(self.eval, True); yield True
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

    def debug_trace(self, token):
        if self.trace:
            if token.name in PALETTES[PALETTE_NAMES.index('turtle')]:
                my_string = "%s\nxcor=%d\nycor=%d\nheading=%d\nscale=%d" %\
                    (token.name,int(self.tw.canvas.xcor),
                     int(self.tw.canvas.ycor),int(self.tw.canvas.heading),
                     int(self.scale))
            elif token.name in PALETTES[PALETTE_NAMES.index('pen')]:
                if self.tw.canvas.pendown:
                    penstatus = "pen down"
                else:
                    penstatus = "pen up"
                my_string = "%s\n%s\ncolor=%d\nshade=%d\npensize=%.1f" %\
                    (token.name, penstatus, int(self.tw.canvas.color),
                     int(self.tw.canvas.shade), self.tw.canvas.pensize)
            else:
                my_string = "%s\nblocks status:\n" % (token.name)
                for k,v in self.boxes.iteritems():
                    tmp = k +":" + str(v) + "\n"
                    my_string += tmp
            shp = 'info'
            self.tw.status_spr.set_shape(self.tw.status_shapes[shp])
            self.tw.status_spr.set_label(_(my_string))
            self.tw.status_spr.set_layer(STATUS_LAYER)
        return
    
    def undefined_check(self, token):
        if token.fcn is not None:
            return False
        raise logoerror("%s %s" % (_("I don't know how to"), token.name))
    
    def no_args_check(self):
        if self.iline and self.iline[0] is not self.symnothing : return
        raise logoerror("#noinput")
    
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

    def prim_bullet(self, title, list):
        self.show_bullets(title, list)
        self.ireturn()
        yield True

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
    
    def ufuncall(self, body):
        ijmp(self.evline, body)
        yield True
    
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

    def defprim(self, name, args, fcn, rprim=False):
        sym = self.intern(name)
        sym.nargs, sym.fcn = args,fcn
        sym.rprim = rprim    

    def start_stack(self):
        if self.tw.running_sugar():
            self.tw.activity.recenter()

    def box(self, x):
        try:
            return self.boxes['box3'+str(x)]
        except:
            self.nobox = str(x)
            raise logoerror("#emptybox")
    
    def loadmyblock(self, x):
        # Execute code imported from the Journal
        if self.tw.myblock is not None:
            y = myfunc_import(self, self.tw.myblock, x)
        else:
            raise logoerror("#nocode")
        return
    
    def callmyfunc(self, f, x):
        y = myfunc(self, f, x)
        if y == None:
            raise logoerror("#syntaxerror")
            stop_logo(self.tw)
        else:
            return y
    
    def show_picture(self, media, x, y, w, h):
        if media == "" or media[6:] == "":
            pass
        elif media[6:] is not "None":
            pixbuf = None
            if self.tw.running_sugar():
                try:
                    dsobject = datastore.get(media[6:])
                except:
                    raise logoerror("#nomedia")
                if movie_media_type(dsobject.file_path[-4:]):
                    play_movie_from_file(self,
                        dsobject.file_path, int(x), int(y), int(w), int(h))
                else:
                    pixbuf = get_pixbuf_from_journal(dsobject, int(w), int(h))
                dsobject.destroy()
            else:
                if movie_media_type(media[-4:]):
                    play_movie_from_file(self, media[6:], int(x), int(y),
                                                          int(w), int(h))
                else:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                 media[6:], int(w), int(h))
            if pixbuf is not None:
                self.tw.canvas.draw_pixbuf(pixbuf, 0, 0, int(x), int(y),
                                                         int(w), int(h))

    def show_description(self, media, x, y, w, h):
        if media == "" or media[6:] == "":
            pass
        elif media[6:] is not "None":
            text = None
            if self.tw.running_sugar():
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

    # title, one image, and description
    def show_template1x1(self, title, media):
        w,h,xo,yo,dx,dy = calc_position(self.tw, 't1x1')
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
        if self.tw.running_sugar():
            x = 0
            self.tw.canvas.setxy(x, y)
            self.show(media.replace("media_","descr_"))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)
    
    # title, two images (horizontal), two descriptions
    def show_template2x1(self, title, media1, media2):
        w,h,xo,yo,dx,dy = calc_position(self.tw, 't2x1')
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
        if self.tw.running_sugar():
            self.tw.canvas.setxy(x, y)
            self.show(media2.replace("media_","descr_"))
            x = -(self.tw.canvas.width/2)+xo
            self.tw.canvas.setxy(x, y)
            self.show(media1.replace("media_","descr_"))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    # title and varible number of  bullets
    def show_bullets(self, title, sarray):
        w,h,xo,yo,dx,dy = calc_position(self.tw, 'bullet')
        x = -(self.tw.canvas.width/2)+xo
        y = self.tw.canvas.height/2
        self.tw.canvas.setxy(x, y)
        # save the text size so we can restore it later
        save_text_size = self.tw.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self.show(title)
        # set body text size
        self.tw.canvas.settextsize(self.bullet_height)
        # leave some space below the title
        y -= int(self.title_height*2*self.tw.lead)
        for s in sarray:
            self.tw.canvas.setxy(x, y)
            self.show(s)
            y -= int(self.bullet_height*2*self.tw.lead)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)
    
    # title, two images (vertical), two desciptions
    def show_template1x2(self, title, media1, media2):
        w,h,xo,yo,dx,dy = calc_position(self.tw, 't1x2')
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
        if self.tw.running_sugar():
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
        w,h,xo,yo,dx,dy = calc_position(self.tw, 't2x2')
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
        w,h,xo,yo,dx,dy = calc_position(self.tw, 't1x1a')
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
        if self.tw.running_sugar():
            if audio[6:] != "None":
                try:
                    dsobject = datastore.get(audio[6:])
                    play_audio(self, dsobject.file_path)
                except:
                    print "Couldn't open id: " + str(audio[6:])
        else:
            play_audio(self, audio[6:])

    def clear(self):
        stop_media(self)
        self.tw.canvas.clearscreen()

    def write(self, string, fsize):
        # convert from Turtle coordinates to screen coordinates
        x = self.tw.canvas.width/2+int(self.tw.canvas.xcor)
        y = self.tw.canvas.height/2-int(self.tw.canvas.ycor)
        self.tw.canvas.draw_text(string,x,y-15,int(fsize),self.tw.canvas.width)

    def hideblocks(self):
        self.tw.hide = False # force hide
        self.tw.hideshow_button()
        # TODO: how do we do this with the new toolbar?
        #for i in self.tw.selbuttons:
        #    hide(i)
        if self.tw.running_sugar():
            self.tw.activity.do_hide()
    
    def doevalstep(self):
        starttime = millis()
        try:
            while (millis()-starttime)<120:
                try:
                    if self.step is not None:
                        self.step.next()
                    else: # TODO: where is doevalstep getting called with None?
                        print "step is None"
                        return False
                except StopIteration:
                    self.tw.active_turtle.show()
                    return False
        except logoerror, e:
            showlabel(self, str(e)[1:-1])
            self.tw.active_turtle.show()
            return False
        return True

    def icall(self, fcn, *args):
        self.istack.append(self.step)
        self.step = fcn(*(args))

    def ireturn(self, res=None):
        self.step = self.istack.pop()
        self.iresult = res

    def ijmp(self, fcn, *args):
        self.step = fcn(*(args))
    
    def heap_print(self):
        self.showlabel(self.heap)

    def status_print(self, n):
        if type(n) == str or type(n) == unicode:
            # show title for Journal entries
            if n[0:6] == 'media_':
                try:
                    dsobject = datastore.get(n[6:])
                    self.showlabel(dsobject.metadata['title'])
                    dsobject.destroy()
                except:
                    self.showlabel(n)
            else:
                self.showlabel(n)
        elif type(n) == int:
            self.showlabel(n)
        else:
            self.showlabel(round_int(n))
    
    def kbinput(self):
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
    
    def showlabel(self, label):
        if label=='#nostack':
            shp = 'nostack'
            label=''
        elif label=='#noinput':
            shp = 'noinput'
            label=''
        elif label=='#emptyheap':
            shp = 'emptyheap'
            label=''
        elif label=='#emptybox':
            shp = 'emptybox'
            label='                    '+self.nobox
        elif label=='#nomedia':
            shp = 'nomedia'
            label=''
        elif label=='#nocode':
            shp = 'nocode'
            label=''
        elif label=='#syntaxerror':
            shp = 'syntaxerror'
            label=''
        elif label=='#overflowerror':
            shp = 'overflowerror'
            label=''
        elif label=='#notanumber':
            shp = 'overflowerror'
            label=''
        else:
            shp = 'status'
        self.tw.status_spr.set_shape(self.tw.status_shapes[shp])
        self.tw.status_spr.set_label(label)
        self.tw.status_spr.set_layer(STATUS_LAYER)

    def setbox(self, name,val):
        self.boxes[name]=val
    
    def push_heap(self, val):
        self.heap.append(val)

    def pop_heap(self):
        try:
            return self.heap.pop(-1)
        except:
            raise logoerror ("#emptyheap")

    def empty_heap(self):
        self.heap = []
