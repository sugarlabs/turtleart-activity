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

    myname = "random"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring = _("random")
    mygroup = "numbers"

    print mystring

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   width=\"280\" \n \
   height=\"48\" \n \
   version=\"1.0\"> \n \
  <defs> \n \
    <linearGradient \n \
       inkscape:collect=\"always\" \n \
       id=\"linearGradient3164\"> \n \
      <stop \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" \n \
         offset=\"0\" \n \
         id=\"stop3166\" /> \n \
      <stop \n \
         style=\"stop-color:#ff00ff;stop-opacity:0;\" \n \
         offset=\"1\" \n \
         id=\"stop3168\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       inkscape:collect=\"always\" \n \
       xlink:href=\"#linearGradient3164\" \n \
       id=\"linearGradient3170\" \n \
       x1=\"0\" \n \
       y1=\"19.625\" \n \
       x2=\"320.75\" \n \
       y2=\"19.625\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       y2=\"21\" \n \
       x2=\"104\" \n \
       y1=\"0\" \n \
       x1=\"0\" \n \
       id=\"linearGradient3172\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientTransform=\"matrix(1.0139238,0,0,1.0946487,31.741439,7.7561892)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         id=\"stop3259\" \n \
         offset=\"0\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" /> \n \
      <stop \n \
         id=\"stop3170\" \n \
         offset=\"1\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:1;\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       inkscape:collect=\"always\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       id=\"linearGradient3258\" \n \
       x1=\"0.11728395\" \n \
       y1=\"24.646091\" \n \
       x2=\"279.92386\" \n \
       y2=\"24.646091\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.9988917,0,0,1.0043477,0.1346121,-0.7532427)\" /> \n \
  </defs> \n \
  <path \n \
     style=\"fill:url(#linearGradient3258);fill-opacity:1;stroke:#a000a0;stroke-width:1.50242388;stroke-opacity:1\" \n \
     d=\"M 259.347,0.75327866 L 22.332204,0.5 C 22.332204,0.5 18.149147,2.8777213 16.783263,4.2670459 C 15.698976,5.3699403 14.110875,8.604136 14.110875,8.604136 L 14.110875,21.830113 L 6.7116766,22.036769 L 6.5061433,18.523618 L 0.5,18.316963 L 0.5,39.395864 L 6.3006101,39.395864 L 6.5061433,35.056091 L 14.110875,35.262746 L 13.905341,43.11567 C 13.905341,43.11567 15.512344,45.123208 16.372196,45.798617 C 17.202851,46.451092 19.45474,47.5 19.45474,47.5 L 267,47.5 L 267,38.775896 L 279.5,38.362584 L 279.5,19.556898 L 267,19.556898 L 267,7.9841684 C 267,7.9841684 265.35487,5.2704925 264.4504,4.2643623 C 263.36589,3.0579557 260.33973,0.75121216 260.33973,0.75121216 L 259.347,0.75327866 L 259.347,0.5\" /> \n \
  <path \n \
     d=\"M 28.755364,18.553513 L 33.824984,18.553513 L 33.824984,22.932108 L 40.922451,22.932108 L 40.922451,18.553513 L 133.69649,18.553513 L 133.69649,40.446487 L 40.922451,40.446487 L 40.922451,36.067892 L 33.824984,36.067892 L 33.824984,40.446487 L 28.755364,40.446487 L 28.755364,18.553513 z\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1.5;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 151.95547,18.553513 L 157.02509,18.553513 L 157.02509,22.932108 L 164.12256,22.932108 L 164.12256,18.553513 L 256,18.553513 L 256,40.446487 L 164.12256,40.446487 L 164.12256,36.067892 L 157.02509,36.067892 L 157.02509,40.446487 L 151.95547,40.446487 L 151.95547,18.553513 z\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1.5;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"140\" \n \
       y=\"15.5\" \n \
       style=\"font-size:14px\">"

    data1 = \
"</tspan></text> \n \
</svg> \n "


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring.encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
