# utils.py - Helper functions for tis2000.py
# Copyright (C) 2010 Emiliano Pastorino <epastorino@plan.ceibal.edu.uy>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from importlib import import_module
import logging

# Keep the historic public imports; conversions have one implementation.
from .utils import strhex2bin, strbin2dec, dec2bin, bin2hex

__all__ = ['find_device', 'strhex2bin', 'strbin2dec', 'dec2bin', 'bin2hex']

_logger = logging.getLogger(__name__)
READERS = ('tis2000', 'rfidrweusb')


def _hal_available():
    """Check HAL backend before constructing any reader"""
    try:
        import dbus
    except ImportError:
        _logger.warning('RFID disabled: Python D-Bus bindings are unavailable.')
        return False
    try:
        # Allow D-Bus activation on older systems where HAL is installed.
        dbus.SystemBus().get_object('org.freedesktop.Hal',
                                    '/org/freedesktop/Hal/Manager')
    except dbus.DBusException as error:
        _logger.warning('RFID disabled: HAL is unavailable (%s).',
                        error.get_dbus_name())
        return False
    return True


def find_device():
    """Return the first supported reader found, or None"""
    if not _hal_available():
        return None
    for name in READERS:
        try:
            module = import_module('.' + name, __package__)
            device = module.RFIDReader()
            if device.get_present():
                return device
        except Exception:
            _logger.warning('Could not probe RFID reader %s', name,
                            exc_info=True)
    return None
