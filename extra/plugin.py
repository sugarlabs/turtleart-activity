
import gobject

class Plugin(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)

    def get_menu(self):
        raise RuntimeError("You need to define get_menu for your plugin.")

