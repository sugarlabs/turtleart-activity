#Copyright (c) 2011, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# it is run, a u-turn block will be added to the Turtle Palette. You
# can use the u-turn block as you would any other block.


def myblock(tw, arg):
    ''' Add a uturn block to the 'turtle' palette '''

    from TurtleArt.tapalette import make_palette, palette_name_to_index
    from TurtleArt.talogo import primitive_dictionary
    from gettext import gettext as _

    # Choose a palette for the new block.
    palette = make_palette('turtle')

    # Create a new block prototype.
    palette.add_block('uturn',
                      style='basic-style-extended-vertical',
                      label=_('uturn'),
                      prim_name='uturn',
                      help_string=_('make a uturn'))

    # Add its primitive to the LogoCode dictionary.
    tw.lc.def_prim('uturn', 0,
                   lambda self: primitive_dictionary['set']
                   ('heading', tw.canvas.seth, tw.canvas.heading + 180))

    # Regenerate the palette, which will now include the new block.
    tw.show_toolbar_palette(palette_name_to_index('turtle'),
                            regenerate=True)
