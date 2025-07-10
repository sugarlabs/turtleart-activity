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

import os

from gettext import gettext as _

from gi.repository import GdkPixbuf

from TurtleArt.tautils import data_to_string, data_from_string, get_path, \
    base64_to_image, debug_output, error_output
from TurtleArt.taconstants import DEFAULT_TURTLE_COLORS

from sugar3 import profile
from sugar3.presence import presenceservice

from .textchannelwrapper import CollabWrapper


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
        self._activity.connect('shared', self._activity_shared_cb)
        self._activity.connect('joined', self._activity_joined_cb)

        self.collab = CollabWrapper(self._activity)
        self.collab.connect('message', self._message_cb)
        self.collab.connect('joined', self._joined_cb)
        self.collab.setup()

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

    def _activity_shared_cb(self, activity):
        self._tw.set_sharing(True)

        self.initiating = True
        self.waiting_for_turtles = False
        self._tw.remote_turtle_dictionary = self._get_dictionary()
        self._enable_share_button()

    def _activity_joined_cb(self, activity):
        self._tw.set_sharing(True)

        self.initiating = False
        # Joiner is to request current state from sharer.
        self.waiting_for_turtles = True
        self._enable_share_button()

    def _joined_cb(self, collab):
        # Now that we have the tube, we can ask for the turtle dictionary.
        debug_output('Sending a request for the turtle dictionary',
                     self._tw.running_sugar)
        # We need to send our own nick, colors, and turtle position
        colors = self._get_colors()
        event = data_to_string([self._get_nick(), colors])
        debug_output(event, self._tw.running_sugar)
        self.send_event('t', event)

    def _enable_share_button(self):
        self._activity.share_button.set_icon_name('shareon')
        self._activity.share_button.set_tooltip(_('Share selected blocks'))

    def _message_cb(self, colab, buddy, msg):
        """
        Events are sent as action and payload.  Everyone gets the
        turtle dictionary from the sharer and watches for 't' events,
        which indicate that a new turtle has joined.
        """

        action = msg.get('action')

        if action in self._processing_methods:
            save_active_turtle = self._tw.turtles.get_active_turtle()
            self._processing_methods[action](msg.get('event'))
            self._tw.turtles.set_turtle(
                self._tw.turtles.get_turtle_key(save_active_turtle))
            return

        if action == '!!ACTION_INIT_REQUEST':
            return

        error_output('unhandled action %r' % action)

    def send_event(self, action, event):
        """ Send event through the tube. """
        event = {'action': action, 'event': event}

        self.collab.post(event)

    def _turtle_request(self, payload):
        ''' incoming turtle from a joiner '''
        if len(payload) > 0:
            [nick, colors] = data_from_string(payload)
            # FIXME: nick may not be unique, use buddy hash
            if nick != self._tw.nick:  # It is not me.
                # There may not be a turtle dictionary.
                if hasattr(self._tw, 'remote_turtle_dictionary'):
                    # Make sure it is not a "rejoin".
                    if nick not in self._tw.remote_turtle_dictionary:
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
            if self._tw.nick not in self._tw.remote_turtle_dictionary:
                self._tw.remote_turtle_dictionary[self._tw.nick] = \
                    self._get_colors()
            event = data_to_string(self._tw.remote_turtle_dictionary)
            self.send_event('T', event)
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
            self.send_event('p', data_to_string([self._get_nick(), False]))
            put_pen_back_down = True
        else:
            put_pen_back_down = False
        self.send_event(
            'x', data_to_string(
                [self._get_nick(),
                 [int(self._tw.turtles.get_active_turtle().get_xy()[0]),
                  int(self._tw.turtles.get_active_turtle().get_xy()[1])]]))
        if put_pen_back_down:
            self.send_event('p', data_to_string([self._get_nick(), True]))
        self.send_event(
            'r', data_to_string(
                [self._get_nick(),
                 int(self._tw.turtles.get_active_turtle().get_heading())]))

    def _reskin_turtle(self, payload):
        if len(payload) > 0:
            [nick, [width, height, data]] = data_from_string(payload)
            if nick != self._tw.nick:
                if self._tw.running_sugar:
                    tmp_path = get_path(self._tw.activity, 'instance')
                else:
                    tmp_path = '/tmp'
                file_name = base64_to_image(data, tmp_path)
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(file_name,
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
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(file_name,
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
                if self._tw.running_sugar:
                    from sugar3.speech import SpeechManager
                    sm = SpeechManager()
                    sm.say_text(text)
                else:
                    os.system(
                        'espeak %s "%s" --stdout | aplay' %
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
