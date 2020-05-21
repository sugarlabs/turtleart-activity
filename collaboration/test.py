#!/usr/bin/env python3


import dbus
import dbus.mainloop
import dbus.mainloop.glib
from .connectionmanager import get_connection_manager
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


conn_manager = get_connection_manager()
account_path, connection = conn_manager.get_preferred_connection()
print(account_path)
