from .device import RFIDDevice
from .serial import Serial
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
from . import utils

HAL_SERVICE = 'org.freedesktop.Hal'
HAL_MGR_PATH = '/org/freedesktop/Hal/Manager'
HAL_MGR_IFACE = 'org.freedesktop.Hal.Manager'
HAL_DEV_IFACE = 'org.freedesktop.Hal.Device'
REGEXP_SERUSB = '/org/freedesktop/Hal/devices/usb_device['\
                'a-z,A-Z,0-9,_]*serial_usb_[0-9]'

VERSIONS = ['301']


class RFIDReader(RFIDDevice):
    """
    RFIDRW-E-W interface.
    """

    def __init__(self):

        RFIDDevice.__init__(self)
        self.last_tag = ""
        self.tags = []
        self.ser = Serial()
        self.device = ''
        self.device_path = ''
        self._connected = False

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
        Checks if RFID-RW-USB device is present.
        Returns True if so, False otherwise.
        """
        hmgr_if = dbus.Interface(
            self.bus.get_object(
                HAL_SERVICE,
                HAL_MGR_PATH),
            HAL_MGR_IFACE)
        serialusb_devices = set(
            hmgr_if.FindDeviceStringMatch(
                'serial.type', 'usb')) & set(
            hmgr_if.FindDeviceStringMatch(
                'info.subsystem', 'tty'))
        for i in serialusb_devices:
            serialusb_if = dbus.Interface(self.bus.get_object(HAL_SERVICE, i),
                                          HAL_DEV_IFACE)
            if serialusb_if.PropertyExists('info.parent'):
                parent_udi = str(serialusb_if.GetProperty('info.parent'))
                parent = dbus.Interface(
                    self.bus.get_object(
                        HAL_SERVICE,
                        parent_udi),
                    HAL_DEV_IFACE)
                if parent.PropertyExists('info.linux.driver') and str(
                        parent.GetProperty('info.linux.driver')) == 'ftdi_sio':
                    device = str(serialusb_if.GetProperty('linux.device_file'))
                    ser = Serial(device, 9600, timeout=0.1)
                    ser.read(100)
                    ser.write('v')
                    ser.write('e')
                    ser.write('r')
                    ser.write('\x0D')
                    resp = ser.read(4)
                    if resp[0:-1] in VERSIONS:
                        self.device = device
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
                if self._select_animal_tag:
                    # gobject.idle_add(self._loop)
                    gobject.timeout_add(1000, self._loop)
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

    def _select_animal_tag(self):
        """
        Sends the "Select Tag 2" (animal tag) command to the device.
        """
        self.ser.read(100)
        self.ser.write('s')
        self.ser.write('t')
        self.ser.write('2')
        self.ser.write('\x0d')
        resp = self.ser.read(3)[0:-1]
        if resp == 'OK':
            return True
        return False

    def get_version(self):
        """
        Sends the version command to the device and returns
        a string with the device version.
        """
        # self.ser.flushInput()
        ver = "???"
        self.ser.read(100)
        self.ser.write('v')
        self.ser.write('e')
        self.ser.write('r')
        self.ser.write('\x0d')
        resp = self.ser.read(4)[0:-1]
        if resp in VERSIONS:
            return "RFIDRW-E-USB " + resp
        return ver

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
            self.tags = []
            self.emit("disconnected", "RFID-RW-USB")

    def _loop(self):
        """
        Threaded loop for reading data from the device.
        """
        if not self._connected:
            return False

        self.ser.read(100)
        self.ser.write('r')
        self.ser.write('a')
        self.ser.write('t')
        self.ser.write('\x0d')
        resp = self.ser.read(33)[0:-1].split('_')
        if (resp.__len__() != 6) or resp in self.tags:
            return True

        self.tags.append(resp)
        anbit_bin = utils.dec2bin(int(resp[2]))
        reserved_bin = '00000000000000'
        databit_bin = utils.dec2bin(int(resp[3]))
        country_bin = utils.dec2bin(int(resp[0]))
        while country_bin.__len__() < 10:
            country_bin = '0' + country_bin
        id_bin = utils.dec2bin(int(resp[1]))
        while id_bin.__len__() < 10:
            id_bin = '0' + id_bin

        tag_bin = anbit_bin + reserved_bin + databit_bin + country_bin + id_bin
        data = utils.bin2hex(tag_bin)
        self.emit("tag-read", data)
        self.last_tag = data
        # sleep(1)
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
#        print "SIPI!"
#        dev.do_connect()
#        dev.connect('tag-read', handler)
#    else:
#        print "Not connected"
#
#    mloop = gobject.MainLoop()
#    mloop.run()
