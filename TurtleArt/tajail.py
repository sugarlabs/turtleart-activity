# Copyright (c) 2009-10, Walter Bender (on behalf of Sugar Labs)

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

# A naive approach to running myfunc in a jail
import traceback


def myfunc(f, args):
    ''' Run inline Python code '''
    # check to make sure no import calls are made
    params = ", ".join(['x', 'y', 'z'][:len(args)])
    myf = ''.join(['def f(', params, '): return ', f.replace('import', '')])
    userdefined = {}
    exec(myf, globals(), userdefined)
    return list(userdefined.values())[0](*args)


def myfunc_import(parent, f, args):
    ''' Run Python code imported from Journal '''
    if 'def myblock(lc,' in f:
        base_class = parent.tw.lc  # pre-v107, we passed lc
    else:
        base_class = parent.tw  # as of v107, we pass tw
    userdefined = {}
    try:
        exec(f, globals(), userdefined)
        return userdefined['myblock'](base_class, args)
    except BaseException:
        traceback.print_exc()
        return None
