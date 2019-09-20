# Copyright (c) 2009-13, Walter Bender

# This procedure is invoked when the user-definable block on the "extras"
# palette is selected. Some examples of how to use this block are included
# below. Try uncommenting an example or write your own Python code.
#
# To uncomment code, remove the '# ' in the Python code. Take care to preserve
# the proper indentations.
#
#
# NOTES:
#
# Turtle Art is created in object oriented Python code. This is based
# around the definition of classes and the creation of object(s) which
# are instance(s) of that class. These objects then have properties and
# methods which are defined by their class.
#
# See http://docs.python.org/tutorial/classes.html for a description of
# classes in Python.
#
# Class			Defined in	Instance	Created in
# TurtleArtWindow	tawindow.py	tw		TurtleArtActivity.py
# LogoCode		talogo.py	lc		tawindow.py
# TurtleGraphics	tacanvas.py	canvas		tawindow.py
# Turtles, Turtle	taturtle.py	turtles		tawindow.py,
#                                                       tacanvas.py
# Blocks, Block		tablock.py	block_list	tawindow.py
#
#
# Class TurtleArtWindow -- useful properties and methods (from within
# tamyblock.py, tw is the class instance)
#
# Methods and data attributes	Example
# set_fullscreen(self)		tw.set_fullscreen()
# Note: Hides the Sugar toolbar
# set_cartesian(self, flag)	tw.set_cartesian(True)
# Note: True will make the overlay visible;
#       False will make it invisible
# set_polar(self, flag)		tw.set_polar(True)
# Note: True will make the overlay visible;
#       False will make it invisible
# hideshow_button(self, flag)	tw.hideshow_button()
# Note: Toggles visibility of blocks and palettes
# self.active_turtle		tw.active_turtle
# Note: The active turtle instance
#
#
# Class TurtleGraphics -- useful properties and methods (from within
# tamyblock.py, tw.canvas is the class instance)
#
# Methods and data attributes	Example
# clearscreen(self)		tw.canvas.clearscreen()
# Note: Clears the screen and resets all turtle and
#       pen attributes to default values
#
#
# Class Turtles -- useful properties and methods (from within
# tamyblock.py, tw.turtles is the class instance)
#
# self.set_turtle(name)		tw.turltes.set_turtle(1)
# Note: Set the current turtle to turtle '1'
# self.get_active_turtle()	tw.turltes.get_active_turtle()
# Note: Returns active turtle (See Class Turtle below)
#
# Class Turtle -- useful properties and methods (from within
# tamyblock.py, tw.turtles.get_active_turtle() is the class instance)
#
# set_pen_state(self, flag)
#       tw.turtles.get_active_turtle().set_pen_state(True)
# Note: True will set the pen "down", enabling drawing;
#       False will set the pen "up"
# forward(self, n)              tw.turtles.get_active_turtle().forward(100)
# Note: Move the turtle forward 100 units
# arc(self, a, r)               tw.turtles.get_active_turtle().arc(120, 50)
# Note: Move the turtle along an arc of 120 degrees
#       (clockwise) and radius of 50 units
# set_heading(self, a)          tw.turtles.get_active_turtle().set_heading(180)
# Note: Set the turtle heading to 180
#       (towards the bottom of the screen)
# self.get_heading()            tw.turtles.get_active_turtle().get_heading()
# Note: The current heading
# set_pen_size(self, n)         tw.turtles.get_active_turtle().set_pen_size(25)
# Note: Set the turtle pensize to 25 units
# self.get_pen_size()           tw.turtles.get_active_turtle().get_pen_size()
# Note: The current pen size
# self.set_color(self, c)       tw.turtles.get_active_turtle().set_color(70)
# Note: Set the pen color to 70 (blue)
# self.color()                  tw.turtles.get_active_turtle().get_color()
# Note: The current pen color
# self.set_shade(self, s)       tw.turtles.get_active_turtle().set_shade(50)
# Note: Set the pen shade to 50
# self.get_shade()              tw.turtles.get_active_turtle().get_shade()
# Note: The current pen shade
# fillscreen(self, c, s)
#       tw.turtles.get_active_turtle().fillscreen(70, 90)
# Note: Fill the screen with color 70, shade 90 (light blue)
# self.set_xy(self, x, y)
#               tw.turtles.get_active_turtle().set_xy(100,100)
# Note: Move the turtle to position (100, 100)
# self.get_xy			tw.turtles.get_active_turtle().get_xy()[0]
# Note: The current x coordinate of the turtle
#       (scaled to current units)
# self.get_xy			tw.turtles.get_active_turtle().get_xy()[1]
# Note: The current y coordinate of the turtle
#       (scaled to current units)
#
#
# Other useful Python functions
# Module			Example
# from math import pow		pow(2,3) returns 2 to the 3rd power
# Note: See http://docs.python.org/library/math.html
# from math import sin, pi	sin(45*pi/180) returns sin of 45 (0.707)
# Note: See http://docs.python.org/library/math.html
# from time import localtime	localtime().tm_hour returns the current hour
# Note: See http://docs.python.org/library/time.html
# 				tw.lc.heap.append(data) adds data to the heap
# Note: See http://docs.python.org/tutorial/datastructures.html
# 				data = tw.lc.heap.pop(-1) pops data off the heap
# Note: See http://docs.python.org/tutorial/datastructures.html
#

# Usage: Import this code into a Python (user-definable) block; when
# this code is run, the turtle will draw a dotted line of the length
# of the numeric argument block docked to the Python block.


def myblock(tw, args):
    ''' Draw a dotted line of length line_length. '''

    try:  # make sure line_length is a number
        line_length = float(args[0])
    except ValueError:
        return
    if tw.turtles.get_active_turtle().get_pen_state():
        dist = 0
        pen_size = tw.turtles.get_active_turtle().get_pen_size()
        while dist + pen_size < line_length:  # repeat drawing dots
            tw.turtles.get_active_turtle().set_pen_state(True)
            tw.turtles.get_active_turtle().forward(1)
            tw.turtles.get_active_turtle().set_pen_state(False)
            tw.turtles.get_active_turtle().forward(pen_size * 2 - 1)
            dist += pen_size * 2
        # make sure we have moved exactly line_length
        tw.turtles.get_active_turtle().forward(line_length - dist)
        tw.turtles.get_active_turtle().set_pen_state(True)
    else:
        tw.turtles.get_active_turtle().forward(line_length)
    return
