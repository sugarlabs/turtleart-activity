# Copyright (c) 2011-2013, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# it is run, a u-turn block will be added to the Turtle Palette. You
# can use the u-turn block as you would any other block.


def myblock(tw, args):
    ''' Add a uturn block to the 'turtle' palette '''

    # def_prim takes 3 arguments: the primitive name, the number of
    # arguments -- 0 in this case -- and the function to call -- in this
    # case, we define the _prim_uturn function to set heading += 180.
    def _prim_uturn(tw):
        value = tw.turtles.get_active_turtle().get_heading() + 180
        tw.turtles.get_active_turtle().set_heading(value)
        # We also update the label on the heading block to indicate
        # the current heading value
        if tw.lc.update_values:
            tw.lc.update_label_value('heading', value)

    from TurtleArt.tapalette import make_palette, palette_name_to_index
    from TurtleArt.taprimitive import Primitive, ConstantArg
    from gettext import gettext as _

    # Choose a palette for the new block.
    palette = make_palette('turtle')

    # Create a new block prototype.
    palette.add_block('uturn',
                      style='basic-style-extended-vertical',
                      label=_('uturn'),
                      prim_name='uturn',
                      help_string=_('turns the turtle 180 degrees'))

    # Add its primitive to the LogoCode dictionary.
    tw.lc.def_prim(
        'uturn',
        0,
        Primitive(
            _prim_uturn,
            arg_descs=[
                ConstantArg(tw)]))

    # Regenerate the palette, which will now include the new block.
    tw.show_toolbar_palette(palette_name_to_index('turtle'),
                            regenerate=True)
