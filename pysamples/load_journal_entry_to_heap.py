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
# this code is run, the chooser will be opened for selecting a file
# from the Journal. The contents of that file will be loaded onto the
# FILO heap.


def myblock(tw, x):  # ignore second argument

    ###########################################################################
    #
    # Load heap from journal
    #
    ###########################################################################

    from TurtleArt.tautils import chooser

    # Choose a datastore object and push data to heap (Sugar only)
    chooser(tw.parent, '', tw.lc.push_file_data_to_heap)
