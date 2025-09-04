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
from gi.repository import Gdk, GdkPixbuf

from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon

from TurtleArt.tapalette import help_windows

import logging
_logger = logging.getLogger('turtleart-activity')


class HelpButton(Gtk.ToolItem):

    def __init__(self, activity):
        self._activity = activity
        self._current_palette = 'turtle'

        Gtk.ToolItem.__init__(self)

        help_button = ToolButton('help-toolbar')
        help_button.set_tooltip(_('Help'))
        self.add(help_button)
        help_button.show()

        self._palette = help_button.get_palette()

        help_button.connect('clicked', self.__help_button_clicked_cb)

    def set_current_palette(self, name):
        self._current_palette = name

    def __help_button_clicked_cb(self, button):
        win = TutorialWindows()
        win.execute()


class TutorialWindows:
    def __init__(self):
        self.array = []

        # Current Index of the Window we are at
        self.curr = 0

        # Add all the windows, with respective text

        # Window 1
        w1 = TutorialWindow()
        w1.description_label.set_text("If it isn't already in the view, add the start block "
                                      "\n Then add the forward block and push start. "
                                      "\n"
                                      "\n Every block inside start is executed after we click the start block.")

        w1.gif_path = "GIF1.gif"
        w1.anim = GdkPixbuf.PixbufAnimation.new_from_file(w1.gif_path)
        w1.gif_image = Gtk.Image.new_from_animation(w1.anim)
        w1.box_gif.pack_start(w1.gif_image, False, False, 0)

        w1.left_arrow.destroy()  # First Window doesn't have a left arrow
        w1.right_arrow.connect("clicked", self.on_right_click)

        self.array.append(w1)

        # Window 2
        w2 = TutorialWindow()
        w2.description_label.set_text("Add the rotate block to make the turtle rotate by the angle specified."
                                      "\n"
                                      "\nEvery block inside the repeat block, will be repeated a specified number of time"
                                      "\n"
                                      "\nAfter that we put a clean button, which cleans the screen after being executed."
                                      "\n"
                                      "\nThen we use the block store in, to store the value 1 inside the box named my box_1."
                                      "\n"
                                      "\nFinally we move the turtle by the value stored in the box my box_1")

        w2.gif_path = "GIF2.gif"
        w2.anim = GdkPixbuf.PixbufAnimation.new_from_file(w2.gif_path)
        w2.gif_image = Gtk.Image.new_from_animation(w2.anim)
        w2.box_gif.pack_start(w2.gif_image, True, True, 0)

        w2.left_arrow.connect("clicked", self.on_left_click)
        w2.right_arrow.connect("clicked", self.on_right_click)

        self.array.append(w2)

        # Window 3
        w3 = TutorialWindow()
        w3.description_label.set_text(
            "At the end of each cycle we increase the value in my box_1, to do this we use the sum block."
            "\n"
            "\nThis block sum the two value given, and when combined with the store in block, the result ends up in the my box_1."
            "\n"
            "\nBy doing so we effectively increase the value stored in my box_1.")

        w3.gif_path = "GIF3.gif"
        w3.anim = GdkPixbuf.PixbufAnimation.new_from_file(w3.gif_path)
        w3.gif_image = Gtk.Image.new_from_animation(w3.anim)
        w3.box_gif.pack_start(w3.gif_image, True, True, 0)

        w3.left_arrow.connect("clicked", self.on_left_click)
        w3.right_arrow.connect("clicked", self.on_right_click)

        self.array.append(w3)

        # Window n
        wn = TutorialWindow()
        wn.description_label.set_text(
            "We reuse the sum block to dynamically change the color of the drawing based on the horizontal coordinate of the turtle (x value)."
            "\nThe horizontal coordinates are taken using the xcor block, then we divide the value by 6, the result is given to set color."
            "\n"
            "\nThe shade is chosen based on the heading of the turtle, taken using set_heading."
            "\n"
            "\n"
            "\nIt's all done, Good Luck and have fun!!!")

        wn.gif_path = "GIF4.gif"
        wn.anim = GdkPixbuf.PixbufAnimation.new_from_file(wn.gif_path)
        wn.gif_image = Gtk.Image.new_from_animation(wn.anim)
        wn.box_gif.pack_start(wn.gif_image, True, True, 0)

        wn.right_arrow.destroy()  # Last Window doesn't have a right arrow
        wn.left_arrow.connect("clicked", self.on_left_click)

        self.array.append(wn)

    def on_right_click(self, button):

        self.array[self.curr + 1].show_all()
        self.array[self.curr].hide()

        # Increase curr by one
        self.curr += 1

    def on_left_click(self, button):
        self.array[self.curr - 1].show_all()
        self.array[self.curr].hide()

        # Decrease curr by one
        self.curr -= 1

    # We start by showing this
    def execute(self):
        self.array[0].show_all()


class TutorialWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="")

        self.set_default_size(800, 800)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.NONE)

        # Main vertical layout
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        self.box_gif = Gtk.Box()
        self.box_gif.set_size_request(100, 100)

        self.gif_path = None
        self.anim = None
        self.gif_image = None

        self.vbox.pack_start(self.box_gif, False, False, 0)

        # Horizontal box for the buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        self.left_arrow = Gtk.Button()
        self.left_arrow.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.button_box.pack_start(self.left_arrow, True, True, 0)

        self.replay_button = Gtk.Button(label="⟳")
        self.replay_button.connect("clicked", self.on_replay_click)
        self.button_box.pack_start(self.replay_button, True, True, 0)

        self.right_arrow = Gtk.Button()
        self.right_arrow.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.button_box.pack_start(self.right_arrow, True, True, 0)

        self.vbox.pack_start(self.button_box, False, False, 0)

        # Centered label below the buttons
        self.description_label = Gtk.Label(label="This will describe what's shown in the GIF.")
        self.description_label.set_justify(Gtk.Justification.CENTER)
        self.description_label.set_line_wrap(True)
        self.vbox.pack_start(self.description_label, False, False, 10)

    def on_replay_click(self, button):
        self.gif_image.destroy()

        self.anim = GdkPixbuf.PixbufAnimation.new_from_file(self.gif_path)
        self.gif_image = Gtk.Image.new_from_animation(self.anim)
        self.box_gif.pack_start(self.gif_image, True, True, 0)

        self.show_all()


def add_section(help_box, section_text, icon=None):
    ''' Add a section to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    max_text_width = int(Gdk.Screen.width() / 3) - 20
    hbox = Gtk.HBox()
    label = Gtk.Label()
    label.set_use_markup(True)
    label.set_markup('<b>%s</b>' % section_text)
    label.set_line_wrap(True)
    label.set_size_request(max_text_width, -1)
    hbox.add(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.add(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show_all()
    help_box.pack_start(hbox, False, False, padding=5)


def add_paragraph(help_box, text, icon=None):
    ''' Add an entry to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    max_text_width = int(Gdk.Screen.width() / 3) - 20
    hbox = Gtk.HBox()
    label = Gtk.Label(label=text)
    label.set_justify(Gtk.Justification.LEFT)
    label.set_line_wrap(True)
    hbox.add(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.add(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show_all()
    help_box.pack_start(hbox, False, False, padding=5)

    return hbox
