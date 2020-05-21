#!/usr/bin/env python3
# Copyright (C) 2007, Red Hat, Inc.
# Copyright (C) 2010-11 Collabora Ltd. <http://www.collabora.co.uk/>
#
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

from functools import partial

import dbus
from dbus import PROPERTIES_IFACE
import gi
gi.require_version('TelepathyGLib', '0.12')
from gi.repository import TelepathyGLib
ACCOUNT = TelepathyGLib.IFACE_ACCOUNT
ACCOUNT_MANAGER = TelepathyGLib.IFACE_ACCOUNT_MANAGER
CHANNEL = TelepathyGLib.IFACE_CHANNEL
CHANNEL_INTERFACE_GROUP = TelepathyGLib.IFACE_CHANNEL_INTERFACE_GROUP
CHANNEL_TYPE_CONTACT_LIST = TelepathyGLib.IFACE_CHANNEL_TYPE_CONTACT_LIST
CHANNEL_TYPE_FILE_TRANSFER = TelepathyGLib.IFACE_CHANNEL_TYPE_FILE_TRANSFER
CLIENT = TelepathyGLib.IFACE_CLIENT
CONNECTION = TelepathyGLib.IFACE_CONNECTION
CONNECTION_INTERFACE_ALIASING = \
    TelepathyGLib.IFACE_CONNECTION_INTERFACE_ALIASING
CONNECTION_INTERFACE_CONTACTS = \
    TelepathyGLib.IFACE_CONNECTION_INTERFACE_CONTACTS
CONNECTION_INTERFACE_CONTACT_CAPABILITIES = \
    TelepathyGLib.IFACE_CONNECTION_INTERFACE_CONTACT_CAPABILITIES
CONNECTION_INTERFACE_REQUESTS = \
    TelepathyGLib.IFACE_CONNECTION_INTERFACE_REQUESTS
CONNECTION_INTERFACE_SIMPLE_PRESENCE = \
    TelepathyGLib.IFACE_CONNECTION_INTERFACE_SIMPLE_PRESENCE

HANDLE_TYPE_CONTACT = TelepathyGLib.HandleType.CONTACT
HANDLE_TYPE_LIST = TelepathyGLib.HandleType.LIST
CONNECTION_PRESENCE_TYPE_OFFLINE = TelepathyGLib.ConnectionPresenceType.OFFLINE
CONNECTION_STATUS_CONNECTED = TelepathyGLib.ConnectionStatus.CONNECTED
CONNECTION_STATUS_DISCONNECTED = TelepathyGLib.ConnectionStatus.DISCONNECTED

from gi.repository.TelepathyGLib import Connection
from gi.repository.TelepathyGLib import Channel

from .buddy import get_owner_instance
from .buddy import BuddyModel

from .xocolor import XoColor
from gi.repository import GObject
from gi.repository import Gio

ACCOUNT_MANAGER_SERVICE = 'org.freedesktop.Telepathy.AccountManager'
ACCOUNT_MANAGER_PATH = '/org/freedesktop/Telepathy/AccountManager'
CHANNEL_DISPATCHER_SERVICE = 'org.freedesktop.Telepathy.ChannelDispatcher'
CHANNEL_DISPATCHER_PATH = '/org/freedesktop/Telepathy/ChannelDispatcher'
SUGAR_CLIENT_SERVICE = 'org.freedesktop.Telepathy.Client.Sugar'
SUGAR_CLIENT_PATH = '/org/freedesktop/Telepathy/Client/Sugar'

CONNECTION_INTERFACE_BUDDY_INFO = 'org.laptop.Telepathy.BuddyInfo'
CONNECTION_INTERFACE_ACTIVITY_PROPERTIES = \
    'org.laptop.Telepathy.ActivityProperties'

_QUERY_DBUS_TIMEOUT = 200
"""
Time in seconds to wait when querying contact properties. Some jabber servers
will be very slow in returning these queries, so just be patient.
"""


