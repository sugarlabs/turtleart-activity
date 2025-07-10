#!/usr/bin/env python3
# Copyright (c) 2011 Walter Bender
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>
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

from gi.repository import GObject


class Plugin(GObject.GObject):

    def __init__(self):
        GObject.GObject.__init__(self)

    def setup(self):
        """ Setup is called once, when the Turtle Window is created. """
        pass

    def start(self):
        """ start is called when run button is pressed. """
        pass

    def stop(self):
        """ stop is called when stop button is pressed. """
        pass

    def clear(self):
        """ clear is called when erase button is pressed and from the
        clean block. """
        pass

    def goto_background(self):
        """ goto_background is called when the activity is sent to the
        background. """
        pass

    def return_to_foreground(self):
        """ return_to_foreground is called when the activity returns to
        the foreground. """
        pass

    def quit(self):
        """ cleanup is called when the activity is exiting. """
        pass
