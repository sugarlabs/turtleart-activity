from plugins.plugin import Plugin
from gettext import gettext as _
import plugins.rpi.functions as fns
from TurtleArt.taprimitive import (ArgSlot, Primitive)
from TurtleArt.tatype import TYPE_NUMBER,TYPE_OBJECT,TYPE_BOOL
from TurtleArt.tawindow import TurtleArtWindow
from TurtleArt.tapalette import (make_palette, define_logo_function)
from gi.repository import GObject

import logging
_logger = logging.getLogger('turtleart-activity RPi plugin')


class Rpi(Plugin):
    def __init__(self, parent: TurtleArtWindow):
        Plugin.__init__(self)
        self._parent = parent
        self.running_sugar = self._parent.running_sugar

    def setup(self):
        palette = make_palette('RaspberryPi',
                               colors=["#abe6ff", "#008080"],
                               help_string=_('Palette of RPi pins'),
                               position=6)

        # palette.add_block('setup', style='clamp-style', label='setup  ')
        # palette.add_block('loop', style='clamp-style', label='loop  ')
        # palette.add_block('def_func', style='clamp-style', label='function')


# Digital Output
        palette.add_block('digitalWrite',
                          style='basic-style-2arg',
                          label=[_('GPIO'), _('set'), _('to')],
                          default='Dx',
                          prim_name='digitalWrite',
                          help_string=_('sets pin to high/low'),
                          logo_command='digitalWrite')
        self._parent.lc.def_prim(
            'digitalWrite', 2,
            Primitive(fns.digitalWrite,
                arg_descs=[ArgSlot(TYPE_OBJECT),ArgSlot(TYPE_NUMBER)]
            ))
# Digital Input
        palette.add_block('digitalRead',
                          style='basic-style-1arg',
                          label=['GPIO\t\t', 'read'],
                          default='Dx',
                          prim_name='digitalRead',
                          help_string=_('sets pin to high/low'),
                          logo_command='digitalRead')
        self._parent.lc.def_prim(
            'digitalRead', 1,
            Primitive(fns.digitalRead,
                arg_descs=ArgSlot(TYPE_OBJECT),return_type=TYPE_BOOL
            ))

# Delay
        palette.add_block('delay',style='basic-style-1arg',\
label='delay (ms)', prim_name='delay',logo_command='delay', default=1000)
        self._parent.lc.def_prim('delay', 1, Primitive(fns.delay,\
arg_descs=ArgSlot(TYPE_NUMBER)))


# Button
        palette.add_block('btn',
                          style='boolean-1arg-block-style',
                          label=_('button'),
                          prim_name='btn',
                          default='Dx',
                          help_string=_('sets pin to high/low'),
                          logo_command='btn')
        self._parent.lc.def_prim('btn', 1, Primitive(fns.btn,
                               return_type=TYPE_BOOL,
                               arg_descs=([ArgSlot(TYPE_OBJECT)])))
        

# HIGH/LOW Blocks
        palette.add_block('high',
                          style='box-style',
                          label=_('HIGH'),
                          prim_name='high',
                          help_string=_('toggles gpio pin high'))
        def _high():
            return 1
        self._parent.lc.def_prim('high', 0,
                                  Primitive(_high,return_type=TYPE_NUMBER))

        palette.add_block('low',
                          style='box-style',
                          label=_('LOW'),
                          prim_name='low',
                          help_string=_('toggles gpio pin low'))
        def _low():
            return 0
        self._parent.lc.def_prim('low', 0,
                                 Primitive(_low, return_type=TYPE_NUMBER))

# HC-SR04 distance sensor
        palette.add_block('dist', 
                            style='box-style',
                            prim_name='dist',
                            label='distance')
        self._parent.lc.def_prim('dist', 0,
                                 Primitive(fns.dist.dst,
                                           return_type=TYPE_NUMBER))

        palette.add_block('def_dist',
                          style='basic-style-2arg',
                          label=['HCSR04', 'trig pin', 'echo pin'],
                          default=['Dx','Dx'],
                          prim_name='def_dist',
                          help_string=_('measure distance using HC-SR04,\
                              distance sensor'))
        self._parent.lc.def_prim('def_dist', 2,
                                 Primitive(fns.dist.def_dist,
                                           arg_descs=([ArgSlot(TYPE_OBJECT),
                                          ArgSlot(TYPE_OBJECT)])))

# String editable blocks
        # palette.add_block('string',
        #                   style='box-style',
        #                   help_string=_('text'))

# OLED-Display
        palette.add_block('define_oled_display', style='basic-style-3arg', 
                                label=[_('OLED\t\t'), _('height'),
                                _('width'),_('text color\n(0 or 1) ')],
                                default=[128,32,1],
                                prim_name='define_oled_display',
                                logo_command='define_oled_display')
        self._parent.lc.def_prim('define_oled_display', 3,
                            Primitive(fns.oled.define,
                            arg_descs=([ArgSlot(TYPE_NUMBER),
                                        ArgSlot(TYPE_NUMBER),
                                        ArgSlot(TYPE_NUMBER)])))

        palette.add_block('oled_print', style='basic-style-1arg',
                            default='text',
                            label='Display', prim_name='oled_print',)
        self._parent.lc.def_prim('oled_print', 1,
                Primitive(fns.oled.print,
                          arg_descs=([ArgSlot(TYPE_OBJECT)])))
