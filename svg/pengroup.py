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

    myname = "pengroup"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("Pen")
    mystring2 = _("pen up")
    mystring3 = _("pen down")
    mystring4 = _("set pen size")
    mystring5 = _("set color")
    mystring6 = _("set shade")
    mystring7 = _("fill screen")
    mystring8 = _("pen size")
    mystring9 = _("color")
    mystring10 = _("shade")
    mystring11 = _("set text size")
    # mystring12 = _("set text color")
    # mystring13 = _("text color")
    mystring14 = _("text size")
    mygroup = "pen"

    print mystring1
    print mystring2
    print mystring3
    print mystring4
    print mystring5
    print mystring6
    print mystring7
    print mystring8
    print mystring9
    print mystring10
    print mystring11
    # print mystring12
    # print mystring13
    print mystring14

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n\
<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\
\n\
<svg\n\
   xmlns:svg=\"http://www.w3.org/2000/svg\"\n\
   xmlns=\"http://www.w3.org/2000/svg\"\n\
   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n\
   version=\"1.0\"\n\
   width=\"145\"\n\
   height=\"500\"\n\
   id=\"svg2\">\n\
  <defs\n\
     id=\"defs4\">\n\
    <linearGradient\n\
       id=\"linearGradient3876\">\n\
      <stop\n\
         id=\"stop3878\"\n\
         style=\"stop-color:#ffffff;stop-opacity:1\"\n\
         offset=\"0\" />\n\
      <stop\n\
         id=\"stop3880\"\n\
         style=\"stop-color:#00ffff;stop-opacity:1\"\n\
         offset=\"1\" />\n\
    </linearGradient>\n\
    <linearGradient\n\
       x1=\"18\"\n\
       y1=\"48\"\n\
       x2=\"67\"\n\
       y2=\"48\"\n\
       id=\"linearGradient4830\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"77\"\n\
       y1=\"48\"\n\
       x2=\"126\"\n\
       y2=\"48\"\n\
       id=\"linearGradient4838\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"95\"\n\
       x2=\"92\"\n\
       y2=\"95\"\n\
       id=\"linearGradient4846\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"147\"\n\
       x2=\"92\"\n\
       y2=\"147\"\n\
       id=\"linearGradient4854\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient4862\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"258\"\n\
       x2=\"92\"\n\
       y2=\"258\"\n\
       id=\"linearGradient4870\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"312\"\n\
       x2=\"107\"\n\
       y2=\"312\"\n\
       id=\"linearGradient4878\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(0,65)\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient4886\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(0,61)\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"362\"\n\
       x2=\"107\"\n\
       y2=\"362\"\n\
       id=\"linearGradient4894\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(0,57)\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient2501\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(0,95)\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"95\"\n\
       x2=\"92\"\n\
       y2=\"95\"\n\
       id=\"linearGradient2560\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"147\"\n\
       x2=\"92\"\n\
       y2=\"147\"\n\
       id=\"linearGradient2562\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient2580\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient2582\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient2584\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(0,95)\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient2598\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"362\"\n\
       x2=\"107\"\n\
       y2=\"362\"\n\
       id=\"linearGradient2600\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"362\"\n\
       x2=\"107\"\n\
       y2=\"362\"\n\
       id=\"linearGradient2627\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient2629\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"362\"\n\
       x2=\"107\"\n\
       y2=\"362\"\n\
       id=\"linearGradient2631\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient2633\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient2521\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient2523\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient2530\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"199\"\n\
       x2=\"92\"\n\
       y2=\"199\"\n\
       id=\"linearGradient2539\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"37\"\n\
       y1=\"337\"\n\
       x2=\"107\"\n\
       y2=\"337\"\n\
       id=\"linearGradient2633-4\"\n\
       xlink:href=\"#linearGradient3876-7\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       id=\"linearGradient3876-7\">\n\
      <stop\n\
         id=\"stop3878-6\"\n\
         style=\"stop-color:#ffffff;stop-opacity:1\"\n\
         offset=\"0\" />\n\
      <stop\n\
         id=\"stop3880-5\"\n\
         style=\"stop-color:#00ffff;stop-opacity:1\"\n\
         offset=\"1\" />\n\
    </linearGradient>\n\
    <linearGradient\n\
       x1=\"77\"\n\
       y1=\"48\"\n\
       x2=\"126\"\n\
       y2=\"48\"\n\
       id=\"linearGradient4087\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(2.054342,4)\" />\n\
    <linearGradient\n\
       x1=\"43\"\n\
       y1=\"95\"\n\
       x2=\"92\"\n\
       y2=\"95\"\n\
       id=\"linearGradient4096\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-33.8333,-2)\" />\n\
    <linearGradient\n\
       x1=\"18\"\n\
       y1=\"48\"\n\
       x2=\"67\"\n\
       y2=\"48\"\n\
       id=\"linearGradient4105\"\n\
       xlink:href=\"#linearGradient3876\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-8,4)\" />\n\
  </defs>\n\
  <path\n\
     d=\"m 0.5,0.5 0,485.5 3.1,6 4.9,4 6.7,3 113.8,0 6.8,-3 6,-4 2.7,-6 0,-485.5 -144,0 z\"\n\
     id=\"path32\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-29\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect40\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-27.799999\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect42\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-474.79999\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect44\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-473.5\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect46\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 80.9,486.4 c 0,4.5 -3.8,8.1 -8.4,8.1 -4.6,0 -8.4,-4.41 -8.4,-8.1 0,-4.5 3.8,-8.1 8.4,-8.1 4.6,0 8.4,3.6 8.4,8.1 l 0,0 z\"\n\
     id=\"path48\"\n\
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" />\n\
  <text\n\
     id=\"text50\"\n\
     style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"68\"\n\
       y=\"491\"\n\
       id=\"tspan52\"\n\
       style=\"font-size:12px;font-weight:bold;fill:#ffffff\">X</tspan>\n\
  </text>\n\
  <text\n\
     id=\"text54\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"72.5\"\n\
       y=\"21\"\n\
       id=\"tspan56\"\n\
       style=\"font-size:20px\">"

    data1 = \
