#!/usr/bin/env python3
# Copyright (c) 2007-8, Playful Invention Company
# Copyright (c) 2008-14, Walter Bender
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import cairo
import getopt
import sys
import os
import os.path
import io
import errno
import configparser
import tarfile
import tempfile
import subprocess

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GdkPixbuf
from gi.repository import Gio

try:
    # Try to use XDG Base Directory standard for config files.
    import xdg.BaseDirectory

    CONFIG_HOME = os.path.join(xdg.BaseDirectory.xdg_config_home, "turtleart")
except ImportError:
    # Default to `.config` per the spec.
    CONFIG_HOME = os.path.expanduser(os.path.join("~", ".config", "turtleart"))

argv = sys.argv[:]  # Workaround for import behavior of gst in tagplay
sys.argv[1:] = []  # Execution of import gst cannot see '--help' or '-h'

import gettext
from gettext import gettext as _

from TurtleArt.taconstants import (
    OVERLAY_LAYER,
    DEFAULT_TURTLE_COLORS,
    TAB_LAYER,
    SUFFIX,
    TMP_SVG_PATH,
    TMP_ODP_PATH,
    PASTE_OFFSET,
)
from TurtleArt.tautils import (
    data_from_string,
    get_load_name,
    get_path,
    get_save_name,
    is_writeable,
)
from TurtleArt.tapalette import default_values
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.taexportlogo import save_logo
from TurtleArt.taexportpython import save_python
from TurtleArt.taprimitive import PyExportError
from TurtleArt.taplugin import (
    load_a_plugin,
    cancel_plugin_install,
    complete_plugin_install,
)

from TurtleArt.util import menubuilder
from TurtleArt.util.menubuilder import (
    make_menu_item,
    make_sub_menu,
    make_checkmenu_item,
)

from TurtleArt.tautils import get_screen_dimensions
from TurtleArt.util.helpbutton import TutorialWindows


