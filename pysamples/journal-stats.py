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
    from gettext import gettext as _

    MAX = 19
    DIROFINTEREST = 'datastore'

    class ParseJournal():

        ''' Simple parser of datastore '''

        def __init__(self):
            self._dsdict = {}
            self._activity_name = []
            self._activity_count = []

            homepath = os.environ['HOME']
            for name in os.listdir(os.path.join(homepath, ".sugar")):
                path = os.path.join(homepath, ".sugar", name)
                if isdsdir(path):
                    self._dsdict[os.path.basename(path)] = []
                    if not os.path.isdir(path):
                        continue

                    for dsobjdir in os.listdir(path):
                        if len(dsobjdir) != DIROFINTEREST + 2:
                            continue

                        dsobjdir = os.path.join(path, dsobjdir)
                        if not os.path.isdir(dsobjdir):
                            continue

                        for dsobj in os.listdir(dsobjdir):
                            dsobj = os.path.join(dsobjdir, dsobj)

                            self._dsdict[os.path.basename(path)].append({})
                            activity = isactivity(dsobj)
                            if not activity:
                                self._dsdict[os.path.basename(path)][-1][
                                    'activity'] = 'media object'
                            else:
                                self._dsdict[os.path.basename(path)][-1][
                                    'activity'] = activity

            for k, v in self._dsdict.items():
                for a in v:
                    if 'activity' in a:
                        if a['activity'] in self._activity_name:
                            i = self._activity_name.index(a['activity'])
                            self._activity_count[i] += 1
                        else:
                            self._activity_name.append(a['activity'])
                            self._activity_count.append(1)

        def get_sorted(self):
            activity_tuples = []
            for i in range(len(self._activity_name)):
                activity_tuples.append((self._activity_name[i],
                                        self._activity_count[i]))
            sorted_tuples = sorted(activity_tuples, key=lambda x: x[1])
            activity_list = []
            count = 0
            length = len(sorted_tuples)
            for i in range(length):
                if i < MAX:
                    activity_list.append([sorted_tuples[length - i - 1][0],
                                          sorted_tuples[length - i - 1][1]])
                else:
                    count += sorted_tuples[length - i - 1][1]
            if count > 0:
                activity_list.append([_('other'), count])
            return activity_list

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

    data = ParseJournal()
    activity_list = data.get_sorted()
    for a in activity_list:
        tw.lc.heap.append(a[0])
        tw.lc.heap.append(a[1])

    tw.lc.heap.append(activity_list[0][1])
    return
