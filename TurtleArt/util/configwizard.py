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

from .configfile import ConfigFile
from gi.repository import Gtk


class ConfigWizard():

    """Simple configuration wizard window."""

    def __init__(self, config_file_path):
        self._config_items = []
        self._config_entries = {}
        self._config_file_path = config_file_path
        self._config_file_obj = None

    """
    [ {item_label, item_type, item_name, item_with_value} , ... ]
    """

    def set_config_items(self, items):
        self._config_items = items
        keys = {}
        for i in self._config_items:
            keys[i["item_name"]] = {"type": i["item_type"]}
        self._valid_keys = keys

    def set_config_file_obj(self, obj):
        self._config_file_obj = obj

    def get_config_file_obj(self, obj):
        return self._config_file_obj

    def show(self, read_from_disc=False):

        if read_from_disc:
            self._config_file_obj = ConfigFile(self._config_file_path)
            self._config_file_obj.set_valid_keys(self._valid_keys)
            self._config_file_obj.load()
        else:
            if self._config_file_obj is None:
                raise RuntimeError("I need the run time obj")

        self._config_popup = Gtk.Window()
        self._config_popup.set_default_size(200, 200)
        self._config_popup.connect('delete_event', self._close_config_cb)
        table = Gtk.Table(12, 1, True)
        self._config_popup.add(table)

        row = 1
        for i in self._config_items:
            hbox = self._create_param(i)
            table.attach(hbox, 0, 1, row, row + 1, xpadding=5, ypadding=2)
            row = row + 1

        hbox = Gtk.HBox()
        save_button = Gtk.Button.new_with_label('Save')
        save_button.set_size_request(50, 15)
        save_button.connect('pressed', self._save_config_cb)
        hbox.add(save_button)
        cancel_button = Gtk.Button.new_with_label('Cancel')
        cancel_button.set_size_request(50, 15)
        cancel_button.connect('pressed', self._close_config_cb)
        hbox.add(cancel_button)
        table.attach(hbox, 0, 1, row, row + 1, xpadding=5, ypadding=2)

        self._config_popup.show_all()

    def _save_config_cb(self, widget):
        try:
            self._do_save_config()
        except Exception as e:
            w = Gtk.Window()
            ls = Gtk.Label(label=e.message)
            w.add(ls)
            w.show_all()
        finally:
            self._config_popup.hide()

    def _do_save_config(self):
        for i in self._config_items:
            param_name = i["item_name"]
            v = self._config_entries[param_name]
            if v.__class__ is Gtk.Entry:
                value = v.get_text()
            elif v.__class__ is Gtk.CheckButton:
                value = v.get_active()
            else:
                raise RuntimeError("Don't recognize the class %s" % type(v))
            self._config_file_obj.set(param_name, value)

        self._config_file_obj.save()

    """
      {item_label, item_type, item_name, item_with_value}
    """

    def _create_param(self, opts):
        param_name = opts["item_name"]
        with_value = opts["item_with_value"] if "item_with_value" in opts \
            else True
        hbox = Gtk.HBox()
        if opts["item_type"] == "text":
            entry = Gtk.Entry()
            entry.set_size_request(150, 25)
            if with_value:
                value = self._config_file_obj.get(param_name, True)
                entry.set_text(str(value))
        elif opts["item_type"] == "boolean":
            entry = Gtk.CheckButton()
            if with_value:
                value = self._config_file_obj.get(param_name, True)
                entry.set_active(value)
        self._config_entries[param_name] = entry
        label = Gtk.Label(label=opts["item_label"] + ': ')
        label.set_alignment(1.0, 0.5)
        label.set_size_request(100, 25)
        hbox.add(label)
        hbox.add(entry)
        return hbox

    def _close_config_cb(self, widget, event=None):
        self._config_popup.hide()


def test_wizard_from_config_file_obj(test_config_file):
    keys = {}
    keys["nick"] = {"type": "text"}
    keys["account_id"] = {"type": "text"}
    keys["server"] = {"type": "text"}
    keys["port"] = {"type": "text"}
    keys["password"] = {"type": "text"}
    keys["register"] = {"type": "text"}

    c = ConfigFile(test_config_file)
    c.set_valid_keys(keys)
    c.set("nick", "rgs")
    c.set("account_id", "rgs@andromeda")
    c.set("server", "andromeda")
    c.set("port", 5223)
    c.set("password", "97c74fa0dc3b39b8c87f119fa53cced2b7040786")
    c.set("register", True)

    c.save()

    c = ConfigFile(test_config_file)
    c.set_valid_keys(keys)
    c.load()

    config_w = ConfigWizard(test_config_file)
    config_items = [
        {"item_label": "Nickname", "item_type": "text", "item_name": "nick"},
        {"item_label": "Account ID", "item_type": "text",
         "item_name": "account_id"},
        {"item_label": "Server", "item_type": "text", "item_name": "server"},
        {"item_label": "Port", "item_type": "text", "item_name": "port"},
        {"item_label": "Password", "item_type": "text",
         "item_name": "password"},
        {"item_label": "Register", "item_type": "text",
         "item_name": "register"}]
    config_w.set_config_items(config_items)
    config_w.set_config_file_obj(c)
    config_w.show()


def test_wizard_from_config_file_path(test_config_file):
    keys = {}
    keys["nick"] = {"type": "text"}
    keys["account_id"] = {"type": "text"}
    keys["server"] = {"type": "text"}
    keys["port"] = {"type": "text"}
    keys["password"] = {"type": "text"}
    keys["register"] = {"type": "text"}

    c = ConfigFile(test_config_file)
    c.set_valid_keys(keys)
    c.set("nick", "rgs")
    c.set("account_id", "rgs@andromeda")
    c.set("server", "andromeda")
    c.set("port", 5223)
    c.set("password", "97c74fa0dc3b39b8c87f119fa53cced2b7040786")
    c.set("register", True)

    c.save()

    config_w = ConfigWizard(test_config_file)
    config_items = [
        {"item_label": "Nickname", "item_type": "text", "item_name": "nick"},
        {"item_label": "Account ID", "item_type": "text",
         "item_name": "account_id"},
        {"item_label": "Server", "item_type": "text", "item_name": "server"},
        {"item_label": "Port", "item_type": "text", "item_name": "port"},
        {"item_label": "Password", "item_type": "text",
         "item_name": "password"},
        {"item_label": "Register", "item_type": "text",
         "item_name": "register"}]
    config_w.set_config_items(config_items)
    config_w.show(True)


if __name__ == "__main__":
    # test_wizard_from_config_file_obj("/tmp/configwizard.test.0001")
    test_wizard_from_config_file_path("/tmp/configwizard.test.0002")
    Gtk.main()
