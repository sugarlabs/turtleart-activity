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
    mystring12 = _("set text color")
    mystring13 = _("text color")
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
    print mystring12
    print mystring13
    print mystring14

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n \
<!-- Created with Inkscape (http://www.inkscape.org/) -->\n \
<svg\n \
   xmlns:svg=\"http://www.w3.org/2000/svg\"\n \
   xmlns=\"http://www.w3.org/2000/svg\"\n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n \
   version=\"1.0\"\n \
   width=\"145\"\n \
   height=\"500\"\n \
   id=\"svg2\">\n \
  <defs\n \
     id=\"defs4\">\n \
    <linearGradient\n \
       id=\"linearGradient3876\">\n \
      <stop\n \
         id=\"stop3878\"\n \
         style=\"stop-color:#ffffff;stop-opacity:1\"\n \
         offset=\"0\" />\n \
      <stop\n \
         id=\"stop3880\"\n \
         style=\"stop-color:#00ffff;stop-opacity:1\"\n \
         offset=\"1\" />\n \
    </linearGradient>\n \
    <linearGradient\n \
       x1=\"18\"\n \
       y1=\"48\"\n \
       x2=\"67\"\n \
       y2=\"48\"\n \
       id=\"linearGradient4830\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"77\"\n \
       y1=\"48\"\n \
       x2=\"126\"\n \
       y2=\"48\"\n \
       id=\"linearGradient4838\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"95\"\n \
       x2=\"92\"\n \
       y2=\"95\"\n \
       id=\"linearGradient4846\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"147\"\n \
       x2=\"92\"\n \
       y2=\"147\"\n \
       id=\"linearGradient4854\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient4862\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"258\"\n \
       x2=\"92\"\n \
       y2=\"258\"\n \
       id=\"linearGradient4870\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"312\"\n \
       x2=\"107\"\n \
       y2=\"312\"\n \
       id=\"linearGradient4878\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,65)\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"337\"\n \
       x2=\"107\"\n \
       y2=\"337\"\n \
       id=\"linearGradient4886\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,61)\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"362\"\n \
       x2=\"107\"\n \
       y2=\"362\"\n \
       id=\"linearGradient4894\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,57)\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"337\"\n \
       x2=\"107\"\n \
       y2=\"337\"\n \
       id=\"linearGradient2501\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,95)\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"95\"\n \
       x2=\"92\"\n \
       y2=\"95\"\n \
       id=\"linearGradient2560\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"147\"\n \
       x2=\"92\"\n \
       y2=\"147\"\n \
       id=\"linearGradient2562\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient2580\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient2582\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"337\"\n \
       x2=\"107\"\n \
       y2=\"337\"\n \
       id=\"linearGradient2584\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,95)\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"337\"\n \
       x2=\"107\"\n \
       y2=\"337\"\n \
       id=\"linearGradient2598\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"362\"\n \
       x2=\"107\"\n \
       y2=\"362\"\n \
       id=\"linearGradient2600\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"362\"\n \
       x2=\"107\"\n \
       y2=\"362\"\n \
       id=\"linearGradient2627\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"337\"\n \
       x2=\"107\"\n \
       y2=\"337\"\n \
       id=\"linearGradient2629\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"362\"\n \
       x2=\"107\"\n \
       y2=\"362\"\n \
       id=\"linearGradient2631\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"337\"\n \
       x2=\"107\"\n \
       y2=\"337\"\n \
       id=\"linearGradient2633\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient2521\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient2523\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient2530\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"199\"\n \
       x2=\"92\"\n \
       y2=\"199\"\n \
       id=\"linearGradient2539\"\n \
       xlink:href=\"#linearGradient3876\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
  </defs>\n \
  <path\n \
     d=\"M 0.5,0.5 L 0.5,486 L 3.6,492 L 8.5,496 L 15.2,499 L 129,499 L 135.8,496 L 141.8,492 L 144.5,486 L 144.5,0.5 L 0.5,0.5 z\"\n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123.6\"\n \
     height=\"0.14\"\n \
     x=\"10.7\"\n \
     y=\"363\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123.6\"\n \
     height=\"0.14\"\n \
     x=\"10.7\"\n \
     y=\"364\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123.6\"\n \
     height=\"0.14\"\n \
     x=\"10.7\"\n \
     y=\"365\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-29\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-27.799999\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-474.79999\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-473.5\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 80.9,486.4 C 80.9,490.9 77.1,494.5 72.5,494.5 C 67.9,494.5 64.1,490.09 64.1,486.4 C 64.1,481.9 67.9,478.3 72.5,478.3 C 77.1,478.3 80.9,481.9 80.9,486.4 L 80.9,486.4 z\"\n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"68\"\n \
       y=\"491\"\n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff\">X</tspan>\n \
  </text>\n \
  <text\n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72.5\"\n \
       y=\"21\"\n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan>\n \
  </text>\n \
  <g>\n \
    <path\n \
       d=\"M 50,34 C 60,34 60,34 60,34 L 64,37 L 66,41 L 66,53 L 64,57 L 60,59 L 49,59 L 49,59 L 49,62 L 36,62 L 36,59 L 24,59 L 21,57 L 18,53 L 18,41 L 21,37 L 24,34 L 35,34 L 35,37 L 50,37 L 50,34 z\"\n \
       style=\"fill:url(#linearGradient4830);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n"

    data2a = \
"    <text\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"43\"\n \
         y=\"51.5\"\n \
         style=\"font-size:11px\">"

    data2b = \
"  <text \n \
     id=\"text49\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"43\" \n \
       y=\"45\" \n \
       style=\"font-size:10px\">"

    data3b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text49\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"43\" \n \
       y=\"55\" \n \
       style=\"font-size:10px\">"

    data4 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g>\n \
    <path\n \
       d=\"M 109,34 C 120,34 120,34 120,34 L 123,37 L 126,41 L 126,53 L 123,57 L 120,59 L 108,59 L 108,59 L 108,62 L 95,62 L 95,59 L 84,59 L 80,57 L 78,53 L 78,41 L 80,37 L 84,34 L 94,34 L 94,37 L 109,37 L 109,34 z\"\n \
       style=\"fill:url(#linearGradient4838);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" />\n"

    data5a = \
"    <text\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"101\"\n \
         y=\"51.5\"\n \
         style=\"font-size:11px\">"

    data5b = \
"  <text \n \
     id=\"text55\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"101\" \n \
       y=\"45\" \n \
       style=\"font-size:10px\">"

    data6b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text55\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"101\" \n \
       y=\"55\" \n \
       style=\"font-size:10px\">"

    data7 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-6)\">\n \
    <path\n \
       d=\"M 90,85 L 101,85 L 101,89 L 98,89 L 98,87 L 91,87\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,103 L 101,103 L 101,99 L 98,99 L 98,101 L 91,101\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 75,76 C 86,76 86,76 86,76 L 89,78 L 92,82 L 92,105 L 89,109 L 86,112 L 74,112 L 74,112 L 74,114 L 61,114 L 61,112 L 50,112 L 46,109 L 44,105 L 44,82 L 46,78 L 50,76 L 60,76 L 60,79 L 75,79 L 75,76 z\"\n \
       style=\"fill:url(#linearGradient2560);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" />\n"

    data8a = \
