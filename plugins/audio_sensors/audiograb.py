#! /usr/bin/python
#
# Author:  Arjun Sarwal   arjun@laptop.org
# Copyright (C) 2007, Arjun Sarwal
# Copyright (C) 2009-12 Walter Bender
# Copyright (C) 2009, Benjamin Berg, Sebastian Berg
# Copyright (C) 2009, Sayamindu Dasgupta
# Copyright (C) 2010, Sascha Silbe
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

import pygst
import gst
import gst.interfaces
from numpy import fromstring
import subprocess
import traceback
from string import find
from threading import Timer

from TurtleArt.taconstants import XO1, XO4
from TurtleArt.tautils import debug_output

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

# Capture modes
SENSOR_AC_NO_BIAS = 'external'
SENSOR_AC_BIAS = 'sound'
SENSOR_DC_NO_BIAS = 'voltage'
SENSOR_DC_BIAS = 'resistance'


class AudioGrab():
    """ The interface between measure and the audio device """

    def __init__(self, callable1, parent,
                 mode=None, bias=None, gain=None, boost=None):
        """ Initialize the class: callable1 is a data buffer;
            parent is the parent class"""

        self.callable1 = callable1
        self.parent = parent
        self.sensor = None

        self.temp_buffer = [0]

        self.rate = RATE
        # Force XO1 and XO4 to use just 1 channel
        if self.parent.hw in [XO1, XO4]:
            self.channels = 1
        else:
            self.channels = None

        self._dc_control = None
        self._mic_bias_control = None
        self._capture_control = None
        self._mic_boost_control = None
        self._labels_available = True  # Query controls for device names

        self._query_mixer()
        # If Channels was not found in the Capture controller, guess.
        if self.channels is None:
            debug_output('Guessing there are 2 channels',
                         self.parent.running_sugar)
            self.channels = 2

        # Set mixer to known state
        self.set_dc_mode(DC_MODE_ENABLE)
        self.set_bias(BIAS)
        self.set_capture_gain(CAPTURE_GAIN)
        self.set_mic_boost(MIC_BOOST)

        self.master = self.get_master()
        self.dc_mode = self.get_dc_mode()
        self.bias = self.get_bias()
        self.capture_gain = self.get_capture_gain()
        self.mic_boost = self.get_mic_boost()

        # Set mixer to desired state
        self._set_sensor_type(mode, bias, gain, boost)
        self.dc_mode = self.get_dc_mode()
        self.bias = self.get_bias()
        self.capture_gain = self.get_capture_gain()
        self.mic_boost = self.get_mic_boost()

        # Set up gstreamer pipeline
        self._pad_count = 0
        self.pads = []
        self.queue = []
        self.fakesink = []
        self.pipeline = gst.Pipeline('pipeline')
        self.alsasrc = gst.element_factory_make('alsasrc', 'alsa-source')
        self.pipeline.add(self.alsasrc)
        self.caps1 = gst.element_factory_make('capsfilter', 'caps1')
        self.pipeline.add(self.caps1)
        caps_str = 'audio/x-raw-int,rate=%d,channels=%d,depth=16' % (
            RATE, self.channels)
        self.caps1.set_property('caps', gst.caps_from_string(caps_str))
        if self.channels == 1:
            self.fakesink.append(gst.element_factory_make('fakesink', 'fsink'))
            self.pipeline.add(self.fakesink[0])
            self.fakesink[0].connect('handoff', self.on_buffer, 0)
            self.fakesink[0].set_property('signal-handoffs', True)
            gst.element_link_many(self.alsasrc, self.caps1, self.fakesink[0])
        else:
            if not hasattr(self, 'splitter'):
                self.splitter = gst.element_factory_make('deinterleave')
                self.pipeline.add(self.splitter)
                self.splitter.set_properties('keep-positions=true', 'name=d')
                self.splitter.connect('pad-added', self._splitter_pad_added)
                gst.element_link_many(self.alsasrc, self.caps1, self.splitter)
            for i in range(self.channels):
                self.queue.append(gst.element_factory_make('queue'))
                self.pipeline.add(self.queue[i])
                self.fakesink.append(gst.element_factory_make('fakesink'))
                self.pipeline.add(self.fakesink[i])
                self.fakesink[i].connect('handoff', self.on_buffer, i)
                self.fakesink[i].set_property('signal-handoffs', True)

        self.dont_queue_the_buffer = False

        # Timer for interval sampling and switch to indicate when to capture
        self.capture_timer = None
        self.capture_interval_sample = False

    def _query_mixer(self):
        self._mixer = gst.element_factory_make('alsamixer')
        rc = self._mixer.set_state(gst.STATE_PAUSED)
        assert rc == gst.STATE_CHANGE_SUCCESS

        # Query the available controls
        tracks_list = self._mixer.list_tracks()
        if hasattr(tracks_list[0].props, 'untranslated_label'):
            self._capture_control = self._find_control(['capture', 'axi'])
            self._dc_control = self._find_control(['dc mode'])
            self._mic_bias_control = self._find_control(['mic bias',
                                                         'dc input bias',
                                                         'v_refout'])
            self._mic_boost_control = self._find_control(['mic boost',
                                                          'mic1 boost',
                                                          'mic boost (+20db)',
                                                          'internal mic boost',
                                                          'analog mic boost'])
            self._mic_gain_control = self._find_control(['mic'])
            self._master_control = self._find_control(['master'])
        else:  # Use hardwired values
            self._labels_available = False

    def _unlink_sink_queues(self):
        ''' Build the sink pipelines '''

        # If there were existing pipelines, unlink them
        for i in range(self._pad_count):
            try:
                self.splitter.unlink(self.queue[i])
                self.queue[i].unlink(self.fakesink[i])
            except:
                traceback.print_exc()

        # Build the new pipelines
        self._pad_count = 0
        self.pads = []

    def _splitter_pad_added(self, element, pad):
        ''' Seems to be the case that ring is right channel 0,
                                       tip is  left channel 1'''
        '''
        debug_output('splitter pad %d added' % (self._pad_count),
                     self.parent.running_sugar)
        '''
        self.pads.append(pad)
        if self._pad_count < self.channels:
            pad.link(self.queue[self._pad_count].get_pad('sink'))
            self.queue[self._pad_count].get_pad('src').link(
                self.fakesink[self._pad_count].get_pad('sink'))
            self._pad_count += 1
        else:
            debug_output('ignoring channels > %d' % (self.channels),
                         self.parent.running_sugar)

    def set_handoff_signal(self, handoff_state):
        '''Sets whether the handoff signal would generate an interrupt
        or not'''
        for i in range(len(self.fakesink)):
            self.fakesink[i].set_property('signal-handoffs', handoff_state)

    def _new_buffer(self, buf, channel):
        ''' Use a new buffer '''
        if not self.dont_queue_the_buffer:
            self.temp_buffer = buf
            self.callable1(buf, channel=channel)
        else:
            pass

    def on_buffer(self, element, data_buffer, pad, channel):
        '''The function that is called whenever new data is available
        This is the signal handler for the handoff signal'''
        temp_buffer = fromstring(data_buffer, 'int16')
        if not self.dont_queue_the_buffer:
            self._new_buffer(temp_buffer, channel=channel)
        return False

    def start_sound_device(self):
        '''Start or Restart grabbing data from the audio capture'''
        gst.event_new_flush_start()
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop_sound_device(self):
        '''Stop grabbing data from capture device'''
        gst.event_new_flush_stop()
        self.pipeline.set_state(gst.STATE_NULL)

    def sample_now(self):
        ''' Log the current sample now. This method is called from the
        capture_timer object when the interval expires. '''
        self.capture_interval_sample = True
        self.make_timer()

    def set_buffer_interval_logging(self, interval=0):
        '''Sets the number of buffers after which a buffer needs to be
        emitted'''
        self.buffer_interval_logging = interval

    def set_sampling_rate(self, sr):
        '''Sets the sampling rate of the capture device
        Sampling rate must be given as an integer for example 16000 for
        setting 16Khz sampling rate
        The sampling rate would be set in the device to the nearest available'''
        self.pause_grabbing()
        caps_str = 'audio/x-raw-int,rate=%d,channels=%d,depth=16' % (
            sr, self.channels)
        self.caps1.set_property('caps', gst.caps_from_string(caps_str))
        self.resume_grabbing()

    def get_sampling_rate(self):
        '''Gets the sampling rate of the capture device'''
        return int(self.caps1.get_property('caps')[0]['rate'])

    def set_callable1(self, callable1):
        '''Sets the callable to the drawing function for giving the
        data at the end of idle-add'''
        self.callable1 = callable1

    def start_grabbing(self):
        '''Called right at the start of the Activity'''
        self.start_sound_device()
        self.set_handoff_signal(True)

    def pause_grabbing(self):
        '''When Activity goes into background'''
        self.save_state()
        self.stop_sound_device()

    def resume_grabbing(self):
        '''When Activity becomes active after going to background'''
        self.start_sound_device()
        self.resume_state()
        self.set_handoff_signal(True)

    def stop_grabbing(self):
        '''Not used ???'''
        self.stop_sound_device()
        self.set_handoff_signal(False)

    def _find_control(self, prefixes):
        '''Try to find a mixer control matching one of the prefixes.

        The control with the best match (smallest difference in length
        between label and prefix) will be returned. If no match is found,
        None is returned.
        '''
        def best_prefix(label, prefixes):
            matches =\
                [len(label) - len(p) for p in prefixes if label.startswith(p)]
            if not matches:
                return None

            matches.sort()
            return matches[0]

        controls = []
        for track in self._mixer.list_tracks():
            label = track.props.untranslated_label.lower()
            diff = best_prefix(label, prefixes)
            if diff is not None:
                controls.append((track, diff))

        controls.sort(key=lambda e: e[1])
        if controls:
            '''
            debug_output('Found control: %s' %\
                          (str(controls[0][0].props.untranslated_label)),
                         self.parent.running_sugar)
            '''
            if self.channels is None:
                if hasattr(controls[0][0], 'num_channels'):
                    channels = controls[0][0].num_channels
                    if channels > 0:
                        self.channels = channels
                        '''
                        debug_output('setting channels to %d' % (self.channels),
                                     self.parent.running_sugar)
                        '''

            return controls[0][0]

        return None

    def save_state(self):
        '''Saves the state of all audio controls'''
        self.master = self.get_master()
        self.bias = self.get_bias()
        self.dc_mode = self.get_dc_mode()
        self.capture_gain = self.get_capture_gain()
        self.mic_boost = self.get_mic_boost()

    def resume_state(self):
        '''Put back all audio control settings from the saved state'''
        self.set_master(self.master)
        self.set_bias(self.bias)
        self.set_dc_mode(self.dc_mode)
        self.set_capture_gain(self.capture_gain)
        self.set_mic_boost(self.mic_boost)

    def _get_mute(self, control, name, default):
        '''Get mute status of a control'''
        if not control:
            return default
        return bool(control.flags & gst.interfaces.MIXER_TRACK_MUTE)

    def _set_mute(self, control, name, value):
        '''Mute a control'''
        if not control:
            return
        self._mixer.set_mute(control, value)

    def _get_volume(self, control, name):
        '''Get volume of a control and convert to a scale of 0-100'''
        if not control:
            return 100
        volume = self._mixer.get_volume(control)
        if type(volume) == tuple:
            hw_volume = volume[0]
        else:
            hw_volume = volume
        min_vol = control.min_volume
        max_vol = control.max_volume
        if max_vol == min_vol:
            percent = 100
        else:
            percent = (hw_volume - min_vol) * 100 // (max_vol - min_vol)
        return percent

    def _set_volume(self, control, name, value):
        '''Sets the level of a control on a scale of 0-100'''
        if not control:
            return
        # convert value to scale of control
        min_vol = control.min_volume
        max_vol = control.max_volume
        if min_vol != max_vol:
            hw_volume = value * (max_vol - min_vol) // 100 + min_vol
            self._mixer.set_volume(control,
                                   (hw_volume,) * control.num_channels)

    def amixer_set(self, control, state):
        ''' Direct call to amixer for old systems. '''
        if state:
            output = check_output(
                ['amixer', 'set', "%s" % (control), 'unmute'],
                'Problem with amixer set "%s" unmute' % (control),
                self.parent.running_sugar)
        else:
            output = check_output(
                ['amixer', 'set', "%s" % (control), 'mute'],
                'Problem with amixer set "%s" mute' % (control),
                self.parent.running_sugar)

    def mute_master(self):
        '''Mutes the Master Control'''
        if self._labels_available and self.parent.hw != XO1:
            self._set_mute(self._master_control, 'Master', True)
        else:
            self.amixer_set('Master', False)

    def unmute_master(self):
        '''Unmutes the Master Control'''
        if self._labels_available and self.parent.hw != XO1:
            self._set_mute(self._master_control, 'Master', True)
        else:
            self.amixer_set('Master', True)

    def set_master(self, master_val):
        '''Sets the Master gain slider settings
        master_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set'''
        if self._labels_available:
            self._set_volume(self._master_control, 'Master', master_val)
        else:
            output = check_output(
                ['amixer', 'set', 'Master', "%d%s" % (master_val, '%')],
                'Problem with amixer set Master',
                self.parent.running_sugar)

    def get_master(self):
        '''Gets the MIC gain slider settings. The value returned is an
        integer between 0-100 and is an indicative of the percentage 0 - 100%'''
        if self._labels_available:
            return self._get_volume(self._master_control, 'master')
        else:
            output = check_output(['amixer', 'get', 'Master'],
                                  'amixer: Could not get Master volume',
                                  self.parent.running_sugar)
            if output is None:
                return 100
            else:
                output = output[find(output, 'Front Left:'):]
                output = output[find(output, '[') + 1:]
                output = output[:find(output, '%]')]
                return int(output)

    def set_bias(self, bias_state=False):
        '''Enables / disables bias voltage.'''
        if self._labels_available and self.parent.hw != XO1:
            if self._mic_bias_control is None:
                return
            # If there is a flag property, use set_mute
            if self._mic_bias_control not in self._mixer.list_tracks() or \
               hasattr(self._mic_bias_control.props, 'flags'):
                self._set_mute(
                    self._mic_bias_control, 'Mic Bias', not bias_state)
            # We assume that values are sorted from lowest (=off) to highest.
            # Since they are mixed strings ('Off', '50%', etc.), we cannot
            # easily ensure this by sorting with the default sort order.
            elif bias_state:  # Otherwise, set with volume
                self._mixer.set_volume(self._mic_bias_control,
                                       self._mic_bias_control.max_volume)
            else:
                self._mixer.set_volume(self._mic_bias_control,
                                       self._mic_bias_control.min_volume)
        elif not self._labels_available:
            self.amixer_set('V_REFOUT Enable', bias_state)
        else:
            self.amixer_set('MIC Bias Enable', bias_state)

    def get_bias(self):
        '''Check whether bias voltage is enabled.'''
        if self._labels_available:
            if self._mic_bias_control is None:
                return False
            if self._mic_bias_control not in self._mixer.list_tracks() or \
               hasattr(self._mic_bias_control.props, 'flags'):
                return not self._get_mute(
                    self._mic_bias_control, 'Mic Bias', False)
            value = self._mixer.get_volume(self._mic_bias_control)
            if value == self._mic_bias_control.min_volume:
                return False
            return True
        else:
            output = check_output(['amixer', 'get', "V_REFOUT Enable"],
                                  'amixer: Could not get mic bias voltage',
                                  self.parent.running_sugar)
            if output is None:
                return False
            else:
                output = output[find(output, 'Mono:'):]
                output = output[find(output, '[') + 1:]
                output = output[:find(output, ']')]
                if output == 'on':
                    return True
                return False

    def set_dc_mode(self, dc_mode=False):
        '''Sets the DC Mode Enable control
        pass False to mute and True to unmute'''
        if self._labels_available and self.parent.hw != XO1:
            if self._dc_control is not None:
                self._set_mute(self._dc_control, 'DC mode', not dc_mode)
        else:
            self.amixer_set('DC Mode Enable', dc_mode)

    def get_dc_mode(self):
        '''Returns the setting of DC Mode Enable control
        i.e. True: Unmuted and False: Muted'''
        if self._labels_available and self.parent.hw != XO1:
            if self._dc_control is not None:
                return not self._get_mute(self._dc_control, 'DC mode', False)
            else:
                return False
        else:
            output = check_output(['amixer', 'get', "DC Mode Enable"],
                                  'amixer: Could not get DC Mode',
                                  self.parent.running_sugar)
            if output is None:
                return False
            else:
                output = output[find(output, 'Mono:'):]
                output = output[find(output, '[') + 1:]
                output = output[:find(output, ']')]
                if output == 'on':
                    return True
                return False

    def set_mic_boost(self, mic_boost=False):
        '''Set Mic Boost.
        True = +20dB, False = 0dB'''
        if self._labels_available:
            if self._mic_boost_control is None:
                return
            # If there is a volume, use set volume
            if hasattr(self._mic_boost_control, 'min_volume'):
                if mic_boost:
                    self._set_volume(self._mic_boost_control, 'boost', 100)
                else:
                    self._set_volume(self._mic_boost_control, 'boost', 0)
            # Else if there is a flag property, use set_mute
            elif self._mic_boost_control not in self._mixer.list_tracks() or \
               hasattr(self._mic_boost_control.props, 'flags'):
                self._set_mute(
                    self._mic_boost_control, 'Mic Boost', not mic_boost)
        else:
            self.amixer_set('Mic Boost (+20dB)', mic_boost)

    def get_mic_boost(self):
        '''Return Mic Boost setting.
        True = +20dB, False = 0dB'''
        if self._labels_available:
            if self._mic_boost_control is None:
                return False
            if self._mic_boost_control not in self._mixer.list_tracks() or \
               hasattr(self._mic_boost_control.props, 'flags'):
                return not self._get_mute(
                    self._mic_boost_control, 'Mic Boost', False)
            else:  # Compare to min value
                value = self._mixer.get_volume(self._mic_boost_control)
                if value != self._mic_boost_control.min_volume:
                    return True
                return False
        else:
            output = check_output(['amixer', 'get', "Mic Boost (+20dB)"],
                                  'amixer: Could not get mic boost',
                                  self.parent.running_sugar)
            if output is None:
                return False
            else:
                output = output[find(output, 'Mono:'):]
                output = output[find(output, '[') + 1:]
                output = output[:find(output, ']')]
                if output == 'on':
                    return True
                return False

    def set_capture_gain(self, capture_val):
        '''Sets the Capture gain slider settings
        capture_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set'''
        if self._labels_available and self.parent.hw != XO1:
            if self._capture_control is not None:
                self._set_volume(self._capture_control, 'Capture', capture_val)
        else:
            output = check_output(
                ['amixer', 'set', 'Capture', "%d%s" % (capture_val, '%')],
                'Problem with amixer set Capture',
                self.parent.running_sugar)

    def get_capture_gain(self):
        '''Gets the Capture gain slider settings. The value returned is an
        integer between 0-100 and is an indicative of the percentage 0 - 100%'''
        if self._labels_available:
            if self._capture_control is not None:
                return self._get_volume(self._capture_control, 'Capture')
            else:
                return 0
        else:
            output = check_output(['amixer', 'get', 'Capture'],
                                  'amixer: Could not get Capture level',
                                  self.parent.running_sugar)
            if output is None:
                return 100
            else:
                output = output[find(output, 'Front Left:'):]
                output = output[find(output, '[') + 1:]
                output = output[:find(output, '%]')]
                return int(output)

    def set_mic_gain(self, mic_val):
        '''Sets the MIC gain slider settings
        mic_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set'''
        if self._labels_available and self.parent.hw != XO1:
            self._set_volume(self._mic_gain_control, 'Mic', mic_val)
        else:
            output = check_output(
                ['amixer', 'set', 'Mic', "%d%s" % (mic_val, '%')],
                'Problem with amixer set Mic',
                self.parent.running_sugar)

    def get_mic_gain(self):
        '''Gets the MIC gain slider settings. The value returned is an
        integer between 0-100 and is an indicative of the percentage 0 - 100%'''
        if self._labels_available and self.parent.hw != XO1:
            return self._get_volume(self._mic_gain_control, 'Mic')
        else:
            output = check_output(['amixer', 'get', 'Mic'],
                                  'amixer: Could not get mic gain level',
                                  self.parent.running_sugar)
            if output is None:
                return 100
            else:
                output = output[find(output, 'Mono:'):]
                output = output[find(output, '[') + 1:]
                output = output[:find(output, '%]')]
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

    def on_activity_quit(self):
        '''When Activity quits'''
        self.set_mic_boost(QUIT_MIC_BOOST)
        self.set_dc_mode(QUIT_DC_MODE_ENABLE)
        self.set_capture_gain(QUIT_CAPTURE_GAIN)
        self.set_bias(QUIT_BIAS)
        self.stop_sound_device()


def check_output(command, warning, running_sugar=True):
    ''' Workaround for old systems without subprocess.check_output'''
    if hasattr(subprocess, 'check_output'):
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError:
            debug_output(warning, running_sugar)
            return None
    else:
        import commands

        cmd = ''
        for c in command:
            cmd += c
            cmd += ' '
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            debug_output(warning, running_sugar)
            return None
    return output
