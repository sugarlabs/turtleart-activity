#Copyright (c) 2010-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the chooser will be opened for selecting a file
# from the GNU/Linux file system. The contents of that file will be
# loaded onto the FILO heap. Data is assumed to be json encoded.


def myblock(tw, path):
    ''' Load heap from file (GNOME only) '''

    import os
    from TurtleArt.tautils import get_load_name, data_from_file

    if type(path) == float:
        path = ''

    if not os.path.exists(path):
        path, tw.load_save_folder = get_load_name('.*', tw.load_save_folder)
        if path is None:
            return

    data = data_from_file(path)
    if data is not None:
        for val in data:
            tw.lc.heap.append(val)
        tw.lc.update_label_value('pop', tw.lc.heap[-1])
