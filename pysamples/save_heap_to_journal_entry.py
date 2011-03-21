#Copyright (c) 2010, Walter Bender, Tony Forster

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

# This procedure is invoked when the user-definable block on the "extras"
# palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the contents of the FILO heap are saved to a
# Journal entry named by the value of the argument to the Python
# block.


def myblock(tw, title):

    ###########################################################################
    #
    # Save heap to journal (Sugar only)
    #
    ###########################################################################

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
