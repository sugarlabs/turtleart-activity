#Copyright (c) 2007-9, Playful Invention Company.

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
import gobject
from operator import isNumberType
import random
import audioop
from math import sqrt
from numpy.oldnumeric import *
from numpy.fft import *
from audiograb import AudioGrab
import subprocess
from UserDict import UserDict
from sugar.datastore import datastore

class noKeyError(UserDict):
    __missing__=lambda x,y: 0

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

def run_blocks(lc, spr, blocks, run_flag):
    # user-defined stacks
    for x in lc.stacks.keys():
        lc.stacks[x]= None
    # two built-in stacks
    lc.stacks['stack1'] = None
    lc.stacks['stack2'] = None
    for i in blocks:
        if i.proto.name=='hat1':
            lc.stacks['stack1']= readline(lc,blocks_to_code(lc,i))
        if i.proto.name=='hat2':
            lc.stacks['stack2']= readline(lc,blocks_to_code(lc,i))
        if i.proto.name=='hat':
            if (i.connections[1]!=None):
                text=i.connections[1].label
                lc.stacks['stack3'+text]= readline(lc,blocks_to_code(lc,i))
    code = blocks_to_code(lc,spr)
    if run_flag == True:
        print code
        setup_cmd(lc, code)
    else: return code

def blocks_to_code(lc,spr):
    if spr==None: return ['%nothing%']
    code = []
    dock = spr.proto.docks[0]
    if len(dock)>4: code.append(dock[4])
    if spr.proto.primname != '': code.append(spr.proto.primname)
    else:
        if spr.proto.name=='number':
            try:
                code.append(float(spr.label))
            except:
                code.append(float(ord(spr.label[0])))
        elif spr.proto.name=='string' or spr.proto.name=='title':
            if type(spr.label) == float or type(spr.label) == int:
                code.append('#s'+str(spr.label))
            else:
                code.append('#s'+spr.label)
        elif spr.proto.name=='journal':
            if spr.ds_id != None:
                code.append('#smedia_'+str(spr.ds_id))
            else:
                code.append('#smedia_None')
        else:
            return ['%nothing%']
    for i in range(1,len(spr.connections)):
        b = spr.connections[i]
        dock = spr.proto.docks[i]
        if len(dock)>4:
            for c in dock[4]: code.append(c)
        if b!=None: code.extend(blocks_to_code(lc,b))
        elif spr.proto.docks[i][0] not in \
            ['flow', 'numend', 'stringend', 'unavailable', 'logi-']:
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
        elif token[0]=='-' and token[1:].isdigit():
            res.append(-float(token[1:]))
        elif token[0] == '"': res.append(token[1:])
        elif token[0:2] == "#s": res.append(token[2:])
        elif token == '[': res.append(readline(lc,line))
        elif token == ']': return res
        else: res.append(intern(lc, token))
    return res

def setup_cmd(lc, str):
    setlayer(lc.tw.turtle.spr,100) 
    lc.procstop=False
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
        if lc.tw.step_time > 0:
            setlayer(lc.tw.turtle.spr,630)
            endtime = millis()+an_int(lc,lc.tw.step_time)*100
            while millis()<endtime:
                yield True
            setlayer(lc.tw.turtle.spr,100)
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
        if type(lc.cfun.fcn)==lc.listtype:
            icall(lc, ufuncall, cfun.fcn); yield True
        else:
            icall(lc, lc.cfun.fcn, *lc.arglist); yield True
        result = None
    else: 
        result = lc.cfun.fcn(lc, *lc.arglist)
    lc.cfun, lc.arglist = oldcfun, oldarglist
    if lc.arglist!=None and result==None:
        raise logoerror("%s didn't output to %s" % \
            (oldcfun.name, lc.cfun.name))
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

def prim_stack(lc,stri):
    if (not lc.stacks.has_key('stack3'+stri)) or \
        lc.stacks['stack3'+stri]==None: raise logoerror("#nostack")
    icall(lc, evline, lc.stacks['stack3'+stri][:]); yield True
    lc.procstop = False
    ireturn(lc); yield True

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

def careful_divide(x,y):
    try:
        if y==0: return 0
        return x/y
    except:
        return 0

