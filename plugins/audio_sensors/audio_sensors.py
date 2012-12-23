#!/usr/bin/env python
#Copyright (c) 2011, 2012 Walter Bender
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
    from numpy import append
    from numpy.fft import rfft
    PITCH_AVAILABLE = True
except:
    PITCH_AVAILABLE = False

from plugins.plugin import Plugin

from plugins.audio_sensors.audiograb import AudioGrab, \
    SENSOR_DC_NO_BIAS, SENSOR_DC_BIAS, SENSOR_AC_BIAS

from plugins.audio_sensors.ringbuffer import RingBuffer1d

from TurtleArt.tapalette import make_palette
from TurtleArt.taconstants import XO1, XO15, XO175, XO30, XO4
from TurtleArt.talogo import primitive_dictionary
from TurtleArt.tautils import debug_output

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
        self._parent = parent
        self._status = True  # TODO: test for audio device
        # These flags are referenced by audiograb
        self.hw = self._parent.hw
        self.running_sugar = self._parent.running_sugar

    def setup(self):
        ''' set up audio-sensor-specific blocks '''
        self.max_samples = 1500
        self.input_step = 1

        self.ringbuffer = []

        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'),
                               position=6)

        primitive_dictionary['sound'] = self.prim_sound
        primitive_dictionary['volume'] = self.prim_volume
        if self._status:
            palette.add_block('sound',
                              style='box-style',
                              label=_('sound'),
                              help_string=_('raw microphone input signal'),
                              value_block=True,
                              prim_name='sound')

            palette.add_block('volume',
                              style='box-style',
                              label=_('loudness'),
                              help_string=_('microphone input volume'),
                              value_block=True,
                              prim_name='volume')
        else:
            palette.add_block('sound',
                              hidden=True,
                              style='box-style',
                              label=_('sound'),
                              help_string=_('raw microphone input signal'),
                              value_block=True,
                              prim_name='sound')
            palette.add_block('volume',
                              hidden=True,
                              style='box-style',
                              label=_('loudness'),
                              help_string=_('microphone input volume'),
                              value_block=True,
                              prim_name='volume')

        self._parent.lc.def_prim(
            'sound', 0, lambda self: primitive_dictionary['sound'](0))
        self._parent.lc.def_prim(
            'volume', 0, lambda self: primitive_dictionary['volume'](0))

        primitive_dictionary['pitch'] = self.prim_pitch
        if PITCH_AVAILABLE and self._status:
            palette.add_block('pitch',
                              style='box-style',
                              label=_('pitch'),
                              help_string=_('microphone input pitch'),
                              value_block=True,
                              prim_name='pitch')
        else:
            palette.add_block('pitch',
                              hidden=True,
                              style='box-style',
                              label=_('pitch'),
                              help_string=_('microphone input pitch'),
                              value_block=True,
                              prim_name='pitch')
        self._parent.lc.def_prim('pitch', 0,
                                 lambda self: primitive_dictionary['pitch'](0))

        primitive_dictionary['resistance'] = self.prim_resistance
        primitive_dictionary['voltage'] = self.prim_voltage
        if self.hw in [XO1, XO15, XO175, XO4, XO30] and self._status:
            if self.hw == XO1:
                self.voltage_gain = 0.000022
                self.voltage_bias = 1.14
            elif self.hw == XO15:
                self.voltage_gain = -0.00015
                self.voltage_bias = 1.70
            elif self.hw in [XO175, XO4]:  # recalibrate in light of #3675?
                self.voltage_gain = 0.000071
                self.voltage_bias = 0.55
            else:  # XO 3.0
                self.voltage_gain = 0.000077
                self.voltage_bias = 0.72
            palette.add_block('resistance',
                              style='box-style',
                              label=_('resistance'),
                              help_string=_('microphone input resistance'),
                              value_block=True,
                              prim_name='resistance')
            palette.add_block('voltage',
                              style='box-style',
                              label=_('voltage'),
                              help_string=_('microphone input voltage'),
                              value_block=True,
                              prim_name='voltage')
        else:
            palette.add_block('resistance',
                              hidden=True,
                              style='box-style',
                              label=_('resistance'),
                              help_string=_('microphone input resistance'),
                              prim_name='resistance')
            palette.add_block('voltage',
                              hidden=True,
                              style='box-style',
                              label=_('voltage'),
                              help_string=_('microphone input voltage'),
                              prim_name='voltage')

        # FIXME: Only add stereo capture for XO15 (broken on ARM #3675)
        if self.hw in [XO15] and self._status:
            palette.add_block('resistance2',
                              style='box-style',
                              label=_('resistance') + '2',
                              help_string=_('microphone input resistance'),
                              value_block=True,
                              prim_name='resistance2')
            palette.add_block('voltage2',
                              style='box-style',
                              label=_('voltage') + '2',
                              help_string=_('microphone input voltage'),
                              value_block=True,
                              prim_name='voltage2')
        else:
            palette.add_block('resistance2',
                              hidden=True,
                              style='box-style',
                              label=_('resistance') + '2',
                              help_string=_('microphone input resistance'),
                              prim_name='resistance2')
            palette.add_block('voltage2',
                              hidden=True,
                              style='box-style',
                              label=_('voltage') + '2',
                              help_string=_('microphone input voltage'),
                              prim_name='voltage2')
        self._parent.lc.def_prim(
            'resistance', 0,
            lambda self: primitive_dictionary['resistance'](0))
        self._parent.lc.def_prim(
            'voltage', 0, lambda self: primitive_dictionary['voltage'](0))
        self._parent.lc.def_prim(
            'resistance2', 0,
            lambda self: primitive_dictionary['resistance'](1))
        self._parent.lc.def_prim(
            'voltage2', 0, lambda self: primitive_dictionary['voltage'](1))

        self.audio_started = False
        if self.hw in [XO175, XO30, XO4]:
            self.PARAMETERS = {
                SENSOR_AC_BIAS: (False, True, 80, True),
                SENSOR_DC_NO_BIAS: (True, False, 80, False),
                SENSOR_DC_BIAS: (True, True, 90, False)
                }
        elif self.hw == XO15:
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
        if self.audio_started:
            self.audiograb.stop_grabbing()
        if len(self._parent.block_list.get_similar_blocks(
                'block', ['volume', 'sound', 'pitch'])) > 0:
            mode, bias, gain, boost = self.PARAMETERS[SENSOR_AC_BIAS]
        elif len(self._parent.block_list.get_similar_blocks(
                'block', ['resistance', 'resistance2'])) > 0:
            mode, bias, gain, boost = self.PARAMETERS[SENSOR_DC_BIAS]
        elif len(self._parent.block_list.get_similar_blocks(
                'block', ['voltage', 'voltage2'])) > 0:
            mode, bias, gain, boost = self.PARAMETERS[SENSOR_DC_NO_BIAS]
        else:
            return  # No audio blocks in use.
        self.audiograb = AudioGrab(self.new_buffer, self,
                                   mode, bias, gain, boost)
        self._channels = self.audiograb.channels
        for i in range(self._channels):
            self.ringbuffer.append(RingBuffer1d(self.max_samples,
                                                dtype='int16'))
        self.audiograb.start_grabbing()
        self.audio_started = True

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

    # Block primitives used in talogo

    def prim_volume(self, channel):
        if not self._status:
            return 0
        # Return average of both channels if sampling in stereo
        if self._channels == 2:
            chan0 = self._prim_volume(0)
            chan1 = self._prim_volume(1)
            return (chan0 + chan1) / 2
        else:
            return self._prim_volume(0)

    def _prim_volume(self, channel):
        ''' return mic in value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            volume = float(_avg(buf, abs_value=True))
            self._parent.lc.update_label_value('volume', volume)
            return volume
        else:
            return 0

    def prim_sound(self, channel):
        if not self._status:
            return 0
        # Return average of both channels if sampling in stereo
        if self._channels == 2:
            chan0 = self._prim_sound(0)
            chan1 = self._prim_sound(1)
            return (chan0 + chan1) / 2
        else:
            return self._prim_sound(0)

    def _prim_sound(self, channel):
        ''' return raw mic in value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            sound = float(buf[0])
            self._parent.lc.update_label_value('sound', sound)
            return sound
        else:
            return 0

    def prim_pitch(self, channel):
        if not PITCH_AVAILABLE or not self._status:
            return 0
        # Return average of both channels if sampling in stereo
        if self._channels == 2:
            chan0 = self._prim_pitch(0)
            chan1 = self._prim_pitch(1)
            return (chan0 + chan1) / 2
        else:
            return self._prim_pitch(0)

    def _prim_pitch(self, channel):
        ''' return index of max value in fft of mic in values '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            buf = rfft(buf)
            buf = abs(buf)
            maxi = buf.argmax()
            if maxi == 0:
                pitch = 0
            else:  # Simple interpolation
                a, b, c = buf[maxi - 1], buf[maxi], buf[maxi + 1]
                maxi -= a / float(a + b + c)
                maxi += c / float(a + b + c)
                pitch = maxi * 48000 / (len(buf) * 2)
            
            self._parent.lc.update_label_value('pitch', pitch)
            return pitch
        else:
            return 0

    def prim_resistance(self, channel):
        if not self.hw in [XO1, XO15, XO175, XO30, XO4] or not self._status:
            return 0
        if self.hw == XO1:
            resistance = self._prim_resistance(0)
            self._update_resistance_labels(0, resistance)
            return resistance
        elif self.hw == XO15:
            resistance = self._prim_resistance(channel)
            self._update_resistance_labels(channel, resistance)
            return resistance
        # FIXME: For ARM (XO175, XO4) channel assignment is seemingly
        # random (#3675), so sum both channels
        else:
            chan0 = self._prim_resistance(0)
            chan1 = self._prim_resistance(1)
            resistance = (chan0 + chan1) / 2.
            self._update_resistance_labels(0, resistance)
            return resistance

    def _prim_resistance(self, channel):
        ''' return resistance sensor value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            # TODO: test this calibration on XO 1.5, XO 1.75
            avg_buf = float(_avg(buf))
            if self.hw == XO1:
                resistance = 2.718 ** ((avg_buf * 0.000045788) + 8.0531)
            elif self.hw == XO15:
                if avg_buf > 0:
                    resistance = (420000000 / avg_buf) - 13500
                else:
                    resistance = 420000000
            elif self.hw in [XO175, XO4]:
                if avg_buf < 30700:
                    resistance = .12 * ((180000000 / (30700 - avg_buf)) - 3150)
                else:
                    resistance = 999999999
            else:  # XO 3.0
                if avg_buf < 30514:
                    resistance = (46000000 / (30514 - avg_buf)) - 1150
                else:
                    resistance = 999999999
            if resistance < 0:
                resistance = 0
            return resistance
        else:
            return 0

    def _update_resistance_labels(self, channel, resistance):
        if channel == 0:
            self._parent.lc.update_label_value('resistance', resistance)
        else:
            self._parent.lc.update_label_value('resistance2', resistance)

    def prim_voltage(self, channel):
        if not self.hw in [XO1, XO15, XO175, XO30, XO4] or not self._status:
            return 0
        if self.hw == XO1:
            voltage = self._prim_voltage(0)
            self._update_voltage_labels(0, voltage)
            return voltage
        elif self.hw == XO15:
            voltage = self._prim_voltage(channel)
            self._update_voltage_labels(channel, voltage)
            return voltage
        # FIXME: For ARM (XO175, XO4) channel assignment is seemingly
        # random (#3675), so sum both channels
        else:
            chan0 = self._prim_voltage(0)
            chan1 = self._prim_voltage(1)
            voltage = (chan0 + chan1) / 2.
            self._update_voltage_labels(0, voltage)
            return voltage

    def _prim_voltage(self, channel):
        ''' return voltage sensor value '''
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            voltage = float(_avg(buf)) * self.voltage_gain + self.voltage_bias
            return voltage
        else:
            return 0

    def _update_voltage_labels(self, channel, voltage):
        if channel == 0:
            self._parent.lc.update_label_value('voltage', voltage)
        else:
            self._parent.lc.update_label_value('voltage2', voltage)
