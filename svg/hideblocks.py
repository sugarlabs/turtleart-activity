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
import gettext

def main():

    myname = "hideblocks"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("hide blocks")
    mygroup = "templates"

    print mystring1

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   width=\"87\" \n \
   height=\"60\" \n \
   version=\"1.0\"> \n \
  <defs> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" \n \
         offset=\"0\" \n \
         id=\"stop3168\" /> \n \
      <stop \n \
         style=\"stop-color:#ffff00;stop-opacity:1;\" \n \
         offset=\"1\" \n \
         id=\"stop3170\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       xlink:href=\"#linearGradient3166\" \n \
       id=\"linearGradient3172\" \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#c0a000;stroke-width:2;stroke-opacity:1\" \n \
     d=\"M 48,1 C 64,1 64,1 64,1 L 69.5,5 L 73,11 L 73,45 L 69.5,51 L 64,55 L 47,55 L 47,55 L 47,59 L 27,59 L 27,55 L 10,55 L 4.5,51 L 1,45 L 1,11 L 4.5,5 L 10,1 L 26,1 L 26,6 L 48,6 L 48,1 z\" /> \n"

    data1a = \
"  <text \n \
       style=\"font-size:18px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"36\" \n \
       style=\"font-size:18px;\">"

    data1b = \
"  <text \n \
       style=\"font-size:18px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"27\" \n \
       style=\"font-size:18px;\">"

    data2b = \
"</tspan> \n \
  </text> \n \
  <text \n \
       style=\"font-size:18px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"46\" \n \
       style=\"font-size:18px;\">"

    data3 = \
"</tspan> \n \
  </text> \n \
</svg> \n"


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    strings = mystring1.split(" ",2)
    if len(strings) == 1:
        FILE.write(data1a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data1b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data2b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data3)
    FILE.close()
    return

if __name__ == "__main__":
    main()