"</tspan>\n\
  </text>\n\
  <path\n\
     d=\"m 42,38 c 10,0 10,0 10,0 0,0 2.932088,1.720414 4,3 0.95517,1.144497 2,4 2,4 l 0,12 c 0,0 -0.945907,2.945907 -2,4 -1.054093,1.054093 -4,2 -4,2 l -11,0 0,0 0,3 -13,0 0,-3 -12,0 c 0,0 -2.126911,-1.17407 -3,-2 -1.210756,-1.145359 -3,-4 -3,-4 l 0,-12 c 0,0 1.419631,-2.919267 2.470149,-4.132463 C 13.462488,39.721531 16,38 16,38 l 11,0 0,3 15,0 0,-3 z\"\n\
     id=\"path60\"\n\
     style=\"fill:url(#linearGradient4105);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
  <text\n\
     x=\"-8\"\n\
     y=\"4\"\n\
     id=\"text49\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"35\"\n\
       y=\"49\"\n\
       id=\"tspan63\"\n\
       style=\"font-size:10px\">"

    data2 = \
"</tspan>\n\
  </text>\n\
  <text\n\
     x=\"-8\"\n\
     y=\"4\"\n\
     id=\"text65\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"35\"\n\
       y=\"59\"\n\
       id=\"tspan67\"\n\
       style=\"font-size:10px\">"

    data3 = \
"</tspan>\n\
  </text>\n\
  <path\n\
     d=\"m 111.05434,38 c 11,0 11,0 11,0 0,0 2.45058,1.535538 3.39739,2.602612 C 126.58219,41.876671 128.05434,45 128.05434,45 l 0,12 c 0,0 -1.78924,2.854641 -3,4 -0.87309,0.82593 -3,2 -3,2 l -12,0 0,0 0,3 -12.999998,0 0,-3 -11,0 c 0,0 -2.945907,-0.945907 -4,-2 -1.054093,-1.054093 -2,-4 -2,-4 l 0,-12 2,-4 4,-3 10,0 0,3 14.999998,0 0,-3 z\"\n\
     id=\"path71\"\n\
     style=\"fill:url(#linearGradient4087);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none\" />\n\
  <text\n\
     x=\"2.054342\"\n\
     y=\"4\"\n\
     id=\"text55\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"103.05434\"\n\
       y=\"49\"\n\
       id=\"tspan74\"\n\
       style=\"font-size:10px\">"

    data4 = \
"</tspan>\n\
  </text>\n\
  <text\n\
     x=\"2.054342\"\n\
     y=\"4\"\n\
     id=\"text76\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"103.05434\"\n\
       y=\"59\"\n\
       id=\"tspan78\"\n\
       style=\"font-size:10px\">"

    data5 = \
