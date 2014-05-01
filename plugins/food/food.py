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

import gtk
from time import time
import os.path
from gettext import gettext as _

try:
    from sugar.datastore import datastore
except ImportError:
    pass

from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette, define_logo_function
from TurtleArt.talogo import logoerror
from TurtleArt.taconstants import (MEDIA_SHAPES, NO_IMPORT, SKIN_PATHS,
                                   EXPAND_SKIN, BLOCKS_WITH_SKIN, CONSTANTS,
                                   Vector)
from TurtleArt.taprimitive import (ArgSlot, ConstantArg, Primitive)
from TurtleArt.tatype import TYPE_NUMBER, TYPE_VECTOR, TYPE_STRING, TYPE_OBJECT

CALORIES = 0
PROTEIN = 1
CARBOHYDRATE = 2
FIBER = 3
FAT = 4


class Food(Plugin):
    """ a class for defining palette of food and nutrition """

    def __init__(self, parent):
        self.tw = parent
        self.calories = 0
        self.protein = 0
        self.carbohydrate = 0
        self.fiber = 0
        self.fat = 0

    def clear(self):
        self._prim_digest()

    def setup(self):
        SKIN_PATHS.append('plugins/food/images')

        self._eat_palette()
        self._food_palette()

    def _eat_palette(self):
        palette = make_palette('eatme',
                               colors=["#FFFFFF", "#A0A0A0"],
                               help_string=_('Palette of nutrition'))

        palette.add_block('get_calories',
                          style='number-style-1arg',
                          label=_('get calories'),
                          prim_name='get_calories',
                          help_string=_('extract caloric content of food'))
        self.tw.lc.def_prim(
            'get_calories', 1,
            Primitive(self._prim_nutriant,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      kwarg_descs={'nutriant': CALORIES},
                      return_type=TYPE_NUMBER))

        palette.add_block('get_protein',
                          style='number-style-1arg',
                          label=_('get protein'),
                          prim_name='get_protein',
                          help_string=_('extract protein content of food'))
        self.tw.lc.def_prim('get_protein', 1,
            Primitive(self._prim_nutriant,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      kwarg_descs={'nutriant': PROTEIN},
                      return_type=TYPE_NUMBER))

        palette.add_block('get_carbohydrate',
                          style='number-style-1arg',
                          label=_('get carbohydrates'),
                          prim_name='get_carbohydrate',
                          help_string=_('extract carbohydrate content of food'))
        self.tw.lc.def_prim('get_carbohydrate', 1,
            Primitive(self._prim_nutriant,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      kwarg_descs={'nutriant': CARBOHYDRATE},
                      return_type=TYPE_NUMBER))

        palette.add_block('calories',
                          style='box-style',
                          label=_('calories eaten'),
                          help_string=\
                              _('stored caloric content of food eaten'),
                          prim_name='calories',
                          value_block=True)
        self.tw.lc.def_prim('calories', 0,
                            Primitive(self._prim_get_calories,
                                      return_type=TYPE_NUMBER))
        palette.add_block('protein',
                          style='box-style',
                          label=_('protein eaten'),
                          help_string=\
                              _('stored protein content of food eaten'),
                          prim_name='protein',
                          value_block=True)
        self.tw.lc.def_prim('protein', 0,
                            Primitive(self._prim_get_protein,
                                      return_type=TYPE_NUMBER))

        palette.add_block('carbohydrate',
                          style='box-style',
                          label=_('carbohydrates eaten'),
                          help_string=\
                              _('stored carbohydrate content of food eaten'),
                          prim_name='carbohydrate',
                          value_block=True)
        self.tw.lc.def_prim('carbohydrate', 0,
                            Primitive(self._prim_get_carbohydrate,
                                      return_type=TYPE_NUMBER))

        palette.add_block('get_fiber',
                          style='number-style-1arg',
                          label=_('get fiber'),
                          prim_name='get_fiber',
                          help_string=_('extract fiber content of food'))
        self.tw.lc.def_prim('get_fiber', 1,
            Primitive(self._prim_nutriant,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      kwarg_descs={'nutriant': FIBER},
                      return_type=TYPE_NUMBER))

        palette.add_block('get_fat',
                          style='number-style-1arg',
                          label=_('get fat'),
                          prim_name='get_fat',
                          help_string=_('extract fat content of food'))
        self.tw.lc.def_prim('get_fat', 1,
            Primitive(self._prim_nutriant,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      kwarg_descs={'nutriant': FAT},
                      return_type=TYPE_NUMBER))

        palette.add_block('eat',
                          style='basic-style-1arg',
                          label=_('eat'),
                          prim_name='eat',
                          help_string=_('eat food and store its nutritional value'))
        self.tw.lc.def_prim('eat', 1,
                            Primitive(self._prim_eat,
                                      arg_descs=[ArgSlot(TYPE_VECTOR)]))
        
        palette.add_block('fiber',
                          style='box-style',
                          label=_('fiber eaten'),
                          help_string=\
                              _('stored fiber content of food eaten'),
                          prim_name='fiber',
                          value_block=True)
        self.tw.lc.def_prim('fiber', 0,
                            Primitive(self._prim_get_fiber,
                                      return_type=TYPE_NUMBER))

        palette.add_block('fat',
                          style='box-style',
                          label=_('fat eaten'),
                          help_string=\
                              _('stored fat content of food eaten'),
                          prim_name='fat',
                          value_block=True)
        self.tw.lc.def_prim('fat', 0,
                            Primitive(self._prim_get_fat,
                                      return_type=TYPE_NUMBER))

        palette.add_block('digest',
                          style='basic-style-extended-vertical',
                          label=_('digest meal'),
                          prim_name='digest',
                          help_string=_('digest food eaten and zero out stored nutritional values'))
        self.tw.lc.def_prim('digest', 0,
                            Primitive(self._prim_digest))

        palette.add_block('get_name',
                          style='number-style-1arg',
                          label=_('get name'),
                          prim_name='get_name',
                          help_string=_('get name of food'))
        self.tw.lc.def_prim('get_name', 1,
            Primitive(self._prim_name,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      return_type=TYPE_STRING))

    def _food_palette(self):
        palette = make_palette('food',
                               colors=["#FFFFFF", "#A0A0A0"],
                               help_string=_('Palette of foods'))

        # nutrients: [cals, protein, carbs, fiber, fat]
        # each food requires two svg files in images/
        # e.g., appleoff.svg and applesmall.svg
        self._make_polynominal(palette, 'apple', _('apple'), [72, 0, 19, 3, 0],
                               expand=(15, 15))
        self._make_polynominal(palette, 'banana', _('banana'),
                               [105, 1, 27, 3, 0], expand=(40, 15))
        self._make_polynominal(palette, 'Orange', _('orange'),
                               [62, 1, 15, 3, 0], expand=(15, 15))
        self._make_polynominal(palette, 'cake', _('chocolate cake'),
                               [387, 4, 69, 2, 13], expand=(20, 15))
        self._make_polynominal(palette, 'cookie', _('chocolate chip cookie'),
                               [68, 1, 8, 0, 4], expand=(15, 15))
        self._make_polynominal(palette, 'bread', _('wheat bread'),
                               [69, 4, 12, 2, 1], expand=(15, 15))
        self._make_polynominal(palette, 'corn', _('corn'), [96, 3, 21, 3, 1],
                               expand=(40, 15))
        self._make_polynominal(palette, 'potato', _('potato'),
                               [159, 4, 36, 4, 0], expand=(15, 15))
        self._make_polynominal(palette, 'sweetpotato', _('sweet potato'),
                               [169, 1, 22, 1, 8], expand=(40, 15))
        self._make_polynominal(palette, 'tomato', _('tomato'),
                               [150, 4, 25, 3, 5], expand=(15, 15))

    def _make_polynominal(self, palette, block_name, i18n_name, polynominal,
                          expand=(0, 0)):
        """ Factory for polynominal blocks """
        CONSTANTS[block_name] = Vector(i18n_name, polynominal)
        palette.add_block(block_name,
                          style='box-style-media',
                          label='',
                          default=None,
                          prim_name=block_name,
                          # TRANS: g is grams, e.g., 3g of fat
                          help_string=_('%(blockname)s: %(no_cal)d %(cal)s\
 (%(no_prot)dg of %(prot)s, %(no_carb)dg of %(carb)s,\
 %(no_fib)dg of %(fib)s, %(no_fat)dg of %(fat)s)') % {
                'blockname': i18n_name, 'no_cal': polynominal[0],
                'cal': _('calories'), 'no_prot': polynominal[1],
                'prot': _('protein'), 'no_carb': polynominal[2],
                'carb': _('carbohydrates'), 'no_fib': polynominal[3],
                'fib': _('fiber'), 'no_fat': polynominal[4],'fat': _('fat')})
        BLOCKS_WITH_SKIN.append(block_name)
        NO_IMPORT.append(block_name)
        MEDIA_SHAPES.append(block_name + 'off')
        MEDIA_SHAPES.append(block_name + 'small')
        if expand > 0:
            EXPAND_SKIN[block_name] = expand
        self.tw.lc.def_prim(block_name, 0,
                            Primitive(CONSTANTS.get,
                                      return_type=TYPE_VECTOR,
                                      arg_descs=[ConstantArg(block_name)]))

    def _prim_digest(self):
        ''' Digest nutrients (i.e., clear) '''
        self.calories = 0
        self.protein = 0
        self.carbohydrate = 0
        self.fiber = 0
        self.fat = 0

    def _prim_eat(self, food):
        if type(food) == Vector:
            self.calories += food.vector[CALORIES]
            self.protein += food.vector[PROTEIN]
            self.carbohydrate += food.vector[CARBOHYDRATE]
            self.fiber += food.vector[FIBER]
            self.fat += food.vector[FAT]
        else:
            raise logoerror("#syntaxerror")

    def _prim_nutriant(self, x, nutriant=0):
        print x
        print type(x)
        if type(x) == Vector:
            return x.vector[nutriant]
        else:
            raise logoerror("#syntaxerror")

    def _prim_name(self, x):
        if type(x) == Vector:
            return x.name
        else:
            raise logoerror("#syntaxerror")

    def _prim_get_calories(self):
        return self.calories

    def _prim_get_carbohydrate(self):
        return self.carbohydrate

    def _prim_get_fat(self):
        return self.fat

    def _prim_get_fiber(self):
        return self.fiber

    def _prim_get_protein(self):
        return self.protein
