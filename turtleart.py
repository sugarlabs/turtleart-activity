#!/usr/bin/env python
#Copyright (c) 2007-8, Playful Invention Company
#Copyright (c) 2008-11, Walter Bender
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

import pygtk
pygtk.require('2.0')
import gtk

import getopt
import sys
import os
import os.path
import cStringIO
import errno

try:
    # Try to use XDG Base Directory standard for config files
    import xdg.BaseDirectory
    CONFIG_HOME = os.path.join(xdg.BaseDirectory.xdg_config_home, 'turtleart')
except ImportError, e:
    # Default to `.config` per the spec.
    CONFIG_HOME = os.path.expanduser(os.path.join('~', '.config', 'turtleart'))

argv = sys.argv[:]  # Workaround for import behavior of gst in tagplay
sys.argv[1:] = []  # Execution of import gst cannot see '--help' or '-h'

import gettext

gettext.bindtextdomain('org.laptop.TurtleArtActivity', 'locale')
gettext.textdomain('org.laptop.TurtleArtActivity')
_ = gettext.gettext

from TurtleArt.taconstants import OVERLAY_LAYER, DEFAULT_TURTLE_COLORS
from TurtleArt.tautils import data_to_string, data_from_string, get_save_name
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.taexporthtml import save_html
from TurtleArt.taexportlogo import save_logo
from extra.upload import Uploader
from extra.collaborationplugin import CollaborationPlugin
from util.menubuilder import MenuBuilder


