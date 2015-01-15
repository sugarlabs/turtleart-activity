#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Ignacio Rodríguez <ignacio@sugarlabs.org>
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

import json
import urllib
import urllib2
from gettext import gettext as _

from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import logoerror

from TurtleArt.taprimitive import (ArgSlot, Primitive)
from TurtleArt.tatype import TYPE_STRING

import logging
_logger = logging.getLogger('turtleart-activity mashape palette')

MASHAPE_KEY = '3Rfxc7fwp2mshJxgtDxKSueYna8Ap1qZfAcjsn2hjpuWPuBCrI'
TRANSLATE_SECRET = '3b68e1d00446eed728cdda66280a8312'
TRANSLATE_PUBLIC = 'nGhwbdV7TrtzC9qLp3DZ'
TRANSLATE_APIURL = 'https://community-onehourtranslation.p.mashape.com/mt/'


class Mashape(Plugin):

    def __init__(self, parent):
        Plugin.__init__(self)
        self._parent = parent
        self.running_sugar = self._parent.running_sugar
        self.from_lang = 'english'
        self.to_lang = 'spanish'

    def setup(self):
        # set up mashape specific blocks
        palette = make_palette('mashape',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Mashape plugins'))

        palette.add_block(
            'setlang',
            style='basic-style-2arg',
            label=[
                _('set lang'),
                _('from'),
                _('to')],
            prim_name='setlang',
            default=[
                'en',
                'es'],
            help_string=_('set translation settings for translate block'),
        )

        palette.add_block(
            'translate',
            style='number-style-1arg',
            label=_('translate'),
            prim_name='translate',
            default=_('hello world'),
            help_string=_('translate strings'),
        )

        palette.add_block(
            'detectlang',
            style='number-style-1arg',
            label=_('detect lang'),
            prim_name='detectlang',
            default=_('hello world'),
            help_string=_('detect lang of string'),
        )

        self._parent.lc.def_prim(
            'setlang',
            2,
            Primitive(
                self.prim_setlang,
                arg_descs=[
                    ArgSlot(TYPE_STRING),
                    ArgSlot(TYPE_STRING)]))

        self._parent.lc.def_prim(
            'translate',
            1,
            Primitive(self.prim_translate, return_type=TYPE_STRING,
                      arg_descs=[ArgSlot(TYPE_STRING)]))

        self._parent.lc.def_prim(
            'detectlang',
            1,
            Primitive(self.prim_detectlang, return_type=TYPE_STRING,
                      arg_descs=[ArgSlot(TYPE_STRING)]))

    def prim_setlang(self, from_lang, to_lang):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def prim_translate(self, text):
        url = TRANSLATE_APIURL + "translate/text"

        values = {'public_key': TRANSLATE_PUBLIC,
                  'secret_key': TRANSLATE_SECRET,
                  'source_content': text,
                  'source_language': self.from_lang,
                  'target_language': self.to_lang}

        data = urllib.urlencode(values)
        headers = {'X-Mashape-Key': MASHAPE_KEY}

        error = _('error trying to translate:') + '"%s", (%s to %s)' % (
            text, self.from_lang, self.to_lang)

        try:
            request = urllib2.Request(url, data, headers)
            data = json.loads(urllib2.urlopen(request).read())
        except:
            raise logoerror(error)

        if data['status']['msg'] != 'ok' or 'error' in data:
            raise logoerror(error)
        else:
            return data['results']['TranslatedText']

    def prim_detectlang(self, text):
        url = TRANSLATE_APIURL + "detect/text"

        values = {'public_key': TRANSLATE_PUBLIC,
                  'secret_key': TRANSLATE_SECRET,
                  'source_content': text}

        data = urllib.urlencode(values)
        headers = {'X-Mashape-Key': MASHAPE_KEY}

        error = _('error trying to detect lang of:') + '"%s"' % text

        try:
            request = urllib2.Request(url, data, headers)
            data = json.loads(urllib2.urlopen(request).read())
        except:
            raise logoerror(error)

        if data['status']['msg'] != 'ok' or 'error' in data:
            raise logoerror(error)
        else:
            return data['results']['language']
