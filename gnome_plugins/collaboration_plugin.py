#!/usr/bin/env python3
# Copyright (c) 2011 Walter Bender
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys

sys.path.append("..")
import os.path

import dbus
from gettext import gettext as _

from .plugin import Plugin

from TurtleArt.util.menubuilder import make_menu_item, make_sub_menu
from TurtleArt.util.configfile import ConfigFile
from TurtleArt.util.configwizard import ConfigWizard

from collaboration.neighborhood import get_neighborhood
from collaboration.connectionmanager import get_connection_manager
from collaboration.activity import Activity
from collaboration import telepathyclient

from TurtleArt.tacollaboration import Collaboration

import traceback

from gi.repository import Gtk
from gi.repository import GObject

CONNECTION_INTERFACE_ACTIVITY_PROPERTIES = \
    'org.laptop.Telepathy.ActivityProperties'


class Collaboration_plugin(Plugin):
    __gsignals__ = {
        'joined': (GObject.SignalFlags.RUN_FIRST, None,
                   ()),
        'shared': (GObject.SignalFlags.RUN_FIRST, None,
                   ()), }

    def __init__(self, parent):
        Plugin.__init__(self)

        self._parent = parent
        self._neighborhood = None
        self._title = _('My Turtle Art session')
        self._bundle_id = "org.laptop.TurtleArt"
        # This could be hashed from the file path (if resuming)
        self._activity_id = "1234567"
        self._nick = ""
        self._setup_has_been_called = False
        # FIXME To fix attribution errors, had to add variable declaration
        self.shared_activity = None
        self.metadata = None

    def _setup_config_file(self, config_file_path):
        self._config_file_path = os.path.join(config_file_path,
                                              'turtleartrc.collab')
        self._collaboration_config_values = ConfigFile(self._config_file_path)
        self._valid_config_values = {
            'nick': {'type': 'text'},
            'account_id': {'type': 'text'},
            'password': {'type': 'text'},
            'server': {'type': 'text'},
            'port': {'type': 'integer'},
            'register': {'type': 'boolean'},
            'colors': {'type': 'text'}}

    def _connect_cb(self, button):
        """ Enable connection """
        self._collaboration_config_values.set_valid_keys(
            self._valid_config_values)
        self._collaboration_config_values.connect(
            'configuration-loaded', self._connect_to_neighborhood)
        self._collaboration_config_values.connect(
            'configuration-saved', self._connect_to_neighborhood)
        self._collaboration_config_values.load()
        self.setup()

    def setup(self):
        self._collaboration = Collaboration(self.tw, self)
        self._collaboration.setup()
        # Do we know if we were successful?
        self._setup_has_been_called = True
        # TODO:
        #     use set_sensitive to enable Share and Configuration menuitems

    def set_tw(self, turtleart_window):
        self.tw = turtleart_window
        self.tw.nick = self._get_nick()
        self._setup_config_file(self._parent.get_config_home())

    def get_menu(self):
        menu = Gtk.Menu()

        make_menu_item(menu, _('Enable collaboration'),
                       self._connect_cb)

        self._activities_submenu = Gtk.Menu()
        activities_menu = make_sub_menu(self._activities_submenu,
                                        _('Activities'))
        menu.append(activities_menu)

        self._buddies_submenu = Gtk.Menu()
        buddies_menu = make_sub_menu(self._buddies_submenu,
                                     _('Buddies'))
        menu.append(buddies_menu)

        make_menu_item(menu, _('Share'), self._share_cb)
        make_menu_item(menu, _('Configuration'),
                       self._config_neighborhood_cb)

        neighborhood_menu = make_sub_menu(menu, _('Neighborhood'))

        return neighborhood_menu

    def send_xy(self):
        ''' Resync xy position (and orientation) of my turtle. '''
        self._collaboration.send_my_xy()

    def get_colors(self):
        return self._colors

    def _get_nick(self):
        return self._nick

    def _get_activity_id(self):
        return self._activity_id

    def _get_bundle_id(self):
        return self._bundle_id

    def _get_title(self):
        return self._title

    def _connect_to_neighborhood(self, config_file_obj):
        if self._neighborhood is not None:
            return

        params = {}
        params['nickname'] = self._collaboration_config_values.get('nick')
        params['account_id'] = self._collaboration_config_values.get(
            'account_id')
        params['server'] = self._collaboration_config_values.get('server')
        params['port'] = self._collaboration_config_values.get('port')
        params['password'] = self._collaboration_config_values.get('password')
        params['register'] = self._collaboration_config_values.get('register')
        if params['server'] == '':
            raise RuntimeError('Invalid server address')

        self._nick = self._collaboration_config_values.get('nick')
        # Tell the parent activity that the nick may have changed
        self._parent.nick_changed(self._nick)

        self._colors = self._collaboration_config_values.get('colors')
        # Tell the parent activity that the colors may have changed
        self._parent.color_changed(self._colors)

        self._activities = {}
        self._buddies = {}

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self._client_handler = telepathyclient.get_instance()
        if self._client_handler is None:
            raise RuntimeError('Telepathy client unavailable')
        self._neighborhood = get_neighborhood(params)
        self._neighborhood.connect('activity-added', self._activity_added_cb)
        self._neighborhood.connect('activity-removed',
                                   self._activity_removed_cb)
        self._neighborhood.connect('buddy-added', self._buddy_added_cb)
        self._neighborhood.connect('buddy-removed', self._buddy_removed_cb)

    # TODO:
    # - show nick of sharer
    # - show icon with color of sharer
    def _activity_added_cb(self, model, activity_model):
        self._activities[activity_model.props.name] = activity_model
        self._recreate_available_activities_menu()

    def _activity_removed_cb(self, model, activity_model):
        try:
            self._activities.pop(activity_model.props.name)
        except BaseException:
            print('Failed to remove activity %s' % activity_model.props.name)

        self._recreate_available_activities_menu()

    def _buddy_added_cb(self, activity, buddy):
        self._buddies[buddy.get_key()] = buddy
        self._recreate_available_buddies_menu()

    def _buddy_removed_cb(self, activity, buddy):
        try:
            self._buddies.pop(buddy.get_key())
        except BaseException:
            print("Couldn't remove buddy %s" % buddy.get_key())
        self._recreate_available_buddies_menu()

    # TODO: we should have a list of available actions over
    #       a given buddy. I.e.: a) chat with him b) make friend
    #       c) invite to current activity
    #
    def _recreate_available_buddies_menu(self):
        for child in self._buddies_submenu.get_children():
            self._buddies_submenu.remove(child)

        for buddy in list(self._buddies.values()):
            key = buddy.get_key()
            if key is None:
                key = ''
            n = buddy.get_nick() + '|' + key[0:15]
            make_menu_item(self._buddies_submenu, n,
                           self._buddy_actions_cb, buddy)

    def _buddy_actions_cb(self, widget, buddy):
        print('do something with %s' % buddy.get_nick())

    # TODO:
    #     we need an extra menu branch with a) 'Join' button b) List of buddies
    def _recreate_available_activities_menu(self):
        for child in self._activities_submenu.get_children():
            self._activities_submenu.remove(child)

        for activity in list(self._activities.values()):
            n = activity.props.name
            make_menu_item(self._activities_submenu, n,
                           self._join_activity_cb, activity)

    def _join_activity_cb(self, widget, activity):
        print('Lets try to join...')

        connection_manager = get_connection_manager()
        account_path, connection = \
            connection_manager.get_preferred_connection()
        if connection is None:
            print('No active connection available')
            return

        properties = {}
        properties['id'] = activity.activity_id
        properties['color'] = activity.get_color()
        print('room handle according to activity %s' % activity.room_handle)
        properties['private'] = True

        try:
            room_handle = connection.GetActivity(
                activity.activity_id,
                dbus_interface=CONNECTION_INTERFACE_ACTIVITY_PROPERTIES)
            print('room_handle = %s' % str(room_handle))
            self._joined_activity = Activity(
                account_path, connection, room_handle, properties=properties)
            # FIXME: this should be unified, no need to keep 2 references
            self.shared_activity = self._joined_activity
        except BaseException:
            traceback.print_exc(file=sys.stdout)

        if self._joined_activity.props.joined:
            raise RuntimeError('Activity %s is already shared.' %
                               activity.activity_id)

        self._joined_activity.connect('joined', self.__joined_cb)
        self._joined_activity.join()

    def __joined_cb(self, activity, success, err):
        print("We've joined an activity")
        self.emit('joined')

    def _config_neighborhood_cb(self, widget):
        if not self._setup_has_been_called:
            return
        config_w = ConfigWizard(self._config_file_path)
        config_items = [
            {'item_label': _('Nickname'), 'item_type': 'text',
             'item_name': 'nick'},
            {'item_label': _('Account ID'), 'item_type': 'text',
             'item_name': 'account_id'},
            {'item_label': _('Server'), 'item_type': 'text',
             'item_name': 'server'},
            {'item_label': _('Port'), 'item_type': 'text',
             'item_name': 'port'},
            {'item_label': _('Password'), 'item_type': 'text',
             'item_name': 'password'},
            {'item_label': _('Register'), 'item_type': 'boolean',
             'item_name': 'register'},
            {'item_label': _('Colors'), 'item_type': 'text',
             'item_name': 'colors'}]
        config_w.set_config_items(config_items)
        config_w.set_config_file_obj(self._collaboration_config_values)
        config_w.show()

    def _share_cb(self, button):
        if not self._setup_has_been_called:
            return
        properties = {}
        properties['id'] = self._get_activity_id()
        properties['type'] = self._get_bundle_id()
        properties['name'] = self._get_title()
        properties['color'] = self.get_colors()
        properties['private'] = False

        connection_manager = get_connection_manager()
        account_path, connection = \
            connection_manager.get_preferred_connection()

        if connection is None:
            print('No active connection available')
            return

        try:
            self._parent.shared_activity = Activity(account_path,
                                                    connection,
                                                    properties=properties)
            # FIXME: this should be unified, no need to keep 2 references
            self.shared_activity = self._parent.shared_activity
        except BaseException:
            traceback.print_exc(file=sys.stdout)

        if self._parent._shared_parent.props.joined:
            raise RuntimeError('Activity %s is already shared.' %
                               self._parent._get_activity_id())

        self._parent._shared_parent.share(self.__share_activity_cb,
                                          self.__share_activity_error_cb)

    def __share_activity_cb(self, activity):
        """Finish sharing the activity"""
        self.emit('shared')

    def __share_activity_error_cb(self, activity, error):
        """Notify with GObject event of unsuccessful sharing of activity"""
        print('%s got error: %s' % (activity, error))


if __name__ == '__main__':
    print('testing collaboration')