"</tspan>\n\
  </text>\n\
  <path\n\
     d=\"m 56.1667,83 11,0 0,4 -3,0 0,-2 -7,0\"\n\
     id=\"path82\"\n\
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 56.1667,101 11,0 0,-4 -3,0 0,2 -7,0\"\n\
     id=\"path84\"\n\
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 41.1667,74 c 11,0 11,0 11,0 0,0 2.126911,1.17407 3,2 1.210756,1.145359 3,4 3,4 l 0,23 c 0,0 -1.643072,3.27076 -2.735075,4.52985 C 54.50503,108.59822 52.1667,110 52.1667,110 l -12,0 0,0 0,2 -13,0 0,-2 -11,0 c 0,0 -2.932088,-1.72041 -4,-3 -0.95517,-1.1445 -2,-4 -2,-4 l 0,-23 c 0,0 0.945907,-2.945907 2,-4 1.054093,-1.054093 4,-2 4,-2 l 10,0 0,3 15,0 0,-3 z\"\n\
     id=\"path86\"\n\
     style=\"fill:url(#linearGradient4096);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none\" />\n\
  <text\n\
     x=\"-33.833302\"\n\
     y=\"-2\"\n\
     id=\"text88\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"34.166698\"\n\
       y=\"87\"\n\
       id=\"tspan90\"\n\
       style=\"font-size:10px\">"

    data6 = \
"</tspan>\n\
  </text>\n\
  <text\n\
     x=\"-33.833302\"\n\
     y=\"-2\"\n\
     id=\"text69\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"34.166698\"\n\
       y=\"96\"\n\
       id=\"tspan93\"\n\
       style=\"font-size:10px\">"

    data7 = \
"</tspan>\n\
  </text>\n\
  <text\n\
     x=\"-33.833302\"\n\
     y=\"-2\"\n\
     id=\"text95\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"34.166698\"\n\
       y=\"106\"\n\
       id=\"tspan97\"\n\
       style=\"font-size:10px\">"

    data8 = \
