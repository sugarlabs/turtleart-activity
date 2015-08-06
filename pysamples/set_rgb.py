# Copyright (c) 2009-11, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected and expanded to 3 arguments.

# Usage: Import this code into a Python (user-definable) block.
# First, expand the Python block to reveal three numerics arguments.
# Set these values to the desired red, green, and blue. When the code
# is run, the red, green, and blue values are used to set the pen
# color.


def myblock(tw, rgb_array):
    ''' Set rgb color from values '''

    tw.canvas._fgrgb = rgb_array[:]
