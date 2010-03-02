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
# palette is selected. Some examples of how to use this block are included
# below. Try uncommenting an example or write your own Python code.
# 
# To uncomment code, remove the '# ' in the Python code. Take care to preserve
# the proper indentations.
#

def myblock(lc, x):

    ###########################################################################
    #
    # Set rgb color
    #
    ###########################################################################

    # r = int(x[0])
    # while r < 0:
    #     r += 256
    # while r > 255:
    #     r -= 256
    # g = int(x[1])
    # while g < 0:
    #     g += 256
    # while g > 255:
    #     g -= 256
    # b = int(x[0])
    # while b < 0:
    #     b += 256
    # while b > 255:
    #     b -= 256
    # rgb = "#%02x%02x%02x" % (r,g,b)
    # lc.tw.canvas.fgcolor = lc.tw.canvas.cm.alloc_color(rgb)
    # return

    ###########################################################################
    #
    # Draw a dotted line of length x.
    #
    ###########################################################################

    try:  # make sure x is a number
        x = float(x)
    except ValueError:
        return
    if lc.tw.canvas.pendown:
        dist = 0
        while dist+lc.tw.canvas.pensize < x:   # repeat drawing dots
            lc.tw.canvas.setpen(True)
            lc.tw.canvas.forward(1)
            lc.tw.canvas.setpen(False)
            lc.tw.canvas.forward((lc.tw.canvas.pensize*2)-1)
            dist += (lc.tw.canvas.pensize*2)
        lc.tw.canvas.forward(x-dist)           # make sure we have moved exactly x
        lc.tw.canvas.setpen(True)
    else:
        lc.tw.canvas.forward(x)
    return

    ###########################################################################
    #
    # Push an uppercase version of a string onto the heap.
    # Use a 'pop' block to use the new string.
    #
    ###########################################################################

    # if type(x) != str:
    #     X = str(x).upper()
    # else:
    #     X = x.upper()
    # lc.heap.append(X)
    # return

    ###########################################################################
    #
    # Push hours, minutes, seconds onto the FILO.
    # Use three 'pop' blocks to retrieve these values.
    # Note: because we use a FILO (first in, last out heap),
    # the first value you will pop will be seconds.
    #
    ###########################################################################

    # lc.heap.append(localtime().tm_hour)
    # lc.heap.append(localtime().tm_min)
    # lc.heap.append(localtime().tm_sec)
    # return

    ###########################################################################
    #
    # Add a third dimension (gray) to the color model.
    #
    ###########################################################################

    # val = 0.3 * lc.tw.rgb[0] + 0.6 * lc.tw.rgb[1] + 0.1 * lc.tw.rgb[2]
    # if x != 100:
    #     x = int(x)%100
    # r = int((val*(100-x) + lc.tw.rgb[0]*x)/100)
    # g = int((val*(100-x) + lc.tw.rgb[1]*x)/100)
    # b = int((val*(100-x) + lc.tw.rgb[2]*x)/100)
    # reallocate current color
    # rgb = "#%02x%02x%02x" % (r,g,b)
    # lc.tw.canvas.fgcolor = lc.tw.canvas.cm.alloc_color(rgb)
    # return

    ###########################################################################
    #
    # Save an image named x to the Sugar Journal.
    #
    ###########################################################################

    # lc.tw.save_as_image(str(x))
    # return


