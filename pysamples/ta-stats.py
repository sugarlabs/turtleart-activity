# Copyright (c) 2012, Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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


def myblock(tw, x):  # ignore second argument
    ''' Load journal stats to heap (Sugar only) '''

    import os

    DIROFINTEREST = 'datastore'

    class ParseJournal():

        ''' Simple parser of datastore for turtle art entries '''

        def __init__(self):
            self._score = []

            homepath = os.environ['HOME']
            for name in os.listdir(os.path.join(homepath, '.sugar')):
                path = os.path.join(homepath, ".sugar", name)
                if isdsdir(path):
                    for dsobjdir in os.listdir(path):
                        if len(dsobjdir) != DIROFINTEREST + 2:
                            continue

                        dsobjdir = os.path.join(path, dsobjdir)
                        for dsobj in dsobjdir:
                            dsobj = os.path.join(dsobjdir, dsobj)
                            if not isactivity(dsobj) == 'TurtleArtActivity':
                                continue
                            if hascomponent(dsobj, 'mime_type') != \
                                    'application/x-turtle-art':
                                continue
                            score = hasturtleblocks(dsobj)
                            if score:
                                self._score.append(score)

    def hascomponent(path, component):
        ''' Return metadata attribute, if any '''
        if not os.path.exists(os.path.join(path, 'metadata')):
            return False
        if not os.path.exists(os.path.join(path, 'metadata', component)):
            return False
        fd = open(os.path.join(path, 'metadata', component))
        data = fd.readline()
        fd.close()
        if len(data) == 0:
            return False
        return data

    def isactivity(path):
        ''' Return activity name '''
        activity = hascomponent(path, 'activity')
        if not activity:
            return False
        else:
            return activity.split('.')[-1]

    def isdsdir(path):
        ''' Only interested if it is a datastore directory '''
        if not os.path.isdir(path):
            return False
        if not os.path.exists(os.path.join(path, DIROFINTEREST)):
            return False
        return True

    TACAT = {'clean': 'forward', 'forward': 'forward', 'back': 'forward',
             'left': 'forward', 'right': 'forward', 'arc': 'arc',
             'xcor': 'coord', 'ycor': 'coord', 'heading': 'coord',
             'setxy2': 'setxy', 'seth': 'setxy', 'penup': 'pen',
             'setpensize': 'pen', 'setcolor': 'pen', 'pensize': 'pen',
             'color': 'pen', 'setshade': 'pen', 'setgray': 'pen',
             'gray': 'pen', 'fillscreen': 'pen', 'startfill': 'fill',
             'stopfill': 'fill', 'plus2': 'number', 'minus2': 'number',
             'product2': 'number', 'division2': 'number',
             'pendown': 'pen', 'shade': 'pen', 'remainder2': 'number',
             'sqrt': 'number', 'identity2': 'number', 'and2': 'boolean',
             'or2': 'boolean', 'not': 'boolean', 'greater2': 'boolean',
             'less2': 'boolean', 'equal2': 'boolean', 'random': 'random',
             'repeat': 'repeat', 'forever': 'repeat', 'if': 'ifthen',
             'ifelse': 'ifthen', 'while': 'ifthen', 'until': 'ifthen',
             'hat': 'action', 'stack': 'action', 'storein': 'box',
             'luminance': 'sensor', 'mousex': 'sensor', 'mousey': 'sensor',
             'mousebutton2': 'sensor', 'keyboard': 'sensor',
             'readpixel': 'sensor', 'see': 'sensor', 'time': 'sensor',
             'sound': 'sensor', 'volume': 'sensor', 'pitch': 'sensor',
             'resistance': 'sensor', 'voltage': 'sensor', 'video': 'media',
             'wait': 'media', 'camera': 'media', 'journal': 'media',
             'audio': 'media', 'show': 'media', 'setscale': 'media',
             'savepix': 'media', 'savesvg': 'media', 'mediawait': 'media',
             'mediapause': 'media', 'mediastop': 'media', 'mediaplay': 'media',
             'speak': 'media', 'sinewave': 'media', 'description': 'media',
             'push': 'extras', 'pop': 'extras', 'printheap': 'extras',
             'clearheap': 'extras', 'isheapempty2': 'extras', 'chr': 'extras',
             'int': 'extras', 'myfunction': 'python', 'userdefined': 'python',
             'box': 'box', 'kbinput': 'sensor',
             'loadblock': 'python', 'loadpalette': 'python'}
    TAPAL = {'forward': 'turtlep', 'arc': 'turtlep', 'coord': 'turtlep',
             'setxy': 'turtlep', 'pen': 'penp', 'fill': 'penp',
             'random': 'numberp', 'boolean': 'numberp', 'repeat': 'flowp',
             'ifthen': 'flowp', 'action': 'boxp', 'box': 'boxp',
             'sensor': 'sensorp', 'media': 'mediap', 'extras': 'extrasp',
             'number': 'numberp', 'python': 'extrasp'}
    TASCORE = {'forward': 3, 'arc': 3, 'setxy': 2.5, 'coord': 4, 'turtlep': 5,
               'pen': 2.5, 'fill': 2.5, 'penp': 5,
               'number': 2.5, 'boolean': 2.5, 'random': 2.5, 'numberp': 0,
               'repeat': 2.5, 'ifthen': 7.5, 'flowp': 10,
               'box': 7.5, 'action': 7.5, 'boxp': 0,
               'media': 5, 'mediap': 0,
               'python': 5, 'extras': 5, 'extrasp': 0,
               'sensor': 5, 'sensorp': 0}
    PALS = ['turtlep', 'penp', 'numberp', 'flowp', 'boxp', 'sensorp', 'mediap',
            'extrasp']

    def hasturtleblocks(path):
        ''' Parse turtle block data and generate score based on rubric '''

        if not os.path.exists(os.path.join(path, 'data')):
            return None
        fd = open(os.path.join(path, 'data'))
        blocks = []
        # block name is second token in each line
        for line in fd:
            tokens = line.split(',')
            if len(tokens) > 1:
                token = tokens[1].strip('" [')
                blocks.append(token)

        score = []
        for i in range(len(PALS)):
            score.append(0)
        cats = []
        pals = []

        for b in blocks:
            if b in TACAT:
                if not TACAT[b] in cats:
                    cats.append(TACAT[b])
        for c in cats:
            if c in TAPAL:
                if not TAPAL[c] in pals:
                    pals.append(TAPAL[c])

        for c in cats:
            if c in TASCORE:
                score[PALS.index(TAPAL[c])] += TASCORE[c]

        for p in pals:
            if p in TASCORE:
                score[PALS.index(p)] += TASCORE[p]

        return score

    data = ParseJournal()
    n = min(40, len(data._score) / len(PALS))
    for i in range(n):
        for j in range(len(PALS)):
            tw.lc.heap.append(data._score[(n - i - 1)][len(PALS) - j - 1])

    tw.lc.heap.append(n)
    return
