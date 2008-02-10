#Copyright (c) 2007-8, Playful Invention Company.

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
from time import clock
from operator import isNumberType
import random
class taLogo: pass

from taturtle import *

procstop = False

class symbol:

    def __init__(self, name):
        self.name = name
        self.nargs = None
        self.fcn = None

    def __str__(self): return self.name
    def __repr__(self): return '#'+self.name

class logoerror(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def run_blocks(lc, spr, blocks):
    lc.stacks['stack1'] = None
    lc.stacks['stack2'] = None
    for i in blocks:
        if i.proto.name=='hat1': lc.stacks['stack1']= readline(lc,blocks_to_code(i))
        if i.proto.name=='hat2': lc.stacks['stack2']= readline(lc,blocks_to_code(i))
    code = blocks_to_code(spr)
    print code
    setup_cmd(lc, code)

def blocks_to_code(spr):
    if spr==None: return ['%nothing%']
    code = []
    dock = spr.proto.docks[0]
    if len(dock)>4: code.append(dock[4])
    if spr.proto.primname != '': code.append(spr.proto.primname)
    else: code.append(float(spr.label))
    for i in range(1,len(spr.connections)):
        b = spr.connections[i]
        dock = spr.proto.docks[i]
        if len(dock)>4:
            for c in dock[4]: code.append(c)
        if b!=None: code.extend(blocks_to_code(b))
        elif spr.proto.docks[i][0] not in ['flow','numend','unavailable','logi-']:
            code.append('%nothing%')
    return code

def intern(lc, str):
    if str in lc.oblist: return lc.oblist[str]
    sym = symbol(str)
    lc.oblist[str] = sym
    return sym


def parseline(str):
    split = re.split(r"\s|([\[\]()])", str)
    return [x for x in split if x and x != ""]

def readline(lc, line):
    res = []
    while line:
        token = line.pop(0)
        if isNumberType(token): res.append(token)
        elif token.isdigit(): res.append(float(token))
        elif token[0]=='-' and token[1:].isdigit(): res.append(-float(token[1:]))
        elif token[0] == '"': res.append(token[1:])
        elif token == '[': res.append(readline(lc,line))
        elif token == ']': return res
        else: res.append(intern(lc, token))
    return res


def setup_cmd(lc, str):
    stopsignon(lc); lc.procstop=False
    list = readline(lc, str)
    lc.step = start_eval(lc, list)

def start_eval(lc, list):
    icall(lc, evline, list); yield True
    yield False

def evline(lc, list):
    oldiline = lc.iline
    lc.iline = list[:]
    lc.arglist = None
    while lc.iline:
        token = lc.iline[0]
        if token==lc.symopar: token=lc.iline[1]
        icall(lc, eval); yield True
        if lc.procstop: break
        if lc.iresult==None: continue
        raise logoerror(str(lc.iresult))
    lc.iline = oldiline
    ireturn(lc); yield True

def eval(lc, infixarg=False):
    token = lc.iline.pop(0)
    if type(token) == lc.symtype:
        icall(lc, evalsym, token); yield True
        res = lc.iresult
    else: res = token
    if not infixarg:
        while infixnext(lc):
            icall(lc, evalinfix, res); yield True
            res = lc.iresult
    ireturn(lc, res); yield True

def evalsym(lc, token):
    undefined_check(lc, token)
    oldcfun, oldarglist = lc.cfun, lc.arglist
    lc.cfun, lc.arglist = token, []
    if token.nargs==None: raise logoerror("#noinput")
    for i in range(token.nargs):
        no_args_check(lc)
        icall(lc, eval); yield True
        lc.arglist.append(lc.iresult)
    if lc.cfun.rprim:
        if type(lc.cfun.fcn)==lc.listtype: icall(lc, ufuncall, cfun.fcn); yield True
        else: icall(lc, lc.cfun.fcn, *lc.arglist); yield True
        result = None
    else: result = lc.cfun.fcn(lc, *lc.arglist)
    lc.cfun, lc.arglist = oldcfun, oldarglist
    if lc.arglist!=None and result==None:
        raise logoerror("%s didn't output to %s" % (oldcfun.name, lc.cfun.name))
    ireturn(lc, result); yield True

def evalinfix(lc, firstarg):
    token = lc.iline.pop(0)
    oldcfun, oldarglist = lc.cfun, lc.arglist
    lc.cfun, lc.arglist = token, [firstarg]
    no_args_check(lc)
    icall(lc, eval,True); yield True
    lc.arglist.append(lc.iresult)
    result = lc.cfun.fcn(lc,*lc.arglist)
    lc.cfun, lc.arglist = oldcfun, oldarglist
    ireturn (lc,result); yield True

def infixnext(lc):
    if len(lc.iline)==0: return False
    if type(lc.iline[0])!=lc.symtype: return False
    return lc.iline[0].name in ['+', '-', '*', '/','%','and','or']

def undefined_check(lc, token):
    if token.fcn != None: return False
    raise logoerror("I don't know how to %s" % token.name)


def no_args_check(lc):
    if lc.iline and lc.iline[0]!=lc.symnothing : return
    raise logoerror("#noinput")

def prim_wait(lc,time):
    setlayer(lc.tw.turtle.spr,630)
    endtime = millis()+an_int(lc,time)*100
    while millis()<endtime:
        yield True
    setlayer(lc.tw.turtle.spr,100)
    ireturn(lc); yield True

def prim_repeat(lc, num, list):
    num = an_int(lc, num)
    for i in range(num):
        icall(lc, evline, list[:]); yield True
        if lc.procstop: break
    ireturn(lc); yield True

def prim_forever(lc, list):
    while True:
        icall(lc,evline, list[:]); yield True
        if lc.procstop: break
    ireturn(lc); yield True

def prim_if(lc, bool, list):
    if bool: icall(lc, evline, list[:]); yield True
    ireturn(lc); yield True

def prim_ifelse(lc, bool, list1,list2):
    if bool: ijmp(lc, evline, list1[:]); yield True
    else: ijmp(lc, evline, list2[:]); yield True

def prim_opar(lc,val):
    lc.iline.pop(0)
    return val

def prim_define(name, body):
    if type(name) != symtype: name = intern(name)
    name.nargs, name.fcn = 0, body
    name.rprim = True

def prim_stack1(lc):
    if lc.stacks['stack1']==None: raise logoerror("#nostack")
    icall(lc, evline, lc.stacks['stack1'][:]); yield True
    lc.procstop = False
    ireturn(lc); yield True

def prim_stack2(lc):
    if lc.stacks['stack2']==None: raise logoerror("#nostack")
    icall(lc, evline, lc.stacks['stack2'][:]); yield True
    lc.procstop = False
    ireturn(lc); yield True

def prim_stopstack(lc):
    lc.procstop = True

def ufuncall(body):
    ijmp(evline, body); yield True

def an_int(lc, n):
    try: return int(n)
    except: raise logoerror("%s doesn't like %s as input" % (lc.cfun.name, str(n)))

def a_float(n):
    try: return int(n)
    except: raise logoerror("%s doesn't like %s as input" % (cfun.name, str(n)))

def defprim(lc, name, args, fcn, rprim=False):
    sym = intern(lc, name)
    sym.nargs, sym.fcn = args,fcn
    sym.rprim = rprim

def lcNew(tw):
    lc = taLogo()
    lc.tw = tw
    lc.oblist = {}

    defprim(lc,'print', 1, lambda lc,x: status_print(lc,x))
#    defprim(lc,'print', 1, lambda lc,x: tyo(int(float(x)*10)/10.))

    defprim(lc,'+', None, lambda lc,x,y:x+y)
    defprim(lc,'-', None, lambda lc,x,y:x-y)
    defprim(lc,'*', None, lambda lc,x,y:x*y)
    defprim(lc,'/', None, lambda lc,x,y:x/y)
    defprim(lc,'random', 2, lambda lc,x,y: int(random.uniform(x,y)))
    defprim(lc,'greater?', 2, lambda lc,x,y: float(x)>float(y))
    defprim(lc,'less?', 2, lambda lc,x,y: float(x)<float(y))
    defprim(lc,'equal?', 2, lambda lc,x,y: float(x)==float(y))
    defprim(lc,'and', None, lambda lc,x,y:x&y)
    defprim(lc,'or', None, lambda lc,x,y:x|y)
    defprim(lc,'not', 1, lambda lc,x:not x)
    defprim(lc,'%', None, lambda lc,x,y:x%y)

    defprim(lc,'clean', 0, lambda lc: clearscreen(lc.tw.turtle))
    defprim(lc,'forward', 1, lambda lc, x: forward(lc.tw.turtle, x))
    defprim(lc,'back', 1, lambda lc,x: forward(lc.tw.turtle,-x))
    defprim(lc,'seth', 1, lambda lc, x: seth(lc.tw.turtle, x))
    defprim(lc,'right', 1, lambda lc, x: right(lc.tw.turtle, x))
    defprim(lc,'left', 1, lambda lc,x: right(lc.tw.turtle,-x))
    defprim(lc,'heading', 0, lambda lc: lc.tw.turtle.heading)
    defprim(lc,'setxy', 2, lambda lc, x, y: setxy(lc.tw.turtle, x, y))
    defprim(lc,'arc', 2, lambda lc, x, y: arc(lc.tw.turtle, x, y))
    defprim(lc,'xcor', 0, lambda lc: lc.tw.turtle.xcor)
    defprim(lc,'ycor', 0, lambda lc: lc.tw.turtle.ycor)

    defprim(lc,'pendown', 0, lambda lc: setpen(lc.tw.turtle, True))
    defprim(lc,'penup', 0, lambda lc: setpen(lc.tw.turtle, False))
    defprim(lc,'(', 1, lambda lc, x: prim_opar(lc,x))
    defprim(lc,'setcolor', 1, lambda lc, x: setcolor(lc.tw.turtle, x))
    defprim(lc,'setshade', 1, lambda lc, x: setshade(lc.tw.turtle, x))
    defprim(lc,'setpensize', 1, lambda lc, x: setpensize(lc.tw.turtle, x))
    defprim(lc,'fillscreen', 2, lambda lc, x, y: fillscreen(lc.tw.turtle, x, y))
    defprim(lc,'color', 0, lambda lc: lc.tw.turtle.color)
    defprim(lc,'shade', 0, lambda lc: lc.tw.turtle.shade)
    defprim(lc,'pensize', 0, lambda lc: lc.tw.turtle.pensize)

    defprim(lc,'wait', 1, prim_wait, True)
    defprim(lc,'repeat', 2, prim_repeat, True)
    defprim(lc,'forever', 1, prim_forever, True)
    defprim(lc,'if', 2, prim_if, True)
    defprim(lc,'ifelse', 3, prim_ifelse, True)
    defprim(lc,'stopstack', 0, prim_stopstack)

    defprim(lc,'stack1', 0, prim_stack1, True)
    defprim(lc,'stack2', 0, prim_stack2, True)
    defprim(lc,'box1', 0, lambda lc: lc.boxes['box1'])
    defprim(lc,'box2', 0, lambda lc: lc.boxes['box2'])
    defprim(lc,'storeinbox1', 1, lambda lc,x: setbox(lc, 'box1',x))
    defprim(lc,'storeinbox2', 1, lambda lc,x: setbox(lc, 'box2',x))

    defprim(lc,'define', 2, prim_define)
    defprim(lc,'nop', 0, lambda lc: None)
    defprim(lc,'start', 0, lambda: None)

    lc.symtype = type(intern(lc, 'print'))
    lc.numtytpe = type(0.)
    lc.listtype = type([])
    lc.symnothing = intern(lc, '%nothing%')
    lc.symopar = intern(lc, '(')

    lc.istack = []
    lc.stacks = {}
    lc.boxes = {'box1': 0, 'box2': 0}

    lc.iline, lc.cfun, lc.arglist, lc.ufun = None, None, None,None

    lc.stopsign = tw.toolsprs['stopit']

    return lc

def doevalstep(lc):
    starttime = millis()
    try:
        while (millis()-starttime)<120:
            if not lc.step.next(): stopsignoff(lc); return False
    except logoerror, e: showlabel(lc, str(e)[1:-1]); stopsignoff(lc); return False
    return True

def icall(lc, fcn, *args):
    lc.istack.append(lc.step)
    lc.step = fcn(lc, *(args))

def ireturn(lc, res=None):
    lc.step = lc.istack.pop()
    lc.iresult = res

def ijmp(lc, fcn, *args):
    lc.step = fcn(lc,*(args))

def status_print(lc,n):
    showlabel(lc,int(float(n)*10)/10.)

def showlabel(lc,l):
    if l=='#nostack': shp = 'nostack'; l=''
    elif l=='#noinput': shp = 'noinput'; l=''
    else:shp = 'status'
    setshape(lc.tw.status_spr, lc.tw.status_shapes[shp])
    setlabel(lc.tw.status_spr,l)
    setlayer(lc.tw.status_spr,710);

def stopsignon(lc):
    setshape(lc.stopsign, lc.stopsign.onshape)
    setlayer(lc.tw.turtle.spr,100)

def stopsignoff(lc):
    setshape(lc.stopsign, lc.stopsign.offshape)
    setlayer(lc.tw.turtle.spr,630)

def stop_logo(tw): tw.lc.step = just_stop()
def just_stop(): yield False

def setbox(lc, name,val): lc.boxes[name]=val
def tyo(n): print n
def millis(): return int(clock()*1000)

