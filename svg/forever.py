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

    myname = "forever"
    mystring = "forever"
    mygroup = "flow"

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
   width=\"156\" \n \
   height=\"44\" \n \
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
     d=\"M 48,1 C 64,1 64.093909,1 64.093909,1 C 64.093909,1 66.999128,2.0158072 67.997462,2.8401016 C 68.910724,3.5941544 70.326142,6.0279188 70.326142,6.0279188 L 155,6.5 L 155.07138,18.133011 L 151.56154,18.128966 C 151.56154,18.128966 149.6815,15.956403 148.70907,15.213754 C 147.6487,14.40395 144.8236,13.04981 144.8236,13.04981 L 128.06091,13.315355 L 128.01396,18.088515 L 108.80964,18.166244 L 108.66878,12.891181 L 88.713197,13.250635 C 88.713197,13.250635 85.374202,16.120059 84,17.5 C 82.52486,18.981301 80.5,22.703046 80.5,22.703046 L 80.5,43.116751 L 10.526354,43.203199 C 10.526354,43.203199 5.8299058,41.169544 4.2078237,39.626397 C 2.9212506,38.402433 0.90609137,34.629442 0.90609137,34.629442 L 1,11 C 1,11 3.1025283,6.5458243 4.5,5 C 5.8682021,3.4865526 10,1 10,1 L 26,1 L 26,6 L 48,6 L 48,1 z\" /> \n"

    data1 = \
"  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\" > \n \
     <tspan \n \
       x=\"39\" \n \
       y=\"28\" \n \
       style=\"font-size:18px;\">"

    data1a = \
"  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\" > \n \
     <tspan \n \
       x=\"39\" \n \
       y=\"20\" \n \
       style=\"font-size:18px;\">"

    data2a = \
"</tspan></text> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\" > \n \
     <tspan \n \
       x=\"39\" \n \
       y=\"36\" \n \
       style=\"font-size:18px;\">"

    data3 = \
"</tspan></text> \n \
</svg> \n"

    strings = _(mystring).split(" ",2)
    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    if len(strings) == 1:
        FILE.write(data1)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data1a)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data2a)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data3)
    FILE.close()
    return

if __name__ == "__main__":
    main()
