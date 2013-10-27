#!/usr/bin/env python

# TODO remove unused imports and global variables
import pygtk
pygtk.require('2.0')
import gtk
import gobject

from gettext import gettext as _

try:
    import gst
    _GST_AVAILABLE = True
except ImportError:
    # Turtle Art should not fail if gst is not available
    _GST_AVAILABLE = False

import os
import subprocess
import errno
from sys import argv

from random import uniform
from math import atan2, pi
DEGTOR = 2 * pi / 360

import locale

from TurtleArt.taconstants import (HORIZONTAL_PALETTE, VERTICAL_PALETTE, BLOCK_SCALE,
                         MEDIA_SHAPES, STATUS_SHAPES, OVERLAY_SHAPES,
                         TOOLBAR_SHAPES, TAB_LAYER, RETURN, OVERLAY_LAYER,
                         CATEGORY_LAYER, BLOCKS_WITH_SKIN, ICON_SIZE,
                         PALETTE_SCALE, PALETTE_WIDTH, SKIN_PATHS, MACROS,
                         TOP_LAYER, BLOCK_LAYER, OLD_NAMES, DEFAULT_TURTLE,
                         TURTLE_LAYER, EXPANDABLE, NO_IMPORT, TEMPLATES,
                         PYTHON_SKIN, PALETTE_HEIGHT, STATUS_LAYER, OLD_DOCK,
                         EXPANDABLE_ARGS, XO1, XO15, XO175, XO30, XO4, TITLEXY,
                         CONTENT_ARGS, CONSTANTS, EXPAND_SKIN, PROTO_LAYER,
                         EXPANDABLE_FLOW, SUFFIX)
from TurtleArt.talogo import (LogoCode, primitive_dictionary, logoerror)
from TurtleArt.tacanvas import TurtleGraphics
from TurtleArt.tablock import (Blocks, Block)
from TurtleArt.taturtle import (Turtles, Turtle)
from TurtleArt.tautils import (magnitude, get_load_name, get_save_name, data_from_file,
                     data_to_file, round_int, get_id, get_pixbuf_from_journal,
                     movie_media_type, audio_media_type, image_media_type,
                     save_picture, calc_image_size, get_path, hide_button_hit,
                     show_button_hit, arithmetic_check, xy,
                     find_block_to_run, find_top_block, journal_check,
                     find_group, find_blk_below, data_to_string,
                     find_start_stack, get_hardware, debug_output,
                     error_output, convert, find_bot_block,
                     restore_clamp, collapse_clamp, data_from_string,
                     increment_name, get_screen_dpi)
from TurtleArt.tasprite_factory import (SVG, svg_str_to_pixbuf, svg_from_file)
from TurtleArt.sprites import (Sprites, Sprite)

if _GST_AVAILABLE:
    from TurtleArt.tagplay import stop_media

import cairo

from TurtleArt.tawindow import TurtleArtWindow


# path to the toplevel directory of the TA installation
_TA_INSTALLATION_PATH = None
# search the PYTHONPATH for a dir containing TurtleArt/tawindow.py
PYTHONPATH = os.environ["PYTHONPATH"]
for path in PYTHONPATH.split(":"):
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
    print _("The path to the TurtleArt installation must be listed in the "
            "environment variable PYTHONPATH.")
    exit(1)

_PLUGIN_SUBPATH = 'plugins'
_MACROS_SUBPATH = 'macros'



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
        self.vbox = gtk.VBox(False, 0)
        self.vbox.show()
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.show()
        self.canvas = gtk.DrawingArea()
        width = gtk.gdk.screen_width() * 2
        height = gtk.gdk.screen_height() * 2
        self.canvas.set_size_request(width, height)
        self.sw.add_with_viewport(self.canvas)
        self.canvas.show()
        self.vbox.pack_end(self.sw, True, True)
        self.win.add(self.vbox)
        self.win.show_all()
        
        # exported code is always in interactive mode
        interactive = True
        
        # copied from turtleblocks.TurtleMain._build_window()
        if interactive:
            gdk_win = self.canvas.get_window()
            cr = gdk_win.cairo_create()
            surface = cr.get_target()
        else:
            img_surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                             1024, 768)
            cr = cairo.Context(img_surface)
            surface = cr.get_target()
        self.turtle_canvas = surface.create_similar(
            cairo.CONTENT_COLOR, max(1024, gtk.gdk.screen_width() * 2),
            max(768, gtk.gdk.screen_height() * 2))
        
        
        
        # instantiate an instance of a dummy sub-class that supports only 
        # the stuff TurtleGraphics needs
        # TODO don't hardcode running_sugar
        self.tw = TurtleArtWindow(self.canvas, _TA_INSTALLATION_PATH,
                                  turtle_canvas=self.turtle_canvas,
                                  parent=self, running_sugar=False, 
                                  running_turtleart=False)
        
        self.name = name


    def _quit_ta(self, widget=None, e=None):
        """Quit all plugins and the main window. No need to prompt the user 
        to save their work, since they cannot change anything.
        """
        for plugin in self.tw.turtleart_plugins:
            if hasattr(plugin, 'quit'):
                plugin.quit()
        gtk.main_quit()
        exit()



def get_tw():
    """ Create a GTK window and instantiate a DummyTurtleMain instance. Return
    the TurtleArtWindow object that holds the turtles and the canvas.
    """
    # copied from turtleblocks.TurtleMain._setup_gtk()
    
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    gui = DummyTurtleMain(win=win, name=argv[0])
    # TODO re-enable this code (after giving gui the right attributes)
    # win.set_default_size(gui.width, gui.height)
    # win.move(gui.x, gui.y)
    win.maximize()
    # win.set_title('%s %s' % (gui.name, str(gui.version)))
    # if os.path.exists(os.path.join(gui._execdirname, gui._ICON_SUBPATH)):
    #     win.set_icon_from_file(os.path.join(gui._execdirname,
    #                                         gui._ICON_SUBPATH))
    win.show()
    win.connect('delete_event', gui._quit_ta)
    
    return gui.tw


