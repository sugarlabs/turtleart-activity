#Copyright (c) 2009, Walter Bender (on behalf of Sugar Labs)

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

"""
Video and audio playback

Based on code snippets from
http://wiki.sugarlabs.org/go/Development_Team/Almanac/GStreamer
"""
import gtk
import pygtk
pygtk.require('2.0')
import pygst
pygst.require('0.10')
import gst
import gst.interfaces
import gobject
gobject.threads_init()

try:
    from sugar.datastore import datastore
except ImportError:
    pass

class Gplay:

    def __init__(self):
        self.window = None
        self.playing = False

        self.player = gst.element_factory_make("playbin", "playbin")
        xis = gst.element_factory_make("xvimagesink", "xvimagesink")
        self.player.set_property("video-sink", xis)
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        self.SYNC_ID = bus.connect('sync-message::element', \
                                   self._onSyncMessageCb)

    def _onSyncMessageCb(self, bus, message):
        if message.structure is None:
            return True
        if message.structure.get_name() == 'prepare-xwindow-id':
            if self.window is None:
                return True
            self.window.set_sink(message.src)
            message.src.set_property('force-aspect-ratio', True)
            return True

    def setFile(self, path):
        uri = "file://" + str(path)
        if (self.player.get_property('uri') == uri):
            self.seek(gst.SECOND*0)
            return

        self.player.set_state(gst.STATE_READY)
        self.player.set_property('uri', uri)
        ext = uri[len(uri)-3:]
        if (ext == "jpg"):
            self.pause()
        else:
            self.play()

    def queryPosition(self):
        #"Returns a (position, duration) tuple"
        try:
            position, format = self.player.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self.player.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE
        return (position, duration)

    def seek(self, time):
        event = gst.event_new_seek(1.0,\
                                   gst.FORMAT_TIME,\
                                   gst.SEEK_FLAG_FLUSH|gst.SEEK_FLAG_ACCURATE,\
                                   gst.SEEK_TYPE_SET,\
                                   time,\
                                   gst.SEEK_TYPE_NONE, 0)
        res = self.player.send_event(event)
        if res:
            self.player.set_new_stream_time(0L)

    def pause(self):
        self.playing = False
        self.player.set_state(gst.STATE_PAUSED)

    def play(self):
        self.playing = True
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.playing = False
        self.player.set_state(gst.STATE_NULL)
        # self.nextMovie()

    def get_state(self, timeout=1):
        return self.player.get_state(timeout=timeout)

    def is_playing(self):
        return self.playing

class PlayVideoWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.imagesink = None
        self.unset_flags(gtk.DOUBLE_BUFFERED)
        self.set_flags(gtk.APP_PAINTABLE)

    def set_sink(self, sink):
        if (self.imagesink != None):
            assert self.window.xid
            self.imagesink = None
            del self.imagesink

        self.imagesink = sink
        if self.window is not None:
            self.imagesink.set_xwindow_id(self.window.xid)

def play_audio(lc, filepath):
    print "loading audio id: " + filepath
    if lc.gplay == None:
        lc.gplay = Gplay()
    lc.gplay.setFile("file:///" + filepath)

def play_movie_from_file(lc, filepath, x, y, w, h):
    if lc.gplay == None:
        lc.gplay = Gplay()
    # wait for current movie to stop playing
    if lc.gplay.is_playing:
        print "already playing..."
    lc.gplay.setFile("file:///" + filepath)
    if lc.gplay.window == None:
        gplayWin = PlayVideoWindow()
    lc.gplay.window = gplayWin
    gplayWin.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
    gplayWin.set_decorated(False)
    if lc.tw.running_sugar:
        gplayWin.set_transient_for(lc.tw.activity)
    # y position is too high for some reason (toolbox?) adding offset
    gplayWin.move(x, y+108)
    gplayWin.resize(w, h)
    gplayWin.show_all()


def stop_media(lc):
    if lc.gplay == None:
        return
    lc.gplay.stop()
    if lc.gplay.window != None:
        # We need to destroy the video window
        # print dir(lc.gplay.window)
        lc.gplay.window.destroy()
        lc.gplay = None