"</tspan>\n\
  </text>\n\
  <g\n\
     transform=\"translate(-34,-8)\"\n\
     id=\"g99\">\n\
    <path\n\
       d=\"m 90,137 11,0 0,4 -3,0 0,-2 -7,0\"\n\
       id=\"path101\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 90,155 11,0 0,-4 -3,0 0,2 -7,0\"\n\
       id=\"path103\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 75,128 c 11,0 11,0 11,0 0,0 2.126911,1.17407 3,2 1.210756,1.14536 3,4 3,4 l 0,23 c 0,0 -1.378146,3.1383 -2.470149,4.39739 C 88.603256,162.46576 86,164 86,164 l -12,0 0,0 0,2 -13,0 0,-2 -11,0 c 0,0 -2.932088,-1.72041 -4,-3 -0.95517,-1.1445 -2,-4 -2,-4 l 0,-23 c 0,0 0.945907,-2.94591 2,-4 1.054093,-1.05409 4,-2 4,-2 l 10,0 0,3 15,0 0,-3 z\"\n\
       id=\"path105\"\n\
       style=\"fill:url(#linearGradient2562);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       id=\"text79\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"145\"\n\
         id=\"tspan108\"\n\
         style=\"font-size:11px\">"

    data9 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text83\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"158\"\n\
         id=\"tspan111\"\n\
         style=\"font-size:11px\">"

    data10 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(35.887642,-42)\"\n\
     id=\"g113\">\n\
    <path\n\
       d=\"m 90,171 11,0 0,4 -3,0 0,-2 -7,0\"\n\
       id=\"path115\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 90,189 11,0 0,-4 -3,0 0,2 -7,0\"\n\
       id=\"path117\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 75,162 c 11,0 11,0 11,0 0,0 2.656762,1.439 3.529851,2.26493 C 90.740607,165.41029 92,168 92,168 l 0,23 c 0,0 -1.245683,3.40322 -2.337686,4.66231 C 88.735719,196.73068 86,198 86,198 l -12,0 0,0 0,2 -13,0 0,-2 -11,0 c 0,0 -2.932088,-1.72041 -4,-3 -0.95517,-1.1445 -2,-4 -2,-4 l 0,-23 c 0,0 0.945907,-2.94591 2,-4 1.054093,-1.05409 4,-2 4,-2 l 10,0 0,3 15,0 0,-3 z\"\n\
       id=\"path119\"\n\
       style=\"fill:url(#linearGradient2539);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       id=\"text93\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"177\"\n\
         id=\"tspan95\"\n\
         style=\"font-size:11px\">"

    data11 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text97\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"190\"\n\
         id=\"tspan99\"\n\
         style=\"font-size:11px\">"

    data12 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(0,-66)\"\n\
     id=\"g125\">\n\
    <path\n\
       d=\"m 89,260 11,0 0,4 -2,0 0,-2 -7,0\"\n\
       id=\"path127\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 89,278 11,0 0,-4 -2,0 0,2 -7,0\"\n\
       id=\"path129\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 90,235 11,0 0,4 -3,0 0,-2 -7,0\"\n\
       id=\"path131\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 90,253 11,0 0,-4 -3,0 0,2 -7,0\"\n\
       id=\"path133\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n\
    <path\n\
       d=\"m 75,232 c 11,0 11,0 11,0 l 3,2 3,4 0,38 -3,3 -3,3 -12,0 0,0 0,2 -13,0 0,-2 -11,0 -4,-3 -2,-3 0,-38 2,-4 4,-2 10,0 0,3 15,0 0,-3 z\"\n\
       id=\"path135\"\n\
       style=\"fill:url(#linearGradient4870);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       id=\"text111\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"255\"\n\
         id=\"tspan113\"\n\
         style=\"font-size:11px\">"

    data13 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text115\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"268\"\n\
         id=\"tspan117\"\n\
         style=\"font-size:11px\">"

    data14 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text119\"\n\
       style=\"font-size:12px;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"91\"\n\
         y=\"243\"\n\
         id=\"tspan121\"\n\
         style=\"font-size:8px\">"

    data15 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text123\"\n\
       style=\"font-size:12px;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"91\"\n\
         y=\"277\"\n\
         id=\"tspan125\"\n\
         style=\"font-size:8px\">"

    data16 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(0,-136)\"\n\
     id=\"g145\">\n\
    <path\n\
       d=\"m 37,372 4,0 0,2 4,0 0,-2 62,0 0,13 -62,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
       id=\"path147\"\n\
       style=\"fill:url(#linearGradient4878);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       x=\"4\"\n\
       y=\"65\"\n\
       id=\"text149\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"76\"\n\
         y=\"381\"\n\
         id=\"tspan151\"\n\
         style=\"font-size:10.5px\">"

    data17 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(0,-136)\"\n\
     id=\"g153\">\n\
    <path\n\
       d=\"m 37,393 4,0 0,2 4,0 0,-2 62,0 0,13 -62,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
       id=\"path155\"\n\
       style=\"fill:url(#linearGradient2633);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       x=\"4\"\n\
       y=\"61\"\n\
       id=\"text157\"\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"76\"\n\
         y=\"402\"\n\
         id=\"tspan159\"\n\
         style=\"font-size:10.5px\">"

    data18 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(0,-135)\"\n\
     id=\"g161\">\n\
    <path\n\
       d=\"m 37,413 4,0 0,3 4,0 0,-3 62,0 0,14 -62,0 0,-3 -4,0 0,3 -4,0 0,-14 z\"\n\
       id=\"path163\"\n\
       style=\"fill:url(#linearGradient2631);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       x=\"4\"\n\
       y=\"57\"\n\
       id=\"text165\"\n\
       style=\"font-size:10px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"76\"\n\
         y=\"423\"\n\
         id=\"tspan167\"\n\
         style=\"font-size:10.5px\">"

    data19 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(35.887642,-226.1667)\"\n\
     id=\"g169\">\n\
    <path\n\
       d=\"m 90,309 11,0 0,4 -2,0 0,-2 -8,0\"\n\
       id=\"path171\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none\" />\n\
    <path\n\
       d=\"m 90,327 11,0 0,-4 -2,0 0,2 -8,0\"\n\
       id=\"path173\"\n\
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none\" />\n\
    <path\n\
       d=\"m 75,300 c 11,0 11,0 11,0 0,0 2.945907,0.94591 4,2 1.054093,1.05409 2,4 2,4 l 0,23 c 0,0 -1.04483,2.8555 -2,4 -1.067912,1.27959 -4,3 -4,3 l -11,0 0,0 0,3 -14,0 0,-3 -11,0 c 0,0 -2.932088,-1.72041 -4,-3 -0.95517,-1.1445 -2,-4 -2,-4 l 0,-23 c 0,0 0.945907,-2.94591 2,-4 1.054093,-1.05409 4,-2 4,-2 l 11,0 0,3 14,0 0,-3 z\"\n\
       id=\"path175\"\n\
       style=\"fill:url(#linearGradient2584);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none\" />\n\
    <text\n\
       id=\"text177\"\n\
       style=\"font-size:10px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"314\"\n\
         id=\"tspan179\"\n\
         style=\"font-size:10.5px\">"

    data20 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text181\"\n\
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"323\"\n\
         id=\"tspan183\"\n\
         style=\"font-size:10.5px\">"

    data21 = \