def ufuncall(body):
    ijmp(evline, body); yield True

def an_int(lc, n):
    if type(n) == int:
        return n
    elif type(n) == float:
        return int(n)
    elif type(n) == str:
        return int(ord(n[0]))
    else:
        raise logoerror("%s doesn't like %s as input" \
            % (lc.cfun.name, str(n)))

def defprim(lc, name, args, fcn, rprim=False):
    sym = intern(lc, name)
    sym.nargs, sym.fcn = args,fcn
    sym.rprim = rprim

def taequal(x,y):
    try:
        return float(x)==float(y)
    except:
        if type(x) == str:
            xx = ord(x[0])
        else:
            xx = x
        if type(y) == str:
            yy = ord(y[0])
        else:
            yy = y
        return xx==yy

def taless(x,y):
    try:
        return(x<y)
    except:
        raise logoerror("#syntaxerror")

def tamore(x,y):
    return taless(y,x)

def taplus(x,y):
    if (type(x) == int or type(x) == float) and \
        (type(y) == int or type(y) == float):
        return(x+y)
    else:
        return(str(x) + str(y))

def taminus(x,y):
    try:
        return(x-y)
    except:
        raise logoerror("#syntaxerror")

def taproduct(x,y):
    try:
        return(x*y)
    except:
        raise logoerror("#syntaxerror")

def tamod(x,y):
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

