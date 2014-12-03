# Copyright (c) 2010-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the "extras"
# palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the contents of the clipboard will be appended to
# the FILO heap.


def myblock(tw, x):  # ignore second argument
    ''' Paste from clipboard to heap '''

    from gtk import Clipboard
    from tautils import data_from_string

    text = Clipboard().wait_for_text()
    if text is not None:
        for val in data_from_string(text):
            tw.lc.heap.append(val)
        tw.lc.update_label_value('pop', val)
