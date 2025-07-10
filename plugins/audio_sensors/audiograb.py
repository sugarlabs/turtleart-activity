#! /usr/bin/python
#
# Author:  Arjun Sarwal   arjun@laptop.org
# Copyright (C) 2007, Arjun Sarwal
# Copyright (C) 2009-11 Walter Bender
# Copyright (C) 2009, Benjamin Berg, Sebastian Berg
# Copyright (C) 2009, Sayamindu Dasgupta
# Copyright (C) 2010, Sascha Silbe
# Copyright (C) 2016, James Cameron [GStreamer 1.0]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA


from gi.repository import Gst

Gst.init(None)

from numpy import fromstring
import subprocess
import traceback
from threading import Timer
from TurtleArt.taconstants import XO1, XO4

import logging

log = logging.getLogger('turtleart-activity')
log.setLevel(logging.ERROR)

# Initial device settings
RATE = 48000
MIC_BOOST = True
DC_MODE_ENABLE = False
CAPTURE_GAIN = 50
BIAS = True

# Setting on quit
QUIT_MIC_BOOST = False
QUIT_DC_MODE_ENABLE = False
QUIT_CAPTURE_GAIN = 100
QUIT_BIAS = True

SENSOR_AC_NO_BIAS = 'external'
SENSOR_AC_BIAS = 'sound'
SENSOR_DC_NO_BIAS = 'voltage'
SENSOR_DC_BIAS = 'resistance'


