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
import os
import os.path
from gettext import gettext as _
from taconstants import OVERLAY_LAYER
from tautils import data_to_string, data_from_string, get_save_name

from tawindow import TurtleArtWindow
from taexporthtml import save_html
from taexportlogo import save_logo

def makepath(path):
    """ Make a path if it doesn't previously exist """
    from os import makedirs
    from os.path import normpath, dirname, exists

    dpath = normpath(dirname(path))
    if not exists(dpath):
        makedirs(dpath)

class TurtleMain():
    def __init__(self):
        """ Launch Turtle Art from outside of Sugar """
        self.i = 0
        self.scale = 2.0
        self.tw = None
        # make sure Sugar paths are present
        tapath = os.path.join(os.environ['HOME'], '.sugar', 'default', \
                              'org.laptop.TurtleArtActivity')
        map (makepath, (os.path.join(tapath, 'data/'), \
                        os.path.join(tapath, 'instance/')))

        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        try:
            data_file = open('.turtleartrc', 'r')
        except IOError:
            data_file = open('.turtleartrc', 'a+')
            data_file.write(str(50)+'\n')
            data_file.write(str(50)+'\n')
            data_file.write(str(800)+'\n')
            data_file.write(str(550)+'\n')
            data_file.seek(0)
        self.x = int(data_file.readline())
        self.y = int(data_file.readline())
        self.width = int(data_file.readline())
        self.height = int(data_file.readline())
        win.set_default_size(self.width, self.height)
        win.move(self.x, self.y)
        win.maximize()
        win.set_title(_("Turtle Art"))
        win.connect("delete_event", lambda w, e: gtk.main_quit())

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("New"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_new_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Open"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_open_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Save"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_save_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Save As"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_save_as_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Save as image"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_save_picture_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Save as HTML"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_save_html_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Save as Logo"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_save_logo_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Quit"))
        menu.append(menu_items)
        menu_items.connect("activate", self.destroy)
        menu_items.show()

        activity_menu = gtk.MenuItem(_("File"))
        activity_menu.show()
        activity_menu.set_submenu(menu)

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("Cartesian coordinates"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_cartesian_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Polar coordinates"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_polar_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_('Rescale coordinates'))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_rescale_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Grow blocks"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_resize_cb, 1.5)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Shrink blocks"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_resize_cb, 0.667)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Reset block size"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_resize_cb, -1)
        menu_items.show()
        
        view_menu = gtk.MenuItem(_("View"))
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
        
        edit_menu = gtk.MenuItem(_("Edit"))
        edit_menu.show()
        edit_menu.set_submenu(menu)

        menu = gtk.Menu()

        menu_items = gtk.MenuItem(_("Show palette"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_palette_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Hide palette"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_hide_palette_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Show/hide blocks"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_hideshow_cb)
        menu_items.show()

        tool_menu = gtk.MenuItem(_("Tools"))
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
        menu_items = gtk.MenuItem(_("Debug"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_trace_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("Stop"))
        menu.append(menu_items)
        menu_items.connect("activate", self._do_stop_cb)
        menu_items.show()

        turtle_menu = gtk.MenuItem(_("Turtle"))
        turtle_menu.show()
        turtle_menu.set_submenu(menu)

        vbox = gtk.VBox(False, 0)
        win.add(vbox)
        vbox.show()

        menu_bar = gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 2)
        menu_bar.show()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.show()
        canvas = gtk.DrawingArea()
        width = gtk.gdk.screen_width() * 2
        height = gtk.gdk.screen_height() * 2
        canvas.set_size_request(width, height) 
        sw.add_with_viewport(canvas)
        canvas.show()
        vbox.pack_end(sw, True, True)

        menu_bar.append(activity_menu)
        menu_bar.append(edit_menu)
        menu_bar.append(view_menu)
        menu_bar.append(tool_menu)
        menu_bar.append(turtle_menu)

        win.show_all()

        if os.path.exists('/usr/share/turtleart'):
            self.tw = TurtleArtWindow(canvas, '/usr/share/turtleart')
        elif os.path.exists('/usr/local/share/turtleart'):
            self.tw = TurtleArtWindow(canvas, '/usr/local/share/turtleart')
        else:
            self.tw = TurtleArtWindow(canvas, os.path.abspath('.'))
        self.tw.win = win
        self.tw.load_start()
        self.tw.save_folder = os.path.expanduser("~")

    def _do_new_cb(self, widget):
        """ Callback for new project. """
        self.tw.new_project()
        self.tw.load_start()

    def _do_open_cb(self, widget):
        """ Callback for open project. """
        self.tw.load_file(True)

    def _do_save_cb(self, widget):
        """ Callback for save project. """
        self.tw.save_file()

    def _do_save_as_cb(self, widget):
        """ Callback for save-as project. """
        self.tw.save_file_name = None
        self.tw.save_file()

    def _do_save_picture_cb(self, widget):
        """ Callback for save canvas. """
        self.tw.save_as_image()

    def _do_save_html_cb(self, widget):
        """ Callback for save project to HTML. """
        html = save_html(self, self.tw, False)
        if len(html) == 0:
            return
        save_type = '.html'
        if len(self.tw.saved_pictures) > 0:
            if self.tw.saved_pictures[0].endswith(('.svg')):
                save_type = '.xml'
        filename, self.tw.load_save_folder = get_save_name(save_type,
                      self.tw.load_save_folder, 'portfolio')
        f = file(filename, "w")
        f.write(html)
        f.close()
        self.tw.saved_pictures = []

    def _do_save_logo_cb(self, widget):
        """ Callback for save project to Logo. """
        logocode = save_logo(self.tw)
        if len(logocode) == 0:
            return
        save_type = '.lg'
        filename, self.tw.load_save_folder = get_save_name(save_type,
                      self.tw.load_save_folder, 'logosession')
        f = file(filename, "w")
        f.write(logocode)
        f.close()

    def _do_resize_cb(self, widget, factor):
        """ Callback to resize blocks. """
        if factor == -1:
            self.tw.block_scale = 2.0     
        else:
            self.tw.block_scale *= factor
        self.tw.resize_blocks()

    def _do_cartesian_cb(self, button):
        """ Callback to display/hide Cartesian coordinate overlay. """
        if self.tw.cartesian is True:
            if self.tw.coord_scale == 1:
                self.tw.overlay_shapes['Cartesian_labeled'].hide()
            else:
                self.tw.overlay_shapes['Cartesian'].hide()
            self.tw.cartesian = False
        else:
            if self.tw.coord_scale == 1:
                self.tw.overlay_shapes['Cartesian_labeled'].set_layer(
                                                              OVERLAY_LAYER)
            else:
                self.tw.overlay_shapes['Cartesian'].set_layer(OVERLAY_LAYER)
            self.tw.cartesian = True

    def _do_polar_cb(self, button):
        """ Callback to display/hide Polar coordinate overlay. """
        if self.tw.polar is True:
            self.tw.overlay_shapes['polar'].hide()
            self.tw.polar = False
        else:
            self.tw.overlay_shapes['polar'].set_layer(OVERLAY_LAYER)
            self.tw.polar = True

    def _do_rescale_cb(self, button):
        """ Callback to rescale coordinate space. """
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height/200
            self.tw.eraser_button()
            if self.tw.cartesian is True:
                self.tw.overlay_shapes['Cartesian_labeled'].hide()
                self.tw.overlay_shapes['Cartesian'].set_layer(OVERLAY_LAYER)
        else:
            self.tw.coord_scale = 1
            self.tw.eraser_button()
            if self.tw.cartesian is True:
                self.tw.overlay_shapes['Cartesian'].hide()
                self.tw.overlay_shapes['Cartesian_labeled'].set_layer(
                                                              OVERLAY_LAYER)

    def _do_palette_cb(self, widget):
        """ Callback to show/hide palette of blocks. """
        self.tw.show_palette(self.i)
        self.i += 1
        if self.i == len(self.tw.palettes):
            self.i = 0

    def _do_hide_palette_cb(self, widget):
        """ Hide the palette of blocks. """
        self.tw.hide_palette()

    def _do_hideshow_cb(self, widget):
        """ Hide/show the blocks. """
        self.tw.hideshow_button()

    def _do_eraser_cb(self, widget):
        """ Callback for eraser button. """
        self.tw.eraser_button()
        return

    def _do_run_cb(self, widget):
        """ Callback for run button (rabbit). """
        self.tw.lc.trace = 0
        self.tw.run_button(0)
        return

    def _do_step_cb(self, widget):
        """ Callback for step button (turtle). """
        self.tw.lc.trace = 0
        self.tw.run_button(3)
        return

    def _do_trace_cb(self, widget):
        """ Callback for debug button (bug). """
        self.tw.lc.trace = 1
        self.tw.run_button(6)
        return

    def _do_stop_cb(self, widget):
        """ Callback for stop button. """
        self.tw.lc.trace = 0
        self.tw.stop_button()
        return

    def _do_copy_cb(self, button):
        """ Callback for copy button. """
        clipBoard = gtk.Clipboard()
        data = self.tw.assemble_data_to_save(False, False)
        if data is not []:
            text = data_to_string(data)
            clipBoard.set_text(text)

    def _do_paste_cb(self, button):
        """ Callback for paste button. """
        clipBoard = gtk.Clipboard()
        text = clipBoard.wait_for_text()
        if text is not None:
            self.tw.process_data(data_from_string(text))

    def _window_event(self, event, data):
        """ Callback for resize event. """
        data_file = open('.turtleartrc', 'w')
        data_file.write(str(data.x)+'\n')
        data_file.write(str(data.y)+'\n')
        data_file.write(str(data.width)+'\n')
        data_file.write(str(data.height)+'\n')

    def destroy(self, event, data=None):
        """ Callback for destroy event. """
        gtk.main_quit()

def main():
    """ python turtleart.py """
    gtk.main()
    return 0

if __name__ == "__main__":
    TurtleMain()
    main()

