#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012, Gonzalo Odiard <godiard@gmail.com>
# Copyright (C) 2012, Walter Bender <walter@sugarlabs.org>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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

# HelpButton widget

from gettext import gettext as _

import gtk

from sugar.graphics.toolbutton import ToolButton

from TurtleArt.tapalette import palette_names, help_windows

import logging
_logger = logging.getLogger('turtleart-activity')


class HelpButton(gtk.ToolItem):

    def __init__(self, **kwargs):
        self._current_palette = 'turtle'

        gtk.ToolItem.__init__(self)

        help_button = ToolButton('help-toolbar')
        help_button.set_tooltip(_('Help'))
        self.add(help_button)
        help_button.show()

        self._palette = help_button.get_palette()

        help_button.connect('clicked', self.__help_button_clicked_cb)

    def set_current_palette(self, name):
        _logger.debug(name)
        self._current_palette = name

    def __help_button_clicked_cb(self, button):
        if not (self._current_palette in help_windows):
            _logger.debug('name %s not found' % (self._current_palette))
            return
        self._palette.set_content(help_windows[self._current_palette])
        help_windows[self._current_palette].show_all()

        self._palette.popup(immediate=True, state=1)
