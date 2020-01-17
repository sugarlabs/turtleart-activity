#!/usr/bin/env python3
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

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon

from TurtleArt.tapalette import help_windows

import logging
_logger = logging.getLogger('turtleart-activity')


class HelpButton(Gtk.ToolItem):

    def __init__(self, activity):
        self._activity = activity
        self._current_palette = 'turtle'

        Gtk.ToolItem.__init__(self)

        help_button = ToolButton('help-toolbar')
        help_button.set_tooltip(_('Help'))
        self.add(help_button)
        help_button.show()

        self._palette = help_button.get_palette()

        help_button.connect('clicked', self.__help_button_clicked_cb)

    def set_current_palette(self, name):
        self._current_palette = name

    def __help_button_clicked_cb(self, button):
        if self._activity.palette_toolbar_button.is_expanded():
            if not (self._current_palette in help_windows):
                _logger.debug('name %s not found' % (self._current_palette))
                return
            self._palette.set_content(help_windows[self._current_palette])
            help_windows[self._current_palette].show_all()
        elif self._activity.edit_toolbar_button.is_expanded():
            self._palette.set_content(help_windows['edit-toolbar'])
            help_windows['edit-toolbar'].show_all()
        elif self._activity.view_toolbar_button.is_expanded():
            self._palette.set_content(help_windows['view-toolbar'])
            help_windows['view-toolbar'].show_all()
        elif self._activity.activity_toolbar_button.is_expanded():
            self._palette.set_content(help_windows['activity-toolbar'])
            help_windows['activity-toolbar'].show_all()
        else:
            self._palette.set_content(help_windows['main-toolbar'])
            help_windows['main-toolbar'].show_all()

        self._palette.popup(immediate=True)


def add_section(help_box, section_text, icon=None):
    ''' Add a section to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    max_text_width = int(Gdk.Screen.width() / 3) - 20
    hbox = Gtk.HBox()
    label = Gtk.Label()
    label.set_use_markup(True)
    label.set_markup('<b>%s</b>' % section_text)
    label.set_line_wrap(True)
    label.set_size_request(max_text_width, -1)
    hbox.add(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.add(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show_all()
    help_box.pack_start(hbox, False, False, padding=5)


def add_paragraph(help_box, text, icon=None):
    ''' Add an entry to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    max_text_width = int(Gdk.Screen.width() / 3) - 20
    hbox = Gtk.HBox()
    label = Gtk.Label(label=text)
    label.set_justify(Gtk.Justification.LEFT)
    label.set_line_wrap(True)
    hbox.add(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.add(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show_all()
    help_box.pack_start(hbox, False, False, padding=5)

    return hbox
