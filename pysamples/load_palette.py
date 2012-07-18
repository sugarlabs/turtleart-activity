#Copyright (c) 2012, Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block; when
# it is run, the selected palette is loaded


def myblock(tw, arg):
    ''' Select a palette '''

    from TurtleArt.tapalette import make_palette, palette_name_to_index
    from TurtleArt.talogo import primitive_dictionary
    from gettext import gettext as _

    # Select the palette, which will now include the new block.
    if type(arg) == int:
        tw.show_toolbar_palette(arg)
    else:
        if type(arg) == unicode:
            arg = arg.encode('ascii', 'replace')
        tw.show_toolbar_palette(palette_name_to_index(arg))

