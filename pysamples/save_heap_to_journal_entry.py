#Copyright (c) 2010-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the contents of the FILO heap are saved to a
# Journal entry named by the value of the argument to the Python
# block.


def myblock(tw, title):
    ''' Save heap to journal (Sugar only) '''

    import os.path
    from gettext import gettext as _

    from sugar.activity import activity
    from sugar.datastore import datastore
    from sugar import profile

    from TurtleArt.tautils import get_path, data_to_file

    # Save JSON-encoded heap to temporary file
    heap_file = os.path.join(get_path(activity, 'instance'),
                             str(title) + '.txt')
    data_to_file(tw.lc.heap, heap_file)

    # Create a datastore object
    dsobject = datastore.create()

    # Write any metadata (specifically set the title of the file
    #                     and specify that this is a plain text file).
    dsobject.metadata['title'] = str(title)
    dsobject.metadata['icon-color'] = profile.get_color().to_string()
    dsobject.metadata['mime_type'] = 'text/plain'
    dsobject.set_file_path(heap_file)
    datastore.write(dsobject)
    dsobject.destroy()
