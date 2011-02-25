#!/usr/bin/env python
#Copyright (c) 2011 Walter Bender

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

import gst
try:
    from numpy import append
    from numpy.fft import rfft
    PITCH_AVAILABLE = True
except:
    PITCH_AVAILABLE = False
import gtk

from gettext import gettext as _

from plugin import Plugin

from audio.audiograb import AudioGrab_Unknown, AudioGrab_XO1, AudioGrab_XO15, \
    SENSOR_DC_NO_BIAS, SENSOR_DC_BIAS

from audio.ringbuffer import RingBuffer1d

from TurtleArt.taprimitive import Primitive
from TurtleArt.taconstants import BOX_STYLE, XO1, XO15
from TurtleArt.talogo import PLUGIN_DICTIONARY
from TurtleArt.tautils import get_path

import logging
_logger = logging.getLogger('turtleart-activity audio sensors plugin')


def _avg(array, abs_value=False):
    """ Calc. the average value of an array """
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


class Audio_sensors_plugin(Plugin):

    def __init__(self, parent):
        self._parent = parent
        self.hw = self._parent.hw
        self.running_sugar = self._parent.running_sugar
        self._status = True  # TODO: test for audio device

    def setup(self):
        # set up audio-sensor-specific blocks
        if not self._status:
            return

        self.max_samples = 1500
        self.input_step = 1

        self.ringbuffer = RingBuffer1d(self.max_samples, dtype='int16')
        if self.hw == XO1:
            self.voltage_gain = 0.00002225
            self.voltage_bias = 1.140
        elif self.hw == XO15:
            self.voltage_gain = -0.0001471
            self.voltage_bias = 1.695

        sound = Primitive('sound')
        sound.set_palette('sensor')
        sound.set_style(BOX_STYLE)
        sound.set_label(_('sound'))
        sound.set_help(_('raw microphone input signal'))
        sound.set_value_block(True)
        sound.set_prim_name('sound')
        PLUGIN_DICTIONARY['sound'] = self.prim_sound
        self._parent.lc._def_prim('sound', 0,
                                  lambda self: PLUGIN_DICTIONARY['sound']())
        sound.add_prim()

        volume = Primitive('volume')
        volume.set_palette('sensor')
        volume.set_style(BOX_STYLE)
        volume.set_label(_('volume'))
        volume.set_help(_('microphone input volume'))
        volume.set_value_block(True)
        volume.set_prim_name('volume')
        PLUGIN_DICTIONARY['volume'] = self.prim_volume
        self._parent.lc._def_prim('volume', 0,
                                  lambda self: PLUGIN_DICTIONARY['volume']())
        volume.add_prim()

        pitch = Primitive('pitch')
        if PITCH_AVAILABLE:
            pitch.set_palette('sensor')
        pitch.set_style(BOX_STYLE)
        pitch.set_label(_('pitch'))
        pitch.set_help(_('microphone input pitch'))
        pitch.set_value_block(True)
        pitch.set_prim_name('pitch')
        PLUGIN_DICTIONARY['pitch'] = self.prim_pitch
        self._parent.lc._def_prim('pitch', 0,
                                  lambda self: PLUGIN_DICTIONARY['pitch']())
        pitch.add_prim()

        if self.hw in [XO1, XO15]:
            resistance = Primitive('resistance')
            resistance.set_palette('sensor')
            resistance.set_style(BOX_STYLE)
            resistance.set_label(_('resistance'))
            resistance.set_help(_('sensor input resistance'))
            resistance.set_value_block(True)
            resistance.set_prim_name('resistance')
            PLUGIN_DICTIONARY['resistance'] = self.prim_resistance
            self._parent.lc._def_prim('resistance', 0,
                lambda self: PLUGIN_DICTIONARY['resistance']())
            resistance.add_prim()

            voltage = Primitive('voltage')
            voltage.set_palette('sensor')
            voltage.set_style(BOX_STYLE)
            voltage.set_label(_('voltage'))
            voltage.set_help(_('sensor input voltage'))
            voltage.set_value_block(True)
            voltage.set_prim_name('voltage')
            PLUGIN_DICTIONARY['voltage'] = self.prim_voltage
            self._parent.lc._def_prim('voltage', 0,
                lambda self: PLUGIN_DICTIONARY['voltage']())
            voltage.add_prim()

        self.audio_started = False

    def start(self):
        # This gets called by the start button
        if not self._status:
            return
        """ Start grabbing audio if there is an audio block in use """
        if len(self._parent.block_list.get_similar_blocks('block',
            ['volume', 'sound', 'pitch', 'resistance', 'voltage'])) > 0:
            if self.audio_started:
                self.audiograb.resume_grabbing()
            else:
                if self.hw == XO15:
                    self.audiograb = AudioGrab_XO15(self.new_buffer, self)
                elif self.hw == XO1:
                    self.audiograb = AudioGrab_XO1(self.new_buffer, self)
                else:
                    self.audiograb = AudioGrab_Unknown(self.new_buffer, self)
                self.audiograb.start_grabbing()
                self.audio_started = True
        self._update_audio_mode()

    def new_buffer(self, buf):
        """ Append a new buffer to the ringbuffer """
        self.ringbuffer.append(buf)
        return True

    def _update_audio_mode(self):
        """ If there are sensor blocks, set the appropriate audio mode """
        if not hasattr(self._parent.lc, 'value_blocks'):
            return
        for name in ['sound', 'volume', 'pitch']:
            if name in self._parent.lc.value_blocks:
                if len(self._parent.lc.value_blocks[name]) > 0:
                    self.audiograb.set_sensor_type()
                    return
        if 'resistance' in self._parent.lc.value_blocks:
            if len(self._parent.lc.value_blocks['resistance']) > 0:
                self.audiograb.set_sensor_type(SENSOR_DC_BIAS)
                return
        if 'voltage' in self._parent.lc.value_blocks:
            if len(self._parent.lc.value_blocks['voltage']) > 0:
                self.audiograb.set_sensor_type(SENSOR_DC_NO_BIAS)
                return

    def stop(self):
        # This gets called by the stop button
        if self._status:
            if self.audio_started:
                self.audiograb.pause_grabbing()

    def goto_background(self):
        # This gets called when your process is sent to the background
        pass

    def return_to_foreground(self):
        # This gets called when your process returns from the background
        pass

    def quit(self):
        # This gets called by the quit button
        self.stop()

    def _status_report(self):
        print 'Reporting audio sensor status: %s' % (str(self._status))
        return self._status

    # Block primitives used in talogo

    def prim_volume(self):
        """ return mic in value """
        #TODO: Adjust gain for different HW
        buf = self.ringbuffer.read(None, self.input_step)
        if len(buf) > 0:
            volume = float(_avg(buf, abs_value=True))
            self._parent.lc.update_label_value('volume', volume)
            return volume
        else:
            return 0

    def prim_sound(self):
        """ return raw mic in value """
        buf = self.ringbuffer.read(None, self.input_step)
        if len(buf) > 0:
            sound = float(buf[0])
            self._parent.lc.update_label_value('sound', sound)
            return sound
        else:
            return 0

    def prim_pitch(self):
        """ return index of max value in fft of mic in values """
        if not PITCH_AVAILABLE:
            return 0
        buf = []
        for i in range(4):
            buf = append(buf, self.ringbuffer.read(None, self.input_step))
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

    def prim_resistance(self):
        """ return resistance sensor value """
        buf = self.ringbuffer.read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            # TODO: test this calibration on XO 1.5
            if self.hw == XO1:
                resistance = 2.718 ** ((float(_avg(buf)) * 0.000045788) + \
                                           8.0531)
            else:
                avg_buf = float(_avg(buf))
                if avg_buf > 0:
                    resistance = (420000000 / avg_buf) - 13500
                else:
                    resistance = 420000000
            self._parent.lc.update_label_value('resistance', resistance)
            return resistance
        else:
            return 0

    def prim_voltage(self):
        """ return voltage sensor value """
        buf = self.ringbuffer.read(None, self.input_step)
        if len(buf) > 0:
            # See <http://bugs.sugarlabs.org/ticket/552#comment:7>
            voltage = float(_avg(buf)) * self.voltage_gain + self.voltage_bias
            self._parent.lc.update_label_value('voltage', voltage)
            return voltage
        else:
            return 0
