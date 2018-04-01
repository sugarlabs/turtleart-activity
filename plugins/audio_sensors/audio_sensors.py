#!/usr/bin/env python
# Copyright (c) 2011, 2012 Walter Bender
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import gettext as _

try:
    from numpy.fft import rfft
    PITCH_AVAILABLE = True
except BaseException:
    PITCH_AVAILABLE = False

from plugins.plugin import Plugin

from plugins.audio_sensors.audiograb import (
    AudioGrab, SENSOR_DC_NO_BIAS, SENSOR_DC_BIAS, SENSOR_AC_BIAS)

from plugins.audio_sensors.ringbuffer import RingBuffer1d

from TurtleArt.tapalette import make_palette
from TurtleArt.taconstants import XO1, XO15, XO175, XO30, XO4
from TurtleArt.tautils import debug_output
from TurtleArt.taprimitive import (ConstantArg, Primitive)
from TurtleArt.tatype import TYPE_NUMBER

import logging
_logger = logging.getLogger('turtleart-activity audio sensors plugin')


def _avg(array, abs_value=False):
    ''' Calc. the average value of an array '''
    if len(array) == 0:
        return 0
    array_sum = 0
    if abs_value:
        for a in array:
            array_sum += abs(a)
    else:
        for a in array:
            array_sum += a
    return float(array_sum) / len(array)


