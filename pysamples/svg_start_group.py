# Copyright (c) 2009-11, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected and expanded to 3 arguments.

# Usage: Import this code into a Python (user-definable) block.
# In using SVG, it is sometimes useful to divide your drawing into
# groups of elements. You can do that by inserting <g> </g> around
# sections of your code.
#
# Place the svg_start_group.py block at the point in your program
# where you'd like to start a group in your SVG output.
#
# Be sure to use the corresponding svg_end_group.py block to close
# the SVG group definition.


def myblock(tw, x):
    ''' Add start group to SVG output '''

    tw.svg_string += '<g>'
