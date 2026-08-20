#!/usr/bin/env python3
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

from gi.repository import Gio
from gi.repository import GLib

MENUBAR = {}
ACTION_GROUP = None
ACTION_COUNTER = 0


def get_sub_menu_by_name(name):
    if name in MENUBAR:
        return MENUBAR[name]
    else:
        return None


def make_sub_menu(menu, name):
    """ add a new submenu to the menu """
    sub_menu = Gio.Menu()
    menu.append_submenu(name, sub_menu)
    MENUBAR[name] = [menu, sub_menu]
    return sub_menu


def make_menu_item(menu, tooltip, callback, arg=None):
    """ add a new item to the submenu """
    global ACTION_GROUP, ACTION_COUNTER
    if ACTION_GROUP is None:
        ACTION_GROUP = Gio.SimpleActionGroup()
        
    action_name = "action_" + str(ACTION_COUNTER)
    ACTION_COUNTER += 1
    
    if arg is None:
        action = Gio.SimpleAction.new(action_name, None)
        action.connect("activate", lambda a, v: callback(a))
    else:
        # Wrap the arg because we don't know its type easily for GLib.Variant
        action = Gio.SimpleAction.new(action_name, None)
        action.connect("activate", lambda a, v, arg=arg: callback(a, arg))
        
    ACTION_GROUP.add_action(action)
    menu.append(tooltip, "win." + action_name)


def make_checkmenu_item(menu, tooltip, callback, status=True, arg=None):
    global ACTION_GROUP, ACTION_COUNTER
    if ACTION_GROUP is None:
        ACTION_GROUP = Gio.SimpleActionGroup()
        
    action_name = "action_" + str(ACTION_COUNTER)
    ACTION_COUNTER += 1
    
    action = Gio.SimpleAction.new_stateful(action_name, None, GLib.Variant.new_boolean(status))
    
    def on_activate(action, param):
        current_state = action.get_state().get_boolean()
        new_state = not current_state
        action.set_state(GLib.Variant.new_boolean(new_state))
        if arg is None:
            callback(action)
        else:
            callback(action, arg)
            
    action.connect("activate", on_activate)
    ACTION_GROUP.add_action(action)
    
    menu.append(tooltip, "win." + action_name)
    return action
