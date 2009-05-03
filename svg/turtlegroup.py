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

    myname = "turtlegroup"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("clean")
    mystring2 = _("forward")
    mystring3 = _("back")
    mystring4 = _("left")
    mystring5 = _("right")
    mystring6 = _("arc")
    mystring7 = _("angle")
    mystring8 = _("radius")
    mystring9 = _("setyx")
    mystring10 = _("x")
    mystring11 = _("y")
    mystring12 = _("set heading")
    mystring13 = _("xcor")
    mystring14 = _("ycor")
    mystring15 = _("heading")
    mystring16 = _("Turtle")
    mystring17 = _("show")
    mystring18 = _("set scale")
    mystring19 = _("scale")
    mygroup = "turtle"

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
    print mystring15
    print mystring16
    print mystring17
    print mystring18
    print mystring19

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
     id=\"defs103\">\n \
    <linearGradient\n \
       id=\"linearGradient3250\">\n \
      <stop\n \
         id=\"stop3252\"\n \
         style=\"stop-color:#ffffff;stop-opacity:1\"\n \
         offset=\"0\" />\n \
      <stop\n \
         id=\"stop3254\"\n \
         style=\"stop-color:#00ff00;stop-opacity:1\"\n \
         offset=\"1\" />\n \
    </linearGradient>\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"22\"\n \
       x2=\"74\"\n \
       y2=\"22\"\n \
       id=\"linearGradient3256\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"22\"\n \
       x2=\"74\"\n \
       y2=\"22\"\n \
       id=\"linearGradient3258\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"22\"\n \
       x2=\"74\"\n \
       y2=\"22\"\n \
       id=\"linearGradient3260\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"22\"\n \
       x2=\"74\"\n \
       y2=\"22\"\n \
       id=\"linearGradient3264\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"22\"\n \
       x2=\"74\"\n \
       y2=\"22\"\n \
       id=\"linearGradient3267\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"7\"\n \
       y1=\"90\"\n \
       x2=\"56\"\n \
       y2=\"90\"\n \
       id=\"linearGradient3333\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"7\"\n \
       y1=\"130\"\n \
       x2=\"56\"\n \
       y2=\"130\"\n \
       id=\"linearGradient3341\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"79\"\n \
       y1=\"90\"\n \
       x2=\"128\"\n \
       y2=\"90\"\n \
       id=\"linearGradient3349\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"79\"\n \
       y1=\"130\"\n \
       x2=\"128\"\n \
       y2=\"130\"\n \
       id=\"linearGradient3357\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"43\"\n \
       y1=\"181\"\n \
       x2=\"92\"\n \
       y2=\"181\"\n \
       id=\"linearGradient3365\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"7\"\n \
       y1=\"251\"\n \
       x2=\"56\"\n \
       y2=\"251\"\n \
       id=\"linearGradient3373\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"79\"\n \
       y1=\"238\"\n \
       x2=\"128\"\n \
       y2=\"238\"\n \
       id=\"linearGradient3381\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"6\"\n \
       y1=\"303\"\n \
       x2=\"72\"\n \
       y2=\"303\"\n \
       id=\"linearGradient3389\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"89\"\n \
       y1=\"314\"\n \
       x2=\"137\"\n \
       y2=\"314\"\n \
       id=\"linearGradient3397\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"359\"\n \
       x2=\"107\"\n \
       y2=\"359\"\n \
       id=\"linearGradient3405\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"382\"\n \
       x2=\"107\"\n \
       y2=\"382\"\n \
       id=\"linearGradient3413\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"406\"\n \
       x2=\"107\"\n \
       y2=\"406\"\n \
       id=\"linearGradient3421\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"79\"\n \
       y1=\"238\"\n \
       x2=\"128\"\n \
       y2=\"238\"\n \
       id=\"linearGradient2505\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"79\"\n \
       y1=\"238\"\n \
       x2=\"128\"\n \
       y2=\"238\"\n \
       id=\"linearGradient2519\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"37\"\n \
       y1=\"406\"\n \
       x2=\"107\"\n \
       y2=\"406\"\n \
       id=\"linearGradient2527\"\n \
       xlink:href=\"#linearGradient3250\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"0\"\n \
       x2=\"100\"\n \
       y2=\"66\"\n \
       id=\"linearGradient3172\"\n \
       xlink:href=\"#linearGradient3166\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       id=\"linearGradient3166\">\n \
      <stop\n \
         id=\"stop3168\"\n \
         style=\"stop-color:#ffffff;stop-opacity:1\"\n \
         offset=\"0\" />\n \
      <stop\n \
         id=\"stop3170\"\n \
         style=\"stop-color:#00ff00;stop-opacity:1\"\n \
         offset=\"1\" />\n \
    </linearGradient>\n \
  </defs>\n \
  <path\n \
     d=\"M 0.58809792,0.55108212 L 0.52581012,484.98977 L 3.6485499,492.43821 L 8.520663,496.82385 L 15.179825,499.47419 L 128.96395,499.47419 L 135.80997,496.63739 L 141.75709,491.22606 L 144.47996,482.0929 L 144.51764,0.52581012 L 0.58809792,0.55108212 z\"\n \
     id=\"path30\"\n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0\"\n \
     x=\"3.7\"\n \
     y=\"213\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"214.3\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"215\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"65\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"66.5\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"67.5\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-26.9\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-25.8\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-472.7\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"-471.4\"\n \
     transform=\"scale(1,-1)\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 134,491 C 134,492 133,493 132,493 C 131,493 131,492 131,491 C 131,491 131,490 132,490 C 133,490 134,491 134,491 z\"\n \
     id=\"path58\"\n \
     style=\"fill:#fff080;fill-opacity:1;stroke:none;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 80,485 C 80,490 77,493 72,493 C 67,493 64,490 64,485 C 64,481 67,477 72,477 C 77,477 80,481 80,485 L 80,485 z\"\n \
     id=\"path60\"\n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:12px;font-weight:bold;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"68\"\n \
       y=\"489\"\n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\">X</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 79,32 C 90,32 90,32 90,32 L 94,35 L 96,39 L 96,52 L 94,55 L 90,58 L 79,58 L 79,58 L 79,60 L 65,60 L 65,58 L 54,58 L 50,55 L 48,52 L 48,39 L 50,35 L 54,32 L 65,32 L 65,36 L 79,36 L 79,32 z\"\n \
     style=\"fill:url(#linearGradient3267);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"49\"\n \
       style=\"font-size:12\">"

    data1 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 54,77 L 65,77 L 65,81 L 62,81 L 62,79 L 55,79\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 54,95 L 65,95 L 65,91 L 62,91 L 62,93 L 55,93\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 39,73 C 50,73 50,73 50,73 L 53,76 L 56,80 L 56,93 L 53,96 L 50,99 L 38,99 L 38,99 L 38,101 L 25,101 L 25,99 L 14,99 L 10,96 L 8,93 L 8,80 L 10,76 L 14,73 L 24,73 L 24,77 L 39,77 L 39,73 z\"\n \
     style=\"fill:url(#linearGradient3333);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"32\"\n \
       y=\"90\"\n \
       style=\"font-size:12\">"

    data2 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 126,77 L 137,77 L 137,81 L 134,81 L 134,79 L 127,79\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 126,95 L 137,95 L 137,91 L 134,91 L 134,93 L 127,93\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 111,73 C 122,73 122,73 122,73 L 125,76 L 128,80 L 128,93 L 125,96 L 122,99 L 110,99 L 110,99 L 110,101 L 97,101 L 97,99 L 86,99 L 82,96 L 80,93 L 80,80 L 82,76 L 86,73 L 96,73 L 96,77 L 111,77 L 111,73 z\"\n \
     style=\"fill:url(#linearGradient3349);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"104\"\n \
       y=\"90\"\n \
       style=\"font-size:12\">"

    data3 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 54,117 L 65,117 L 65,121 L 62,121 L 62,119 L 55,119\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 54,136 L 65,136 L 65,132 L 62,132 L 62,134 L 55,134\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 39,114 C 50,114 50,114 50,114 L 53,117 L 56,121 L 56,133 L 53,137 L 50,139 L 38,139 L 38,139 L 38,142 L 25,142 L 25,139 L 14,139 L 10,137 L 8,133 L 8,121 L 10,117 L 14,114 L 24,114 L 24,117 L 39,117 L 39,114 z\"\n \
     style=\"fill:url(#linearGradient3341);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"32\"\n \
       y=\"131\"\n \
       style=\"font-size:12\">"

    data4 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 126,117 L 137,117 L 137,121 L 134,121 L 134,119 L 127,119\"\n \
     id=\"path112\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 126,136 L 137,136 L 137,132 L 134,132 L 134,134 L 127,134\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 111,114 C 122,114 122,114 122,114 L 125,117 L 128,121 L 128,133 L 125,137 L 122,139 L 110,139 L 110,139 L 110,142 L 97,142 L 97,139 L 86,139 L 82,137 L 80,133 L 80,121 L 82,117 L 86,114 L 96,114 L 96,117 L 111,117 L 111,114 z\"\n \
     style=\"fill:url(#linearGradient3357);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"104\"\n \
       y=\"131\"\n \
       style=\"font-size:12\">"

    data5 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 89,181 L 100,181 L 100,185 L 98,185 L 98,183 L 91,183\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 89,199 L 100,199 L 100,195 L 98,195 L 98,197 L 91,197\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 90,156 L 101,156 L 101,160 L 98,160 L 98,158 L 91,158\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 90,174 L 101,174 L 101,170 L 98,170 L 98,172 L 91,172\"\n \
     id=\"path130\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 75,153 C 86,153 86,153 86,153 L 89,155 L 92,159 L 92,197 L 89,200 L 86,203 L 74,203 L 74,203 L 74,205 L 61,205 L 61,203 L 50,203 L 46,200 L 44,197 L 44,159 L 46,155 L 50,153 L 60,153 L 60,156 L 75,156 L 75,153 z\"\n \
     style=\"fill:url(#linearGradient3365);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"68\"\n \
       y=\"181\"\n \
       id=\"tspan136\"\n \
       style=\"font-size:12\">"

    data6 = \
"</tspan>\n \
  </text>\n \
  <text\n \
     style=\"font-size:8;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"90\"\n \
       y=\"167\"\n \
       style=\"font-size:9\">"

    data7 = \
"</tspan>\n \
    <tspan\n \
       x=\"90\"\n \
       y=\"196\"\n \
       style=\"font-size:9\">"

    data8 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 53,250 L 64,250 L 64,254 L 62,254 L 62,252 L 55,252\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 53,268 L 64,268 L 64,264 L 62,264 L 62,266 L 55,266\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 54,225 L 65,225 L 65,229 L 62,229 L 62,227 L 55,227\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 54,244 L 65,244 L 65,240 L 62,240 L 62,242 L 55,242\"\n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 39,222 C 50,222 50,222 50,222 L 53,225 L 56,229 L 56,266 L 53,269 L 50,272 L 38,272 L 38,272 L 38,275 L 25,275 L 25,272 L 14,272 L 10,269 L 8,266 L 8,229 L 10,225 L 14,222 L 24,222 L 24,225 L 39,225 L 39,222 z\"\n \
     style=\"fill:url(#linearGradient3373);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:12;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"32\"\n \
       y=\"250\"\n \
       id=\"tspan158\"\n \
       style=\"font-size:12\">"

    data9 = \
