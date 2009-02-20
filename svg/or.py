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

    myname = "or"
    mystring = "or"
    mygroup = "numbers"

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
   width=\"92\" \n \
   height=\"46\" \n \
   version=\"1.0\"> \n \
  <defs> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" \n \
         offset=\"0\" \n \
         id=\"stop3168\" /> \n \
      <stop \n \
         style=\"stop-color:#ff00ff;stop-opacity:1;\" \n \
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
       gradientTransform=\"matrix(1.0000896,0,0,0.9890701,0.2458786,0.2513884)\" /> \n \
  </defs> \n \
  <path \n \
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#a000a0;stroke-width:1.49184680000000003px;stroke-opacity:1;opacity:1\" \n \
     d=\"M 0.74592343,0.74592343 L 91.754077,0.74592343 L 91.754077,4.2076687 C 91.754077,4.2076687 79.069042,5.9236467 74,9 C 71.203841,10.696962 66.759508,15.097466 65.251702,18 C 64.484155,19.477532 64.087075,21.336249 64.151604,23 C 64.189862,23.986414 64.551215,26.149113 65.051684,27 C 67.351348,30.909843 70.1144,33.659607 74,36 C 78.30402,38.592418 91.754077,41.792331 91.754077,41.792331 L 91.754077,45.254077 L 0.74592343,45.254077 L 0.74592343,41.792331 C 0.74592343,41.792331 14.227222,39.463583 19.247581,36 C 22.495791,33.759036 26.081665,30.711113 27.348298,27 C 27.684138,26.016021 27.779735,23.994457 27.748342,23 C 27.71695,22.005542 27.616888,18.878752 27.248298,18 C 25.790481,14.524428 22.470929,10.998997 19.247581,9 C 14.258161,5.9057523 0.74592343,4.2076687 0.74592343,4.2076687 L 0.74592343,0.74592343 z\" /> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"46\" \n \
       y=\"29\" \n \
       style=\"font-size:18px\">"

    data1 = \
"</tspan></text> \n \
</svg> \n"

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring).encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
