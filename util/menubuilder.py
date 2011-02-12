#!/usr/bin/python
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import gtk


class MenuBuilder():
    @classmethod
    def make_sub_menu(cls, menu, name):
        """ add a new submenu to the toolbar """
        sub_menu = gtk.MenuItem(name)
        sub_menu.show()
        sub_menu.set_submenu(menu)
        return sub_menu

    @classmethod
    def make_menu_item(cls, menu, tooltip, callback, arg=None):
        """ add a new item to the submenu """
        menu_items = gtk.MenuItem(tooltip)
        menu.append(menu_items)
        if arg is None:
            menu_items.connect('activate', callback)
        else:
            menu_items.connect('activate', callback, arg)
        menu_items.show()
