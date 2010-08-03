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

import getopt
import sys
import os
import os.path

import pycurl
import xmlrpclib

argv = sys.argv[:]  # Workaround for import behavior of gst in tagplay
sys.argv[1:] = []  # Execution of import gst cannot see '--help' or '-h'

from gettext import gettext as _

from taconstants import OVERLAY_LAYER
from tautils import data_to_string, data_from_string, get_save_name
from tawindow import TurtleArtWindow
from taexporthtml import save_html
from taexportlogo import save_logo

HELP_MSG = 'turtleart.py: ' + _('usage is') + """
 \tturtleart.py 
 \tturtleart.py project.ta
 \tturtleart.py --output_png project.ta
 \tturtleart.py -o project"""


def _make_sub_menu(menu, name):
    """ add a new submenu to the toolbar """
    sub_menu = gtk.MenuItem(name)
    sub_menu.show()
    sub_menu.set_submenu(menu)
    return sub_menu


def _make_menu_item(menu, tooltip, callback, arg=None):
    """ add a new item to the submenu """
    menu_items = gtk.MenuItem(tooltip)
    menu.append(menu_items)
    if arg is None:
        menu_items.connect('activate', callback)
    else:
        menu_items.connect('activate', callback, arg)
    menu_items.show()


def makepath(path):
    """ Make a path if it doesn't previously exist """
    from os import makedirs
    from os.path import normpath, dirname, exists

    dpath = normpath(dirname(path))
    if not exists(dpath):
        makedirs(dpath)


