# -*- coding: utf-8 -*-
# Copyright (c) 2012, Walter Bender
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

import os
import tempfile
from time import time
from gettext import gettext as _

from plugins.plugin import Plugin
from TurtleArt.tapalette import (make_palette, define_logo_function)
from TurtleArt.talogo import (primitive_dictionary, logoerror)
from TurtleArt.taconstants import (CONSTANTS, MACROS, KEY_DICT, MEDIA_SHAPES,
                                   REVERSE_KEY_DICT, SKIN_PATHS,
                                   BLOCKS_WITH_SKIN, PYTHON_SKIN,
                                   MEDIA_BLOCK2TYPE, VOICES)
from TurtleArt.tautils import (debug_output, get_path, data_to_string,
                               hat_on_top, listify, data_from_file,
                               get_endswith_files)
from TurtleArt.taprimitive import (ArgSlot, ConstantArg, Primitive)
from TurtleArt.tatype import (TYPE_BOOL, TYPE_BOX, TYPE_CHAR, TYPE_INT,
                              TYPE_FLOAT, TYPE_OBJECT, TYPE_STRING,
                              TYPE_NUMBER)
from TurtleArt.taturtle import Turtle


class Turtle_blocks_extras(Plugin):
    """ a class for defining the extra palettes that distinguish Turtle Blocks
    from Turtle Art """

    def __init__(self, turtle_window):
        Plugin.__init__(self)
        self.tw = turtle_window

    def setup(self):
        SKIN_PATHS.append('plugins/turtle_blocks_extras/images')

        self.heap = self.tw.lc.heap
        self.title_height = int((self.tw.canvas.height / 20) * self.tw.scale)

        # set up Turtle Block palettes
        self._flow_palette()

        self._sensor_palette()

        self._media_palette()

        self._extras_palette()

        self._portfolio_palette()

        self._myblocks_palette()

    # Palette definitions

    def _flow_palette(self):
        palette = make_palette('flow',
                               colors=["#FFC000", "#A08000"],
                               help_string=_('Palette of flow operators'))

        palette.add_block('while',
                          style='clamp-style-boolean',
                          label=_('while'),
                          prim_name='while',
                          default=[None, None],
                          special_name=_('while'),
                          help_string=_('do-while-True operator that uses \
boolean operators from Numbers palette'))
        self.tw.lc.def_prim(
            'while', 2,
            Primitive(self.tw.lc.prim_loop,
                      arg_descs=[
                          ArgSlot(TYPE_OBJECT,
                                  call_arg=False,
                                  wrapper=Primitive(
                                      Primitive.controller_while,
                                      arg_descs=[ArgSlot(TYPE_BOOL,
                                                         call_arg=False)])),
                          ArgSlot(TYPE_OBJECT)]),
            True)

        palette.add_block('until',
                          style='clamp-style-until',
                          label=_('until'),
                          prim_name='until',
                          default=[None, None],
                          special_name=_('until'),
                          help_string=_('do-until-True operator that uses \
boolean operators from Numbers palette'))
        self.tw.lc.def_prim(
            'until', 2,
            Primitive(self.tw.lc.prim_loop,
                      arg_descs=[
                          ArgSlot(TYPE_OBJECT,
                                  call_arg=False,
                                  # TODO can we use controller_while in
                                  # combination with not_?
                                  wrapper=Primitive(
                                      Primitive.controller_until,
                                      arg_descs=[ArgSlot(TYPE_BOOL,
                                                         call_arg=False)])),
                          ArgSlot(TYPE_OBJECT)]),
            True)

        palette.add_block('sandwichclamp',
                          style='clamp-style-collapsible',
                          label=' ',
                          special_name=_('top'),
                          prim_name='clamp',
                          help_string=_('top of a collapsible stack'))
        self.tw.lc.def_prim('clamp', 1,
                            Primitive(self.tw.lc.prim_clamp,
                                      arg_descs=[ArgSlot(TYPE_OBJECT)]),
                            True)

    def _media_palette(self):

        palette = make_palette('media',
                               colors=["#A0FF00", "#80A000"],
                               help_string=_('Palette of media objects'),
                               position=7,
                               translation=_('media'))

        palette.add_block('journal',
                          style='box-style-media',
                          label=' ',
                          default='None',
                          special_name=_('journal'),
                          help_string=_('Sugar Journal media object'))
        MEDIA_BLOCK2TYPE['journal'] = 'media'
        BLOCKS_WITH_SKIN.append('journal')
        MEDIA_SHAPES.append('journalsmall')
        MEDIA_SHAPES.append('journaloff')
        MEDIA_SHAPES.append('journalon')

        palette.add_block('audio',
                          hidden=True,
                          style='box-style-media',
                          label=' ',
                          special_name=_('audio'),
                          default='None',
                          help_string=_('Sugar Journal audio object'))
        BLOCKS_WITH_SKIN.append('audio')
        MEDIA_BLOCK2TYPE['audio'] = 'audio'
        MEDIA_SHAPES.append('audiosmall')
        MEDIA_SHAPES.append('audiooff')
        MEDIA_SHAPES.append('audioon')

        palette.add_block('video',
                          hidden=True,
                          style='box-style-media',
                          label=' ',
                          special_name=_('video'),
                          default='None',
                          help_string=_('Sugar Journal video object'))
        BLOCKS_WITH_SKIN.append('video')
        MEDIA_BLOCK2TYPE['video'] = 'video'
        MEDIA_SHAPES.append('videosmall')
        MEDIA_SHAPES.append('videooff')
        MEDIA_SHAPES.append('videoon')

        palette.add_block('description',
                          hidden=True,
                          style='box-style-media',
                          label=' ',
                          special_name=_('description'),
                          default='None',
                          help_string=_('Sugar Journal description field'))
        BLOCKS_WITH_SKIN.append('description')
        MEDIA_BLOCK2TYPE['description'] = 'descr'
        MEDIA_SHAPES.append('descriptionsmall')
        MEDIA_SHAPES.append('descriptionoff')
        MEDIA_SHAPES.append('descriptionon')

        palette.add_block('string',
                          style='box-style',
                          label=_('text'),
                          default=_('text'),
                          special_name=_('text'),
                          help_string=_('string value'))

        palette.add_block('show',
                          style='basic-style-1arg',
                          label=_('show'),
                          default=_('text'),
                          prim_name='show',
                          logo_command='label',
                          help_string=_('draws text or show media from the \
Journal'))
        self.tw.lc.def_prim('show', 1,
                            Primitive(self.tw.lc.show,
                                      arg_descs=[ArgSlot(TYPE_OBJECT),
                                                 ConstantArg(True)]))

        palette.add_block('showaligned',
                          hidden=True,
                          colors=["#A0FF00", "#80A000"],
                          style='basic-style-1arg',
                          label=_('show aligned'),
                          default=_('text'),
                          prim_name='showaligned',
                          logo_command='label',
                          help_string=_('draws text or show media from the \
Journal'))
        self.tw.lc.def_prim('showaligned', 1,
                            Primitive(self.tw.lc.show,
                                      arg_descs=[ArgSlot(TYPE_OBJECT),
                                                 ConstantArg(False)]))

        palette.add_block('setscale',
                          style='basic-style-1arg',
                          label=_('set scale'),
                          prim_name='setscale',
                          default=33,
                          logo_command='setlabelheight',
                          help_string=_('sets the scale of media'))
        self.tw.lc.def_prim(
            'setscale', 1,
            Primitive(self.tw.lc.set_scale,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      call_afterwards=lambda value: self.after_set(
                          'scale', value)))

        palette.add_block(
            'setfont',
            style='basic-style-1arg',
            label=_('set font'),
            prim_name='setfont',
            default='Sans',
            help_string=_('sets the font used by the show block'))
        self.tw.lc.def_prim('setfont', 1,
                            Primitive(self.tw.canvas.set_font,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('savepix',
                          style='basic-style-1arg',
                          label=_('save picture'),
                          prim_name='savepix',
                          default=_('picture name'),
                          help_string=_('saves a picture to the Sugar \
Journal'))
        self.tw.lc.def_prim('savepix', 1,
                            Primitive(self.tw.save_as_image,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('savesvg',
                          style='basic-style-1arg',
                          label=_('save SVG'),
                          prim_name='savesvg',
                          default=_('picture name'),
                          help_string=_('saves turtle graphics as an SVG file \
in the Sugar Journal'))
        self.tw.lc.def_prim('savesvg', 1,
                            Primitive(self.tw.save_as_image,
                                      arg_descs=[ArgSlot(TYPE_STRING)],
                                      kwarg_descs={'svg': ConstantArg(True)}))

        palette.add_block('scale',
                          style='box-style',
                          label=_('scale'),
                          prim_name='scale',
                          value_block=True,
                          logo_command='labelsize',
                          help_string=_('holds current scale value'))
        self.tw.lc.def_prim('scale', 0,
                            Primitive(self.tw.lc.get_scale,
                                      return_type=TYPE_NUMBER))

        palette.add_block('mediawait',
                          style='basic-style-extended-vertical',
                          label=_('media wait'),
                          prim_name='mediawait',
                          help_string=_('wait for current video or audio to \
complete'))
        self.tw.lc.def_prim('mediawait', 0, self.tw.lc.media_wait, True)

        palette.add_block('mediastop',
                          style='basic-style-extended-vertical',
                          label=_('media stop'),
                          prim_name='mediastop',
                          help_string=_('stop video or audio'))
        self.tw.lc.def_prim('mediastop', 0, self.tw.lc.media_stop, True)

        palette.add_block('mediapause',
                          style='basic-style-extended-vertical',
                          label=_('media pause'),
                          prim_name='mediapause',
                          help_string=_('pause video or audio'))
        self.tw.lc.def_prim('mediapause', 0, self.tw.lc.media_pause, True)

        palette.add_block('mediaplay',
                          style='basic-style-extended-vertical',
                          label=_('media resume'),
                          prim_name='mediaplay',
                          help_string=_('resume playing video or audio'))
        self.tw.lc.def_prim('mediaplay', 0, self.tw.lc.media_play, True)

        palette.add_block('speak',
                          style='basic-style-1arg',
                          label=_('speak'),
                          prim_name='speak',
                          default=_('hello'),
                          help_string=_('speaks text'))
        self.tw.lc.def_prim('speak', 1,
                            Primitive(self.prim_speak,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('sinewave',
                          style='basic-style-3arg',
                          # TRANS: pitch, duration, amplitude
                          label=[_('sinewave') + '\n\n', _('pitch'),
                                 _('amplitude'), _('duration')],
                          prim_name='sinewave',
                          default=[1000, 5000, 1],
                          help_string=_('plays a sinewave at frequency, \
amplitude, and duration (in seconds)'))
        self.tw.lc.def_prim('sinewave', 3,
                            Primitive(self.prim_sinewave,
                                      arg_descs=[ArgSlot(TYPE_NUMBER),
                                                 ArgSlot(TYPE_NUMBER),
                                                 ArgSlot(TYPE_NUMBER)]))

    def _sensor_palette(self):

        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'),
                               position=6,
                               translation=_('sensor'))

        palette.add_block('mousebutton',
                          hidden=True,
                          style='box-style',
                          label=_('button down'),
                          prim_name='mousebutton',
                          value_block=True,
                          help_string=_('returns 1 if mouse button is \
pressed'))
        self.tw.lc.def_prim('mousebutton', 0,
                            Primitive(self.tw.get_mouse_flag,
                                      return_type=TYPE_NUMBER))

        palette.add_block('mousebutton2',
                          style='boolean-block-style',
                          label=_('button down'),
                          prim_name='mousebutton2',
                          value_block=True,
                          help_string=_('returns True if mouse button is \
pressed'))
        self.tw.lc.def_prim('mousebutton2', 0,
                            Primitive(self.tw.get_mouse_button,
                                      return_type=TYPE_BOOL))

        palette.add_block('mousex',
                          style='box-style',
                          label=_('mouse x'),
                          prim_name='mousex',
                          value_block=True,
                          help_string=_('returns mouse x coordinate'))
        self.tw.lc.def_prim('mousex', 0,
                            Primitive(self.tw.get_mouse_x,
                                      return_type=TYPE_NUMBER,
                                      call_afterwards=self.after_mouse_x))

        palette.add_block('mousey',
                          style='box-style',
                          label=_('mouse y'),
                          prim_name='mousey',
                          value_block=True,
                          help_string=_('returns mouse y coordinate'))
        self.tw.lc.def_prim('mousey', 0,
                            Primitive(self.tw.get_mouse_y,
                                      return_type=TYPE_NUMBER,
                                      call_afterwards=self.after_mouse_y))

        palette.add_block('kbinput',
                          style='basic-style-extended-vertical',
                          label=_('query keyboard'),
                          prim_name='kbinput',
                          help_string=_('query for keyboard input (results \
stored in keyboard block)'))
        self.tw.lc.def_prim('kbinput', 0,
                            Primitive(self.tw.get_keyboard_input,
                                      call_afterwards=self.after_keypress))

        palette.add_block('keyboard',
                          style='box-style',
                          label=_('keyboard'),
                          prim_name='keyboard',
                          value_block=True,
                          logo_command='make "keyboard readchar',
                          help_string=_('holds results of query-keyboard \
block as ASCII'))
        self.tw.lc.def_prim('keyboard', 0,
                            Primitive(self.tw.get_keyboard,
                                      return_type=TYPE_NUMBER))

        palette.add_block('readpixel',
                          style='basic-style-extended-vertical',
                          label=_('read pixel'),
                          prim_name='readpixel',
                          logo_command=':keyboard',
                          help_string=_('RGB color under the turtle is pushed \
to the stack'))
        self.tw.lc.def_prim('readpixel', 0,
                            Primitive(Turtle.read_pixel))

        palette.add_block('see',
                          style='box-style',
                          label=_('turtle sees'),
                          value_block=True,
                          prim_name='see',
                          help_string=_('returns the color that the turtle \
"sees"'))
        self.tw.lc.def_prim('see', 0,
                            Primitive(Turtle.get_color_index,
                                      return_type=TYPE_NUMBER,
                                      call_afterwards=self.after_see))

        palette.add_block('time',
                          style='box-style',
                          label=_('time'),
                          prim_name='time',
                          value_block=True,
                          help_string=_('elapsed time (in seconds) since \
program started'))
        self.tw.lc.def_prim(
            'time', 0,
            Primitive(
                Primitive.identity,
                return_type=TYPE_INT,
                arg_descs=[
                    ConstantArg(
                        Primitive(
                            int,
                            arg_descs=[ConstantArg(
                                Primitive(Primitive.minus,
                                          arg_descs=[
                                              ConstantArg(Primitive(time)),
                                              ConstantArg(Primitive(
                                                  self.tw.lc.get_start_time))])
                            )]
                        ))],
                call_afterwards=self.after_time))

    def _extras_palette(self):

        palette = make_palette('extras',
                               colors=["#FF0000", "#A00000"],
                               help_string=_('Palette of extra options'),
                               position=8,
                               translation=_('extras'))

        palette.add_block('push',
                          style='basic-style-1arg',
                          # TRANS: push adds a new item to the program stack
                          label=_('push'),
                          prim_name='push',
                          logo_command='tapush',
                          help_string=_('pushes value onto FILO (first-in \
last-out heap)'))
        self.tw.lc.def_prim(
            'push', 1,
            Primitive(self.tw.lc.append_heap,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      call_afterwards=self.after_push))
        define_logo_function('tapush', 'to tapush :foo\nmake "taheap fput \
:foo :taheap\nend\nmake "taheap []\n')

        palette.add_block('printheap',
                          style='basic-style-extended-vertical',
                          label=_('show heap'),
                          prim_name='printheap',
                          logo_command='taprintheap',
                          help_string=_('shows values in FILO (first-in \
last-out heap)'))
        self.tw.lc.def_prim(
            'printheap', 0,
            Primitive(self.tw.print_,
                      arg_descs=[ConstantArg(Primitive(self.tw.lc.get_heap)),
                                 ConstantArg(False)]))
        define_logo_function('taprintheap', 'to taprintheap \nprint :taheap\n\
end\n')

        palette.add_block('clearheap',
                          style='basic-style-extended-vertical',
                          label=_('empty heap'),
                          prim_name='clearheap',
                          logo_command='taclearheap',
                          help_string=_('emptys FILO (first-in-last-out \
heap)'))
        self.tw.lc.def_prim(
            'clearheap', 0,
            Primitive(self.tw.lc.reset_heap, call_afterwards=self.after_pop))
        define_logo_function('taclearheap', 'to taclearheap\nmake "taheap []\n\
end\n')

        palette.add_block('pop',
                          style='box-style',
                          # TRANS: pop removes a new item from the program
                          # stack
                          label=_('pop'),
                          prim_name='pop',
                          value_block=True,
                          logo_command='tapop',
                          help_string=_('pops value off FILO (first-in \
last-out heap)'))
        self.tw.lc.def_prim(
            'pop', 0,
            Primitive(self.tw.lc.pop_heap, return_type=TYPE_BOX,
                      call_afterwards=self.after_pop))
        define_logo_function('tapop', 'to tapop\nif emptyp :taheap [stop]\n\
make "tmp first :taheap\nmake "taheap butfirst :taheap\noutput :tmp\nend\n')

        palette.add_block('isheapempty',
                          hidden=True,
                          style='box-style',
                          label=_('empty heap?'),
                          prim_name='isheapempty',
                          value_block=True,
                          help_string=_('returns True if heap is empty'))
        self.tw.lc.def_prim(
            'isheapempty', 0,
            Primitive(int, return_type=TYPE_INT,
                      arg_descs=[ConstantArg(
                          Primitive(Primitive.not_, return_type=TYPE_BOOL,
                                    arg_descs=[ConstantArg(
                                        Primitive(self.tw.lc.get_heap,
                                                  return_type=TYPE_BOOL))]))]))

        palette.add_block('saveheap',
                          style='basic-style-1arg',
                          label=_('save heap to file'),
                          default=_('filename'),
                          prim_name='saveheap',
                          help_string=_('saves FILO (first-in \
last-out heap) to a file'))

        self.tw.lc.def_prim('saveheap', 1,
                            Primitive(self.tw.lc.save_heap,
                                      arg_descs=[ArgSlot(TYPE_OBJECT)]))

        if self.tw.running_sugar:
            palette.add_block('loadheap',
                              style='basic-style-1arg',
                              hidden=True,
                              label=_('load heap from file'),
                              default=_('filename'),
                              prim_name='loadheap',
                              help_string=_('loads FILO (first-in \
last-out heap) from a file'))
            # macro
            palette.add_block('loadheapfromjournal',
                              style='basic-style-1arg',
                              label=_('load heap from file'),
                              help_string=_('loads FILO (first-in \
last-out heap) from a file'))
        else:
            palette.add_block('loadheap',
                              style='basic-style-1arg',
                              label=_('load heap from file'),
                              default=_('filename'),
                              prim_name='loadheap',
                              help_string=_('loads FILO (first-in \
last-out heap) from a file'))

        self.tw.lc.def_prim('loadheap', 1,
                            Primitive(self.tw.lc.load_heap,
                                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                                      call_afterwards=self.after_push))

        palette.add_block('isheapempty2',
                          style='boolean-block-style',
                          label=_('empty heap?'),
                          prim_name='isheapempty2',
                          value_block=True,
                          help_string=_('returns True if heap is empty'))
        self.tw.lc.def_prim(
            'isheapempty2', 0,
            # Python automatically converts the heap to a boolean in contexts
            # where a boolean is needed
            Primitive(Primitive.not_, return_type=TYPE_BOOL,
                      arg_descs=[ConstantArg(
                          Primitive(self.tw.lc.get_heap,
                                    return_type=TYPE_BOOL))]))

        palette.add_block('comment',
                          style='basic-style-1arg',
                          label=_('comment'),
                          prim_name='comment',
                          default=_('comment'),
                          string_or_number=True,
                          help_string=_('places a comment in your code'))
        self.tw.lc.def_prim(
            'comment', 1,
            Primitive(Primitive.comment, arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('print',
                          style='basic-style-1arg',
                          label=_('print'),
                          prim_name='print',
                          logo_command='label',
                          string_or_number=True,
                          help_string=_('prints value in status block at \
bottom of the screen'))
        self.tw.lc.def_prim(
            'print', 1,
            Primitive(self.tw.print_,
                      arg_descs=[ArgSlot(TYPE_OBJECT), ConstantArg(False)]))

        palette.add_block('chr',
                          style='number-style-1arg',
                          label='chr',
                          prim_name='chr',
                          help_string=_('Python chr operator'))
        self.tw.lc.def_prim(
            'chr', 1,
            Primitive(chr, return_type=TYPE_CHAR,
                      arg_descs=[ArgSlot(TYPE_INT)]))

        palette.add_block('int',
                          style='number-style-1arg',
                          label='int',
                          prim_name='int',
                          help_string=_('Python int operator'))
        self.tw.lc.def_prim(
            'int', 1,
            # leave over the actual work to the type system, and just demand
            # that the argument be converted to an integer
            Primitive(Primitive.identity, return_type=TYPE_INT,
                      arg_descs=[ArgSlot(TYPE_INT)]))

        palette.add_block('polar',
                          style='basic-style-extended-vertical',
                          label=_('polar'),
                          prim_name='polar',
                          help_string=_('displays polar coordinates'))
        self.tw.lc.def_prim('polar', 0,
                            lambda self: self.tw.set_polar(True))

        palette.add_block('myfunc1arg',
                          style='number-style-var-arg',
                          label=[_('Python'), 'f(x)', 'x'],
                          prim_name='myfunction',
                          default=['x', 100],
                          string_or_number=True,
                          help_string=_('a programmable block: used to add \
advanced single-variable math equations, e.g., sin(x)'))
        self.tw.lc.def_prim(
            'myfunction', 2,
            Primitive(self.tw.lc.prim_myfunction, return_type=TYPE_FLOAT,
                      arg_descs=[ArgSlot(TYPE_STRING), ArgSlot(TYPE_FLOAT)]))

        palette.add_block('myfunc2arg',
                          hidden=True,
                          colors=["#FF0000", "#A00000"],
                          style='number-style-var-arg',
                          label=[_('Python'), 'f(x,y)', ' '],
                          prim_name='myfunction2',
                          default=['x+y', 100, 100],
                          string_or_number=True,
                          help_string=_('a programmable block: used to add \
advanced multi-variable math equations, e.g., sqrt(x*x+y*y)'))
        self.tw.lc.def_prim(
            'myfunction2', 3,
            Primitive(self.tw.lc.prim_myfunction, return_type=TYPE_FLOAT,
                      arg_descs=[ArgSlot(TYPE_STRING), ArgSlot(TYPE_FLOAT),
                                 ArgSlot(TYPE_FLOAT)]))

        palette.add_block('myfunc3arg',
                          hidden=True,
                          colors=["#FF0000", "#A00000"],
                          style='number-style-var-arg',
                          label=[_('Python'), 'f(x,y,z)', ' '],
                          prim_name='myfunction3',
                          default=['x+y+z', 100, 100, 100],
                          string_or_number=True,
                          help_string=_('a programmable block: used to add \
advanced multi-variable math equations, e.g., sin(x+y+z)'))
        self.tw.lc.def_prim(
            'myfunction3', 4,
            Primitive(self.tw.lc.prim_myfunction, return_type=TYPE_FLOAT,
                      arg_descs=[ArgSlot(TYPE_STRING), ArgSlot(TYPE_FLOAT),
                                 ArgSlot(TYPE_FLOAT), ArgSlot(TYPE_FLOAT)]))

        palette.add_block('cartesian',
                          style='basic-style-extended-vertical',
                          label=_('Cartesian'),
                          prim_name='cartesian',
                          help_string=_('displays Cartesian coordinates'))
        self.tw.lc.def_prim('cartesian', 0,
                            lambda self: self.tw.set_cartesian(True))

        palette.add_block('userdefined',
                          style='basic-style-var-arg',
                          label=' ',
                          prim_name='userdefined',
                          string_or_number=True,
                          special_name=_('Python block'),
                          default=100,
                          help_string=_('runs code found in the tamyblock.py \
module found in the Journal'))
        self.tw.lc.def_prim('userdefined', 1,
                            Primitive(self.tw.lc.prim_myblock,
                                      arg_descs=[ArgSlot(TYPE_OBJECT)]))
        BLOCKS_WITH_SKIN.append('userdefined')
        PYTHON_SKIN.append('userdefined')

        palette.add_block('userdefined2args',
                          hidden=True,
                          colors=["#FF0000", "#A00000"],
                          style='basic-style-var-arg',
                          label=' ',
                          prim_name='userdefined2',
                          string_or_number=True,
                          special_name=_('Python block'),
                          default=[100, 100],
                          help_string=_('runs code found in the tamyblock.py \
module found in the Journal'))
        self.tw.lc.def_prim('userdefined2', 2,
                            Primitive(self.tw.lc.prim_myblock,
                                      arg_descs=[ArgSlot(TYPE_OBJECT),
                                                 ArgSlot(TYPE_OBJECT)]))
        BLOCKS_WITH_SKIN.append('userdefined2args')
        PYTHON_SKIN.append('userdefined2args')

        palette.add_block('userdefined3args',
                          hidden=True,
                          colors=["#FF0000", "#A00000"],
                          style='basic-style-var-arg',
                          label=' ',
                          prim_name='userdefined3',
                          special_name=_('Python block'),
                          default=[100, 100, 100],
                          string_or_number=True,
                          help_string=_('runs code found in the tamyblock.py \
module found in the Journal'))
        self.tw.lc.def_prim('userdefined3', 3,
                            Primitive(self.tw.lc.prim_myblock,
                                      arg_descs=[ArgSlot(TYPE_OBJECT),
                                                 ArgSlot(TYPE_OBJECT),
                                                 ArgSlot(TYPE_OBJECT)]))
        BLOCKS_WITH_SKIN.append('userdefined3args')
        PYTHON_SKIN.append('userdefined3args')
        MEDIA_SHAPES.append('pythonsmall')
        MEDIA_SHAPES.append('pythonoff')
        MEDIA_SHAPES.append('pythonon')

        palette.add_block('getfromurl',
                          style='number-style-1arg',
                          # TRANS: URL is universal resource locator
                          label=_('URL'),
                          default='http://wiki.sugarlabs.org/images/2/2c/Logo_alt_3.svg',
                          prim_name='getfromurl',
                          help_string=_(
                              'gets a text string or an image from a URL'))
        self.tw.lc.def_prim('getfromurl', 1,
                            Primitive(self.tw.lc.get_from_url,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('skin',
                          hidden=True,
                          colors=["#FF0000", "#A00000"],
                          style='basic-style-1arg',
                          label=_('turtle shell'),
                          prim_name='skin',
                          help_string=_("put a custom 'shell' on the turtle"))
        self.tw.lc.def_prim('skin', 1,
                            Primitive(self.tw.lc.reskin,
                                      arg_descs=[ArgSlot(TYPE_OBJECT)]))

        # macro
        palette.add_block('reskin',
                          style='basic-style-1arg',
                          label=_('turtle shell'),
                          help_string=_("put a custom 'shell' on the turtle"))

        palette.add_block('addturtle',
                          style='basic-style-1arg',
                          label=_('turtle'),
                          prim_name='addturtle',
                          default=1,
                          string_or_number=True,
                          help_string=_('chooses which turtle to command'))
        self.tw.lc.def_prim('addturtle', 1,
                            Primitive(self.tw.lc.prim_turtle,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('turtlex',
                          style='number-style-1arg',
                          label=_('turtle x'),
                          prim_name='turtlex',
                          default=['Yertle'],
                          help_string=_('Returns x coordinate of turtle'))
        self.tw.lc.def_prim(
            'turtlex', 1,
            Primitive(self.tw.turtles.get_turtle_x,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      return_type=TYPE_BOX))

        palette.add_block('turtley',
                          style='number-style-1arg',
                          label=_('turtle y'),
                          prim_name='turtley',
                          default=['Yertle'],
                          help_string=_('Returns y coordinate of turtle'))
        self.tw.lc.def_prim(
            'turtley', 1,
            Primitive(self.tw.turtles.get_turtle_y,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      return_type=TYPE_BOX))

        palette.add_block('activeturtle',
                          style='box-style',
                          label=_('active turtle'),
                          prim_name='activeturtle',
                          value_block=True,
                          help_string=_('the name of the active turtle'))
        self.tw.lc.def_prim(
            'activeturtle', 0,
            Primitive(Turtle.get_name,
                      return_type=TYPE_BOX))

        palette.add_block('turtleh',
                          style='number-style-1arg',
                          label=_('turtle heading'),
                          prim_name='turtleh',
                          default=['Yertle'],
                          help_string=_('Returns heading of turtle'))
        self.tw.lc.def_prim(
            'turtleh', 1,
            Primitive(self.tw.turtles.get_turtle_heading,
                      arg_descs=[ArgSlot(TYPE_OBJECT)],
                      return_type=TYPE_BOX))

        palette.add_block('sandwichclampcollapsed',
                          hidden=True,
                          style='clamp-style-collapsed',
                          label=_('click to open'),
                          prim_name='clamp',
                          special_name=_('top'),
                          help_string=_('top of a collapsed stack'))

        palette.add_block('loadpalette',
                          style='basic-style-1arg',
                          string_or_number=True,
                          label=_('select palette'),
                          prim_name='loadpalette',
                          default=_('turtle'),
                          help_string=_('selects a palette'))
        self.tw.lc.def_prim('loadpalette', 1,
                            Primitive(self.tw.prim_load_palette,
                                      export_me=False,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('loadblock',
                          style='basic-style-var-arg',
                          label=_('load'),
                          prim_name='loadblock',
                          default=_('forward'),
                          help_string=_('loads a block'))
        self.tw.lc.def_prim('loadblock', 1,
                            Primitive(self.tw.prim_load_block,
                                      export_me=False,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))

        palette.add_block('loadblock2arg',
                          style='basic-style-var-arg',
                          hidden=True,
                          label=_('load'),
                          prim_name='loadblock2',
                          string_or_number=True,
                          default=[_('forward'), 100],
                          help_string=_('loads a block'))
        self.tw.lc.def_prim('loadblock2', 2,
                            Primitive(self.tw.prim_load_block,
                                      export_me=False,
                                      arg_descs=[ArgSlot(TYPE_STRING),
                                                 ArgSlot(TYPE_OBJECT)]))

        palette.add_block('loadblock3arg',
                          style='basic-style-var-arg',
                          hidden=True,
                          label=_('load'),
                          string_or_number=True,
                          prim_name='loadblock3',
                          default=[_('setxy'), 0, 0],
                          help_string=_('loads a block'))
        self.tw.lc.def_prim('loadblock3', 3,
                            Primitive(self.tw.prim_load_block,
                                      export_me=False,
                                      arg_descs=[ArgSlot(TYPE_STRING),
                                                 ArgSlot(TYPE_OBJECT),
                                                 ArgSlot(TYPE_OBJECT)]))

        # macro
        palette.add_block('indexblock',
                          style='basic-style-extended-vertical',
                          label=_('index'),
                          help_string=_('return the text of the positions'))

        palette.add_block('index',
                          hidden=True,
                          style='number-style-var-3arg',
                          label=[_('index') + '\n\n', _('string'),
                                 _('start'), _('end')],
                          prim_name='index',
                          default=[_('text'), 0, 1],
                          string_or_number=True,
                          help_string=_('return the text of the positions'))

        self.tw.lc.def_prim('index', 3,
                            Primitive(self.prim_index,
                                      return_type=TYPE_STRING,
                                      arg_descs=[ArgSlot(TYPE_STRING),
                                                 ArgSlot(TYPE_INT),
                                                 ArgSlot(TYPE_INT)]))

    def _portfolio_palette(self):

        palette = make_palette('portfolio',
                               colors=["#0606FF", "#0606A0"],
                               help_string=_('Palette of presentation \
templates'),
                               position=9,
                               translation=_('portfolio'))

        palette.add_block('hideblocks',
                          style='basic-style-extended-vertical',
                          label=_('hide blocks'),
                          prim_name='hideblocks',
                          help_string=_('declutters canvas by hiding blocks'))
        self.tw.lc.def_prim(
            'hideblocks', 0,
            Primitive(self._prim_hideblocks, export_me=False))

        palette.add_block('showblocks',
                          style='basic-style-extended-vertical',
                          label=_('show blocks'),
                          prim_name='showblocks',
                          help_string=_('restores hidden blocks'))
        self.tw.lc.def_prim(
            'showblocks', 0,
            Primitive(self._prim_showblocks, export_me=False))

        palette.add_block('fullscreen',
                          style='basic-style-extended-vertical',
                          label=_('Fullscreen').lower(),
                          prim_name='fullscreen',
                          help_string=_('hides the Sugar toolbars'))
        self.tw.lc.def_prim(
            'fullscreen', 0,
            Primitive(self.tw.set_fullscreen, export_me=False))

        primitive_dictionary['bulletlist'] = self._prim_list
        palette.add_block('bulletlist',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='bullet-style',
                          label=_('list'),
                          string_or_number=True,
                          prim_name='bulletlist',
                          default=['∙ ', '∙ '],
                          help_string=_('presentation bulleted list'))
        self.tw.lc.def_prim('bulletlist', 1,
                            primitive_dictionary['bulletlist'], True)

        # macros
        palette.add_block('list',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: list of \
bullets'))
        MEDIA_SHAPES.append('list')

        palette.add_block('1x1a',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select \
Journal object (no description)'))
        MEDIA_SHAPES.append('1x1a')

        palette.add_block('1x1',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select \
Journal object (with description)'))
        MEDIA_SHAPES.append('1x1')

        palette.add_block('2x2',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select four \
Journal objects'))
        MEDIA_SHAPES.append('2x2')

        palette.add_block('2x1',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select two \
Journal objects'))
        MEDIA_SHAPES.append('2x1')

        palette.add_block('1x2',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select two \
Journal objects'))
        MEDIA_SHAPES.append('1x2')

        # Display-dependent constants
        palette.add_block('leftpos',
                          style='box-style',
                          label=_('left'),
                          prim_name='lpos',
                          logo_command='lpos',
                          help_string=_('xcor of left of screen'))
        self.tw.lc.def_prim(
            'lpos', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('leftpos')]))

        palette.add_block('bottompos',
                          style='box-style',
                          label=_('bottom'),
                          prim_name='bpos',
                          logo_command='bpos',
                          help_string=_('ycor of bottom of screen'))
        self.tw.lc.def_prim(
            'bpos', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('bottompos')]))

        palette.add_block('width',
                          style='box-style',
                          label=_('width'),
                          prim_name='hres',
                          logo_command='width',
                          help_string=_('the canvas width'))
        self.tw.lc.def_prim(
            'hres', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('width')]))

        palette.add_block('rightpos',
                          style='box-style',
                          label=_('right'),
                          prim_name='rpos',
                          logo_command='rpos',
                          help_string=_('xcor of right of screen'))
        self.tw.lc.def_prim(
            'rpos', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('rightpos')]))

        palette.add_block('toppos',
                          style='box-style',
                          label=_('top'),
                          prim_name='tpos',
                          logo_command='tpos',
                          help_string=_('ycor of top of screen'))
        self.tw.lc.def_prim(
            'tpos', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('toppos')]))

        palette.add_block('height',
                          style='box-style',
                          label=_('height'),
                          prim_name='vres',
                          logo_command='height',
                          help_string=_('the canvas height'))
        self.tw.lc.def_prim(
            'vres', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('height')]))

        palette.add_block('titlex',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='box-style',
                          label=_('title x'),
                          logo_command='titlex',
                          prim_name='titlex')
        self.tw.lc.def_prim(
            'titlex', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('titlex')]))

        palette.add_block('titley',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='box-style',
                          label=_('title y'),
                          logo_command='titley',
                          prim_name='titley')
        self.tw.lc.def_prim(
            'titley', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('titley')]))

        palette.add_block('leftx',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='box-style',
                          label=_('left x'),
                          prim_name='leftx',
                          logo_command='leftx')
        self.tw.lc.def_prim(
            'leftx', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('leftx')]))

        palette.add_block('topy',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='box-style',
                          label=_('top y'),
                          prim_name='topy',
                          logo_command='topy')
        self.tw.lc.def_prim(
            'topy', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('topy')]))

        palette.add_block('rightx',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='box-style',
                          label=_('right x'),
                          prim_name='rightx',
                          logo_command='rightx')
        self.tw.lc.def_prim(
            'rightx', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('rightx')]))

        palette.add_block('bottomy',
                          hidden=True,
                          colors=["#0606FF", "#0606A0"],
                          style='box-style',
                          label=_('bottom y'),
                          prim_name='bottomy',
                          logo_command='bottomy')
        self.tw.lc.def_prim(
            'bottomy', 0,
            Primitive(CONSTANTS.get, return_type=TYPE_INT,
                      arg_descs=[ConstantArg('bottomy')]))

    def _myblocks_palette(self):
        ''' User-defined macros are saved as a json-encoded file;
        these get loaded into a palette on startup '''

        if hasattr(self.tw, 'macros_path') and \
                os.path.exists(self.tw.macros_path):
            files = get_endswith_files(self.tw.macros_path, ".tb")
            if len(files) > 0:
                palette = make_palette(
                    'myblocks',
                    colors=["#FFFF00", "#A0A000"],
                    help_string=_('Palette of user-defined operators'),
                    translation=_('my blocks'))

            for tafile in files:
                data = data_from_file(tafile)
                name = os.path.basename(tafile)[:-3]
                # print 'loading macro %s' % (name)
                MACROS['user-defined-' + name] = hat_on_top(listify(data))
                palette.add_block('user-defined-' + name,
                                  style='basic-style-extended-vertical',
                                  label=name)

    # Block primitives

    def after_keypress(self):
        if self.tw.lc.update_values:
            if self.tw.keypress in KEY_DICT:
                if KEY_DICT[self.tw.keypress] in REVERSE_KEY_DICT:
                    self.tw.lc.update_label_value(
                        'keyboard', REVERSE_KEY_DICT[
                            KEY_DICT[self.tw.keypress]])
                else:
                    self.tw.lc.update_label_value(
                        'keyboard', chr(KEY_DICT[self.tw.keypress]))
            elif self.tw.keyboard > 0:
                self.tw.lc.update_label_value('keyboard',
                                              chr(self.tw.keyboard))
        self.tw.keypress = ''

    def after_pop(self, *ignored_args):
        if self.tw.lc.update_values:
            if not self.tw.lc.heap:
                self.tw.lc.update_label_value('pop')
            else:
                self.tw.lc.update_label_value('pop', self.tw.lc.heap[-1])

    def after_push(self, *ignored_args):
        if self.tw.lc.update_values:
            if not self.tw.lc.heap:
                self.tw.lc.update_label_value('pop')
            else:
                self.tw.lc.update_label_value('pop', self.tw.lc.heap[-1])

    def prim_speak(self, text):
        """ Speak text """
        if isinstance(text, float) and int(text) == text:
            text = int(text)

        lang = os.environ['LANG'][0:2]
        if lang in VOICES:
            language_option = '-v ' + VOICES[lang]
        else:
            language_option = ''

        if self.tw.running_sugar:
            from sugar3.speech import SpeechManager
            sm = SpeechManager()
            sm.say_text(text)
        else:
            os.system(
                'espeak %s "%s" --stdout | aplay' %
                (language_option, str(text)))

        if self.tw.sharing():
            if language_option == '':
                event = 'S|%s' % (data_to_string([self.tw.nick, 'None', text]))
            else:
                event = 'S|%s' % (data_to_string([self.tw.nick,
                                                  language_option, text]))
            self.tw.send_event(event)

    def prim_sinewave(self, pitch, amplitude, duration):
        """ Create a Csound score to play a sine wave. """
        self.orchlines = []
        self.scorelines = []
        self.instrlist = []

        try:
            pitch = abs(float(pitch))
            amplitude = abs(float(amplitude))
            duration = abs(float(duration))
        except ValueError:
            self.tw.lc.stop_logo()
            raise logoerror("#notanumber")

        self._play_sinewave(pitch, amplitude, duration)

        if self.tw.running_sugar:
            path = os.path.join(get_path(self.tw.activity, 'instance'),
                                'tmp.csd')
        else:
            path = os.path.join(tempfile.gettempdir(), 'tmp.csd')
        # Create a csound file from the score.
        self._audio_write(path)
        # Play the csound file.
        os.system('csound ' + path + ' > /dev/null 2>&1')

    def _play_sinewave(self, pitch, amplitude, duration, starttime=0,
                       pitch_envelope=99, amplitude_envelope=100,
                       instrument=1):

        pitenv = pitch_envelope
        ampenv = amplitude_envelope
        if 1 not in self.instrlist:
            self.orchlines.append("instr 1\n")
            self.orchlines.append("kpitenv oscil 1, 1/p3, p6\n")
            self.orchlines.append("aenv oscil 1, 1/p3, p7\n")
            self.orchlines.append("asig oscil p5*aenv, p4*kpitenv, p8\n")
            self.orchlines.append("out asig\n")
            self.orchlines.append("endin\n\n")
            self.instrlist.append(1)

        self.scorelines.append("i1 %s %s %s %s %s %s %s\n" %
                               (str(starttime), str(duration), str(pitch),
                                str(amplitude), str(pitenv), str(ampenv),
                                str(instrument)))

    def _audio_write(self, file):
        """ Compile a .csd file. """

        csd = open(file, "w")
        csd.write("<CsoundSynthesizer>\n\n")
        csd.write("<CsOptions>\n")
        csd.write("-+rtaudio=alsa -odevaudio -m0 -d -b256 -B512\n")
        csd.write("</CsOptions>\n\n")
        csd.write("<CsInstruments>\n\n")
        csd.write("sr=16000\n")
        csd.write("ksmps=50\n")
        csd.write("nchnls=1\n\n")
        for line in self.orchlines:
            csd.write(line)
        csd.write("\n</CsInstruments>\n\n")
        csd.write("<CsScore>\n\n")
        csd.write("f1 0 2048 10 1\n")
        csd.write("f2 0 2048 10 1 0 .33 0 .2 0 .143 0 .111\n")
        csd.write("f3 0 2048 10 1 .5 .33 .25 .2 .175 .143 .125 .111 .1\n")
        csd.write("f10 0 2048 10 1 0 0 .3 0 .2 0 0 .1\n")
        csd.write("f99 0 2048 7 1 2048 1\n")
        csd.write("f100 0 2048 7 0. 10 1. 1900 1. 132 0.\n")
        csd.write(self.scorelines.pop())
        csd.write("e\n")
        csd.write("\n</CsScore>\n")
        csd.write("\n</CsoundSynthesizer>")
        csd.close()

    def after_mouse_x(self):
        """ Show mouse x coordinate """
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value('mousex', self.tw.get_mouse_x())

    def after_mouse_y(self):
        """ Show mouse y coordinate """
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value('mousey', self.tw.get_mouse_y())

    def after_see(self):
        """ Show color under turtle """
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value(
                'see',
                self.tw.turtles.get_active_turtle().get_color_index())

    def _prim_list(self, blklist):
        """ Expandable list block """
        self.tw.lc.showlist(blklist)
        self.tw.lc.ireturn()
        yield True

    def after_time(self, elapsed_time):
        """ Update the label of the 'time' block after computing the new
        value. """
        if self.tw.lc.update_values:
            self.tw.lc.update_label_value('time', elapsed_time)

    def _prim_hideblocks(self):
        """ hide blocks and show showblocks button """
        self.tw.hideblocks()
        self.tw.lc.trace = 0
        self.tw.step_time = 0
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon_name("hideshowoff")
            self.tw.activity.stop_turtle_button.set_tooltip(_('Show blocks'))

    def _prim_showblocks(self):
        """ show blocks and show stop turtle button """
        self.tw.showblocks()
        self.tw.lc.trace = 1
        self.tw.step_time = 3
        if self.tw.running_sugar:
            self.tw.activity.stop_turtle_button.set_icon_name("stopiton")
            self.tw.activity.stop_turtle_button.set_tooltip(_('Stop turtle'))

    def after_set(self, name, value=None):
        ''' Update the associated value blocks '''
        if value is not None:
            if self.tw.lc.update_values:
                self.tw.lc.update_label_value(name, value)

    def prim_index(self, string, start, end):
        start = int(start)
        end = int(end)

        return string[start:end]
