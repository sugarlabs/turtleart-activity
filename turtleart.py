#!/usr/bin/env python
#Copyright (c) 2007-8, Playful Invention Company
#Copyright (c) 2008-10, Walter Bender

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
from tautils import data_to_string, data_from_string
from tawindow import TurtleArtWindow

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
        self.scale=2.0
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

        menu_items = gtk.MenuItem(_("Larger"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_resize_cb, 1.5)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Reset"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_resize_cb, -1)
        menu_items.show()
        
        view_menu = gtk.MenuItem("View")
        view_menu.show()
        view_menu.set_submenu(menu)

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("Copy"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_copy_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Paste"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_paste_cb)
        menu_items.show()
        
        edit_menu = gtk.MenuItem("Edit")
        edit_menu.show()
        edit_menu.set_submenu(menu)

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("Palette"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_palette_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Hide Palette"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_hide_palette_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Blocks"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_hideshow_cb)
        menu_items.show()

        tool_menu = gtk.MenuItem("Tools")
        tool_menu.show()
        tool_menu.set_submenu(menu)

        menu = gtk.Menu()

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

        turtle_menu = gtk.MenuItem("Turtle")
        turtle_menu.show()
        turtle_menu.set_submenu(menu)

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
        menu_bar.append(edit_menu)
        menu_bar.append(view_menu)
        menu_bar.append(tool_menu)
        menu_bar.append(turtle_menu)

        win.show_all()
        self.tw = TurtleArtWindow(canvas, os.path.abspath('.'), lang)
        self.tw.win = win

    def _do_open_cb(self, widget):
        self.tw.load_file(True)

    def _do_save_cb(self, widget):
        self.tw.save_file()

    def _do_resize_cb(self, widget, factor):
        if factor == -1:
            self.tw.block_scale = 2.0     
        else:
            self.tw.block_scale *= factor
        self.tw.resize_blocks()

    def _do_palette_cb(self, widget):
        self.tw.show_toolbar_palette(self.i)
        self.i += 1
        if self.i == len(self.tw.palettes):
            self.i = 0

    def _do_hide_palette_cb(self, widget):
        self.tw.hide_toolbar_palette()

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
        self.tw.stop_button()
        return

    def _do_copy_cb(self, button):
        clipBoard = gtk.Clipboard()
        data = self.tw.assemble_data_to_save(False, False)
        if data is not []:
            text = data_to_string(data)
            clipBoard.set_text(text)

    def _do_paste_cb(self, button):
        clipBoard = gtk.Clipboard()
        text = clipBoard.wait_for_text()
        if text is not None:
            self.tw.process_data(data_from_string(text))

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    TurtleMain()
    main()

