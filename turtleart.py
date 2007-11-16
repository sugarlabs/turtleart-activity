import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import os.path

from tawindow import *

def main():
    win1 = gtk.Window(gtk.WINDOW_TOPLEVEL)
    twNew(win1, os.path.abspath('.'))
    win1.connect("destroy", lambda w: gtk.main_quit())
#    win2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
#    twNew(win2, os.path.abspath('.'))
    gtk.main()
    return 0

if __name__ == "__main__":
    main()


