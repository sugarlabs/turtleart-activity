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

    myname = "if"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("if")
    mystring2 = _("then")
    mygroup = "flow"

    print mystring1
    print mystring2

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   width=\"171\" \n \
   height=\"120\" \n \
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
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#a97513;stroke-width:2;stroke-opacity:1;opacity:1\" \n \
     d=\"M 48,1 C 64,1 64.187817,1 64.187817,1 C 64.187817,1 67.093036,1.8126092 68.09137,2.6369032 C 69.004632,3.3909562 70.42005,6 70.42005,6 L 109,6 L 109,10.362744 C 109,10.362744 95.936038,11.968359 91.234146,14.580971 C 87.185598,16.830552 81.69394,20.427467 79.862644,24.586001 C 78.615904,27.417117 78.754707,32.093211 80.064747,34.895598 C 81.739279,38.477693 86.523166,41.68078 90.010223,43.545156 C 95.034158,46.231233 109,48.539891 109,48.539891 L 109,55 L 163.09536,55 L 167.25404,58.346432 L 170,62.732031 L 170,78 L 165.20874,78 C 165.20874,78 163.93784,75.60092 162.96541,74.858271 C 161.90504,74.048467 159,73 159,73 L 142,73 L 142,78 L 122,78 L 122,73 L 103,73 C 103,73 99.222895,75.806066 98,77 C 96.517521,78.447372 95,82.347563 95,82.347563 L 95,105 L 75.204118,104.90405 C 75.204118,104.90405 73.24214,109.39853 71.78641,110.85394 C 70.354258,112.28578 65.932154,114.215 65.932154,114.215 L 47,114 L 47,119 L 28,119 L 28,114 L 10.924831,114 C 10.924831,114 6.228383,112.0831 4.6063009,110.53995 C 3.3197278,109.31599 1,105.54299 1,105.54299 L 1,10.796801 C 1,10.796801 3.196437,6.3426262 4.5939087,4.7968012 C 5.9621108,3.2833542 10.093909,1 10.093909,1 L 26,1 d L 26,6 L 48,6 L 48,1 z\" /> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"37\" \n \
       y=\"34.5\" \n \
       style=\"font-size:24px\">"

    data1 = \
"</tspan></text> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
     <tspan \n \
       x=\"132\" \n \
       y=\"68.5\" \n \
       style=\"font-size:14px\">"

    data2 = \
"</tspan></text> \n \
</svg> \n"

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname+".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring1.encode("utf-8"))
    FILE.write(data1)
    FILE.write(mystring2.encode("utf-8"))
    FILE.write(data2)
    FILE.close()
    return

if __name__ == "__main__":
    main()