class AudioGrab():
    """ The interface between measure and the audio device """

    def __init__(self, callable1, parent,
                 mode=None, bias=None, gain=None, boost=None):
        """ Initialize the class: callable1 is a data buffer;
            activity is the parent class """

        self.callable1 = callable1
        self.parent = parent
        self.rate = RATE
        if self.parent.hw in [XO1, XO4]:
            self.channels = 1
        else:
            self.channels = None
        if self.channels is None:
            self.channels = 2

        self.we_are_logging = False
        self._log_this_sample = False
        self._logging_timer = None
        self._logging_counter = 0
        self._image_counter = 0
        self._logging_interval = 0
        self._channels_logged = []
        self._busy = False

        self._dont_queue_the_buffer = False

        # self._display_counter = DISPLAY_DUTY_CYCLE

        # self.activity.wave.set_channels(self.channels)
        for i in range(self.channels):
            self._channels_logged.append(False)

        # Set mixer to known state
        self.set_dc_mode(DC_MODE_ENABLE)
        self.set_bias(BIAS)
        self.set_capture_gain(CAPTURE_GAIN)
        self.set_mic_boost(MIC_BOOST)

        self._set_sensor_type(mode, bias, gain, boost)
        self.master = self.get_master()
        self.dc_mode = self.get_dc_mode()
        self.bias = self.get_bias()
        self.capture_gain = self.get_capture_gain()
        self.mic_boost = self.get_mic_boost()

        # Set up gstreamer pipeline
        self._pad_count = 0
        self.pads = []
        self.queue = []
        self.fakesink = []
        self.pipeline = Gst.Pipeline.new('pipeline')
        self.alsasrc = Gst.ElementFactory.make('alsasrc', 'alsa-source')
        self.pipeline.add(self.alsasrc)
        self.caps1 = Gst.ElementFactory.make('capsfilter', 'caps1')
        self.pipeline.add(self.caps1)
        caps_str = 'audio/x-raw,rate=(int)%d,channels=(int)%d,depth=(int)16'\
                   % (RATE, self.channels)
        self.caps1.set_property('caps', Gst.caps_from_string(caps_str))
        if self.channels == 1:
            self.fakesink.append(Gst.ElementFactory.make('fakesink', 'fsink'))
            self.pipeline.add(self.fakesink[0])
            self.fakesink[0].connect('handoff', self.on_buffer, 0)
            self.fakesink[0].set_property('signal-handoffs', True)
            self.alsasrc.link(self.caps1)
            self.caps1.link(self.fakesink[0])
        else:
            if not hasattr(self, 'splitter'):
                self.splitter = Gst.ElementFactory.make('deinterleave')
                self.pipeline.add(self.splitter)
                self.splitter.set_properties('keep-positions=true', 'name=d')
                self.splitter.connect('pad-added', self._splitter_pad_added)
                self.alsasrc.link(self.caps1)
                self.caps1.link(self.splitter)
            for i in range(self.channels):
                self.queue.append(Gst.ElementFactory.make('queue'))
                self.pipeline.add(self.queue[i])
                self.fakesink.append(Gst.ElementFactory.make('fakesink'))
                self.pipeline.add(self.fakesink[i])
                self.fakesink[i].connect('handoff', self.on_buffer, i)
                self.fakesink[i].set_property('signal-handoffs', True)

    def _unlink_sink_queues(self):
        ''' Build the sink pipelines '''

        # If there were existing pipelines, unlink them
        for i in range(self._pad_count):
            log.debug('unlinking old elements')
            try:
                self.splitter.unlink(self.queue[i])
                self.queue[i].unlink(self.fakesink[i])
            except BaseException:
                traceback.print_exc()

        # Build the new pipelines
        self._pad_count = 0
        self.pads = []
        log.debug('building new pipelines')

    def _splitter_pad_added(self, element, pad):
        ''' Seems to be the case that ring is right channel 0,
                                       tip is  left channel 1'''
        self.pads.append(pad)
        if self._pad_count < self.channels:
            pad.link(self.queue[self._pad_count].get_static_pad('sink'))
            self.queue[self._pad_count].get_static_pad('src').link(
                self.fakesink[self._pad_count].get_static_pad('sink'))
            self._pad_count += 1
        else:
            log.debug('ignoring channels > %d' % self.channels)

    def set_handoff_signal(self, handoff_state):
        '''Sets whether the handoff signal would generate an interrupt
        or not'''
        for i in range(len(self.fakesink)):
            self.fakesink[i].set_property('signal-handoffs', handoff_state)

    def _new_buffer(self, buf, channel):
        ''' Use a new buffer '''
        if not self._dont_queue_the_buffer:
            self.callable1(buf, channel=channel)

    def on_buffer(self, element, data_buffer, pad, channel):
        '''The function that is called whenever new data is available
        This is the signal handler for the handoff signal'''
        temp_buffer = fromstring(data_buffer.extract_dup(
            0, data_buffer.get_size()), 'int16')
        if not self._dont_queue_the_buffer:
            self._new_buffer(temp_buffer, channel=channel)
        return False

    def set_freeze_the_display(self, freeze=False):
        ''' Useful when just the display is needed to be frozen, but
        logging should continue '''
        self._dont_queue_the_buffer = not freeze

    def get_freeze_the_display(self):
        '''Returns state of queueing the buffer'''
        return not self._dont_queue_the_buffer

    def start_sound_device(self):
        '''Start or Restart grabbing data from the audio capture'''
        Gst.Event.new_flush_start()
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop_sound_device(self):
        '''Stop grabbing data from capture device'''
        Gst.Event.new_flush_stop(False)
        self.pipeline.set_state(Gst.State.NULL)

    def set_logging_params(self, start_stop=False, interval=0):
        ''' Configures for logging of data: starts or stops a session;
        and sets the logging interval. '''
        self.we_are_logging = start_stop
        self._logging_interval = interval
        if not start_stop:
            if self._logging_timer:
                self._logging_timer.cancel()
                self._logging_timer = None
                self._log_this_sample = False
                self._logging_counter = 0
        elif interval != 0:
            self._make_timer()
        self._busy = False

    def _sample_now(self):
        ''' Log the current sample now. This method is called from the
        _logging_timer object when the interval expires. '''
        self._log_this_sample = True
        self._make_timer()

    def _make_timer(self):
        ''' Create the next timer that will trigger data logging. '''
        self._logging_timer = Timer(self._logging_interval, self._sample_now)
        self._logging_timer.start()

    def set_sampling_rate(self, sr):
        ''' Sets the sampling rate of the logging device. Sampling
        rate must be given as an integer for example 16000 for setting
        16Khz sampling rate The sampling rate would be set in the
        device to the nearest available. '''
        self.pause_grabbing()
        caps_str = 'audio/x-raw-int,rate=%d,channels=%d,depth=16' % (
            sr, self.channels)
        self.caps1.set_property('caps', Gst.caps_from_string(caps_str))
        self.resume_grabbing()

    def set_callable1(self, callable1):
        '''Sets the callable to the drawing function for giving the
        data at the end of idle-add'''
        self.callable1 = callable1

    def get_sampling_rate(self):
        ''' Gets the sampling rate of the capture device '''
        return int(self.caps1.get_property('caps')[0]['rate'])

    def start_grabbing(self):
        '''Called right at the start of the Activity'''
        self.start_sound_device()
        self.set_handoff_signal(True)

    def pause_grabbing(self):
        '''When Activity goes into background'''
        if self.we_are_logging:
            log.debug('We are logging... will not pause grabbing.')
        else:
            log.debug('Pause grabbing.')
            self.save_state()
            self.stop_sound_device()
        return

    def resume_grabbing(self):
        '''When Activity becomes active after going to background'''
        if self.we_are_logging:
            log.debug('We are logging... already grabbing.')
        else:
            log.debug('Restore grabbing.')
            self.restore_state()
            self.start_sound_device()
            self.set_handoff_signal(True)
        return

    def stop_grabbing(self):
        '''Not used ???'''
        self.stop_sound_device()
        self.set_handoff_signal(False)

    def save_state(self):
        '''Saves the state of all audio controls'''
        self.master = self.get_master()
        self.bias = self.get_bias()
        self.dc_mode = self.get_dc_mode()
        self.capture_gain = self.get_capture_gain()
        self.mic_boost = self.get_mic_boost()

    def restore_state(self):
        '''Put back all audio control settings from the saved state'''
        self.set_master(self.master)
        self.set_bias(self.bias)
        self.stop_grabbing()
        if self.channels > 1:
            self._unlink_sink_queues()
        self.set_dc_mode(self.dc_mode)
        self.start_grabbing()
        self.set_capture_gain(self.capture_gain)
        self.set_mic_boost(self.mic_boost)

    def amixer_set(self, control, state):
        ''' Direct call to amixer for old systems. '''
        if state:
            check_output(
                ['amixer', 'set', "%s" % (control), 'unmute'],
                'Problem with amixer set "%s" unmute' % (control))
        else:
            check_output(
                ['amixer', 'set', "%s" % (control), 'mute'],
                'Problem with amixer set "%s" mute' % (control))

    def mute_master(self):
        '''Mutes the Master Control'''
        self.amixer_set('Master', False)

    def unmute_master(self):
        '''Unmutes the Master Control'''
        self.amixer_set('Master', True)

    def set_master(self, master_val):
        '''Sets the Master gain slider settings
        master_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set'''
        check_output(
            ['amixer', 'set', 'Master', "%d%s" % (master_val, '%')],
            'Problem with amixer set Master')

    def get_master(self):
        '''Gets the MIC gain slider settings. The value returned is an
        integer between 0 and 100 and is an indicative of the
        percentage 0 to 100%'''
        output = check_output(['amixer', 'get', 'Master'],
                              'amixer: Could not get Master volume')
        if output is None:
            return 100
        else:
            pos = output.find('Front Left:')
            if pos == -1:
                pos = output.find('Mono:')
            output = output[pos:]
            output = output[output.find('[') + 1:]
            output = output[:output.find('%]')]
            return int(output)

    def set_bias(self, bias_state=False):
        '''Enables / disables bias voltage.'''
        if self.parent.hw == XO1:
            self.amixer_set('MIC Bias Enable', bias_state)
        else:
            self.amixer_set('V_REFOUT Enable', bias_state)

    def get_bias(self):
        '''Check whether bias voltage is enabled.'''
        if self.parent.hw == XO1:
            control = 'MIC Bias Enable'
        else:
            control = 'V_REFOUT Enable'
        output = check_output(['amixer', 'get', control],
                              'amixer: Could not get mic bias voltage')
        if output is None:
            return False
        else:
            output = output[output.find('Mono:'):]
            output = output[output.find('[') + 1:]
            output = output[:output.find(']')]
            if output == 'on':
                return True
            return False

    def set_dc_mode(self, dc_mode=False):
        '''Sets the DC Mode Enable control
        pass False to mute and True to unmute'''
        self.amixer_set('DC Mode Enable', dc_mode)

    def get_dc_mode(self):
        '''Returns the setting of DC Mode Enable control
        i.e. True: Unmuted and False: Muted'''
        output = check_output(['amixer', 'get', "DC Mode Enable"],
                              'amixer: Could not get DC Mode')
        if output is None:
            return False
        else:
            output = output[output.find('Mono:'):]
            output = output[output.find('[') + 1:]
            output = output[:output.find(']')]
            if output == 'on':
                return True
            return False

    def set_mic_boost(self, mic_boost=False):
        '''Set Mic Boost.
        for analog mic boost: True = +20dB, False = 0dB
        for mic1 boost: True = 8, False = 0'''
        self.amixer_set('Mic Boost (+20dB)', mic_boost)

    def get_mic_boost(self):
        '''Return Mic Boost setting.
        for analog mic boost: True = +20dB, False = 0dB
        for mic1 boost: True = 8, False = 0'''
        output = check_output(['amixer', 'get', "Mic Boost (+20dB)"],
                              'amixer: Could not get mic boost')
        if output is None:
            return False
        else:
            output = output[output.find('Mono:'):]
            output = output[output.find('[') + 1:]
            output = output[:output.find(']')]
            if output == 'on':
                return True
            return False

    def set_capture_gain(self, capture_val):
        '''Sets the Capture gain slider settings capture_val must be
        given as an integer between 0 and 100 indicating the
        percentage of the slider to be set'''
        check_output(
            ['amixer', 'set', 'Capture', "%d%s" % (capture_val, '%')],
            'Problem with amixer set Capture')

    def get_capture_gain(self):
        '''Gets the Capture gain slider settings. The value returned
        is an integer between 0 and 100 and is an indicative of the
        percentage 0 to 100%'''
        output = check_output(['amixer', 'get', 'Capture'],
                              'amixer: Could not get Capture level')
        if output is None:
            return 100
        else:
            pos = output.find('Front Left:')
            if pos == -1:
                pos = output.find('Mono:')
            output = output[pos:]
            output = output[output.find('[') + 1:]
            output = output[:output.find('%]')]
            return int(output)

    def set_mic_gain(self, mic_val):
        '''Sets the MIC gain slider settings mic_val must be given as
        an integer between 0 and 100 indicating the percentage of the
        slider to be set'''
        check_output(
            ['amixer', 'set', 'Mic', "%d%s" % (mic_val, '%')],
            'Problem with amixer set Mic')

    def get_mic_gain(self):
        '''Gets the MIC gain slider settings. The value returned is an
        integer between 0 and 100 and is an indicative of the
        percentage 0 to 100%'''
        output = check_output(['amixer', 'get', 'Mic'],
                              'amixer: Could not get mic gain level')
        if output is None:
            return 100
        else:
            output = output[output.find('Mono:'):]
            output = output[output.find('[') + 1:]
            output = output[:output.find('%]')]
            return int(output)

    def _set_sensor_type(self, mode=None, bias=None, gain=None, boost=None):
        '''Helper to modify (some) of the sensor settings.'''

        if mode is not None:
            self.set_dc_mode(mode)

        if bias is not None:
            self.set_bias(bias)

        if gain is not None:
            self.set_capture_gain(gain)

        if boost is not None:
            self.set_mic_boost(boost)

        self.save_state()

    def _on_activity_quit(self):
        '''When Activity quits'''
        self.set_mic_boost(QUIT_MIC_BOOST)
        self.set_dc_mode(QUIT_DC_MODE_ENABLE)
        self.set_capture_gain(QUIT_CAPTURE_GAIN)
        self.set_bias(QUIT_BIAS)
        self.stop_sound_device()

    def on_activity_quit(self):
        AudioGrab._on_activity_quit(self)
        check_output(
            ['amixer', 'set', 'Analog Mic Boost', "62%"],
            'restore Analog Mic Boost')


def check_output(command, warning):
    ''' Workaround for old systems without subprocess.check_output'''
    if hasattr(subprocess, 'check_output'):
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError:
            log.warning(warning)
            return None
    else:
        import subprocess

        cmd = ''
        for c in command:
            cmd += c
            cmd += ' '
        (status, output) = subprocess.getstatusoutput(cmd)
        if status != 0:
            log.warning(warning)
            return None
    return output
