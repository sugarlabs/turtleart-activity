#!/usr/bin/python

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
