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
import tarfile
import tempfile
import subprocess

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
from TurtleArt.tautils import (data_from_string, get_load_name,
                               get_path, get_save_name)
from TurtleArt.tapalette import default_values
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.taexportlogo import save_logo
from TurtleArt.taexportpython import save_python
from TurtleArt.taprimitive import PyExportError
from TurtleArt.taplugin import (load_a_plugin, cancel_plugin_install,
                                complete_plugin_install)

from util.menubuilder import MenuBuilder


class TurtleMain():
    ''' Launch Turtle Art in GNOME (from outside of Sugar). '''
    _INSTALL_PATH = '/usr/share/sugar/activities/TurtleArt.activity'
    _ALTERNATIVE_INSTALL_PATH = \
        '/usr/local/share/sugar/activities/TurtleArt.activity'
    _ICON_SUBPATH = 'images/turtle.png'
    _GNOME_PLUGIN_SUBPATH = 'gnome_plugins'
    _HOVER_HELP = '/desktop/sugar/activities/turtleart/hoverhelp'
    _ORIENTATION = '/desktop/sugar/activities/turtleart/orientation'
    _COORDINATE_SCALE = '/desktop/sugar/activities/turtleart/coordinatescale'

    def __init__(self):
        self._setting_gconf_overrides = False
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
        self.bundle_path = self._abspath
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
        self._selected_challenge = None
        self._challenge_window = None
        self.has_toolbarbox = False

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
            self._create_store()
        else:
            self.win.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            gobject.idle_add(self._project_loader, self._ta_file)
        self._set_gconf_overrides()
        self._draw_cartoon()
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
            cairo.CONTENT_COLOR,
            # max(1024, gtk.gdk.screen_width() * 2),
            # max(768, gtk.gdk.screen_height() * 2))
            gtk.gdk.screen_width() * 2,
            gtk.gdk.screen_height() * 2)
        self.tw = TurtleArtWindow(self.canvas, self._execdirname,
                                  turtle_canvas=self.turtle_canvas,
                                  activity=self, running_sugar=False)
        self.tw.save_folder = self._abspath  # os.path.expanduser('~')

        if hasattr(self, 'client'):
            if self.client.get_int(self._HOVER_HELP) == 1:
                self.hover.set_active(False)
                self._do_hover_help_off_cb(None)
            if not self.client.get_int(self._COORDINATE_SCALE) in [0, 1]:
                self.tw.coord_scale = 1
            else:
                self.tw.coord_scale = 0
            if self.client.get_int(self._ORIENTATION) == 1:
                self.tw.orientation = 1

    def _set_gconf_overrides(self):
        if self.tw.coord_scale == 0:
            self.tw.coord_scale = 1
        else:
            self._do_rescale_cb(None)
        if self.tw.coord_scale != 1:
            self._setting_gconf_overrides = True
            self.coords.set_active(True)
            self._setting_gconf_overrides = False

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

    def restore_cursor(self):
        ''' No longer copying or sharing, so restore standard cursor. '''
        self.tw.copying_blocks = False
        self.tw.sharing_blocks = False
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        if hasattr(self, 'get_window'):
            if hasattr(self.get_window(), 'get_cursor'):
                self.get_window().set_cursor(self._old_cursor)
            else:
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

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
        MenuBuilder.make_menu_item(menu, _('Show challenges'),
                                   self._create_store)
        MenuBuilder.make_menu_item(menu, _('Open'), self._do_open_cb)
        MenuBuilder.make_menu_item(menu, _('Add project'), self._do_load_cb)
        MenuBuilder.make_menu_item(menu, _('Load plugin'),
                                   self._do_load_plugin_cb)
        MenuBuilder.make_menu_item(menu, _('Save'), self._do_save_cb)
        MenuBuilder.make_menu_item(menu, _('Save as'), self._do_save_as_cb)
        MenuBuilder.make_menu_item(menu, _('Save as image'),
                                   self._do_save_picture_cb)
        MenuBuilder.make_menu_item(menu, _('Save as Logo'),
                                   self._do_save_logo_cb)
        MenuBuilder.make_menu_item(menu, _('Save as Python'),
                                   self._do_save_python_cb)
        MenuBuilder.make_menu_item(menu, _('Quit'), self._quit_ta)
        activity_menu = MenuBuilder.make_sub_menu(menu, _('File'))

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Cartesian coordinates'),
                                   self._do_cartesian_cb)
        MenuBuilder.make_menu_item(menu, _('Polar coordinates'),
                                   self._do_polar_cb)
        self.coords = MenuBuilder.make_checkmenu_item(
            menu, _('Rescale coordinates'),
            self._do_rescale_cb, status=False)
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

        self._custom_filepath = None
        '''
        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Show challenges'),
                                   self._create_store)
        challenges_menu = MenuBuilder.make_sub_menu(menu, _('Challenges'))
        '''

        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('About...'), self._do_about_cb)
        help_menu = MenuBuilder.make_sub_menu(menu, _('Help'))

        menu_bar = gtk.MenuBar()
        menu_bar.append(activity_menu)
        menu_bar.append(edit_menu)
        menu_bar.append(view_menu)
        menu_bar.append(tool_menu)
        menu_bar.append(turtle_menu)
        # menu_bar.append(challenges_menu)

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
            resp = self._show_save_dialog(e == None)
            if resp == gtk.RESPONSE_YES:
                if self.tw.is_new_project():
                    self._save_as()
                else:
                    if self.tw.project_has_changed():
                        self._save_changes()
            elif resp == gtk.RESPONSE_CANCEL:
                return

        if hasattr(self, 'client'):
            self.client.set_int(self._ORIENTATION, self.tw.orientation)

        for plugin in self.tw.turtleart_plugins:
            if hasattr(plugin, 'quit'):
                plugin.quit()
        gtk.main_quit()
        exit()

    def _show_save_dialog(self, add_cancel=False):
        ''' Dialog for save project '''
        dlg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_INFO,
                                buttons=gtk.BUTTONS_YES_NO,
                                message_format=_('You have unsaved work. \
Would you like to save before quitting?'))
        if add_cancel:
            dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.set_title(_('Save project?'))
        dlg.set_property('skip-taskbar-hint', False)

        resp = dlg.run()
        dlg.destroy()
        return resp

    def _reload_plugin_alert(self, tmp_dir, tmp_path, plugin_path, plugin_name,
                             file_info):
        print "Already installed"
        title = _('Plugin %s already installed') % plugin_name
        msg = _('Do you want to reinstall %s?') % plugin_name
        dlg = gtk.MessageDialog(parent=None, type=gtk.MESSAGE_INFO,
                                buttons=gtk.BUTTONS_YES_NO,
                                message_format=title)
        dlg.format_secondary_text(msg)
        dlg.set_title(title)
        dlg.set_property('skip-taskbar-hint', False)

        resp = dlg.run()
        dlg.destroy()

        if resp is gtk.RESPONSE_OK:
            complete_plugin_install(tmp_dir, tmp_path, plugin_path,
                                    plugin_name, file_info)
        elif resp is gtk.RESPONSE_CANCEL:
            cancel_plugin_install(tmp_dir)

    def _do_new_cb(self, widget):
        ''' Callback for new project. '''
        self.tw.new_project()
        self.tw.load_start()

    def _do_open_cb(self, widget):
        ''' Callback for open project. '''
        self.tw.load_file_from_chooser(True)

    def _do_load_cb(self, widget):
        ''' Callback for load project (add to current project). '''
        self.tw.load_file_from_chooser(False)

    def _do_load_plugin_cb(self, widget):
        self.tw.load_save_folder = self._get_execution_dir()
        file_path, loaddir = get_load_name('.tar.gz', self.tw.load_save_folder)
        if file_path is None:
            return
        try:
            # Copy to tmp file since some systems had trouble
            # with gunzip directly from datastore
            datapath = get_path(None, 'instance')
            if not os.path.exists(datapath):
                os.makedirs(datapath)
            tmpfile = os.path.join(datapath, 'tmpfile.tar.gz')
            subprocess.call(['cp', file_path, tmpfile])
            status = subprocess.call(['gunzip', tmpfile])
            if status == 0:
                tar_fd = tarfile.open(tmpfile[:-3], 'r')
            else:
                tar_fd = tarfile.open(tmpfile, 'r')
        except:
            tar_fd = tarfile.open(file_path, 'r')

        tmp_dir = tempfile.mkdtemp()

        try:
            tar_fd.extractall(tmp_dir)
            load_a_plugin(self, tmp_dir)
            self.restore_cursor()
        except:
            self.restore_cursor()
        finally:
            tar_fd.close()
            # Remove tmpfile.tar
            subprocess.call(['rm',
                             os.path.join(datapath, 'tmpfile.tar')])

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
        self.tw.load_save_folder = self._get_execution_dir()
        filename, self.tw.load_save_folder = get_save_name(
            save_type, self.tw.load_save_folder, 'logosession')
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        if filename is not None:
            f = file(filename, 'w')
            f.write(logocode)
            f.close()

    def _do_save_python_cb(self, widget):
        ''' Callback for saving the project as Python code. '''
        # catch PyExportError and display a user-friendly message instead
        try:
            pythoncode = save_python(self.tw)
        except PyExportError as pyee:
            if pyee.block is not None:
                pyee.block.highlight()
            self.tw.showlabel('status', str(pyee))
            print pyee
            return
        if not pythoncode:
            return
        # use name of TA project if it has been saved already
        default_name = self.tw.save_file_name
        if default_name is None:
            default_name = _("myproject")
        elif default_name.endswith(".ta") or default_name.endswith(".tb"):
            default_name = default_name[:-3]
        save_type = '.py'
        self.tw.load_save_folder = self._get_execution_dir()
        filename, self.tw.load_save_folder = get_save_name(
            save_type, self.tw.load_save_folder, default_name)
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        if filename is not None:
            f = file(filename, 'w')
            f.write(pythoncode)
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
        if self._setting_gconf_overrides:
            return
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height / 40
            self.tw.update_overlay_position()
            if self.tw.cartesian is True:
                self.tw.overlay_shapes['Cartesian_labeled'].hide()
                self.tw.overlay_shapes['Cartesian'].set_layer(OVERLAY_LAYER)
            default_values['forward'] = [10]
            default_values['back'] = [10]
            default_values['arc'] = [90, 10]
            default_values['setpensize'] = [1]
            self.tw.turtles.get_active_turtle().set_pen_size(1)
        else:
            self.tw.coord_scale = 1
            if self.tw.cartesian is True:
                self.tw.overlay_shapes['Cartesian'].hide()
                self.tw.overlay_shapes['Cartesian_labeled'].set_layer(
                    OVERLAY_LAYER)
            default_values['forward'] = [100]
            default_values['back'] = [100]
            default_values['arc'] = [90, 100]
            default_values['setpensize'] = [5]
            self.tw.turtles.get_active_turtle().set_pen_size(5)
        if hasattr(self, 'client'):
            self.client.set_int(self._COORDINATE_SCALE,
                                int(self.tw.coord_scale))

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
        if hasattr(self, 'client'):
            self.client.set_int(self._HOVER_HELP, 0)

    def _do_hover_help_off_cb(self, button):
        ''' Turn hover help off '''
        if self.tw.no_help:  # Debounce
            return
        self.tw.no_help = True
        self.tw.last_label = None
        if self.tw.status_spr is not None:
            self.tw.status_spr.hide()
        self.hover.set_active(False)
        if hasattr(self, 'client'):
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
        self.restore_state()
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

    def restore_state(self):
        ''' Restore the current challange after a clear screen '''
        if self._custom_filepath is None:
            self._load_level()
        else:
            self._load_level(custom=True)

    def _draw_cartoon(self):
        pos = self.tw.turtles.get_active_turtle().get_xy()
        self.tw.turtles.get_active_turtle().set_xy(
            int(-gtk.gdk.screen_width() / 2), 0, pendown=False)
        self.tw.lc.insert_image(center=False, resize=False,
                                filepath=os.path.join(
                self._get_execution_dir(), 'images', 'turtle-a.png'))
        self.tw.turtles.get_active_turtle().set_xy(pos[0], pos[1],
                                                   pendown=False)

    def _load_level(self, custom=False):
        self.tw.canvas.clearscreen()
        self._draw_cartoon()
        if custom:
            self.tw.turtles.get_active_turtle().set_xy(0, 0, pendown=False)
            self.tw.lc.insert_image(center=True,
                                    filepath=self._custom_filepath,
                                    resize=True, offset=False)
        else:
            basename = os.path.basename(self._selected_challenge)[:-4]
            if basename in self.offsets:
                offset = [self.offsets[basename][0] - 3,
                          self.offsets[basename][1] - 33]
                scale = self.offsets[basename][2]
            else:
                offset = [-3, -33]
                scale = 33
            save_scale = self.tw.lc.scale
            self.tw.turtles.get_active_turtle().set_xy(offset[0],
                                                       offset[1],
                                                       pendown=False)

            self.tw.lc.scale = scale
            self.tw.lc.insert_image(center=False,
                                    filepath=self._selected_challenge,
                                    resize=False,
                                    offset=True)
            self.tw.lc.scale = save_scale
        self.tw.turtles.get_active_turtle().set_xy(0, 0, pendown=False)

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

    def hide_store(self, widget=None):
        if self._challenge_window is not None:
            self._challenge_box.hide()

    def _create_store(self, widget=None):
        if self._challenge_window is None:
            self._challenge_box = gtk.EventBox()
            self._challenge_window = gtk.ScrolledWindow()
            self._challenge_window.set_policy(gtk.POLICY_NEVER,
                                              gtk.POLICY_AUTOMATIC)
            width = gtk.gdk.screen_width() / 2
            height = gtk.gdk.screen_height() / 2
            self._challenge_window.set_size_request(width, height)
            self._challenge_window.show()

            store = gtk.ListStore(gtk.gdk.Pixbuf, str)

            icon_view = gtk.IconView()
            icon_view.set_model(store)
            icon_view.set_selection_mode(gtk.SELECTION_SINGLE)
            icon_view.connect('selection-changed', self._challenge_selected,
                              store)
            icon_view.set_pixbuf_column(0)
            icon_view.grab_focus()
            self._challenge_window.add_with_viewport(icon_view)
            icon_view.show()
            self._fill_challenges_list(store)

            width = gtk.gdk.screen_width() / 4
            height = gtk.gdk.screen_height() / 4

            self._challenge_box.add(self._challenge_window)
            self.fixed.put(self._challenge_box, width, height)

            self.offsets = {}
            offset_fd = open(os.path.join(self._get_execution_dir(),
                                          'challenges',
                                          'offsets'))
            for line in offset_fd:
                try:
                    idx, offsets = line.strip('\n').split(':')
                    xoffset, yoffset, scale = offsets.split(',')
                    self.offsets['confusion-' + idx] = (int(xoffset),
                                                        int(yoffset),
                                                        int(scale))
                except ValueError:
                    pass
            offset_fd.close()

        self._challenge_window.show()
        self._challenge_box.show()

    def _get_selected_path(self, widget, store):
        try:
            iter_ = store.get_iter(widget.get_selected_items()[0])
            image_path = store.get(iter_, 1)[0]

            return image_path, iter_
        except:
            return None

    def _challenge_selected(self, widget, store):
        selected = self._get_selected_path(widget, store)

        if selected is None:
            self._selected_challenge = None
            self._challenge_window.hide()
            return

        image_path, _iter = selected
        iter_ = store.get_iter(widget.get_selected_items()[0])
        image_path = store.get(iter_, 1)[0]

        self._selected_challenge = image_path
        self._challenge_window.hide()
        self._load_level()

    def _fill_challenges_list(self, store):
        '''
        Append images from the artwork_paths to the store.
        '''
        for filepath in self._scan_for_challenges():
            pixbuf = None
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                filepath, 100, 100)
            store.append([pixbuf, filepath])

    def _scan_for_challenges(self):
        file_list = list(glob.glob(os.path.join(self._get_execution_dir(),
                                           'samples', 'thumbnails', '*.svg')))
        file_list.sort()
        return file_list


if __name__ == '__main__':
    TurtleMain()