"</tspan>\n \
  </text>\n \
  <text\n \
     style=\"font-size:9;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"54\"\n \
       y=\"236\"\n \
       style=\"font-size:9\">"

    data10 = \
"</tspan>\n \
    <tspan\n \
       x=\"54\"\n \
       y=\"265\"\n \
       style=\"font-size:9\">"

    data11 = \
"</tspan>\n \
  </text>\n \
  <g\n \
     transform=\"translate(0,-2)\">\n \
    <path\n \
       d=\"M 126,227 L 137.08348,227 L 137,231 L 134,231 L 134,229 L 127,229\"\n \
       style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 126,246 L 137,246 L 137,242 L 134,242 L 134,244 L 127,244\"\n \
       style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 111,224 C 122,224 122,224 122,224 L 125,227 L 128,231 L 128,243 L 125,247 L 122,250 L 110,250 L 110,250 L 110,252 L 97,252 L 97,250 L 86,250 L 82,247 L 80,243 L 80,231 L 82,227 L 86,224 L 96,224 L 96,227 L 111,227 L 111,224 z\"\n \
       style=\"fill:url(#linearGradient3381);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n"
    data12a = \
"    <text\n \
       style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"104\"\n \
         y=\"241\"\n \
         style=\"font-size:12\">"

    data12b = \
