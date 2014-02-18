# -*- coding: utf-8 -*-
#Copyright (c) 2012, Walter Bender
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

from gettext import gettext as _

from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette
from TurtleArt.taprimitive import (ArgSlot, ConstantArg, Primitive)
from TurtleArt.tatype import (TYPE_FLOAT, TYPE_NUMBER)
from TurtleArt.taturtle import Turtle


class Threed(Plugin):
    """ a class for defining the 3-D Turtle Blocks """

    def __init__(self, turtle_window):
        Plugin.__init__(self)
        self.tw = turtle_window

    def setup(self):
        self._turtle_palette()

    def _turtle_palette(self):
        palette = make_palette('turtle',
                               colors=["#00FF00", "#00A000"],
                               help_string=_('Palette of turtle commands'),
                               translation=_('turtle'))

        palette.add_block('zcor',
                          style='box-style',
                          label=_('zcor'),
                          help_string=_(
                              'holds current z-coordinate value of the turtle '
                              '(can be used in place of a number block)'),
                          value_block=True,
                          prim_name='zcor')
        self.tw.lc.def_prim(
            'zcor', 0,
            Primitive(Primitive.divide, return_type=TYPE_FLOAT,
                      arg_descs=[ConstantArg(Primitive(Turtle.get_z)),
                                 ConstantArg(Primitive(
                                     self.tw.get_coord_scale))]))

        palette.add_block('setxyz',
                          style='basic-style-3arg',
                          # TRANS: xyz are coordinates in a 3-dimensional space
                          label=[_('set xyz') + '\n\n',
                                 _('x'), _('y'), _('z')],
                          prim_name='setxyz',
                          default=[0, 0, 0],
                          help_string=_('sets the xyz-coordinates of the '
                                        'turtle'))
        self.tw.lc.def_prim(
            'setxyz', 3,
            Primitive(Turtle.set_xyz,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER),
                                 ArgSlot(TYPE_NUMBER)],
                      call_afterwards=self.after_move))

    def after_move(self, *ignored_args, **ignored_kwargs):
        ''' Update labels after moving the turtle '''
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value(
                'xcor',
                self.tw.turtles.get_active_turtle().get_xy()[0] /
                self.tw.coord_scale)
            self.tw.lc.update_label_value(
                'ycor',
                self.tw.turtles.get_active_turtle().get_xy()[1] /
                self.tw.coord_scale)
            self.tw.lc.update_label_value(
                'zcor',
                self.tw.turtles.get_active_turtle().get_xyz()[2] /
                self.tw.coord_scale)
