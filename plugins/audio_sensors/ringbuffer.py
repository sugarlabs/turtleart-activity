#    Copyright (C) 2009, Benjamin Berg, Sebastian Berg
#    Copyright (C) 2010, Walter Bender
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import numpy as np


class RingBuffer1d(object):
    """This class implements an array being written in as a ring and that can
    be read from continuously ending with the newest data or starting with the
    oldest. It returns a numpy array copy of the data;
    """

    def __init__(self, length, dtype=None):
        """Initialize the 1 dimensional ring buffer with the given lengths.
        The initial values are all 0s
        """
        self.offset = 0

        self._data = np.zeros(length, dtype=dtype)

        self.stored = 0

    def fill(self, number):
        self._data.fill(number)
        self.offset = 0

    def append(self, data):
        """Append to the ring buffer (and overwrite old data). If len(data)
        is greater then the ring buffers length, the newest data takes
        precedence.
        """
        data = np.asarray(data)

        if len(self._data) == 0:
            return

        if len(data) >= len(self._data):
            self._data[:] = data[-len(self._data):]
            self.offset = 0
            self.stored = len(self._data)

        elif len(self._data) - self.offset >= len(data):
            self._data[self.offset: self.offset + len(data)] = data
            self.offset = self.offset + len(data)
            self.stored += len(data)
        else:
            self._data[self.offset:] = data[:len(self._data) - self.offset]
            self._data[:len(data) - (len(self._data) - self.offset)] = \
                data[-len(data) + (len(self._data) - self.offset):]
            self.offset = len(data) - (len(self._data) - self.offset)
            self.stored += len(data)

        if len(self._data) <= self.stored:
            self.read = self._read

    def read(self, number=None, step=1):
        """Read the ring Buffer. Number can be positive or negative.
        Positive values will give the latest information, negative values will
        give the newest added information from the buffer. (in normal order)

        Before the buffer is filled once: This returns just None
        """
        return np.array([])

    def _read(self, number=None, step=1):
        """Read the ring Buffer. Number can be positive or negative.
        Positive values will give the latest information, negative values will
        give the newest added information from the buffer. (in normal order)
        """
        if number is None:
            number = len(self._data) // step

        number *= step
        assert abs(number) <= len(self._data), \
            'Number to read*step must be smaller then length'

        if number < 0:
            if abs(number) <= self.offset:
                return self._data[self.offset + number:self.offset:step]

            spam = (self.offset - 1) % step

            return np.concatenate(
                (self._data[step - spam - 1 + self.offset + number::step],
                 self._data[spam:self.offset:step]))

        if number - (len(self._data) - self.offset) > 0:
            spam = ((self.offset + number) - self.offset - 1) % step
            return np.concatenate(
                (self._data[self.offset:self.offset + number:step],
                 self._data[spam:number - (
                     len(self._data) - self.offset):step]))

        return self._data[self.offset:self.offset + number:step].copy()
