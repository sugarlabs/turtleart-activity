#!/usr/bin/env python
# Copyright (C) 2010,11 Emiliano Pastorino <epastorino@plan.ceibal.edu.uy>
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

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gettext import gettext as _

from plugins.rfid.rfidutils import strhex2bin, strbin2dec, find_device
from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.tautils import debug_output
from TurtleArt.taprimitive import Primitive
from TurtleArt.tatype import TYPE_STRING

import logging

_logger = logging.getLogger('turtleart-activity RFID plugin')

HAL_SERVICE = 'org.freedesktop.Hal'
HAL_MGR_PATH = '/org/freedesktop/Hal/Manager'
HAL_MGR_IFACE = 'org.freedesktop.Hal.Manager'
HAL_DEV_IFACE = 'org.freedesktop.Hal.Device'
REGEXP_SERUSB = '/org/freedesktop/Hal/devices/usb_device[' \
                'a-z,A-Z,0-9,_]*serial_usb_[0-9]'


class Rfid(Plugin):

    def __init__(self, parent):
        Plugin.__init__(self)
        self._parent = parent
        self._status = False

        """
        The following code will initialize a USB RFID reader. Please note that
        in order to make this initialization function work, it is necessary to
        set the permission for the ttyUSB device to 0666. You can do this by
        adding a rule to /etc/udev/rules.d

        As root (using sudo or su), copy the following text into a new file in
        /etc/udev/rules.d/94-ttyUSB-rules

        KERNEL=="ttyUSB[0-9]",MODE="0666"

        You only have to do this once.
        """

        self.rfid_connected = False
        self.rfid_device = find_device()
        self.rfid_idn = ''

        if self.rfid_device is not None:
            _logger.info("RFID device found")
            self.rfid_connected = self.rfid_device.do_connect()
            if self.rfid_connected:
                self.rfid_device.connect("tag-read", self._tag_read_cb)
                self.rfid_device.connect("disconnected", self._disconnected_cb)

            loop = DBusGMainLoop()
            bus = dbus.SystemBus(mainloop=loop)
            hmgr_iface = dbus.Interface(
                bus.get_object(
                    HAL_SERVICE,
                    HAL_MGR_PATH),
                HAL_MGR_IFACE)

            hmgr_iface.connect_to_signal('DeviceAdded', self._device_added_cb)

            self._status = True

    def setup(self):
        # set up RFID-specific blocks
        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'),
                               position=6)

        if self._status:
            palette.add_block('rfid',
                              style='box-style',
                              label=_('RFID'),
                              help_string=_('read value from RFID device'),
                              value_block=True,
                              prim_name='rfid')
        else:
            palette.add_block('rfid',
                              hidden=True,
                              style='box-style',
                              label=_('RFID'),
                              help_string=_('read value from RFID device'),
                              value_block=True,
                              prim_name='rfid')

        self._parent.lc.def_prim(
            'rfid', 0,
            Primitive(self.prim_read_rfid,
                      return_type=TYPE_STRING,
                      call_afterwards=self.after_rfid))

    def _status_report(self):
        debug_output('Reporting RFID status: %s' % (str(self._status)))
        return self._status

    def _device_added_cb(self, path):
        """
        Called from hal connection when a new device is plugged.
        """
        if not self.rfid_connected:
            self.rfid_device = find_device()
            _logger.debug("DEVICE_ADDED: %s" % self.rfid_device)
            if self.rfid_device is not None:
                _logger.debug("DEVICE_ADDED: RFID device is not None!")
                self.rfid_connected = self._device.do_connect()
            if self.rfid_connected:
                _logger.debug("DEVICE_ADDED: Connected!")
                self.rfid_device.connect("tag-read", self._tag_read_cb)
                self.rfid_device.connect("disconnected", self._disconnected_cb)

    def _disconnected_cb(self, device, text):
        """
        Called when the device is disconnected.
        """
        self.rfid_connected = False
        self.rfid_device = None

    def _tag_read_cb(self, device, tagid):
        """
        Callback for "tag-read" signal. Receives the read tag id.
        """
        idbin = strhex2bin(tagid)
        self.rfid_idn = strbin2dec(idbin[26:64])
        while self.rfid_idn.__len__() < 9:
            self.rfid_idn = '0' + self.rfid_idn
        print(tagid, idbin, self.rfid_idn)
        self.tw.lc.update_label_value('rfid', self.rfid_idn)

    # Block primitives used in talogo

    def prim_read_rfid(self):
        if self._status:
            return self.rfid_idn
        else:
            return '0'

    def after_rfid(self):
        if self._parent.lc.update_values:
            self._parent.lc.update_label_value('rfid', self.rfid_idn)