def lcNew(tw):
    lc = taLogo()
    lc.tw = tw
    lc.oblist = {}

    defprim(lc,'print', 1, lambda lc,x: status_print(lc,x))
    defprim(lc,'+', None, lambda lc,x,y:x+y)
    defprim(lc,'plus', 2, lambda lc,x,y:taplus(x,y))
    defprim(lc,'-', None, lambda lc,x,y:x-y)
    defprim(lc,'minus', 2, lambda lc,x,y:taminus(x,y))
    defprim(lc,'*', None, lambda lc,x,y:x*y)
    defprim(lc,'product', 2, lambda lc,x,y:taproduct(x,y))
    defprim(lc,'/', None, lambda lc,x,y:careful_divide(x,y))
    defprim(lc,'division', 2, lambda lc,x,y:careful_divide(x,y))
    defprim(lc,'random', 2, lambda lc,x,y: int(random.uniform(x,y)))
    defprim(lc,'greater?', 2, lambda lc,x,y: tamore(x,y))
    defprim(lc,'less?', 2, lambda lc,x,y: taless(x,y))
    defprim(lc,'equal?', 2, lambda lc,x,y: taequal(x,y))
    defprim(lc,'and', None, lambda lc,x,y:x&y)
    defprim(lc,'or', None, lambda lc,x,y:x|y)
    defprim(lc,'not', 1, lambda lc,x:not x)
    defprim(lc,'%', None, lambda lc,x,y:x%y)
    defprim(lc,'mod', 2, lambda lc,x,y:tamod(x,y))
    defprim(lc,'sqrt', 1, lambda lc,x: sqrt(x))
    defprim(lc,'id',1, lambda lc,x: identity(x))
    
    defprim(lc,'sensor_val0', 0, lambda lc: sensor_val(lc, 0))
    defprim(lc,'sensor_val1', 0, lambda lc: sensor_val(lc, 1))
    defprim(lc,'sensor_val2', 0, lambda lc: sensor_val(lc, 2))
    defprim(lc,'sensor_val3', 0, lambda lc: sensor_val(lc, 3))

    defprim(lc,'clean', 0, lambda lc: clear(lc))
    defprim(lc,'forward', 1, lambda lc, x: forward(lc.tw.turtle, x))
    defprim(lc,'back', 1, lambda lc,x: forward(lc.tw.turtle,-x))
    defprim(lc,'seth', 1, lambda lc, x: seth(lc.tw.turtle, x))
    defprim(lc,'right', 1, lambda lc, x: right(lc.tw.turtle, x))
    defprim(lc,'left', 1, lambda lc,x: right(lc.tw.turtle,-x))
    defprim(lc,'heading', 0, lambda lc: lc.tw.turtle.heading)
    defprim(lc,'setxy', 2, lambda lc, x, y: setxy(lc.tw.turtle, x, y))
    defprim(lc,'write',2,lambda lc, x,y: write(lc.tw.turtle, x,y))
    defprim(lc,'insertimage', 1, lambda lc,x: insert_image(lc, x))
    defprim(lc,'arc', 2, lambda lc, x, y: arc(lc.tw.turtle, x, y))
    defprim(lc,'xcor', 0, lambda lc: lc.tw.turtle.xcor)
    defprim(lc,'ycor', 0, lambda lc: lc.tw.turtle.ycor)

    defprim(lc,'pendown', 0, lambda lc: setpen(lc.tw.turtle, True))
    defprim(lc,'penup', 0, lambda lc: setpen(lc.tw.turtle, False))
    defprim(lc,'(', 1, lambda lc, x: prim_opar(lc,x))
    defprim(lc,'setcolor', 1, lambda lc, x: setcolor(lc.tw.turtle, x))
    defprim(lc,'settextcolor', 1, lambda lc, x: settextcolor(lc.tw.turtle, x))
    defprim(lc,'setshade', 1, lambda lc, x: setshade(lc.tw.turtle, x))
    defprim(lc,'setpensize', 1, lambda lc, x: setpensize(lc.tw.turtle, x))
    defprim(lc,'fillscreen', 2, lambda lc, x, y: \
        fillscreen(lc.tw.turtle, x, y))
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
    defprim(lc,'stack', 1, prim_stack, True)
    defprim(lc,'box1', 0, lambda lc: lc.boxes['box1'])
    defprim(lc,'box2', 0, lambda lc: lc.boxes['box2'])
    defprim(lc,'box', 1, lambda lc,x: lc.boxes['box3'+str(x)])
    defprim(lc,'storeinbox1', 1, lambda lc,x: setbox(lc, 'box1',x))
    defprim(lc,'storeinbox2', 1, lambda lc,x: setbox(lc, 'box2',x))
    defprim(lc,'storeinbox', 2, lambda lc,x,y: setbox(lc, 'box3'+str(x),y))
    defprim(lc,'push', 1, lambda lc,x: push_heap(lc,x))
    defprim(lc,'pop', 0, lambda lc: pop_heap(lc))
    defprim(lc,'heap', 0, lambda lc: heap_print(lc))
    defprim(lc,'emptyheap', 0, lambda lc: empty_heap(lc))

    defprim(lc,'define', 2, prim_define)
    defprim(lc,'nop', 0, lambda lc: None)
    defprim(lc,'nop1', 0, lambda lc: None)
    defprim(lc,'nop2', 0, lambda lc: None)
    defprim(lc,'nop3', 1, lambda lc,x: None)
    defprim(lc,'start', 0, lambda: None)

    lc.symtype = type(intern(lc, 'print'))
    lc.listtype = type([])
    lc.symnothing = intern(lc, '%nothing%')
    lc.symopar = intern(lc, '(')

    lc.istack = []
    lc.stacks = {}
    lc.boxes = noKeyError({'box1': 0, 'box2': 0})
    lc.heap = []
    lc.keyboard = 0
    lc.gplay = None
    lc.title_height = int((tw.turtle.height/30)*tw.scale)
    lc.body_height = int((tw.turtle.height/60)*tw.scale)
    lc.bullet_height = int((tw.turtle.height/45)*tw.scale)

    lc.iline, lc.cfun, lc.arglist, lc.ufun = None, None, None,None

    return lc

def show_picture(lc, media, x, y, w, h):
    if media == "" or media[6:] == "":
#        raise logoerror("#nomedia")
         print "no media"
    elif media[6:] != "None":
        try:
            dsobject = datastore.get(media[6:])
        except:
            raise logoerror("#nomedia")
        # check to see if it is a movie
        print dsobject.file_path
        if dsobject.file_path[-4:] == '.ogv':
            print "playing movie x:" + str(x) + " y:" + str(y) + " w:" \
                + str(w) + " h:" + str(h)
            play_dsobject(lc, dsobject, int(x), int(y), int(w), int(h))
        else:
            pixbuf = get_pixbuf_from_journal(dsobject,w,h)
            if pixbuf != None:
                draw_pixbuf(lc.tw.turtle, pixbuf, 0, 0, int(x), int(y), \
                    int(w), int(h))
        dsobject.destroy()

