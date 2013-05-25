#!/usr/bin/env python
#Copyright (c) 2007-8, Playful Invention Company
#Copyright (c) 2008-13, Walter Bender
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
import gobject
import cairo

import getopt
import sys
import os
import os.path
import glob
import cStringIO
import errno
import ConfigParser
import gconf

try:
    # Try to use XDG Base Directory standard for config files.
    import xdg.BaseDirectory
    CONFIG_HOME = os.path.join(xdg.BaseDirectory.xdg_config_home, 'turtleart')
except ImportError, e:
    # Default to `.config` per the spec.
    CONFIG_HOME = os.path.expanduser(os.path.join('~', '.config', 'turtleart'))

argv = sys.argv[:]  # Workaround for import behavior of gst in tagplay
sys.argv[1:] = []  # Execution of import gst cannot see '--help' or '-h'

import gettext
from gettext import gettext as _

from TurtleArt.taconstants import (OVERLAY_LAYER, DEFAULT_TURTLE_COLORS,
                                   TAB_LAYER, SUFFIX)
from TurtleArt.tautils import (data_from_string, get_save_name)
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.taexportlogo import save_logo

from util.menubuilder import MenuBuilder


class TurtleMain():
    ''' Launch Turtle Art in GNOME (from outside of Sugar). '''
    _INSTALL_PATH = '/usr/share/sugar/activities/TurtleArt.activity'
    _ALTERNATIVE_INSTALL_PATH = \
        '/usr/local/share/sugar/activities/TurtleArt.activity'
    _ICON_SUBPATH = 'images/turtle.png'
    _GNOME_PLUGIN_SUBPATH = 'gnome_plugins'
    _HOVER_HELP = '/desktop/sugar/activities/turtleart/hoverhelp'

    def __init__(self):
        self._abspath = os.path.abspath('.')
        self._execdirname = self._get_execution_dir()
        if self._execdirname is not None:
            os.chdir(self._execdirname)
        file_activity_info = ConfigParser.ConfigParser()
        activity_info_path = os.path.abspath('./activity/activity.info')
        file_activity_info.read(activity_info_path)
        bundle_id = file_activity_info.get('Activity', 'bundle_id')
        self.version = file_activity_info.get('Activity', 'activity_version')
        self.name = file_activity_info.get('Activity', 'name')
        self.summary = file_activity_info.get('Activity', 'summary')
        self.website = file_activity_info.get('Activity', 'website')
        self.icon_name = file_activity_info.get('Activity', 'icon')
        path = os.path.abspath('./locale/')
        gettext.bindtextdomain(bundle_id, path)
        gettext.textdomain(bundle_id)
        global _
        _ = gettext.gettext
        self._HELP_MSG = 'turtleblocks.py: ' + _('usage is') + '''
 \tturtleblocks.py
 \tturtleblocks.py project.tb
 \tturtleblocks.py --output_png project.tb
 \tturtleblocks.py -o project
 \tturtleblocks.py --run project.tb
 \tturtleblocks.py -r project'''
        self._init_vars()
        self._parse_command_line()
        self._ensure_sugar_paths()
        self._gnome_plugins = []

        if self._output_png:
            # Outputing to file, so no need for a canvas
            self.canvas = None
            self._build_window(interactive=False)
            self._draw_and_quit()
        else:
            self._read_initial_pos()
            self._init_gnome_plugins()
            self._get_gconf_settings()
            self._setup_gtk()
            self._build_window()
            self._run_gnome_plugins()
            self._start_gtk()

    def _get_gconf_settings(self):
        self.client = gconf.client_get_default()

    def get_config_home(self):
        return CONFIG_HOME

    def _get_gnome_plugin_home(self):
        ''' Use plugin directory associated with execution path. '''
        if os.path.exists(os.path.join(self._execdirname,
                                       self._GNOME_PLUGIN_SUBPATH)):
            return os.path.join(self._execdirname, self._GNOME_PLUGIN_SUBPATH)
        else:
            return None

    def _get_plugin_candidates(self, path):
        ''' Look for plugin files in plugin directory. '''
        plugin_files = []
        if path is not None:
            candidates = os.listdir(path)
            for c in candidates:
                if c[-10:] == '_plugin.py' and c[0] != '#' and c[0] != '.':
                    plugin_files.append(c.split('.')[0])
        return plugin_files

    def _init_gnome_plugins(self):
        ''' Try launching any plugins we may have found. '''
        for p in self._get_plugin_candidates(self._get_gnome_plugin_home()):
            P = p.capitalize()
            f = "def f(self): from gnome_plugins.%s import %s; \
return %s(self)" % (p, P, P)
            plugin = {}
            try:
                exec f in globals(), plugin
                self._gnome_plugins.append(plugin.values()[0](self))
            except ImportError, e:
                print 'failed to import %s: %s' % (P, str(e))

    def _run_gnome_plugins(self):
        ''' Tell the plugin about the TurtleWindow instance. '''
        for p in self._gnome_plugins:
            p.set_tw(self.tw)

    def _mkdir_p(self, path):
        '''Create a directory in a fashion similar to `mkdir -p`.'''
        try:
            os.makedirs(path)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    def _makepath(self, path):
        ''' Make a path if it doesn't previously exist '''
        from os import makedirs
        from os.path import normpath, dirname, exists

        dpath = normpath(dirname(path))
        if not exists(dpath):
            makedirs(dpath)

    def _start_gtk(self):
        ''' Get a main window set up. '''
        self.win.connect('configure_event', self.tw.update_overlay_position)
        self.tw.parent = self.win
        self.init_complete = True
        if self._ta_file is None:
            self.tw.load_start()
        else:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            gobject.idle_add(self._project_loader, self._ta_file)
        gtk.main()

    def _project_loader(self, file_name):
        self.tw.load_start(self._ta_file)
        self.tw.lc.trace = 0
        if self._run_on_launch:
            self._do_run_cb()
        self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    def _draw_and_quit(self):
        ''' Non-interactive mode: run the project, save it to a file
        and quit. '''
        self.tw.load_start(self._ta_file)
        self.tw.lc.trace = 0
        self.tw.run_button(0)
        self.tw.save_as_image(self._ta_file)

    def _build_window(self, interactive=True):
        ''' Initialize the TurtleWindow instance. '''
        if interactive:
            win = self.canvas.get_window()
            cr = win.cairo_create()
            surface = cr.get_target()
        else:
            img_surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                             1024, 768)
            cr = cairo.Context(img_surface)
            surface = cr.get_target()
        self.turtle_canvas = surface.create_similar(
            cairo.CONTENT_COLOR, max(1024, gtk.gdk.screen_width() * 2),
            max(768, gtk.gdk.screen_height() * 2))
        self.tw = TurtleArtWindow(self.canvas, self._execdirname,
                                  turtle_canvas=self.turtle_canvas,
                                  parent=self, running_sugar=False)
        self.tw.save_folder = self._abspath  # os.path.expanduser('~')
        if self.client.get_int(self._HOVER_HELP) == 1:
            self.hover.set_active(False)
            self._do_hover_help_off_cb(None)

    def _init_vars(self):
        ''' If we are invoked to start a project from Gnome, we should make
        sure our current directory is TA's source dir. '''
        self._ta_file = None
        self._output_png = False
        self._run_on_launch = False
        self.current_palette = 0
        self.scale = 2.0
        self.tw = None
        self.init_complete = False

    def _parse_command_line(self):
        ''' Try to make sense of the command-line arguments. '''
        try:
            opts, args = getopt.getopt(argv[1:], 'hor',
                                       ['help', 'output_png', 'run'])
        except getopt.GetoptError, err:
            print str(err)
            print self._HELP_MSG
            sys.exit(2)
        self._run_on_launch = False
        for o, a in opts:
            if o in ('-h', '--help'):
                print self._HELP_MSG
                sys.exit()
            if o in ('-o', '--output_png'):
                self._output_png = True
            elif o in ('-r', '--run'):
                self._run_on_launch = True
            else:
                assert False, _('No option action:') + ' ' + o
        if args:
            self._ta_file = args[0]

        if len(args) > 1 or self._output_png and self._ta_file is None:
            print self._HELP_MSG
            sys.exit()

        if self._ta_file is not None:
            if not self._ta_file.endswith(SUFFIX):
                self._ta_file += '.tb'
            if not os.path.exists(self._ta_file):
                self._ta_file = os.path.join(self._abspath, self._ta_file)
                if not os.path.exists(self._ta_file):
                    assert False, ('%s: %s' %
                                   (self._ta_file, _('File not found')))

    def _ensure_sugar_paths(self):
        ''' Make sure Sugar paths are present. '''
        tapath = os.path.join(os.environ['HOME'], '.sugar', 'default',
                              'org.laptop.TurtleArtActivity')
        map(self._makepath, (os.path.join(tapath, 'data/'),
                             os.path.join(tapath, 'instance/')))

    def _read_initial_pos(self):
        ''' Read saved configuration. '''
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

    def _fixed_resize_cb(self, widget=None, rect=None):
        ''' If a toolbar opens or closes, we need to resize the vbox
        holding out scrolling window. '''
        self.vbox.set_size_request(rect[2], rect[3])
        self.menu_height = self.menu_bar.size_request()[1]

    def _setup_gtk(self):
        ''' Set up a scrolled window in which to run Turtle Blocks. '''
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_default_size(self.width, self.height)
        win.move(self.x, self.y)
        win.maximize()
        win.set_title('%s %s' % (self.name, str(self.version)))
        if os.path.exists(os.path.join(self._execdirname, self._ICON_SUBPATH)):
            win.set_icon_from_file(os.path.join(self._execdirname,
                                                self._ICON_SUBPATH))
        win.show()
        win.connect('delete_event', self._quit_ta)

        ''' Create a scrolled window to contain the turtle canvas. We
        add a Fixed container in order to position text Entry widgets
        on top of string and number blocks.'''

        self.fixed = gtk.Fixed()
        self.fixed.connect('size-allocate', self._fixed_resize_cb)
        width = gtk.gdk.screen_width() - 80
        height = gtk.gdk.screen_height() - 80
        self.fixed.set_size_request(width, height)

        self.vbox = gtk.VBox(False, 0)
        self.vbox.show()

        self.menu_bar = self._get_menu_bar()
        self.vbox.pack_start(self.menu_bar, False, False, 2)
        self.menu_bar.show()
        self.menu_height = self.menu_bar.size_request()[1]

        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.show()
        canvas = gtk.DrawingArea()
        width = gtk.gdk.screen_width() * 2
        height = gtk.gdk.screen_height() * 2
        canvas.set_size_request(width, height)
        self.sw.add_with_viewport(canvas)
        canvas.show()
        self.vbox.pack_end(self.sw, True, True)
        self.fixed.put(self.vbox, 0, 0)
        self.fixed.show()

        win.add(self.fixed)
        win.show_all()
        self.win = win
        self.canvas = canvas

    def _get_menu_bar(self):
        ''' Instead of Sugar toolbars, use GNOME menus. '''
        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('New'), self._do_new_cb)
        MenuBuilder.make_menu_item(menu, _('Open'), self._do_open_cb)
        MenuBuilder.make_menu_item(menu, _('Save'), self._do_save_cb)
        MenuBuilder.make_menu_item(menu, _('Save as'), self._do_save_as_cb)
        MenuBuilder.make_menu_item(menu, _('Save as image'),
                                   self._do_save_picture_cb)
        MenuBuilder.make_menu_item(menu, _('Save as Logo'),
                                   self._do_save_logo_cb)
        MenuBuilder.make_menu_item(menu, _('Quit'), self._quit_ta)
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
        self.hover = MenuBuilder.make_checkmenu_item(
            menu, _('Turn on hover help'),
            self._do_toggle_hover_help_cb, status=True)
        view_menu = MenuBuilder.make_sub_menu(menu, _('View'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Copy'), self._do_copy_cb)
        MenuBuilder.make_menu_item(menu, _('Paste'), self._do_paste_cb)
        MenuBuilder.make_menu_item(menu, _('Save stack'),
                                   self._do_save_macro_cb)
        MenuBuilder.make_menu_item(menu, _('Delete stack'),
                                   self._do_delete_macro_cb)
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

        menu = gtk.Menu()
        self._level = 0
        self._levels = self._get_levels()
        self._custom_filepath = None
        for i in range(len(self._levels)):
            MenuBuilder.make_menu_item(menu, _('Challenge') + ' ' + str(i + 1),
                                       self._do_level_cb, i)
        turtle_menu = MenuBuilder.make_sub_menu(menu, _('Challenges'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('About...'), self._do_about_cb)
        help_menu = MenuBuilder.make_sub_menu(menu, _('Help'))

        menu_bar = gtk.MenuBar()
        menu_bar.append(activity_menu)
        menu_bar.append(edit_menu)
        menu_bar.append(view_menu)
        menu_bar.append(tool_menu)
        menu_bar.append(turtle_menu)

        # Add menus for plugins
        for p in self._gnome_plugins:
            menu_item = p.get_menu()
            if menu_item is not None:
                menu_bar.append(menu_item)

        menu_bar.append(help_menu)

        return menu_bar

    def _quit_ta(self, widget=None, e=None):
        ''' Save changes on exit '''
        project_empty = self.tw.is_project_empty()
        if not project_empty:
            if self.tw.is_new_project():
                self._show_save_dialog(True)
            else:
                if self.tw.project_has_changed():
                    self._show_save_dialog(False)
        for plugin in self.tw.turtleart_plugins:
            if hasattr(plugin, 'quit'):
                plugin.quit()
        gtk.main_quit()
        exit()

    def _show_save_dialog(self, new_project=True):
        ''' Dialog for save project '''
        dlg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_INFO,
                                buttons=gtk.BUTTONS_YES_NO,
                                message_format=_('You have unsaved work. \
Would you like to save before quitting?'))
        dlg.set_title(_('Save project?'))
        dlg.set_property('skip-taskbar-hint', False)

        resp = dlg.run()
        dlg.destroy()
        if resp == gtk.RESPONSE_YES:
            if new_project:
                self._save_as()
            else:
                self._save_changes()

    def _do_new_cb(self, widget):
        ''' Callback for new project. '''
        self.tw.new_project()
        self.tw.load_start()

    def _do_open_cb(self, widget):
        ''' Callback for open project. '''
        self.tw.load_file_from_chooser(True)

    def _do_save_cb(self, widget):
        ''' Callback for save project. '''
        self.tw.save_file(self._ta_file)

    def _do_save_as_cb(self, widget):
        ''' Callback for save-as project. '''
        self._save_as()

    def _save_as(self):
        ''' Save as is called from callback and quit '''
        self.tw.save_file_name = self._ta_file
        self.tw.save_file()

    def _save_changes(self):
        ''' Save changes to current project '''
        self.tw.save_file_name = self._ta_file
        self.tw.save_file(self.tw._loaded_project)

    def _do_save_picture_cb(self, widget):
        ''' Callback for save canvas. '''
        self.tw.save_as_image()

    def _do_save_logo_cb(self, widget):
        ''' Callback for save project to Logo. '''
        logocode = save_logo(self.tw)
        if len(logocode) == 0:
            return
        save_type = '.lg'
        filename, self.tw.load_save_folder = get_save_name(
            save_type, self.tw.load_save_folder, 'logosession')
        if isinstance(filename, unicode):
            filename = filename.encode('ascii', 'replace')
        if filename is not None:
            f = file(filename, 'w')
            f.write(logocode)
            f.close()

    def _do_resize_cb(self, widget, factor):
        ''' Callback to resize blocks. '''
        if factor == -1:
            self.tw.block_scale = 2.0
        else:
            self.tw.block_scale *= factor
        self.tw.resize_blocks()

    def _do_cartesian_cb(self, button):
        ''' Callback to display/hide Cartesian coordinate overlay. '''
        self.tw.set_cartesian(True)

    def _do_polar_cb(self, button):
        ''' Callback to display/hide Polar coordinate overlay. '''
        self.tw.set_polar(True)

    def _do_rescale_cb(self, button):
        ''' Callback to rescale coordinate space. '''
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

    def _do_toggle_hover_help_cb(self, button):
        ''' Toggle hover help on/off '''
        self.tw.no_help = not self.tw.no_help
        if self.tw.no_help:
            self._do_hover_help_off_cb(None)
        else:
            self._do_hover_help_on_cb(None)

    def _do_hover_help_on_cb(self, button):
        ''' Turn hover help on '''
        self.tw.no_help = False
        self.hover.set_active(True)
        self.client.set_int(self._HOVER_HELP, 0)

    def _do_hover_help_off_cb(self, button):
        ''' Turn hover help off '''
        self.tw.no_help = True
        self.tw.last_label = None
        self.tw.status_spr.hide()
        self.hover.set_active(False)
        self.client.set_int(self._HOVER_HELP, 1)

    def _do_palette_cb(self, widget):
        ''' Callback to show/hide palette of blocks. '''
        self.tw.show_palette(self.current_palette)
        self.current_palette += 1
        if self.current_palette == len(self.tw.palettes):
            self.current_palette = 0

    def _do_hide_palette_cb(self, widget):
        ''' Hide the palette of blocks. '''
        self.tw.hide_palette()

    def _do_hideshow_cb(self, widget):
        ''' Hide/show the blocks. '''
        self.tw.hideshow_button()

    def _do_eraser_cb(self, widget):
        ''' Callback for eraser button. '''
        self.tw.eraser_button()
        return

    def _do_run_cb(self, widget=None):
        ''' Callback for run button (rabbit). '''
        self.tw.lc.trace = 0
        self.tw.hideblocks()
        self.tw.display_coordinates(clear=True)
        self.tw.toolbar_shapes['stopiton'].set_layer(TAB_LAYER)
        self.tw.run_button(0, running_from_button_push=True)
        return

    def _do_step_cb(self, widget):
        ''' Callback for step button (turtle). '''
        self.tw.lc.trace = 1
        self.tw.run_button(3, running_from_button_push=True)
        return

    def _do_trace_cb(self, widget):
        ''' Callback for debug button (bug). '''
        self.tw.lc.trace = 1
        self.tw.run_button(9, running_from_button_push=True)
        return

    def _do_stop_cb(self, widget):
        ''' Callback for stop button. '''
        if self.tw.running_blocks:
            self.tw.toolbar_shapes['stopiton'].hide()
        if self.tw.hide:
            self.tw.showblocks()
        self.tw.stop_button()
        self.tw.display_coordinates()

    def _do_save_macro_cb(self, widget):
        ''' Callback for save stack button. '''
        self.tw.copying_blocks = False
        self.tw.deleting_blocks = False
        if self.tw.saving_blocks:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self.tw.saving_blocks = False
        else:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
            self.tw.saving_blocks = True

    def _do_delete_macro_cb(self, widget):
        ''' Callback for delete stack button. '''
        self.tw.copying_blocks = False
        self.tw.saving_blocks = False
        if self.tw.deleting_blocks:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self.tw.deleting_blocks = False
        else:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
            self.tw.deleting_blocks = True


    def restore_challenge(self):
        ''' Restore the current challange after a clear screen '''
        if self._custom_filepath is None:
            self._load_level()
        else:
            self._load_level(custom=True)

    def _load_level(self, custom=False):
        self.tw.canvas.clearscreen()
        if custom:
            self.tw.canvas.setxy(0, 0, pendown=False)
            self.tw.lc.insert_image(center=True,
                                    filepath=self._custom_filepath,
                                    resize=True, offset=False)
        else:
            self.tw.canvas.setxy(int(-gtk.gdk.screen_width() / 2), 0,
                                 pendown=False)
            self.tw.lc.insert_image(center=False, resize=False,
                                    filepath=os.path.join(
                    self._get_execution_dir(), 'images',
                    'mexico-tortuga.png'))
            # Slight offset to account for stroke width
            if self._level + 1 in self.offsets:
                xoffset = self.offsets[self._level + 1][0]
                yoffset = self.offsets[self._level + 1][1]
            else:
                xoffset = 0
                yoffset = 0
            self.tw.canvas.setxy(-2.5 + xoffset, -2.5 + yoffset, pendown=False)
            self.tw.lc.insert_image(center=False,
                                    filepath=os.path.join(
                    self._get_execution_dir(), 'challenges',
                    self._levels[self._level] + '.svg'), resize=False,
                                    offset=True)
        self.tw.canvas.setxy(0, 0, pendown=False)

    def _do_level_cb(self, widget, level):
        ''' Callback to resize blocks. '''
        self._level = level
        self._load_level()

    def _get_levels(self):
        ''' Look for level files in lessons directory. '''
        levels = glob.glob(os.path.join(self._get_execution_dir(),
                                        'challenges', '*.svg'))

        level_files = []
        for i in range(len(levels)):
            level_files.append('mexico-%d' % (i+1))

        self.offsets = {}
        offset_fd = open(os.path.join(self._get_execution_dir(), 'challenges',
                                      'offsets'))
        for line in offset_fd:
            try:
                idx, offsets = line.strip('\n').split(':')
                xoffset, yoffset = offsets.split(',')
                self.offsets[int(idx)] = (int(xoffset), int(yoffset))
            except ValueError:
                pass
        offset_fd.close()
        return level_files

    def _do_copy_cb(self, button):
        ''' Callback for copy button. '''
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        if self.tw.copying_blocks:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self.tw.copying_blocks = False
        else:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
            self.tw.copying_blocks = True

    def _do_paste_cb(self, button):
        ''' Callback for paste button. '''
        self.tw.copying_blocks = False
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
        clipBoard = gtk.Clipboard()
        text = clipBoard.wait_for_text()
        if text is not None:
            if self.tw.selected_blk is not None and \
               self.tw.selected_blk.name == 'string':
                self.tw.text_buffer.set_text(
                    self.tw.text_buffer.get_text() + text)
                self.tw.text_entry.set_buffer(self.tw.text_buffer)
                self.tw.selected_blk.resize()
            elif text[0:2] == '[[':
                self.tw.process_data(data_from_string(text),
                                     self.tw.paste_offset)
                self.tw.paste_offset += 20

    def _do_about_cb(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name(_(self.name))
        about.set_version(self.version)
        about.set_comments(_(self.summary))
        about.set_website(self.website)
        about.set_logo(
            gtk.gdk.pixbuf_new_from_file(
                'activity/' + self.icon_name + '.svg'))
        about.run()
        about.destroy()

    def _window_event(self, event, data):
        ''' Callback for resize event. '''
        data_file = open('.turtleartrc', 'w')
        data_file.write(str(data.x) + '\n')
        data_file.write(str(data.y) + '\n')
        data_file.write(str(data.width) + '\n')
        data_file.write(str(data.height) + '\n')

    def nick_changed(self, nick):
        ''' TODO: Rename default turtle in dictionary '''
        pass

    def color_changed(self, colors):
        ''' Reskin turtle with collaboration colors '''
        turtle = self.tw.turtles.get_turtle(self.tw.default_turtle_name)
        try:
            turtle.colors = colors.split(',')
        except:
            turtle.colors = DEFAULT_TURTLE_COLORS
        turtle.custom_shapes = True  # Force regeneration of shapes
        turtle.reset_shapes()
        turtle.show()

    def _get_execution_dir(self):
        ''' From whence is the program being executed? '''
        dirname = os.path.dirname(__file__)
        if dirname == '':
            if os.path.exists(os.path.join('~', 'Activities',
                                           'TurtleArt.activity')):
                return os.path.join('~', 'Activities', 'TurtleArt.activity')
            elif os.path.exists(self._INSTALL_PATH):
                return self._INSTALL_PATH
            elif os.path.exists(self._ALTERNATIVE_INSTALL_PATH):
                return self._ALTERNATIVE_INSTALL_PATH
            else:
                return os.path.abspath('.')
        else:
            return os.path.abspath(dirname)


if __name__ == '__main__':
    TurtleMain()
