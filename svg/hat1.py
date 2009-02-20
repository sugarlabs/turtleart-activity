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

    myname = "hat1"
    mystring = "stack 1"
    mygroup = "myblocks"

    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    print _(mystring)

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   width=\"99\" \n \
   height=\"56\" \n \
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
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(12.5,12)\" /> \n \
    <inkscape:perspective \n \
       id=\"perspective2472\" \n \
       inkscape:persp3d-origin=\"372.04724 : 350.78739 : 1\" \n \
       inkscape:vp_z=\"744.09448 : 526.18109 : 1\" \n \
       inkscape:vp_y=\"0 : 1000 : 0\" \n \
       inkscape:vp_x=\"0 : 526.18109 : 1\" \n \
       sodipodi:type=\"inkscape:persp3d\" /> \n \
  </defs> \n \
  <path \n \
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#c0a000;stroke-width:2;stroke-opacity:1\" \n \
     d=\"M 98.5,28 L 98.5,28 L 59.5,51 L 59.5,51 L 59.5,55 L 39.5,55 L 39.5,51 C 39.5,51 0.5,28 0.5,28 C 0.5,28 49.5,1 49.5,1 C 49.5,1 98.5,28 98.5,28 z\" /> \n \
  <path \n \
     style=\"fill:none;stroke:#606000;stroke-width:1;stroke-opacity:1\" \n \
     d=\"M 39,55.5 L 60,55.5\" /> \n \
  <text \n \
      style=\"font-size:18px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"49\" \n \
       y=\"35\" \n \
style=\"font-size:18px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
</svg> \n "


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring).encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