class ActivityModel(GObject.GObject):
    __gsignals__ = {
        'current-buddy-added': (GObject.SignalFlags.RUN_FIRST, None,
                                ([object])),
        'current-buddy-removed': (GObject.SignalFlags.RUN_FIRST, None,
                                  ([object])),
        'buddy-added': (GObject.SignalFlags.RUN_FIRST, None,
                        ([object])),
        'buddy-removed': (GObject.SignalFlags.RUN_FIRST, None,
                          ([object])),
    }

    def __init__(self, activity_id, room_handle):
        GObject.GObject.__init__(self)

        self.activity_id = activity_id
        self.room_handle = room_handle
        self._bundle = None
        self._color = None
        self._private = True
        self._name = None
        self._current_buddies = []
        self._buddies = []

        self._settings_collaboration = \
            Gio.Settings('org.sugarlabs.collaboration')
        self._settings_collaboration.connect(
            'changed::jabber-server', self.__jabber_server_changed_cb)
        self._settings_user = Gio.Settings('org.sugarlabs.user')
        self._settings_user.connect(
            'changed::nick', self.__nick_changed_cb)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    color = GObject.Property(type=object, getter=get_color, setter=set_color)

    def get_bundle(self):
        return self._bundle

    def set_bundle(self, bundle):
        self._bundle = bundle

    bundle = GObject.Property(type=object, getter=get_bundle,
                              setter=set_bundle)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = GObject.Property(type=object, getter=get_name, setter=set_name)

    def is_private(self):
        return self._private

    def set_private(self, private):
        self._private = private

    private = GObject.Property(type=object, getter=is_private,
                               setter=set_private)

    def get_buddies(self):
        return self._buddies

    def add_buddy(self, buddy):
        self._buddies.append(buddy)
        self.notify('buddies')
        self.emit('buddy-added', buddy)

    def remove_buddy(self, buddy):
        self._buddies.remove(buddy)
        self.notify('buddies')
        self.emit('buddy-removed', buddy)

    buddies = GObject.Property(type=object, getter=get_buddies)

    def get_current_buddies(self):
        return self._current_buddies

    def add_current_buddy(self, buddy):
        self._current_buddies.append(buddy)
        self.notify('current-buddies')
        self.emit('current-buddy-added', buddy)

    def remove_current_buddy(self, buddy):
        self._current_buddies.remove(buddy)
        self.notify('current-buddies')
        self.emit('current-buddy-removed', buddy)

    current_buddies = GObject.Property(type=object, getter=get_current_buddies)


