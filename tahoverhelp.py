# -*- coding: utf-8 -*-
#Copyright (c) 2009, Walter Bender, Raúl Gutiérrez Segalés

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

# popup help dictionary

from gettext import gettext as _
hover_dict = { \
    "turtle":_("palette of turtle commands"), \
    "pen":_("palette of pen commands"), \
    "numbers":_("palette of numeric operators"), \
    "sensors":_("palette of extra options"), \
    "flow":_("palette of flow operators"), \
    "myblocks":_("palette of variable blocks"), \
    "templates":_("palette of presentation templates"), \
    "clean":_("clear the screen and reset the turtle"), \
    "forward":_("move turtle forward"), \
    "back":_("move turtle backward"), \
    "left":_("turn turtle counterclockwise (angle in degrees)"), \
    "right":_("turn turtle clockwise (angle in degrees)"), \
    "arc":_("move turtle along an arc"), \
    "setxy":_("move turtle to position xcor, ycor; (0, 0) is in the center of the screen."), \
    "seth":_("set the heading of the turtle (0 is towards the top of the screen.)"), \
    "show":_("draw text or show media from the Journal"), \
    "setscale":_("set the scale of media"), \
    "xcor":_("holds current x-coordinate value of the turtle (can be used in place of a number block)"), \
    "ycor":_("holds current y-coordinate value of the turtle (can be used in place of a number block)"), \
    "heading":_("holds current heading value of the turtle (can be used in place of a number block)"), \
    "scale":_("holds current scale value (can be used in place of a number block)"), \
    "penup":_("turtle will not draw when moved"), \
    "pendown":_("turtle will draw when moved"), \
    "setpensize":_("set size of the line drawn by the turtle"), \
    "setcolor":_("set color of the line drawn by the turtle"), \
    "setshade":_("set shade of the line drawn by the turtle"), \
    "settextcolor":_("set color of text drawn by the turtle"), \
    "settextsize":_("set size of text drawn by turtle"), \
    "fillscreen":_("fills the background with (color, shade)"), \
    "pensize":_("holds current pen size (can be used in place of a number block)"), \
    "color":_("holds current pen color (can be used in place of a number block)"), \
    "shade":_("holds current pen shade (can be used in place of a number block)"), \
    "textsize":_("holds current text size (can be used in place of a number block)"), \
    "textcolor":_("holds current text color (can be used in place of a number block)"), \
    "number":_("used as numeric input in mathematic operators"), \
    "plus2":_("adds two numeric inputs"), \
    "minus2":_("subtracts bottom numeric input from top numeric input"), \
    "product2":_("multiplies two numeric inputs"), \
    "division2":_("divides top numeric input (numerator) by bottom numeric input (denominator)"), \
    "remainder2":_("modular (remainder) operator"), \
    "identity":_("identity operator used for extending blocks"), \
    "identity2":_("identity operator used for extending blocks"), \
    "sqrt":_("calculate square root"), \
    "random":_("returns random number between minimum (left) and maximum (right) values"), \
    "equal":_("logical equal-to operator"), \
    "greater":_("logical greater-than operator"), \
    "less":_("logical less-than operator"), \
    "and":_("logical AND operator"), \
    "or":_("logical OR operator"), \
    "not":_("logical NOT operator"), \
    "print":_("prints value in status block at bottom of the screen"), \
    "kbinput":_("query for keyboard input (results stored in keyboard block)"), \
    "keyboard":_("holds results of query-keyboard block"), \
    "nop":_("runs code found in the tamyblock.py module found in the Journal"), \
    "myfunc":_("a programmable block: add your own math equation in the block, e.g., sin(x)"), \
    "hres":_("the canvas width"), \
    "vres":_("the canvas height"), \
    "leftpos":_("xcor of left of screen"), \
    "toppos":_("ycor of top of screen"), \
    "rightpos":_("xcor of right of screen"), \
    "bottompos":_("ycor of bottom of screen"), \
    "push":_("push value onto FILO (first-in last-out) heap"), \
    "pop":_("pop value off FILO"), \
    "prnthear":_("show FILO in status block"), \
    "clearheap":_("empty FILO"), \
    "wait":_("wait specified number of seconds"), \
    "forever":_("loop forever"), \
    "repeat":_("loop specified number of times"), \
    "if":_("if-then operator that uses boolean operators from Numbers palette"), \
    "ifelse":_("if-then-else operator that uses boolean operators from Numbers palette"), \
    "stopstack":_("do not continue current action"), \
    "hspace":_("jog stack right"), \
    "vspace":_("jog stack down"), \
    "start":_("connects action to toolbar run buttons"), \
    "hat1":_("top of action 1 stack"), \
    "stack1":_("invoke action 1 stack"), \
    "hat2":_("top of action 2 stack"), \
    "stack2":_("invoke action 2 stack"), \
    "hat":_("top of nameable action stack"), \
    "stack":_("invoke named action stack"), \
    "storeinbox1":_("store numeric value in variable 1"), \
    "box1":_("variable 1 (numeric value)"), \
    "storeinbox2":_("store numeric value in variable 2"), \
    "box2":_("variable 2 (numeric value)"), \
    "storein":_("store numeric value in named variable"), \
    "box":_("named variable (numeric value)"), \
    "string":_("string value"), \
    "journal":_("Sugar Journal media object"), \
    "audiooff":_("Sugar Journal audio object"), \
    "descriptionoff":_("Sugar Journal description field"), \
    "template1":_("presentation template: select Journal object (with description)"), \
    "template2":_("presentation template: select two Journal objects"), \
    "template6":_("presentation template: select two Journal objects"), \
    "template7":_("presentation template: select four Journal objects"), \
    "template4":_("presentation template: select Journal object (no description)"), \
    "template3":_("presentation template: seven bullets"), \
    "hideblocks":_("declutter canvas by hiding blocks")}
