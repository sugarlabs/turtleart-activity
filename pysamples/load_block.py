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

# This procedure is invoked when the user-definable block on the "extras"
# palette is selected.


def myblock(lc, blkname):

    ###########################################################################
    #
    # Load a block on to the canvas
    #
    ###########################################################################

    from taconstants import BLOCK_NAMES, PRIMITIVES, CONTENT_BLOCKS, \
        SPECIAL_NAMES
    from tautils import find_group

    def make_block(lc, name, x, y, defaults):
        x_pos = x + 20
        y_pos = y + 20
        lc.tw._new_block(name, x_pos, y_pos, defaults)

        # Find the block we just created and attach it to a stack.
        lc.tw.drag_group = None
        spr = lc.tw.sprite_list.find_sprite((x_pos, y_pos))
        if spr is not None:
            blk = lc.tw.block_list.spr_to_block(spr)
            if blk is not None:
                lc.tw.drag_group = find_group(blk)
                lc.tw._snap_to_dock()

        # Disassociate new block from mouse.
        lc.tw.drag_group = None
        return blk.height

    def find_block(lc, blkname, x, y, defaults=None):
        """ Create a new block. It is a bit more work than just calling
        _new_block(). We need to:
        (1) translate the label name into the internal block name;
        (2) 'dock' the block onto a stack where appropriate; and
        (3) disassociate the new block from the mouse. """

        print blkname
        for name in BLOCK_NAMES:
            # Translate label name into block/prim name.
            if blkname in BLOCK_NAMES[name]:
                if (name in PRIMITIVES and PRIMITIVES[name] == name) or \
                   name in CONTENT_BLOCKS:
                    return make_block(lc, name, x, y, defaults)
        for name in SPECIAL_NAMES:
            # Translate label name into block/prim name.
            if blkname in SPECIAL_NAMES[name]:
                return make_block(lc, name, x, y, defaults)
        return -1

    # Place the block at the active turtle (x, y) and
    # push height to stack.
    x, y = lc.tw.active_turtle.get_xy()
    if type(blkname) == type([]):
        name = blkname[0]
        value = blkname[1:]
        dy = int(find_block(lc, name, x, y, value))
    else:
        name = blkname
        dy = int(find_block(lc, name, x, y))
    if dy != -1:
        lc.heap.append(dy)