"  <text \n \
     style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"236\" \n \
       style=\"font-size:10.5px\">"

    data13b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"247\" \n \
       style=\"font-size:10.5px\">"

    data14 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <path\n \
     d=\"M 38,379 L 41,379 L 41,382 L 46,382 L 46,379 L 107,379 L 107,393 L 46,393 L 46,390 L 41,390 L 41,393 L 38,393 L 38,379 z\"\n \
     style=\"fill:url(#linearGradient3405);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"390\"\n \
       style=\"font-size:10.5\">"

    data15 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 38,403 L 41,403 L 41,406 L 46,406 L 46,403 L 107,403 L 107,417 L 46,417 L 46,414 L 41,414 L 41,417 L 38,417 L 38,403 z\"\n \
     style=\"fill:url(#linearGradient3413);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"413\"\n \
       style=\"font-size:10.5\">"

    data16 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 38,427 L 41,427 L 41,430 L 46,430 L 46,427 L 107,427 L 107,441 L 46,441 L 46,438 L 41,438 L 41,441 L 38,441 L 38,427 z\"\n \
     style=\"fill:url(#linearGradient3421);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"437\"\n \
       style=\"font-size:10.5px\">"

    data17 = \
"</tspan>\n \
  </text>\n \
  <text\n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"19\"\n \
       style=\"font-size:20px\">"

    data18 = \
"</tspan>\n \
  </text>\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"280.6\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"281.7\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"282.6\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"372.5\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"373.6\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137.5\"\n \
     height=\"0.14\"\n \
     x=\"3.7\"\n \
     y=\"374.6\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" />\n \
  <g\n \
     transform=\"translate(-72,65)\">\n \
    <path\n \
       d=\"M 126,227 L 137,227 L 137,231 L 134,231 L 134,229 L 127,229\"\n \
       style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 126,246 L 137,246 L 137,242 L 134,242 L 134,244 L 127,244\"\n \
       style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 111,224 C 122,224 122,224 122,224 L 125,227 L 128,231 L 128,243 L 125,247 L 122,250 L 110,250 L 110,250 L 110,252 L 97,252 L 97,250 L 86,250 L 82,247 L 80,243 L 80,231 L 82,227 L 86,224 L 96,224 L 96,227 L 111,227 L 111,224 z\"\n \
       style=\"fill:url(#linearGradient2505);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
    <text\n \
       style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"104\"\n \
         y=\"241\"\n \
         style=\"font-size:12\">"

    data19 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <g\n \
     transform=\"translate(0,65)\">\n \
    <path\n \
       d=\"M 126,227 L 137,227 L 137,231 L 134,231 L 134,229 L 127,229\"\n \
       style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 126,246 L 137,246 L 137,242 L 134,242 L 134,244 L 127,244\"\n \
       style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-opacity:1\" />\n \
    <path\n \
       d=\"M 111,224 C 122,224 122,224 122,224 L 125,227 L 128,231 L 128,243 L 125,247 L 122,250 L 110,250 L 110,250 L 110,252 L 97,252 L 97,250 L 86,250 L 82,247 L 80,243 L 80,231 L 82,227 L 86,224 L 96,224 L 96,227 L 111,227 L 111,224 z\"\n \
       style=\"fill:url(#linearGradient2519);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n"

    data19a = \
