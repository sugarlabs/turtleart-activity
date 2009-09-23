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

    myname = "repeat"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring = _("repeat")
    mygroup = "flow"

    print mystring

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   width=\"170\" \n \
   height=\"95\" \n \
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
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(9.39087e-2,-0.2031988)\" /> \n \
  </defs> \n \
  <path \n \
     style=\"opacity:1;fill:url(#linearGradient3172);fill-opacity:1;stroke:#a97513;stroke-width:2;stroke-opacity:1\" \n \
     d=\"M 48,1 C 64,1 64.187817,1 64.187817,1 C 64.187817,1 67.093036,1.8126092 68.09137,2.6369032 C 69.004632,3.3909562 70.572334,5.3908629 70.572334,5.3908629 L 98,5.6954315 L 98,11 L 93.51841,11 L 93.263659,8 L 85,8 L 85,31 L 93.310656,31 L 93.360477,28 L 98,28 L 98,41 L 170,41 L 170,53 L 164.5996,52.913706 C 164.5996,52.913706 163.3287,50.514626 162.35627,49.771977 C 161.2959,48.962173 159,48 159,48 L 142,48 L 142,53 L 122,53 L 122,48 L 103,48 C 103,48 99.722895,50.806066 98.5,52 C 97.017521,53.447372 95,56.347563 95,56.347563 L 95,81 L 75.204118,80.90405 C 75.204118,80.90405 73.24214,85.39853 71.78641,86.85394 C 70.354258,88.28578 65.932154,90 65.932154,90 L 47,90 L 47,94 L 28,94 L 28,90 L 10.924831,90 C 10.924831,90 6.228383,88.0831 4.6063009,86.53995 C 3.3197278,85.31599 1,81.54299 1,81.54299 L 1,10.796801 C 1,10.796801 3.196437,6.3426262 4.5939087,4.7968012 C 5.9621108,3.2833542 10.093909,1 10.093909,1 L 26,1 L 26,6 L 48,6 L 48,1 z\" /> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\" \n \
     id=\"text2553\"><tspan \n \
       x=\"37\" \n \
       y=\"27.5\" \n \
       style=\"font-size:18px;\">"

    data1 = \
"</tspan></text> \n \
</svg> \n"


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring.encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
