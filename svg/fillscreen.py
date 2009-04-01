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

    myname = "fillscreen"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("fill screen")
    mystring2 = _("color")
    mystring3 = _("shade")
    mygroup = "pen"

    print mystring1
    print mystring2
    print mystring3

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   width=\"87\" \n \
   height=\"81\" \n \
   version=\"1.0\"> \n \
  <defs> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" \n \
         offset=\"0\" \n \
         id=\"stop3168\" /> \n \
      <stop \n \
         style=\"stop-color:#00ffff;stop-opacity:1;\" \n \
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
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.5;stroke-opacity:1\" \n \
     d=\"M 69.75,42.75 L 86.25,42.75 L 86.25,49 L 82.25,49 L 82.25,45.75 L 71.75,45.75\" /> \n \
  <path \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.5;stroke-opacity:1\" \n \
     d=\"M 69.75,70.25 L 86.25,70.25 L 86.25,64.249999 L 82.25,64.249999 L 82.25,67.249999 L 71.75,67.249999\" /> \n \
  <path \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.5;stroke-opacity:1\" \n \
     d=\"M 70,6 L 86.5,6 L 86.5,12 L 82.5,12 L 82.5,9 L 72,9\" /> \n \
  <path \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.5;stroke-opacity:1\" \n \
     d=\"M 70,33.5 L 86.5,33.5 L 86.5,27.5 L 82.5,27.5 L 82.5,30.5 L 72,30.5\" /> \n \
  <path \n \
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#00a0a0;stroke-width:2;stroke-opacity:1\" \n \
     d=\"M 48,1 C 64,1 64,1 64,1 L 69.5,5 L 73,11 L 73,67 L 69.5,72 L 64,76 L 47,76 L 47,76 L 47,80 L 27,80 L 27,76 L 10,76 L 4.5,72 L 1,67 L 1,11 L 4.5,5 L 10,1 L 26,1 L 26,6 L 48,6 L 48,1 z\" /> \n \
  <text \n \
     style=\"font-size:18px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"37\" \n \
       y=\"38\" \n \
       style=\"font-size:16px;\">"

    data1 = \
"</tspan><tspan \n \
       x=\"37\" \n \
       y=\"54\" \n \
       style=\"font-size:16px;\">"

    data2 = \
"</tspan></text> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:end;text-align:end;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"68\" \n \
       y=\"22\" \n \
       style=\"font-size:14px\">"

    data3 = \
"</tspan></text> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:end;text-align:end;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"68\" \n \
       y=\"66\" \n \
       style=\"font-size:14px\">"

    data4 = \
"</tspan></text> \n \
</svg> \n "

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    strings = mystring1.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data1)
    if len(strings) == 2:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data2)
    FILE.write(mystring2.encode("utf-8"))
    FILE.write(data3)
    FILE.write(mystring3.encode("utf-8"))
    FILE.write(data4)
    FILE.close()
    return

if __name__ == "__main__":
    main()