class _Account(GObject.GObject):
    __gsignals__ = {
        'activity-added': (GObject.SignalFlags.RUN_FIRST, None,
                           ([object, object])),
        'activity-updated': (GObject.SignalFlags.RUN_FIRST, None,
                             ([object, object])),
        'activity-removed': (GObject.SignalFlags.RUN_FIRST, None,
                             ([object])),
        'buddy-added': (GObject.SignalFlags.RUN_FIRST, None,
                        ([object, object, object])),
        'buddy-updated': (GObject.SignalFlags.RUN_FIRST, None,
                          ([object, object])),
        'buddy-removed': (GObject.SignalFlags.RUN_FIRST, None,
                          ([object])),
        'buddy-joined-activity': (GObject.SignalFlags.RUN_FIRST, None,
                                  ([object, object])),
        'buddy-left-activity': (GObject.SignalFlags.RUN_FIRST, None,
                                ([object, object])),
        'current-activity-updated': (GObject.SignalFlags.RUN_FIRST,
                                     None, ([object, object])),
        'connected': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'disconnected': (GObject.SignalFlags.RUN_FIRST, None, ([])),
    }

    def __init__(self, account_path):
        GObject.GObject.__init__(self)

        self.object_path = account_path

        self._connection = None
        self._buddy_handles = {}
        self._activity_handles = {}
        self._self_handle = None

        self._buddies_per_activity = {}
        self._activities_per_buddy = {}

        self._start_listening()

    def _start_listening(self):
        bus = dbus.Bus()
        obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, self.object_path)
        obj.Get(ACCOUNT, 'Connection',
                reply_handler=self.__got_connection_cb,
                error_handler=partial(self.__error_handler_cb,
                                      'Account.GetConnection'))
        obj.connect_to_signal(
            'AccountPropertyChanged', self.__account_property_changed_cb)

    def __error_handler_cb(self, function_name, error):
        raise RuntimeError('Error when calling %s: %s' % (function_name,
                                                          error))

    def __got_connection_cb(self, connection_path):
        # print('_Account.__got_connection_cb %r', connection_path)

        if connection_path == '/':
            self._check_registration_error()
            return

        self._prepare_connection(connection_path)

    def _check_registration_error(self):
        """
        See if a previous connection attempt failed and we need to unset
        the register flag.
        """
        bus = dbus.Bus()
        obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, self.object_path)
        obj.Get(ACCOUNT, 'ConnectionError',
                reply_handler=self.__got_connection_error_cb,
                error_handler=partial(self.__error_handler_cb,
                                      'Account.GetConnectionError'))

    def __got_connection_error_cb(self, error):
        # print('_Account.__got_connection_error_cb %r', error)
        if error == 'org.freedesktop.Telepathy.Error.RegistrationExists':
            bus = dbus.Bus()
            obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, self.object_path)
            obj.UpdateParameters({'register': False}, [],
                                 dbus_interface=ACCOUNT)

    def __account_property_changed_cb(self, properties):
        # print('_Account.__account_property_changed_cb %r %r %r',
        # self.object_path, properties.get('Connection', None),
        #          self._connection)
        if 'Connection' not in properties:
            return
        if properties['Connection'] == '/':
            self._check_registration_error()
            self._connection = None
        elif self._connection is None:
            self._prepare_connection(properties['Connection'])

    def _prepare_connection(self, connection_path):
        connection_name = connection_path.replace('/', '.')[1:]
        print(("Preparing %s" % connection_name))
        self._connection = Connection(connection_name, connection_path,
                                      ready_handler=self.__connection_ready_cb)

    def __connection_ready_cb(self, connection):
        print(('_Account.__connection_ready_cb %r', connection.object_path))
        connection.connect_to_signal('StatusChanged',
                                     self.__status_changed_cb)

        connection[PROPERTIES_IFACE].Get(
            CONNECTION,
            'Status',
            reply_handler=self.__get_status_cb,
            error_handler=partial(self.__error_handler_cb,
                                  'Connection.GetStatus'))

    def __get_status_cb(self, status):
        # print('_Account.__get_status_cb %r %r',
        # self._connection.object_path, status)
        self._update_status(status)

    def __status_changed_cb(self, status, reason):
        # print('_Account.__status_changed_cb %r %r', status, reason)
        self._update_status(status)

    def _update_status(self, status):
        if status == CONNECTION_STATUS_CONNECTED:
            self._connection[PROPERTIES_IFACE].Get(
                CONNECTION,
                'SelfHandle',
                reply_handler=self.__get_self_handle_cb,
                error_handler=partial(self.__error_handler_cb,
                                      'Connection.GetSelfHandle'))
            self.emit('connected')
        else:
            for contact_handle, contact_id in list(
                    self._buddy_handles.items()):
                if contact_id is not None:
                    self.emit('buddy-removed', contact_id)

            for room_handle, activity_id in list(
                    self._activity_handles.items()):
                self.emit('activity-removed', activity_id)

            self._buddy_handles = {}
            self._activity_handles = {}
            self._buddies_per_activity = {}
            self._activities_per_buddy = {}

            self.emit('disconnected')

        if status == CONNECTION_STATUS_DISCONNECTED:
            self._connection = None

    def __get_self_handle_cb(self, self_handle):
        self._self_handle = self_handle

        if CONNECTION_INTERFACE_CONTACT_CAPABILITIES in self._connection:
            interface = CONNECTION_INTERFACE_CONTACT_CAPABILITIES
            connection = self._connection[interface]
            client_name = CLIENT + '.Sugar.FileTransfer'
            file_transfer_channel_class = {
                CHANNEL + '.ChannelType': CHANNEL_TYPE_FILE_TRANSFER,
                CHANNEL + '.TargetHandleType': HANDLE_TYPE_CONTACT}
            capabilities = []
            connection.UpdateCapabilities(
                [(client_name, [file_transfer_channel_class], capabilities)],
                reply_handler=self.__update_capabilities_cb,
                error_handler=partial(self.__error_handler_cb,
                                      'Connection.UpdateCapabilities'))

        connection = self._connection[CONNECTION_INTERFACE_ALIASING]
        connection.connect_to_signal('AliasesChanged',
                                     self.__aliases_changed_cb)

        connection = self._connection[CONNECTION_INTERFACE_SIMPLE_PRESENCE]
        connection.connect_to_signal('PresencesChanged',
                                     self.__presences_changed_cb)

        if CONNECTION_INTERFACE_BUDDY_INFO in self._connection:
            connection = self._connection[CONNECTION_INTERFACE_BUDDY_INFO]
            connection.connect_to_signal('PropertiesChanged',
                                         self.__buddy_info_updated_cb,
                                         byte_arrays=True)

            connection.connect_to_signal('ActivitiesChanged',
                                         self.__buddy_activities_changed_cb)

            connection.connect_to_signal('CurrentActivityChanged',
                                         self.__current_activity_changed_cb)
        else:
            print(('Connection %s does not support OLPC buddy '
                   'properties', self._connection.object_path))
            pass

        if CONNECTION_INTERFACE_ACTIVITY_PROPERTIES in self._connection:
            connection = self._connection[
                CONNECTION_INTERFACE_ACTIVITY_PROPERTIES]
            connection.connect_to_signal(
                'ActivityPropertiesChanged',
                self.__activity_properties_changed_cb)
        else:
            print(('Connection %s does not support OLPC activity '
                   'properties', self._connection.object_path))
            pass

        properties = {
            CHANNEL + '.ChannelType': CHANNEL_TYPE_CONTACT_LIST,
            CHANNEL + '.TargetHandleType': HANDLE_TYPE_LIST,
            CHANNEL + '.TargetID': 'subscribe', }
        properties = dbus.Dictionary(properties, signature='sv')
        connection = self._connection[CONNECTION_INTERFACE_REQUESTS]
        is_ours, channel_path, properties = \
            connection.EnsureChannel(properties)

        channel = Channel(self._connection.service_name, channel_path)
        channel[CHANNEL_INTERFACE_GROUP].connect_to_signal(
            'MembersChanged',
            self.__members_changed_cb)

        channel[PROPERTIES_IFACE].Get(
            CHANNEL_INTERFACE_GROUP,
            'Members',
            reply_handler=self.__get_members_ready_cb,
            error_handler=partial(self.__error_handler_cb,
                                  'Connection.GetMembers'))

    def __update_capabilities_cb(self):
        pass

    def __aliases_changed_cb(self, aliases):
        # print('_Account.__aliases_changed_cb')
        for handle, alias in aliases:
            if handle in self._buddy_handles:
                # print('Got handle %r with nick %r, going to update',
                #              handle, alias)
                properties = {CONNECTION_INTERFACE_ALIASING + '/alias': alias}
                self.emit('buddy-updated', self._buddy_handles[handle],
                          properties)

    def __presences_changed_cb(self, presences):
        # print('_Account.__presences_changed_cb %r', presences)
        for handle, presence in presences.items():
            if handle in self._buddy_handles:
                presence_type, status_, message_ = presence
                if presence_type == CONNECTION_PRESENCE_TYPE_OFFLINE:
                    contact_id = self._buddy_handles[handle]
                    del self._buddy_handles[handle]
                    self.emit('buddy-removed', contact_id)

    def __buddy_info_updated_cb(self, handle, properties):
        # print('_Account.__buddy_info_updated_cb %r', handle)
        self.emit('buddy-updated', self._buddy_handles[handle], properties)

    def __current_activity_changed_cb(self, contact_handle, activity_id,
                                      room_handle):
        # print('_Account.__current_activity_changed_cb %r %r %r',
        #              contact_handle, activity_id, room_handle)
        if contact_handle in self._buddy_handles:
            contact_id = self._buddy_handles[contact_handle]
            if not activity_id and room_handle:
                activity_id = self._activity_handles.get(room_handle, '')
            self.emit('current-activity-updated', contact_id, activity_id)

    def __get_current_activity_cb(self, contact_handle, activity_id,
                                  room_handle):
        # print('_Account.__get_current_activity_cb %r %r %r',
        #              contact_handle, activity_id, room_handle)
        contact_id = self._buddy_handles[contact_handle]
        self.emit('current-activity-updated', contact_id, activity_id)

    def __buddy_activities_changed_cb(self, buddy_handle, activities):
        self._update_buddy_activities(buddy_handle, activities)

    def _update_buddy_activities(self, buddy_handle, activities):
        # print('_Account._update_buddy_activities')
        if buddy_handle not in self._buddy_handles:
            self._buddy_handles[buddy_handle] = None

        if buddy_handle not in self._activities_per_buddy:
            self._activities_per_buddy[buddy_handle] = set()

        for activity_id, room_handle in activities:
            if room_handle not in self._activity_handles:
                self._activity_handles[room_handle] = activity_id
                self.emit('activity-added', room_handle, activity_id)

                connection = self._connection[
                    CONNECTION_INTERFACE_ACTIVITY_PROPERTIES]
                connection.GetProperties(
                    room_handle,
                    reply_handler=partial(self.__get_properties_cb,
                                          room_handle),
                    error_handler=partial(self.__error_handler_cb,
                                          'ActivityProperties.GetProperties'))

                # Sometimes we'll get CurrentActivityChanged before we get to
                # know about the activity so we miss the event. In that case,
                # request again the current activity for this buddy.
                connection = self._connection[CONNECTION_INTERFACE_BUDDY_INFO]
                connection.GetCurrentActivity(
                    buddy_handle,
                    reply_handler=partial(self.__get_current_activity_cb,
                                          buddy_handle),
                    error_handler=partial(self.__error_handler_cb,
                                          'BuddyInfo.GetCurrentActivity'))

            if activity_id not in self._buddies_per_activity:
                self._buddies_per_activity[activity_id] = set()
            self._buddies_per_activity[activity_id].add(buddy_handle)
            if activity_id not in self._activities_per_buddy[buddy_handle]:
                self._activities_per_buddy[buddy_handle].add(activity_id)
                if self._buddy_handles[buddy_handle] is not None:
                    self.emit('buddy-joined-activity',
                              self._buddy_handles[buddy_handle],
                              activity_id)

        current_activity_ids = \
            [activity_id for activity_id, room_handle in activities]
        for activity_id in self._activities_per_buddy[buddy_handle].copy():
            if activity_id not in current_activity_ids:
                self._remove_buddy_from_activity(buddy_handle, activity_id)

    def __get_properties_cb(self, room_handle, properties):
        # print('_Account.__get_properties_cb %r %r', room_handle,
        #              properties)
        if properties:
            self._update_activity(room_handle, properties)

    def _remove_buddy_from_activity(self, buddy_handle, activity_id):
        if buddy_handle in self._buddies_per_activity[activity_id]:
            self._buddies_per_activity[activity_id].remove(buddy_handle)

        if activity_id in self._activities_per_buddy[buddy_handle]:
            self._activities_per_buddy[buddy_handle].remove(activity_id)

        if self._buddy_handles[buddy_handle] is not None:
            self.emit('buddy-left-activity',
                      self._buddy_handles[buddy_handle],
                      activity_id)

        if not self._buddies_per_activity[activity_id]:
            del self._buddies_per_activity[activity_id]

            for room_handle in self._activity_handles.copy():
                if self._activity_handles[room_handle] == activity_id:
                    del self._activity_handles[room_handle]
                    break

            self.emit('activity-removed', activity_id)

    def __activity_properties_changed_cb(self, room_handle, properties):
        # print('_Account.__activity_properties_changed_cb %r %r',
        #              room_handle, properties)
        self._update_activity(room_handle, properties)

    def _update_activity(self, room_handle, properties):
        if room_handle in self._activity_handles:
            self.emit('activity-updated', self._activity_handles[room_handle],
                      properties)
        else:
            # print('_Account.__activity_properties_changed_cb unknown '
            #              'activity')
            # We don't get ActivitiesChanged for the owner of the connection,
            # so we query for its activities in order to find out.
            if CONNECTION_INTERFACE_BUDDY_INFO in self._connection:
                handle = self._self_handle
                connection = self._connection[CONNECTION_INTERFACE_BUDDY_INFO]
                connection.GetActivities(
                    handle,
                    reply_handler=partial(self.__got_activities_cb, handle),
                    error_handler=partial(self.__error_handler_cb,
                                          'BuddyInfo.Getactivities'))

    def __members_changed_cb(self, message, added, removed, local_pending,
                             remote_pending, actor, reason):
        self._add_buddy_handles(added)

    def __get_members_ready_cb(self, handles):
        # print('_Account.__get_members_ready_cb %r', handles)
        if not handles:
            return

        self._add_buddy_handles(handles)

    def _add_buddy_handles(self, handles):
        # print('_Account._add_buddy_handles %r', handles)
        interfaces = [CONNECTION, CONNECTION_INTERFACE_ALIASING]
        self._connection[CONNECTION_INTERFACE_CONTACTS].GetContactAttributes(
            handles, interfaces, False,
            reply_handler=self.__get_contact_attributes_cb,
            error_handler=partial(self.__error_handler_cb,
                                  'Contacts.GetContactAttributes'))

    def __got_buddy_info_cb(self, handle, nick, properties):
        # print('_Account.__got_buddy_info_cb %r', handle)
        self.emit('buddy-updated', self._buddy_handles[handle], properties)

    def __get_contact_attributes_cb(self, attributes):
        # print('_Account.__get_contact_attributes_cb %r',
        #              attributes.keys())

        for handle in list(attributes.keys()):
            nick = attributes[handle][CONNECTION_INTERFACE_ALIASING + '/alias']

            if handle in self._buddy_handles and \
                    not self._buddy_handles[handle] is None:
                # print('Got handle %r with nick %r, going to update',
                #              handle, nick)
                self.emit('buddy-updated', self._buddy_handles[handle],
                          attributes[handle])
            else:
                # print('Got handle %r with nick %r, going to add',
                #              handle, nick)

                contact_id = attributes[handle][CONNECTION + '/contact-id']
                self._buddy_handles[handle] = contact_id

                if CONNECTION_INTERFACE_BUDDY_INFO in self._connection:
                    connection = \
                        self._connection[CONNECTION_INTERFACE_BUDDY_INFO]

                    connection.GetProperties(
                        handle,
                        reply_handler=partial(self.__got_buddy_info_cb, handle,
                                              nick),
                        error_handler=partial(self.__error_handler_cb,
                                              'BuddyInfo.GetProperties'),
                        byte_arrays=True,
                        timeout=_QUERY_DBUS_TIMEOUT)

                    connection.GetActivities(
                        handle,
                        reply_handler=partial(self.__got_activities_cb,
                                              handle),
                        error_handler=partial(self.__error_handler_cb,
                                              'BuddyInfo.GetActivities'),
                        timeout=_QUERY_DBUS_TIMEOUT)

                    connection.GetCurrentActivity(
                        handle,
                        reply_handler=partial(self.__get_current_activity_cb,
                                              handle),
                        error_handler=partial(self.__error_handler_cb,
                                              'BuddyInfo.GetCurrentActivity'),
                        timeout=_QUERY_DBUS_TIMEOUT)

                self.emit('buddy-added', contact_id, nick, handle)

    def __got_activities_cb(self, buddy_handle, activities):
        # print('_Account.__got_activities_cb %r %r', buddy_handle,
        #              activities)
        self._update_buddy_activities(buddy_handle, activities)

    def enable(self):
        # print('_Account.enable %s', self.object_path)
        self._set_enabled(True)

    def disable(self):
        # print('_Account.disable %s', self.object_path)
        self._set_enabled(False)
        self._connection = None

    def _set_enabled(self, value):
        bus = dbus.Bus()
        obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, self.object_path)
        obj.Set(ACCOUNT, 'Enabled', value,
                reply_handler=self.__set_enabled_cb,
                error_handler=partial(self.__error_handler_cb,
                                      'Account.SetEnabled'),
                dbus_interface='org.freedesktop.DBus.Properties')

    def __set_enabled_cb(self):
        # print('_Account.__set_enabled_cb success')
        pass


