import re
from time import clock
from operator import isNumberType
import random

oblist = {}

iline = None
cfun = None
arglist = None

istack = []
iresult = None
step = None
procstop = False

boxes = {'box1': 0, 'box2': 0}
stacks = {}

utime_start = 0

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


def run_blocks(spr, blocks):
    stacks['stack1'] = None
    stacks['stack2'] = None
    for i in blocks:
        if i.proto.name=='hat1': stacks['stack1']= readline(blocks_to_code(i))
        if i.proto.name=='hat2': stacks['stack2']= readline(blocks_to_code(i))
    code = blocks_to_code(spr)
    print code
    setup_cmd(code)

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
    
def intern(str):
    if str in oblist: return oblist[str]
    sym = symbol(str)
    oblist[str] = sym
    return sym
    

def parseline(str):
    split = re.split(r"\s|([\[\]()])", str)
    return [x for x in split if x and x != ""]

def readline(line):
    res = []
    while line:
        token = line.pop(0)
        if isNumberType(token): res.append(token)
        elif token.isdigit(): res.append(float(token))
        elif token[0]=='-' and token[1:].isdigit(): res.append(-float(token[1:]))
        elif token[0] == '"': res.append(token[1:])
        elif token == '[': res.append(readline(line))
        elif token == ']': return res
        else: res.append(intern(token))
    return res


def setup_cmd(str):
    global iline, step, procstop
    stopsignon(); procstop=False
    list = readline(str)
    step = start_eval(list)

def start_eval(list):
    icall(evline, list); yield True
    yield False

def evline(list):
    global cfun, arglist, iline
    oldiline = iline
    iline = list[:]
    arglist = None
    while iline: 
        token = iline[0]
        if token==symopar: token=iline[1]
        icall(eval); yield True
        if procstop: break
        if iresult==None: continue
        raise logoerror("You don't say what to do with %s" % token)
    iline = oldiline
    ireturn(); yield True
        
def eval(infixarg=False):
    token = iline.pop(0)
    if type(token) == symtype: 
        icall(evalsym, token); yield True
        res = iresult
    else: res = token
    if not infixarg:
        while infixnext():
            icall(evalinfix, res); yield True
            res = iresult
    ireturn(res); yield True    
            
def evalsym(token):
    global cfun, arglist
    undefined_check(token)
    oldcfun, oldarglist = cfun, arglist
    cfun, arglist = token, []
    for i in range(token.nargs):
        no_args_check()
        icall(eval); yield True
        arglist.append(iresult)
    if cfun.rprim:
        if type(cfun.fcn)==listtype: icall(ufuncall, cfun.fcn); yield True
        else: icall(cfun.fcn, *arglist); yield True
        result = None
    else: result = cfun.fcn(*arglist)
    cfun, arglist = oldcfun, oldarglist
    if arglist!=None and result==None: 
        raise logoerror("%s didn't output to %s" % (oldcfun.name, cfun.name)) 
    ireturn(result); yield True

def evalinfix(firstarg):
    global cfun, arglist
    token = iline.pop(0)
    oldcfun, oldarglist = cfun, arglist
    cfun, arglist = token, [firstarg]
    no_args_check()
    icall(eval,True); yield True
    arglist.append(iresult)
    result = cfun.fcn(*arglist)
    cfun, arglist = oldcfun, oldarglist
    ireturn (result); yield True   

def infixnext():
    if len(iline)==0: return False
    if type(iline[0])!=symtype: return False
    return iline[0].name in ['+', '-', '*', '/','%','and','or']

def undefined_check(token):
    if token.fcn != None: return False
    raise logoerror("I don't know how to %s" % token.name) 

    
def no_args_check():
    if iline and iline[0]!=symnothing : return
    raise logoerror("Not enough inputs to %s" % cfun.name) 

def prim_wait(time):
    turtle_spr.setlayer(630)
    endtime = millis()+an_int(time)*100
    while millis()<endtime:
        yield True
    turtle_spr.setlayer(100)
    ireturn(); yield True

def prim_repeat(num, list):
    num = an_int(num)
    for i in range(num):
        icall(evline, list[:]); yield True
        if procstop: break
    ireturn(); yield True

def prim_forever(list):
    while True:
        icall(evline, list[:]); yield True
        if procstop: break
    ireturn(); yield True

def prim_if(bool, list):
    if bool: icall(evline, list[:]); yield True
    ireturn(); yield True

def prim_ifelse(bool, list1,list2):
    if bool: ijmp(evline, list1[:]); yield True
    else: ijmp(evline, list2[:]); yield True

def prim_opar(val):
    iline.pop(0)
    return val
    
def prim_define(name, body):
    if type(name) != symtype: name = intern(name)
    name.nargs, name.fcn = 0, body
    name.rprim = True

def prim_stack1(): 
    global procstop
    if stacks['stack1']==None: raise logoerror("stack1 undefined")
    icall(evline, stacks['stack1'][:]); yield True
    procstop = False
    ireturn(); yield True

def prim_stack2(): 
    global procstop
    if stacks['stack2']==None: raise logoerror("stack2 undefined")
    icall(evline, stacks['stack2'][:]); yield True
    procstop = False
    ireturn(); yield True

