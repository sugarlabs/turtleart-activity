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


def strhex2bin(value):
    """Convert hexadecimal to binary, preserving leading zeroes."""
    return ''.join(format(int(digit, 16), '04b') for digit in value)


def strbin2dec(value):
    """Convert binary to a decimal string."""
    return str(int(value, 2)) if value else '0'


def dec2bin(value):
    """Convert an integer to binary (legacy nonpositive values map to zero)."""
    return format(value, 'b') if value > 0 else '0'


def bin2hex(value):
    """Convert binary to uppercase hexadecimal, preserving leading zeroes."""
    if not value:
        return ''
    width = (len(value) + 3) // 4
    return format(int(value, 2), '0%dX' % width)
