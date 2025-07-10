"""
 tagplay.py
 refactored based on Jukebox Activity
 Copyright (C) 2007 Andy Wingo <wingo@pobox.com>
 Copyright (C) 2007 Red Hat, Inc.
 Copyright (C) 2008-2010 Kushal Das <kushal@fedoraproject.org>
 Copyright (C) 2010 Walter Bender
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import os

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gtk
from gi.repository import Gst
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkX11, GstVideo  # noqa: F401
GObject.threads_init()
Gst.init(None)


from .tautils import error_output, debug_output


def play_audio_from_file(lc, file_path):
    """ Called from Show block of audio media """
    if lc.gplay is not None and lc.gplay.player is not None:
        if lc.gplay.player.playing:
            lc.gplay.player.stop()
        if lc.gplay.bin is not None:
            lc.gplay.bin.destroy()

    lc.gplay = Gplay(lc, lc.tw.canvas.width, lc.tw.canvas.height, 4, 3)
    lc.gplay.start(file_path)


def play_movie_from_file(lc, filepath, x, y, w, h):
    """ Called from Show block of video media """
    if lc.gplay is not None and lc.gplay.player is not None:
        if lc.gplay.player.playing:
            lc.gplay.player.stop()
        if lc.gplay.bin is not None:
            lc.gplay.bin.destroy()

    lc.gplay = Gplay(lc, x, y, w, h)
    lc.gplay.start(filepath)


def stop_media(lc):
    """ Called from Clean block and toolbar Stop button """
    if lc.gplay is None:
        return False

    if lc.gplay.player is not None:
        lc.gplay.player.stop()
    if lc.gplay.bin is not None:
        lc.gplay.bin.destroy()

    lc.gplay = None


def pause_media(lc):
    """ From pause media block """
    if lc.gplay is None:
        return False

    if lc.gplay.player is not None:
        lc.gplay.player.pause()


def play_media(lc):
    """ From play media block """
    if lc.gplay is None:
        return False

    if lc.gplay.player is not None:
        lc.gplay.player.play()


def media_playing(lc):
    if lc.gplay is None:
        return False
    return lc.gplay.player.is_playing()


class Gplay():
    UPDATE_INTERVAL = 500

    def __init__(self, lc, x, y, w, h):
        self.running_sugar = lc.tw.running_sugar
        self.player = None
        self.uri = None
        self.playlist = []
        self.jobjectlist = []
        self.playpath = None
        self.only_audio = False
        self.got_stream_info = False
        self.currentplaying = 0

        self.bin = Gtk.Window()

        self.videowidget = VideoWidget()
        self.bin.add(self.videowidget)
        self.bin.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.bin.set_decorated(False)
        if self.running_sugar:
            self.bin.set_transient_for(lc.tw.activity)

        self.bin.move(x, y)
        self.bin.resize(w, h)
        self.bin.show_all()

        self._want_document = True

    def _player_eos_cb(self, widget):
        debug_output('end of stream', self.running_sugar)
        # Make sure player is stopped after EOS
        self.player.stop()

    def _player_error_cb(self, widget, message, detail):
        self.player.stop()
        self.player.set_uri(None)
        error_output('Error: %s - %s' % (message, detail),
                     self.running_sugar)

    def _player_stream_info_cb(self, widget, stream_info):
        if not len(stream_info) or self.got_stream_info:
            return

        GST_STREAM_TYPE_VIDEO = 2

        only_audio = True
        for item in stream_info:
            if item.props.type == GST_STREAM_TYPE_VIDEO:
                only_audio = False
        self.only_audio = only_audio
        self.got_stream_info = True

    def start(self, file_path=None):
        self._want_document = False
        self.playpath = os.path.dirname(file_path)
        if not file_path:
            return False
        self.playlist.append('file://' + os.path.abspath(file_path))
        if not self.player:
            # Lazy init the player so that videowidget is realized
            # and has a valid widget allocation.
            self.player = GstPlayer(self.videowidget, self.running_sugar)
            self.player.connect('eos', self._player_eos_cb)
            self.player.connect('error', self._player_error_cb)
            self.player.connect('stream-info', self._player_stream_info_cb)

        try:
            if not self.currentplaying:
                debug_output('Playing: %s' % (self.playlist[0]),
                             self.running_sugar)
                self.player.set_uri(self.playlist[0])
                self.currentplaying = 0
                self.play_toggled()
        except Exception as e:
            error_output('Error playing %s: %s' % (self.playlist[0], e),
                         self.running_sugar)
        return False

    def play_toggled(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            if self.player.error:
                pass
            else:
                self.player.play()


class GstPlayer(GObject.GObject):
    __gsignals__ = {
        'error': (GObject.SignalFlags.RUN_FIRST, None, [str, str]),
        'eos': (GObject.SignalFlags.RUN_FIRST, None, []),
        'stream-info': (GObject.SignalFlags.RUN_FIRST, None, [object])}

    def __init__(self, videowidget, running_sugar):
        GObject.GObject.__init__(self)

        self.running_sugar = running_sugar
        self.playing = False
        self.error = False

        self.player = Gst.ElementFactory.make('playbin', 'player')

        videowidget.realize()
        self.videowidget = videowidget
        self.videowidget_xid = videowidget.get_property('window').get_xid()
        self._init_video_sink()

        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('sync-message::element', self.on_sync_message)
        bus.connect('message', self.on_message)

    def set_uri(self, uri):
        self.player.set_property('uri', uri)

    def on_sync_message(self, bus, message):
        if message.get_structure() is None:
            return
        if message.get_structure().get_name() == 'prepare-window-handle':
            self.videowidget.set_sink(message.src, self.videowidget_xid)
            message.src.set_property('force-aspect-ratio', True)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            error_output('Error: %s - %s' % (err, debug),
                         self.running_sugar)
            self.error = True
            self.emit('eos')
            self.playing = False
            self.emit('error', str(err), str(debug))
        elif t == Gst.MessageType.EOS:
            self.emit('eos')
            self.playing = False
        elif t == Gst.MessageType.STATE_CHANGED:
            old, new, pen = message.parse_state_changed()
            if old == Gst.State.READY and new == Gst.State.PAUSED and \
               hasattr(self.player.props, 'stream_info_value_array'):
                self.emit('stream-info',
                          self.player.props.stream_info_value_array)

    def _init_video_sink(self):
        self.bin = Gst.Bin.new()
        videoscale = Gst.ElementFactory.make('videoscale', None)
        self.bin.add(videoscale)
        pad = videoscale.get_static_pad('sink')
        ghostpad = Gst.GhostPad.new('sink', pad)
        self.bin.add_pad(ghostpad)
        videoscale.set_property('method', 0)

        caps_string = 'video/x-raw, '
        r = self.videowidget.get_allocation()
        if r.width > 500 and r.height > 500:
            # Sigh... xvimagesink on the XOs will scale the video to fit
            # but ximagesink in Xephyr does not.  So we live with unscaled
            # video in Xephyr so that the XO can work right.
            w = 480
            h = float(w) / float(float(r.width) / float(r.height))
            caps_string += 'width=%d, height=%d' % (w, h)
        else:
            caps_string += 'width=480, height=360'
        caps = Gst.Caps.from_string(caps_string)
        self.filter = Gst.ElementFactory.make('capsfilter', 'filter')
        self.bin.add(self.filter)
        self.filter.set_property('caps', caps)

        conv = Gst.ElementFactory.make('videoconvert', 'conv')
        self.bin.add(conv)
        videosink = Gst.ElementFactory.make('autovideosink')
        self.bin.add(videosink)

        videoscale.link(self.filter)
        self.filter.link(conv)
        conv.link(videosink)

        self.player.set_property('video-sink', self.bin)

    def pause(self):
        self.player.set_state(Gst.State.PAUSED)
        self.playing = False
        # debug_output('pausing player', self.running_sugar)

    def play(self):
        self.player.set_state(Gst.State.PLAYING)
        self.playing = True
        self.error = False
        # debug_output('playing player', self.running_sugar)

    def stop(self):
        self.player.set_state(Gst.State.NULL)
        self.playing = False
        # debug_output('stopped player', self.running_sugar)

    def get_state(self, timeout=1):
        return self.player.get_state(timeout=timeout)

    def is_playing(self):
        return self.playing


class VideoWidget(Gtk.DrawingArea):

    def __init__(self):
        GObject.GObject.__init__(self)
        self.set_events(Gdk.EventMask.EXPOSURE_MASK)
        self.imagesink = None
        self.set_double_buffered(True)
        self.set_app_paintable(True)

    def do_expose_event(self, event):
        if self.imagesink:
            self.imagesink.expose()
            return False
        else:
            return True

    def set_sink(self, sink, xid):
        self.imagesink = sink
        self.imagesink.set_window_handle(xid)
