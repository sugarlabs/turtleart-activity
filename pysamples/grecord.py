#Copyright (c) 2008, Media Modifications Ltd.
#Copyright (c) 2011, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; Pass
# it 'start' to start recording; 'stop' to stop recording; 'play'
# to play back your recording; or 'save' to save to the Sugar Journal.


def myblock(tw, arg):
    ''' Record and playback a sound (Sugar only) '''
    import os
    import time

    import gtk
    import gst

    import gobject
    gobject.threads_init()

    from TurtleArt.tautils import get_path
    from TurtleArt.tagplay import play_audio_from_file
    from sugar.datastore import datastore
    from sugar import profile


    class Grecord:

        def __init__(self, tw):
            ''' Set up the stream. '''
            datapath = get_path(tw.parent, 'instance')
            self.capture_file = os.path.join(datapath, 'output.wav')
            self.save_file = os.path.join(datapath, 'output.ogg')
            self._eos_cb = None

            self._can_limit_framerate = False
            self._playing = False

            self._audio_transcode_handler = None
            self._transcode_id = None

            self._pipeline = gst.Pipeline("Record")
            self._create_audiobin()
            self._pipeline.add(self._audiobin)

            bus = self._pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._bus_message_handler)

        def _create_audiobin(self):
            src = gst.element_factory_make("alsasrc", "absrc")

            # attempt to use direct access to the 0,0 device, solving some A/V
            # sync issues
            src.set_property("device", "plughw:0,0")
            hwdev_available = src.set_state(gst.STATE_PAUSED) != \
                              gst.STATE_CHANGE_FAILURE
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
            sink.set_property("location", self.capture_file)

            self._audiobin = gst.Bin("audiobin")
            self._audiobin.add(src, rate, queue, enc, sink)

            src.link(rate, srccaps)
            gst.element_link_many(rate, queue, enc, sink)

        def _log_queue_overrun(self, queue):
            cbuffers = queue.get_property("current-level-buffers")
            cbytes = queue.get_property("current-level-bytes")
            ctime = queue.get_property("current-level-time")
 
        def play(self):
            if self._get_state() == gst.STATE_PLAYING:
                return

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
            self.stop()

            audio_path = self.capture_file
            if not os.path.exists(audio_path) or \
                   os.path.getsize(audio_path) <= 0:
                return

            line = 'filesrc location=' + audio_path + ' name=audioFilesrc ! wavparse name=audioWavparse ! audioconvert name=audioAudioconvert ! vorbisenc name=audioVorbisenc ! oggmux name=audioOggmux ! filesink name=audioFilesink'
            audioline = gst.parse_launch(line)

            vorbis_enc = audioline.get_by_name('audioVorbisenc')

            audioFilesink = audioline.get_by_name('audioFilesink')
            audioOggFilepath = self.save_file
            audioFilesink.set_property("location", audioOggFilepath)

            audioBus = audioline.get_bus()
            audioBus.add_signal_watch()
            self._audio_transcode_handler = audioBus.connect(
                'message', self._onMuxedAudioMessageCb, audioline)
            self._transcode_id = gobject.timeout_add(
                200, self._transcodeUpdateCb, audioline)
            audioline.set_state(gst.STATE_PLAYING)

        def blockedCb(self, x, y, z):
            pass

        def record_audio(self):
            self.play()

        def _transcodeUpdateCb(self, pipe):
            position, duration = self._query_position(pipe)
            if position != gst.CLOCK_TIME_NONE:
                value = position * 100.0 / duration
                value = value/100.0
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

            wavFilepath = self.capture_file
            oggFilepath = self.save_file
            os.remove( wavFilepath )
            return False

        def _bus_message_handler(self, bus, message):
            t = message.type
            if t == gst.MESSAGE_EOS:
                if self._eos_cb:
                    cb = self._eos_cb
                    self._eos_cb = None
                    cb()
            elif t == gst.MESSAGE_ERROR:
                # TODO: if we come out of suspend/resume with errors, then
                # get us back up and running...  TODO: handle "No space
                # left on the resource.gstfilesink.c" err, debug =
                # message.parse_error()
                pass

    # We store the stream as tw.grecord so that we can use it repeatedly.
    if not hasattr(tw, 'grecord'):
        tw.grecord = Grecord(tw)

    # Sometime we need to pass multiple arguments, e.g., save, savename
    savename = _('turtle audio recording')
    if type(arg) == type([]):
        cmd = arg[0]
        if len(arg) > 1:
            savename = str(arg[1])
    else:
        cmd = arg

    if cmd == _('start'):
        tw.grecord.record_audio()
    elif cmd == _('stop'):
        if os.path.exists(tw.grecord.save_file):
            os.remove(tw.grecord.save_file)
        tw.grecord.stop_recording_audio()
    elif cmd == _('play'):
        play_audio_from_file(tw.lc, tw.grecord.save_file)
    elif cmd == _('save'):
        if os.path.exists(tw.grecord.save_file):
            if tw.running_sugar:
                dsobject = datastore.create()
                dsobject.metadata['title'] = savename
                dsobject.metadata['icon-color'] = \
                    profile.get_color().to_string()
                dsobject.metadata['mime_type'] = 'audio/ogg'
                dsobject.set_file_path(tw.grecord.save_file)
                datastore.write(dsobject)
                dsobject.destroy()
