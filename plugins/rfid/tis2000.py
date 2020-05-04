from .device import RFIDDevice
from .serial import Serial
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import re
from time import sleep

HAL_SERVICE = 'org.freedesktop.Hal'
HAL_MGR_PATH = '/org/freedesktop/Hal/Manager'
HAL_MGR_IFACE = 'org.freedesktop.Hal.Manager'
HAL_DEV_IFACE = 'org.freedesktop.Hal.Device'
REGEXP_SERUSB = '/org/freedesktop/Hal/devices/usb_device['\
                'a-z,A-Z,0-9,_]*serial_usb_[0-9]'

STATE_WAITING = 0
STATE_WAITING2 = 1
STATE_READING = 2


class RFIDReader(RFIDDevice):
    """
    TIS-2000 interface.
    """

    def __init__(self):

        RFIDDevice.__init__(self)
        self.last_tag = ""
        self.ser = Serial()
        self.device = ''
        self.device_path = ''
        self._connected = False
        self._state = STATE_WAITING

        loop = DBusGMainLoop()
        self.bus = dbus.SystemBus(mainloop=loop)
        hmgr_iface = dbus.Interface(
            self.bus.get_object(
                HAL_SERVICE,
                HAL_MGR_PATH),
            HAL_MGR_IFACE)

        hmgr_iface.connect_to_signal('DeviceRemoved', self._device_removed_cb)

    def get_present(self):
        """
        Checks if TI-S2000 device is present.
        Returns True if so, False otherwise.
        """
        hmgr_if = dbus.Interface(
            self.bus.get_object(
                HAL_SERVICE,
                HAL_MGR_PATH),
            HAL_MGR_IFACE)
        tiusb_devices = set(hmgr_if.FindDeviceStringMatch(
            'serial.type', 'usb')) & \
            set(hmgr_if.FindDeviceStringMatch(
                'info.product', 'TUSB3410 Microcontroller'))
        for i in tiusb_devices:
            tiusb_if = dbus.Interface(self.bus.get_object(HAL_SERVICE, i),
                                      HAL_DEV_IFACE)
            if tiusb_if.PropertyExists('linux.device_file'):
                self.device = str(tiusb_if.GetProperty('linux.device_file'))
                self.device_path = i
                return True
        return False

    def do_connect(self):
        """
        Connects to the device.
        Returns True if successfull, False otherwise.
        """
        retval = False
        if self.get_present():
            try:
                self.ser = Serial(self.device, 9600, timeout=0.1)
                self._connected = True
                self._escape()
                self._clear()
                self._format()
                gobject.idle_add(self._loop)
                retval = True
            except BaseException:
                self._connected = False
        return retval

    def do_disconnect(self):
        """
        Disconnect from the device.
        """
        self.ser.close()
        self._connected = False

    def read_tag(self):
        """
        Returns the last read value.
        """
        return self.last_tag

    def write_tag(self, hexval):
        """
        Usage: write_tag(hexval)

            Writes the hexadecimal string "hexval" into the tag.
            Returns True if successfull, False otherwise.
        """
        # self.ser.flushInput()
        reg = re.compile('([^0-9A-F]+)')
        if not (hexval.__len__() == 16 and reg.findall(hexval) == []):
            return False
        self.ser.read(100)
        self.ser.write('P')
        for i in hexval:
            self.ser.write(i)
        sleep(1)
        resp = self.ser.read(64)
        resp = resp.split()[0]
        if resp == "P0":
            return True
        else:
            return False

    def _escape(self):
        """
        Sends the scape command to the TIS-2000 device.
        """
        try:
            # self.ser.flushInput()
            self.ser.read(100)
            self.ser.write('\x1B')
            resp = self.ser.read()
            if resp == 'E':
                return True
            else:
                return False
        except BaseException:
            return False

    def _format(self):
        """
        Sends the format command to the TIS-2000 device.
        """
        try:
            # self.ser.flushInput()
            self.ser.read(100)
            self.ser.write('F')
            resp = self.ser.read()
            if resp == 'F':
                return True
            else:
                return False
        except BaseException:
            return False

    def _clear(self):
        """
        Sends the clear command to the TIS-2000 device.
        """
        try:
            # self.ser.flushInput()
            self.ser.read(100)
            self.ser.write('C')
            resp = self.ser.read()
            if resp == 'C':
                return True
            else:
                return False
        except BaseException:
            return False

    def get_version(self):
        """
        Sends the version command to the TIS-2000 device and returns
        a string with the device version.
        """
        # self.ser.flushInput()
        self.ser.read(100)
        self.ser.write('V')
        version = []
        tver = ""
        while True:
            resp = self.ser.read()
            if resp == '\x0A' or resp == '':
                break
            if resp != '\n' and resp != '\r':
                version.append(resp)
        for i in version:
            tver = tver + i
        if tver != "":
            return tver
        return "Unknown"

    def _device_removed_cb(self, path):
        """
        Called when a device is removed.
        Checks if the removed device is itself and emits the "disconnected"
        signal if so.
        """
        if path == self.device_path:
            self.device_path = ''
            self.ser.close()
            self._connected = False
            self.emit("disconnected", "TIS-2000")

    def _loop(self):
        """
        Threaded loop for reading data sent from the TIS-2000.
        """
        if not self._connected:
            return False

        if self._state is STATE_WAITING:
            data = self.ser.read()
            if data in ['W', 'R']:
                self._state = STATE_WAITING2
            return True

        elif self._state is STATE_WAITING2:
            data = self.ser.read()
            if data.isspace():
                self._state = STATE_READING
            else:
                self._clear()
                self._state = STATE_WAITING
            return True

        elif self._state is STATE_READING:
            data = self.ser.read(16)
            if data.__len__() < 16:
                self._clear()
                self._state = STATE_WAITING
            else:
                reg = re.compile('([^0-9A-F]+)')
                if reg.findall(data) == []:
                    self.emit("tag-read", data)
                    self.last_tag = data
                self._clear()
                self._state = STATE_WAITING
            return True
        return True

# Testing
# if __name__ == '__main__':
#    def handler(device, idhex):
#        """
#        Handler for "tag-read" signal.
#        Prints the tag id.
#        """
#        print "ID: ", idhex
#
#    dev = RFIDReader()
#    if dev.get_present():
#        dev.do_connect()
#        dev.connect('tag-read', handler)
#    else:
#        print "Not connected"
#
#    mloop = gobject.MainLoop()
#    mloop.run()
