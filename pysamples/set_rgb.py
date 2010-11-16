#Copyright (c) 2009-10, Walter Bender

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

#
# This procedure is invoked when the user-definable block on the "extras"
# palette is selected and expanded to 3 arguments.

def myblock(lc, x):

    ###########################################################################
    #
    # Set rgb color from values
    #
    ###########################################################################

    # assuming x is an array [r, g, b]
    b = int(x[2])
    while b < 0:
        b += 256
    while b > 255:
        b -= 256
    g = int(x[1])
    while g < 0:
        g += 256
    while g > 255:
        g -= 256
    r = int(x[0])
    while r < 0:
        r += 256
    while r > 255:
        r -= 256
    rgb = "#%02x%02x%02x" % (r,g,b)
    lc.tw.canvas.fgcolor = lc.tw.canvas.cm.alloc_color(rgb)
