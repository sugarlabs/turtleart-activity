#!/usr/bin/env python3
#
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

from gi.repository import GObject


class ConfigFile(GObject.GObject):
    """Load/save a simple (key = value) config file"""

    __gsignals__ = {
        'configuration-loaded': (GObject.SignalFlags.RUN_FIRST, None,
                                 ()),
        'configuration-saved': (GObject.SignalFlags.RUN_FIRST, None,
                                ()),
    }

    def __init__(self, config_file_path, valid_keys={}):
        GObject.GObject.__init__(self)

        self._config_file_path = config_file_path
        self._valid_keys = valid_keys
        self._config_hash = {}
        self._is_loaded = False

    def set_valid_keys(self, valid_keys):
        self._valid_keys = valid_keys

    def is_loaded(self):
        return self._is_loaded

    def get(self, key, empty_if_not_loaded=False):
        if key not in self._valid_keys:
            raise RuntimeError("Unknown config value %s" % key)

        if key in self._config_hash:
            value = self._config_hash[key]
        else:
            if self._valid_keys[key]["type"] == "text":
                value = ""
            elif self._valid_keys[key]["type"] == "boolean":
                value = False
            elif self._valid_keys[key]["type"] == "integer":
                value = 0

        return value

    def set(self, key, value):
        if key not in self._valid_keys:
            raise RuntimeError("Unknown config value %s" % key)

        self._config_hash[key] = value

    def load(self):
        try:
            config_file = open(self._config_file_path, 'r')
            lines = config_file.readlines()
            config_file.close()
            for line in lines:
                line = line.strip()
                k, v = line.split('=')
                k = k.strip(' ')
                v = v.strip(' ')
                if k not in self._valid_keys:
                    raise RuntimeError("Unknown config value %s" % k)
                value_type = self._valid_keys[k]["type"]
                if value_type == "text":
                    value = v
                elif value_type == "boolean":
                    value = eval(v)
                elif value_type == "integer":
                    value = int(v)
                self._config_hash[k] = value
            self._is_loaded = True
            self.emit('configuration-loaded')
        except Exception as e:
            print(e)

        return self._is_loaded

    def save(self):
        config_file = open(self._config_file_path, 'w')
        for k in list(self._config_hash.keys()):
            v = self._config_hash[k]
            ls = "%s = %s\n" % (k, v)
            config_file.write(ls)
        config_file.close()
        self.emit('configuration-saved')

    def dump_keys(self):
        print("\n\nDumping keys\n\n")
        for k in list(self._config_hash.keys()):
            v = self._config_hash[k]
            ls = "%s = %s\n" % (k, v)
            print(ls)


def test_save_load(test_config_file):
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
    c.dump_keys()


def _configuration_saved_cb(config_file_obj):
    print("_configuration_saved_cb called")
    config_file_obj.dump_keys()


def _configuration_loaded_cb(config_file_obj):
    print("_configuration_loaded_cb called")
    config_file_obj.dump_keys()


def test_signals(test_config_file):
    keys = {}
    keys["nick"] = {"type": "text"}
    keys["account_id"] = {"type": "text"}
    keys["server"] = {"type": "text"}
    keys["port"] = {"type": "text"}
    keys["password"] = {"type": "text"}
    keys["register"] = {"type": "text"}

    c = ConfigFile(test_config_file)
    c.connect('configuration-saved', _configuration_saved_cb)
    c.set_valid_keys(keys)
    c.set("nick", "rgs")
    c.set("account_id", "rgs@andromeda")
    c.set("server", "andromeda")
    c.set("port", 5223)
    c.set("password", "97c74fa0dc3b39b8c87f119fa53cced2b7040786")
    c.set("register", True)

    c.save()

    c = ConfigFile(test_config_file)
    c.connect('configuration-loaded', _configuration_loaded_cb)
    c.set_valid_keys(keys)
    c.load()


if __name__ == "__main__":
    test_save_load("/tmp/configfile.0001")
    test_signals("/tmp/configfile.0002")
