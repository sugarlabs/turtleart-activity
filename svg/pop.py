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

    myname = "pop"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring = _("pop")
    mygroup = "sensors"

    print mystring

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<!-- Created with Inkscape (http://www.inkscape.org/) --> \n \
<svg \n \
   xmlns:svg=\"http://www.w3.org/2000/svg\" \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   version=\"1.0\" \n \
   width=\"105\" \n \
   height=\"21\" \n \
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
         style=\"stop-color:#ff0000;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"104\" \n \
       y2=\"21\" \n \
       id=\"linearGradient3172\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 1,0.5 L 6,0.5 L 6,4.5 L 13,4.5 L 13,0.5 L 104.5,0.5 L 104.5,20.5 L 13,20.5 L 13,16.5 L 6,16.5 L 6,20.5 L 1,20.5 L 1,0.5 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#a00000;stroke-width:2;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text12\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"52\" \n \
       y=\"15.5\" \n \
       id=\"tspan14\" \n \
       style=\"font-size:16px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
</svg> \n"


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring.encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
