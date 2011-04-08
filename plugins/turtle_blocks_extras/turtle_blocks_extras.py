# -*- coding: utf-8 -*-
#Copyright (c) 2011, Walter Bender
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

try:
    from sugar.datastore import datastore
except ImportError:
    pass

from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette, define_logo_function
from TurtleArt.talogo import primitive_dictionary, logoerror, \
    media_blocks_dictionary
from TurtleArt.taconstants import DEFAULT_SCALE, ICON_SIZE, CONSTANTS
from TurtleArt.tautils import convert, round_int, debug_output
from TurtleArt.tajail import myfunc, myfunc_import


def _num_type(x):
    """ Is x a number type? """
    if type(x) == int:
        return True
    if type(x) == float:
        return True
    if type(x) == ord:
        return True
    return False


def _string_to_num(x):
    """ Try to comvert a string to a number """
    xx = convert(x.replace(self.tw.decimal_point, '.'), float)
    if type(xx) is float:
        return xx
    else:
        xx, xflag = chr_to_ord(x)
        if xflag:
            return xx
        else:
            raise logoerror("#syntaxerror")


def _millisecond():
    """ Current time in milliseconds """
    return time() * 1000


class Turtle_blocks_extras(Plugin):
    """ a class for defining the extra palettes that distinguish Turtle Blocks
    from Turtle Art """

    def __init__(self, parent):
        self.tw = parent

    def setup(self):
        self.heap = self.tw.lc.heap
        self.keyboard = self.tw.lc.keyboard
        self.title_height = int((self.tw.canvas.height / 20) * self.tw.scale)

        # set up Turtle Block palettes
        self._flow_palette()

        self._media_palette()

        self._sensor_palette()

        self._extras_palette()

        self._portfolio_palette()

    # Palette definitions

    def _flow_palette(self):
        palette = make_palette('flow',
                               colors=["#FFC000", "#A08000"],
                               help_string=_('Palette of flow operators'))

        # macro
        palette.add_block('while',
                          style='flow-style-boolean',
                          label=_('while'),
                          help_string=_('do-while-True operator that uses \
boolean operators from Numbers palette'))

        # macro
        palette.add_block('until',
                          style='flow-style-boolean',
                          label=_('until'),
                          help_string=_('do-until-True operator that uses \
boolean operators from Numbers palette'))

    def _media_palette(self):

        palette = make_palette('media',
                     colors=["#A0FF00", "#80A000"],
                     help_string=_('Palette of media objects'))

        palette.add_block('journal',
                          style='box-style-media',
                          label=' ',
                          default='None',
                          special_name=_('journal'),
                          help_string=_('Sugar Journal media object'))

        palette.add_block('audio',
                          style='box-style-media',
                          label=' ',
                          special_name=_('audio'),
                          default='None',
                          help_string=_('Sugar Journal audio object'))

        palette.add_block('video',
                          style='box-style-media',
                          label=' ',
                          special_name=_('video'),
                          default='None',
                          help_string=_('Sugar Journal video object'))

        palette.add_block('description',
                          style='box-style-media',
                          label=' ',
                          special_name=_('description'),
                          default='None',
                          help_string=_('Sugar Journal description field'))

        palette.add_block('string',
                          style='box-style',
                          label=_('text'),
                          default=_('text'),
                          special_name=_('text'),
                          help_string=_('string value'))

        primitive_dictionary['show'] = self._prim_show
        palette.add_block('show',
                          style='basic-style-1arg',
                          label=_('show'),
                          default=_('text'),
                          prim_name='show',
                          logo_command='label',
                          help_string=_('draws text or show media from the \
Journal'))
        self.tw.lc.def_prim('show', 1,
            lambda self, x: primitive_dictionary['show'](x, True))

        palette.add_block('showaligned',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('show aligned'),
                          default=_('text'),
                          prim_name='showaligned',
                          logo_command='label',
                          help_string=_('draws text or show media from the \
Journal'))
        self.tw.lc.def_prim('showaligned', 1,
            lambda self, x: primitive_dictionary['show'](x, False))

        # deprecated
        primitive_dictionary['write'] = self._prim_write
        palette.add_block('write',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('show'),
                          default=[_('text'), 32],
                          prim_name='write',
                          logo_command='label',
                          help_string=_('draws text or show media from the \
Journal'))
        self.tw.lc.def_prim('write', 2,
            lambda self, x, y: primitive_dictionary['write'](x, y))

        primitive_dictionary['setscale'] = self._prim_setscale
        palette.add_block('setscale',
                          style='basic-style-1arg',
                          label=_('set scale'),
                          prim_name='setscale',
                          default=33,
                          logo_command='setlabelheight',
                          help_string=_('sets the scale of media'))
        self.tw.lc.def_prim('setscale', 1,
            lambda self, x: primitive_dictionary['setscale'](x))

        primitive_dictionary['savepix'] = self._prim_save_picture
        palette.add_block('savepix',
                          style='basic-style-1arg',
                          label=_('save picture'),
                          prim_name='savepix',
                          default=_('picture name'),
                          help_string=_('saves a picture to the Sugar \
Journal'))
        self.tw.lc.def_prim('savepix', 1,
                            lambda self, x: primitive_dictionary['savepix'](x))

        primitive_dictionary['savesvg'] = self._prim_save_svg
        palette.add_block('savesvg',
                          style='basic-style-1arg',
                          label=_('save SVG'),
                          prim_name='savesvg',
                          default=_('picture name'),
                          help_string=_('saves turtle graphics as an SVG file \
in the Sugar Journal'))
        self.tw.lc.def_prim('savesvg', 1,
                            lambda self, x: primitive_dictionary['savesvg'](x))

        palette.add_block('scale',
                          style='box-style',
                          label=_('scale'),
                          prim_name='scale',
                          value_block=True,
                          logo_command='labelsize',
                          help_string=_('holds current scale value'))
        self.tw.lc.def_prim('scale', 0, lambda self: self.tw.lc.scale)

        palette.add_block('mediawait',
                          style='basic-style-extended-vertical',
                          label=_('media wait'),
                          prim_name='mediawait',
                          help_string=_('wait for current video or audio to \
complete'))
        self.tw.lc.def_prim('mediawait', 0, self.tw.lc.media_wait, True)

    def _sensor_palette(self):

        palette = make_palette('sensor',
                     colors=["#FF6060", "#A06060"],
                     help_string=_('Palette of sensor blocks'))

        primitive_dictionary['kbinput'] = self._prim_kbinput
        palette.add_block('kbinput',
                          style='basic-style-extended-vertical',
                          label=_('query keyboard'),
                          prim_name='kbinput',
                          help_string=_('query for keyboard input (results \
stored in keyboard block)'))
        self.tw.lc.def_prim('kbinput', 0,
                            lambda self: primitive_dictionary['kbinput']())

        palette.add_block('keyboard',
                          style='box-style',
                          label=_('keyboard'),
                          prim_name='keyboard',
                          value_block=True,
                          logo_command='make "keyboard readchar',
                          help_string=_('holds results of query-keyboard \
block'))
        self.tw.lc.def_prim('keyboard', 0, lambda self: self.tw.lc.keyboard)

        primitive_dictionary['readpixel'] = self._prim_readpixel
        palette.add_block('readpixel',
                          style='basic-style-extended-vertical',
                          label=_('read pixel'),
                          prim_name='readpixel',
                          logo_command=':keyboard',
                          help_string=_('RGB color under the turtle is pushed \
to the stack'))
        self.tw.lc.def_prim('readpixel', 0,
                            lambda self: primitive_dictionary['readpixel']())

        primitive_dictionary['see'] = self._prim_see
        palette.add_block('see',
                          style='box-style',
                          label=_('turtle sees'),
                          prim_name='see',
                          help_string=_('returns the color that the turtle \
"sees"'))
        self.tw.lc.def_prim('see', 0,
                            lambda self: primitive_dictionary['see']())

        primitive_dictionary['time'] = self._prim_time
        palette.add_block('time',
                          style='box-style',
                          label=_('time'),
                          prim_name='time',
                          value_block=True,
                          help_string=_('elapsed time (in seconds) since \
program started'))
        self.tw.lc.def_prim('time', 0,
                            lambda self: primitive_dictionary['time']())

    def _extras_palette(self):

        palette = make_palette('extras',
                     colors=["#FF0000", "#A00000"],
                     help_string=_('Palette of extra options'))

        primitive_dictionary['push'] = self._prim_push
        palette.add_block('push',
                          style='basic-style-1arg',
                          label=_('push'),
                          prim_name='push',
                          logo_command='tapush',
                          help_string=_('pushes value onto FILO (first-in \
last-out heap)'))
        self.tw.lc.def_prim('push', 1,
                            lambda self, x: primitive_dictionary['push'](x))
        define_logo_function('tapush', 'to tapush :foo\rmake "taheap fput \
:foo :taheap\rend\rmake "taheap []\r')

        primitive_dictionary['printheap'] = self._prim_printheap
        palette.add_block('printheap',
                          style='basic-style-extended-vertical',
                          label=_('show heap'),
                          prim_name='printheap',
                          logo_command='taprintheap',
                          help_string=_('shows values in FILO (first-in \
last-out heap)'))
        self.tw.lc.def_prim('printheap', 0,
                            lambda self: primitive_dictionary['printheap']())
        define_logo_function('taprintheap', 'to taprintheap \rprint :taheap\r\
end\r')

        primitive_dictionary['clearheap'] = self._prim_emptyheap
        palette.add_block('clearheap',
                          style='basic-style-extended-vertical',
                          label=_('empty heap'),
                          prim_name='clearheap',
                          logo_command='taclearheap',
                          help_string=_('emptys FILO (first-in-last-out \
heap)'))
        self.tw.lc.def_prim('clearheap', 0,
                            lambda self: primitive_dictionary['clearheap']())
        define_logo_function('taclearheap', 'to taclearheap\rmake "taheap []\r\
end\r')

        primitive_dictionary['pop'] = self._prim_pop
        palette.add_block('pop',
                          style='box-style',
                          label=_('pop'),
                          prim_name='pop',
                          value_block=True,
                          logo_command='tapop',
                          help_string=_('pops value off FILO (first-in \
last-out heap)'))
        self.tw.lc.def_prim('pop', 0,
                            lambda self: primitive_dictionary['pop']())
        define_logo_function('tapop', 'to tapop\rif emptyp :taheap [stop]\r\
make "tmp first :taheap\rmake "taheap butfirst :taheap\routput :tmp\rend\r')

        primitive_dictionary['print'] = self._prim_print
        palette.add_block('comment',
                          style='basic-style-1arg',
                          label=_('comment'),
                          prim_name='comment',
                          default=_('comment'),
                          help_string=_('places a comment in your code'))
        self.tw.lc.def_prim('comment', 1,
            lambda self, x: primitive_dictionary['print'](x, True))

        palette.add_block('print',
                          style='basic-style-1arg',
                          label=_('print'),
                          prim_name='print',
                          logo_command='label',
                          help_string=_('prints value in status block at \
bottom of the screen'))
        self.tw.lc.def_prim('print', 1,
            lambda self, x: primitive_dictionary['print'](x, False))

        primitive_dictionary['myfunction'] = self._prim_myfunction
        palette.add_block('myfunc1arg',
                          style='number-style-var-arg',
                          label=[_('Python'), 'f(x)', 'x'],
                          prim_name='myfunction',
                          default=['x', 100],
                          help_string=_('a programmable block: used to add \
advanced single-variable math equations, e.g., sin(x)'))
        self.tw.lc.def_prim('myfunction', 2,
            lambda self, f, x: primitive_dictionary['myfunction'](f, [x]))

        palette.add_block('myfunc2arg',
                          hidden=True,
                          style='number-style-var-arg',
                          label=[_('Python'), 'f(x,y)', 'x'],
                          prim_name='myfunction2',
                          default=['x+y', 100, 100],
                          help_string=_('a programmable block: used to add \
advanced multi-variable math equations, e.g., sqrt(x*x+y*y)'))
        self.tw.lc.def_prim('myfunction2', 3,
            lambda self, f, x, y: primitive_dictionary['myfunction'](
                f, [x, y]))

        palette.add_block('myfunc3arg',
                          hidden=True,
                          style='number-style-var-arg',
                          label=[_('Python'), 'f(x,y,z)', 'x'],
                          prim_name='myfunction3',
                          default=['x+y+z', 100, 100, 100],
                          help_string=_('a programmable block: used to add \
advanced multi-variable math equations, e.g., sin(x+y+z)'))
        self.tw.lc.def_prim('myfunction3', 4,
            lambda self, f, x, y, z: primitive_dictionary['myfunction'](
                f, [x, y, z]))

        primitive_dictionary['userdefined'] = self._prim_myblock
        palette.add_block('userdefined',
                          style='basic-style-var-arg',
                          label=' ',
                          prim_name='userdefined',
                          special_name=_('Python block'),
                          default=100,
                          help_string=_('runs code found in the tamyblock.py \
module found in the Journal'))
        self.tw.lc.def_prim('userdefined', 1,
            lambda self, x: primitive_dictionary['userdefined']([x]))

        palette.add_block('userdefined2args',
                          hidden=True,
                          style='basic-style-var-arg',
                          label=' ',
                          prim_name='userdefined2',
                          special_name=_('Python block'),
                          default=[100, 100],
                          help_string=_('runs code found in the tamyblock.py \
module found in the Journal'))
        self.tw.lc.def_prim('userdefined2', 2,
            lambda self, x, y: primitive_dictionary['userdefined']([x, y]))

        palette.add_block('userdefined3args',
                          hidden=True,
                          style='basic-style-var-arg',
                          label=' ',
                          prim_name='userdefined3',
                          special_name=_('Python block'),
                          default=[100, 100, 100],
                          help_string=_('runs code found in the tamyblock.py \
module found in the Journal'))
        self.tw.lc.def_prim('userdefined3', 3,
            lambda self, x, y, z: primitive_dictionary['userdefined'](
                [x, y, z]))

        palette.add_block('cartesian',
                          style='basic-style-extended-vertical',
                          label=_('Cartesian'),
                          prim_name='cartesian',
                          help_string=_('displays Cartesian coordinates'))
        self.tw.lc.def_prim('cartesian', 0,
                             lambda self: self.tw.set_cartesian(True))

        palette.add_block('polar',
                          style='basic-style-extended-vertical',
                          label=_('polar'),
                          prim_name='polar',
                          help_string=_('displays polar coordinates'))
        self.tw.lc.def_prim('polar', 0,
                             lambda self: self.tw.set_polar(True))

        palette.add_block('addturtle',
                          style='basic-style-1arg',
                          label=_('turtle'),
                          prim_name='turtle',
                          default=1,
                          help_string=_('chooses which turtle to command'))
        self.tw.lc.def_prim('turtle', 1,
            lambda self, x: self.tw.canvas.set_turtle(x))

        primitive_dictionary['skin'] = self._prim_reskin
        palette.add_block('skin',
                          hidden=True,
                          style='basic-style-1arg',
                          label=_('turtle shell'),
                          prim_name='skin',
                          help_string=_("put a custom 'shell' on the turtle"))
        self.tw.lc.def_prim('skin', 1,
            lambda self, x: primitive_dictionary['skin'](x))

        # macro
        palette.add_block('reskin',
                          style='basic-style-1arg',
                          label=_('turtle shell'),
                          help_string=_("put a custom 'shell' on the turtle"))

        palette.add_block('sandwichtop_no_label',
                          style='collapsible-top-no-label',
                          label=[' ', ' '],
                          special_name=_('top'),
                          prim_name='nop',
                          help_string=_('top of a collapsed stack'))

        palette.add_block('sandwichbottom',
                          style='collapsible-bottom',
                          label=[' ', ' '],
                          prim_name='nop',
                          special_name=_('bottom'),
                          help_string=_('bottom of a collapsible stack'))

        palette.add_block('sandwichcollapsed',
                          hidden=True,
                          style='invisible',
                          label=' ',
                          prim_name='nop',
                          help_string=_('bottom block in a collapsed stack: \
click to open'))

        # deprecated blocks
        palette.add_block('sandwichtop',
                          hidden=True,
                          style='collapsible-top',
                          label=_('top of stack'),
                          default=_('label'),
                          prim_name='comment',
                          help_string=_('top of stack'))

        palette.add_block('sandwichtop_no_arm',
                          hidden=True,
                          style='collapsible-top-no-arm',
                          label=_('top of a collapsible stack'),
                          default=_('label'),
                          prim_name='comment',
                          help_string=_('top of stack'))

        palette.add_block('sandwichtop_no_arm_no_label',
                          hidden=True,
                          style='collapsible-top-no-arm-no-label',
                          label=[' ', _('click to open')],
                          prim_name='nop',
                          help_string=_('top of stack'))

    def _portfolio_palette(self):

        palette = make_palette('portfolio',
                     colors=["#0606FF", "#0606A0"],
                     help_string=_('Palette of presentation templates'))

        palette.add_block('hideblocks',
                          style='basic-style-extended-vertical',
                          label=_('hide blocks'),
                          prim_name='hideblocks',
                          help_string=_('declutters canvas by hiding blocks'))
        self.tw.lc.def_prim('hideblocks', 0, lambda self: self.tw.hideblocks())

        palette.add_block('showblocks',
                          style='basic-style-extended-vertical',
                          label=_('show blocks'),
                          prim_name='showblocks',
                          help_string=_('restores hidden blocks'))
        self.tw.lc.def_prim('showblocks', 0, lambda self: self.tw.showblocks())

        palette.add_block('fullscreen',
                          style='basic-style-extended-vertical',
                          label=_('full screen'),
                          prim_name='fullscreen',
                          help_string=_('hides the Sugar toolbars'))
        self.tw.lc.def_prim('fullscreen', 0,
                             lambda self: self.tw.set_fullscreen())

        primitive_dictionary['bulletlist'] = self._prim_list
        palette.add_block('list',
                          hidden=True,
                          style='bullet-style',
                          label=_('list'),
                          prim_name='bulletlist',
                          default=['∙ ', '∙ '],
                          help_string=_('presentation bulleted list'))
        self.tw.lc.def_prim('bulletlist', 1,
                             primitive_dictionary['bulletlist'], True)

        # macros
        palette.add_block('picturelist',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: list of \
bullets'))

        palette.add_block('picture1x1a',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select \
Journal object (no description)'))

        palette.add_block('picture1x1',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select \
Journal object (with description)'))

        palette.add_block('picture2x2',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select four \
Journal objects'))

        palette.add_block('picture2x1',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select two \
Journal objects'))

        palette.add_block('picture1x2',
                          style='basic-style-extended',
                          label=' ',
                          help_string=_('presentation template: select two \
Journal objects'))

        # Display-dependent constants
        palette.add_block('leftpos',
                          style='box-style',
                          label=_('left'),
                          prim_name='lpos',
                          logo_command='lpos',
                          help_string=_('xcor of left of screen'))
        self.tw.lc.def_prim('lpos', 0, lambda self: CONSTANTS['leftpos'])

        palette.add_block('bottompos',
                          style='box-style',
                          label=_('bottom'),
                          prim_name='bpos',
                          logo_command='bpos',
                          help_string=_('ycor of bottom of screen'))
        self.tw.lc.def_prim('bpos', 0, lambda self: CONSTANTS['bottompos'])

        palette.add_block('width',
                          style='box-style',
                          label=_('width'),
                          prim_name='hres',
                          logo_command='width',
                          help_string=_('the canvas width'))
        self.tw.lc.def_prim('hres', 0, lambda self: CONSTANTS['width'])

        palette.add_block('rightpos',
                          style='box-style',
                          label=_('right'),
                          prim_name='rpos',
                          logo_command='rpos',
                          help_string=_('xcor of right of screen'))
        self.tw.lc.def_prim('rpos', 0, lambda self: CONSTANTS['rightpos'])

        palette.add_block('toppos',
                          style='box-style',
                          label=_('top'),
                          prim_name='tpos',
                          logo_command='tpos',
                          help_string=_('ycor of top of screen'))
        self.tw.lc.def_prim('tpos', 0, lambda self: CONSTANTS['toppos'])

        palette.add_block('height',
                          style='box-style',
                          label=_('height'),
                          prim_name='vres',
                          logo_command='height',
                          help_string=_('the canvas height'))
        self.tw.lc.def_prim('vres', 0, lambda self: CONSTANTS['height'])

        palette.add_block('titlex',
                          hidden=True,
                          style='box-style',
                          label=_('title x'),
                          logo_command='titlex',
                          prim_name='titlex')
        self.tw.lc.def_prim('titlex', 0, lambda self: CONSTANTS['titlex'])

        palette.add_block('titley',
                          hidden=True,
                          style='box-style',
                          label=_('title y'),
                          logo_command='titley',
                          prim_name='titley')
        self.tw.lc.def_prim('titley', 0, lambda self: CONSTANTS['titley'])

        palette.add_block('leftx',
                          hidden=True,
                          style='box-style',
                          label=_('left x'),
                          prim_name='leftx',
                          logo_command='leftx')
        self.tw.lc.def_prim('leftx', 0, lambda self: CONSTANTS['leftx'])

        palette.add_block('topy',
                          hidden=True,
                          style='box-style',
                          label=_('top y'),
                          prim_name='topy',
                          logo_command='topy')
        self.tw.lc.def_prim('topy', 0, lambda self: CONSTANTS['topy'])

        palette.add_block('rightx',
                          hidden=True,
                          style='box-style',
                          label=_('right x'),
                          prim_name='rightx',
                          logo_command='rightx')
        self.tw.lc.def_prim('rightx', 0, lambda self: CONSTANTS['rightx'])

        palette.add_block('bottomy',
                          hidden=True,
                          style='box-style',
                          label=_('bottom y'),
                          prim_name='bottomy',
                          logo_command='bottomy')
        self.tw.lc.def_prim('bottomy', 0, lambda self: CONSTANTS['bottomy'])

        # deprecated blocks

        primitive_dictionary['t1x1'] = self._prim_t1x1
        palette.add_block('template1x1',
                          hidden=True,
                          style='portfolio-style-1x1',
                          label=' ',
                          prim_name='t1x1',
                          default=[_('Title'), 'None'],
                          special_name=_('presentation 1x1'),
                          help_string=_('presentation template: select \
Journal object (with description)'))
        self.tw.lc.def_prim('t1x1', 2,
            lambda self, a, b: primitive_dictionary['t1x1'](a, b))

        primitive_dictionary['t1x1a'] = self._prim_t1x1a
        palette.add_block('template1x1a',
                          hidden=True,
                          style='portfolio-style-1x1',
                          label=' ',
                          prim_name='t1x1a',
                          default=[_('Title'), 'None'],
                          special_name=_('presentation 1x1'),
                          help_string=_('presentation template: select \
Journal object (no description)'))
        self.tw.lc.def_prim('t1x1a', 2,
            lambda self, a, b: primitive_dictionary['t1x1a'](a, b))

        primitive_dictionary['2x1'] = self._prim_t2x1
        palette.add_block('template2x1',
                          hidden=True,
                          style='portfolio-style-2x1',
                          label=' ',
                          prim_name='t2x1',
                          default=[_('Title'), 'None', 'None'],
                          special_name=_('presentation 2x1'),
                          help_string=_("presentation template: select two \
Journal objects"))
        self.tw.lc.def_prim('t2x1', 3,
            lambda self, a, b, c: primitive_dictionary['t2x1'](a, b, c))

        primitive_dictionary['1x2'] = self._prim_t1x2
        palette.add_block('template1x2',
                          hidden=True,
                          style='portfolio-style-1x2',
                          label=' ',
                          prim_name='t1x2',
                          default=[_('Title'), 'None', 'None'],
                          special_name=_('presentation 1x2'),
                          help_string=_("presentation template: select two \
Journal objects"))
        self.tw.lc.def_prim('t1x2', 3,
            lambda self, a, b, c: primitive_dictionary['t1x2'](a, b, c))

        primitive_dictionary['t2x2'] = self._prim_t2x2
        palette.add_block('template2x2',
                          hidden=True,
                          style='portfolio-style-2x2',
                          label=' ',
                          prim_name='t2x2',
                          default=[_('Title'), 'None', 'None', 'None', 'None'],
                          special_name=_('presentation 2x2'),
                          help_string=_("presentation template: select four \
Journal objects"))
        self.tw.lc.def_prim('t2x2', 5,
            lambda self, a, b, c, d, e: primitive_dictionary['t2x2'](
                a, b, c, d, e))

        palette.add_block('templatelist',
                          hidden=True,
                          style='bullet-style',
                          label=' ',
                          prim_name='bullet',
                          default=[_('Title'), '∙ '],
                          special_name=_('presentation bulleted list'),
                          help_string=_('presentation template: list of \
bullets'))
        self.tw.lc.def_prim('bullet', 1, self._prim_list, True)

    # Block primitives

    def _prim_emptyheap(self):
        """ Empty FILO """
        self.tw.lc.heap = []

    def _prim_kbinput(self):
        """ Query keyboard """
        if len(self.tw.keypress) == 1:
            self.tw.lc.keyboard = ord(self.tw.keypress[0])
        else:
            try:
                self.tw.lc.keyboard = {'Escape': 27, 'space': 32, ' ': 32,
                    'Return': 13, 'KP_Up': 2, 'KP_Down': 4, 'KP_Left': 1,
                    'KP_Right': 3}[self.tw.keypress]
            except KeyError:
                self.tw.lc.keyboard = 0
        self.tw.lc.update_label_value('keyboard', self.tw.lc.keyboard)
        self.tw.keypress = ''

    def _prim_list(self, blklist):
        """ Expandable list block """
        self._prim_showlist(blklist)
        self.tw.lc.ireturn()
        yield True

    def _prim_myblock(self, x):
        """ Run Python code imported from Journal """
        if self.tw.lc.bindex is not None and \
           self.tw.lc.bindex in self.tw.myblock:
            try:
                if len(x) == 1:
                    myfunc_import(self, self.tw.myblock[self.tw.lc.bindex],
                                  x[0])
                else:
                    myfunc_import(self, self.tw.myblock[self.tw.lc.bindex], x)
            except:
                raise logoerror("#syntaxerror")

    def _prim_myfunction(self, f, x):
        """ Programmable block """
        try:
            y = myfunc(f, x)
            if str(y) == 'nan':
                debug_output('Python function returned NAN',
                             self.tw.running_sugar)
                self.tw.lc.stop_logo()
                raise logoerror("#notanumber")
            else:
                return y
        except ZeroDivisionError:
            self.tw.lc.stop_logo()
            raise logoerror("#zerodivide")
        except ValueError, e:
            self.tw.lc.stop_logo()
            raise logoerror('#' + str(e))
        except SyntaxError, e:
            self.tw.lc.stop_logo()
            raise logoerror('#' + str(e))
        except NameError, e:
            self.tw.lc.stop_logo()
            raise logoerror('#' + str(e))
        except OverflowError:
            self.tw.lc.stop_logo()
            raise logoerror("#overflowerror")
        except TypeError:
            self.tw.lc.stop_logo()
            raise logoerror("#notanumber")

    def _prim_pop(self):
        """ Pop value off of FILO """
        if len(self.tw.lc.heap) == 0:
            raise logoerror("#emptyheap")
        else:
            if len(self.tw.lc.heap) == 1:
                self.tw.lc.update_label_value('pop')
            else:
                self.tw.lc.update_label_value('pop', self.tw.lc.heap[-2])
            return self.tw.lc.heap.pop(-1)

    def _prim_print(self, n, flag):
        """ Print object n """
        if flag and (self.tw.hide or self.tw.step_time == 0):
            return
        if type(n) == str or type(n) == unicode:
            if n[0:6] == 'media_' and \
               n[6:].lower not in media_blocks_dictionary:
                try:
                    if self.tw.running_sugar:
                        try:
                            dsobject = datastore.get(n[6:])
                        except:
                            debug_output("Couldn't open %s" % (n[6:]),
                                         self.tw.running_sugar)
                        self.tw.showlabel('status', dsobject.metadata['title'])
                        dsobject.destroy()
                    else:
                        self.tw.showlabel('status', n[6:])
                except IOError:
                    self.tw.showlabel('status', n)
            else:
                self.tw.showlabel('status', n)
        elif type(n) == int:
            self.tw.showlabel('status', n)
        else:
            self.tw.showlabel('status',
                str(round_int(n)).replace('.', self.tw.decimal_point))

    def _prim_printheap(self):
        """ Display contents of heap """
        heap_as_string = str(self.tw.lc.heap)
        if len(heap_as_string) > 80:
            self.tw.showlabel('status', str(self.tw.lc.heap)[0:79] + '…')
        else:
            self.tw.showlabel('status', str(self.tw.lc.heap))

    def _prim_push(self, val):
        """ Push value onto FILO """
        self.tw.lc.heap.append(val)
        self.tw.lc.update_label_value('pop', val)

    def _prim_readpixel(self):
        """ Read r, g, b, a from the canvas and push b, g, r to the stack """
        r, g, b, a = self.tw.canvas.get_pixel()
        self.tw.lc.heap.append(b)
        self.tw.lc.heap.append(g)
        self.tw.lc.heap.append(r)

    def _prim_reskin(self, media):
        """ Reskin the turtle with an image from a file """
        scale = int(ICON_SIZE * float(self.tw.lc.scale) / DEFAULT_SCALE)
        if scale < 1:
            return
        self.tw.lc.filepath = None
        dsobject = None
        if os.path.exists(media[6:]):  # is it a path?
            self.tw.lc.filepath = media[6:]
        elif self.tw.running_sugar:  # is it a datastore object?
            try:
                dsobject = datastore.get(media[6:])
            except:
                debug_output("Couldn't open skin %s" % (media[6:]),
                             self.tw.running_sugar)
            if dsobject is not None:
                self.tw.lc.filepath = dsobject.file_path
        if self.tw.lc.filepath == None:
            self.tw.showlabel('nojournal', self.tw.lc.filepath)
            return
        pixbuf = None
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.tw.lc.filepath,
                                                          scale, scale)
        except:
            self.tw.showlabel('nojournal', self.tw.lc.filepath)
            debug_output("Couldn't open skin %s" % (self.tw.lc.filepath),
                         self.tw.running_sugar)
        if pixbuf is not None:
            self.tw.active_turtle.set_shapes([pixbuf])
            pen_state = self.tw.active_turtle.get_pen_state()
            if pen_state:
                self.tw.canvas.setpen(False)
            self.tw.canvas.forward(0)
            if pen_state:
                self.tw.canvas.setpen(True)

    def _prim_save_picture(self, name):
        """ Save canvas to file as PNG """
        self.tw.save_as_image(name)

    def _prim_save_svg(self, name):
        """ Save SVG to file """
        self.tw.canvas.svg_close()
        self.tw.save_as_image(name, True)

    def _prim_see(self):
        """ Read r, g, b from the canvas and return a corresponding palette
        color """
        r, g, b, a = self.tw.canvas.get_pixel()
        color_index = self.tw.canvas.get_color_index(r, g, b)
        self.tw.lc.update_label_value('see', color_index)
        return color_index

    def _prim_setscale(self, scale):
        """ Set the scale used by the show block """
        self.tw.lc.scale = scale
        self.tw.lc.update_label_value('scale', scale)

    def _prim_show(self, string, center=False):
        """ Show is the general-purpose media-rendering block. """
        if type(string) == str or type(string) == unicode:
            if string in  ['media_', 'descr_', 'audio_', 'video_',
                           'media_None', 'descr_None', 'audio_None',
                           'video_None']:
                pass
            elif string[0:6] in ['media_', 'descr_', 'audio_', 'video_']:
                self.tw.lc.filepath = None
                self.tw.lc.dsobject = None
                if string[6:].lower() in media_blocks_dictionary:
                    media_blocks_dictionary[string[6:].lower()]()
                elif os.path.exists(string[6:]):  # is it a path?
                    self.tw.lc.filepath = string[6:]
                elif self.tw.running_sugar:  # is it a datastore object?
                    try:
                        self.tw.lc.dsobject = datastore.get(string[6:])
                    except:
                        debug_output("Couldn't find dsobject %s" % (
                                string[6:]), self.tw.running_sugar)
                    if self.tw.lc.dsobject is not None:
                        self.tw.lc.filepath = self.tw.lc.dsobject.file_path
                if self.tw.lc.filepath == None:
                    if self.tw.lc.dsobject is not None:
                        self.tw.showlabel('nojournal',
                            self.tw.lc.dsobject.metadata['title'])
                    else:
                        self.tw.showlabel('nojournal', string[6:])
                    debug_output("Couldn't open %s" % (string[6:]),
                                 self.tw.running_sugar)
                elif string[0:6] == 'media_':
                    self.tw.lc.insert_image(center)
                elif string[0:6] == 'descr_':
                    mimetype = None
                    if self.tw.lc.dsobject is not None and \
                       'mime_type' in self.tw.lc.dsobject.metadata:
                        mimetype = self.tw.lc.dsobject.metadata['mime_type']
                    description = None
                    if self.tw.lc.dsobject is not None and \
                       'description' in self.tw.lc.dsobject.metadata:
                        description = self.tw.lc.dsobject.metadata[
                            'description']
                    self.tw.lc.insert_desc(mimetype, description)
                elif string[0:6] == 'audio_':
                    self.tw.lc.play_sound()
                elif string[0:6] == 'video_':
                    self.tw.lc.play_video()
                if self.tw.lc.dsobject is not None:
                    self.tw.lc.dsobject.destroy()
            else:  # assume it is text to display
                x, y = self.tw.lc.x2tx(), self.tw.lc.y2ty()
                if center:
                    y -= self.tw.canvas.textsize
                self.tw.canvas.draw_text(string, x, y,
                                         int(self.tw.canvas.textsize * \
                                             self.tw.lc.scale / 100.),
                                         self.tw.canvas.width - x)
        elif type(string) == float or type(string) == int:
            string = round_int(string)
            x, y = self.tw.lc.x2tx(), self.tw.lc.y2ty()
            if center:
                y -= self.tw.canvas.textsize
            self.tw.canvas.draw_text(string, x, y,
                                     int(self.tw.canvas.textsize * \
                                         self.tw.lc.scale / 100.),
                                     self.tw.canvas.width - x)

    def _prim_showlist(self, sarray):
        """ Display list of media objects """
        x = self.tw.canvas.xcor / self.tw.coord_scale
        y = self.tw.canvas.ycor / self.tw.coord_scale
        for s in sarray:
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(s)
            y -= int(self.tw.canvas.textsize * self.tw.lead)

    def _prim_time(self):
        """ Number of seconds since program execution has started or
        clean (prim_clear) block encountered """
        elapsed_time = int(time() - self.tw.lc.start_time)
        self.tw.lc.update_label_value('time', elapsed_time)
        return elapsed_time

    # Deprecated blocks

    def _prim_t1x1(self, title, media):
        """ title, one image, and description """
        xo = self.tw.calc_position('t1x1')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._prim_show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) \
                      / self.tw.canvas.height
        self._prim_setscale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.tw.lc.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(media.replace('media_', 'descr_'))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _prim_t2x1(self, title, media1, media2):
        """ title, two images (horizontal), two descriptions """
        xo = self.tw.calc_position('t2x1')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._prim_show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                  self.tw.canvas.height
        self._prim_setscale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.tw.lc.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media1)
        x = 0
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media2)
        y = -self.title_height
        if self.tw.running_sugar:
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(media2.replace('media_', 'descr_'))
            x = -(self.tw.canvas.width / 2) + xo
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(media1.replace('media_', 'descr_'))
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _prim_t1x2(self, title, media1, media2):
        """ title, two images (vertical), two desciptions """
        xo = self.tw.calc_position('t1x2')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._prim_show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                 self.tw.canvas.height
        self._prim_setscale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.tw.lc.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media1)
        if self.tw.running_sugar:
            x = 0
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(media1.replace('media_', 'descr_'))
            y = -self.title_height
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(media2.replace('media_', 'descr_'))
            x = -(self.tw.canvas.width / 2) + xo
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(media2)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _prim_t2x2(self, title, media1, media2, media3, media4):
        """ title and four images """
        xo = self.tw.calc_position('t2x2')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._prim_show(title)
        # calculate and set scale for media blocks
        myscale = 45 * (self.tw.canvas.height - self.title_height * 2) / \
                  self.tw.canvas.height
        self._prim_setscale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.tw.lc.body_height)
        # render four quadrents
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media1)
        x = 0
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media2)
        y = -self.title_height
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media4)
        x = -(self.tw.canvas.width / 2) + xo
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media3)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _prim_t1x1a(self, title, media1):
        """ title, one media object """
        xo = self.tw.calc_position('t1x1a')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._prim_show(title)
        # calculate and set scale for media blocks
        myscale = 90 * (self.tw.canvas.height - self.title_height * 2) / \
                       self.tw.canvas.height
        self._prim_setscale(myscale)
        # set body text size
        self.tw.canvas.settextsize(self.tw.lc.body_height)
        # render media object
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        self.tw.canvas.setxy(x, y, pendown=False)
        self._prim_show(media1)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _prim_write(self, string, fsize):
        """ Write string at size """
        x = self.tw.canvas.width / 2 + int(self.tw.canvas.xcor)
        y = self.tw.canvas.height / 2 - int(self.tw.canvas.ycor)
        self.tw.canvas.draw_text(string, x, y - 15, int(fsize),
                                 self.tw.canvas.width)
