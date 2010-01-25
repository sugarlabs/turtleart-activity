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
import locale
from gettext import gettext as _

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
class TurtleMain():
    def __init__(self):
        self.i = 0
        tw = None
        # make sure Sugar paths are present
        tapath = os.path.join(os.environ['HOME'],'.sugar','default', \
                              'org.laptop.TurtleArtActivity')
        map (makepath, (os.path.join(tapath,'data/'), \
                        os.path.join(tapath,'instance/')))

        """
        Find closest match for the user's $LANG
        """
        lang = locale.getdefaultlocale()[0]
        if not lang:
            lang = 'en'
        lang = lang[0:2]
        
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.maximize()
        win.set_title(_("Turtle Art"))
        win.connect("delete_event", lambda w,e: gtk.main_quit())

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("Open"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_open_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Save"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_save_cb)
        menu_items.show()
        
        activity_menu = gtk.MenuItem("File")
        activity_menu.show()
        activity_menu.set_submenu(menu)

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("Turtle"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_turtle_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Palette"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_palette_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Blocks"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_hideshow_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Clean"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_eraser_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Run"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_run_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Step"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_step_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Stop"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_stop_cb)
        menu_items.show()

        project_menu = gtk.MenuItem("Tools")
        project_menu.show()
        project_menu.set_submenu(menu)

        vbox = gtk.VBox(False, 0)
        win.add(vbox)
        vbox.show()

        menu_bar = gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 2)
        menu_bar.show()

        canvas = gtk.DrawingArea()
        vbox.pack_end(canvas, True, True)
        canvas.show()

        menu_bar.append(activity_menu)
        menu_bar.append(project_menu)

        win.show_all()
        self.tw = TurtleArtWindow(canvas, os.path.abspath('.'), lang)
        self.tw.win = win

    def _do_open_cb(self, widget):
        load_file(self.tw, True)

    def _do_save_cb(self, widget):
        save_file(self.tw)

    def _do_turtle_cb(self, widget):
        self.tw.show_toolbar_palette(self.i)
        self.i += 1
        if self.i > 6:
            self.i = 0

    def _do_palette_cb(self, widget):
        if self.tw.palette == True:
            self.tw.hideshow_palette(False)
        else:
            self.tw.hideshow_palette(True)

    def _do_hideshow_cb(self, widget):
        self.tw.hideshow_button()

    def _do_eraser_cb(self, widget):
        self.tw.eraser_button()
        return

    def _do_run_cb(self, widget):
        self.tw.lc.trace = 0
        self.tw.run_button(0)
        return

    def _do_step_cb(self, widget):
        self.tw.lc.trace = 0
        self.tw.run_button(3)
        return

    def _do_stop_cb(self, widget):
        self.tw.lc.trace = 0
        stop_button(self.tw)
        return


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    TurtleMain()
    main()

