# Copyright (c) 2009-11, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the current hour, minute, and second are pushed to
# the FILO heap. To use these values, pop second, then minute, then
# hour from the FILO.

from time import localtime


def myblock(tw, x):  # ignore second argument
    ''' Push hours, minutes, seconds onto the FILO. '''

    # Use three 'pop' blocks to retrieve these values.
    # Note: because we use a FILO (first in, last out heap),
    # the first value you pop off of the FILO will be seconds.

    tw.lc.heap.append(localtime().tm_hour)
    tw.lc.heap.append(localtime().tm_min)
    tw.lc.heap.append(localtime().tm_sec)