class Neighborhood(GObject.GObject):
    __gsignals__ = {
        'activity-added': (GObject.SignalFlags.RUN_FIRST, None,
                           ([object])),
        'activity-removed': (GObject.SignalFlags.RUN_FIRST, None,
                             ([object])),
        'buddy-added': (GObject.SignalFlags.RUN_FIRST, None,
                        ([object])),
        'buddy-removed': (GObject.SignalFlags.RUN_FIRST, None,
                          ([object])), }

    def __init__(self, params={}):
        GObject.GObject.__init__(self)

        self._buddies = {None: get_owner_instance()}
        self._activities = {}
        self._server_account = None
        self._nicks = {}

        #
        # Jabber params
        #
        self._nickname = params["nickname"]
        self._account_id = params["account_id"]
        self._server = params["server"]
        self._port = params["port"]
        self._password = params["password"]
        self._register = params["register"]

        bus = dbus.Bus()
        obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, ACCOUNT_MANAGER_PATH)
        account_manager = dbus.Interface(obj, ACCOUNT_MANAGER)
        account_manager.Get(ACCOUNT_MANAGER, 'ValidAccounts',
                            dbus_interface=PROPERTIES_IFACE,
                            reply_handler=self.__got_accounts_cb,
                            error_handler=self.__error_handler_cb)

    def show_buddies(self):
        print("\n\nBuddy list\n\n")
        for k in list(self._nicks.keys()):
            try:
                print("%s = %s" % (k, self._nicks[k]))
            except BaseException:
                pass

        print("\n\nActivities list\n\n")
        for k in list(self._activities.keys()):
            try:
                print("%s" % k)
            except BaseException:
                pass

    def __got_accounts_cb(self, account_paths):
        self._server_account = self._ensure_server_account(account_paths)
        self._connect_to_account(self._server_account)

    def __error_handler_cb(self, error):
        raise RuntimeError(error)

    def _connect_to_account(self, account):
        account.connect('buddy-added', self.__buddy_added_cb)
        account.connect('buddy-updated', self.__buddy_updated_cb)
        account.connect('buddy-removed', self.__buddy_removed_cb)
        account.connect('buddy-joined-activity',
                        self.__buddy_joined_activity_cb)
        account.connect('buddy-left-activity', self.__buddy_left_activity_cb)
        account.connect('activity-added', self.__activity_added_cb)
        account.connect('activity-updated', self.__activity_updated_cb)
        account.connect('activity-removed', self.__activity_removed_cb)
        account.connect('current-activity-updated',
                        self.__current_activity_updated_cb)
        account.connect('connected', self.__account_connected_cb)
        account.connect('disconnected', self.__account_disconnected_cb)

    def __account_connected_cb(self, account):
        # print('__account_connected_cb %s', account.object_path)
        if account == self._server_account:
            # self._link_local_account.disable()
            pass

    def __account_disconnected_cb(self, account):
        # print('__account_disconnected_cb %s', account.object_path)
        if account == self._server_account:
            self._link_local_account.enable()

    def _ensure_link_local_account(self, account_paths):
        for account_path in account_paths:
            if 'salut' in account_path:
                # print('Already have a Salut account')
                account = _Account(account_path)
                account.enable()
                return account

        # print('Still dont have a Salut account, creating one')

        nick = self._settings_user.get_string('nick')

        params = {
            'nickname': nick,
            'first-name': '',
            'last-name': '',
            'jid': self._get_jabber_account_id(),
            'published-name': nick, }

        properties = {
            ACCOUNT + '.Enabled': True,
            ACCOUNT + '.Nickname': nick,
            ACCOUNT + '.ConnectAutomatically': True, }

        bus = dbus.Bus()
        obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, ACCOUNT_MANAGER_PATH)
        account_manager = dbus.Interface(obj, ACCOUNT_MANAGER)
        account_path = account_manager.CreateAccount('salut', 'local-xmpp',
                                                     'salut', params,
                                                     properties)
        return _Account(account_path)

    def _ensure_server_account(self, account_paths):
        bus = dbus.Bus()

        for account_path in account_paths:
            if 'gabble' in account_path:
                obj_acct_mgr = bus.get_object(
                    ACCOUNT_MANAGER_SERVICE,
                    account_path)
                properties = obj_acct_mgr.Get(ACCOUNT, 'Parameters')
                if "server" in properties and \
                        properties["server"] == self._server:
                    print(("Enabiling account_path = %s, server = %s",
                           account_path, self._server))
                    account = _Account(account_path)
                    account.enable()
                    return account

        params = {
            'account': self._get_jabber_account_id(),
            'password': self._password,
            'server': self._server,
            'resource': 'sugar',
            'require-encryption': True,
            'ignore-ssl-errors': True,
            'register': self._register,
            'old-ssl': True,
            'port': dbus.UInt32(self._port), }

        properties = {
            ACCOUNT + '.Enabled': True,
            ACCOUNT + '.Nickname': self._nickname,
            ACCOUNT + '.ConnectAutomatically': True, }

        obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, ACCOUNT_MANAGER_PATH)
        account_manager = dbus.Interface(obj, ACCOUNT_MANAGER)
        account_path = account_manager.CreateAccount('gabble', 'jabber',
                                                     'jabber', params,
                                                     properties)
        return _Account(account_path)

    def _get_jabber_account_id(self):
        return self._account_id

    def __jabber_server_changed_cb(self, settings, key):
        # print('__jabber_server_changed_cb')

        bus = dbus.Bus()
        account = bus.get_object(ACCOUNT_MANAGER_SERVICE,
                                 self._server_account.object_path)

        server = settings.get_string('jabber_server')
        account_id = self._get_jabber_account_id()
        needs_reconnect = account.UpdateParameters(
            {'server': server,
             'account': account_id,
             'register': True},
            dbus.Array([], 's'),
            dbus_interface=ACCOUNT)
        if needs_reconnect:
            account.Reconnect()

        self._update_jid()

    def __nick_changed_cb(self, settings, key):
        nick = settings.get_string('nick')
        for account in self._server_account, self._link_local_account:
            bus = dbus.Bus()
            obj = bus.get_object(ACCOUNT_MANAGER_SERVICE, account.object_path)
            obj.Set(ACCOUNT, 'Nickname', nick, dbus_interface=PROPERTIES_IFACE)

        self._update_jid()

    def _update_jid(self):
        bus = dbus.Bus()
        account = bus.get_object(ACCOUNT_MANAGER_SERVICE,
                                 self._link_local_account.object_path)

        account_id = self._get_jabber_account_id()
        needs_reconnect = account.UpdateParameters({'jid': account_id},
                                                   dbus.Array([], 's'),
                                                   dbus_interface=ACCOUNT)
        if needs_reconnect:
            account.Reconnect()

    def __buddy_added_cb(self, account, contact_id, nick, handle):
        self._nicks[contact_id] = nick
        if contact_id in self._buddies:
            # print('__buddy_added_cb buddy already tracked')
            return

        buddy = BuddyModel(
            nick=nick,
            account=account.object_path,
            contact_id=contact_id,
            handle=handle)
        self._buddies[contact_id] = buddy

    def __buddy_updated_cb(self, account, contact_id, properties):
        # print('__buddy_updated_cb %r', contact_id)
        if contact_id is None:
            # Don't know the contact-id yet, will get the full state later
            return

        if contact_id not in self._buddies:
            # print('__buddy_updated_cb Unknown buddy with contact_id'
            #              ' %r', contact_id)
            return

        buddy = self._buddies[contact_id]

        is_new = buddy.props.key is None and 'key' in properties

        if 'color' in properties:
            buddy.props.color = XoColor(properties['color'])

        if 'key' in properties:
            buddy.props.key = properties['key']

        if 'nick' in properties:
            buddy.props.nick = properties['nick']

        if is_new:
            self.emit('buddy-added', buddy)

    def __buddy_removed_cb(self, account, contact_id):
        # print('Neighborhood.__buddy_removed_cb %r', contact_id)
        try:
            self._nicks.pop(contact_id)
        except BaseException:
            pass
        if contact_id not in self._buddies:
            # print('Neighborhood.__buddy_removed_cb Unknown buddy with '
            #              'contact_id %r', contact_id)
            return

        buddy = self._buddies[contact_id]
        del self._buddies[contact_id]

        if buddy.props.key is not None:
            self.emit('buddy-removed', buddy)

    def __activity_added_cb(self, account, room_handle, activity_id):
        # print('__activity_added_cb %r %r', room_handle, activity_id)
        if activity_id in self._activities:
            # print('__activity_added_cb activity already tracked')
            return

        activity = ActivityModel(activity_id, room_handle)
        self._activities[activity_id] = activity

    def __activity_updated_cb(self, account, activity_id, properties):
        print(('__activity_updated_cb %r %r', activity_id, properties))
        if activity_id not in self._activities:
            print((
                '__activity_updated_cb: Unknown activity with activity_id %r',
                activity_id))
            return

        # we should somehow emulate this and say we only have TurtleArtActivity
        # registry = bundleregistry.get_registry()
        # bundle = registry.get_bundle(properties['type'])
        # bundle = None
        # if not bundle:
        # print('Ignoring shared activity we don''t have')
        #   return

        activity = self._activities[activity_id]

        is_new = activity.props.bundle is None

        if 'color' in properties:
            activity.props.color = XoColor(properties['color'])
        # FIXME: we have no access to the bundleregistry
        activity.props.bundle = None
        if 'name' in properties:
            activity.props.name = properties['name']
        if 'private' in properties:
            activity.props.private = properties['private']
        # FIXME: this should be configurable, we only care about the
        #        activity thats using this lib i.e.: Turtle Art
        if properties['type']:
            activity.props.bundle = properties['type']

        if is_new:
            print("The activity is new")
            self.emit('activity-added', activity)
        else:
            print("The activity is *NOT* new")

    def __activity_removed_cb(self, account, activity_id):
        if activity_id not in self._activities:
            print(('Unknown activity with id %s. Already removed?',
                   activity_id))
            return
        activity = self._activities[activity_id]
        del self._activities[activity_id]

        self.emit('activity-removed', activity)

    def __current_activity_updated_cb(self, account, contact_id, activity_id):
        # print('__current_activity_updated_cb %r %r', contact_id,
        #              activity_id)
        if contact_id not in self._buddies:
            # print('__current_activity_updated_cb Unknown buddy with '
            #              'contact_id %r', contact_id)
            return
        if activity_id and activity_id not in self._activities:
            # print('__current_activity_updated_cb Unknown activity with'
            #              ' id %s', activity_id)
            activity_id = ''

        buddy = self._buddies[contact_id]
        if buddy.props.current_activity is not None:
            if buddy.props.current_activity.activity_id == activity_id:
                return
            buddy.props.current_activity.remove_current_buddy(buddy)

        if activity_id:
            activity = self._activities[activity_id]
            buddy.props.current_activity = activity
            activity.add_current_buddy(buddy)
        else:
            buddy.props.current_activity = None

    def __buddy_joined_activity_cb(self, account, contact_id, activity_id):
        if contact_id not in self._buddies:
            # print('__buddy_joined_activity_cb Unknown buddy with '
            #              'contact_id %r', contact_id)
            return

        if activity_id not in self._activities:
            # print('__buddy_joined_activity_cb Unknown activity with '
            #              'activity_id %r', activity_id)
            return

        self._activities[activity_id].add_buddy(self._buddies[contact_id])

    def __buddy_left_activity_cb(self, account, contact_id, activity_id):
        if contact_id not in self._buddies:
            # print('__buddy_left_activity_cb Unknown buddy with '
            #              'contact_id %r', contact_id)
            return

        if activity_id not in self._activities:
            # print('__buddy_left_activity_cb Unknown activity with '
            #              'activity_id %r', activity_id)
            return

        self._activities[activity_id].remove_buddy(self._buddies[contact_id])

    def get_buddies(self):
        return list(self._buddies.values())

    def get_buddy_by_key(self, key):
        for buddy in list(self._buddies.values()):
            if buddy.key == key:
                return buddy
        return None

    def get_buddy_by_handle(self, contact_handle):
        for buddy in list(self._buddies.values()):
            if not buddy.is_owner() and buddy.handle == contact_handle:
                return buddy
        return None

    def get_activity(self, activity_id):
        return self._activities.get(activity_id, None)

    def get_activity_by_room(self, room_handle):
        for activity in list(self._activities.values()):
            if activity.room_handle == room_handle:
                return activity
        return None

    def get_activities(self):
        return list(self._activities.values())


_neighborhood = None


def get_neighborhood(params={}):
    global _neighborhood
    if _neighborhood is None:
        _neighborhood = Neighborhood(params)
    return _neighborhood


if __name__ == "__main__":
    params = {}
    params["nickname"] = "test"
    params["account_id"] = "test"
    params["server"] = "localhost"
    params["port"] = 5223
    params["password"] = "test"
    params["register"] = True

    loop = GObject.MainLoop()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    n = get_neighborhood(params)
    loop.run()
