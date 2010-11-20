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
from gettext import gettext as _
import os

from sugar.activity import activity
from sugar.graphics.objectchooser import ObjectChooser
from sugar import mime

import pygtk
pygtk.require('2.0')

import sys

import gobject

import pygst
pygst.require('0.10')
import gst
import gst.interfaces
import gtk

import urllib
from ConfigParser import ConfigParser
cf = ConfigParser()


def play_audio(lc, file_path):
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
    return lc.gplay.player.playing


class Gplay():
    UPDATE_INTERVAL = 500

    def __init__(self, lc, x, y, w, h):

        self.update_id = -1
        self.changed_id = -1
        self.seek_timeout_id = -1
        self.player = None
        self.uri = None
        self.playlist = []
        self.jobjectlist = []
        self.playpath = None
        self.only_audio = False
        self.got_stream_info = False
        self.currentplaying = 0
        self.p_position = gst.CLOCK_TIME_NONE
        self.p_duration = gst.CLOCK_TIME_NONE

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
        pass

    def _player_error_cb(self, widget, message, detail):
        self.player.stop()
        self.player.set_uri(None)
        logging.debug('Error: %s - %s' % (message, detail))

    def _player_stream_info_cb(self, widget, stream_info):
        if not len(stream_info) or self.got_stream_info:
            return

        GST_STREAM_TYPE_UNKNOWN = 0
        GST_STREAM_TYPE_AUDIO = 1
        GST_STREAM_TYPE_VIDEO = 2
        GST_STREAM_TYPE_TEXT = 3

        only_audio = True
        for item in stream_info:
            if item.props.type == GST_STREAM_TYPE_VIDEO:
                only_audio = False
        self.only_audio = only_audio
        self.got_stream_info = True

    def read_file(self, file_path):
        self.uri = os.path.abspath(file_path)
        if os.path.islink(self.uri):
            self.uri = os.path.realpath(self.uri)
        gobject.idle_add(self.start, self.uri)

    def getplaylist(self, links):
        result = []
        for x in links:
            if x.startswith('http://'):
                result.append(x)
            elif x.startswith('#'):
                continue
            else:
                result.append('file://' + \
                                  urllib.quote(os.path.join(self.playpath, x)))
        return result

    def start(self, uri=None):
        self._want_document = False
        self.playpath = os.path.dirname(uri)
        if not uri:
            return False
        # FIXME: parse m3u files and extract actual URL
        if uri.endswith('.m3u') or uri.endswith('.m3u8'):
            self.playlist.extend(self.getplaylist([line.strip() \
                for line in open(uri).readlines()]))
        elif uri.endswith('.pls'):
            try:
                cf.readfp(open(uri))
                x = 1
                while True:
                    self.playlist.append(cf.get('playlist', 'File' + str(x)))
                    x += 1
            except:
                #read complete
                pass
        else:
            self.playlist.append('file://' + \
                                     urllib.quote(os.path.abspath(uri)))
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
                if self.update_id == -1:
                    self.update_id = gobject.timeout_add(self.UPDATE_INTERVAL,
                                                         self.update_scale_cb)

    def volume_changed_cb(self, widget, value):
        if self.player:
            self.player.player.set_property('volume', value)

    def scale_button_press_cb(self, widget, event):
        self.was_playing = self.player.is_playing()
        if self.was_playing:
            self.player.pause()

        # don't timeout-update position during seek
        if self.update_id != -1:
            gobject.source_remove(self.update_id)
            self.update_id = -1

    def scale_value_changed_cb(self, scale):
        # see seek.c:seek_cb
        real = long(scale.get_value() * self.p_duration / 100)  # in ns
        self.player.seek(real)
        # allow for a preroll
        self.player.get_state(timeout=50 * gst.MSECOND)  # 50 ms

    def scale_button_release_cb(self, widget, event):
        # see seek.cstop_seek
        widget.disconnect(self.changed_id)
        self.changed_id = -1

        if self.seek_timeout_id != -1:
            gobject.source_remove(self.seek_timeout_id)
            self.seek_timeout_id = -1
        else:
            if self.was_playing:
                self.player.play()

        if self.update_id != -1:
            self.error('Had a previous update timeout id')
        else:
            self.update_id = gobject.timeout_add(self.UPDATE_INTERVAL,
                self.update_scale_cb)

    def update_scale_cb(self):
        self.p_position, self.p_duration = self.player.query_position()
        if self.p_position != gst.CLOCK_TIME_NONE:
            value = self.p_position * 100.0 / self.p_duration

        return True


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

    def query_position(self):
        """ Returns a (position, duration) tuple """
        try:
            position, format = self.player.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self.player.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position, duration)

    def seek(self, location):
        """
        @param location: time to seek to, in nanoseconds
        """
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, location,
            gst.SEEK_TYPE_NONE, 0)

        res = self.player.send_event(event)
        if res:
            self.player.set_new_stream_time(0L)
        else:
            logging.debug('seek to %r failed' % location)

    def pause(self):
        logging.debug('pausing player')
        self.player.set_state(gst.STATE_PAUSED)
        self.playing = False

    def play(self):
        logging.debug('playing player')
        self.player.set_state(gst.STATE_PLAYING)
        self.playing = True
        self.error = False

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
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
