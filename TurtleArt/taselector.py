# -*- coding: utf-8 -*-
# Copyright (c) 2014, Walter Bender

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

from .tautils import debug_output, error_output
from .tapalette import palette_names
from .taconstants import ICON_SIZE, CATEGORY_LAYER, TAB_LAYER
from .tasprite_factory import SVG, svg_from_file, svg_str_to_pixbuf
from .sprites import Sprite


def create_toolbar_background(sprite_list, width):
    # Create the toolbar background for the selectors
    spr = Sprite(sprite_list, 0, 0,
                 svg_str_to_pixbuf(SVG().toolbar(2 * width, ICON_SIZE)))
    spr.type = 'toolbar'
    spr.set_layer(CATEGORY_LAYER)
    return spr


class Selector():

    ''' Selector class abstraction  '''

    def __init__(self, turtle_window, n):
        '''This class handles the display of palette selectors (Only relevant
        to GNOME version and very old versions of Sugar).
        '''

        self.shapes = []
        self.spr = None
        self._turtle_window = turtle_window
        self._index = n

        if not n < len(palette_names):
            # Shouldn't happen, but hey...
            debug_output('palette index %d is out of range' % n,
                         self._turtle_window.running_sugar)
            self._name = 'extras'
        else:
            self._name = palette_names[n]

        icon_pathname = None
        for path in self._turtle_window.icon_paths:
            if os.path.exists(os.path.join(path, '%soff.svg' % (self._name))):
                icon_pathname = os.path.join(path, '%soff.svg' % (self._name))
                break

        if icon_pathname is not None:
            off_shape = svg_str_to_pixbuf(svg_from_file(icon_pathname))
        else:
            off_shape = svg_str_to_pixbuf(svg_from_file(os.path.join(
                self._turtle_window.icon_paths[0], 'extrasoff.svg')))
            error_output('Unable to open %soff.svg' % (self._name),
                         self._turtle_window.running_sugar)

        icon_pathname = None
        for path in self._turtle_window.icon_paths:
            if os.path.exists(os.path.join(path, '%son.svg' % (self._name))):
                icon_pathname = os.path.join(path, '%son.svg' % (self._name))
                break

        if icon_pathname is not None:
            on_shape = svg_str_to_pixbuf(svg_from_file(icon_pathname))
        else:
            on_shape = svg_str_to_pixbuf(svg_from_file(os.path.join(
                self._turtle_window.icon_paths[0], 'extrason.svg')))
            error_output('Unable to open %son.svg' % (self._name),
                         self._turtle_window.running_sugar)

        self.shapes.append(off_shape)
        self.shapes.append(on_shape)

        x = int(ICON_SIZE * self._index)
        self.spr = Sprite(self._turtle_window.sprite_list, x, 0, off_shape)
        self.spr.type = 'selector'
        self.spr.name = self._name
        self.set_layer()

    def set_shape(self, i):
        if self.spr is not None and i in [0, 1]:
            self.spr.set_shape(self.shapes[i])

    def set_layer(self, layer=TAB_LAYER):
        if self.spr is not None:
            self.spr.set_layer(layer)

    def hide(self):
        if self.spr is not None:
            self.spr.hide()
