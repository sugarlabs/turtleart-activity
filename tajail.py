#Copyright (c) 2009, Walter Bender (on behalf of Sugar Labs)

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

# a naive approach to running myfun in a jail
from time import *
from math import *
try:
    from numpy import *
except:
    pass
from taturtle import *

def myfunc(lc, f, x):
    # check to make sure no import calls are made
    myf = "def f(x): return " + f.replace("import","")
    userdefined = {}
    try:
        exec myf in globals(), userdefined
        return userdefined.values()[0](x)
    except:
        return None

def myfunc_import(lc, f, x):
    userdefined = {}
    exec f in globals(), userdefined
    return userdefined['myblock'](lc,x)