class TurtleMain():
    """ Launch Turtle Art from outside of Sugar """

    def __init__(self):
        """ Parse command-line options and initialize class """

        self.ta_file = None
        self.output_png = False
        self.uploading = False

        # Parse command line
        try:
            opts, args = getopt.getopt(argv[1:], 'ho',
                                       ['help', 'output_png'])
        except getopt.GetoptError, err:
            print str(err)
            print HELP_MSG
            sys.exit(2)
        for o, a in opts:
            if o in ('-h', '--help'):
                print HELP_MSG
                sys.exit()
            if o in ('-o', '--output_png'):
                self.output_png = True
            else:
                assert False, _('No option action:') + ' ' + o
        if args:
            self.ta_file = args[0]

        if len(args) > 1 or self.output_png and self.ta_file is None:
            print HELP_MSG
            sys.exit()

        if self.ta_file is not None:
            if not self.ta_file.endswith(('.ta')):
                self.ta_file += '.ta'
            if not os.path.exists(self.ta_file):
                assert False, ('%s: %s' % (self.ta_file, _('File not found')))

        self.i = 0
        self.scale = 2.0
        self.tw = None
        # make sure Sugar paths are present
        tapath = os.path.join(os.environ['HOME'], '.sugar', 'default',
                              'org.laptop.TurtleArtActivity')
        map (makepath, (os.path.join(tapath, 'data/'),
                        os.path.join(tapath, 'instance/')))

        if self.output_png:
            pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                    gtk.gdk.screen_width(),
                                    gtk.gdk.screen_height())
            canvas, mask = pixbuf.render_pixmap_and_mask()
        else:
            win = gtk.Window(gtk.WINDOW_TOPLEVEL)

            try:
                data_file = open('.turtleartrc', 'r')
            except IOError:
                data_file = open('.turtleartrc', 'a+')
                data_file.write(str(50) + '\n')
                data_file.write(str(50) + '\n')
                data_file.write(str(800) + '\n')
                data_file.write(str(550) + '\n')
                data_file.seek(0)
            self.x = int(data_file.readline())
            self.y = int(data_file.readline())
            self.width = int(data_file.readline())
            self.height = int(data_file.readline())

            win.set_default_size(self.width, self.height)
            win.move(self.x, self.y)
            win.maximize()
            win.set_title(_('Turtle Art'))
            win.set_icon_from_file('images/turtle.png')
            win.connect('delete_event', self._quit_ta)

            menu = gtk.Menu()
            _make_menu_item(menu, _('New'), self._do_new_cb)
            _make_menu_item(menu, _('Open'), self._do_open_cb)
            _make_menu_item(menu, _('Save'), self._do_save_cb)
            _make_menu_item(menu, _('Save As'), self._do_save_as_cb)
            _make_menu_item(menu, _('Save as image'), self._do_save_picture_cb)
            _make_menu_item(menu, _('Save as HTML'), self._do_save_html_cb)
            _make_menu_item(menu, _('Save as Logo'), self._do_save_logo_cb)
            _make_menu_item(menu, _('Upload to Web'), self._do_upload_to_web)
            _make_menu_item(menu, _('Quit'), self.destroy)
            activity_menu = _make_sub_menu(menu, _('File'))

            menu = gtk.Menu()
            _make_menu_item(menu, _('Cartesian coordinates'),
                           self._do_cartesian_cb)
            _make_menu_item(menu, _('Polar coordinates'), self._do_polar_cb)
            _make_menu_item(menu, _('Rescale coordinates'),
                            self._do_rescale_cb)
            _make_menu_item(menu, _('Grow blocks'), self._do_resize_cb, 1.5)
            _make_menu_item(menu, _('Shrink blocks'),
                            self._do_resize_cb, 0.667)
            _make_menu_item(menu, _('Reset block size'),
                            self._do_resize_cb, -1)
            view_menu = _make_sub_menu(menu, _('View'))

            menu = gtk.Menu()
            _make_menu_item(menu, _('Copy'), self._do_copy_cb)
            _make_menu_item(menu, _('Paste'), self._do_paste_cb)
            edit_menu = _make_sub_menu(menu, _('Edit'))

            menu = gtk.Menu()
            _make_menu_item(menu, _('Show palette'), self._do_palette_cb)
            _make_menu_item(menu, _('Hide palette'), self._do_hide_palette_cb)
            _make_menu_item(menu, _('Show/hide blocks'), self._do_hideshow_cb)
            tool_menu = _make_sub_menu(menu, _('Tools'))

            menu = gtk.Menu()
            _make_menu_item(menu, _('Clean'), self._do_eraser_cb)
            _make_menu_item(menu, _('Run'), self._do_run_cb)
            _make_menu_item(menu, _('Step'), self._do_step_cb)
            _make_menu_item(menu, _('Debug'), self._do_trace_cb)
            _make_menu_item(menu, _('Stop'), self._do_stop_cb)
            turtle_menu = _make_sub_menu(menu, _('Turtle'))

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

        self.tw.save_folder = os.path.expanduser('~')

        if not self.output_png:
            win.connect('configure_event', self.tw.update_overlay_position)
            self.tw.win = win
            if self.ta_file is None:
                self.tw.load_start()
            else:
                print self.ta_file
                self.tw.load_start(self.ta_file)
                self.tw.lc.trace = 0
                self.tw.run_button(0)

            gtk.main()

        else:
            self.tw.load_start(self.ta_file)
            self.tw.lc.trace = 0
            self.tw.run_button(0)
            self.tw.save_as_image(self.ta_file, canvas)

    def _quit_ta(self, widget=None, e=None):
        """ Save changes on exit """
        project_empty = self.tw.is_project_empty()
        if not project_empty:
            if self.tw.is_new_project():
                self._show_save_dialog(True)
            else:
                if self.tw.project_has_changes():
                    self._show_save_dialog(False)
        gtk.main_quit()

    def _show_save_dialog(self, new_project=True):
        """ Dialog for save project """
        dlg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_INFO,
                                buttons=gtk.BUTTONS_OK_CANCEL,
                                message_format=\
           _('You have unsaved work. Would you like to save before quitting?'))
        dlg.set_title(_('Save project?'))
        dlg.set_property('skip-taskbar-hint', False)

        resp = dlg.run()
        dlg.destroy()
        if resp == gtk.RESPONSE_OK:
            if new_project:
                self._save_as()
            else:
                self._save_changes()

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
        self._save_as()

    def _save_as(self):
        """ Save as is called from callback and quit """
        self.tw.save_file_name = None
        self.tw.save_file()

    def _save_changes(self):
        """ Save changes to current project """
        self.tw.save_file_name = None
        self.tw.save_file(self.tw._loaded_project)

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
        f = file(filename, 'w')
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
        f = file(filename, 'w')
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
            self.tw.coord_scale = self.tw.height / 200
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
            if self.tw.selected_blk is not None and\
               self.tw.selected_blk.name == 'string':
                for i in text:
                    self.tw.process_alphanumeric_input(i, -1)
                self.tw.selected_blk.resize()
            else:
                self.tw.process_data(data_from_string(text),
                                     self.tw.paste_offset)
                self.tw.paste_offset += 20

    def _window_event(self, event, data):
        """ Callback for resize event. """
        data_file = open('.turtleartrc', 'w')
        data_file.write(str(data.x) + '\n')
        data_file.write(str(data.y) + '\n')
        data_file.write(str(data.width) + '\n')
        data_file.write(str(data.height) + '\n')

    def destroy(self, event, data=None):
        """ Callback for destroy event. """
        gtk.main_quit()

    def _do_upload_to_web(self, widget):
        """ Create dialog for uploading current project to the Web """
        if not self.uploading:
            self.uploading = True
            self.pop_up = gtk.Window()
            self.pop_up.set_default_size(600, 400)
            self.pop_up.connect('delete_event', self._stop_uploading)
            table = gtk.Table(False, 1, 8)
            self.pop_up.add(table)
            login_label = gtk.Label(_('You must have an account at \
http://turtleartsite.sugarlabs.org to upload your project.'))
            table.attach(login_label, 0, 1, 0, 1)
            self.login_message = gtk.Label('')
            table.attach(self.login_message, 0, 1, 1, 2)

            self.Hbox1 = gtk.HBox()
            table.attach(self.Hbox1, 0, 1, 2, 3)
            self.username_entry = gtk.Entry()
            username_label = gtk.Label(_('Username:') + ' ')
            username_label.set_size_request(150, 25)
            self.username_entry.set_size_request(450, 25)
            self.Hbox1.add(username_label)
            self.Hbox1.add(self.username_entry)

            self.Hbox2 = gtk.HBox()
            table.attach(self.Hbox2, 0, 1, 3, 4)
            self.password_entry = gtk.Entry()
            password_label = gtk.Label(_('Password:') + ' ')
            self.password_entry.set_visibility(False)
            password_label.set_size_request(150, 25)
            self.password_entry.set_size_request(450, 25)
            self.Hbox2.add(password_label)
            self.Hbox2.add(self.password_entry)

            self.Hbox3 = gtk.HBox()
            table.attach(self.Hbox3, 0, 1, 4, 5)
            self.title_entry = gtk.Entry()
            title_label = gtk.Label(_('Title:') + ' ')
            title_label.set_size_request(150, 25)
            self.title_entry.set_size_request(450, 25)
            self.Hbox3.add(title_label)
            self.Hbox3.add(self.title_entry)

            self.Hbox4 = gtk.HBox()
            table.attach(self.Hbox4, 0, 1, 5, 6)
            self.description_entry = gtk.TextView()
            description_label = gtk.Label(_('Description:') + ' ')
            description_label.set_size_request(150, 25)
            self.description_entry.set_wrap_mode(gtk.WRAP_WORD)
            self.description_entry.set_size_request(450, 25)
            self.Hbox4.add(description_label)
            self.Hbox4.add(self.description_entry)

            self.submit_button = gtk.Button(_('Submit to Web'))
            self.submit_button.set_size_request(600, 25)
            self.submit_button.connect('pressed', self._do_remote_logon)
            table.attach(self.submit_button, 0, 1, 6, 7)
            self.pop_up.show_all()
            
    def _stop_uploading(self, widget, event):
        """ Hide the popup when the upload is complte """
        self.uploading = False
        self.pop_up.hide()

    def _do_remote_logon(self, widget):
        """ Log into the upload server """
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()
        server=xmlrpclib.ServerProxy(
            'http://turtleartsite.appspot.com/call/xmlrpc')
        logged_in = server.login_remote(username,password)
        if logged_in: 
            upload_key = logged_in
            self._do_submit_to_web(upload_key)
        else:
            self.login_message.set_text(_('Login failed'))

    def _do_submit_to_web(self, key):
        """ Submit project to the server """
        title = self.title_entry.get_text()
        description = self.description_entry.get_buffer().get_text(
            *self.description_entry.get_buffer().get_bounds())
        tafile, imagefile = self.tw.save_for_upload(title)

        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.URL, 'http://turtleartsite.appspot.com/upload')
        c.setopt(c.HTTPHEADER, ["Expect:"])
        c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, tafile)),
                              ('newimage', (c.FORM_FILE, imagefile)),
                              ('small_image', (c.FORM_FILE, imagefile)),
                              ('title', title),
                              ('description', description),
                              ('upload_key',key), ('_formname',
                                                   'image_create')])
        c.perform()
        error_code = c.getinfo(c.HTTP_CODE)
        c.close
        os.remove(imagefile)
        os.remove(tafile)
        if error_code == 400:
            self.login_message.set_text(_('Failed to upload!'))
        else:
            self.pop_up.hide()
            self.uploading = False


if __name__ == "__main__":
    TurtleMain()
