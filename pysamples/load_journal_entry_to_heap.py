#Copyright (c) 2010-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the chooser will be opened for selecting a file
# from the Journal. The contents of that file will be loaded onto the
# FILO heap.


def myblock(tw, x):  # ignore second argument
    ''' Load heap from journal (Sugar only) '''

    from TurtleArt.tautils import chooser

    # Choose a datastore object and push data to heap (Sugar only)
    chooser(tw.parent, '', tw.lc.push_file_data_to_heap)
