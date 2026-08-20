#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2012, Gonzalo Odiard <godiard@gmail.com>
# Copyright (C) 2012, Walter Bender <walter@sugarlabs.org>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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

# HelpButton widget

from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import Gdk, GdkPixbuf, GLib

from sugar4.graphics.toolbutton import ToolButton
from sugar4.graphics.icon import Icon

from TurtleArt.tapalette import help_windows
from TurtleArt.tautils import get_screen_dimensions

import os
import logging
_logger = logging.getLogger('turtleart-activity')


class AnimatedGIFPicture(Gtk.Picture):
    def __init__(self, filename):
        super().__init__()
        self.anim = GdkPixbuf.PixbufAnimation.new_from_file(filename)
        self.iter = self.anim.get_iter(None)
        self._timeout_id = None
        self.connect('map', self._on_map)
        self.connect('unmap', self._on_unmap)
        self._update_frame()

    def _on_map(self, widget):
        self._schedule_next()

    def _on_unmap(self, widget):
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None

    def _update_frame(self):
        pixbuf = self.iter.get_pixbuf()
        if pixbuf:
            texture = Gdk.Texture.new_for_pixbuf(pixbuf)
            self.set_paintable(texture)

    def _schedule_next(self):
        delay = self.iter.get_delay_time()
        if delay >= 0:
            self._timeout_id = GLib.timeout_add(delay if delay > 0 else 100, self._on_timeout)

    def _on_timeout(self):
        self._timeout_id = None
        self.iter.advance(None)
        self._update_frame()
        self._schedule_next()
        return False


class HelpButton(Gtk.Box):

    def __init__(self, activity):
        self._activity = activity
        self._current_palette = 'turtle'

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        help_button = ToolButton('help-toolbar')
        help_button.set_tooltip(_('Help'))
        self.append(help_button)
        help_button.show()

        self._palette = help_button.get_palette()

        help_button.connect('clicked', self.__help_button_clicked_cb)

    def set_current_palette(self, name):
        self._current_palette = name

    def __help_button_clicked_cb(self, button):
        win = TutorialWindows(self._activity)
        win.execute()


class TutorialWindows:
    def __init__(self, parent_window=None):
        self.array = []
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        # Current Index of the Window we are at
        self.curr = 0

        # Add all the windows, with respective text

        w1 = TutorialWindow(parent_window)
        w1.description_label.set_text(
            "If it isn't already in the view, add the start block "
            "\nThen add the forward block and push start. "
            "\n"
            "\nEvery block inside start is executed after we click the start block.")

        w1.load_gif(os.path.join(self.base_dir, "GIF1.gif"), expand=False)

        w1.left_arrow.unparent()  # First Window doesn't have a left arrow
        w1.right_arrow.connect("clicked", self.on_right_click)

        self.array.append(w1)

        w2 = TutorialWindow(parent_window)
        w2.description_label.set_text(
            "Add the rotate block to make the turtle rotate by the angle specified."
            "\n"
            "\nEvery block inside the repeat block, will be repeated a specified number of time"
            "\n"
            "\nAfter that we put a clean button, which cleans the screen after being executed."
            "\n"
            "\nThen we use the block store in, to store the value 1 inside the box named my box_1."
            "\n"
            "\nFinally we move the turtle by the value stored in the box my box_1")

        w2.load_gif(os.path.join(self.base_dir, "GIF2.gif"))

        w2.left_arrow.connect("clicked", self.on_left_click)
        w2.right_arrow.connect("clicked", self.on_right_click)

        self.array.append(w2)

        w3 = TutorialWindow(parent_window)
        w3.description_label.set_text(
            "At the end of each cycle we increase the value in my box_1, to do this we use the sum block."
            "\n"
            "\nThis block sum the two value given, and when combined with the store in block, the result ends up in the my box_1."
            "\n"
            "\nBy doing so we effectively increase the value stored in my box_1.")

        w3.load_gif(os.path.join(self.base_dir, "GIF3.gif"))

        w3.left_arrow.connect("clicked", self.on_left_click)
        w3.right_arrow.connect("clicked", self.on_right_click)

        self.array.append(w3)

        # Add window n, that is the last window in our tutorial
        wn = TutorialWindow(parent_window)
        wn.description_label.set_text(
            "We reuse the sum block to dynamically change the color of the drawing based on the horizontal coordinate of the turtle (x value)."
            "\nThe horizontal coordinates are taken using the xcor block, then we divide the value by 6, the result is given to set color."
            "\n"
            "\nThe shade is chosen based on the heading of the turtle, taken using set_heading."
            "\n"
            "\n"
            "\nIt's all done, Good Luck and have fun!!!")

        wn.load_gif(os.path.join(self.base_dir, "GIF4.gif"))

        wn.right_arrow.unparent()  # Last Window doesn't have a right arrow
        wn.left_arrow.connect("clicked", self.on_left_click)

        self.array.append(wn)

    def on_right_click(self, button):

        self.array[self.curr + 1].show()
        self.array[self.curr].hide()

        # Increase curr by one
        self.curr += 1

    def on_left_click(self, button):
        self.array[self.curr - 1].show()
        self.array[self.curr].hide()

        # Decrease curr by one
        self.curr -= 1

    # We start by showing this
    def execute(self):
        self.array[0].show()


