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


import logging
import os

import pygtk
pygtk.require('2.0')

import gobject
gobject.threads_init()

import pygst
import gst
import gst.interfaces
import gtk

import urllib


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
    if lc.gplay == None:
        return

    if lc.gplay.player is not None:
        lc.gplay.player.stop()
    if lc.gplay.bin != None:
        lc.gplay.bin.destroy()

    lc.gplay = None


def media_playing(lc):
    if lc.gplay == None:
        return False
    return lc.gplay.player.is_playing()


class Gplay():
    UPDATE_INTERVAL = 500

    def __init__(self, lc, x, y, w, h):

        self.player = None
        self.uri = None
        self.playlist = []
        self.jobjectlist = []
        self.playpath = None
        self.only_audio = False
        self.got_stream_info = False
        self.currentplaying = 0

        self.bin = gtk.Window()

        self.videowidget = VideoWidget()
        self.bin.add(self.videowidget)
        self.bin.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        self.bin.set_decorated(False)
        if lc.tw.running_sugar:
            self.bin.set_transient_for(lc.tw.activity)

        self.bin.move(x, y + 108)
        self.bin.resize(w, h)
        self.bin.show_all()

        self._want_document = True

    def _player_eos_cb(self, widget):
        logging.debug('end of stream')

    def _player_error_cb(self, widget, message, detail):
        self.player.stop()
        self.player.set_uri(None)
        logging.debug('Error: %s - %s' % (message, detail))

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

    def start(self, uri=None):
        self._want_document = False
        self.playpath = os.path.dirname(uri)
        if not uri:
            return False
        self.playlist.append('file://' + urllib.quote(os.path.abspath(uri)))
        if not self.player:
            # lazy init the player so that videowidget is realized
            # and has a valid widget allocation
            self.player = GstPlayer(self.videowidget)
            self.player.connect('eos', self._player_eos_cb)
            self.player.connect('error', self._player_error_cb)
            self.player.connect('stream-info', self._player_stream_info_cb)

        try:
            if not self.currentplaying:
                logging.info('Playing: ' + self.playlist[0])
                self.player.set_uri(self.playlist[0])
                self.currentplaying = 0
                self.play_toggled()
                self.show_all()
            else:
                pass
        except:
            pass
        return False

    def play_toggled(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            if self.player.error:
                pass
            else:
                self.player.play()


class GstPlayer(gobject.GObject):
    __gsignals__ = {
        'error': (gobject.SIGNAL_RUN_FIRST, None, [str, str]),
        'eos': (gobject.SIGNAL_RUN_FIRST, None, []),
        'stream-info': (gobject.SIGNAL_RUN_FIRST, None, [object])}

    def __init__(self, videowidget):
        gobject.GObject.__init__(self)

        self.playing = False
        self.error = False

        self.player = gst.element_factory_make('playbin', 'player')

        self.videowidget = videowidget
        self._init_video_sink()

        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('sync-message::element', self.on_sync_message)
        bus.connect('message', self.on_message)

    def set_uri(self, uri):
        self.player.set_property('uri', uri)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        if message.structure.get_name() == 'prepare-xwindow-id':
            self.videowidget.set_sink(message.src)
            message.src.set_property('force-aspect-ratio', True)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            logging.debug('Error: %s - %s' % (err, debug))
            self.error = True
            self.emit('eos')
            self.playing = False
            self.emit('error', str(err), str(debug))
        elif t == gst.MESSAGE_EOS:
            self.emit('eos')
            self.playing = False
        elif t == gst.MESSAGE_STATE_CHANGED:
            old, new, pen = message.parse_state_changed()
            if old == gst.STATE_READY and new == gst.STATE_PAUSED:
                self.emit('stream-info',
                          self.player.props.stream_info_value_array)

    def _init_video_sink(self):
        self.bin = gst.Bin()
        videoscale = gst.element_factory_make('videoscale')
        self.bin.add(videoscale)
        pad = videoscale.get_pad('sink')
        ghostpad = gst.GhostPad('sink', pad)
        self.bin.add_pad(ghostpad)
        videoscale.set_property('method', 0)

        caps_string = 'video/x-raw-yuv, '
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

        caps = gst.Caps(caps_string)
        self.filter = gst.element_factory_make('capsfilter', 'filter')
        self.bin.add(self.filter)
        self.filter.set_property('caps', caps)

        conv = gst.element_factory_make('ffmpegcolorspace', 'conv')
        self.bin.add(conv)
        videosink = gst.element_factory_make('autovideosink')
        self.bin.add(videosink)
        gst.element_link_many(videoscale, self.filter, conv, videosink)
        self.player.set_property('video-sink', self.bin)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.playing = False
        logging.debug('pausing player')

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)
        self.playing = True
        self.error = False
        logging.debug('playing player')

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.playing = False
        logging.debug('stopped player')

    def get_state(self, timeout=1):
        return self.player.get_state(timeout=timeout)

    def is_playing(self):
        return self.playing


class VideoWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_events(gtk.gdk.EXPOSURE_MASK)
        self.imagesink = None
        self.unset_flags(gtk.DOUBLE_BUFFERED)
        self.set_flags(gtk.APP_PAINTABLE)

    def do_expose_event(self, event):
        if self.imagesink:
            self.imagesink.expose()
            return False
        else:
            return True

    def set_sink(self, sink):
        assert self.window.xid
        self.imagesink = sink
        self.imagesink.set_xwindow_id(self.window.xid)