"</tspan>\n\
    </text>\n\
    <text\n\
       id=\"text185\"\n\
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"68\"\n\
         y=\"332\"\n\
         id=\"tspan187\"\n\
         style=\"font-size:10.5px\">"

    data22 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(0,-156)\"\n\
     id=\"g217\">\n\
    <path\n\
       d=\"m 37,456 4,0 0,3 4,0 0,-3 62,0 0,14 -62,0 0,-3 -4,0 0,3 -4,0 0,-14 z\"\n\
       id=\"path219\"\n\
       style=\"fill:url(#linearGradient2627);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       id=\"text221\"\n\
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"76\"\n\
         y=\"466\"\n\
         id=\"tspan223\"\n\
         style=\"font-size:10.5px\">"

    data23 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <path\n\
     d=\"m 37.5,371.92597 4,0 0,2 4,0 0,-2 62,0 0,13 -62,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9\"\n\
     style=\"fill:#ffff00;fill-opacity:1;stroke:#ffff00;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 37.499995,391.09974 4,0 0,2 4,0 0,-2 62.000015,0 0,13 -62.000015,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9-4\"\n\
     style=\"fill:#00ff00;fill-opacity:1;stroke:#00ff00;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 37.499995,411.12887 4,0 0,2 4,0 0,-2 62.000015,0 0,13 -62.000015,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9-5\"\n\
     style=\"fill:#00ffff;fill-opacity:1;stroke:#00ffff;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 37.499995,430.30264 4,0 0,2 4,0 0,-2 62.000015,0 0,13 -62.000015,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9-4-2\"\n\
     style=\"fill:#0000ff;fill-opacity:1;stroke:#0000ff;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 37.499995,450.84918 4,0 0,2 4,0 0,-2 62.000015,0 0,13 -62.000015,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9-47\"\n\
     style=\"fill:#ff00ff;fill-opacity:1;stroke:#ff00ff;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 37.5,331.07232 4,0 0,2 4,0 0,-2 62,0 0,13 -62,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9-4-0\"\n\
     style=\"fill:#ff0000;fill-opacity:1;stroke:#ff0000;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"m 37.5,351.10145 4,0 0,2 4,0 0,-2 62,0 0,13 -62,0 0,-3 -4,0 0,3 -4,0 0,-13 z\"\n\
     id=\"path155-9-5-7\"\n\
     style=\"fill:#ff8000;fill-opacity:1;stroke:#ff8000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-323.66998\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect40-8\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-322.47\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect42-6\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-226.66998\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect40-8-9\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-225.47\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect42-6-2\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
</svg>\n"

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring1.encode("utf-8"))
    FILE.write(data1)
    strings = mystring2.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data2)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data3)
    strings = mystring3.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data4)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data5)
    strings = mystring4.split(" ",3)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data6)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data7)
    if len(strings) > 2:
        FILE.write(strings[2].encode("utf-8"))
    FILE.write(data8)
    strings = mystring5.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data9)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data10)
    strings = mystring6.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data11)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data12)
    strings = mystring7.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data13)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data14)
    FILE.write(mystring9.encode("utf-8"))
    FILE.write(data15)
    FILE.write(mystring10.encode("utf-8"))
    FILE.write(data16)
    FILE.write(mystring8.encode("utf-8"))
    FILE.write(data17)
    FILE.write(mystring14.encode("utf-8"))
    FILE.write(data18)
    FILE.write(mystring9.encode("utf-8"))
    FILE.write(data19)
    strings = mystring11.split(" ",3)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data20)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data21)
    if len(strings) > 2:
        FILE.write(strings[2].encode("utf-8"))
    FILE.write(data22)
    FILE.write(mystring10.encode("utf-8"))
    FILE.write(data23)
    FILE.close()
    return

if __name__ == "__main__":
    main()
