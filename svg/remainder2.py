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

    myname = "remainder2"
    mystring = "mod"
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
<!-- Created with Inkscape (http://www.inkscape.org/) --> \n \
<svg \n \
   xmlns:svg=\"http://www.w3.org/2000/svg\" \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   version=\"1.0\" \n \
   width=\"71.75\" \n \
   height=\"70.5\" \n \
   id=\"svg2\"> \n \
  <defs \n \
     id=\"defs4\"> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         id=\"stop3168\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3170\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"-0.25\" \n \
       y1=\"18.5\" \n \
       x2=\"52.25\" \n \
       y2=\"18.5\" \n \
       id=\"linearGradient3173\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"104\" \n \
       y2=\"21\" \n \
       id=\"linearGradient3172\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-0.2720588,8.0000002)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2480\"> \n \
      <stop \n \
         id=\"stop2482\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2484\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"-0.25\" \n \
       y1=\"18.5\" \n \
       x2=\"52.25\" \n \
       y2=\"18.5\" \n \
       id=\"linearGradient2490\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(1.78e-7,29.691177)\" /> \n \
    <linearGradient \n \
       x1=\"-0.25\" \n \
       y1=\"18.5\" \n \
       x2=\"52.25\" \n \
       y2=\"18.5\" \n \
       id=\"linearGradient2493\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(8.8e-8,33.25)\" /> \n \
    <linearGradient \n \
       x1=\"-0.25\" \n \
       y1=\"18.5\" \n \
       x2=\"52.25\" \n \
       y2=\"18.5\" \n \
       id=\"linearGradient2495\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0.25,0.25)\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 10.75,0.75 L 52,0.75 L 52,9.75 L 47.75,9.75 L 47.75,6.75 L 38.75,6.75 L 38.75,29.75 L 47.75,29.75 L 47.75,26.75 L 52,26.75 L 52,34.75 L 71,34.75 L 71,42.75 L 67,42.75 L 67,39.75 L 58,39.75 L 58,62.959 L 67,62.959 L 67,59.75 L 71,59.75 L 71,69.75 L 10.75,69.75 L 10.75,41.25 L 6.25,41.25 L 6.25,45.25 L 0.75,45.25 L 0.75,24.75 L 6.25,24.75 L 6.25,28.75 L 10.75,28.75 L 10.75,0.75 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient2495);fill-opacity:1;stroke:#a000a0;stroke-width:1.5px;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"8.25\" \n \
     y=\"16.773438\" \n \
     id=\"text12\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"34.25\" \n \
       y=\"58\" \n \
       id=\"tspan14\" \n \
       style=\"font-size:18px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
</svg> \n"


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring).encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