"    <text\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"93\"\n \
         style=\"font-size:11px\">"

    data8b = \
"  <text \n \
     id=\"text65\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"93\" \n \
       style=\"font-size:11px\">"

    data8c = \
"  <text \n \
     id=\"text65\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"89\" \n \
       style=\"font-size:10px\">"

    data9b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text69\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"106\" \n \
       style=\"font-size:11px\">"

    data9c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text69\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"98\" \n \
       style=\"font-size:10px\">"

    data10c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text69\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"108\" \n \
       style=\"font-size:10px\">"

    data11 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-12)\">\n \
    <path\n \
       d=\"M 90,137 L 101,137 L 101,141 L 98,141 L 98,139 L 91,139\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,155 L 101,155 L 101,151 L 98,151 L 98,153 L 91,153\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 75,128 C 86,128 86,128 86,128 L 89,130 L 92,134 L 92,157 L 89,161 L 86,164 L 74,164 L 74,164 L 74,166 L 61,166 L 61,164 L 50,164 L 46,161 L 44,157 L 44,134 L 46,130 L 50,128 L 60,128 L 60,131 L 75,131 L 75,128 z\"\n \
       style=\"fill:url(#linearGradient2562);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n"

    data12a = \
"    <text\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"151\"\n \
         style=\"font-size:11px\">"

    data12b = \
"  <text \n \
     id=\"text79\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"145\" \n \
       style=\"font-size:11px\">"

    data13b =\
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text83\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"158\" \n \
       style=\"font-size:11px\">"

    data14 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g>\n \
    <path\n \
       d=\"M 90,171 L 101,171 L 101,175 L 98,175 L 98,173 L 91,173\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,189 L 101,189 L 101,185 L 98,185 L 98,187 L 91,187\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 75,162 C 86,162 86,162 86,162 L 89,164 L 92,168 L 92,191 L 89,195 L 86,198 L 74,198 L 74,198 L 74,200 L 61,200 L 61,198 L 50,198 L 46,195 L 44,191 L 44,168 L 46,164 L 50,162 L 60,162 L 60,165 L 75,165 L 75,162 z\"\n \
       style=\"fill:url(#linearGradient2539);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n"

    data15a = \
