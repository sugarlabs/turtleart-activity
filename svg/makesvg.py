#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (c) 2009, Sugar Labs

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

import sys
import os
import os.path

def main():

    py = [ \
 "and.py", \
 "arc.py", \
 "back.py", \
 "box1.py", \
 "box2.py", \
 "clean.py", \
 "clearheap.py", \
 "color.py", \
 "fillscreen.py", \
 "flowgroup.py", \
 "forever.py", \
 "forward.py", \
 "hat1.py", \
 "hat2.py", \
 "heading.py", \
 "hideblocks.py", \
 "hres.py", \
 "ifelse.py", \
 "if.py", \
 "kbinput.py", \
 "keyboard.py", \
 "left.py", \
 "myblocksgroup.py", \
 "not.py", \
 "numbersgroup.py", \
 "or.py", \
 "pendown.py", \
 "pengroup.py", \
 "pensize.py", \
 "penup.py", \
 "pop.py", \
 "printheap.py", \
 "print.py", \
 "random.py", \
 "random.pyc", \
 "remainder2.py", \
 "remainder.py", \
 "repeat.py", \
 "right.py", \
 "sensorsgroup.py", \
 "setcolor.py", \
 "seth.py", \
 "setpensize.py", \
 "setshade.py", \
 "settextcolor.py", \
 "setxy.py", \
 "shade.py", \
 "sound.py", \
 "stack1.py", \
 "stack2.py", \
 "start.py", \
 "stopstack.py", \
 "storeinbox1.py", \
 "storeinbox2.py", \
 "templatesgroup.py", \
 "turtlegroup.py", \
 "vres.py", \
 "wait.py", \
 "xcor.py", \
 "ycor.py" ]

    if len(sys.argv) != 2:
        print "Error: Usage is makesvg.py lang"
        return

    # start from a copy of the en images
    print "os.system(" + "cp -r ../images/en ../image/" + sys.argv[1] + ")"
    os.system("cp -r ../images/en ../images/" + sys.argv[1])

    # make a copy of the samples directory too
    os.system("cp -r ../samples/en ../samples/" + sys.argv[1])

    # run the scripts to generate the language-specific files
    for p in py:
        print "building: " + p
        os.system("python " + p + " " + sys.argv[1])

if __name__ == "__main__":
    main()
