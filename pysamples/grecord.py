# Copyright (c) 2008, Media Modifications Ltd.
# Copyright (c) 2011, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; Pass
# it 'start' to start recording; 'stop' to stop recording; 'play' to
# play back your recording; or 'save' to save your recording to the
# Sugar Journal.
from gi.repository import GObject
from gi.repository import Gst


def myblock(tw, args):
    ''' Record and playback a sound (Sugar only) '''
    import os
    GObject.threads_init()

    from TurtleArt.tautils import get_path
    from TurtleArt.tagplay import play_audio_from_file
    from sugar3.datastore import datastore
    from sugar3 import profile

    from gettext import gettext as _

    class Grecord:

        ''' A class for creating a gstreamer session for recording audio. '''

        def __init__(self, tw):
            ''' Set up the stream. We save to a raw .wav file and then
            convert the sound to .ogg for saving. '''
            datapath = get_path(tw.parent, 'instance')
            self.capture_file = os.path.join(datapath, 'output.wav')
            self.save_file = os.path.join(datapath, 'output.ogg')
            self._eos_cb = None

            self._can_limit_framerate = False
            self._recording = False

            self._audio_transcode_handler = None
            self._transcode_id = None

            self._pipeline = Gst.Pipeline("Record")
            self._create_audiobin()
            self._pipeline.add(self._audiobin)

            bus = self._pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._bus_message_handler)

        def _create_audiobin(self):
            ''' Assemble all the pieces we need. '''
            src = Gst.ElementFactory.make("alsasrc", "absrc")

            # attempt to use direct access to the 0,0 device, solving
            # some A/V sync issues
            src.set_property("device", "plughw:0,0")
            hwdev_available = src.set_state(Gst.State.PAUSED) != \
                Gst.StateChangeReturn.FAILURE
            src.set_state(Gst.State.NULL)
            if not hwdev_available:
                src.set_property("device", "default")

            srccaps = Gst.Caps(
                "audio/x-raw-int,rate=16000,channels=1,depth=16")

            # guarantee perfect stream, important for A/V sync
            rate = Gst.ElementFactory.make("audiorate")

            # without a buffer here, gstreamer struggles at the start
            # of the recording and then the A/V sync is bad for the
            # whole video (possibly a gstreamer/ALSA bug -- even if it
            # gets caught up, it should be able to resync without
            # problem)
            queue = Gst.ElementFactory.make("queue", "audioqueue")
            queue.set_property("leaky", True)  # prefer fresh data
            queue.set_property("max-size-time", 5000000000)  # 5 seconds
            queue.set_property("max-size-buffers", 500)

            enc = Gst.ElementFactory.make("wavenc", "abenc")

            sink = Gst.ElementFactory.make("filesink", "absink")
            sink.set_property("location", self.capture_file)

            self._audiobin = Gst.Bin("audiobin")
            self._audiobin.add(src, rate, queue, enc, sink)

            src.link(rate, srccaps)
            Gst.element_link_many(rate, queue, enc, sink)

        def is_recording(self):
            ''' Are we recording? '''
            return self._recording

        def _get_state(self):
            ''' What is the state of our gstreamer pipeline? '''
            return self._pipeline.get_state()[1]

        def start_recording_audio(self):
            ''' Start the stream in order to start recording. '''
            if self._get_state() == Gst.State.PLAYING:
                return
            self._pipeline.set_state(Gst.State.PLAYING)
            self._recording = True

        def stop_recording_audio(self):
            ''' Stop recording and then convert the results into a
            .ogg file using a new stream. '''
            self._pipeline.set_state(Gst.State.NULL)
            self._recording = False

            if not os.path.exists(self.capture_file) or \
                    os.path.getsize(self.capture_file) <= 0:
                return

            # Remove previous transcoding results.
            if os.path.exists(self.save_file):
                os.remove(self.save_file)

            line = 'filesrc location=' + self.capture_file + \
                ' name=audioFilesrc ! wavparse name=audioWavparse \
! audioconvert name=audioAudioconvert ! vorbisenc name=audioVorbisenc \
! oggmux name=audioOggmux ! filesink name=audioFilesink'
            audioline = Gst.parse_launch(line)

            # vorbis_enc = audioline.get_by_name('audioVorbisenc')

            audioFilesink = audioline.get_by_name('audioFilesink')
            audioFilesink.set_property("location", self.save_file)

            audioBus = audioline.get_bus()
            audioBus.add_signal_watch()
            self._audio_transcode_handler = audioBus.connect(
                'message', self._onMuxedAudioMessageCb, audioline)
            self._transcode_id = GObject.timeout_add(
                200, self._transcodeUpdateCb, audioline)
            audioline.set_state(Gst.State.PLAYING)

        def _transcodeUpdateCb(self, pipe):
            ''' Where are we in the transcoding process? '''
            position, duration = self._query_position(pipe)
            if position != Gst.CLOCK_TIME_NONE:
                value = position * 100.0 / duration
                value = value / 100.0
            return True

        def _query_position(self, pipe):
            ''' Where are we in the stream? '''
            try:
                position, format = pipe.query_position(Gst.Format.TIME)
            except BaseException:
                position = Gst.CLOCK_TIME_NONE

            try:
                duration, format = pipe.query_duration(Gst.Format.TIME)
            except BaseException:
                duration = Gst.CLOCK_TIME_NONE

            return (position, duration)

        def _onMuxedAudioMessageCb(self, bus, message, pipe):
            ''' Clean up at end of stream.'''
            if message.type != Gst.MessageType.EOS:
                return True

            GObject.source_remove(self._audio_transcode_handler)
            self._audio_transcode_handler = None
            GObject.source_remove(self._transcode_id)
            self._transcode_id = None
            pipe.set_state(Gst.State.NULL)
            pipe.get_bus().remove_signal_watch()
            pipe.get_bus().disable_sync_message_emission()

            os.remove(self.capture_file)
            return False

        def _bus_message_handler(self, bus, message):
            ''' Handle any messages associated with the stream. '''
            t = message.type
            if t == Gst.MessageType.EOS:
                if self._eos_cb:
                    cb = self._eos_cb
                    self._eos_cb = None
                    cb()
            elif t == Gst.MessageType.ERROR:
                # TODO: if we come out of suspend/resume with errors, then
                # get us back up and running...  TODO: handle "No space
                # left on the resource.gstfilesink.c" err, debug =
                # message.parse_error()
                pass

    # We store the audio-record stream instance as tw.grecord so that
    # we can use it repeatedly.
    if not hasattr(tw, 'grecord'):
        tw.grecord = Grecord(tw)

    # Sometime we need to parse multiple arguments, e.g., save, savename
    save_name = '%s_%s' % (tw.activity.name, _('sound'))
    cmd = args[0].lower()
    if len(args) > 1:
        save_name = str(args[1])

    if cmd == 'start' or cmd == _('start').lower():
        tw.grecord.start_recording_audio()
    elif cmd == 'stop' or cmd == _('stop').lower():
        tw.grecord.stop_recording_audio()
    elif cmd == 'play' or cmd == _('play').lower():
        play_audio_from_file(tw.lc, tw.grecord.save_file)
    elif cmd == 'save' or cmd == _('save').lower():
        if os.path.exists(tw.grecord.save_file) and tw.running_sugar:
            dsobject = datastore.create()
            dsobject.metadata['title'] = save_name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'audio/ogg'
            dsobject.set_file_path(tw.grecord.save_file)
            datastore.write(dsobject)
            dsobject.destroy()
