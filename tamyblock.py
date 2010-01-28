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
# To uncomment code, remove the #s before python code
#

def myblock(lc,x):

    ###########################################################################
    #
    # draw a dotted line of length x
    #
    ###########################################################################

    try:  # make sure x is a number
       x = float(x)
    except ValueError:
        return

    pen = lc.tw.canvas.pendown              # save current turtle pen state

    dist = 0
    while dist+lc.tw.canvas.pensize < x:    # repeat drawing dots
        lc.tw.canvas.setpen(True)
        lc.tw.canvas.forward(1)
        lc.tw.canvas.setpen(False)
        lc.tw.canvas.forward((lc.tw.canvas.pensize*2)-1)
        dist += (lc.tw.canvas.pensize*2)
    lc.tw.canvas.forward(x-dist)           # make sure we have moved x

    lc.tw.canvas.setpen(pen)               # restore pen state


    ###########################################################################
    #
    # push an uppercase version of a string onto the heap
    #
    ###########################################################################

    # if type(x) != str:
    #     X = str(x).upper()
    # else:
    #     X = x.upper()
    # push result onto heap (use the pop block to use the new string)
    # lc.heap.append(X)


    ###########################################################################
    #
    # push hours, minutes, seconds onto the heap
    # use three pop blocks to retrieve the values
    # remember: the heap is a FILO (first in, last out)
    # the first value you will pop will be seconds
    #
    ###########################################################################

    # lc.heap.append(localtime().tm_hour)
    # lc.heap.append(localtime().tm_min)
    # lc.heap.append(localtime().tm_sec)


    ###########################################################################
    #
    # add a third dimension (gray) to the color model
    # calculate the value (brightness) of the current color
    # val = 0.3 * lc.tw.rgb[0] + 0.6 * lc.tw.rgb[1] + 0.1 * lc.tw.rgb[2]
    # make sure gray is in range from 0 to 100
    #
    ###########################################################################


    # if x != 100:
    #     x = int(x)%100
    # mix in gray
    # r = int((val*(100-x) + lc.tw.rgb[0]*x)/100)
    # g = int((val*(100-x) + lc.tw.rgb[1]*x)/100)
    # b = int((val*(100-x) + lc.tw.rgb[2]*x)/100)
    # reallocate current color
    # lc.tw.fgcolor = lc.tw.cm.alloc_color(r<<8,g<<8,b<<8)


    ###########################################################################
    #
    # save a screen- image in the journal
    #
    ###########################################################################

    # lc.tw.activity._do_save_as_image_cb(lc.tw.activity)

    return

