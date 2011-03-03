# -*- coding: utf-8 -*-
#Copyright (c) 2011, Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import gtk
from time import time
import os.path
from gettext import gettext as _

try:
    from sugar.datastore import datastore
except ImportError:
    pass

from plugin import Plugin
from TurtleArt.taprimitive import Palette, Primitive, make_prim
from TurtleArt.talogo import PLUGIN_DICTIONARY, logoerror, \
    MEDIA_BLOCKS_DICTIONARY
from TurtleArt.taconstants import DEFAULT_SCALE, CONSTANTS, BLACK, WHITE, \
    ICON_SIZE
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


class Turtle_blocks_plugin(Plugin):
    """ a class for defining the extra palettes that distinguish Turtle Blocks
    from Turtle Art """

    def __init__(self, parent):
        self.tw = parent

    def setup(self):
        self.heap = self.tw.lc.heap
        self.keyboard = self.tw.lc.keyboard

        # set up Turtle Block palettes
        self._flow_palette()

        p = Palette('media', ["#A0FF00", "#80A000"])
        p.set_help(_('Palette of media objects'))
        p.add_palette()
        self._media_palette()

        p = Palette('sensor', ["#FF6060", "#A06060"])
        p.set_help(_('Palette of sensor blocks'))
        p.add_palette()
        self._sensor_palette()

        p = Palette('extras', ["#FF0000", "#A00000"])
        p.set_help(_('Palette of extra options'))
        p.add_palette()
        self._extras_palette()

        p = Palette('portfolio', ["#0606FF", "#0606A0"])
        p.set_help(_('Palette of presentation templates'))
        p.add_palette()
        self._portfolio_palette()

    def start(self):
        pass

    def stop(self):
        pass

    def goto_background(self):
        pass

    def return_to_foreground(self):
        pass

    def quit(self):
        pass

    # Palette definitions

    def _flow_palette(self):
        # macro
        make_prim('while',
                  palette='flow',
                  style='flow-style-boolean',
                  label=_('while'),
                  help_string=_('do-while-True operator that uses boolean \
operators from Numbers palette'))

        # macro
        make_prim('until',
                  palette='flow',
                  style='flow-style-boolean',
                  label=_('until'),
                  help_string=_('do-until-True operator that uses boolean \
operators from Numbers palette'))

    def _media_palette(self):
        make_prim('journal',
                  palette='media',
                  style='box-style-media',
                  label=' ',
                  default='None',
                  special_name=_('journal'),
                  help_string=_('Sugar Journal media object'))

        make_prim('audio',
                  palette='media',
                  style='box-style-media',
                  label=' ',
                  special_name=_('audio'),
                  default='None',
                  help_string=_('Sugar Journal audio object'))

        make_prim('video',
                  palette='media',
                  style='box-style-media',
                  label=' ',
                  special_name=_('video'),
                  default='None',
                  help_string=_('Sugar Journal video object'))

        make_prim('description',
                  palette='media',
                  style='box-style-media',
                  label=' ',
                  special_name=_('description'),
                  default='None',
                  help_string=_('Sugar Journal description field'))

        make_prim('string',
                  palette='media',
                  style='box-style',
                  label=_('text'),
                  default=_('text'),
                  special_name='',
                  help_string=_('string value'))

        PLUGIN_DICTIONARY['show'] = self._prim_show
        make_prim('show',
                  palette='media',
                  style='basic-style-1arg',
                  label=_('show'),
                  default=_('text'),
                  prim_name='show',
                  help_string=_('draws text or show media from the Journal'))
        self.tw.lc._def_prim('show', 1, 
            lambda self, x: PLUGIN_DICTIONARY['show'](x, True))

        make_prim('showaligned',
                  style='basic-style-1arg',
                  label=_('show aligned'),
                  default=_('text'),
                  prim_name='showaligned',
                  help_string=_('draws text or show media from the Journal'))
        self.tw.lc._def_prim('showaligned', 1, 
            lambda self, x: PLUGIN_DICTIONARY['show'](x, False))

        # depreciated
        PLUGIN_DICTIONARY['write'] = self._prim_write
        make_prim('write',
                  style='basic-style-1arg',
                  label=_('show'),
                  default=[_('text'), 32],
                  prim_name='write',
                  help_string=_('draws text or show media from the Journal'))
        self.tw.lc._def_prim('write', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['write'](x, y))

        PLUGIN_DICTIONARY['setscale'] = self._prim_setscale
        make_prim('setscale',
                  palette='media',
                  style='basic-style-1arg',
                  label=_('set scale'),
                  prim_name='setscale',
                  default=33,
                  help_string=_('sets the scale of media'))
        self.tw.lc._def_prim('setscale', 1,
                             lambda self, x: PLUGIN_DICTIONARY['setscale'](x))

        PLUGIN_DICTIONARY['savepix'] = self._prim_save_picture
        make_prim('savepix',
                  palette='media',
                  style='basic-style-1arg',
                  label=_('save picture'),
                  prim_name='savepix',
                  default=_('picture name'),
                  help_string=_('saves a picture to the Sugar Journal'))
        self.tw.lc._def_prim('savepix', 1,
                             lambda self, x: PLUGIN_DICTIONARY['savepix'](x))

        PLUGIN_DICTIONARY['savesvg'] = self._prim_save_svg
        make_prim('savesvg',
                  palette='media',
                  style='basic-style-1arg',
                  label=_('save SVG'),
                  prim_name='savesvg',
                  default=_('picture name'),
                  help_string=_('saves turtle graphics as an SVG file in the \
Sugar Journal'))
        self.tw.lc._def_prim('savesvg', 1,
                             lambda self, x: PLUGIN_DICTIONARY['savesvg'](x))

        make_prim('scale',
                  palette='media',
                  style='box-style',
                  label=_('scale'),
                  prim_name='scale',
                  value_block=True,
                  help_string=_('holds current scale value'))
        self.tw.lc._def_prim('scale', 0, lambda self: self.tw.lc.scale)

        make_prim('mediawait',
                  palette='media',
                  style='basic-style-extended-vertical',
                  label=_('media wait'),
                  prim_name='mediawait',
                  help_string=_('wait for current video or audio to complete'))
        self.tw.lc._def_prim('mediawait', 0, self.tw.lc._media_wait, True)

    def _sensor_palette(self):

        PLUGIN_DICTIONARY['kbinput'] = self._prim_kbinput
        make_prim('kbinput',
                  palette='sensor',
                  style='basic-style-extended-vertical',
                  label=_('query keyboard'),
                  prim_name='kbinput',
                  help_string=_('query for keyboard input (results stored in \
keyboard block)'))
        self.tw.lc._def_prim('kbinput', 0, 
                             lambda self: PLUGIN_DICTIONARY['kbinput']())


        make_prim('keyboard',
                  palette='sensor',
                  style='box-style',
                  label=_('keyboard'),
                  prim_name='keyboard',
                  value_block=True,
                  help_string=_('holds results of query-keyboard block'))
        self.tw.lc._def_prim('keyboard', 0, lambda self: self.tw.lc.keyboard)

        PLUGIN_DICTIONARY['readpixel'] = self._prim_readpixel
        make_prim('readpixel',
                  palette='sensor',
                  style='basic-style-extended-vertical',
                  label=_('read pixel'),
                  prim_name='readpixel',
                  help_string=_('RGB color under the turtle is pushed to the \
stack'))
        self.tw.lc._def_prim('readpixel', 0, 
                             lambda self: PLUGIN_DICTIONARY['readpixel']())

        PLUGIN_DICTIONARY['see'] = self._prim_see
        make_prim('see',
                  palette='sensor',
                  style='box-style',
                  label=_('turtle sees'),
                  prim_name='see',
                  help_string=_('returns the color that the turtle "sees"'))
        self.tw.lc._def_prim('see', 0, 
                             lambda self: PLUGIN_DICTIONARY['see']())

        PLUGIN_DICTIONARY['time'] = self._prim_time
        make_prim('time',
                  palette='sensor',
                  style='box-style',
                  label=_('time'),
                  prim_name='time',
                  value_block=True,
                  help_string=_('elapsed time (in seconds) since program \
started'))
        self.tw.lc._def_prim('time', 0, 
                             lambda self: PLUGIN_DICTIONARY['time']())

    def _extras_palette(self):

        PLUGIN_DICTIONARY['push'] = self._prim_push
        make_prim('push',
                  palette='extras',
                  style='basic-style-1arg',
                  label=_('push'),
                  prim_name='push',
                  help_string=_('pushes value onto FILO (first-in last-out \
heap)'))
        self.tw.lc._def_prim('push', 1,
                             lambda self, x: PLUGIN_DICTIONARY['push'](x))

        PLUGIN_DICTIONARY['printheap'] = self._prim_printheap
        make_prim('printheap',
                  palette='extras',
                  style='basic-style-extended-vertical',
                  label=_('show heap'),
                  prim_name='printheap',
                  help_string=_('shows values in FILO (first-in last-out \
heap)'))
        self.tw.lc._def_prim('printheap', 0, 
                             lambda self: PLUGIN_DICTIONARY['printheap']())

        PLUGIN_DICTIONARY['clearheap'] = self._prim_emptyheap
        make_prim('clearheap',
                  palette='extras',
                  style='basic-style-extended-vertical',
                  label=_('empty heap'),
                  prim_name='clearheap',
                  help_string=_('emptys FILO (first-in-last-out heap)'))
        self.tw.lc._def_prim('clearheap', 0, 
                             lambda self: PLUGIN_DICTIONARY['clearheap']())

        PLUGIN_DICTIONARY['pop'] = self._prim_pop
        make_prim('pop',
                  palette='extras',
                  style='box-style',
                  label=_('pop'),
                  prim_name='pop',
                  value_block=True,
                  help_string=_('pops value off FILO (first-in last-out heap)'))
        self.tw.lc._def_prim('pop', 0, 
                             lambda self: PLUGIN_DICTIONARY['pop']())

        PLUGIN_DICTIONARY['print'] = self._prim_print
        make_prim('comment',
                  palette='extras',
                  style='basic-style-1arg',
                  label=_('comment'),
                  prim_name='comment',
                  default=_('comment'),
                  help_string=_('places a comment in your code'))
        self.tw.lc._def_prim('comment', 1,
            lambda self, x: PLUGIN_DICTIONARY['print'](x, True))

        make_prim('print',
                  palette='extras',
                  style='basic-style-1arg',
                  label=_('print'),
                  prim_name='print',
                  help_string=_('prints value in status block at bottom of \
the screen'))
        self.tw.lc._def_prim('print', 1,
            lambda self, x: PLUGIN_DICTIONARY['print'](x, False))

        PLUGIN_DICTIONARY['myfunction'] = self._prim_myfunction
        make_prim('myfunc1arg',
                  palette='extras',
                  style='number-style-var-arg',
                  label=[_('Python'), 'f(x)', 'x'],
                  prim_name='myfunction',
                  default=['x', 100],
                  help_string=_('a programmable block: used to add advanced \
single-variable math equations, e.g., sin(x)'))
        self.tw.lc._def_prim('myfunction', 2,
            lambda self, f, x: PLUGIN_DICTIONARY['myfunction'](f, [x]))

        make_prim('myfunc2arg',
                  style='number-style-var-arg',
                  label=[_('Python'), 'f(x,y)', 'x'],
                  prim_name='myfunction2',
                  default=['x+y', 100, 100],
                  help_string=_('a programmable block: used to add advanced \
multi-variable math equations, e.g., sqrt(x*x+y*y)'))
        self.tw.lc._def_prim('myfunction2', 3,
            lambda self, f, x: PLUGIN_DICTIONARY['myfunction'](f, [x, y]))

        make_prim('myfunc3arg',
                  style='number-style-var-arg',
                  label=[_('Python'), 'f(x,y,z)', 'x'],
                  prim_name='myfunction3',
                  default=['x+y+z', 100, 100, 100],
                  help_string=_('a programmable block: used to add advanced \
multi-variable math equations, e.g., sin(x+y+z)'))
        self.tw.lc._def_prim('myfunction3', 4,
            lambda self, f, x, y, z: PLUGIN_DICTIONARY['myfunction'](
                f, [x, y, z]))

        PLUGIN_DICTIONARY['userdefined'] = self._prim_myblock
        make_prim('userdefined',
                  palette='extras',
                  style='basic-style-var-arg',
                  label=' ',
                  prim_name='userdefined',
                  special_name=_('Python block'),
                  default=100,
                  help_string=_('runs code found in the tamyblock.py module \
found in the Journal'))
        self.tw.lc._def_prim('userdefined', 1,
            lambda self, x: PLUGIN_DICTIONARY['userdefined']([x]))

        make_prim('userdefined2args',
                  style='basic-style-var-arg',
                  label=' ',
                  prim_name='userdefined2',
                  special_name=_('Python block'),
                  default=[100, 100],
                  help_string=_('runs code found in the tamyblock.py module \
found in the Journal'))
        self.tw.lc._def_prim('userdefined2', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['userdefined']([x, y]))

        make_prim('userdefined3args',
                  style='basic-style-var-arg',
                  label=' ',
                  prim_name='userdefined3',
                  special_name=_('Python block'),
                  default=[100, 100, 100],
                  help_string=_('runs code found in the tamyblock.py module \
found in the Journal'))
        self.tw.lc._def_prim('userdefined3', 3,
            lambda self, x, y, z: PLUGIN_DICTIONARY['userdefined']([x, y, z]))

        make_prim('cartesian',
                  palette='extras',
                  style='basic-style-extended-vertical',
                  label=_('Cartesian'),
                  prim_name='cartesian',
                  help_string=_('displays Cartesian coordinates'))
        self.tw.lc._def_prim('cartesian', 0,
                             lambda self: self.tw.set_cartesian(True))

        make_prim('polar',
                  palette='extras',
                  style='basic-style-extended-vertical',
                  label=_('polar'),
                  prim_name='polar',
                  help_string=_('displays polar coordinates'))
        self.tw.lc._def_prim('polar', 0, 
                             lambda self: self.tw.set_polar(True))

        make_prim('addturtle',
                  palette='extras',
                  style='basic-style-1arg',
                  label=_('turtle'),
                  prim_name='turtle',
                  default=1,
                  help_string=_('chooses which turtle to command'))
        self.tw.lc._def_prim('turtle', 1,
            lambda self, x: self.tw.canvas.set_turtle(x))

        PLUGIN_DICTIONARY['skin'] = self._prim_reskin
        make_prim('skin',
                  style='basic-style-1arg',
                  label=_('turtle shell'),
                  prim_name='skin',
                  help_string=_("put a custom 'shell' on the turtle"))
        self.tw.lc._def_prim('skin', 1,
            lambda self, x: PLUGIN_DICTIONARY['skin'](x))

        # macro
        make_prim('reskin',
                  palette='extras',
                  style='basic-style-1arg',
                  label=_('turtle shell'),
                  help_string=_("put a custom 'shell' on the turtle"))

        make_prim('sandwichtop_no_label',
                  palette='extras',
                  style='collapsible-top-no-label',
                  label=[' ', ' '],
                  special_name=_('top'),
                  prim_name='nop',
                  help_string=_('top of a collapsed stack'))

        make_prim('sandwichbottom',
                  palette='extras',
                  style='collapsible-bottom',
                  label=[' ', ' '],
                  prim_name='nop',
                  special_name=_('bottom'),
                  help_string=_('bottom of a collapsible stack'))

        make_prim('sandwichcollapsed',
                  style='invisible',
                  label=' ',
                  prim_name='nop',
                  help_string=_('bottom block in a collapsed stack: click to \
open'))

        # depreciated blocks
        make_prim('sandwichtop',
                  style='collapsible-top',
                  label=_('top of stack'),
                  default=_('label'),
                  prim_name='comment',
                  help_string=_('top of stack'))

        make_prim('sandwichtop_no_arm',
                  style='collapsible-top-no-arm',
                  label=_('top of a collapsible stack'),
                  default=_('label'),
                  prim_name='comment',
                  help_string=_('top of stack'))

        make_prim('sandwichtop_no_arm_no_label',
                  style='collapsible-top-no-arm-no-label',
                  label=[' ', _('click to open')],
                  prim_name='nop',
                  help_string=_('top of stack'))

    def _portfolio_palette(self):

        make_prim('hideblocks',
                  palette='portfolio',
                  style='basic-style-extended-vertical',
                  label=_('hide blocks'),
                  prim_name='hideblocks',
                  help_string=_('declutters canvas by hiding blocks'))
        self.tw.lc._def_prim('hideblocks', 0, lambda self: self.tw.hideblocks())

        make_prim('showblocks',
                  palette='portfolio',
                  style='basic-style-extended-vertical',
                  label=_('show blocks'),
                  prim_name='showblocks',
                  help_string=_('restores hidden blocks'))
        self.tw.lc._def_prim('showblocks', 0, lambda self: self.tw.showblocks())

        make_prim('fullscreen',
                  palette='portfolio',
                  style='basic-style-extended-vertical',
                  label=_('full screen'),
                  prim_name='fullscreen',
                  help_string=_('hides the Sugar toolbars'))
        self.tw.lc._def_prim('fullscreen', 0,
                             lambda self: self.tw.set_fullscreen())

        PLUGIN_DICTIONARY['bulletlist'] = self._prim_list
        make_prim('list',
                  style='bullet-style',
                  label=_('list'),
                  prim_name='bulletlist',
                  default=['∙ ', '∙ '],
                  help_string=_('presentation bulleted list'))
        self.tw.lc._def_prim('bulletlist', 1,
                             PLUGIN_DICTIONARY['bulletlist'], True)

        # macros
        make_prim('picturelist',
                  palette='portfolio',
                  style='basic-style-extended',
                  label=' ',
                  help_string=_('presentation template: list of bullets'))

        make_prim('picture1x1a',
                  palette='portfolio',
                  style='basic-style-extended',
                  label=' ',
                  help_string=_('presentation template: select Journal object \
(no description)'))

        make_prim('picture1x1',
                  palette='portfolio',
                  style='basic-style-extended',
                  label=' ',
                  help_string=_('presentation template: select Journal object \
(with description)'))

        make_prim('picture2x2',
                  palette='portfolio',
                  style='basic-style-extended',
                  label=' ',
                  help_string=_('presentation template: select four Journal \
objects'))

        make_prim('picture2x1',
                  palette='portfolio',
                  style='basic-style-extended',
                  label=' ',
                  help_string=_('presentation template: select two Journal \
objects'))

        make_prim('picture1x2',
                  palette='portfolio',
                  style='basic-style-extended',
                  label=' ',
                  help_string=_('presentation template: select two Journal \
objects'))

        # Display-dependent constants
        make_prim('leftpos',
                  palette='portfolio',
                  style='box-style',
                  label=_('left'),
                  prim_name='lpos',
                  help_string=_('xcor of left of screen'))
        self.tw.lc._def_prim('lpos', 0, lambda self: CONSTANTS['leftpos'])

        make_prim('bottompos',
                  palette='portfolio',
                  style='box-style',
                  label=_('bottom'),
                  prim_name='bpos',
                  help_string=_('ycor of bottom of screen'))
        self.tw.lc._def_prim('bpos', 0, lambda self: CONSTANTS['bottompos'])

        make_prim('width',
                  palette='portfolio',
                  style='box-style',
                  label=_('width'),
                  prim_name='hres',
                  help_string=_('the canvas width'))
        self.tw.lc._def_prim('hres', 0, lambda self: CONSTANTS['width'])

        make_prim('rightpos',
                  palette='portfolio',
                  style='box-style',
                  label=_('right'),
                  prim_name='rpos',
                  help_string=_('xcor of right of screen'))
        self.tw.lc._def_prim('rpos', 0, lambda self: CONSTANTS['rightpos'])

        make_prim('toppos',
                  palette='portfolio',
                  style='box-style',
                  label=_('top'),
                  prim_name='tpos',
                  help_string=_('ycor of top of screen'))
        self.tw.lc._def_prim('tpos', 0, lambda self: CONSTANTS['toppos'])

        make_prim('height',
                  palette='portfolio',
                  style='box-style',
                  label=_('height'),
                  prim_name='vres',
                  help_string=_('the canvas height'))
        self.tw.lc._def_prim('vres', 0, lambda self: CONSTANTS['height'])

        make_prim('titlex',
                  style='box-style',
                  label=_('title x'),
                  prim_name='titlex')
        self.tw.lc._def_prim('titlex', 0, lambda self: CONSTANTS['titlex'])

        make_prim('titley',
                  style='box-style',
                  label=_('title y'),
                  prim_name='titley')
        self.tw.lc._def_prim('titley', 0, lambda self: CONSTANTS['titley'])

        make_prim('leftx',
                  style='box-style',
                  label=_('left x'),
                  prim_name='leftx')
        self.tw.lc._def_prim('leftx', 0, lambda self: CONSTANTS['leftx'])

        make_prim('topy',
                  style='box-style',
                  label=_('top y'),
                  prim_name='topy')
        self.tw.lc._def_prim('topy', 0, lambda self: CONSTANTS['topy'])

        make_prim('rightx',
                  style='box-style',
                  label=_('right x'),
                  prim_name='rightx')
        self.tw.lc._def_prim('rightx', 0, lambda self: CONSTANTS['rightx'])

        make_prim('bottomy',
                  style='box-style',
                  label=_('bottom y'),
                  prim_name='bottomy')
        self.tw.lc._def_prim('bottomy', 0, lambda self: CONSTANTS['bottomy'])

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
        self.tw.lc._ireturn()
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
               n[6:].lower not in MEDIA_BLOCKS_DICTIONARY:
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
        self.tw.showlabel('status', str(self.tw.lc.heap) + '      ')

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
            print self.tw.lc.filepath, scale, scale
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
                print string[6:], MEDIA_BLOCKS_DICTIONARY
                if string[6:].lower() in MEDIA_BLOCKS_DICTIONARY:
                    MEDIA_BLOCKS_DICTIONARY[string[6:].lower()]()
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
                    self.tw.lc._insert_image(center)
                elif string[0:6] == 'descr_':
                    mimetype = None
                    if self.tw.lc.dsobject is not None and \
                       'mime_type' in self.tw.lc.dsobject.metadata:
                        mimetype = self.tw.lc.dsobject.metadata['mime_type']
                    description = None
                    if self.tw.lc.dsobject is not None and \
                       'description' in self.tw.lc.dsobject.metadata:
                        description = self.tw.lc.dsobject.metadata['description']
                    self.tw.lc._insert_desc(mimetype, description)
                elif string[0:6] == 'audio_':
                    self.tw.lc._play_sound()
                elif string[0:6] == 'video_':
                    self.tw.lc._play_video()
                if self.tw.lc.dsobject is not None:
                    self.tw.lc.dsobject.destroy()
            else:  # assume it is text to display
                x, y = self.tw.lc._x(), self.tw.lc._y()
                if center:
                    y -= self.tw.canvas.textsize
                self.tw.canvas.draw_text(string, x, y,
                                         int(self.tw.canvas.textsize * \
                                             self.tw.lc.scale / 100.),
                                         self.tw.canvas.width - x)
        elif type(string) == float or type(string) == int:
            string = round_int(string)
            x, y = self.tw.lc._x(), self.tw.lc._y()
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
        elapsed_time = int(time() - self.tw.lc._start_time)
        self.tw.lc.update_label_value('time', elapsed_time)
        return elapsed_time

    # Depreciated blocks
    # TODO: reinstate these blocks
    """
PORTFOLIO_STYLE_2x2 = ['template2x2']
PORTFOLIO_STYLE_1x1 = ['template1x1', 'template1x1a']
PORTFOLIO_STYLE_2x1 = ['template2x1']
PORTFOLIO_STYLE_1x2 = ['template1x2']
    'template1x1': [' '],
    'template1x1a': [' '],
    'template1x2': [' '],
    'template2x1': [' '],
    'template2x2': [' '],
    'templatelist': [' '],
    'template1x1': 't1x1',
    'template1x1a': 't1x1a',
    'template1x2': 't1x2',
    'template2x1': 't2x1',
    'template2x2': 't2x2',
    'templatelist': 'bullet',

        't1x1': [2, lambda self, x, y: self._show_template1x1(x, y)],
        't1x1a': [2, lambda self, x, y: self._show_template1x1a(x, y)],
        't1x2': [3, lambda self, x, y, z: self._show_template1x2(x, y, z)],
        't2x1': [3, lambda self, x, y, z: self._show_template2x1(x, y, z)],
        't2x2': [5, lambda self, x, y, z, a, b: self._show_template2x2(
                    x, y, z, a, b)],
    'template1x1': [_('Title'), 'None'],
    'template1x1a': [_('Title'), 'None'],
    'template1x2': [_('Title'), 'None', 'None'],
    'template2x1': [_('Title'), 'None', 'None'],
    'template2x2': [_('Title'), 'None', 'None', 'None', 'None'],
    'templatelist': [_('Title'), '∙ '],

    'template1x1a': _('presentation 1x1'),
    'template1x2': _('presentation 1x2'),
    'template2x1': _('presentation 2x1'),
    'template2x2': _('presentation 2x2'),
    'templatelist': _('presentation bulleted list'),
    'template1x1': _(
        "presentation template: select Journal object (with description)"),
    'template1x1a': _(
        "presentation template: select Journal object (no description)"),
    'template1x2': _("presentation template: select two Journal objects"),
    'template2x1': _("presentation template: select two Journal objects"),
    'template2x2': _("presentation template: select four Journal objects"),
    'templatelist': _("presentation template: list of bullets"),
    """

    def _show_template1x1(self, title, media):
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
        self.tw.canvas.settextsize(self.body_height)
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

    def _show_template2x1(self, title, media1, media2):
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
        self.tw.canvas.settextsize(self.body_height)
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

    def _show_bullets(self, sarray):
        """ title and varible number of  bullets """
        xo = self.tw.calc_position('bullet')[2]
        x = -(self.tw.canvas.width / 2) + xo
        y = self.tw.canvas.height / 2
        self.tw.canvas.setxy(x, y, pendown=False)
        # save the text size so we can restore it later
        save_text_size = self.tw.canvas.textsize
        # set title text
        self.tw.canvas.settextsize(self.title_height)
        self._prim_show(sarray[0])
        # set body text size
        self.tw.canvas.settextsize(self.bullet_height)
        # leave some space below the title
        y -= int(self.title_height * 2 * self.tw.lead)
        for s in sarray[1:]:
            self.tw.canvas.setxy(x, y, pendown=False)
            self._prim_show(s)
            y -= int(self.bullet_height * 2 * self.tw.lead)
        # restore text size
        self.tw.canvas.settextsize(save_text_size)

    def _show_template1x2(self, title, media1, media2):
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
        self.tw.canvas.settextsize(self.body_height)
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

    def _show_template2x2(self, title, media1, media2, media3, media4):
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
        self.tw.canvas.settextsize(self.body_height)
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

    def _show_template1x1a(self, title, media1):
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
        self.tw.canvas.settextsize(self.body_height)
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
