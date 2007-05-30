import ta

from sugar.activity import activity

class TurtleArtActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.connect('destroy', self._cleanup_cb)
        
        self.gamename = 'turtleart'
        self.set_title("TurtleArt")
        
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)
        ta.init(self, activity.get_bundle_path())
        

    def _cleanup_cb(self, data=None):
        return

    def _focus_in(self, event, data=None):
        return

    def _focus_out(self, event, data=None):
        return
