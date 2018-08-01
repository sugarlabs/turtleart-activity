#!/usr/bin/env python
# Copyright (c) 2011 Walter Bender
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

import os

from gettext import gettext as _

from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.tautils import debug_output
from TurtleArt.taprimitive import Primitive

import logging
_logger = logging.getLogger('turtleart-activity accelerometer plugin')


ACCELEROMETER_DEVICE = '/sys/devices/platform/lis3lv02d/position'


class Accelerometer(Plugin):

    def __init__(self, parent):
        Plugin.__init__(self)
        self._parent = parent
        if os.path.exists(ACCELEROMETER_DEVICE):
            self._status = True
        else:
            self._status = False
        self.running_sugar = self._parent.running_sugar

        self.variant = self._parent.variant

        if self.variant == 'Art':
            self.hidden = not self._status
            self.palette_name = 'sensor'
            self.translation = _('sensor')
            self.colors = ["#FF6060", "#A06060"]
            self.help_string = _('Palette of sensor blocks')
            self.position = 6

        elif self.variant == 'Confusion':
            self.hidden = True
            self.palette_name = 'extras'
            self.translation = _('extras')
            self.colors = colors=["#FF0000", "#A00000"]
            self.help_string = _('Palette of extra options')
            self.position = 8

    def setup(self):
        # set up accelerometer specific blocks
        palette = make_palette(self.palette_name,
                               colors=self.colors,
                               help_string=self.help_string,
                               position=self.position,
                               translation=self.translation)

        palette.add_block('xyz',
                          hidden=self.hidden,
                          style='basic-style-extended-vertical',
                          label=_('acceleration'),
                          help_string=_(
                                  'push acceleration in x, y, z to heap'),
                          prim_name='xyz')

        self._parent.lc.def_prim(
            'xyz', 0,
            Primitive(self.prim_xyz))

    def _status_report(self):
        debug_output('Reporting accelerator status: %s' % (str(self._status)))
        return self._status

    # Block primitives used in talogo

    def prim_xyz(self):
        ''' push accelerometer xyz to stack '''
        if not self._status:
            self._parent.lc.heap.append(0)
            self._parent.lc.heap.append(0)
            self._parent.lc.heap.append(0)
        else:
            fh = open(ACCELEROMETER_DEVICE)
            string = fh.read()
            xyz = string[1:-2].split(',')
            self._parent.lc.heap.append(float(xyz[2]) / 18)
            self._parent.lc.heap.append(float(xyz[1]) / 18)
            self._parent.lc.heap.append(float(xyz[0]) / 18)
            fh.close()