class Audio_sensors(Plugin):

    def __init__(self, parent):
        Plugin.__init__(self)
        self._parent = parent
        self.audio_started = False
        self._sound_init = False
        self._resistance_init = False
        self._voltage_init = False
        self._status = True  # TODO: test for audio device
        # These flags are referenced by audiograb
        self.hw = self._parent.hw
        self.running_sugar = self._parent.running_sugar

    def setup(self):
        ''' set up audio-sensor-specific blocks '''
        self._sound = [0, 0]
        self._volume = [0, 0]
        self._pitch = [0, 0]
        self._resistance = [0, 0]
        self._voltage = [0, 0]
        self.max_samples = 1500
        self.input_step = 1
        self.ringbuffer = []

        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'),
                               position=6)
        hidden = True
        if self._status:
            hidden = False

        palette.add_block('sound',
                          hidden=hidden,
                          style='box-style',
                          label=_('sound'),
                          help_string=_('raw microphone input signal'),
                          value_block=True,
                          prim_name='sound')
        palette.add_block('volume',
                          hidden=hidden,
                          style='box-style',
                          label=_('loudness'),
                          help_string=_('microphone input volume'),
                          value_block=True,
                          prim_name='volume')

        self._parent.lc.def_prim(
            'sound', 0,
            Primitive(self.prim_sound,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(0)},
                      call_afterwards=self.after_sound))

        self._parent.lc.def_prim(
            'volume', 0,
            Primitive(self.prim_volume,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(0)},
                      call_afterwards=self.after_volume))

        hidden = True
        if PITCH_AVAILABLE and self._status:
            hidden = False

        palette.add_block('pitch',
                          hidden=hidden,
                          style='box-style',
                          label=_('pitch'),
                          help_string=_('microphone input pitch'),
                          value_block=True,
                          prim_name='pitch')
        self._parent.lc.def_prim(
            'pitch', 0,
            Primitive(self.prim_pitch,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(0)},
                      call_afterwards=self.after_pitch))

        hidden = True
        if self.hw in [XO1, XO15, XO175, XO4, XO30] and self._status:
            # Calibration based on http://bugs.sugarlabs.org/ticket/4649
            if self.hw == XO1:
                self.voltage_gain = 0.000022
                self.voltage_bias = 1.14
            elif self.hw == XO15:
                self.voltage_gain = -0.00015
                self.voltage_bias = 1.70
            elif self.hw == XO175:  # Range 0.01V to 3.01V
                self.voltage_gain = 0.0000516
                self.voltage_bias = 1.3598
            elif self.hw == XO4:  # Range 0.17V to 3.08V
                self.voltage_gain = 0.0004073
                self.voltage_bias = 1.6289
            else:  # XO 3.0
                self.voltage_gain = 0.000077
                self.voltage_bias = 0.72
            hidden = False

        palette.add_block('resistance',
                          hidden=hidden,
                          style='box-style',
                          label=_('resistance'),
                          help_string=_('microphone input resistance'),
                          prim_name='resistance')
        palette.add_block('voltage',
                          hidden=hidden,
                          style='box-style',
                          label=_('voltage'),
                          help_string=_('microphone input voltage'),
                          prim_name='voltage')

        hidden = True
        # Only add stereo capture for XO15 (broken on ARM #3675)
        if self.hw in [XO15] and self._status:
            hidden = False

        palette.add_block('resistance2',
                          hidden=hidden,
                          style='box-style',
                          label=_('resistance') + '2',
                          help_string=_('microphone input resistance'),
                          prim_name='resistance2')
        palette.add_block('voltage2',
                          hidden=hidden,
                          style='box-style',
                          label=_('voltage') + '2',
                          help_string=_('microphone input voltage'),
                          prim_name='voltage2')
        self._parent.lc.def_prim(
            'resistance', 0,
            Primitive(self.prim_resistance,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(0)},
                      call_afterwards=self.after_resistance))
        self._parent.lc.def_prim(
            'voltage', 0,
            Primitive(self.prim_voltage,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(0)},
                      call_afterwards=self.after_voltage))
        self._parent.lc.def_prim(
            'resistance2', 0,
            Primitive(self.prim_resistance,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(1)},
                      call_afterwards=self.after_resistance))
        self._parent.lc.def_prim(
            'voltage2', 0,
            Primitive(self.prim_voltage,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'channel': ConstantArg(1)},
                      call_afterwards=self.after_voltage))

        if self.hw in [XO15, XO175, XO30, XO4]:
            self.PARAMETERS = {
                SENSOR_AC_BIAS: (False, True, 80, True),
                SENSOR_DC_NO_BIAS: (True, False, 80, False),
                SENSOR_DC_BIAS: (True, True, 90, False)
            }
        elif self.hw == XO1:
            self.PARAMETERS = {
                SENSOR_AC_BIAS: (False, True, 40, True),
                SENSOR_DC_NO_BIAS: (True, False, 0, False),
                SENSOR_DC_BIAS: (True, True, 0, False)
            }
        else:
            self.PARAMETERS = {
                SENSOR_AC_BIAS: (None, True, 40, True),
                SENSOR_DC_NO_BIAS: (True, False, 80, False),
                SENSOR_DC_BIAS: (True, True, 90, False)
            }

    def start(self):
        ''' Start grabbing audio if there is an audio block in use '''
        if not self._status:
            return

        self._sound_init = False
        self._resistance_init = False
        self._voltage_init = False

        self._sound = [0, 0]
        self._volume = [0, 0]
        self._pitch = [0, 0]
        self._resistance = [0, 0]
        self._voltage = [0, 0]

        if self.audio_started:
            self.audiograb.stop_grabbing()

    def new_buffer(self, buf, channel=0):
        ''' Append a new buffer to the ringbuffer '''
        self.ringbuffer[channel].append(buf)
        return True

    def stop(self):
        ''' This gets called by the stop button '''
        if self._status and self.audio_started:
            self.audiograb.on_activity_quit()  # reset all setting
        self.audio_started = False

    def goto_background(self):
        ''' This gets called when your process is sent to the background '''
        pass

    def return_to_foreground(self):
        ''' This gets called when your process returns from the background '''
        pass

    def quit(self):
        ''' This gets called by the quit button '''
        if self._status and self.audio_started:
            self.audiograb.on_activity_quit()

    def _status_report(self):
        debug_output(
            'Reporting audio sensor status: %s' % (str(self._status)),
            self._parent.running_sugar)
        return self._status

    # Block primitives

    def prim_sound(self, channel=0):
        if not self._status:
            return 0

        self._init_sound()

        self._prim_sound(0)
        # Return average of both channels if sampling in stereo
        if self._channels == 2:
            self._prim_sound(1)
            return (self._sound[0] + self._sound[1]) / 2.0
        else:
            return self._sound[0]

    def _init_sound(self):
        if not self._sound_init:
            mode, bias, gain, boost = self.PARAMETERS[SENSOR_AC_BIAS]
            self.audiograb = AudioGrab(self.new_buffer, self,
                                       mode, bias, gain, boost)
            self._channels = self.audiograb.channels
            for i in range(self._channels):
                self.ringbuffer.append(RingBuffer1d(self.max_samples,
                                                    dtype='int16'))
            self.audiograb.start_grabbing()
            self.audio_started = True
            self._sound_init = True

    def _prim_sound(self, channel):
        ''' return raw mic in value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            self._sound[channel] = float(buf[0])
        else:
            self._sound[channel] = 0

    def after_sound(self, channel=0):
        if self._parent.lc.update_values:
            self._parent.lc.update_label_value('sound', self._sound[channel])

    def prim_volume(self, channel=0):
        if not self._status:
            return 0

        self._init_sound()

        self._prim_volume(0)
        # Return average of both channels if sampling in stereo
        if self._channels == 2:
            self._prim_volume(1)
            return (self._volume[0] + self._volume[1]) / 2.0
        else:
            return self._volume[0]

    def _prim_volume(self, channel):
        ''' return raw mic in value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            self._volume[channel] = float(_avg(buf, abs_value=True))
        else:
            self._volume[channel] = 0

    def after_volume(self, channel=0):
        if self._parent.lc.update_values:
            self._parent.lc.update_label_value('volume', self._volume[channel])

    def prim_pitch(self, channel=0):
        if not self._status:
            return 0

        self._init_sound()

        self._prim_pitch(0)
        # Return average of both channels if sampling in stereo
        if self._channels == 2:
            self._prim_pitch(1)
            return (self._pitch[0] + self._pitch[1]) / 2.0
        else:
            return self._pitch[0]

    def _prim_pitch(self, channel):
        ''' return raw mic in value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            buf = rfft(buf)
            buf = abs(buf)
            maxi = buf.argmax()
            if maxi == 0:
                self._pitch[channel] = 0
            else:  # Simple interpolation
                a, b, c = buf[maxi - 1], buf[maxi], buf[maxi + 1]
                maxi -= a / float(a + b + c)
                maxi += c / float(a + b + c)
                self._pitch[channel] = maxi * 48000 / (len(buf) * 2)
        else:
            self._pitch[channel] = 0

    def after_pitch(self, channel=0):
        if self._parent.lc.update_values:
            self._parent.lc.update_label_value('pitch', self._pitch[channel])

    def prim_resistance(self, channel=0):
        if self.hw not in [XO1, XO15, XO175, XO30, XO4] or not self._status:
            return 0

        if not self._resistance_init:
            mode, bias, gain, boost = self.PARAMETERS[SENSOR_DC_BIAS]
            self.audiograb = AudioGrab(self.new_buffer, self,
                                       mode, bias, gain, boost)
            self._channels = self.audiograb.channels
            for i in range(self._channels):
                self.ringbuffer.append(RingBuffer1d(self.max_samples,
                                                    dtype='int16'))
            self.audiograb.start_grabbing()
            self.audio_started = True
            self._resistance_init = True

        if self.hw in [XO1, XO4]:
            self._prim_resistance(0)
            return self._resistance[0]
        elif self.hw == XO15:
            self._prim_resistance(channel)
            return self._resistance[channel]
        # For XO175: channel assignment is seemingly random
        # (#3675), one of them will be 0
        else:
            self._prim_resistance(0)
            if self._resistance[0] != 999999999:
                return self._resistance[0]
            else:
                self._prim_resistance(1)
                return self._resistance[1]

    def _prim_resistance(self, channel):
        ''' return resistance sensor value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            # See http://bugs.sugarlabs.org/ticket/552#comment:7
            # and http://bugs.sugarlabs.org/ticket/4649
            avg_buf = float(_avg(buf))
            if self.hw == XO1:
                self._resistance[channel] = \
                    2.718 ** ((avg_buf * 0.000045788) + 8.0531)
            elif self.hw == XO15:
                if avg_buf > 0:
                    self._resistance[channel] = (420000000 / avg_buf) - 13500
                else:
                    self._resistance[channel] = 420000000
            elif self.hw == XO175:  # Range 0 to inf ohms
                if avg_buf < 30519:
                    self._resistance[channel] = \
                        (92000000. / (30519 - avg_buf)) - 1620
                else:
                    self._resistance[channel] = 999999999
            elif self.hw == XO4:  # Range 0 to inf ohms
                if avg_buf < 6629:
                    self._resistance[channel] = \
                        (50000000. / (6629 - avg_buf)) - 3175
                else:
                    self._resistance[channel] = 999999999
            else:  # XO 3.0
                if avg_buf < 30514:
                    self._resistance[channel] = \
                        (46000000. / (30514 - avg_buf)) - 1150
                else:
                    self._resistance[channel] = 999999999
            if self._resistance[channel] < 0:
                self._resistance[channel] = 0
        else:
            self._resistance[channel] = 0

    def after_resistance(self, channel=0):
        if self._parent.lc.update_values:
            self._parent.lc.update_label_value(
                ['resistance', 'resistance2'][channel],
                self._resistance[channel])

    def prim_voltage(self, channel=0):
        if self.hw not in [XO1, XO15, XO175, XO30, XO4] or not self._status:
            return 0

        if not self._voltage_init:
            mode, bias, gain, boost = self.PARAMETERS[SENSOR_DC_NO_BIAS]
            self.audiograb = AudioGrab(self.new_buffer, self,
                                       mode, bias, gain, boost)
            self._channels = self.audiograb.channels
            for i in range(self._channels):
                self.ringbuffer.append(RingBuffer1d(self.max_samples,
                                                    dtype='int16'))
            self.audiograb.start_grabbing()
            self.audio_started = True
            self._voltage_init = True

        if self.hw in [XO1, XO4]:
            self._prim_voltage(0)
            return self._voltage[0]
        elif self.hw == XO15:
            self._prim_voltage(channel)
            return self._voltage[channel]
        # FIXME: For XO175: channel assignment is seemingly random
        # (#3675), one of them will be 0
        else:
            self._prim_voltage(0)
            if self._voltage[0] != 0:
                return self._voltage[0]
            else:
                self._prim_voltage(1)
                return self._voltage[1]

    def _prim_voltage(self, channel):
        ''' return voltage sensor value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            self._voltage[channel] = \
                float(_avg(buf)) * self.voltage_gain + self.voltage_bias
        else:
            self._voltage[channel] = 0

    def after_voltage(self, channel=0):
        if self._parent.lc.update_values:
            self._parent.lc.update_label_value(
                ['voltage', 'voltage2'][channel],
                self._voltage[channel])
