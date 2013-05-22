#Copyright (c) 2011,2012 Walter Bender

# DEPRECATED by load block on extras palette.

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the turtle will create a block at the current
# location of the turtle.  The first argument to the Python block
# should be a string containing the name of the desired
# block. Arguments to the block can be passed by expanding the Python
# block to include up to two additional arguments.  Note that the
# turtle is moved to the bottom of the block after it is loaded in
# order position another block to the bottom of the stack.

# The status of these blocks is set to 'load block'

# For example, try the following to place forward 100, right 90 on the canvas:
# start
# Python(forward, 100)  <-- Python load_block.py expanded to two arguments
# Python(right, 90)  <-- Python load_block.py expanded to two arguments


def myblock(tw, blkname):
    ''' Load a block on to the canvas '''

    from TurtleArt.tapalette import block_names, block_primitives, \
        special_names, content_blocks
    from TurtleArt.tautils import find_group

    def make_block(tw, name, x, y, defaults):
        tw._new_block(name, x, y, defaults)

        # Find the block we just created and attach it to a stack.
        tw.drag_group = None
        spr = tw.sprite_list.find_sprite((x, y))
        if spr is not None:
            blk = tw.block_list.spr_to_block(spr)
            if blk is not None:
                tw.drag_group = find_group(blk)
                for b in tw.drag_group:
                    b.status = 'load block'
                tw._snap_to_dock()

        # Disassociate new block from mouse.
        tw.drag_group = None
        return blk.docks[-1][3]

    def find_block(tw, blkname, x, y, defaults=None):
        """ Create a new block. It is a bit more work than just calling
        _new_block(). We need to:
        (1) translate the label name into the internal block name;
        (2) 'dock' the block onto a stack where appropriate; and
        (3) disassociate the new block from the mouse. """

        for name in block_names:
            # Translate label name into block/prim name.
            if blkname in block_names[name]:
                if name in block_primitives and \
                        block_primitives[name] == name:
                    return make_block(tw, name, x, y, defaults)
                elif name in content_blocks:
                    return make_block(tw, name, x, y, defaults)
        for name in special_names:
            # Translate label name into block/prim name.
            if blkname in special_names[name]:
                return make_block(tw, name, x, y, defaults)
        return -1

    # Place the block at the active turtle (x, y) and move the turtle
    # into position to place the next block in the stack.
    x, y = tw.active_turtle.get_xy()
    if isinstance(blkname, list):
        name = blkname[0]
        value = blkname[1:]
        dy = int(find_block(tw, name, x, y, value))
    else:
        name = blkname
        if name == 'delete':
            for blk in tw.just_blocks():
                if blk.status == 'load block':
                    blk.type = 'trash'
                    blk.spr.hide()
            dy = 0
        else:
            dy = int(find_block(tw, name, x, y))

    tw.canvas.ypos -= dy
    tw.canvas.move_turtle()
