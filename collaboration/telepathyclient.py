# Copyright (C) 2010 Collabora Ltd. <http://www.collabora.co.uk/>
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

import logging

import dbus
from dbus import PROPERTIES_IFACE
from gi.repository import TelepathyGLib
import dbus.service
from gi.repository import Gio

CLIENT = TelepathyGLib.IFACE_CLIENT
CLIENT_APPROVER = TelepathyGLib.IFACE_CLIENT_APPROVER
CLIENT_HANDLER = TelepathyGLib.IFACE_CLIENT_HANDLER
CLIENT_INTERFACE_REQUESTS = TelepathyGLib.IFACE_CLIENT_INTERFACE_REQUESTS

# FIXME Review the following code in replacement for
# telepathy.server.DBusProperties
DBusProperties = Gio.DBusPropertyInfo

from . import dispatch

SUGAR_CLIENT_SERVICE = 'org.freedesktop.Telepathy.Client.Sugar'
SUGAR_CLIENT_PATH = '/org/freedesktop/Telepathy/Client/Sugar'

_instance = None


class TelepathyClient(dbus.service.Object):

    def __init__(self):
        self._interfaces = set([CLIENT, CLIENT_HANDLER,
                                CLIENT_INTERFACE_REQUESTS, PROPERTIES_IFACE,
                                CLIENT_APPROVER])

        bus = dbus.Bus()
        bus_name = dbus.service.BusName(SUGAR_CLIENT_SERVICE, bus=bus)

        dbus.service.Object.__init__(self, bus_name, SUGAR_CLIENT_PATH)

        self._prop_getters = {}
        self._prop_setters = {}
        self._prop_getters.setdefault(CLIENT, {}).update({
            'Interfaces': lambda: list(self._interfaces),
        })
        self._prop_getters.setdefault(CLIENT_HANDLER, {}).update({
            'HandlerChannelFilter': self.__get_filters_cb,
        })

        self._prop_getters.setdefault(CLIENT_APPROVER, {}).update({
            'HandlerChannelFilter': self.__get_filters_cb,
        })
        self.got_channel = dispatch.Signal()
        self.got_dispatch_operation = dispatch.Signal()

    def __get_filters_cb(self):
        logging.debug('__get_filters_cb')
        filter_dict = dbus.Dictionary({}, signature='sv')
        return dbus.Array([filter_dict], signature='a{sv}')

    @dbus.service.method(dbus_interface=CLIENT_HANDLER,
                         in_signature='ooa(oa{sv})aota{sv}', out_signature='')
    def HandleChannels(self, account, connection, channels, requests_satisfied,
                       user_action_time, handler_info):
        logging.debug('HandleChannels\n%r\n%r\n%r\n%r\n%r\n%r\n', account,
                      connection, channels, requests_satisfied,
                      user_action_time, handler_info)
        for channel in channels:
            self.got_channel.send(self, account=account,
                                  connection=connection, channel=channel)

    @dbus.service.method(dbus_interface=CLIENT_INTERFACE_REQUESTS,
                         in_signature='oa{sv}', out_signature='')
    def AddRequest(self, request, properties):
        logging.debug('AddRequest\n%r\n%r', request, properties)

    @dbus.service.method(dbus_interface=CLIENT_APPROVER,
                         in_signature='a(oa{sv})oa{sv}', out_signature='',
                         async_callbacks=('success_cb', 'error_cb_'))
    def AddDispatchOperation(self, channels, dispatch_operation_path,
                             properties, success_cb, error_cb_):
        success_cb()
        try:
            logging.debug('AddDispatchOperation\n%r\n%r\n%r', channels,
                          dispatch_operation_path, properties)

            self.got_dispatch_operation.send(
                self,
                channels=channels,
                dispatch_operation_path=dispatch_operation_path,
                properties=properties)
        except Exception as e:
            logging.exception(e)

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        if interface_name in self._prop_getters \
                and property_name in self._prop_getters[interface_name]:
            return self._prop_getters[interface_name][property_name]()
        else:
            logging.debug('InvalidArgument')

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='ssv', out_signature='')
    def Set(self, interface_name, property_name, value):
        if interface_name in self._prop_setters \
                and property_name in self._prop_setters[interface_name]:
            self._prop_setters[interface_name][property_name](value)
        else:
            logging.debug('PermissionDenied')

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        if interface_name in self._prop_getters:
            r = {}
            for k, v in self._prop_getters[interface_name].items():
                r[k] = v()
            return r
        else:
            logging.debug('InvalidArgument')


def get_instance():
    global _instance
    if not _instance:
        _instance = TelepathyClient()
    return _instance
