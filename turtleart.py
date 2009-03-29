#!/usr/bin/env python
#Copyright (c) 2007-8, Playful Invention Company
#Copyright (c) 2008-9, Walter Bender

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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import os.path

from tawindow import *

"""
Make a path if it doesn't previously exist
"""
def makepath(path):

    from os import makedirs
    from os.path import normpath, dirname, exists

    dpath = normpath(dirname(path))
    if not exists(dpath): makedirs(dpath)

"""
Launch Turtle Art from outside of Sugar
$ python turtleart.py

Caveats:
    * no Sugar toolbars
    * no Sugar Journal access
    * no Sugar sharing
"""
def main():
    # make sure Sugar paths are present
    tapath = os.path.join(os.environ['HOME'],'.sugar','default', \
                          'org.laptop.TurtleArtActivity')
    map (makepath, (os.path.join(tapath,'data/'), \
                    os.path.join(tapath,'instance/')))

    win1 = gtk.Window(gtk.WINDOW_TOPLEVEL)
    twNew(win1, os.path.abspath('.'),os.environ['LANG'])
    win1.connect("destroy", lambda w: gtk.main_quit())
    gtk.main()
    return 0

if __name__ == "__main__":
    main()


