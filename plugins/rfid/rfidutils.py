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

import os
import logging


def find_device():
    """
    Search for devices.
    Return a device instance or None.
    """
    device = None
    path = os.path.dirname(os.path.abspath(__file__))
    for i in os.listdir(path):
        if not os.path.isdir(os.path.join(path, i)):
            try:
                _tempmod = __import__('rfid.%s' % i.split('.')[0], globals(),
                                      locals(), ['RFIDReader'], -1)
                devtemp = _tempmod.RFIDReader()
                if devtemp.get_present():
                    device = devtemp
            except Exception:
                # logging.error("FIND_DEVICE: %s: %s"%(i, e))
                pass
    if device is None:
        logging.debug("No RFID device found")
    return device


def strhex2bin(strhex):
    """
    Convert a string representing an hex value into a
    string representing the same value in binary format.
    """
    dic = {'0': "0000",
           '1': "0001",
           '2': "0010",
           '3': "0011",
           '4': "0100",
           '5': "0101",
           '6': "0110",
           '7': "0111",
           '8': "1000",
           '9': "1001",
           'A': "1010",
           'B': "1011",
           'C': "1100",
           'D': "1101",
           'E': "1110",
           'F': "1111"
           }
    binstr = ""
    for i in strhex:
        binstr = binstr + dic[i.upper()]
    return binstr


def strbin2dec(strbin):
    """
    Convert a string representing a binary value into a
    string representing the same value in decimal format.
    """
    strdec = "0"
    for i in range(1, strbin.__len__() + 1):
        strdec = str(int(strdec) + int(strbin[-i]) * int(pow(2, i - 1)))
    return strdec


def dec2bin(ndec):
    """
    Convert a decimal number into a string representing
    the same value in binary format.
    """
    if ndec < 1:
        return "0"
    binary = []
    while ndec != 0:
        binary.append(ndec % 2)
        ndec = ndec / 2
    strbin = ""
    binary.reverse()
    for i in binary:
        strbin = strbin + str(i)
    return strbin


def bin2hex(strbin):
    """
    Convert a string representing a binary number into a string
    representing the same value in hexadecimal format.
    """
    dic = {"0000": "0",
           "0001": "1",
           "0010": "2",
           "0011": "3",
           "0100": "4",
           "0101": "5",
           "0110": "6",
           "0111": "7",
           "1000": "8",
           "1001": "9",
           "1010": "A",
           "1011": "B",
           "1100": "C",
           "1101": "D",
           "1110": "E",
           "1111": "F"
           }
    while strbin.__len__() % 4 != 0:
        strbin = '0' + strbin
    strh = ""
    for i in range(0, strbin.__len__() / 4):
        strh = strh + dic[str(strbin[i * 4:i * 4 + 4])]
    return strh
