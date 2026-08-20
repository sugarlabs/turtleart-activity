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

from gi.repository import Gtk

from .configfile import ConfigFile


class ConfigWizard:

    """Simple configuration wizard window."""

    def __init__(self, config_file_path, parent_window=None):
        self._config_items = []
        self._config_entries = {}
        self._config_file_path = config_file_path
        self._config_file_obj = None
        self._parent_window = parent_window

    def set_config_items(self, items):
        """
        items: [ {item_label, item_type, item_name, item_with_value} , ... ]
        """
        self._config_items = items
        keys = {}
        for i in self._config_items:
            keys[i["item_name"]] = {"type": i["item_type"]}
        self._valid_keys = keys

    def set_config_file_obj(self, obj):
        self._config_file_obj = obj

    def get_config_file_obj(self):
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
        if self._parent_window is not None:
            self._config_popup.set_transient_for(self._parent_window)
            self._config_popup.set_modal(True)
        self._config_popup.set_default_size(200, 200)
        self._config_popup.connect('close-request', self._close_config_cb)
        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        self._config_popup.set_child(grid)

        row = 1
        for i in self._config_items:
            hbox = self._create_param(i)
            hbox.set_margin_start(5)
            hbox.set_margin_end(5)
            hbox.set_margin_top(2)
            hbox.set_margin_bottom(2)
            grid.attach(hbox, 0, row, 1, 1)
            row = row + 1

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        save_button = Gtk.Button.new_with_label('Save')
        save_button.set_size_request(50, 15)
        save_button.connect('clicked', self._save_config_cb)
        hbox.append(save_button)
        cancel_button = Gtk.Button.new_with_label('Cancel')
        cancel_button.set_size_request(50, 15)
        cancel_button.connect('clicked', self._close_config_cb)
        hbox.append(cancel_button)
        hbox.set_margin_start(5)
        hbox.set_margin_end(5)
        hbox.set_margin_top(2)
        hbox.set_margin_bottom(2)
        grid.attach(hbox, 0, row, 1, 1)

        self._config_popup.present()

    def _save_config_cb(self, widget):
        try:
            self._do_save_config()
        except Exception as e:
            w = Gtk.Window()
            if self._parent_window is not None:
                w.set_transient_for(self._parent_window)
                w.set_modal(True)
            ls = Gtk.Label(label=str(e))
            w.set_child(ls)
            w.present()
        finally:
            self._config_popup.destroy()

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

    def _create_param(self, opts):
        """
        opts: {item_label, item_type, item_name, item_with_value}
        """
        param_name = opts["item_name"]
        with_value = opts["item_with_value"] if "item_with_value" in opts \
            else True
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
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
        label.set_xalign(1.0)
        label.set_yalign(0.5)
        label.set_size_request(100, 25)
        hbox.append(label)
        hbox.append(entry)
        return hbox

    def _close_config_cb(self, widget, event=None):
        self._config_popup.destroy()
        return True

