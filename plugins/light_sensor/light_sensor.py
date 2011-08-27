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

import os

from gettext import gettext as _

from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import primitive_dictionary
from TurtleArt.tautils import debug_output

import logging
_logger = logging.getLogger('turtleart-activity light-sensor plugin')


LIGHT_SENSOR_DEVICE = '/sys/devices/platform/olpc-ols.0/power_state'


class Light_sensor(Plugin):

    def __init__(self, parent):
        self._parent = parent
        if os.path.exists(LIGHT_SENSOR_DEVICE):
            self._status = True
        else:
            self._status = False
        self.running_sugar = self._parent.running_sugar

    def setup(self):
        # set up light-sensor specific blocks
        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'))

        primitive_dictionary['lightsensor'] = self.prim_lightsensor
        if self._status:
            palette.add_block('lightsensor',
                              style='box-style',
                              label=_('brightness'),
                              help_string=\
                                  _('light level detected by light sensor'),
                              prim_name='lightsensor')
        else:
            palette.add_block('lightsensor',
                              style='box-style',
                              label=_('brightness'),
                              help_string=\
                                  _('light level detected by light sensor'),
                              hidden=True,
                              prim_name='lightsensor')

        self._parent.lc.def_prim(
            'lightsensor', 0,
            lambda self: primitive_dictionary['lightsensor']())

    def _status_report(self):
        debug_output('Reporting light-sensor status: %s' % (str(self._status)))
        return self._status

    # Block primitives used in talogo

    def prim_lightsensor(self):
        ''' push accelerometer xyz to stack '''
        if not self._status:
            return -1
        else:
            fh = open(LIGHT_SENSOR_DEVICE)
            string = fh.read()
            fh.close()
            return float(string)