"    <text\n \
       y=\"-18\"\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"184\"\n \
         style=\"font-size:11px\">"

    data15b = \
"  <text \n \
     id=\"text93\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"177\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:11px\">"

    data16b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text97\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"190\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:11px\">"

    data17 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-24)\">\n \
    <path\n \
       d=\"M 89,260 L 100,260 L 100,264 L 98,264 L 98,262 L 91,262\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 89,278 L 100,278 L 100,274 L 98,274 L 98,276 L 91,276\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,235 L 101,235 L 101,239 L 98,239 L 98,237 L 91,237\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,253 L 101,253 L 101,249 L 98,249 L 98,251 L 91,251\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 75,232 C 86,232 86,232 86,232 L 89,234 L 92,238 L 92,276 L 89,279 L 86,282 L 74,282 L 74,282 L 74,284 L 61,284 L 61,282 L 50,282 L 46,279 L 44,276 L 44,238 L 46,234 L 50,232 L 60,232 L 60,235 L 75,235 L 75,232 z\"\n \
       style=\"fill:url(#linearGradient4870);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n \
  <text \n \
     id=\"text111\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"255\" \n \
       id=\"tspan113\" \n \
       style=\"font-size:11px\">"

    data18 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text115\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"268\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:11px\">"

    data19 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text119\" \n \
     style=\"font-size:12px;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"91\" \n \
       y=\"243\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:8px\">"

    data20 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text123\" \n \
     style=\"font-size:12px;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"91\" \n \
       y=\"277\" \n \
       id=\"tspan125\" \n \
       style=\"font-size:8px\">"

    data21 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-2)\">\n \
    <path\n \
       d=\"M 37,372 L 41,372 L 41,374 L 45,374 L 45,372 L 107,372 L 107,385 L 45,385 L 45,382 L 41,382 L 41,385 L 37,385 L 37,372 z\"\n \
       style=\"fill:url(#linearGradient4878);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n \
    <text\n \
       x=\"4\"\n \
       y=\"65\"\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"76\"\n \
         y=\"381\"\n \
         style=\"font-size:10.5\">"

    data22 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-2)\">\n \
    <path\n \
       d=\"M 37,393 L 41,393 L 41,395 L 45,395 L 45,393 L 107,393 L 107,406 L 45,406 L 45,403 L 41,403 L 41,406 L 37,406 L 37,393 z\"\n \
       style=\"fill:url(#linearGradient2633);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n \
    <text\n \
       x=\"4\"\n \
       y=\"61\"\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"76\"\n \
         y=\"402\"\n \
         style=\"font-size:10.5\">"

    data23 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-1)\">\n \
    <path\n \
       d=\"M 37,413 L 41,413 L 41,416 L 45,416 L 45,413 L 107,413 L 107,427 L 45,427 L 45,424 L 41,424 L 41,427 L 37,427 L 37,413 z\"\n \
       style=\"fill:url(#linearGradient2631);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n \
    <text\n \
       x=\"4\"\n \
       y=\"57\"\n \
       style=\"font-size:10px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"76\"\n \
         y=\"423\"\n \
         style=\"font-size:10.5\">"

    data24 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-30)\">\n \
    <path\n \
       d=\"M 90,309 L 101,309 L 101,313 L 99,313 L 99,311 L 91,311\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,327 L 101,327 L 101,323 L 99,323 L 99,325 L 91,325\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 75,300 C 86,300 86,300 86,300 L 90,302 L 92,306 L 92,329 L 90,333 L 86,336 L 75,336 L 75,336 L 75,339 L 61,339 L 61,336 L 50,336 L 46,333 L 44,329 L 44,306 L 46,302 L 50,300 L 61,300 L 61,303 L 75,303 L 75,300 z\"\n \
       style=\"fill:url(#linearGradient2584);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
    <text\n \
       style=\"font-size:10;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"314\"\n \
         style=\"font-size:10.5\">"

    data25 = \
"</tspan>\n \
    </text>\n \
    <text\n \
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"323\"\n \
         style=\"font-size:10.5px\">"

    data26 = \
