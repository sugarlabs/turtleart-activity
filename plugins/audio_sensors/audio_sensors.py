#!/usr/bin/env python
#Copyright (c) 2011 Walter Bender
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
from TurtleArt.taconstants import XO1, XO15, XO175
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
                               help_string=_('Palette of sensor blocks'))

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
        if self.hw in [XO1, XO15, XO175] and self._status:
            if self.hw == XO1:
                self.voltage_gain = 0.00002225
                self.voltage_bias = 1.140
            elif self.hw == XO15:
                self.voltage_gain = -0.0001471
                self.voltage_bias = 1.695
            else:  # FIXME: Calibrate 1.75
                self.voltage_gain = -0.0001471
                self.voltage_bias = 1.695
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
            palette.add_block('resistance',
                              hidden=True,
                              style='box-style',
                              label=_('resistance') + '2',
                              help_string=_('microphone input resistance'),
                              prim_name='resistance2')
            palette.add_block('voltage',
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
        if self.hw == XO175:
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
            return  # no audio blocks in play
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
        ''' return mic in value '''
        if not self._status:
            return 0
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            volume = float(_avg(buf, abs_value=True))
            self._parent.lc.update_label_value('volume', volume)
            return volume
        else:
            return 0

    def prim_sound(self, channel):
        ''' return raw mic in value '''
        if not self._status:
            return 0
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            sound = float(buf[0])
            self._parent.lc.update_label_value('sound', sound)
            return sound
        else:
            return 0

    def prim_pitch(self, channel):
        ''' return index of max value in fft of mic in values '''
        if not PITCH_AVAILABLE or not self._status:
            return 0
        buf = []
        for i in range(4):
            buf = append(
                buf, self.ringbuffer[channel].read(None, self.input_step))
        if len(buf) > 0:
            r = []
            for j in rfft(buf):
                r.append(abs(j))
            # Convert output to Hertz
            pitch = r.index(max(r)) * 48000 / len(buf)
            self._parent.lc.update_label_value('pitch', pitch)
            return pitch
        else:
            return 0

    def prim_resistance(self, channel):
        ''' return resistance sensor value '''
        if not self.hw in [XO1, XO15, XO175] or not self._status:
            return 0
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            # TODO: test this calibration on XO 1.5, XO 1.75
            if self.hw == XO1:
                resistance = 2.718 ** ((float(_avg(buf)) * 0.000045788) + \
                                           8.0531)
            else:
                avg_buf = float(_avg(buf))
                if avg_buf > 0:
                    resistance = (420000000 / avg_buf) - 13500
                else:
                    resistance = 420000000
            if channel == 0:
                self._parent.lc.update_label_value('resistance', resistance)
            else:
                self._parent.lc.update_label_value('resistance2', resistance)
            return resistance
        else:
            return 0

    def prim_voltage(self, channel):
        ''' return voltage sensor value '''
        if not self.hw in [XO1, XO15, XO175] or not self._status:
            return 0
        buf = self.ringbuffer[channel].read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            voltage = float(_avg(buf)) * self.voltage_gain + self.voltage_bias
            if channel == 0:
                self._parent.lc.update_label_value('voltage', voltage)
            else:
                self._parent.lc.update_label_value('voltage2', voltage)
            return voltage
        else:
            return 0
