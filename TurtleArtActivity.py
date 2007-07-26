import ta
import pygtk
pygtk.require('2.0')
import gtk

from sugar.activity import activity

class TurtleArtActivity(activity.Activity):
    def __init__(self, handle):
        super(TurtleArtActivity,self).__init__(handle)
        
        self.gamename = 'turtleart'
        self.set_title("TurtleArt")
        toolbar = activity.ActivityToolbar(self)
        toolbar.show()
        self.set_toolbox(toolbar)

        self.connect('destroy', self._cleanup_cb)
#        self.connect('focus_in_event', self._focus_in)
#        self.connect('focus_out_event', self._focus_out)
        
        canvas = gtk.EventBox()
        self.set_canvas(canvas)
        ta.init(canvas, activity.get_bundle_path(),self)
        

    def _cleanup_cb(self, data=None):
        return

    def _focus_in(self, event, data=None):
        return

    def _focus_out(self, event, data=None):
        return