class TurtleMain():
    """ Launch Turtle Art from outside of Sugar """

    _HELP_MSG = 'turtleart.py: ' + _('usage is') + """
 \tturtleart.py
 \tturtleart.py project.ta
 \tturtleart.py --output_png project.ta
 \tturtleart.py -o project"""
    _INSTALL_PATH = '/usr/share/turtleart'
    _ALTERNATE_INSTALL_PATH = '/usr/local/share/turtleart'
    _ICON_SUBPATH = 'images/turtle.png'

    def __init__(self):
        self._init_vars()
        self._parse_command_line()
        self._ensure_sugar_paths()

        if self.output_png:
            pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                    gtk.gdk.screen_width(),
                                    gtk.gdk.screen_height())
            self.canvas, mask = pixbuf.render_pixmap_and_mask()
            self._build_window()
            self._draw_and_quit()
        else:
            self._read_initial_pos()
            self._init_plugins()
            self._setup_gtk()
            self._build_window()
            self._run_plugins()
            self._start_gtk()

    def _init_plugins(self):
        config_file_path = os.path.join(CONFIG_HOME, 'turtleartrc.collab')
        self._collab_plugin = CollaborationPlugin(self, config_file_path)
        self._uploader = Uploader()

    def _run_plugins(self):
        self._uploader.set_tw(self.tw)
        self._collab_plugin.set_tw(self.tw)
        # self._collab_plugin.setup()

    def _mkdir_p(self, path):
        '''Create a directory in a fashion similar to `mkdir -p`'''
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    def _makepath(self, path):
        """ Make a path if it doesn't previously exist """
        from os import makedirs
        from os.path import normpath, dirname, exists

        dpath = normpath(dirname(path))
        if not exists(dpath):
            makedirs(dpath)

    def _start_gtk(self):
        self.win.connect('configure_event', self.tw.update_overlay_position)
        self.tw.win = self.win
        if self.ta_file is None:
            self.tw.load_start()
        else:
            print self.ta_file
            self.tw.load_start(self.ta_file)
            self.tw.lc.trace = 0
            self.tw.run_button(0)
        gtk.main()

    def _draw_and_quit(self):
        self.tw.load_start(self.ta_file)
        self.tw.lc.trace = 0
        self.tw.run_button(0)
        self.tw.save_as_image(self.ta_file, self.canvas)

    def _build_window(self):
        if os.path.exists(self._INSTALL_PATH):
            self.tw = TurtleArtWindow(self.canvas, self._INSTALL_PATH)
        elif os.path.exists(self._ALTERNATE_INSTALL_PATH):
            self.tw = TurtleArtWindow(self.canvas,
                                      self._ALTERNATE_INSTALL_PATH)
        else:
            self.tw = TurtleArtWindow(self.canvas, os.path.abspath('.'))

        self.tw.save_folder = os.path.expanduser('~')

    def _init_vars(self):
        """ If we are invoked to start a project from Gnome, we should make
        sure our current directory is TA's source dir. """
        os.chdir(os.path.dirname(__file__))

        self.ta_file = None
        self.output_png = False
        self.i = 0  # FIXME: use a better name for this variable
        self.scale = 2.0
        self.tw = None

    def _parse_command_line(self):
        try:
            opts, args = getopt.getopt(argv[1:], 'ho',
                                       ['help', 'output_png'])
        except getopt.GetoptError, err:
            print str(err)
            print self._HELP_MSG
            sys.exit(2)
        for o, a in opts:
            if o in ('-h', '--help'):
                print self._HELP_MSG
                sys.exit()
            if o in ('-o', '--output_png'):
                self.output_png = True
            else:
                assert False, _('No option action:') + ' ' + o
        if args:
            self.ta_file = args[0]

        if len(args) > 1 or self.output_png and self.ta_file is None:
            print self._HELP_MSG
            sys.exit()

        if self.ta_file is not None:
            if not self.ta_file.endswith(('.ta')):
                self.ta_file += '.ta'
            if not os.path.exists(self.ta_file):
                assert False, ('%s: %s' % (self.ta_file, _('File not found')))

    def _ensure_sugar_paths(self):
        """ Make sure Sugar paths are present. """
        tapath = os.path.join(os.environ['HOME'], '.sugar', 'default',
                              'org.laptop.TurtleArtActivity')
        map(self._makepath, (os.path.join(tapath, 'data/'),
                       os.path.join(tapath, 'instance/')))

    def _read_initial_pos(self):
        try:
            data_file = open(os.path.join(CONFIG_HOME, 'turtleartrc'), 'r')
        except IOError:
            # Opening the config file failed
            # We'll assume it needs to be created
            try:
                self._mkdir_p(CONFIG_HOME)
                data_file = open(os.path.join(CONFIG_HOME, 'turtleartrc'),
                                 'a+')
            except IOError, e:
                # We can't write to the configuration file, use
                # a faux file that will persist for the length of
                # the session.
                print _('Configuration directory not writable: %s') % (e)
            data_file = cStringIO.StringIO()
            data_file.write(str(50) + '\n')
            data_file.write(str(50) + '\n')
            data_file.write(str(800) + '\n')
            data_file.write(str(550) + '\n')
            data_file.seek(0)
        try:
            self.x = int(data_file.readline())
            self.y = int(data_file.readline())
            self.width = int(data_file.readline())
            self.height = int(data_file.readline())
        except ValueError:
            self.x = 50
            self.y = 50
            self.width = 800
            self.height = 550

    def _setup_gtk(self):
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_default_size(self.width, self.height)
        win.move(self.x, self.y)
        win.maximize()
        win.set_title(_('Turtle Art'))
        if os.path.exists(os.path.join(self._INSTALL_PATH,
                                       self._ICON_SUBPATH)):
            win.set_icon_from_file(os.path.join(self._INSTALL_PATH,
                                                self._ICON_SUBPATH))
        else:
            try:
                win.set_icon_from_file(self._ICON_SUBPATH)
            except IOError:
                pass
        win.connect('delete_event', self._quit_ta)

        vbox = gtk.VBox(False, 0)
        win.add(vbox)
        vbox.show()

        menu_bar = self._get_menu_bar()
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

        win.show_all()
        self.win = win
        self.canvas = canvas

    def _get_menu_bar(self):
        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('New'), self._do_new_cb)
        MenuBuilder.make_menu_item(menu, _('Open'), self._do_open_cb)
        MenuBuilder.make_menu_item(menu, _('Save'), self._do_save_cb)
        MenuBuilder.make_menu_item(menu, _('Save as'), self._do_save_as_cb)
        MenuBuilder.make_menu_item(menu, _('Save as image'),
                                   self._do_save_picture_cb)
        MenuBuilder.make_menu_item(menu, _('Save as HTML'),
                                   self._do_save_html_cb)
        MenuBuilder.make_menu_item(menu, _('Save as Logo'),
                                   self._do_save_logo_cb)
        if self._uploader.enabled():
            MenuBuilder.make_menu_item(menu, _('Upload to Web'),
                                 self._uploader.do_upload_to_web)
        MenuBuilder.make_menu_item(menu, _('Quit'), self.destroy)
        activity_menu = MenuBuilder.make_sub_menu(menu, _('File'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Cartesian coordinates'),
                        self._do_cartesian_cb)
        MenuBuilder.make_menu_item(menu, _('Polar coordinates'),
                                   self._do_polar_cb)
        MenuBuilder.make_menu_item(menu, _('Rescale coordinates'),
                        self._do_rescale_cb)
        MenuBuilder.make_menu_item(menu, _('Grow blocks'),
                                   self._do_resize_cb, 1.5)
        MenuBuilder.make_menu_item(menu, _('Shrink blocks'),
                        self._do_resize_cb, 0.667)
        MenuBuilder.make_menu_item(menu, _('Reset block size'),
                        self._do_resize_cb, -1)
        view_menu = MenuBuilder.make_sub_menu(menu, _('View'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Copy'), self._do_copy_cb)
        MenuBuilder.make_menu_item(menu, _('Paste'), self._do_paste_cb)
        edit_menu = MenuBuilder.make_sub_menu(menu, _('Edit'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Show palette'),
                                   self._do_palette_cb)
        MenuBuilder.make_menu_item(menu, _('Hide palette'),
                                   self._do_hide_palette_cb)
        MenuBuilder.make_menu_item(menu, _('Show/hide blocks'),
                                   self._do_hideshow_cb)
        tool_menu = MenuBuilder.make_sub_menu(menu, _('Tools'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Clean'), self._do_eraser_cb)
        MenuBuilder.make_menu_item(menu, _('Run'), self._do_run_cb)
        MenuBuilder.make_menu_item(menu, _('Step'), self._do_step_cb)
        MenuBuilder.make_menu_item(menu, _('Debug'), self._do_trace_cb)
        MenuBuilder.make_menu_item(menu, _('Stop'), self._do_stop_cb)
        turtle_menu = MenuBuilder.make_sub_menu(menu, _('Turtle'))

        collaboration_menu = self._collab_plugin.get_menu()

        menu_bar = gtk.MenuBar()
        menu_bar.append(activity_menu)
        menu_bar.append(edit_menu)
        menu_bar.append(view_menu)
        menu_bar.append(tool_menu)
        menu_bar.append(turtle_menu)
        menu_bar.append(collaboration_menu)
        return menu_bar

    def _quit_ta(self, widget=None, e=None):
        """ Save changes on exit """
        project_empty = self.tw.is_project_empty()
        if not project_empty:
            if self.tw.is_new_project():
                self._show_save_dialog(True)
            else:
                if self.tw.project_has_changed():
                    self._show_save_dialog(False)
        gtk.main_quit()

    def _show_save_dialog(self, new_project=True):
        """ Dialog for save project """
        dlg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_INFO,
                                buttons=gtk.BUTTONS_OK_CANCEL,
                                message_format=_(
             'You have unsaved work. Would you like to save before quitting?'))
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

    def nick_changed(self, nick):
        """ TODO: Rename default turtle in dictionary """
        pass

    def color_changed(self, colors):
        """ Reskin turtle with collaboration colors """
        turtle = self.tw.turtles.get_turtle(self.tw.default_turtle_name)
        try:
            turtle.colors = colors.split(',')
        except:
            turtle.colors = DEFAULT_TURTLE_COLORS
        turtle.custom_shapes = True  # Force regeneration of shapes
        turtle.reset_shapes()
        turtle.show()


if __name__ == "__main__":
    TurtleMain()
