# Copyright (c) 2014, Walter Bender

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the turtle will draw a line composed of text of
# the length of the numeric argument block docked to the Python block.
# A second, optional, argument can be used to specify the text. The
# default is '*'.


def myblock(tw, args):
    ''' Draw a line of length line_length composed of text characters '''

    try:  # make sure line_length is a number
        line_length = float(args[0])
    except ValueError:
        return
    # An optional second argument can be used for setting the text.
    if len(args) > 1:
        string = str(args[1])
    else:
        string = '*'

    turtle = tw.turtles.get_active_turtle()
    if turtle.get_pen_state():
        dist = 0
        pen_size = turtle.get_pen_size()
        heading = turtle.get_heading()
        i = 0  # index into text string
        while dist + pen_size < line_length:
            turtle.set_pen_state(True)
            x, y = tw.turtles.turtle_to_screen_coordinates(
                turtle.get_xy())
            turtle.set_heading(heading - 90)
            turtle.draw_text(string[i % len(string)], x, y, pen_size,
                             pen_size * 1.5)
            i += 1
            turtle.set_heading(heading)
            turtle.set_pen_state(False)
            turtle.forward(pen_size * 1.5)
            dist += pen_size * 1.5
        # make sure we have moved exactly line_length
        turtle.forward(line_length - dist)
        turtle.set_pen_state(True)
    else:
        turtle.forward(line_length)
