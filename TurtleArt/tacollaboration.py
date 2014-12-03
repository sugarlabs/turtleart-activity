# Copyright (c) 2011-13 Walter Bender
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

from dbus.service import signal
from dbus.gobject_service import ExportedGObject
import telepathy
import os
import gtk

from gettext import gettext as _

from TurtleArt.tautils import (data_to_string, data_from_string, get_path,
                               base64_to_image, debug_output, error_output)
from TurtleArt.taconstants import DEFAULT_TURTLE_COLORS

try:
    from sugar import profile
    from sugar.presence import presenceservice
    from sugar.presence.tubeconn import TubeConnection
except:
    profile = None
    from collaboration import presenceservice
    from collaboration.tubeconn import TubeConnection

SERVICE = 'org.laptop.TurtleArtActivity'
IFACE = SERVICE
PATH = '/org/laptop/TurtleArtActivity'


class Collaboration():

    def __init__(self, tw, activity):
        """ A simplistic sharing model: the sharer is the master """
        self._tw = tw
        self._tw.send_event = self.send_event
        self._tw.remote_turtle_dictionary = {}
        self._activity = activity
        self._setup_dispatch_table()

    def setup(self):
        # TODO: hand off role of master if sharer leaves
        self.pservice = presenceservice.get_instance()
        self.initiating = None  # sharing (True) or joining (False)

        # Add my buddy object to the list
        owner = self.pservice.get_owner()
        self.owner = owner
        self._tw.buddies.append(self.owner)
        self._share = ''
        self._activity.connect('shared', self._shared_cb)
        self._activity.connect('joined', self._joined_cb)

    def _setup_dispatch_table(self):
        self._processing_methods = {
            't': self._turtle_request,
            'T': self._receive_turtle_dict,
            'R': self._reskin_turtle,
            'f': self._move_forward,
            'a': self._move_in_arc,
            'r': self._rotate_turtle,
            'x': self._set_xy,
            'W': self._draw_text,
            'c': self._set_pen_color,
            'g': self._set_pen_gray_level,
            's': self._set_pen_shade,
            'w': self._set_pen_width,
            'p': self._set_pen_state,
            'F': self._fill_polygon,
            'P': self._draw_pixbuf,
            'B': self._paste,
            'S': self._speak
        }

    def _shared_cb(self, activity):
        self._shared_activity = self._activity.get_shared_activity()
        if self._shared_activity is None:
            debug_output('Failed to share or join activity ... \
                _shared_activity is null in _shared_cb()',
                         self._tw.running_sugar)
            return

        self._tw.set_sharing(True)

        self.initiating = True
        self.waiting_for_turtles = False
        self._tw.remote_turtle_dictionary = self._get_dictionary()

        debug_output('I am sharing...', self._tw.running_sugar)

        self.conn = self._shared_activity.telepathy_conn
        self.tubes_chan = self._shared_activity.telepathy_tubes_chan
        self.text_chan = self._shared_activity.telepathy_text_chan

        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal(
            'NewTube', self._new_tube_cb)

        debug_output('This is my activity: making a tube...',
                     self._tw.running_sugar)

        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferDBusTube(
            SERVICE, {})
        self._enable_share_button()

    def _joined_cb(self, activity):
        self._shared_activity = self._activity.get_shared_activity()
        if self._shared_activity is None:
            debug_output('Failed to share or join activity ... \
                _shared_activity is null in _shared_cb()',
                         self._tw.running_sugar)
            return

        self._tw.set_sharing(True)

        self.initiating = False
        self.conn = self._shared_activity.telepathy_conn
        self.tubes_chan = self._shared_activity.telepathy_tubes_chan
        self.text_chan = self._shared_activity.telepathy_text_chan

        # call back for "NewTube" signal
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal(
            'NewTube', self._new_tube_cb)

        debug_output('I am joining an activity: waiting for a tube...',
                     self._tw.running_sugar)
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb,
            error_handler=self._list_tubes_error_cb)

        # Joiner should request current state from sharer.
        self.waiting_for_turtles = True
        self._enable_share_button()

    def _enable_share_button(self):
        self._activity.share_button.set_icon('shareon')
        self._activity.share_button.set_tooltip(_('Share selected blocks'))

    def _list_tubes_reply_cb(self, tubes):
        for tube_info in tubes:
            self._new_tube_cb(*tube_info)

    def _list_tubes_error_cb(self, e):
        error_output('ListTubes() failed: %s' % (e), self._tw.running_sugar)

    def _new_tube_cb(self, id, initiator, type, service, params, state):
        """ Create a new tube. """
        debug_output(
            'New tube: ID=%d initator=%d type=%d service=%s \
                     params=%r state=%d' %
            (id, initiator, type, service, params, state), self._tw.running_sugar)

        if (type == telepathy.TUBE_TYPE_DBUS and service == SERVICE):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES]\
                    .AcceptDBusTube(id)

            tube_conn = TubeConnection(
                self.conn,
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES],
                id,
                group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])

            # We'll use a chat tube to send serialized stacks back and forth.
            self.chattube = ChatTube(tube_conn, self.initiating,
                                     self.event_received_cb)

            # Now that we have the tube, we can ask for the turtle dictionary.
            if self.waiting_for_turtles:  # A joiner must wait for turtles.
                debug_output('Sending a request for the turtle dictionary',
                             self._tw.running_sugar)
                # We need to send our own nick, colors, and turtle position
                colors = self._get_colors()
                event = 't|' + data_to_string([self._get_nick(), colors])
                debug_output(event, self._tw.running_sugar)
                self.send_event(event)

    def event_received_cb(self, event_message):
        """
        Events are sent as a tuple, nick|cmd, where nick is a turle name
        and cmd is a turtle event. Everyone gets the turtle dictionary from
        the sharer and watches for 't' events, which indicate that a new
        turtle has joined.
        """
        if len(event_message) == 0:
            return

       # Save active Turtle
        save_active_turtle = self._tw.turtles.get_active_turtle()

        try:
            command, payload = event_message.split('|', 2)
        except ValueError:
            debug_output('Could not split event message [%s]' % event_message,
                         self._tw.running_sugar)

        self._processing_methods[command](payload)

        # Restore active Turtle
        self._tw.turtles.set_turtle(
            self._tw.turtles.get_turtle_key(save_active_turtle))

    def send_event(self, entry):
        """ Send event through the tube. """
        if hasattr(self, 'chattube') and self.chattube is not None:
            self.chattube.SendText(entry)

    def _turtle_request(self, payload):
        ''' incoming turtle from a joiner '''
        if payload > 0:
            [nick, colors] = data_from_string(payload)
            if nick != self._tw.nick:  # It is not me.
                # There may not be a turtle dictionary.
                if hasattr(self._tw, 'remote_turtle_dictionary'):
                    # Make sure it is not a "rejoin".
                    if not nick in self._tw.remote_turtle_dictionary:
                        # Add new turtle for the joiner.
                        self._tw.turtles.set_turtle(nick, colors)
                        self._tw.label_remote_turtle(nick, colors)
                    self._tw.remote_turtle_dictionary[nick] = colors
                else:
                    self._tw.remote_turtle_dictionary = self._get_dictionary()
                    # Add new turtle for the joiner.
                    self._tw.turtles.set_turtle(nick, colors)
                    self._tw.label_remote_turtle(nick, colors)

        # Sharer should send the updated remote turtle dictionary to everyone.
        if self.initiating:
            if not self._tw.nick in self._tw.remote_turtle_dictionary:
                self._tw.remote_turtle_dictionary[self._tw.nick] = \
                    self._get_colors()
            event_payload = data_to_string(self._tw.remote_turtle_dictionary)
            self.send_event('T|' + event_payload)
            self.send_my_xy()  # And the sender should report her xy position.

    def _receive_turtle_dict(self, payload):
        ''' Any time there is a new joiner, an updated turtle dictionary is
        circulated. Everyone must report their turtle positions so that we
        are in sync. '''
        if self.waiting_for_turtles:
            if len(payload) > 0:
                # Grab the new remote turtles dictionary.
                remote_turtle_dictionary = data_from_string(payload)
                # Add see what is new.
                for nick in remote_turtle_dictionary:
                    if nick == self._tw.nick:
                        debug_output('skipping my nick %s' %
                                     (nick), self._tw.running_sugar)
                    elif nick != self._tw.remote_turtle_dictionary:
                        # Add new the turtle.
                        colors = remote_turtle_dictionary[nick]
                        self._tw.remote_turtle_dictionary[nick] = colors
                        self._tw.turtles.set_turtle(nick, colors)
                        # Label the remote turtle.
                        self._tw.label_remote_turtle(nick, colors)
                        debug_output('adding %s to remote turtle dictionary' %
                                     (nick), self._tw.running_sugar)
                    else:
                        debug_output('%s already in remote turtle dictionary' %
                                     (nick), self._tw.running_sugar)
            self.waiting_for_turtles = False
        self.send_my_xy()

    def send_my_xy(self):
        ''' Set xy location so joiner can sync turtle positions. Should be
        used to sync positions after turtle drag. '''
        self._tw.turtles.set_turtle(self._get_nick())
        if self._tw.turtles.get_active_turtle().get_pen_state():
            self.send_event('p|%s' % (data_to_string([self._get_nick(),
                                                      False])))
            put_pen_back_down = True
        else:
            put_pen_back_down = False
        self.send_event('x|%s' % (data_to_string(
            [self._get_nick(),
             [int(self._tw.turtles.get_active_turtle().get_xy()[0]),
              int(self._tw.turtles.get_active_turtle().get_xy()[1])]])))
        if put_pen_back_down:
            self.send_event('p|%s' % (data_to_string([self._get_nick(),
                                                      True])))
        self.send_event('r|%s' % (data_to_string(
            [self._get_nick(),
             int(self._tw.turtles.get_active_turtle().get_heading())])))

    def _reskin_turtle(self, payload):
        if len(payload) > 0:
            [nick, [width, height, data]] = data_from_string(payload)
            if nick != self._tw.nick:
                if self._tw.running_sugar:
                    tmp_path = get_path(self._tw.activity, 'instance')
                else:
                    tmp_path = '/tmp'
                file_name = base64_to_image(data, tmp_path)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(file_name,
                                                              width, height)
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_shapes([pixbuf])

    def _draw_pixbuf(self, payload):
        if len(payload) > 0:
            [nick, [a, b, x, y, w, h, width, height, data]] =\
                data_from_string(payload)
            if nick != self._tw.nick:
                if self._tw.running_sugar:
                    tmp_path = get_path(self._tw.activity, 'instance')
                else:
                    tmp_path = '/tmp'
                file_name = base64_to_image(data, tmp_path)
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(file_name,
                                                              width, height)
                pos = self._tw.turtles.turtle_to_screen_coordinates((x, y))
                self._tw.turtles.get_active_turtle().draw_pixbuf(
                    pixbuf, a, b, pos[0], pos[1], w, h, file_name, False)

    def _move_forward(self, payload):
        if len(payload) > 0:
            [nick, x] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().forward(x, False)

    def _move_in_arc(self, payload):
        if len(payload) > 0:
            [nick, [a, r]] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().arc(a, r, False)

    def _rotate_turtle(self, payload):
        if len(payload) > 0:
            [nick, h] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_heading(h, False)

    def _set_xy(self, payload):
        if len(payload) > 0:
            [nick, [x, y]] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_xy(x, y, share=False)

    def _draw_text(self, payload):
        if len(payload) > 0:
            [nick, [label, x, y, size, w]] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().draw_text(
                    label, x, y, size, w, False)

    def _set_pen_color(self, payload):
        if len(payload) > 0:
            [nick, x] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_color(x, False)

    def _set_pen_gray_level(self, payload):
        if len(payload) > 0:
            [nick, x] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_gray(x, False)

    def _set_pen_shade(self, payload):
        if len(payload) > 0:
            [nick, x] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_shade(x, False)

    def _set_pen_width(self, payload):
        if len(payload) > 0:
            [nick, x] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_pen_size(x, False)

    def _set_pen_state(self, payload):
        if len(payload) > 0:
            [nick, x] = data_from_string(payload)
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_pen_state(x, False)

    def _fill_polygon(self, payload):
        if len(payload) > 0:
            [nick, poly_points] = data_from_string(payload)
            shared_poly_points = []
            for i in range(len(poly_points)):
                x, y = self._tw.turtles.screen_to_turtle_coordinates(
                    (poly_points[i][1], poly_points[i][2]))
                if poly_points[i][0] in ['move', 'line']:
                    shared_poly_points.append((poly_points[i][0], x, y))
                elif poly_points[i][0] in ['rarc', 'larc']:
                    shared_poly_points.append(
                        (poly_points[i][0],
                         x,
                         y,
                         poly_points[i][3],
                            poly_points[i][4],
                            poly_points[i][5]))
            if nick != self._tw.nick:
                self._tw.turtles.set_turtle(nick)
                self._tw.turtles.get_active_turtle().set_poly_points(
                    shared_poly_points)
                self._tw.turtles.get_active_turtle().stop_fill(False)

    def _speak(self, payload):
        if len(payload) > 0:
            [nick, language_option, text] = data_from_string(payload)
            if language_option == 'None':
                language_option = ''
            if text is not None:
                os.system('espeak %s "%s" --stdout | aplay' %
                          (language_option, str(text)))

    def _paste(self, payload):
        if len(payload) > 0:
            [nick, text] = data_from_string(payload)
            if text is not None:
                self._tw.process_data(data_from_string(text),
                                      self._tw.paste_offset)
                self._tw.paste_offset += 20

    def _get_dictionary(self):
        return {self._get_nick(): self._get_colors()}

    def _get_nick(self):
        return self._tw.nick

    def _get_colors(self):
        colors = None
        if self._tw.running_sugar:
            if profile.get_color() is not None:
                colors = profile.get_color().to_string()
        else:
            colors = self._activity.get_colors()
        if colors is None:
            colors = '%s,%s' % (DEFAULT_TURTLE_COLORS[0],
                                DEFAULT_TURTLE_COLORS[1])
        return colors.split(',')


class ChatTube(ExportedGObject):

    def __init__(self, tube, is_initiator, stack_received_cb):
        """Class for setting up tube for sharing."""
        super(ChatTube, self).__init__(tube, PATH)
        self.tube = tube
        self.is_initiator = is_initiator  # Are we sharing or joining activity?
        self.stack_received_cb = stack_received_cb
        self.stack = ''

        self.tube.add_signal_receiver(self.send_stack_cb, 'SendText', IFACE,
                                      path=PATH, sender_keyword='sender')

    def send_stack_cb(self, text, sender=None):
        if sender == self.tube.get_unique_name():
            return
        self.stack = text
        self.stack_received_cb(text)

    @signal(dbus_interface=IFACE, signature='s')
    def SendText(self, text):
        self.stack = text