"    <text\n \
       style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"104\"\n \
         y=\"241\"\n \
         style=\"font-size:12\">"

    data19b = \
"    <text\n \
       style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"104\"\n \
         y=\"236\"\n \
         style=\"font-size:12\">"

    data19c = \
"</tspan>\n \
    </text>\n \
    <text\n \
       style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
      <tspan\n \
         x=\"104\"\n \
         y=\"246\"\n \
         style=\"font-size:12\">"

    data20 = \
"</tspan>\n \
    </text>\n \
  </g>\n \
  <path\n \
     d=\"M 38,451 L 41,451 L 41,454 L 46,454 L 46,451 L 107,451 L 107,465 L 46,465 L 46,462 L 41,462 L 41,465 L 38,465 L 38,451 z\"\n \
     id=\"path2521\"\n \
     style=\"fill:url(#linearGradient2527);fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-opacity:1\" />\n \
  <text\n \
     style=\"font-size:8;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"71\"\n \
       y=\"461\"\n \
       style=\"font-size:10.5\">"

    data21 = \
"</tspan>\n \
  </text>\n \
  <g\n \
     transform=\"matrix(0.67,0,0,0.67,39,323.6)\">\n \
    <path\n \
       d=\"M 1,23.25 L 6,23.25 L 6,27 L 13,27 L 13,1 L 99,1 L 99,65 L 13,65 L 13,37.5 L 6,37.5 L 6,41.5 L 1,41.5 L 1,23.25 z\"\n \
       style=\"fill:url(#linearGradient3172);fill-opacity:1;fill-rule:nonzero;stroke:#00a000;stroke-width:2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1\" />\n \
    <rect\n \
       width=\"75\"\n \
       height=\"54\"\n \
       x=\"19\"\n \
       y=\"6\"\n \
       style=\"opacity:1;fill:#ffffff;fill-opacity:1;stroke:none\" />\n \
  </g>\n \
</svg>"

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring1.encode("utf-8"))
    FILE.write(data1)
    FILE.write(mystring2.encode("utf-8"))
    FILE.write(data2)
    FILE.write(mystring3.encode("utf-8"))
    FILE.write(data3)
    FILE.write(mystring4.encode("utf-8"))
    FILE.write(data4)
    FILE.write(mystring5.encode("utf-8"))
    FILE.write(data5)
    FILE.write(mystring6.encode("utf-8"))
    FILE.write(data6)
    FILE.write(mystring7.encode("utf-8"))
    FILE.write(data7)
    FILE.write(mystring8.encode("utf-8"))
    FILE.write(data8)
    FILE.write(mystring9.encode("utf-8"))
    FILE.write(data9)
    FILE.write(mystring10.encode("utf-8"))
    FILE.write(data10)
    FILE.write(mystring11.encode("utf-8"))
    FILE.write(data11)
    strings = mystring12.split(" ",2)
    if len(strings) == 1:
        FILE.write(data12a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data12b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data13b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data14)
    FILE.write(mystring13.encode("utf-8"))
    FILE.write(data15)
    FILE.write(mystring14.encode("utf-8"))
    FILE.write(data16)
    FILE.write(mystring15.encode("utf-8"))
    FILE.write(data17)
    FILE.write(mystring16.encode("utf-8"))
    FILE.write(data18)
    FILE.write(mystring17.encode("utf-8"))
    FILE.write(data19)
    strings = mystring18.split(" ",2)
    if len(strings) == 1:
        FILE.write(data19a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data19b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data19c)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data20)
    FILE.write(mystring19.encode("utf-8"))
    FILE.write(data21)
    FILE.close()
    return

if __name__ == "__main__":
    main()