class TurtleMain:

    """ Launch Turtle Art in GNOME (from outside of Sugar). """

    _INSTALL_PATH = "/usr/share/sugar/activities/TurtleArt.activity"
    _ALTERNATIVE_INSTALL_PATH = "/usr/local/share/sugar/activities/TurtleArt.activity"
    _ICON_SUBPATH = "images/turtle.png"
    _GNOME_PLUGIN_SUBPATH = "gnome_plugins"
    _GIO_SETTINGS = "org.laptop.TurtleArtActivity"
    _HOVER_HELP = "hover-help"
    _ORIENTATION = "palette-orientation"
    _COORDINATE_SCALE = "coordinate-scale"
    _PLUGINS_LIST = "plugins"

    def __init__(self, lib_path, share_path):
        self._gio_settings_overrides = False

        self._lib_path = lib_path
        self._share_path = share_path
        self._abspath = os.path.abspath(".")

        file_activity_info = configparser.ConfigParser()
        activity_info_path = os.path.join(share_path, "activity/activity.info")
        file_activity_info.read(activity_info_path)
        bundle_id = file_activity_info.get("Activity", "bundle_id")
        self.version = file_activity_info.get("Activity", "activity_version")
        self.name = file_activity_info.get("Activity", "name")
        self.summary = file_activity_info.get("Activity", "summary")
        self.website = file_activity_info.get("Activity", "url")
        self.icon_name = file_activity_info.get("Activity", "icon")

        path = os.path.join(share_path, "locale")
        if os.path.isdir(path):
            gettext.bindtextdomain(bundle_id, path)
        gettext.textdomain(bundle_id)
        global _
        _ = gettext.gettext
        self._HELP_MSG = (
            "turtleblocks.py: "
            + _("usage is")
            + """
 \tturtleblocks.py
 \tturtleblocks.py project.tb
 \tturtleblocks.py --output_png project.tb
 \tturtleblocks.py -o project
 \tturtleblocks.py --run project.tb
 \tturtleblocks.py -r project"""
        )
        self._init_vars()
        self._parse_command_line()
        self._ensure_sugar_paths()
        self._gnome_plugins = []
        self._selected_sample = None
        self._sample_window = None

        if self._output_png:
            # Outputing to file, so no need for a canvas
            self.canvas = None
            self._get_gio_settings()
            self._build_window(interactive=False)
            self._draw_and_quit()
        else:
            self._read_initial_pos()
            self._init_gnome_plugins()
            self._get_gio_settings()
            self._setup_gtk()
            self._build_window()
            self._run_gnome_plugins()
            self._start_gtk()

    def _get_local_settings(self, activity_root):
        """return an activity-specific Gio.Settings"""
        # create compiled schema file if missing from activity root
        compiled = os.path.join(activity_root, "gschemas.compiled")
        if not os.access(compiled, os.R_OK):
            # create schemas directory if missing
            path = os.path.join(get_path(None, "data"), "schemas")
            if not os.access(path, os.F_OK):
                os.makedirs(path)

            # create compiled schema file if missing
            compiled = os.path.join(path, "gschemas.compiled")
            if not os.access(compiled, os.R_OK):
                src = "%s.gschema.xml" % self._GIO_SETTINGS
                lines = open(os.path.join(activity_root, src), "r").readlines()
                open(os.path.join(path, src), "w").writelines(lines)
                os.system("glib-compile-schemas %s" % path)
                os.remove(os.path.join(path, src))

            schemas_path = path
        else:
            schemas_path = activity_root

        # create a local Gio.Settings based on the compiled schema
        source = Gio.SettingsSchemaSource.new_from_directory(schemas_path, None, True)
        schema = source.lookup(self._GIO_SETTINGS, True)
        _settings = Gio.Settings.new_full(schema, None, None)
        return _settings

    def _get_gio_settings(self):
        self._settings = self._get_local_settings(self._share_path)

    def get_config_home(self):
        return CONFIG_HOME

    def _get_gnome_plugin_home(self):
        """ Use plugin directory associated with execution path. """
        if os.path.exists(os.path.join(self._lib_path, self._GNOME_PLUGIN_SUBPATH)):
            return os.path.join(self._lib_path, self._GNOME_PLUGIN_SUBPATH)
        else:
            return None

    def _get_plugin_candidates(self, path):
        """ Look for plugin files in plugin directory. """
        plugin_files = []
        if path is not None:
            candidates = os.listdir(path)
            for c in candidates:
                if c[-10:] == "_plugin.py" and c[0] != "#" and c[0] != ".":
                    plugin_files.append(c.split(".")[0])
        return plugin_files

    def _init_gnome_plugins(self):
        """ Try launching any plugins we may have found. """
        for p in self._get_plugin_candidates(self._get_gnome_plugin_home()):
            P = p.capitalize()
            f = (
                "def f(self): from gnome_plugins.%s import %s; \
return %s(self)"
                % (p, P, P)
            )
            plugin = {}
            try:
                exec(f, globals(), plugin)
                self._gnome_plugins.append(list(plugin.values())[0](self))
            except ImportError as e:
                print("failed to import %s: %s" % (P, str(e)))
            except ValueError as e:
                print("failed to import %s: %s" % (P, str(e)))

    def _run_gnome_plugins(self):
        """ Tell the plugin about the TurtleWindow instance. """
        for p in self._gnome_plugins:
            p.set_tw(self.tw)

    def _mkdir_p(self, path):
        """Create a directory in a fashion similar to `mkdir -p`."""
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    def _makepath(self, path):
        """ Make a path if it doesn't previously exist """
        dpath = os.path.normpath(os.path.dirname(path))
        if not os.path.exists(dpath):
            os.makedirs(dpath)

    def _start_gtk(self):
        """ Get a main window set up. """
        self.canvas.connect("resize", self.tw.update_overlay_position)
        self.tw.parent = self.win
        self.init_complete = True
        if self._ta_file is None:
            self.tw.load_start()
        else:
            self.win.set_cursor(Gdk.Cursor.new_from_name("wait"))
            GLib.idle_add(self._project_loader, self._ta_file)
        self._set_gio_settings_overrides()
        self.loop = GLib.MainLoop()
        self.loop.run()

    def _project_loader(self, file_name):
        self.tw.load_start(self._ta_file)
        self.tw.lc.trace = 0
        if self._run_on_launch:
            self._do_run_cb()
        self.win.set_cursor(Gdk.Cursor.new_from_name("default"))

    def _draw_and_quit(self):
        """Non-interactive mode: run the project, save it to a file
        and quit."""
        self.tw.load_start(self._ta_file)
        self.tw.lc.trace = 0
        self.tw.run_button(0, running_from_button_push=True)
        self.tw.save_as_image(self._ta_file)

    def _build_window(self, interactive=True):
        """ Initialize the TurtleWindow instance. """
        screen_w, screen_h = get_screen_dimensions()
        self.turtle_canvas = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, screen_w * 2, screen_h * 2
        )

        # Make sure the autosave directory is writeable
        if is_writeable(self._share_path):
            self._autosavedirname = self._share_path
        else:
            self._autosavedirname = os.path.expanduser("~")
        self.tw = TurtleArtWindow(
            self.canvas,
            self._lib_path,
            self._share_path,
            turtle_canvas=self.turtle_canvas,
            activity=self,
            running_sugar=False,
        )
        self.tw.save_folder = self._abspath  # os.path.expanduser('~')

        if interactive:
            if self._settings.get_int(self._HOVER_HELP) == 1:
                self.tw.no_help = True
                self.hover.set_state(GLib.Variant.new_boolean(False))
                self._do_hover_help_off_cb()
            if not self._settings.get_int(self._COORDINATE_SCALE) in [0, 1]:
                self.tw.coord_scale = 1
            else:
                self.tw.coord_scale = 0
            if self._settings.get_int(self._ORIENTATION) == 1:
                self.tw.orientation = 1
        else:
            self.tw.coord_scale = 1

    def _set_gio_settings_overrides(self):
        if self.tw.coord_scale == 0:
            self.tw.coord_scale = 1
        else:
            self._do_rescale_cb(None)
        if self.tw.coord_scale != 1:
            self._gio_settings_overrides = True
            self.coords.set_state(GLib.Variant.new_boolean(True))
            self._gio_settings_overrides = False

    def _init_vars(self):
        """If we are invoked to start a project from Gnome, we should make
        sure our current directory is TA's source dir."""
        self._ta_file = None
        self._output_png = False
        self._run_on_launch = False
        self.current_palette = 0
        self.scale = 2.0
        self.tw = None
        self.init_complete = False

    def _parse_command_line(self):
        """ Try to make sense of the command-line arguments. """
        try:
            opts, args = getopt.getopt(argv[1:], "hor", ["help", "output_png", "run"])
        except getopt.GetoptError as err:
            print(str(err))
            print(self._HELP_MSG)
            sys.exit(2)
        self._run_on_launch = False
        for o, a in opts:
            if o in ("-h", "--help"):
                print(self._HELP_MSG)
                sys.exit()
            if o in ("-o", "--output_png"):
                self._output_png = True
            elif o in ("-r", "--run"):
                self._run_on_launch = True
            else:
                assert False, _("No option action:") + " " + o
        if args:
            self._ta_file = args[0]

        if len(args) > 1 or self._output_png and self._ta_file is None:
            print(self._HELP_MSG)
            sys.exit()

        if self._ta_file is not None:
            if not self._ta_file.endswith(SUFFIX):
                self._ta_file += ".tb"
            if not os.path.exists(self._ta_file):
                self._ta_file = os.path.join(self._abspath, self._ta_file)
                if not os.path.exists(self._ta_file):
                    assert False, "%s: %s" % (self._ta_file, _("File not found"))

    def _ensure_sugar_paths(self):
        """ Make sure Sugar paths are present. """
        tapath = os.path.join(
            os.environ["HOME"], ".sugar", "default", "org.laptop.TurtleArtActivity"
        )
        list(
            map(
                self._makepath,
                (os.path.join(tapath, "data/"), os.path.join(tapath, "instance/")),
            )
        )

    def _read_initial_pos(self):
        """ Read saved configuration. """
        try:
            data_file = open(os.path.join(CONFIG_HOME, "turtleartrc"), "r")
        except IOError:
            # Opening the config file failed
            # We'll assume it needs to be created
            try:
                self._mkdir_p(CONFIG_HOME)
                data_file = open(os.path.join(CONFIG_HOME, "turtleartrc"), "a+")
            except IOError as e:
                # We can't write to the configuration file, use
                # a faux file that will persist for the length of
                # the session.
                print(_("Configuration directory not writable: %s") % (e))
            data_file = io.StringIO()
            data_file.write(str(50) + "\n")
            data_file.write(str(50) + "\n")
            data_file.write(str(800) + "\n")
            data_file.write(str(550) + "\n")
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

    def restore_cursor(self):
        """ No longer copying or sharing, so restore standard cursor. """
        self.tw.copying_blocks = False
        self.tw.sharing_blocks = False
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        if hasattr(self, "win") and self.win:
            self.win.set_cursor(Gdk.Cursor.new_from_name("default"))

    def _setup_gtk(self):
        """ Set up a scrolled window in which to run Turtle Blocks. """
        win = Gtk.Window()
        self.win = win
        win.set_default_size(self.width, self.height)
        win.maximize()
        win.set_title("%s %s" % (self.name, str(self.version)))
        win.show()
        win.connect("close-request", self._quit_ta)

        # Create a scrolled window to contain the turtle canvas. We
        # add a Fixed container in order to position text Entry widgets
        # on top of string and number blocks.

        self.overlay = Gtk.Overlay()
        self.fixed = Gtk.Fixed()
        self.fixed.set_can_target(False)
        screen_width, screen_height = get_screen_dimensions()

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.menu_bar = self._get_menu_bar()
        self.vbox.append(self.menu_bar)
        
        # Calculate actual menu height instead of hardcoding
        _, nat_height, _, _ = self.menu_bar.measure(Gtk.Orientation.VERTICAL, -1)
        self.menu_height = nat_height if nat_height > 0 else 34

        self.sw = Gtk.ScrolledWindow()
        self.sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        canvas = Gtk.DrawingArea()
        width = screen_width * 2
        height = screen_height * 2
        canvas.set_size_request(width, height)
        self.sw.set_child(canvas)
        self.sw.set_vexpand(True)
        self.vbox.append(self.sw)
        
        self.overlay.set_child(self.vbox)
        self.overlay.add_overlay(self.fixed)

        win.set_child(self.overlay)
        self.canvas = canvas

    def _get_menu_bar(self):
        """ Instead of Sugar toolbars, use GNOME menus. """
        from gi.repository import Gio
        
        menu_bar_model = Gio.Menu()
        
        file_menu = make_sub_menu(menu_bar_model, _("File"))
        make_menu_item(file_menu, _("New"), self._do_new_cb)
        make_menu_item(file_menu, _("Show sample projects"), self._create_store)
        make_menu_item(file_menu, _("Open"), self._do_open_cb)
        make_menu_item(file_menu, _("Add project"), self._do_load_cb)
        make_menu_item(file_menu, _("Load plugin"), self._do_load_plugin_cb)
        make_menu_item(file_menu, _("Save"), self._do_save_cb)
        make_menu_item(file_menu, _("Save as"), self._do_save_as_cb)

        export_submenu = make_sub_menu(file_menu, _("Export as"))
        make_menu_item(export_submenu, _("image"), self._do_save_picture_cb)
        make_menu_item(export_submenu, _("image (blocks)"), self._do_save_blocks_image_cb)
        make_menu_item(export_submenu, _("SVG"), self._do_save_svg_cb)
        make_menu_item(export_submenu, _("icon"), self._do_save_as_icon_cb)
        make_menu_item(export_submenu, _("ODP"), self._do_save_as_odp_cb)
        make_menu_item(export_submenu, _("Logo"), self._do_save_logo_cb)
        make_menu_item(export_submenu, _("Python"), self._do_save_python_cb)
        make_menu_item(file_menu, _("Quit"), self._quit_ta)

        view_menu = make_sub_menu(menu_bar_model, _("View"))
        make_menu_item(view_menu, _("Cartesian coordinates"), self._do_cartesian_cb)
        make_menu_item(view_menu, _("Polar coordinates"), self._do_polar_cb)
        self.coords = make_checkmenu_item(
            view_menu, _("Rescale coordinates"), self._do_rescale_cb, status=False
        )
        make_menu_item(view_menu, _("Grow blocks"), self._do_resize_cb, 1.5)
        make_menu_item(view_menu, _("Shrink blocks"), self._do_resize_cb, 0.667)
        make_menu_item(view_menu, _("Reset block size"), self._do_resize_cb, -1)
        self.hover = make_checkmenu_item(
            view_menu, _("Turn on hover help"), self._do_toggle_hover_help_cb, status=True
        )

        edit_menu = make_sub_menu(menu_bar_model, _("Edit"))
        make_menu_item(edit_menu, _("Copy"), self._do_copy_cb)
        make_menu_item(edit_menu, _("Paste"), self._do_paste_cb)
        make_menu_item(edit_menu, _("Save stack"), self._do_save_macro_cb)
        make_menu_item(edit_menu, _("Delete stack"), self._do_delete_macro_cb)

        tool_menu = make_sub_menu(menu_bar_model, _("Tools"))
        make_menu_item(tool_menu, _("Show palette"), self._do_palette_cb)
        make_menu_item(tool_menu, _("Hide palette"), self._do_hide_palette_cb)
        make_menu_item(tool_menu, _("Show/hide blocks"), self._do_hideshow_cb)

        turtle_menu = make_sub_menu(menu_bar_model, _("Turtle"))
        make_menu_item(turtle_menu, _("Clean"), self._do_eraser_cb)
        make_menu_item(turtle_menu, _("Run"), self._do_run_cb)
        make_menu_item(turtle_menu, _("Step"), self._do_step_cb)
        make_menu_item(turtle_menu, _("Debug"), self._do_trace_cb)
        make_menu_item(turtle_menu, _("Stop"), self._do_stop_cb)

        self._plugin_menu = make_sub_menu(menu_bar_model, _("Plugins"))

        # Add menus for plugins
        for p in self._gnome_plugins:
            menu_item = p.get_menu()
            if menu_item is not None:
                menu_bar_model.append_section(None, menu_item)

        help_menu = make_sub_menu(menu_bar_model, _("Help"))
        make_menu_item(help_menu, _("About..."), self._do_about_cb)
        make_menu_item(help_menu, _("Tutorial"), self._do_tutorial_cb)

        if menubuilder.ACTION_GROUP is not None:
            self.win.insert_action_group("win", menubuilder.ACTION_GROUP)

        menu_bar = Gtk.PopoverMenuBar.new_from_model(menu_bar_model)
        return menu_bar

    def _quit_ta(self, widget=None, e=None):
        """ Save changes on exit """
        project_empty = self.tw.is_project_empty()
        if not project_empty:
            if hasattr(self, '_quit_in_progress') and self._quit_in_progress:
                return True
            self._quit_in_progress = True
            self._show_save_dialog(e is None, self._quit_dialog_response_cb)
            return True

        self._finish_quit_ta()

    def _quit_dialog_response_cb(self, dialog, response_id):
        dialog.destroy()
        if response_id == Gtk.ResponseType.YES:
            if self.tw.is_new_project():
                self._save_as()
            else:
                if self.tw.project_has_changed():
                    self._save_changes()
        elif response_id == Gtk.ResponseType.CANCEL or response_id == Gtk.ResponseType.DELETE_EVENT:
            self._quit_in_progress = False
            return

        self._finish_quit_ta()

    def _finish_quit_ta(self):
        if hasattr(self, "_settings"):
            self._settings.set_int(self._ORIENTATION, self.tw.orientation)

        for plugin in list(self.tw.turtleart_plugins.values()):
            if hasattr(plugin, "quit"):
                plugin.quit()

        # Clean up temporary files
        try:
            os.remove(TMP_SVG_PATH)
        except BaseException:
            pass
        try:
            os.remove(TMP_ODP_PATH)
        except BaseException:
            pass

        try:
            if hasattr(self, "win") and self.win:
                with open(os.path.join(CONFIG_HOME, "turtleartrc"), "w") as data_file:
                    data_file.write(str(self.x) + "\n")
                    data_file.write(str(self.y) + "\n")
                    data_file.write(str(self.win.get_width()) + "\n")
                    data_file.write(str(self.win.get_height()) + "\n")
        except IOError:
            pass

        try:
            if hasattr(self, 'loop'):
                self.loop.quit()
        except Exception:
            pass
        exit()

    def _show_save_dialog(self, add_cancel=False, callback=None):
        """ Dialog for save project """
        dlg = Gtk.MessageDialog(
            transient_for=self.win,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_(
                "You have unsaved work. \
Would you like to save before quitting?"
            ),
        )
        if add_cancel:
            dlg.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
        dlg.set_title(_("Save project?"))

        if callback:
            dlg.connect("response", callback)
            
        dlg.show()

    def _reload_plugin_alert(
        self, tmp_dir, tmp_path, plugin_path, plugin_name, file_info
    ):
        print("Already installed")
        title = _("Plugin %s already installed") % plugin_name
        msg = _("Do you want to reinstall %s?") % plugin_name
        dlg = Gtk.MessageDialog(
            transient_for=self.win,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text=title,
        )
        dlg.props.secondary_text = msg
        dlg.set_title(title)

        def on_response(dialog, response_id):
            dialog.destroy()
            if response_id == Gtk.ResponseType.YES:
                complete_plugin_install(
                    self, tmp_dir, tmp_path, plugin_path, plugin_name, file_info
                )
            else:
                cancel_plugin_install(tmp_dir)

        dlg.connect("response", on_response)
        dlg.show()

    def _do_tutorial_cb(self, widget):
        win = TutorialWindows(self.win)
        win.execute()

    def _do_new_cb(self, widget):
        """ Callback for new project. """
        self.tw.new_project()
        self.tw.load_start()

    def _do_open_cb(self, widget):
        """ Callback for open project. """
        self.tw.load_file_from_chooser(True)

    def _do_load_cb(self, widget):
        """ Callback for load project (add to current project). """
        self.tw.load_file_from_chooser(False)

    def _do_load_plugin_cb(self, widget):
        def on_plugin_selected(file_path, loaddir):
            if file_path is None:
                return
            try:
                # Copy to tmp file since some systems had trouble
                # with gunzip directly from datastore
                datapath = get_path(None, "instance")
                if not os.path.exists(datapath):
                    os.makedirs(datapath)
                tmpfile = os.path.join(datapath, "tmpfile.tar.gz")
                subprocess.call(["cp", file_path, tmpfile])
                status = subprocess.call(["gunzip", tmpfile])
                if status == 0:
                    tar_fd = tarfile.open(tmpfile[:-3], "r")
                else:
                    tar_fd = tarfile.open(tmpfile, "r")
            except BaseException:
                tar_fd = tarfile.open(file_path, "r")

            tmp_dir = tempfile.mkdtemp()

            try:
                tar_fd.extractall(tmp_dir)
                load_a_plugin(self, tmp_dir)
                self.restore_cursor()
            except BaseException:
                self.restore_cursor()
            finally:
                tar_fd.close()
                # Remove tmpfile.tar
                subprocess.call(["rm", os.path.join(datapath, "tmpfile.tar")])

        get_load_name(".tar.gz", callback=on_plugin_selected, window=self.win)

    def _do_save_cb(self, widget):
        """ Callback for save project. """
        self.tw.save_file(self._ta_file)

    def _do_save_as_cb(self, widget):
        """ Callback for save-as project. """
        self._save_as()

    def autosave(self):
        """ Autosave is called each type the run button is pressed """
        temp_load_save_folder = self.tw.load_save_folder
        temp_save_folder = self.tw.save_folder
        self.tw.load_save_folder = self._autosavedirname
        self.tw.save_folder = self._autosavedirname
        self.tw.save_file(file_name=os.path.join(self._autosavedirname, "autosave.tb"))
        self.tw.save_folder = temp_save_folder
        self.tw.load_save_folder = temp_load_save_folder

    def _save_as(self):
        """ Save as is called from callback and quit """
        self.tw.save_file_name = self._ta_file
        self.tw.save_file()

    def _save_changes(self):
        """ Save changes to current project """
        self.tw.save_file_name = self._ta_file
        self.tw.save_file(self.tw._loaded_project)

    def _do_save_blocks_image_cb(self, widget):
        """ Callback for save blocks as image. """
        self.tw.save_blocks_as_image()

    def _do_save_picture_cb(self, widget):
        """ Callback for save canvas. """
        self.tw.save_as_image()

    def _do_save_svg_cb(self, widget):
        """ Callback for save canvas as SVG. """
        self.tw.save_as_image(svg=True)

    def _do_save_as_icon_cb(self, widget):
        """ Callback for save canvas. """
        self.tw.write_svg_operation()
        self.tw.save_as_icon()

    def _do_save_as_odp_cb(self, widget):
        """ Callback for save canvas. """
        self.tw.save_as_odp()

    def _do_save_logo_cb(self, widget):
        """ Callback for save project to Logo. """
        logocode = save_logo(self.tw)
        if len(logocode) == 0:
            return
        save_type = ".lg"

        def _on_save_cb(filename, datapath):
            if filename is None:
                return
            self.tw.load_save_folder = datapath
            if isinstance(filename, str):
                filename = filename.encode("utf-8")
            with open(filename, "wb") as f:
                f.write(logocode.encode("utf-8") if isinstance(logocode, str) else logocode)

        get_save_name(
            save_type, None, "logosession", callback=_on_save_cb, window=self.tw.window
        )

    def _do_save_python_cb(self, widget):
        """ Callback for saving the project as Python code. """
        # catch PyExportError and display a user-friendly message instead
        try:
            pythoncode = save_python(self.tw)
        except PyExportError as pyee:
            if pyee.block is not None:
                pyee.block.highlight()
            self.tw.showlabel("status", str(pyee))
            print(pyee)
            return
        if not pythoncode:
            return
        # use name of TA project if it has been saved already
        default_name = self.tw.save_file_name
        if default_name is None:
            default_name = _("myproject")
        elif default_name.endswith(".ta") or default_name.endswith(".tb"):
            default_name = default_name[:-3]
        save_type = ".py"

        def _on_save_cb(filename, datapath):
            if filename is None:
                return
            self.tw.load_save_folder = datapath
            if isinstance(filename, str):
                filename = filename.encode("utf-8")
            with open(filename, "wb") as f:
                f.write(pythoncode.encode("utf-8") if isinstance(pythoncode, str) else pythoncode)

        get_save_name(
            save_type, None, default_name, callback=_on_save_cb, window=self.tw.window
        )

    def _do_resize_cb(self, widget, factor):
        """ Callback to resize blocks. """
        if factor == -1:
            self.tw.block_scale = 2.0
        else:
            self.tw.block_scale *= factor
        self.tw.resize_blocks()

    def _do_cartesian_cb(self, *args):
        """ Callback to display/hide Cartesian coordinate overlay. """
        if self.tw.cartesian:
            self.tw.set_cartesian(False)
        else:
            self.tw.set_cartesian(True)

    def _do_polar_cb(self, *args):
        """ Callback to display/hide Polar coordinate overlay. """
        if self.tw.polar:
            self.tw.set_polar(False)
        else:
            self.tw.set_polar(True)

    def _do_rescale_cb(self, button):
        """ Callback to rescale coordinate space. """
        if self._gio_settings_overrides:
            return
        if self.tw.coord_scale == 1:
            self.tw.coord_scale = self.tw.height / 40
            self.tw.update_overlay_position()
            if self.tw.cartesian is True:
                self.tw.overlay_shapes["Cartesian_labeled"].hide()
                self.tw.overlay_shapes["Cartesian"].set_layer(OVERLAY_LAYER)
            default_values["forward"] = [10]
            default_values["back"] = [10]
            default_values["arc"] = [90, 10]
            default_values["setpensize"] = [1]
            self.tw.turtles.get_active_turtle().set_pen_size(1)
        else:
            self.tw.coord_scale = 1
            if self.tw.cartesian is True:
                self.tw.overlay_shapes["Cartesian"].hide()
                self.tw.overlay_shapes["Cartesian_labeled"].set_layer(OVERLAY_LAYER)
            default_values["forward"] = [100]
            default_values["back"] = [100]
            default_values["arc"] = [90, 100]
            default_values["setpensize"] = [5]
            self.tw.turtles.get_active_turtle().set_pen_size(5)
        if hasattr(self, "_settings"):
            self._settings.set_int(self._COORDINATE_SCALE, int(self.tw.coord_scale))

        self.tw.recalculate_constants()

    def _do_toggle_hover_help_cb(self, button):
        """ Toggle hover help on/off """
        self.tw.no_help = not button.get_state().get_boolean()
        if self.tw.no_help:
            self._do_hover_help_off_cb()
        else:
            self._do_hover_help_on_cb()

    def _do_toggle_plugin_cb(self, button, name):
        if hasattr(self, "_settings"):
            plugins_list = self._settings.get_string(self._PLUGINS_LIST)
            plugins = plugins_list.split(",")
            if button.get_state().get_boolean():
                if name not in plugins:
                    plugins.append(name)
                    self._settings.set_string(self._PLUGINS_LIST, ",".join(plugins))
                label = _("Please restart %s in order to use the plugin.") % self.name
            else:
                if name in plugins:
                    plugins.remove(name)
                    self._settings.set_string(self._PLUGINS_LIST, ",".join(plugins))
                label = (
                    _("Please restart %s in order to unload the plugin.") % self.name
                )
        self.tw.showlabel("status", label)

    def _do_hover_help_on_cb(self):
        """ Turn hover help on """
        if hasattr(self, "_settings"):
            self._settings.set_int(self._HOVER_HELP, 0)

    def _do_hover_help_off_cb(self):
        """ Turn hover help off """
        self.tw.last_label = None
        if self.tw.status_spr is not None:
            self.tw.status_spr.hide()
        if hasattr(self, "_settings"):
            self._settings.set_int(self._HOVER_HELP, 1)

    def _do_palette_cb(self, widget):
        """ Callback to show/hide palette of blocks. """
        self.tw.show_palette(self.current_palette)

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

    def _do_run_cb(self, widget=None):
        """ Callback for run button (rabbit). """
        self.tw.lc.trace = 0
        self.tw.hideblocks()
        self.tw.display_coordinates(clear=True)
        self.tw.toolbar_shapes["stopiton"].set_layer(TAB_LAYER)
        self.tw.run_button(0, running_from_button_push=True)
        return

    def _do_step_cb(self, widget):
        """ Callback for step button (turtle). """
        self.tw.lc.trace = 1
        self.tw.run_button(3, running_from_button_push=True)
        return

    def _do_trace_cb(self, widget):
        """ Callback for debug button (bug). """
        self.tw.lc.trace = 1
        self.tw.run_button(9, running_from_button_push=True)
        return

    def _do_stop_cb(self, widget):
        """ Callback for stop button. """
        if self.tw.running_blocks:
            self.tw.toolbar_shapes["stopiton"].hide()
        if self.tw.hide:
            self.tw.showblocks()
        self.tw.stop_button()
        self.tw.display_coordinates()

    def _do_save_macro_cb(self, widget):
        """ Callback for save stack button. """
        self.tw.copying_blocks = False
        self.tw.deleting_blocks = False
        if self.tw.saving_blocks:
            self.win.set_cursor(Gdk.Cursor.new_from_name("default"))
            self.tw.saving_blocks = False
        else:
            self.win.set_cursor(Gdk.Cursor.new_from_name("pointer"))
            self.tw.saving_blocks = True

    def _do_delete_macro_cb(self, widget):
        """ Callback for delete stack button. """
        self.tw.copying_blocks = False
        self.tw.saving_blocks = False
        if self.tw.deleting_blocks:
            self.win.set_cursor(Gdk.Cursor.new_from_name("default"))
            self.tw.deleting_blocks = False
        else:
            self.win.set_cursor(Gdk.Cursor.new_from_name("pointer"))
            self.tw.deleting_blocks = True

    def _do_copy_cb(self, button):
        """ Callback for copy button. """
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        if self.tw.copying_blocks:
            self.win.set_cursor(Gdk.Cursor.new_from_name("default"))
            self.tw.copying_blocks = False
        else:
            self.win.set_cursor(Gdk.Cursor.new_from_name("pointer"))
            self.tw.copying_blocks = True

    def _do_paste_cb(self, button):
        """ Callback for paste button. """
        self.tw.copying_blocks = False
        self.tw.saving_blocks = False
        self.tw.deleting_blocks = False
        self.win.set_cursor(Gdk.Cursor.new_from_name("default"))
        display = Gdk.Display.get_default()
        clipboard = display.get_clipboard()
        
        def on_read_text(clipboard, result):
            try:
                text = clipboard.read_text_finish(result)
            except Exception:
                text = None
            if text is not None:
                if (
                    self.tw.selected_blk is not None
                    and self.tw.selected_blk.name == "string"
                    and text[0:2] != "[["
                ):  # Don't paste block data into a string
                    self.tw.paste_text_in_block_label(text)
                    self.tw.selected_blk.resize()
                else:
                    self.tw.process_data(data_from_string(text), self.tw.paste_offset)
                    self.tw.paste_offset += PASTE_OFFSET
        
        clipboard.read_text_async(None, on_read_text)

    def _do_about_cb(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name(_(self.name))
        about.set_version(self.version)
        about.set_comments(_(self.summary))
        about.set_website(self.website)
        logo_path = os.path.join(self._share_path, "activity", self.icon_name + ".svg")
        about.set_logo(Gdk.Texture.new_from_filename(logo_path))
        about.present()



    def nick_changed(self, nick):
        """ TODO: Rename default turtle in dictionary """
        pass

    def color_changed(self, colors):
        """ Reskin turtle with collaboration colors """
        turtle = self.tw.turtles.get_turtle(self.tw._default_turtle_name)
        try:
            turtle.colors = colors.split(",")
        except BaseException:
            turtle.colors = DEFAULT_TURTLE_COLORS
        turtle.custom_shapes = True  # Force regeneration of shapes
        turtle.reset_shapes()
        turtle.show()

    def _get_execution_dir(self):
        """ From whence is the program being executed? """
        dirname = os.path.dirname(__file__)
        if dirname == "":
            if os.path.exists(os.path.join("~", "Activities", "TurtleArt.activity")):
                return os.path.join("~", "Activities", "TurtleArt.activity")
            elif os.path.exists(self._INSTALL_PATH):
                return self._INSTALL_PATH
            elif os.path.exists(self._ALTERNATIVE_INSTALL_PATH):
                return self._ALTERNATIVE_INSTALL_PATH
            else:
                return os.path.abspath(".")
        else:
            return os.path.abspath(dirname)

    def restore_state(self):
        """ Anything that needs restoring after a clear screen can go here """
        pass

    def hide_store(self, widget=None):
        if self._sample_window is not None:
            self._sample_box.hide()

    def _create_store(self, widget=None):
        if self._sample_window is None:
            self._sample_box = Gtk.Box()
            self._sample_window = Gtk.ScrolledWindow()
            self._sample_window.set_policy(
                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
            )
            screen_width, screen_height = get_screen_dimensions()
            width = screen_width / 2
            height = screen_height / 2
            self._sample_window.set_size_request(width, height)
            self._sample_window.show()

            flowbox = Gtk.FlowBox()
            flowbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
            flowbox.connect("child-activated", self._sample_selected)
            self._sample_window.set_child(flowbox)
            flowbox.grab_focus()
            flowbox.show()
            self._fill_samples_list(flowbox)

            x = screen_width / 4
            y = screen_height / 4

            self._sample_box.append(self._sample_window)
            self.fixed.put(self._sample_box, x, y)
        self._sample_box.show()

    def _sample_selected(self, flowbox, child):
        if child is None:
            self._selected_sample = None
            self._sample_window.hide()
            return

        self._selected_sample = child.filepath
        self._sample_window.hide()

        self.win.set_cursor(Gdk.Cursor.new_from_name("wait"))
        GLib.idle_add(self._sample_loader)

    def _sample_loader(self):
        # Convert from thumbnail path to sample path
        basename = os.path.basename(self._selected_sample)[:-4]
        for suffix in [".ta", ".tb"]:
            file_path = os.path.join(self._share_path, "samples", basename + suffix)
            if os.path.exists(file_path):
                self.tw.load_files(file_path)
                break
        self.win.set_cursor(Gdk.Cursor.new_from_name("default"))

    def _fill_samples_list(self, flowbox):
        """
        Append images from the artwork_paths to the flowbox.
        """
        for filepath in self._scan_for_samples():
            pic = Gtk.Picture.new_for_filename(filepath)
            pic.set_size_request(100, 100)
            pic.set_can_shrink(True)
            
            child = Gtk.FlowBoxChild()
            child.set_child(pic)
            child.filepath = filepath
            flowbox.append(child)

    def _scan_for_samples(self):
        path = os.path.join(self._share_path, "samples", "thumbnails")
        samples = []
        for name in os.listdir(path):
            if name.endswith(".png"):
                samples.append(os.path.join(path, name))
        samples.sort()
        return samples
