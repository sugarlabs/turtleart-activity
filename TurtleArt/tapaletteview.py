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

_SKIN_IMAGE = 1
_MARGIN = 5
_BUTTON_SIZE = 32

from .tautils import find_group, debug_output, get_stack_width_and_height
from .tablock import Block
from .tapalette import (palette_names, palette_blocks, hidden_proto_blocks,
                        block_styles)
from .taconstants import (PALETTE_SCALE, ICON_SIZE, PYTHON_SKIN, XO1,
                          HORIZONTAL_PALETTE, PALETTE_WIDTH, PALETTE_HEIGHT,
                          CATEGORY_LAYER, TOP_LAYER, PROTO_LAYER)
from .tasprite_factory import SVG, svg_str_to_pixbuf
from .sprites import Sprite


class PaletteView():

    ''' Palette View class abstraction  '''

    def __init__(self, turtle_window, n):
        '''
        This class handles the display of block palettes
        '''
        self.blocks = []
        self.backgrounds = [None, None]
        self.visible = False
        self.populated = False

        self._turtle_window = turtle_window
        self._palette_index = n

        if not n < len(palette_names):
            # Shouldn't happen, but hey...
            debug_output('palette index %d is out of range' % n,
                         self._turtle_window.running_sugar)
            self._name = 'undefined'
        else:
            self._name = palette_names[n]

    def create(self, regenerate=True, show=False):
        if not self._name == 'undefined':
            # Create proto blocks for each palette entry
            self._create_proto_blocks()

            save_selected = self._turtle_window.selected_palette
            self.layout(regenerate=regenerate,
                        show=(show or save_selected == self._palette_index))

    def show(self):
        ''' Show palette background and proto blocks. If needed, display
            shift button. '''
        orientation = self._turtle_window.orientation
        if self.backgrounds[orientation] is not None:
            self.backgrounds[orientation].set_layer(CATEGORY_LAYER)

        for blk in self.blocks:
            if blk.get_visibility():
                blk.spr.set_layer(PROTO_LAYER)
            else:
                blk.spr.hide()

        self.display_palette_shift_buttons()

        self.visible = True

    def hide(self):
        ''' Hide the palette. '''
        for background in self.backgrounds:
            if background is not None:
                background.hide()

        for blk in self.blocks:
            blk.spr.hide()

        self._hide_palette_shift_buttons()

        if self._trash_palette():
            for blk in self._turtle_window.trash_stack:
                for gblk in find_group(blk):
                    gblk.spr.hide()

        self.visible = False

    def move(self, x, y):
        ''' Move the palette. '''
        buttons = self._turtle_window.palette_button

        for blk in self.blocks:
            blk.spr.move((x + blk.spr.save_xy[0], y + blk.spr.save_xy[1]))

        for button in buttons:
            button.move((x + button.save_xy[0], y + button.save_xy[1]))

        for spr in self.backgrounds:
            if spr is not None:
                spr.move((x + spr.save_xy[0], y + spr.save_xy[1]))

        if self._trash_palette():
            for blk in self._turtle_window.trash_stack:
                for gblk in find_group(blk):
                    gblk.spr.move((x + gblk.spr.save_xy[0],
                                   y + gblk.spr.save_xy[1]))

    def shift(self):
        ''' Shift blocks on the palette. '''
        buttons = self._turtle_window.palette_button
        orientation = self._turtle_window.orientation

        x, y = self.backgrounds[orientation].get_xy()
        w, h = self.backgrounds[orientation].get_dimensions()
        bx, by = self.blocks[0].spr.get_xy()
        if orientation == 0:
            width = self._turtle_window.width

            if bx != _BUTTON_SIZE:
                dx = w - width
            else:
                dx = width - w
            dy = 0
        else:
            height = self._turtle_window.height
            offset = self._turtle_window.toolbar_offset

            dx = 0
            if by != offset + _BUTTON_SIZE + _MARGIN:
                dy = h - height + ICON_SIZE
            else:
                dy = height - h - ICON_SIZE

        for blk in self.blocks:
            if blk.get_visibility():
                blk.spr.move_relative((dx, dy))

        buttons[orientation].set_layer(TOP_LAYER)
        if dx < 0 or dy < 0:
            buttons[orientation + 5].set_layer(TOP_LAYER)
            buttons[orientation + 3].hide()
        else:
            buttons[orientation + 5].hide()
            buttons[orientation + 3].set_layer(TOP_LAYER)

    def _create_proto_blocks(self):
        '''
        Create the proto blocks that will populate this palette.
        Reload the palette, but reuse the existing blocks.
        If a block doesn't exist, add it.
        '''
        for blk in self.blocks:
            blk.spr.hide()

        preexisting_blocks = self.blocks[:]
        self.blocks = []
        for name in palette_blocks[self._palette_index]:
            # Did we already create this block?
            preexisting_block = False
            for blk in preexisting_blocks:
                if blk.name == name:
                    self.blocks.append(blk)
                    preexisting_block = True
                    break

            # If not, create it now.
            if not preexisting_block:
                self.blocks.append(Block(self._turtle_window.block_list,
                                         self._turtle_window.sprite_list,
                                         name, 0, 0, 'proto', [],
                                         PALETTE_SCALE))
                if name in hidden_proto_blocks:
                    self.blocks[-1].set_visibility(False)
                else:
                    self.blocks[-1].spr.set_layer(PROTO_LAYER)
                    self.blocks[-1].unhighlight()
                    self.blocks[-1].resize()

                # Some proto blocks get a skin.
                if name in block_styles['box-style-media']:
                    self._proto_skin(name + 'small', self.blocks[-1].spr)
                elif name in block_styles['basic-style-extended']:
                    if name in self._turtle_window.media_shapes:
                        self._proto_skin(name, self.blocks[-1].spr)
                elif name in PYTHON_SKIN:
                    self._proto_skin('pythonsmall', self.blocks[-1].spr)
                elif len(self.blocks[-1].spr.labels) > 0:
                    self.blocks[-1].refresh()

        self.populated = True

    def _proto_skin(self, name, spr):
        ''' Utility for creating proto block skins '''
        x, y = self._turtle_window.calc_image_offset(name, spr)
        spr.set_image(self._turtle_window.media_shapes[name], _SKIN_IMAGE,
                      x, y)

    def _float_palette(self, spr):
        ''' We sometimes let the palette move with the canvas. '''
        if self._turtle_window.running_sugar and \
           self._turtle_window.hw not in [XO1]:
            spr.move_relative(
                (self._turtle_window.activity.hadj_value,
                 self._turtle_window.activity.vadj_value))

    def _trash_palette(self):
        return 'trash' in palette_names and \
            self._palette_index == palette_names.index('trash')

    def layout(self, regenerate=False, show=True):
        ''' Layout prototypes in a palette. '''

        offset = self._turtle_window.toolbar_offset
        buttons = self._turtle_window.palette_button
        orientation = self._turtle_window.orientation
        w = PALETTE_WIDTH
        h = PALETTE_HEIGHT

        if orientation == HORIZONTAL_PALETTE:
            x, y, max_w = self._horizontal_layout(
                _BUTTON_SIZE, offset + _MARGIN, self.blocks)
            if self._trash_palette():
                blocks = []  # self.blocks[:]
                for blk in self._turtle_window.trash_stack:
                    blocks.append(blk)
                x, y, max_w = self._horizontal_layout(x + max_w, y, blocks)
            w = x + max_w + _BUTTON_SIZE + _MARGIN
            if show:
                buttons[2].move((w - _BUTTON_SIZE, offset))
                buttons[4].move((_BUTTON_SIZE, offset))
                buttons[6].move((_BUTTON_SIZE, offset))
        else:
            x, y, max_h = self._vertical_layout(
                _MARGIN, offset + _BUTTON_SIZE + _MARGIN, self.blocks)
            if self._trash_palette():
                blocks = []  # self.blocks[:]
                for blk in self._turtle_window.trash_stack:
                    blocks.append(blk)
                x, y, max_h = self._vertical_layout(x, y + max_h, blocks)
            h = y + max_h + _BUTTON_SIZE + _MARGIN - offset
            if show:
                buttons[2].move((PALETTE_WIDTH - _BUTTON_SIZE, offset))
                buttons[3].move((0, offset + _BUTTON_SIZE))
                buttons[5].move((0, offset + _BUTTON_SIZE))

        self._make_background(0, offset, w, h, regenerate)

        if show:
            for blk in self.blocks:
                if blk.get_visibility():
                    blk.spr.set_layer(PROTO_LAYER)
                else:
                    blk.spr.hide()

            buttons[2].save_xy = buttons[2].get_xy()
            self._float_palette(buttons[2])
            self.backgrounds[orientation].set_layer(CATEGORY_LAYER)
            self.display_palette_shift_buttons()

            if self._trash_palette():
                for blk in self._turtle_window.trash_stack:
                    for gblk in find_group(blk):
                        gblk.spr.set_layer(PROTO_LAYER)

                svg = SVG()
                self.backgrounds[orientation].set_shape(
                    svg_str_to_pixbuf(svg.palette(w, h)))

    def _make_background(self, x, y, w, h, regenerate=False):
        ''' Make the background sprite for the palette. '''
        orientation = self._turtle_window.orientation

        if regenerate and not self.backgrounds[orientation] is None:
            self.backgrounds[orientation].hide()
            self.backgrounds[orientation] = None

        if self.backgrounds[orientation] is None:
            svg = SVG()
            self.backgrounds[orientation] = \
                Sprite(self._turtle_window.sprite_list, x, y,
                       svg_str_to_pixbuf(svg.palette(w, h)))
            self.backgrounds[orientation].save_xy = (x, y)

            self._float_palette(self.backgrounds[orientation])

            if orientation == 0 and w > self._turtle_window.width:
                self.backgrounds[orientation].type = \
                    'category-shift-horizontal'
            elif orientation == 1 and \
                    h > self._turtle_window.height - ICON_SIZE:
                self.backgrounds[orientation].type = \
                    'category-shift-vertical'
            else:
                self.backgrounds[orientation].type = 'category'

            '''
            if self._trash_palette():
                svg = SVG()
                self.backgrounds[orientation].set_shape(
                    svg_str_to_pixbuf(svg.palette(w, h)))
            '''

    def _horizontal_layout(self, x, y, blocks):
        ''' Position prototypes in a horizontal palette. '''
        offset = self._turtle_window.toolbar_offset
        max_w = 0

        for blk in blocks:
            if not blk.get_visibility():
                continue

            w, h = get_stack_width_and_height(blk)
            if y + h > PALETTE_HEIGHT + offset:
                x += int(max_w + 3)
                y = offset + 3
                max_w = 0

            (bx, by) = blk.spr.get_xy()
            dx = x - bx
            dy = y - by
            for g in find_group(blk):
                g.spr.move_relative((int(dx), int(dy)))
                g.spr.save_xy = g.spr.get_xy()
                self._float_palette(g.spr)
            y += int(h + 3)
            if w > max_w:
                max_w = w

        return x, y, max_w

    def _vertical_layout(self, x, y, blocks):
        ''' Position prototypes in a vertical palette. '''
        row = []
        row_w = 0
        max_h = 0

        for blk in blocks:
            if not blk.get_visibility():
                continue

            w, h = get_stack_width_and_height(blk)
            if x + w > PALETTE_WIDTH:
                # Recenter row.
                dx = int((PALETTE_WIDTH - row_w) / 2)
                for r in row:
                    for g in find_group(r):
                        g.spr.move_relative((dx, 0))
                        g.spr.save_xy = (g.spr.save_xy[0] + dx,
                                         g.spr.save_xy[1])
                row = []
                row_w = 0
                x = 4
                y += int(max_h + 3)
                max_h = 0

            row.append(blk)
            row_w += (4 + w)

            (bx, by) = blk.spr.get_xy()
            dx = int(x - bx)
            dy = int(y - by)
            for g in find_group(blk):
                g.spr.move_relative((dx, dy))
                g.spr.save_xy = g.spr.get_xy()
                self._float_palette(g.spr)

            x += int(w + 4)
            if h > max_h:
                max_h = h

        # Recenter last row.
        dx = int((PALETTE_WIDTH - row_w) / 2)
        for r in row:
            for g in find_group(r):
                g.spr.move_relative((dx, 0))
                g.spr.save_xy = (g.spr.save_xy[0] + dx, g.spr.save_xy[1])

        return x, y, max_h

    def _hide_palette_shift_buttons(self):
        buttons = self._turtle_window.palette_button
        for i in range(4):
            buttons[i + 3].hide()

    def display_palette_shift_buttons(self):
        ''' Palettes too wide (or tall) for the screen get a shift button. '''
        self._hide_palette_shift_buttons()

        buttons = self._turtle_window.palette_button
        orientation = self._turtle_window.orientation

        if self.backgrounds[orientation].type == 'category-shift-horizontal':
            buttons[3].set_layer(CATEGORY_LAYER)
        elif self.backgrounds[orientation].type == 'category-shift-vertical':
            buttons[4].set_layer(CATEGORY_LAYER)
