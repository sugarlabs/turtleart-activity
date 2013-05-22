#Copyright (c) 2012, Walter Bender

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the turtle will draw a line of the length of the
# numeric argument block docked to the Python block. But before
# drawing the line, it pushes the rgb values of the destination to the
# FILO.


def myblock(tw, name):
    ''' '''

    def _prim_forward_push(tw, line_length):
        try:  # make sure line_length is a number
            line_length = float(line_length)
        except ValueError:
            return
        penstatus = tw.canvas.pendown
        tw.canvas.setpen(False)
        tw.canvas.forward(line_length)
        r, g, b, a = tw.canvas.get_pixel()
        tw.lc.heap.append(b)
        tw.lc.heap.append(g)
        tw.lc.heap.append(r)
        tw.canvas.forward(-line_length)
        tw.canvas.setpen(penstatus)
        tw.canvas.forward(line_length)
        return

    from TurtleArt.tapalette import make_palette, palette_name_to_index
    from TurtleArt.talogo import primitive_dictionary
    from gettext import gettext as _

    # Choose a palette for the new block.
    palette = make_palette('turtle')

    primitive_dictionary['forwardpush'] = _prim_forward_push

    # Create a new block prototype.
    palette.add_block('forwardpush',
                      style='basic-style-1arg',
                      label=name,
                      default=100,
                      prim_name='forwardpush',
                      help_string=_('push destination rgb value to heap'))

    # Add its primitive to the LogoCode dictionary.
    tw.lc.def_prim('forwardpush', 1,
                   lambda self, x: primitive_dictionary['forwardpush'](tw, x))

    # Regenerate the palette, which will now include the new block.
    tw.show_toolbar_palette(palette_name_to_index('turtle'),
                            regenerate=True)
