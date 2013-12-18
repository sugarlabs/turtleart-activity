#Copyright (c) 2008, Media Modifications Ltd.

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

import os
from gettext import gettext as _
import time

import gtk
import gst
import pygst
pygst.require('0.10')
import gobject
gobject.threads_init()

from sugar.activity.activity import get_bundle_path
import logging

from instance import Instance
import constants
import utils

logger = logging.getLogger('glive')

OGG_TRAITS = {
        0: { 'width': 160, 'height': 120, 'quality': 16 },
        1: { 'width': 384, 'height': 288, 'quality': 16 } }

class Glive:
    PHOTO_MODE_PHOTO = 0
    PHOTO_MODE_AUDIO = 1

    def __init__(self, activity_obj, model):
        self.activity = activity_obj
        self.model = model
        self._eos_cb = None

        self._has_camera = False
        self._can_limit_framerate = False
        self._playing = False
        self._pic_exposure_open = False
        self._thumb_exposure_open = False
        self._photo_mode = self.PHOTO_MODE_PHOTO

        self._audio_transcode_handler = None
        self._transcode_id = None
        self._video_transcode_handler = None
        self._thumb_handoff_handler = None

        self._audio_pixbuf = None

        self._detect_camera()

        self._pipeline = gst.Pipeline("Record")
        self._create_photobin()
        self._create_audiobin()
        self._create_videobin()
        self._create_xbin()
        self._create_pipeline()

        self._thumb_pipes = []
        self._mux_pipes = []

        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._bus_message_handler)

    def _detect_camera(self):
        v4l2src = gst.element_factory_make('v4l2src')
        if v4l2src.props.device_name is None:
            return

        self._has_camera = True

        # Figure out if we can place a framerate limit on the v4l2 element,
        # which in theory will make it all the way down to the hardware.
        # ideally, we should be able to do this by checking caps. However, I
        # can't find a way to do this (at this time, XO-1 cafe camera driver
        # doesn't support framerate changes, but gstreamer caps suggest
        # otherwise)
        pipeline = gst.Pipeline()
        caps = gst.Caps('video/x-raw-yuv,framerate=10/1')
        fsink = gst.element_factory_make('fakesink')
        pipeline.add(v4l2src, fsink)
        v4l2src.link(fsink, caps)
        self._can_limit_framerate = pipeline.set_state(gst.STATE_PAUSED) != gst.STATE_CHANGE_FAILURE
        pipeline.set_state(gst.STATE_NULL)

    def get_has_camera(self):
        return self._has_camera

    def _create_photobin(self):
        queue = gst.element_factory_make("queue", "pbqueue")
        queue.set_property("leaky", True)
        queue.set_property("max-size-buffers", 1)

        colorspace = gst.element_factory_make("ffmpegcolorspace", "pbcolorspace")
        jpeg = gst.element_factory_make("jpegenc", "pbjpeg")

        sink = gst.element_factory_make("fakesink", "pbsink")
        sink.connect("handoff", self._photo_handoff)
        sink.set_property("signal-handoffs", True)

        self._photobin = gst.Bin("photobin")
        self._photobin.add(queue, colorspace, jpeg, sink)

        gst.element_link_many(queue, colorspace, jpeg, sink)

        pad = queue.get_static_pad("sink")
        self._photobin.add_pad(gst.GhostPad("sink", pad))

    def _create_audiobin(self):
        src = gst.element_factory_make("alsasrc", "absrc")

        # attempt to use direct access to the 0,0 device, solving some A/V
        # sync issues
        src.set_property("device", "plughw:0,0")
        hwdev_available = src.set_state(gst.STATE_PAUSED) != gst.STATE_CHANGE_FAILURE
        src.set_state(gst.STATE_NULL)
        if not hwdev_available:
            src.set_property("device", "default")

        srccaps = gst.Caps("audio/x-raw-int,rate=16000,channels=1,depth=16")

        # guarantee perfect stream, important for A/V sync
        rate = gst.element_factory_make("audiorate")

        # without a buffer here, gstreamer struggles at the start of the
        # recording and then the A/V sync is bad for the whole video
        # (possibly a gstreamer/ALSA bug -- even if it gets caught up, it
        # should be able to resync without problem)
        queue = gst.element_factory_make("queue", "audioqueue")
        queue.set_property("leaky", True) # prefer fresh data
        queue.set_property("max-size-time", 5000000000) # 5 seconds
        queue.set_property("max-size-buffers", 500)
        queue.connect("overrun", self._log_queue_overrun)

        enc = gst.element_factory_make("wavenc", "abenc")

        sink = gst.element_factory_make("filesink", "absink")
        sink.set_property("location", os.path.join(Instance.instancePath, "output.wav"))

        self._audiobin = gst.Bin("audiobin")
        self._audiobin.add(src, rate, queue, enc, sink)

        src.link(rate, srccaps)
        gst.element_link_many(rate, queue, enc, sink)

    def _create_videobin(self):
        queue = gst.element_factory_make("queue", "videoqueue")
        queue.set_property("max-size-time", 5000000000) # 5 seconds
        queue.set_property("max-size-bytes", 33554432) # 32mb
        queue.connect("overrun", self._log_queue_overrun)

        scale = gst.element_factory_make("videoscale", "vbscale")

        scalecapsfilter = gst.element_factory_make("capsfilter", "scalecaps")

        scalecaps = gst.Caps('video/x-raw-yuv,width=160,height=120')
        scalecapsfilter.set_property("caps", scalecaps)

        colorspace = gst.element_factory_make("ffmpegcolorspace", "vbcolorspace")

        enc = gst.element_factory_make("theoraenc", "vbenc")
        enc.set_property("quality", 16)

        mux = gst.element_factory_make("oggmux", "vbmux")

        sink = gst.element_factory_make("filesink", "vbfile")
        sink.set_property("location", os.path.join(Instance.instancePath, "output.ogg"))

        self._videobin = gst.Bin("videobin")
        self._videobin.add(queue, scale, scalecapsfilter, colorspace, enc, mux, sink)

        queue.link(scale)
        scale.link_pads(None, scalecapsfilter, "sink")
        scalecapsfilter.link_pads("src", colorspace, None)
        gst.element_link_many(colorspace, enc, mux, sink)

        pad = queue.get_static_pad("sink")
        self._videobin.add_pad(gst.GhostPad("sink", pad))

    def _create_xbin(self):
        scale = gst.element_factory_make("videoscale")
        cspace = gst.element_factory_make("ffmpegcolorspace")
        xsink = gst.element_factory_make("ximagesink", "xsink")
        xsink.set_property("force-aspect-ratio", True)

        # http://thread.gmane.org/gmane.comp.video.gstreamer.devel/29644
        xsink.set_property("sync", False)

        self._xbin = gst.Bin("xbin")
        self._xbin.add(scale, cspace, xsink)
        gst.element_link_many(scale, cspace, xsink)

        pad = scale.get_static_pad("sink")
        self._xbin.add_pad(gst.GhostPad("sink", pad))

    def _config_videobin(self, quality, width, height):
        vbenc = self._videobin.get_by_name("vbenc")
        vbenc.set_property("quality", 16)
        scaps = self._videobin.get_by_name("scalecaps")
        scaps.set_property("caps", gst.Caps("video/x-raw-yuv,width=%d,height=%d" % (width, height)))

    def _create_pipeline(self):
        if not self._has_camera:
            return

        src = gst.element_factory_make("v4l2src", "camsrc")
        try:
            # old gst-plugins-good does not have this property
            src.set_property("queue-size", 2)
        except:
            pass

        # if possible, it is important to place the framerate limit directly
        # on the v4l2src so that it gets communicated all the way down to the
        # camera level
        if self._can_limit_framerate:
            srccaps = gst.Caps('video/x-raw-yuv,framerate=10/1')
        else:
            srccaps = gst.Caps('video/x-raw-yuv')

        # we attempt to limit the framerate on the v4l2src directly, but we
        # can't trust this: perhaps we are falling behind in our capture,
        # or maybe the kernel driver doesn't provide the exact framerate.
        # the videorate element guarantees a perfect framerate and is important
        # for A/V sync because OGG does not store timestamps, it just stores
        # the FPS value.
        rate = gst.element_factory_make("videorate")
        ratecaps = gst.Caps('video/x-raw-yuv,framerate=10/1')

        tee = gst.element_factory_make("tee", "tee")
        queue = gst.element_factory_make("queue", "dispqueue")

        # prefer fresh frames
        queue.set_property("leaky", True)
        queue.set_property("max-size-buffers", 2)

        self._pipeline.add(src, rate, tee, queue)
        src.link(rate, srccaps)
        rate.link(tee, ratecaps)
        tee.link(queue)

        self._xvsink = gst.element_factory_make("xvimagesink", "xsink")
        self._xv_available = self._xvsink.set_state(gst.STATE_PAUSED) != gst.STATE_CHANGE_FAILURE
        self._xvsink.set_state(gst.STATE_NULL)

        # http://thread.gmane.org/gmane.comp.video.gstreamer.devel/29644
        self._xvsink.set_property("sync", False)

        self._xvsink.set_property("force-aspect-ratio", True)

    def _log_queue_overrun(self, queue):
        cbuffers = queue.get_property("current-level-buffers")
        cbytes = queue.get_property("current-level-bytes")
        ctime = queue.get_property("current-level-time")
        logger.error("Buffer overrun in %s (%d buffers, %d bytes, %d time)"
            % (queue.get_name(), cbuffers, cbytes, ctime))
 
    def _thumb_element(self, name):
        return self._thumb_pipes[-1].get_by_name(name)

    def is_using_xv(self):
        return self._pipeline.get_by_name("xsink") == self._xvsink

    def _configure_xv(self):
        if self.is_using_xv():
            # nothing to do, Xv already configured
            return self._xvsink

        queue = self._pipeline.get_by_name("dispqueue")
        if self._pipeline.get_by_name("xbin"):
            # X sink is configured, so remove it
            queue.unlink(self._xbin)
            self._pipeline.remove(self._xbin)

        self._pipeline.add(self._xvsink)
        queue.link(self._xvsink)
        return self._xvsink

    def _configure_x(self):
        if self._pipeline.get_by_name("xbin") == self._xbin:
            # nothing to do, X already configured
            return self._xbin.get_by_name("xsink")

        queue = self._pipeline.get_by_name("dispqueue")
        xvsink = self._pipeline.get_by_name("xsink")

        if xvsink:
            # Xv sink is configured, so remove it
            queue.unlink(xvsink)
            self._pipeline.remove(xvsink)

        self._pipeline.add(self._xbin)
        queue.link(self._xbin)
        return self._xbin.get_by_name("xsink")

    def play(self, use_xv=True):
        if self._get_state() == gst.STATE_PLAYING:
            return

        if self._has_camera:
            if use_xv and self._xv_available:
                xsink = self._configure_xv()
            else:
                xsink = self._configure_x()

            # X overlay must be set every time, it seems to forget when you stop
            # the pipeline.
            self.activity.set_glive_sink(xsink)

        self._pipeline.set_state(gst.STATE_PLAYING)
        self._playing = True

    def pause(self):
        self._pipeline.set_state(gst.STATE_PAUSED)
        self._playing = False

    def stop(self):
        self._pipeline.set_state(gst.STATE_NULL)
        self._playing = False

    def is_playing(self):
        return self._playing

    def _get_state(self):
        return self._pipeline.get_state()[1]

    def stop_recording_audio(self):
        # We should be able to simply pause and remove the audiobin, but
        # this seems to cause a gstreamer segfault. So we stop the whole
        # pipeline while manipulating it.
        # http://dev.laptop.org/ticket/10183
        self._pipeline.set_state(gst.STATE_NULL)
        self.model.shutter_sound()
        self._pipeline.remove(self._audiobin)

        audio_path = os.path.join(Instance.instancePath, "output.wav")
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) <= 0:
            # FIXME: inform model of failure?
            return

        if self._audio_pixbuf:
            self.model.still_ready(self._audio_pixbuf)

        line = 'filesrc location=' + audio_path + ' name=audioFilesrc ! wavparse name=audioWavparse ! audioconvert name=audioAudioconvert ! vorbisenc name=audioVorbisenc ! oggmux name=audioOggmux ! filesink name=audioFilesink'
        audioline = gst.parse_launch(line)

        taglist = self._get_tags(constants.TYPE_AUDIO)

        if self._audio_pixbuf:
            pixbuf_b64 = utils.getStringEncodedFromPixbuf(self._audio_pixbuf)
            taglist[gst.TAG_EXTENDED_COMMENT] = "coverart=" + pixbuf_b64

        vorbis_enc = audioline.get_by_name('audioVorbisenc')
        vorbis_enc.merge_tags(taglist, gst.TAG_MERGE_REPLACE_ALL)

        audioFilesink = audioline.get_by_name('audioFilesink')
        audioOggFilepath = os.path.join(Instance.instancePath, "output.ogg")
        audioFilesink.set_property("location", audioOggFilepath)

        audioBus = audioline.get_bus()
        audioBus.add_signal_watch()
        self._audio_transcode_handler = audioBus.connect('message', self._onMuxedAudioMessageCb, audioline)
        self._transcode_id = gobject.timeout_add(200, self._transcodeUpdateCb, audioline)
        audioline.set_state(gst.STATE_PLAYING)

    def _get_tags(self, type):
        tl = gst.TagList()
        tl[gst.TAG_ARTIST] = self.model.get_nickname()
        tl[gst.TAG_COMMENT] = "olpc"
        #this is unfortunately, unreliable
        #record.Record.log.debug("self.ca.metadata['title']->" + str(self.ca.metadata['title']) )
        tl[gst.TAG_ALBUM] = "olpc" #self.ca.metadata['title']
        tl[gst.TAG_DATE] = utils.getDateString(int(time.time()))
        stringType = constants.MEDIA_INFO[type]['istr']
        
        # Translators: photo by photographer, e.g. "Photo by Mary"
        tl[gst.TAG_TITLE] = _('%(type)s by %(name)s') % {'type': stringType,
                'name': self.model.get_nickname()}
        return tl

    def _take_photo(self, photo_mode):
        if self._pic_exposure_open:
            return

        self._photo_mode = photo_mode
        self._pic_exposure_open = True
        pad = self._photobin.get_static_pad("sink")
        self._pipeline.add(self._photobin)
        self._photobin.set_state(gst.STATE_PLAYING)
        self._pipeline.get_by_name("tee").link(self._photobin)

    def take_photo(self):
        if self._has_camera:
            self._take_photo(self.PHOTO_MODE_PHOTO)

    def _photo_handoff(self, fsink, buffer, pad, user_data=None):
        if not self._pic_exposure_open:
            return

        pad = self._photobin.get_static_pad("sink")
        self._pipeline.get_by_name("tee").unlink(self._photobin)
        self._pipeline.remove(self._photobin)

        self._pic_exposure_open = False
        pic = gtk.gdk.pixbuf_loader_new_with_mime_type("image/jpeg")
        pic.write( buffer )
        pic.close()
        pixBuf = pic.get_pixbuf()
        del pic

        self.save_photo(pixBuf)

    def save_photo(self, pixbuf):
        if self._photo_mode == self.PHOTO_MODE_AUDIO:
            self._audio_pixbuf = pixbuf
        else:
            self.model.save_photo(pixbuf)

    def record_video(self, quality):
        if not self._has_camera:
            return

        self._ogg_quality = quality
        self._config_videobin(OGG_TRAITS[quality]['quality'],
            OGG_TRAITS[quality]['width'],
            OGG_TRAITS[quality]['height'])

        # If we use pad blocking and adjust the pipeline on-the-fly, the
        # resultant video has bad A/V sync :(
        # If we pause the pipeline while adjusting it, the A/V sync is better
        # but not perfect :(
        # so we stop the whole thing while reconfiguring to get the best results
        self._pipeline.set_state(gst.STATE_NULL)
        self._pipeline.add(self._videobin)
        self._pipeline.get_by_name("tee").link(self._videobin)
        self._pipeline.add(self._audiobin)
        self.play()

    def record_audio(self):
        if self._has_camera:
            self._audio_pixbuf = None
            self._take_photo(self.PHOTO_MODE_AUDIO)

        # we should be able to add the audiobin on the fly, but unfortunately
        # this results in several seconds of silence being added at the start
        # of the recording. So we stop the whole pipeline while adjusting it.
        # SL#2040
        self._pipeline.set_state(gst.STATE_NULL)
        self._pipeline.add(self._audiobin)
        self.play()

    def stop_recording_video(self):
        if not self._has_camera:
            return

        # We stop the pipeline while we are adjusting the pipeline to stop
        # recording because if we do it on-the-fly, the following video live
        # feed to the screen becomes several seconds delayed. Weird!
        # FIXME: retest on F11
        # FIXME: could this be the result of audio shortening problems?
        self._eos_cb = self._video_eos
        self._pipeline.get_by_name('camsrc').send_event(gst.event_new_eos())
        self._audiobin.get_by_name('absrc').send_event(gst.event_new_eos())

    def _video_eos(self):
        self._pipeline.set_state(gst.STATE_NULL)
        self._pipeline.get_by_name("tee").unlink(self._videobin)
        self._pipeline.remove(self._videobin)
        self._pipeline.remove(self._audiobin)

        self.model.shutter_sound()

        if len(self._thumb_pipes) > 0:
            thumbline = self._thumb_pipes[-1]
            thumbline.get_by_name('thumb_fakesink').disconnect(self._thumb_handoff_handler)

        ogg_path = os.path.join(Instance.instancePath, "output.ogg") #ogv
        if not os.path.exists(ogg_path) or os.path.getsize(ogg_path) <= 0:
            # FIXME: inform model of failure?
            return

        line = 'filesrc location=' + ogg_path + ' name=thumbFilesrc ! oggdemux name=thumbOggdemux ! theoradec name=thumbTheoradec ! tee name=thumb_tee ! queue name=thumb_queue ! ffmpegcolorspace name=thumbFfmpegcolorspace ! jpegenc name=thumbJPegenc ! fakesink name=thumb_fakesink'
        thumbline = gst.parse_launch(line)
        thumb_queue = thumbline.get_by_name('thumb_queue')
        thumb_queue.set_property("leaky", True)
        thumb_queue.set_property("max-size-buffers", 1)
        thumb_tee = thumbline.get_by_name('thumb_tee')
        thumb_fakesink = thumbline.get_by_name('thumb_fakesink')
        self._thumb_handoff_handler = thumb_fakesink.connect("handoff", self.copyThumbPic)
        thumb_fakesink.set_property("signal-handoffs", True)
        self._thumb_pipes.append(thumbline)
        self._thumb_exposure_open = True
        thumbline.set_state(gst.STATE_PLAYING)

    def copyThumbPic(self, fsink, buffer, pad, user_data=None):
        if not self._thumb_exposure_open:
            return

        self._thumb_exposure_open = False
        loader = gtk.gdk.pixbuf_loader_new_with_mime_type("image/jpeg")
        loader.write(buffer)
        loader.close()
        self.thumbBuf = loader.get_pixbuf()
        self.model.still_ready(self.thumbBuf)

        self._thumb_element('thumb_tee').unlink(self._thumb_element('thumb_queue'))

        oggFilepath = os.path.join(Instance.instancePath, "output.ogg") #ogv
        wavFilepath = os.path.join(Instance.instancePath, "output.wav")
        muxFilepath = os.path.join(Instance.instancePath, "mux.ogg") #ogv

        muxline = gst.parse_launch('filesrc location=' + str(oggFilepath) + ' name=muxVideoFilesrc ! oggdemux name=muxOggdemux ! theoraparse ! oggmux name=muxOggmux ! filesink location=' + str(muxFilepath) + ' name=muxFilesink filesrc location=' + str(wavFilepath) + ' name=muxAudioFilesrc ! wavparse name=muxWavparse ! audioconvert name=muxAudioconvert ! vorbisenc name=muxVorbisenc ! muxOggmux.')
        taglist = self._get_tags(constants.TYPE_VIDEO)
        vorbis_enc = muxline.get_by_name('muxVorbisenc')
        vorbis_enc.merge_tags(taglist, gst.TAG_MERGE_REPLACE_ALL)

        muxBus = muxline.get_bus()
        muxBus.add_signal_watch()
        self._video_transcode_handler = muxBus.connect('message', self._onMuxedVideoMessageCb, muxline)
        self._mux_pipes.append(muxline)
        #add a listener here to monitor % of transcoding...
        self._transcode_id = gobject.timeout_add(200, self._transcodeUpdateCb, muxline)
        muxline.set_state(gst.STATE_PLAYING)

    def _transcodeUpdateCb( self, pipe ):
        position, duration = self._query_position( pipe )
        if position != gst.CLOCK_TIME_NONE:
            value = position * 100.0 / duration
            value = value/100.0
            self.model.set_progress(value, _('Saving...'))
        return True

    def _query_position(self, pipe):
        try:
            position, format = pipe.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = pipe.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position, duration)

    def _onMuxedVideoMessageCb(self, bus, message, pipe):
        if message.type != gst.MESSAGE_EOS:
            return True

        gobject.source_remove(self._video_transcode_handler)
        self._video_transcode_handler = None
        gobject.source_remove(self._transcode_id)
        self._transcode_id = None
        pipe.set_state(gst.STATE_NULL)
        pipe.get_bus().remove_signal_watch()
        pipe.get_bus().disable_sync_message_emission()

        wavFilepath = os.path.join(Instance.instancePath, "output.wav")
        oggFilepath = os.path.join(Instance.instancePath, "output.ogg") #ogv
        muxFilepath = os.path.join(Instance.instancePath, "mux.ogg") #ogv
        os.remove( wavFilepath )
        os.remove( oggFilepath )
        self.model.save_video(muxFilepath, self.thumbBuf)
        return False

    def _onMuxedAudioMessageCb(self, bus, message, pipe):
        if message.type != gst.MESSAGE_EOS:
            return True

        gobject.source_remove(self._audio_transcode_handler)
        self._audio_transcode_handler = None
        gobject.source_remove(self._transcode_id)
        self._transcode_id = None
        pipe.set_state(gst.STATE_NULL)
        pipe.get_bus().remove_signal_watch()
        pipe.get_bus().disable_sync_message_emission()

        wavFilepath = os.path.join(Instance.instancePath, "output.wav")
        oggFilepath = os.path.join(Instance.instancePath, "output.ogg")
        os.remove( wavFilepath )
        self.model.save_audio(oggFilepath, self._audio_pixbuf)
        return False

    def _bus_message_handler(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            if self._eos_cb:
                cb = self._eos_cb
                self._eos_cb = None
                cb()
        elif t == gst.MESSAGE_ERROR:
            #todo: if we come out of suspend/resume with errors, then get us back up and running...
            #todo: handle "No space left on the resource.gstfilesink.c"
            #err, debug = message.parse_error()
            pass

    def abandonMedia(self):
        self.stop()

        if self._audio_transcode_handler:
            gobject.source_remove(self._audio_transcode_handler)
            self._audio_transcode_handler = None
        if self._transcode_id:
            gobject.source_remove(self._transcode_id)
            self._transcode_id = None
        if self._video_transcode_handler:
            gobject.source_remove(self._video_transcode_handler)
            self._video_transcode_handler = None

        wav_path = os.path.join(Instance.instancePath, "output.wav")
        if os.path.exists(wav_path):
            os.remove(wav_path)
        ogg_path = os.path.join(Instance.instancePath, "output.ogg") #ogv
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        mux_path = os.path.join(Instance.instancePath, "mux.ogg") #ogv
        if os.path.exists(mux_path):
            os.remove(mux_path)

