#!/usr/bin/env python
#Copyright (c) 2011 Walter Bender
#Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

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

import gobject


class Plugin(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)

    def setup(self):
        """ Setup is called once, when the Turtle Window is created. """
        raise RuntimeError("You need to define setup for your plugin.")

    def start(self):
        """ start is called when run button is pressed. """
        raise RuntimeError("You need to define start for your plugin.")

    def stop(self):
        """ stop is called when stop button is pressed. """
        raise RuntimeError("You need to define stop for your plugin.")

    def goto_background(self):
        """ goto_background is called when the activity is sent to the
        background. """
        raise RuntimeError(
            "You need to define goto_background for your plugin.")

    def return_to_foreground(self):
        """ return_to_foreground is called when the activity returns to
        the foreground. """
        raise RuntimeError(
            "You need to define return_to_foreground for your plugin.")

    def quit(self):
        """ cleanup is called when the activity is exiting. """
        raise RuntimeError("You need to define quit for your plugin.")