def get_pixbuf_from_journal(dsobject,w,h):
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(dsobject.file_path,w,h)
    except:
        try:
            # print "Trying preview..."
            pixbufloader = gtk.gdk.pixbuf_loader_new_with_mime_type \
                ('image/png')
            pixbufloader.set_size(min(300,w),min(225,h))
            pixbufloader.write(dsobject.metadata['preview'])
            pixbufloader.close()
#            gtk.gdk_pixbuf_loader_close(pixbufloader)
            pixbuf = pixbufloader.get_pixbuf()
        except:
            # print "No preview"
            pixbuf = None
    return pixbuf

# image only (at current x,y)
def insert_image(lc, media):
    w = 0.25
    h = 0.25
    w *= lc.tw.turtle.width
    h *= lc.tw.turtle.height
    # convert from Turtle coordinates to screen coordinates
    x = lc.tw.turtle.width/2+int(lc.tw.turtle.xcor)
    y = lc.tw.turtle.height/2-int(lc.tw.turtle.ycor)
    if media[0:5] == 'media':
        show_picture(lc, media, x, y, w, h)

def clear(lc):
    clearscreen(lc.tw.turtle)

def write(lc, string, fsize):
    # convert from Turtle coordinates to screen coordinates
    x = lc.tw.turtle.width/2+int(lc.tw.turtle.xcor)
    y = lc.tw.turtle.height/2-int(lc.tw.turtle.ycor)
    draw_text(lc.tw.turtle,string,x,y,int(fsize),lc.tw.turtle.width)

def hideblocks(lc):
    from tawindow import hideshow_button
    lc.tw.hide = False # force hide
    hideshow_button(lc.tw)
    for i in lc.tw.selbuttons: hide(i)
    lc.tw.activity.projectToolbar.do_hide()

def doevalstep(lc):
    starttime = millis()
    try:
        while (millis()-starttime)<120:
            try:
                lc.step.next()
            except StopIteration:
                setlayer(lc.tw.turtle.spr,630)
                return False
    except logoerror, e:
        showlabel(lc, str(e)[1:-1])
        setlayer(lc.tw.turtle.spr,630)
        return False
    return True

def icall(lc, fcn, *args):
    lc.istack.append(lc.step)
    lc.step = fcn(lc, *(args))

def ireturn(lc, res=None):
    lc.step = lc.istack.pop()
    lc.iresult = res

def ijmp(lc, fcn, *args):
    lc.step = fcn(lc,*(args))

def heap_print(lc):
    showlabel(lc,lc.heap)

def status_print(lc,n):
    if type(n) == str:
        showlabel(lc,n)
    else:
        showlabel(lc,int(float(n)*10)/10.)

def showlabel(lc,l):
    if l=='#nostack': shp = 'nostack'; l=''
    elif l=='#noinput': shp = 'noinput'; l=''
    elif l=='#emptyheap': shp = 'emptyheap'; l=''
    elif l=='#nomedia': shp = 'nomedia'; l=''
    elif l=='#syntaxerror': shp = 'syntaxerror'; l=''
    else:shp = 'status'
    setshape(lc.tw.status_spr, lc.tw.status_shapes[shp])
    setlabel(lc.tw.status_spr,l)
    setlayer(lc.tw.status_spr,710)

def stop_logo(tw):
    tw.step_time = 0
    tw.lc.step = just_stop()

def just_stop(): yield False

def setbox(lc, name,val): lc.boxes[name]=val

def push_heap(lc,val): lc.heap.append(val)

def pop_heap(lc):
    try: return lc.heap.pop(-1)
    except: raise logoerror ("#emptyheap")

def empty_heap(lc): lc.heap = []

def tyo(n): print n

def millis(): return int(clock()*1000)

def sensor_val(lc, y):    
    return_this = 0
    ag = AudioGrab()
    return_this = ag.get_sensor_val(y)
    if y==3:
        return_this = ag.get_sensor_val(y)
    return return_this

