# Copyright (c) 2010-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the FILO heap will be copied to the clipboard.


def myblock(tw, x):  # second argument is ignored
    ''' Copy heap to clipboard '''

    from gtk import Clipboard
    from TurtleArt.tautils import data_to_string

    Clipboard().set_text(data_to_string(tw.lc.heap))
