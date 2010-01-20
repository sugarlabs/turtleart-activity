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
import block_factory
import sprites

#
# A class for the list of blocks and everything they share in common
#
class Blocks:
    def __init__(self, sprites):
        self.list = []
        self.sprites = sprites

    def get_block(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self,block):
        self.list.append(block)

    def insert_in_list(self,block,i):
        if i < 0:
            self.list.insert(0, block)
        elif i > len(self.list)-1:
            self.list.append(block)
        else:
            self.list.insert(i, block)

    def remove_from_list(self, block):
        if block in self.list:
            self.list.remove(block)

    #
    # block and spr utilities
    #
    def spr_to_block(self, spr):
        for b in self.list:
            if spr = b.spr:
                return b

#
# A class for the individual blocks
#
class Block:
    def __init__(self, blocks, proto_name, x, y, labels=[], 
                 colors=["#00A000","#00FF00"], scale=2.0):
        self.blocks = blocks
        self.spr = None
        self._new_block_from_prototype(proto_name, labels, colors, scale, x, y)
        self.blocks.append_to_list(self)
        #
        # TODO:
        # save arguments
        # dock and connection info
        # highlight image
        # Logo code
        # HTML code
        # debug code
        # etc.

    def _new_block_from_prototype(self, name, labels, colors, scale, x, y):
        if len(labels) == 0:
            print "%s (%d %d)" % (name, x, y)
        else:
            print "%s %s (%d %d)" % (name, labels[0], x, y)
        basic_style = ['forward', 'back', 'left', 'right', 'seth']
        box_style = ['number']
        if name in basic_style:
            svg = block_factory.SVG()
            svg.set_scale(scale)
            svg.expand(20,0)
            svg.set_innie([True])
            svg.set_outie(False)
            svg.set_tab(True)
            svg.set_slot(True)
            svg.set_gradiant(True)
            svg.set_colors(colors)
            self.spr = sprites.Sprite(self.blocks.sprites, x, y,
                                      svg_str_to_pixbuf(svg.basic_block()))
            print "created new basic block: %s" % (str(self.spr))
            self.spr.set_layer(2000)
            self.spr.draw()
            self.spr.set_label(labels[0])
        elif name in box_style:
            svg = block_factory.SVG()
            svg.set_scale(scale)
            svg.expand(60,0)
            svg.set_gradiant(True)
            svg.set_colors(colors)
            self.spr = sprites.Sprite(self.blocks.sprites, x, y,
                                      svg_str_to_pixbuf(svg.basic_box()))
            print "created new box block: %s" % (str(self.spr))
        else:
            print "don't know how to create a block for %s" % (name)
            return

        for label in labels:
            self.spr.set_label(label, labels.index(label))

#
# Load pixbuf from SVG string
#
def svg_str_to_pixbuf(svg_string):
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf

