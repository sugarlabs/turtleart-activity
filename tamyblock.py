#Copyright (c) 2009-10, Walter Bender

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

#
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
# tamyblock.py, lc.tw is the class instance)
# 
# Methods and data attributes	Example
# set_fullscreen(self)		lc.tw.set_fullscreen()
# Note: Hides the Sugar toolbar
# set_cartesian(self, flag)	lc.tw.set_cartesian(True)
# Note: True will make the overlay visible;
#       False will make it invisible
# set_polar(self, flag)		lc.tw.set_polar(True)
# Note: True will make the overlay visible;
#       False will make it invisible
# hideshow_button(self, flag)	lc.tw.hideshow_button()
# Note: Toggles visibility of blocks and palettes
# self.active_turtle		lc.tw.active_turtle
# Note: The active turtle instance
# 
# 
# Class TurtleGraphics -- useful properties and methods (from within
# tamyblock.py, lc.tw.canvas is the class instance)
# 
# Methods and data attributes	Example
# clearscreen(self)		lc.tw.canvas.clearscreen()
# Note: Clears the screen and resets all turtle and
#       pen attributes to default values
# setpen(self, flag)		lc.tw.canvas.setpen(True)
# Note: True will set the pen "down", enabling drawing;
#       False will set the pen "up"
# forward(self, n)		lc.tw.canvas.forward(100)
# Note: Move the turtle forward 100 units
# arc(self, a, r)		lc.tw.canvas.arc(120, 50)
# Note: Move the turtle along an arc of 120 degrees
#       (clockwise) and radius of 50 units
# setheading(self, a)		lc.tw.canvas.setheading(180)
# Note: Set the turtle heading to 180
#       (towards the bottom of the screen)
# self.heading			lc.tw.canvas.heading
# Note: The current heading
# setpensize(self, n)		lc.tw.canvas.setpensize(25)
# Note: Set the turtle pensize to 25 units
# self.pensize			lc.tw.canvas.pensize
# Note: The current pensize
# setcolor(self, c)		lc.tw.canvas.color(70)
# Note:	Set the pen color to 70 (blue)
# self.color			lc.tw.canvas.color
# Note: The current pen color
# setshade(self, s)		lc.tw.canvas.shade(50)
# Note:	Set the pen shade to 50
# self.shade			lc.tw.canvas.shade
# Note: The current pen shade
# fillscreen(self, c, s)	lc.tw.canvas.fillscreen(70, 90)
# Note: Fill the screen with color 70, shade 90 (light blue)
# setxy(self, x, y)		lc.tw.canvas.setxy(100,100)
# Note: Move the turtle to position (100, 100)
# self.xcor			lc.tw.canvas.xcor
# Note: The current x coordinate of the turtle
#       (scaled to current units)
# self.ycor			lc.tw.canvas.ycor
# Note: The current y coordinate of the turtle
#       (scaled to current units)
# self.set_turtle(name)		lc.tw.canvas.set_turtle(1)
# Note: Set the current turtle to turtle '1'
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
# 				lc.heap.append(data) adds data to the heap
# Note: See http://docs.python.org/tutorial/datastructures.html
# 				data = lc.heap.pop(-1) pops data off the heap
# Note: See http://docs.python.org/tutorial/datastructures.html
#

def myblock(lc, x):

    ###########################################################################
    #
    # Set rgb color
    #
    ###########################################################################

    # r = int(x[0])
    # while r < 0:
    #     r += 256
    # while r > 255:
    #     r -= 256
    # g = int(x[1])
    # while g < 0:
    #     g += 256
    # while g > 255:
    #     g -= 256
    # b = int(x[2])
    # while b < 0:
    #     b += 256
    # while b > 255:
    #     b -= 256
    # rgb = "#%02x%02x%02x" % (r,g,b)
    # lc.tw.canvas.fgcolor = lc.tw.canvas.cm.alloc_color(rgb)
    # return

    ###########################################################################
    #
    # Draw a dotted line of length x.
    #
    ###########################################################################

    try:  # make sure x is a number
        x = float(x)
    except ValueError:
        return
    if lc.tw.canvas.pendown:
        dist = 0
        while dist+lc.tw.canvas.pensize < x:   # repeat drawing dots
            lc.tw.canvas.setpen(True)
            lc.tw.canvas.forward(1)
            lc.tw.canvas.setpen(False)
            lc.tw.canvas.forward((lc.tw.canvas.pensize*2)-1)
            dist += (lc.tw.canvas.pensize*2)
        lc.tw.canvas.forward(x-dist)  # make sure we have moved exactly x
        lc.tw.canvas.setpen(True)
    else:
        lc.tw.canvas.forward(x)
    return

    ###########################################################################
    #
    # Push an uppercase version of a string onto the heap.
    # Use a 'pop' block to use the new string.
    #
    ###########################################################################

    # if type(x) != str:
    #     X = str(x).upper()
    # else:
    #     X = x.upper()
    # lc.heap.append(X)
    # return

    ###########################################################################
    #
    # Push hours, minutes, seconds onto the FILO.
    # Use three 'pop' blocks to retrieve these values.
    # Note: because we use a FILO (first in, last out heap),
    # the first value you will pop will be seconds.
    #
    ###########################################################################

    # lc.heap.append(localtime().tm_hour)
    # lc.heap.append(localtime().tm_min)
    # lc.heap.append(localtime().tm_sec)
    # return

    ###########################################################################
    #
    # Add a third dimension (gray) to the color model.
    #
    ###########################################################################

    # val = 0.3 * lc.tw.rgb[0] + 0.6 * lc.tw.rgb[1] + 0.1 * lc.tw.rgb[2]
    # if x != 100:
    #     x = int(x)%100
    # r = int((val*(100-x) + lc.tw.rgb[0]*x)/100)
    # g = int((val*(100-x) + lc.tw.rgb[1]*x)/100)
    # b = int((val*(100-x) + lc.tw.rgb[2]*x)/100)
    # reallocate current color
    # rgb = "#%02x%02x%02x" % (r,g,b)
    # lc.tw.canvas.fgcolor = lc.tw.canvas.cm.alloc_color(rgb)
    # return

    ###########################################################################
    #
    # Save an image named x to the Sugar Journal.
    #
    ###########################################################################

    # lc.tw.save_as_image(str(x))
    # return

    ###########################################################################
    #
    # Push mouse event to stack
    #
    ###########################################################################

    # if lc.tw.mouse_flag == 1:
    #     lc.heap.append(lc.tw.mouse_y)
    #     lc.heap.append(lc.tw.mouse_x)
    #     lc.heap.append(1) # mouse event
    #     lc.tw.mouseflag = 0
    # else:
    #     lc.heap.append(0) # no mouse event
    # return
