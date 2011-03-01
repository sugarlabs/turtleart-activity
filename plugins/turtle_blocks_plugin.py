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
from TurtleArt.taprimitive import Palette, Primitive
from TurtleArt.talogo import PLUGIN_DICTIONARY, logoerror, \
    MEDIA_BLOCKS_DICTIONARY
from TurtleArt.taconstants import DEFAULT_SCALE, CONSTANTS, BLACK, WHITE, \
    ICON_SIZE
from TurtleArt.tautils import convert, round_int, debug_output
from TurtleArt.tajail import myfunc, myfunc_import

# TODO: add expandibles to taprimitives
#       fix position problem


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
        b = Primitive('while')  # macro
        b.set_palette('flow')
        b.set_style('flow-style-boolean')
        b.set_label(_('while'))
        b.set_help(_('do-while-True operator that uses boolean operators from Numbers palette'))
        b.add_prim()

        b = Primitive('until')  # macro
        b.set_palette('flow')
        b.set_style('flow-style-boolean')
        b.set_label(_('until'))
        b.set_help(_('do-until-True operator that uses boolean operators from Numbers palette'))
        b.add_prim()

    def _media_palette(self):
        b = Primitive('journal')
        b.set_palette('media')
        b.set_style('box-style-media')
        b.set_label(' ')
        b.set_special_name(_('journal'))
        b.set_default(None)
        b.set_help(_('Sugar Journal media object'))
        b.add_prim()

        b = Primitive('audio')
        b.set_palette('media')
        b.set_style('box-style-media')
        b.set_label(' ')
        b.set_special_name(_('audio'))
        b.set_default(None)
        b.set_help(_('Sugar Journal audio object'))
        b.add_prim()

        b = Primitive('video')
        b.set_palette('media')
        b.set_style('box-style-media')
        b.set_label(' ')
        b.set_special_name(_('video'))
        b.set_default(None)
        b.set_help(_('Sugar Journal video object'))
        b.add_prim()

        b = Primitive('description')
        b.set_palette('media')
        b.set_style('box-style-media')
        b.set_label(' ')
        b.set_special_name(_('description'))
        b.set_default(None)
        b.set_help(_('Sugar Journal description field'))
        b.add_prim()

        b = Primitive('string')
        b.set_palette('media')
        b.set_style('box-style')
        b.set_label(_('text'))
        b.set_default(_('text'))
        b.set_special_name('')
        b.set_help('string value')
        b.add_prim()

        b = Primitive('show')
        b.set_palette('media')
        b.set_style('basic-style-1arg')
        b.set_label(_('show'))
        b.set_default(_('text'))
        b.set_prim_name('show')
        b.set_help(_('draws text or show media from the Journal'))
        PLUGIN_DICTIONARY['show'] = self._prim_show
        self.tw.lc._def_prim('show', 1, 
            lambda self, x: PLUGIN_DICTIONARY['show'](x, True))
        b.add_prim()

        b = Primitive('showaligned')
        b.set_style('basic-style-1arg')
        b.set_label(_('show aligned'))
        b.set_default(_('text'))
        b.set_prim_name('showaligned')
        b.set_help(_('draws text or show media from the Journal'))
        self.tw.lc._def_prim('showaligned', 1, 
            lambda self, x: PLUGIN_DICTIONARY['show'](x, False))
        b.add_prim()

        b = Primitive('setscale')
        b.set_palette('media')
        b.set_style('basic-style-1arg')
        b.set_label(_('set scale'))
        b.set_prim_name('setscale')
        b.set_default(33)
        b.set_help(_('sets the scale of media'))
        PLUGIN_DICTIONARY['setscale'] = self._prim_setscale
        self.tw.lc._def_prim('setscale', 1,
                             lambda self, x: PLUGIN_DICTIONARY['setscale'](x))

        b.add_prim()

        b = Primitive('savepix')
        b.set_palette('media')
        b.set_style('basic-style-1arg')
        b.set_label(_('save picture'))
        b.set_prim_name('savepix')
        b.set_default(_('picture name'))
        b.set_help(_('saves a picture to the Sugar Journal'))
        PLUGIN_DICTIONARY['savepix'] = self._prim_save_picture
        self.tw.lc._def_prim('savepix', 1,
                             lambda self, x: PLUGIN_DICTIONARY['savepix'](x))
        b.add_prim()

        b = Primitive('savesvg')
        b.set_palette('media')
        b.set_style('basic-style-1arg')
        b.set_label(_('save SVG'))
        b.set_prim_name('savesvg')
        b.set_default(_('picture name'))
        b.set_help(_('saves turtle graphics as an SVG file in the Sugar Journal'))
        PLUGIN_DICTIONARY['savesvg'] = self._prim_save_svg
        self.tw.lc._def_prim('savesvg', 1,
                             lambda self, x: PLUGIN_DICTIONARY['savesvg'](x))
        b.add_prim()

        b = Primitive('scale')
        b.set_palette('media')
        b.set_style('box-style')
        b.set_label(_('scale'))
        b.set_prim_name('scale')
        b.set_value_block(True)
        b.set_help(_('holds current scale value'))
        self.tw.lc._def_prim('scale', 0, lambda self: self.tw.lc.scale)
        b.add_prim()

        b = Primitive('mediawait')
        b.set_palette('media')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('media wait'))
        b.set_prim_name('mediawait')
        b.set_help(_('wait for current video or audio to complete'))
        self.tw.lc._def_prim('mediawait', 0, self.tw.lc._media_wait, True)
        b.add_prim()

    def _sensor_palette(self):
        b = Primitive('kbinput')
        b.set_palette('sensor')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('query keyboard'))
        b.set_prim_name('kbinput')
        b.set_help(_('query for keyboard input (results stored in keyboard block)'))
        PLUGIN_DICTIONARY['kbinput'] = self._prim_kbinput
        self.tw.lc._def_prim('kbinput', 0, 
                             lambda self: PLUGIN_DICTIONARY['kbinput']())
        b.add_prim()

        b = Primitive('keyboard')
        b.set_palette('sensor')
        b.set_style('box-style')
        b.set_label(_('keyboard'))
        b.set_prim_name('keyboard')
        b.set_value_block(True)
        b.set_help(_('holds results of query-keyboard block'))
        self.tw.lc._def_prim('keyboard', 0, lambda self: self.tw.lc.keyboard)
        b.add_prim()

        b = Primitive('readpixel')
        b.set_palette('sensor')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('read pixel'))
        b.set_prim_name('readpixel')
        b.set_help(_('RGB color under the turtle is pushed to the stack'))
        PLUGIN_DICTIONARY['readpixel'] = self._prim_readpixel
        self.tw.lc._def_prim('readpixel', 0, 
                             lambda self: PLUGIN_DICTIONARY['readpixel']())
        b.add_prim()

        b = Primitive('see')
        b.set_palette('sensor')
        b.set_style('box-style')
        b.set_label(_('turtle sees'))
        b.set_prim_name('see')
        b.set_help(_('returns the color that the turtle "sees"'))
        b.set_value_block(True)
        PLUGIN_DICTIONARY['see'] = self._prim_see
        self.tw.lc._def_prim('see', 0, 
                             lambda self: PLUGIN_DICTIONARY['see']())
        b.add_prim()

        b = Primitive('time')
        b.set_palette('sensor')
        b.set_style('box-style')
        b.set_label(_('time'))
        b.set_prim_name('time')
        b.set_value_block(True)
        b.set_help(_('elapsed time (in seconds) since program started'))
        PLUGIN_DICTIONARY['time'] = self._prim_time
        self.tw.lc._def_prim('time', 0, 
                             lambda self: PLUGIN_DICTIONARY['time']())
        b.add_prim()

    def _extras_palette(self):
        b = Primitive('push')
        b.set_palette('extras')
        b.set_style('basic-style-1arg')
        b.set_label(_('push'))
        b.set_prim_name('push')
        b.set_help(_('pushes value onto FILO (first-in last-out heap)'))
        PLUGIN_DICTIONARY['push'] = self._prim_push
        self.tw.lc._def_prim('push', 1,
                             lambda self, x: PLUGIN_DICTIONARY['push'](x))
        b.add_prim()

        b = Primitive('printheap')
        b.set_palette('extras')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('show heap'))
        b.set_prim_name('printheap')
        b.set_help(_('shows values in FILO (first-in last-out heap)'))
        PLUGIN_DICTIONARY['printheap'] = self._prim_printheap
        self.tw.lc._def_prim('printheap', 0, 
                             lambda self: PLUGIN_DICTIONARY['printheap']())
        b.add_prim()

        b = Primitive('clearheap')
        b.set_palette('extras')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('empty heap'))
        b.set_prim_name('clearheap')
        b.set_help(_('emptys FILO (first-in-last-out heap)'))
        PLUGIN_DICTIONARY['clearheap'] = self._prim_emptyheap
        self.tw.lc._def_prim('clearheap', 0, 
                             lambda self: PLUGIN_DICTIONARY['clearheap']())
        b.add_prim()

        b = Primitive('pop')
        b.set_palette('extras')
        b.set_style('box-style')
        b.set_label(_('pop'))
        b.set_prim_name('pop')
        b.set_value_block(True)
        b.set_help(_('pops value off FILO (first-in last-out heap)'))
        PLUGIN_DICTIONARY['pop'] = self._prim_pop
        self.tw.lc._def_prim('pop', 0, 
                             lambda self: PLUGIN_DICTIONARY['pop']())
        b.add_prim()

        b = Primitive('comment')
        b.set_palette('extras')
        b.set_style('basic-style-1arg')
        b.set_label(_('comment'))
        b.set_prim_name('comment')
        b.set_default(_('comment'))
        b.set_help(_('places a comment in your code'))
        PLUGIN_DICTIONARY['print'] = self._prim_print
        self.tw.lc._def_prim('comment', 1,
            lambda self, x: PLUGIN_DICTIONARY['print'](x, True))
        b.add_prim()

        b = Primitive('print')
        b.set_palette('extras')
        b.set_style('basic-style-1arg')
        b.set_label(_('print'))
        b.set_prim_name('print')
        b.set_help(_('prints value in status block at bottom of the screen'))
        self.tw.lc._def_prim('print', 1,
            lambda self, x: PLUGIN_DICTIONARY['print'](x, False))
        b.add_prim()

        b = Primitive('myfunc1arg')
        b.set_palette('extras')
        b.set_style('number-style-var-arg')
        b.set_label([_('Python'), 'f(x)', 'x'])
        b.set_prim_name('myfunction')
        b.set_default(['x', 100])
        b.set_help(_('a programmable block: used to add advanced single-variable math equations, e.g., sin(x)'))
        PLUGIN_DICTIONARY['myfunction'] = self._prim_myfunction
        self.tw.lc._def_prim('myfunction', 2,
            lambda self, f, x: PLUGIN_DICTIONARY['myfunction'](f, [x]))
        b.add_prim()

        b = Primitive('myfunc2arg')
        b.set_style('number-style-var-arg')
        b.set_label([_('Python'), 'f(x,y)', 'x'])
        b.set_prim_name('myfunction2')
        b.set_default(['x+y', 100, 100])
        b.set_help(_('a programmable block: used to add advanced multi-variable math equations, e.g., sqrt(x*x+y*y)'))
        self.tw.lc._def_prim('myfunction2', 3,
            lambda self, f, x: PLUGIN_DICTIONARY['myfunction'](f, [x, y]))
        b.add_prim()

        b = Primitive('myfunc3arg')
        b.set_style('number-style-var-arg')
        b.set_label([_('Python'), 'f(x,y,z)', 'x'])
        b.set_prim_name('myfunction3')
        b.set_default(['x+y+z', 100, 100, 100])
        b.set_help(_('a programmable block: used to add advanced multi-variable math equations, e.g., sin(x+y+z)'))
        self.tw.lc._def_prim('myfunction3', 4,
            lambda self, f, x, y, z: PLUGIN_DICTIONARY['myfunction'](
                f, [x, y, z]))
        b.add_prim()

        b = Primitive('userdefined')
        b.set_palette('extras')
        b.set_style('basic-style-var-arg')
        b.set_label(' ')
        b.set_prim_name('userdefined')
        b.set_special_name(_('Python block'))
        b.set_default(100)
        b.set_help(_('runs code found in the tamyblock.py module found in the Journal'))
        PLUGIN_DICTIONARY['userdefined'] = self._prim_myblock
        self.tw.lc._def_prim('userdefined', 1,
            lambda self, x: PLUGIN_DICTIONARY['userdefined']([x]))
        b.add_prim()

        b = Primitive('userdefined2')
        b.set_style('basic-style-var-arg')
        b.set_label(' ')
        b.set_prim_name('userdefined')
        b.set_special_name(_('Python block'))
        b.set_default([100, 100])
        b.set_help(_('runs code found in the tamyblock.py module found in the Journal'))
        self.tw.lc._def_prim('userdefined2', 2,
            lambda self, x, y: PLUGIN_DICTIONARY['userdefined']([x, y]))
        b.add_prim()

        b = Primitive('userdefined3')
        b.set_style('basic-style-var-arg')
        b.set_label(' ')
        b.set_prim_name('userdefined')
        b.set_special_name(_('Python block'))
        b.set_default([100, 100, 100])
        b.set_help(_('runs code found in the tamyblock.py module found in the Journal'))
        self.tw.lc._def_prim('userdefined3', 3,
            lambda self, x, y, z: PLUGIN_DICTIONARY['userdefined']([x, y, z]))
        b.add_prim()

        b = Primitive('cartesian')
        b.set_palette('extras')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('Cartesian'))
        b.set_prim_name('cartesian')
        b.set_help(_('displays Cartesian coordinates'))
        self.tw.lc._def_prim('cartesian', 0, 
                             lambda self: self.tw.set_cartesian(True))
        b.add_prim()

        b = Primitive('polar')
        b.set_palette('extras')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('polar'))
        b.set_prim_name('polar')
        b.set_help(_('displays polar coordinates'))
        self.tw.lc._def_prim('polar', 0, 
                             lambda self: self.tw.set_polar(True))
        b.add_prim()

        b = Primitive('addturtle')
        b.set_palette('extras')
        b.set_style('basic-style-1arg')
        b.set_label(_('turtle'))
        b.set_prim_name('turtle')
        b.set_default(1)
        b.set_help(_('chooses which turtle to command'))
        self.tw.lc._def_prim('turtle', 1,
            lambda self, x: self.tw.canvas.set_turtle(x))
        b.add_prim()

        b = Primitive('skin')
        b.set_style('basic-style-1arg')
        b.set_label(_('turtle shell'))
        b.set_prim_name('skin')
        b.set_help(_("put a custom 'shell' on the turtle"))
        PLUGIN_DICTIONARY['skin'] = self._prim_reskin
        self.tw.lc._def_prim('skin', 1,
            lambda self, x: PLUGIN_DICTIONARY['skin'](x))
        b.add_prim()

        b = Primitive('reskin')  # macro
        b.set_palette('extras')
        b.set_style('basic-style-1arg')
        b.set_label(_('turtle shell'))
        b.set_help(_("put a custom 'shell' on the turtle"))
        b.add_prim()

        b = Primitive('sandwichtop_no_label')
        b.set_palette('extras')
        b.set_style('collapsible-top-no-label')
        b.set_label([' ', ' '])
        b.set_prim_name('nop')
        b.set_help(_('top of a collapsed stack'))
        b.add_prim()

        b = Primitive('sandwichbottom')
        b.set_palette('extras')
        b.set_style('collapsible-bottom')
        b.set_label([' ', ' '])
        b.set_prim_name('nop')
        b.set_help(_('bottom of a collapsed stack'))
        b.add_prim()

        b = Primitive('sandwichcollapsed')
        b.set_style('invisible')
        b.set_label(' ')
        b.set_prim_name('nop')
        b.set_help(_('bottom block in a collapsed stack: click to open'))
        b.add_prim()

        b = Primitive('sandwichtop')  # depreciated
        b.set_style('collapsible-top')
        b.set_label(_('top of stack'))
        b.set_default(_('label'))
        b.set_prim_name('comment')
        b.set_help(_('top of stack'))
        b.add_prim()

        b = Primitive('sandwichtop_no_arm')  # depreciated
        b.set_style('collapsible-top-no-arm')
        b.set_label(_('top of a collapsible stack'))
        b.set_default(_('label'))
        b.set_prim_name('comment')
        b.set_help(_('top of stack'))
        b.add_prim()

        b = Primitive('sandwichtop_no_arm_no_label')  # depreciated
        b.set_style('collapsible-top-no-arm-no-label')
        b.set_label([' ', _('click to open')])
        b.set_prim_name('nop')
        b.set_help(_('top of stack'))
        b.add_prim()

    def _portfolio_palette(self):
        b = Primitive('hideblocks')
        b.set_palette('portfolio')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('hide blocks'))
        b.set_prim_name('hideblocks')
        b.set_help(_('declutters canvas by hiding blocks'))
        self.tw.lc._def_prim('hideblocks', 0, lambda self: self.tw.hideblocks())
        b.add_prim()

        b = Primitive('showblocks')
        b.set_palette('portfolio')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('show blocks'))
        b.set_prim_name('showblocks')
        b.set_help(_('restores hidden blocks'))
        self.tw.lc._def_prim('showblocks', 0, lambda self: self.tw.showblocks())
        b.add_prim()

        b = Primitive('fullscreen')
        b.set_palette('portfolio')
        b.set_style('basic-style-extended-vertical')
        b.set_label(_('full screen'))
        b.set_prim_name('fullscreen')
        b.set_help(_('hides the Sugar toolbars'))
        self.tw.lc._def_prim('fullscreen', 0,
                             lambda self: self.tw.set_fullscreen())
        b.add_prim()

        b = Primitive('picturelist')  # macro
        b.set_palette('portfolio')
        b.set_style('basic-style-extended')
        b.set_label(' ')
        b.set_help(_('presentation template: list of bullets'))
        b.add_prim()

        b = Primitive('picture1x1a')  # macro
        b.set_palette('portfolio')
        b.set_style('basic-style-extended')
        b.set_label(' ')
        b.set_help(_('presentation template: select Journal object (no description)'))
        b.add_prim()

        b = Primitive('picture1x1')  # macro
        b.set_palette('portfolio')
        b.set_style('basic-style-extended')
        b.set_label(' ')
        b.set_help(_('presentation template: select Journal object (with description)'))
        b.add_prim()

        b = Primitive('picture2x2')  # macro
        b.set_palette('portfolio')
        b.set_style('basic-style-extended')
        b.set_label(' ')
        b.set_help(_('presentation template: select four Journal objects'))
        b.add_prim()

        b = Primitive('picture2x1')  # macro
        b.set_palette('portfolio')
        b.set_style('basic-style-extended')
        b.set_label(' ')
        b.set_help(_('presentation template: select two Journal objects'))
        b.add_prim()

        b = Primitive('picture1x2')  # macro
        b.set_palette('portfolio')
        b.set_style('basic-style-extended')
        b.set_label(' ')
        b.set_help(_('presentation template: select two Journal objects'))
        b.add_prim()

        b = Primitive('leftpos')
        b.set_palette('portfolio')
        b.set_style('box-style')
        b.set_label(_('left'))
        b.set_prim_name('lpos')
        b.set_help(_('xcor of left of screen'))
        self.tw.lc._def_prim('lpos', 0, lambda self: CONSTANTS['leftpos'])
        b.add_prim()

        b = Primitive('bottompos')
        b.set_palette('portfolio')
        b.set_style('box-style')
        b.set_label(_('bottom'))
        b.set_prim_name('bpos')
        b.set_help(_('ycor of bottom of screen'))
        self.tw.lc._def_prim('bpos', 0, lambda self: CONSTANTS['bottompos'])
        b.add_prim()

        b = Primitive('width')
        b.set_palette('portfolio')
        b.set_style('box-style')
        b.set_label(_('width'))
        b.set_prim_name('hres')
        b.set_help(_('the canvas width'))
        self.tw.lc._def_prim('hres', 0, lambda self: CONSTANTS['width'])
        b.add_prim()

        b = Primitive('rightpos')
        b.set_palette('portfolio')
        b.set_style('box-style')
        b.set_label(_('right'))
        b.set_prim_name('rpos')
        b.set_help(_('xcor of right of screen'))
        self.tw.lc._def_prim('rpos', 0, lambda self: CONSTANTS['rightpos'])
        b.add_prim()

        b = Primitive('toppos')
        b.set_palette('portfolio')
        b.set_style('box-style')
        b.set_label(_('top'))
        b.set_prim_name('tpos')
        b.set_help(_('ycor of top of screen'))
        self.tw.lc._def_prim('tpos', 0, lambda self: CONSTANTS['toppos'])
        b.add_prim()

        b = Primitive('height')
        b.set_palette('portfolio')
        b.set_style('box-style')
        b.set_label(_('height'))
        b.set_prim_name('vres')
        b.set_help(_('the canvas height'))
        self.tw.lc._def_prim('vres', 0, lambda self: CONSTANTS['height'])
        b.add_prim()

        b = Primitive('titlex')
        b.set_style('box-style')
        b.set_label(_('title x'))
        b.set_prim_name('titlex')
        self.tw.lc._def_prim('titlex', 0, lambda self: CONSTANTS['titlex'])
        b.add_prim()

        b = Primitive('titley')
        b.set_style('box-style')
        b.set_label(_('title y'))
        b.set_prim_name('titley')
        self.tw.lc._def_prim('titley', 0, lambda self: CONSTANTS['titley'])
        b.add_prim()

        b = Primitive('leftx')
        b.set_style('box-style')
        b.set_label(_('left x'))
        b.set_prim_name('leftx')
        self.tw.lc._def_prim('leftx', 0, lambda self: CONSTANTS['leftx'])
        b.add_prim()

        b = Primitive('topy')
        b.set_style('box-style')
        b.set_label(_('top y'))
        b.set_prim_name('topy')
        self.tw.lc._def_prim('topy', 0, lambda self: CONSTANTS['topy'])
        b.add_prim()

        b = Primitive('rightx')
        b.set_style('box-style')
        b.set_label(_('right x'))
        b.set_prim_name('rightx')
        self.tw.lc._def_prim('rightx', 0, lambda self: CONSTANTS['rightx'])
        b.add_prim()

        b = Primitive('bottomy')
        b.set_style('box-style')
        b.set_label(_('bottom y'))
        b.set_prim_name('bottomy')
        self.tw.lc._def_prim('bottomy', 0, lambda self: CONSTANTS['bottomy'])
        b.add_prim()

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

    def _prim_time(self):
        """ Number of seconds since program execution has started or
        clean (prim_clear) block encountered """
        elapsed_time = int(time() - self.tw.lc._start_time)
        self.tw.lc.update_label_value('time', elapsed_time)
        return elapsed_time

    # Depreciated blocks

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
        'write': [2, lambda self, x, y: self._write(self, x, y)]
    'template1x1': [_('Title'), 'None'],
    'template1x1a': [_('Title'), 'None'],
    'template1x2': [_('Title'), 'None', 'None'],
    'template2x1': [_('Title'), 'None', 'None'],
    'template2x2': [_('Title'), 'None', 'None', 'None', 'None'],
    'templatelist': [_('Title'), '∙ '],
    'write': [_('text'), 32]}

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

    def _write(self, string, fsize):
        """ Write string at size """
        x = self.tw.canvas.width / 2 + int(self.tw.canvas.xcor)
        y = self.tw.canvas.height / 2 - int(self.tw.canvas.ycor)
        self.tw.canvas.draw_text(string, x, y - 15, int(fsize),
                                 self.tw.canvas.width)