"</tspan>\n \
    </text>\n \
    <text\n \
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"332\"\n \
         style=\"font-size:10.5px\">"

    data27 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,18)\">\n \
    <path\n \
       d=\"M 90,309 L 101,309 L 101,313 L 99,313 L 99,311 L 91,311\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 90,327 L 101,327 L 101,323 L 99,323 L 99,325 L 91,325\"\n \
       style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 75,300 C 86,300 86,300 86,300 L 90,302 L 92,306 L 92,329 L 90,333 L 86,336 L 75,336 L 75,336 L 75,339 L 61,339 L 61,336 L 50,336 L 46,333 L 44,329 L 44,306 L 46,302 L 50,300 L 61,300 L 61,303 L 75,303 L 75,300 z\"\n \
       style=\"fill:url(#linearGradient2501);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
    <text\n \
       style=\"font-size:10.5;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"314\"\n \
         style=\"font-size:10.5\">"

    data28 = \
"</tspan>\n \
    </text>\n \
    <text\n \
       style=\"font-size:10.5;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"323\"\n \
         style=\"font-size:10.5px\">"

    data29 = \
"</tspan>\n \
    </text>\n \
    <text\n \
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"68\"\n \
         y=\"332\"\n \
         style=\"font-size:10.5px\">"

    data30 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-2)\">\n \
    <path\n \
       d=\"M 37,435 L 41,435 L 41,438 L 45,438 L 45,435 L 107,435 L 107,449 L 45,449 L 45,446 L 41,446 L 41,449 L 37,449 L 37,435 z\"\n \
       style=\"fill:url(#linearGradient2629);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n \
    <text\n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"76\"\n \
         y=\"445\"\n \
         style=\"font-size:10.5px\">"

    data31 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,-2)\">\n \
    <path\n \
       d=\"M 37,456 L 41,456 L 41,459 L 45,459 L 45,456 L 107,456 L 107,470 L 45,470 L 45,467 L 41,467 L 41,470 L 37,470 L 37,456 z\"\n \
       style=\"fill:url(#linearGradient2627);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" />\n \
    <text\n \
       style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"76\"\n \
         y=\"466\"\n \
         style=\"font-size:10.5\">"

    data32 = \
"</tspan> \n \
  </text> \n \
  </g>\n \
</svg> \n "


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring1.encode("utf-8"))
    FILE.write(data1)
    strings = mystring2.split(" ",3)
    if len(strings) == 1:
        FILE.write(data2a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data2b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data3b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data4)
    strings = mystring3.split(" ",3)
    if len(strings) == 1:
        FILE.write(data5a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data5b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data6b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data7)
    strings = mystring4.split(" ",3)
    if len(strings) == 1:
        FILE.write(data8a)
        FILE.write(strings[0].encode("utf-8"))
    elif len(strings) == 2:
        FILE.write(data8b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data9b)
        FILE.write(strings[1].encode("utf-8"))
    else:
        FILE.write(data8c)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data9c)
        FILE.write(strings[1].encode("utf-8"))
        FILE.write(data10c)
        FILE.write(strings[2].encode("utf-8"))
        if len(strings) > 3:
            FILE.write(" " + strings[3].encode("utf-8"))
    FILE.write(data11)
    strings = mystring5.split(" ",3)
    if len(strings) == 1:
        FILE.write(data12a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data12b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data13b)
        FILE.write(strings[1].encode("utf-8"))
    if len(strings) > 2:
        FILE.write(" " + strings[2].encode("utf-8"))
    FILE.write(data14)
    strings = mystring6.split(" ",3)
    if len(strings) == 1:
        FILE.write(data15a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data15b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data16b)
        FILE.write(strings[1].encode("utf-8"))
    if len(strings) > 2:
        FILE.write(" " + strings[2].encode("utf-8"))
    FILE.write(data17)
    strings = mystring7.split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data18)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    if len(strings) > 2:
        FILE.write(" " + strings[2].encode("utf-8"))
    FILE.write(data19)
    FILE.write(mystring9.encode("utf-8"))
    FILE.write(data20)
    FILE.write(mystring10.encode("utf-8"))
    FILE.write(data21)
    FILE.write(mystring8.encode("utf-8"))
    FILE.write(data22)
    FILE.write(mystring9.encode("utf-8"))
    FILE.write(data23)
    FILE.write(mystring10.encode("utf-8"))
    FILE.write(data24)
    strings = mystring11.split(" ",3)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data25)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data26)
    if len(strings) > 2:
        FILE.write(strings[2].encode("utf-8"))
    FILE.write(data27)
    strings = mystring12.split(" ",3)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data28)
    if len(strings) > 1:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data29)
    if len(strings) > 2:
        FILE.write(strings[2].encode("utf-8"))
    FILE.write(data30)
    FILE.write(mystring13.encode("utf-8"))
    FILE.write(data31)
    FILE.write(mystring14.encode("utf-8"))
    FILE.write(data32)
    FILE.close()
    return

if __name__ == "__main__":
    main()
