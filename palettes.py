# -*- coding: utf-8 -*-
# Copyright (c) 2009, Raúl Gutiérrez Segalés
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
import tempfile
import urlparse
from gettext import gettext as _
import gobject

import gtk

from sugar.graphics.palette import Palette, Invoker
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar import profile
from sugar.activity import activity


class ContentInvoker(Invoker):

    def __init__(self, help_message):
        Invoker.__init__(self)
        self._position_hint = self.AT_CURSOR
        self.palette = BlockHelpPalette(help_message)

    def get_default_position(self):
        return self.AT_CURSOR

    def get_rect(self):
        return gtk.gdk.Rectangle()

    def get_toplevel(self):
        return None

    def showPopup(self, data = ""):
        if self.palette.is_up() == False:
            self.palette.popup()
            gobject.timeout_add(1500, self.close_palette, "")

    def close_palette(self, data = ""):
        self.palette.popdown()


class BlockHelpPalette(Palette):
    def __init__(self, help_message):
        Palette.__init__(self)

        self._help_message = help_message

        self.props.primary_text = help_message
