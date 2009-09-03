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

    myname = "storein"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring = _("store in")
    mygroup = "myblocks"

    print mystring

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>]\n\
<!-- Created with Inkscape (http://www.inkscape.org/) -->]\n\
<svg]\n\
   xmlns:svg=\"http://www.w3.org/2000/svg\"]\n\
   xmlns=\"http://www.w3.org/2000/svg\"]\n\
   xmlns:xlink=\"http://www.w3.org/1999/xlink\"]\n\
   version=\"1.0\"]\n\
   width=\"142\"]\n\
   height=\"60\"]\n\
   id=\"svg2\">]\n\
  <defs]\n\
     id=\"defs4\">]\n\
    <linearGradient]\n\
       id=\"linearGradient3166\">]\n\
      <stop]\n\
         id=\"stop3168\"]\n\
         style=\"stop-color:#ffffff;stop-opacity:1\"]\n\
         offset=\"0\" />]\n\
      <stop]\n\
         id=\"stop3170\"]\n\
         style=\"stop-color:#ffff00;stop-opacity:1\"]\n\
         offset=\"1\" />]\n\
    </linearGradient>]\n\
    <linearGradient]\n\
       x1=\"0\"]\n\
       y1=\"22\"]\n\
       x2=\"128\"]\n\
       y2=\"22\"]\n\
       id=\"linearGradient3172\"]\n\
       xlink:href=\"#linearGradient3166\"]\n\
       gradientUnits=\"userSpaceOnUse\" />]\n\
  </defs>]\n\
  <g]\n\
     transform=\"translate(60,54)\"]\n\
    <path]\n\
       d=\"M 64.871323,-38.92647 L 81.371323,-38.92647 L 81.371323,-32.92647 L 77.371323,-32.92647 L 77.371323,-35.92647 L 66.871323,-35.92647\"]\n\
       style=\"fill:#e0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.5;stroke-opacity:1\" />]\n\
    <path]\n\
       d=\"M 64.871323,-11.42647 L 81.371323,-11.42647 L 81.371323,-17.42647 L 77.371323,-17.42647 L 77.371323,-14.42647 L 66.871323,-14.42647\"]\n\
       style=\"fill:#e0e000;fill-opacity:1;stroke:#908000;stroke-width:1.5;stroke-opacity:1\" />]\n\
  </g>]\n\
  <path]\n\
     d=\"M 47,1 C 63,1 120,1 120,1 C 120,1 124.1318,3.4865526 125.5,5 C 126.89747,6.5458243 129,11 129,11 L 129,46 C 129,46 126.78295,49.693654 125.5,51 C 124.07044,52.455629 120,55 120,55 L 47,55 L 47,55 L 47,59 L 27,59 L 27,55 L 10,55 C 10,55 5.9295605,52.455629 4.5,51 C 3.2170498,49.693654 1,46 1,46 L 1,11 C 1,11 3.1025283,6.5458243 4.5,5 C 5.8682021,3.4865526 10,1 10,1 L 27,1 L 27,6 L 47,6 L 47,1 z\"]\n\
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#c0a000;stroke-width:2;stroke-opacity:1\" />]\n\
  <path]\n\
     d=\"M 13,28 L 18,28 L 18,32 L 24.999999,32 L 24.999999,28 L 116.50001,28 L 116.50001,48 L 24.999999,48 L 24.999999,44 L 18,44 L 18,48 L 13,48 L 13,28 z\"]\n\
     style=\"fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:2;stroke-opacity:1\" />]\n\
  <text]\n\
     style=\"font-size:18px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">]\n\
    <tspan]\n\
       x=\"65\"]\n\
       y=\"24\"]\n\
       style=\"font-size:18px\">"

    data1 = \
"</tspan> \n\
  </text> \n\
</svg> \n"

    strings = mystring.split(" ",3)
    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname+".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring.encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
