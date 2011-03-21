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

# Usage: Import this code into a Python (user-definable) block.
# First, expand the Python block to reveal three numerics arguments.
# Set these values to the desired red, green, and blue. When the code
# is run, the red, green, and blue values are used to set the pen
# color.


def myblock(tw, rgb_array):

    ###########################################################################
    #
    # Set rgb color from values
    #
    ###########################################################################

    
    rgb = "#%02x%02x%02x" % ((int(rgb_array[0]) % 256),
                             (int(rgb_array[1]) % 256),
                             (int(rgb_array[2]) % 256))
    tw.canvas.fgcolor = tw.canvas.cm.alloc_color(rgb)
