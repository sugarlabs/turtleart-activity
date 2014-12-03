# Copyright (c) 2009-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the current mouse status will be pushed to the
# FILO heap. If a mouse button event occurs, a y, x, and 1 are pushed
# to the heap. If no button is pressed, 0 is pushed to the heap.

# To use these data, pop the heap in a compare block to determine if a
# button has been pushed. If a 1 was popped from the heap, pop the x
# and y coordinates.


def myblock(tw, x):  # ignore second argument
    ''' Push mouse event to stack '''

    if tw.mouse_flag == 1:
        # push y first so x will be popped first
        tw.lc.heap.append((tw.canvas.height / 2) - tw.mouse_y)
        tw.lc.heap.append(tw.mouse_x - (tw.canvas.width / 2))
        tw.lc.heap.append(1)  # mouse event
        tw.mouse_flag = 0
    else:
        tw.lc.heap.append(0)  # no mouse event
