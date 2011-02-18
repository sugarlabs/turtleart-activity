#!/usr/bin/env python
#Copyright (C) 2010 Emiliano Pastorino <epastorino@plan.ceibal.edu.uy>
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

import os

from gettext import gettext as _

from rfid.rfidutils import strhex2bin, strbin2dec, find_device

from plugin import Plugin
from TurtleArt.taconstants import PALETTES, PALETTE_NAMES, BOX_STYLE_MEDIA, \
    CONTENT_BLOCKS, BLOCK_NAMES, DEFAULTS, SPECIAL_NAMES, HELP_STRINGS, \
    BOX_STYLE
from TurtleArt.talogo import VALUE_BLOCKS, MEDIA_BLOCKS_DICTIONARY, \
    PLUGIN_DICTIONARY

import logging
_logger = logging.getLogger('turtleart-activity RFID plugin')

HAL_SERVICE = 'org.freedesktop.Hal'
HAL_MGR_PATH = '/org/freedesktop/Hal/Manager'
HAL_MGR_IFACE = 'org.freedesktop.Hal.Manager'
HAL_DEV_IFACE = 'org.freedesktop.Hal.Device'
REGEXP_SERUSB = '\/org\/freedesktop\/Hal\/devices\/usb_device['\
                'a-z,A-Z,0-9,_]*serial_usb_[0-9]'


class Rfid_plugin(Plugin):

    def __init__(self, parent):
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
            hmgr_iface = dbus.Interface(bus.get_object(HAL_SERVICE,
                HAL_MGR_PATH), HAL_MGR_IFACE)

            hmgr_iface.connect_to_signal('DeviceAdded', self._device_added_cb)

            self._status = True

    def setup(self):
        # set up camera-specific blocks
        if self._self_test():
            PALETTES[PALETTE_NAMES.index('sensor')].append('rfid')
            BOX_STYLE.append('rfid')
            BLOCK_NAMES['rfid'] = [_('RFID')]
            HELP_STRINGS['rfid'] = _("read value from RFID device")
            PRIMITIVES['rfid'] = 'rfid'
            VALUE_BLOCKS.append('rfid')
            PLUGIN_DICTIONARY['rfid'] = self.prim_read_rfid
            self._parent.lc._def_prim('rfid', 0,
                lambda self: PLUGIN_DICTIONARY['rfid'](True))

    def stop(self):
        # Ths gets called by the stop button
        pass

    def _self_test(self):
        print 'reporting RFID status %s' % (str(self._status))
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
        print tagid, idbin, self.rfid_idn

    # Block primitives used in talogo

    def prim_read_rfid(self):
        if self._self_test():
            return self.rfid_idn