def prim_stopstack():
    global procstop
    procstop = True

def prim_utimer():
    return float(int((clock()-utime_start)*1000000))
    
def prim_resetut():
    global utime_start
    utime_start = clock()


def ufuncall(body):
    ijmp(evline, body); yield True
    
def an_int(n):
    try: return int(n)
    except: raise logoerror("%s doesn't like %s as input" % (cfun.name, str(n)))

def a_float(n):
    try: return int(n)
    except: raise logoerror("%s doesn't like %s as input" % (cfun.name, str(n)))

def defprim(name, args, fcn, rprim=False):
    sym = intern(name)
    sym.nargs, sym.fcn = args,fcn
    sym.rprim = rprim

def init():
    global symtype, numtype, listtype, symnothing, symopar
    defprim('print', 1, lambda x:showlabel(int(float(x)*10)/10.))

    defprim('sum', 2, lambda x,y:x+y)
    defprim('+', None, lambda x,y:x+y)
    defprim('difference', 2, lambda x,y:x-y)
    defprim('-', None, lambda x,y:x-y)
    defprim('product', 2, lambda x,y:x*y)
    defprim('*', None, lambda x,y:x*y)
    defprim('quotient', 2, lambda x,y:x/y)
    defprim('/', None, lambda x,y:x/y)
    defprim('random', 2, lambda x,y: int(random.uniform(x,y)))
    defprim('greater?', 2, lambda x,y: float(x)>float(y))
    defprim('less?', 2, lambda x,y: float(x)<float(y))
    defprim('equal?', 2, lambda x,y: float(x)==float(y))
    defprim('and', None, lambda x,y:x&y)
    defprim('or', None, lambda x,y:x|y)
    defprim('not', 1, lambda x:not x)
    defprim('%', None, lambda x,y:x%y)

    defprim('clean', 0, turtle.clearscreen)
    defprim('forward', 1, turtle.forward)
    defprim('back', 1, lambda x: turtle.forward(-x))
    defprim('seth', 1, turtle.seth)
    defprim('right', 1, turtle.right)
    defprim('left', 1, lambda x:turtle.right(-x))
    defprim('heading', 0, lambda: turtle.heading)
    defprim('setxy', 2, turtle.setxy)
    defprim('arc', 2, turtle.arc)
    defprim('xcor', 0, lambda: turtle.xcor)
    defprim('ycor', 0, lambda: turtle.ycor)

    defprim('pendown', 0, lambda: turtle.setpen(True))
    defprim('penup', 0, lambda: turtle.setpen(False))
    defprim('(', 1, prim_opar)
    defprim('setcolor', 1, turtle.setcolor)
    defprim('setshade', 1, turtle.setshade)
    defprim('setpensize', 1, turtle.setpensize)
    defprim('fillscreen', 2, turtle.fillscreen)
    defprim('color', 0, lambda: turtle.color)
    defprim('shade', 0, lambda: turtle.shade)
    defprim('pensize', 0, lambda: turtle.pensize)

    defprim('wait', 1, prim_wait, True)
    defprim('repeat', 2, prim_repeat, True)
    defprim('forever', 1, prim_forever, True)
    defprim('if', 2, prim_if, True)
    defprim('ifelse', 3, prim_ifelse, True)
    defprim('stopstack', 0, prim_stopstack)

    defprim('stack1', 0, prim_stack1, True)
    defprim('stack2', 0, prim_stack2, True)
    defprim('box1', 0, lambda: boxes['box1'])
    defprim('box2', 0, lambda: boxes['box2'])
    defprim('storeinbox1', 1, lambda x: setbox('box1',x))
    defprim('storeinbox2', 1, lambda x: setbox('box2',x))

    defprim('define', 2, prim_define)
    defprim('resetut', 0, prim_resetut)
    defprim('utimer', 0, prim_utimer)
    defprim('nop', 0, lambda: None)
    defprim('start', 0, lambda: None)

    symtype = type(intern('print'))
    numtytpe = type(0.)
    listtype = type([])

    symnothing = intern('%nothing%')
    symopar = intern('(')

def doevalstep():
    starttime = millis()
    try: 
        while (millis()-starttime)<120:
            if not step.next(): stopsignoff(); return False
    except logoerror, e: showlabel(str(e)[1:-1]); stopsignoff(); return False
    return True

def icall(fcn, *args):
    global step
    istack.append(step)
    step = fcn(*(args))
    
def ireturn(res=None):
    global step, iresult
    step = istack.pop()
    iresult = res
    
def ijmp(fcn, *args):
    global step
    step = fcn(*(args))

def showlabel(l):
    status.setlabel(l)
    status.setlayer(710);

def stopsignon(): 
    stopsign.setshape(stopsign.onshape)
    turtle_spr.setlayer(100)

def stopsignoff():
    stopsign.setshape(stopsign.offshape)
    turtle_spr.setlayer(630)

def setbox(name,val): boxes[name]=val
def tyo(n): print n
def millis(): return int(clock()*1000)

