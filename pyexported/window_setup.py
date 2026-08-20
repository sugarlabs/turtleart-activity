#!/usr/bin/env python3

import os
import sys
from gettext import gettext as _

import cairo
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.tautils import get_screen_dimensions


# search sys.path for a dir containing TurtleArt/tawindow.py
# path to the toplevel directory of the TA installation
_TA_INSTALLATION_PATH = None
for path in sys.path:
    try:
        entries = os.listdir(path)
    except OSError:
        continue
    if "TurtleArt" in entries:
        new_path = os.path.join(path, "TurtleArt")
        try:
            new_entries = os.listdir(new_path)
        except OSError:
            continue
        if "tawindow.py" in new_entries:
            _TA_INSTALLATION_PATH = path
            break
# if the TA installation path was not found, notify the user and refuse to run
if _TA_INSTALLATION_PATH is None:
    print(_("The path to the TurtleArt installation must be listed in the "
            "environment variable PYTHONPATH."))
    exit(1)



class DummyTurtleMain(object):

    """Keep the main objects for running a dummy TA window in one place.
    (Try not to have to inherit from turtleblocks.TurtleMain.)
    """

    def __init__(self, win, name="exported project"):
        """Create a scrolled window to contain the turtle canvas.
        win -- a GTK toplevel window
        """
        self.win = win
        self.set_title = self.win.set_title

        # setup a scrolled container for the canvas
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sw = Gtk.ScrolledWindow()
        self.sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.canvas = Gtk.DrawingArea()
        
        screen_width, screen_height = get_screen_dimensions()
        width = screen_width * 2
        height = screen_height * 2
        
        self.canvas.set_size_request(width, height)
        self.sw.set_child(self.canvas)
        self.sw.set_vexpand(True)
        self.sw.set_hexpand(True)
        self.vbox.append(self.sw)
        self.win.set_child(self.vbox)

        # copied from turtleblocks.TurtleMain._build_window()
        self.turtle_canvas = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            max(1024, width), max(768, height))

        # instantiate an instance of a dummy sub-class that supports only
        # the stuff TurtleGraphics needs
        # TODO don't hardcode running_sugar
        share_path = _TA_INSTALLATION_PATH
        self.tw = TurtleArtWindow(self.canvas, _TA_INSTALLATION_PATH,
                                  share_path,
                                  turtle_canvas=self.turtle_canvas,
                                  parent=self, running_sugar=False,
                                  running_turtleart=False)

        self.name = name

    def _quit_ta(self, widget=None, e=None):
        """Quit all plugins and the main window. No need to prompt the user
        to save their work, since they cannot change anything.
        """
        for plugin in list(self.tw.turtleart_plugins.values()):
            if hasattr(plugin, 'quit'):
                plugin.quit()
        sys.exit(0)


def get_tw():
    """ Create a GTK window and instantiate a DummyTurtleMain instance. Return
    the TurtleArtWindow object that holds the turtles and the canvas.
    """
    # copied from turtleblocks.TurtleMain._setup_gtk()

    win = Gtk.Window()
    gui = DummyTurtleMain(win=win, name=sys.argv[0])
    win.maximize()
    win.set_title(str(gui.name))
    win.present()
    win.connect('close-request', gui._quit_ta)

    return gui.tw
