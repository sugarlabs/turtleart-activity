# -*- coding: utf-8 -*-
#Copyright (c) 2010 Walter Bender

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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango

#
# A class for the list of blocks and everything they share in common
#
class Blocks:
    def __init__(self):
        self.list = []

    def get_block(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self,spr):
        self.list.append(spr)

    def insert_in_list(self,spr,i):
        if i < 0:
            self.list.insert(0, spr)
        elif i > len(self.list)-1:
            self.list.append(spr)
        else:
            self.list.insert(i, spr)

    def remove_from_list(self,spr):
        if spr in self.list:
            self.list.remove(spr)

#
# A class for the individual blocks
#
class Block:
    def __init__(self, blocks, prototype_style, color=["#00A000","#00FF00"], scale=1.0):
        self.blocks = blocks
        self._new_block_from_prototype(prototype_style, color, scale)
        self.blocks.append_to_list(self)

    def _new_block_from_prototype(self, style, color, scale):
        pass


