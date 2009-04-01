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

    myname = "stopstack"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring = _("stop stack")
    mygroup = "flow"

    print mystring


    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   width=\"74\" \n \
   height=\"49\" \n \
   version=\"1.0\"> \n \
  <defs> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" \n \
         offset=\"0\" \n \
         id=\"stop3168\" /> \n \
      <stop \n \
         style=\"stop-color:#feb00a;stop-opacity:1;\" \n \
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
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#a97513;stroke-width:2;stroke-opacity:1\" \n \
     d=\"M 48,1 C 64,1 64,1 64,1 C 64,1 68.131798,3.4865526 69.5,5 C 70.897472,6.5458243 73,11 73,11 L 73,29 L 37.5,48 C 37.5,48 1,29 1,29 L 1,11 C 1,11 3.1025283,6.5458243 4.5,5 C 5.8682021,3.4865526 10,1 10,1 L 26,1 L 26,6 L 48,6 L 48,1 z\" /> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       sodipodi:role=\"line\" \n \
       x=\"37\" \n \
       y=\"17.5\" \n \
       style=\"font-size:14px;text-anchor:middle\">"

    data1 = \
"</tspan><tspan \n \
       x=\"37\" \n \
       y=\"35\" \n \
       style=\"font-size:14px;text-anchor:middle\">"

    data2 = \
"</tspan></text> \n \
</svg> \n"

    strings = mystring.split(" ",2)
    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname+".svg"), "w")
    FILE.write(data0)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data1)
    if len(strings) == 2:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data2)
    FILE.close()
    return

if __name__ == "__main__":
    main()
