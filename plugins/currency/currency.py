# -*- coding: utf-8 -*-
#Copyright (c) 2011-13, Walter Bender
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

import gtk
from time import time
import os.path
from gettext import gettext as _

try:
    from sugar.datastore import datastore
except ImportError:
    pass

from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette
from TurtleArt.taconstants import (MEDIA_SHAPES, NO_IMPORT, SKIN_PATHS,
                                   EXPAND_SKIN, BLOCKS_WITH_SKIN, CONSTANTS)
from TurtleArt.taprimitive import (ConstantArg, Primitive)
from TurtleArt.tatype import TYPE_NUMBER

class Currency(Plugin):
    """ a class for defining palette of money """

    def __init__(self, parent):
        self.tw = parent

    def setup(self):
        self.title_height = int((self.tw.canvas.height / 20) * self.tw.scale)

        SKIN_PATHS.append('plugins/currency/images')

        self._currency_palette()

    def _currency_palette(self):
        palette = make_palette(
            'currency', colors=["#FFFFFF", "#A0A0A0"],
            help_string=_('Palette of Australian currencies'),
            translation=_('currency'))

        self._make_constant(palette, '5 cents', 0.05, expand=(0, 10))
        self._make_constant(palette, '10 cents', 0.1, expand=(0, 10))
        self._make_constant(palette, '20 cents', 0.2, expand=(0, 10))
        self._make_constant(palette, '50 cents', 0.5, expand=(0, 10))
        self._make_constant(palette, '1 dollar', 1, expand=(0, 10))
        self._make_constant(palette, '2 dollars', 2, expand=(0, 10))

        self._make_constant(palette, '5 dollars', 5, expand=(60, 20))
        self._make_constant(palette, '10 dollars', 10, expand=(60, 20))
        self._make_constant(palette, '20 dollars', 20, expand=(60, 20))
        self._make_constant(palette, '50 dollars', 50, expand=(60, 20))
        self._make_constant(palette, '100 dollars', 100, expand=(60, 20))

    def _make_constant(self, palette, block_name, constant, expand=(0, 0)):
        """ Factory for constant blocks """
        CONSTANTS[block_name] = constant
        palette.add_block(block_name,
                          style='box-style-media',
                          label='',
                          default=constant,
                          prim_name=block_name,
                          help_string=_(str(constant)))
        BLOCKS_WITH_SKIN.append(block_name)
        NO_IMPORT.append(block_name)
        MEDIA_SHAPES.append(block_name + 'off')
        MEDIA_SHAPES.append(block_name + 'small')
        if expand > 0:
            EXPAND_SKIN[block_name] = expand
        self.tw.lc.def_prim(block_name, 0,
                            Primitive(CONSTANTS.get,
                                      return_type=TYPE_NUMBER,
                                      arg_descs=[ConstantArg(block_name)]))