class TutorialWindow(Gtk.Window):
    def __init__(self, parent_window=None):
        super().__init__(title="")
        
        if parent_window:
            self.set_transient_for(parent_window)

        self.set_default_size(800, 800)

        # Main vertical layout
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox.set_margin_top(20)
        self.vbox.set_margin_bottom(20)
        self.vbox.set_margin_start(20)
        self.vbox.set_margin_end(20)
        self.set_child(self.vbox)

        self.box_gif = Gtk.Box()
        self.box_gif.set_size_request(100, 100)

        self.gif_path = None
        self.anim = None
        self.gif_image = None

        self.vbox.append(self.box_gif)

        # Horizontal box for the buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        self.left_arrow = Gtk.Button(label="←")
        self.left_arrow.set_hexpand(True)
        self.button_box.append(self.left_arrow)

        self.replay_button = Gtk.Button(label="⟳")
        self.replay_button.connect("clicked", self.on_replay_click)
        self.replay_button.set_hexpand(True)
        self.button_box.append(self.replay_button)

        self.right_arrow = Gtk.Button(label="→")
        self.right_arrow.set_hexpand(True)
        self.button_box.append(self.right_arrow)

        self.vbox.append(self.button_box)

        # Centered label below the buttons
        self.description_label = Gtk.Label(label="This will describe what's shown in the GIF.")
        self.description_label.set_justify(Gtk.Justification.CENTER)
        self.description_label.set_wrap(True)
        self.description_label.set_margin_bottom(10)
        self.description_label.set_margin_top(10)
        self.vbox.append(self.description_label)

    def load_gif(self, path, expand=True):
        if self.gif_image:
            self.gif_image.unparent()

        self.gif_path = path
        try:
            self.gif_image = AnimatedGIFPicture(self.gif_path)
        except Exception as e:
            self.gif_image = Gtk.Label(label="Failed to load image!\nPath: " + self.gif_path + "\nError: " + str(e))
            
        if expand:
            self.gif_image.set_hexpand(True)
            self.gif_image.set_vexpand(True)
        else:
            self.gif_image.set_hexpand(False)
            self.gif_image.set_vexpand(False)
        self.box_gif.append(self.gif_image)

    def on_replay_click(self, button):
        self.load_gif(self.gif_path)
        self.show()


def add_section(help_box, section_text, icon=None):
    ''' Add a section to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    screen_w, screen_h = get_screen_dimensions()
    max_text_width = int(screen_w / 3) - 20
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    label = Gtk.Label()
    label.set_use_markup(True)
    label.set_markup('<b>%s</b>' % section_text)
    label.set_wrap(True)
    label.set_size_request(max_text_width, -1)
    hbox.append(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.append(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show()
    hbox.set_margin_start(5)
    hbox.set_margin_end(5)
    hbox.set_margin_top(5)
    hbox.set_margin_bottom(5)
    help_box.append(hbox)


def add_paragraph(help_box, text, icon=None):
    ''' Add an entry to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    screen_w, screen_h = get_screen_dimensions()
    max_text_width = int(screen_w / 3) - 20
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    label = Gtk.Label(label=text)
    label.set_justify(Gtk.Justification.LEFT)
    label.set_wrap(True)
    hbox.append(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.append(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show()
    hbox.set_margin_start(5)
    hbox.set_margin_end(5)
    hbox.set_margin_top(5)
    hbox.set_margin_bottom(5)
    help_box.append(hbox)

    return hbox
