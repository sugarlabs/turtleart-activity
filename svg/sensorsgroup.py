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

    myname = "sensorsgroup"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("Extras")
    mystring2 = _("read key")
    mystring3 = _("keyboard")
    mystring4 = _("width")
    mystring5 = _("height")
    mystring6 = _("pop")
    mystring7 = _("show heap")
    mystring8 = _("empty heap")
    mystring9 = _("push")
    mystring10 = _("left")
    mystring11 = _("top")
    mystring12 = _("right")
    mystring13 = _("bottom")
    mygroup = "sensors"

    print mystring1
    print mystring2
    s3 = mystring1
    s3lower = s3.lower()
    print s3lower
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


    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n\
<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\
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
       id=\"linearGradient3712\">\n\
      <stop\n\
         id=\"stop3714\"\n\
         style=\"stop-color:#ffffff;stop-opacity:1\"\n\
         offset=\"0\" />\n\
      <stop\n\
         id=\"stop3716\"\n\
         style=\"stop-color:#ff0000;stop-opacity:1\"\n\
         offset=\"1\" />\n\
    </linearGradient>\n\
    <linearGradient\n\
       x1=\"69\"\n\
       y1=\"226\"\n\
       x2=\"140\"\n\
       y2=\"226\"\n\
       id=\"linearGradient2431\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524281,-133.82775)\" />\n\
    <linearGradient\n\
       x1=\"0\"\n\
       y1=\"22\"\n\
       x2=\"74\"\n\
       y2=\"22\"\n\
       id=\"linearGradient3208\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"matrix(0.67,0,0,0.67,47.71,36.248183)\" />\n\
    <linearGradient\n\
       x1=\"69\"\n\
       y1=\"226\"\n\
       x2=\"140\"\n\
       y2=\"226\"\n\
       id=\"linearGradient2505\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524278,106.11408)\" />\n\
    <linearGradient\n\
       x1=\"69.85585\"\n\
       y1=\"226.65366\"\n\
       x2=\"140.1927\"\n\
       y2=\"226.65366\"\n\
       id=\"linearGradient2507\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524276,132.44905)\" />\n\
    <linearGradient\n\
       x1=\"0\"\n\
       y1=\"22\"\n\
       x2=\"74\"\n\
       y2=\"22\"\n\
       id=\"linearGradient2513\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"matrix(0.5,0,0,0.5,34.0625,146.60834)\" />\n\
    <linearGradient\n\
       x1=\"34.0625\"\n\
       y1=\"156.60834\"\n\
       x2=\"110.9375\"\n\
       y2=\"156.60834\"\n\
       id=\"linearGradient3199\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"34.0625\"\n\
       y1=\"156.60834\"\n\
       x2=\"110.9375\"\n\
       y2=\"156.60834\"\n\
       id=\"linearGradient3209\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"34.0625\"\n\
       y1=\"156.60834\"\n\
       x2=\"110.9375\"\n\
       y2=\"156.60834\"\n\
       id=\"linearGradient3213\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"34.0625\"\n\
       y1=\"156.60834\"\n\
       x2=\"110.9375\"\n\
       y2=\"156.60834\"\n\
       id=\"linearGradient3219\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"34.0625\"\n\
       y1=\"156.60834\"\n\
       x2=\"110.9375\"\n\
       y2=\"156.60834\"\n\
       id=\"linearGradient3222\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"34.0625\"\n\
       y1=\"156.60834\"\n\
       x2=\"110.9375\"\n\
       y2=\"156.60834\"\n\
       id=\"linearGradient3225\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\" />\n\
    <linearGradient\n\
       x1=\"0\"\n\
       y1=\"22\"\n\
       x2=\"74\"\n\
       y2=\"22\"\n\
       id=\"linearGradient3318\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"matrix(0.67,0,0,0.67,15.710001,283.04264)\" />\n\
    <linearGradient\n\
       x1=\"0\"\n\
       y1=\"22\"\n\
       x2=\"74\"\n\
       y2=\"22\"\n\
       id=\"linearGradient3320\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"matrix(0.67,0,0,0.67,77.710001,282.90001)\" />\n\
    <linearGradient\n\
       x1=\"69\"\n\
       y1=\"226\"\n\
       x2=\"140\"\n\
       y2=\"226\"\n\
       id=\"linearGradient3322\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-33.02428,30.4667)\" />\n\
    <linearGradient\n\
       x1=\"0\"\n\
       y1=\"22\"\n\
       x2=\"74\"\n\
       y2=\"22\"\n\
       id=\"linearGradient3452\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"matrix(0.67,0,0,0.67,43.3125,226.87273)\" />\n\
    <linearGradient\n\
       x1=\"0\"\n\
       y1=\"22\"\n\
       x2=\"74\"\n\
       y2=\"22\"\n\
       id=\"linearGradient3338\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"matrix(0.67,0,0,0.67,43.33,112.19)\" />\n\
    <linearGradient\n\
       x1=\"69\"\n\
       y1=\"226\"\n\
       x2=\"140\"\n\
       y2=\"226\"\n\
       id=\"linearGradient3510\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524279,130.83345)\" />\n\
    <linearGradient\n\
       x1=\"69.85585\"\n\
       y1=\"226.65366\"\n\
       x2=\"140.1927\"\n\
       y2=\"226.65366\"\n\
       id=\"linearGradient3512\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524276,196.22361)\" />\n\
    <linearGradient\n\
       x1=\"69\"\n\
       y1=\"226\"\n\
       x2=\"140\"\n\
       y2=\"226\"\n\
       id=\"linearGradient3514\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524279,174.35571)\" />\n\
    <linearGradient\n\
       x1=\"69.85585\"\n\
       y1=\"226.65366\"\n\
       x2=\"140.1927\"\n\
       y2=\"226.65366\"\n\
       id=\"linearGradient3516\"\n\
       xlink:href=\"#linearGradient3712\"\n\
       gradientUnits=\"userSpaceOnUse\"\n\
       gradientTransform=\"translate(-32.524276,152.70135)\" />\n\
  </defs>\n\
  <path\n\
     d=\"M 0.4344301,0.5 L 0.37211997,486.41023 L 3.4959793,493.14297 L 8.369839,497.1072 L 15.031388,499.50288 L 128.8563,499.50288 L 135.70478,496.93866 L 141.65403,492.04729 L 144.37788,483.79171 L 144.41557,0.5 L 0.4344301,0.5 z\"\n\
     id=\"path23\"\n\
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1px;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 79.5,438.375 C 79.5,442.86231 75.750385,446.5 71.125,446.5 C 66.499615,446.5 62.75,442.86231 62.75,438.375 C 62.75,433.88769 66.499615,430.25 71.125,430.25 C 75.750385,430.25 79.5,433.88769 79.5,438.375 L 79.5,438.375 z\"\n\
     transform=\"translate(1.375,47.250977)\"\n\
     id=\"path39\"\n\
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" />\n\
  <text\n\
     id=\"text41\"\n\
     style=\"font-size:12px;font-variant:normal;font-weight:bold;text-align:start;text-anchor:start;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:1px;stroke-opacity:1;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"68\"\n\
       y=\"490\"\n\
       id=\"tspan43\"\n\
       style=\"font-size:12px\">X</tspan>\n\
  </text>\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-28.9\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect15\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-27.8\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect17\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-340.7\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect19\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.7\"\n\
     y=\"-339.4\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect4001\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <text\n\
     id=\"text28\"\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"72.5\"\n\
       y=\"21.5\"\n\
       id=\"tspan30\"\n\
       style=\"font-size:20px\">"

    data1 = \
"</tspan>\n\
  </text>\n\
  <path\n\
     d=\"M 79.87,36.918183 C 90.59,36.918183 90.59,36.918183 90.59,36.918183 L 94.275,39.598183 L 96.62,43.618183 L 96.62,66.398183 L 94.275,70.418183 L 90.59,73.098183 L 79.2,73.098183 L 79.2,73.098183 L 79.2,75.778183 L 65.8,75.778183 L 65.8,73.098183 L 54.41,73.098183 L 50.725,70.418183 L 48.38,66.398183 L 48.38,43.618183 L 50.725,39.598183 L 54.41,36.918183 L 65.13,36.918183 L 65.13,40.268183 L 79.87,40.268183 L 79.87,36.918183 z\"\n\
     id=\"path10\"\n\
     style=\"fill:url(#linearGradient3208);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <text\n\
     style=\"font-size:8.03999996px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n "

    data2a = \
"<tspan\n\
       x=\"72.\"\n\
       y=\"60.\"\n\
       id=\"tspan14\"\n\
       style=\"font-size:12.06000042px\">"

    data2b = \
"<tspan\n\
       x=\"72.\"\n\
       y=\"54.\"\n\
       id=\"tspan14\"\n\
       style=\"font-size:12.06000042px\">"

    data3b = \
"</tspan>\n\
  </text>\n\
  <text\n\
     style=\"font-size:8.03999996px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"72.\"\n\
       y=\"67.\"\n\
       id=\"tspan18\"\n\
       style=\"font-size:12.06000042px\">"

    data4 = \
"</tspan>\n\
  </text>\n\
  <path\n\
     d=\"M 37.998269,86.158913 L 41.33177,86.158913 L 41.33177,88.825713 L 45.998669,88.825713 L 45.998669,86.158913 L 107.00173,86.158913 L 107.00173,99.492913 L 45.998669,99.492913 L 45.998669,96.826113 L 41.33177,96.826113 L 41.33177,99.492913 L 37.998269,99.492913 L 37.998269,86.158913 z\"\n\
     id=\"path2425\"\n\
     style=\"fill:url(#linearGradient2431);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
  <text\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"72.5\"\n\
       y=\"96.\"\n\
       id=\"tspan2429\"\n\
       style=\"font-size:11px\">"

    data5 = \
"</tspan>\n\
    </text>\n\
  <g\n\
     transform=\"translate(-1e-6,-151.4585)\"\n\
     id=\"g2492\">\n\
    <path\n\
       d=\"M 37.998272,326.10074 L 41.331772,326.10074 L 41.331772,328.76753 L 45.998672,328.76753 L 45.998672,326.10074 L 107.00173,326.10074 L 107.00173,339.43473 L 45.998672,339.43473 L 45.998672,336.76793 L 41.331772,336.76793 L 41.331772,339.43473 L 37.998272,339.43473 L 37.998272,326.10074 z\"\n\
       id=\"path2435\"\n\
       style=\"fill:url(#linearGradient2505);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72.\"\n\
         y=\"336\"\n\
         id=\"tspan2439\"\n\
         style=\"font-size:11px\">"

    data6 = \
"</tspan>\n\
  </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(-5e-7,-155.92557)\"\n\
     id=\"g2497\">\n\
    <path\n\
       d=\"M 37.998271,352.4357 L 41.331771,352.4357 L 41.331771,355.1025 L 45.998671,355.1025 L 45.998671,352.4357 L 107.00173,352.4357 L 107.00173,365.7697 L 45.998671,365.7697 L 45.998671,363.1029 L 41.331771,363.1029 L 41.331771,365.7697 L 37.998271,365.7697 L 37.998271,352.4357 z\"\n\
       id=\"path2429\"\n\
       style=\"fill:url(#linearGradient2507);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72.5\"\n\
         y=\"362.\"\n\
         id=\"tspan2433\"\n\
         style=\"font-size:11px\">"

    data7 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-108.\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect2656\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-107.\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect2658\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 102.1875,149.98334 L 110.4375,149.98334 L 110.4375,152.98334 L 108.4375,152.98334 L 108.4375,151.48334 L 103.1875,151.48334\"\n\
     id=\"path2493\"\n\
     style=\"fill:url(#linearGradient3225);fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 102.1875,163.73334 L 110.4375,163.73334 L 110.4375,160.73334 L 108.4375,160.73334 L 108.4375,162.23334 L 103.1875,162.23334\"\n\
     id=\"path2495\"\n\
     style=\"fill:url(#linearGradient3222);fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 63.3125,147.10834 C 71.3125,147.10834 99.8125,147.10834 99.8125,147.10834 C 99.8125,147.10834 101.8784,148.35162 102.5625,149.10834 C 103.26124,149.88125 104.3125,152.10834 104.3125,152.10834 L 104.3125,161.60834 C 104.3125,161.60834 103.20397,163.45517 102.5625,164.10834 C 101.84772,164.83615 99.8125,166.10834 99.8125,166.10834 L 63.3125,166.10834 L 63.3125,166.10834 L 53.3125,166.10834 L 44.8125,166.10834 C 44.8125,166.10834 42.777281,165.22627 42.0625,164.49846 C 41.421025,163.84529 40.3125,162.60834 40.3125,162.60834 L 40.181985,160.60834 L 36.8125,160.60834 L 36.8125,162.60834 L 34.5625,162.60834 L 34.5625,152.60834 L 36.8125,152.60834 L 36.8125,154.60834 L 40.3125,154.60834 L 40.3125,152.10834 C 40.3125,152.10834 41.363764,149.88125 42.0625,149.10834 C 42.746601,148.35162 44.8125,147.10834 44.8125,147.10834 L 53.3125,147.10834 L 63.3125,147.10834 z\"\n\
     id=\"path2653\"\n\
     style=\"fill:url(#linearGradient3219);fill-opacity:1;stroke:#a00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 46.3125,152.60834 L 48.8125,152.60834 L 48.8125,154.60834 L 52.3125,154.60834 L 52.3125,152.60834 L 98.062505,152.60834 L 98.062505,162.60834 L 52.3125,162.60834 L 52.3125,160.60834 L 48.8125,160.60834 L 48.8125,162.60834 L 46.3125,162.60834 L 46.3125,152.60834 z\"\n\
     id=\"path9\"\n\
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <text\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"72.5\"\n\
       y=\"160.7\"\n\
       id=\"tspan2696\"\n\
       style=\"font-size:11px;fill:#000000;fill-opacity:1\">x</tspan>\n\
  </text>\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-219.6\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect3247\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" />\n\
  <rect\n\
     width=\"137.5\"\n\
     height=\"0.14\"\n\
     x=\"3.75\"\n\
     y=\"-218.\"\n\
     transform=\"scale(1,-1)\"\n\
     id=\"rect3249\"\n\
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" />\n\
  <g\n\
     transform=\"translate(0,14)\"\n\
     id=\"g3283\">\n\
    <path\n\
       d=\"M 37.498269,250.45337 L 40.83177,250.45337 L 40.83177,253.12016 L 45.498669,253.12016 L 45.498669,250.45337 L 106.50173,250.45337 L 106.50173,263.78737 L 45.498669,263.78737 L 45.498669,261.12056 L 40.83177,261.12056 L 40.83177,263.78737 L 37.498269,263.78737 L 37.498269,250.45337 z\"\n\
       id=\"path3261\"\n\
       style=\"fill:url(#linearGradient3322);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72\"\n\
         y=\"260\"\n\
         id=\"tspan3265\"\n\
         style=\"font-size:11px\">"

    data8 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g\n\
     transform=\"translate(1,4)\"\n\
     id=\"g3304\">\n\
    <g\n\
       transform=\"translate(0,-0.14263)\"\n\
       id=\"g3288\">\n\
      <path\n\
         d=\"M 47.87,283.71263 C 58.590001,283.71263 58.590001,283.71263 58.590001,283.71263 L 62.275001,286.39263 L 64.620001,290.41264 L 64.620001,313.19263 L 62.275001,317.21263 L 58.590001,319.89263 L 47.200001,319.89263 L 47.200001,319.89263 L 47.200001,322.57263 L 33.8,322.57263 L 33.8,319.89263 L 22.41,319.89263 L 18.725001,317.21263 L 16.38,313.19263 L 16.38,290.41264 L 18.725001,286.39263 L 22.41,283.71263 L 33.13,283.71263 L 33.13,287.06264 L 47.87,287.06264 L 47.87,283.71263 z\"\n\
         id=\"path3251\"\n\
         style=\"fill:url(#linearGradient3318);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n"

    data9a = \
"      <text\n\
         style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
        <tspan\n\
           x=\"40\"\n\
           y=\"307\"\n\
           id=\"tspan3255\"\n\
           style=\"font-size:12px\">"

    data9b = \
"      <text\n\
         style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
        <tspan\n\
           x=\"40\"\n\
           y=\"301\"\n\
           id=\"tspan3255\"\n\
           style=\"font-size:12px\">"

    data10b = \
"</tspan>\n\
      </text>\n\
      <text\n\
         style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
        <tspan\n\
           x=\"40\"\n\
           y=\"313.8\"\n\
           id=\"tspan3259\"\n\
           style=\"font-size:12px\">"

    data11 = \
"</tspan>\n\
      </text>\n\
    </g>\n\
    <g\n\
       id=\"g3295\">\n\
      <path\n\
         d=\"M 109.87,283.57 C 120.59,283.57 120.59,283.57 120.59,283.57 L 124.275,286.25 L 126.62,290.27001 L 126.62,313.05 L 124.275,317.07 L 120.59,319.75 L 109.2,319.75 L 109.2,319.75 L 109.2,322.43 L 95.8,322.43 L 95.8,319.75 L 84.41,319.75 L 80.725001,317.07 L 78.38,313.05 L 78.38,290.27001 L 80.725001,286.25 L 84.41,283.57 L 95.13,283.57 L 95.13,286.92001 L 109.87,286.92001 L 109.87,283.57 z\"\n\
         id=\"path3271\"\n\
         style=\"fill:url(#linearGradient3320);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n"

    data12a = \
"      <text\n\
         style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
        <tspan\n\
           x=\"102\"\n\
           y=\"307\"\n\
           id=\"tspan3275\"\n\
           style=\"font-size:12px\">"

    data12b = \
"      <text\n\
         style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
        <tspan\n\
           x=\"102\"\n\
           y=\"301\"\n\
           id=\"tspan3275\"\n\
           style=\"font-size:12px\">"

    data13b = \
"</tspan>\n\
      </text>\n\
      <text\n\
         style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
        <tspan\n\
           x=\"102\"\n\
           y=\"314\"\n\
           id=\"tspan3279\"\n\
           style=\"font-size:12px\">"

    data14 = \
"</tspan>\n\
      </text>\n\
    </g>\n\
  </g>\n\
  <path\n\
     d=\"M 90.2125,230.89273 L 101.2675,230.89273 L 101.2675,234.91273 L 98.5875,234.91273 L 98.5875,232.90273 L 91.5525,232.90273\"\n\
     id=\"path3422\"\n\
     style=\"fill:#e00000;fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 90.2125,249.31773 L 101.2675,249.31773 L 101.2675,245.29773 L 98.5875,245.29773 L 98.5875,247.30773 L 91.5525,247.30773\"\n\
     id=\"path3424\"\n\
     style=\"fill:#e00000;fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 75.4725,227.54273 C 86.1925,227.54273 86.1925,227.54273 86.1925,227.54273 C 86.1925,227.54273 88.960805,229.20872 89.8775,230.22273 C 90.813806,231.25843 92.2225,234.24273 92.2225,234.24273 L 92.2225,246.97273 C 92.2225,246.97273 90.737077,249.44748 89.8775,250.32273 C 88.919695,251.298 86.1925,253.00273 86.1925,253.00273 L 74.8025,253.00273 L 74.8025,253.00273 L 74.8025,255.68273 L 61.4025,255.68273 L 61.4025,253.00273 L 50.0125,253.00273 C 50.0125,253.00273 47.285306,251.298 46.3275,250.32273 C 45.467923,249.44748 43.9825,246.97273 43.9825,246.97273 L 43.9825,234.24273 C 43.9825,234.24273 45.391194,231.25843 46.3275,230.22273 C 47.244195,229.20872 50.0125,227.54273 50.0125,227.54273 L 60.7325,227.54273 L 60.7325,230.89273 L 75.4725,230.89273 L 75.4725,227.54273 z\"\n\
     id=\"path3426\"\n\
     style=\"fill:url(#linearGradient3452);fill-opacity:1;stroke:#c00000;stroke-width:1.33000004;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <text\n\
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
    <tspan\n\
       x=\"68\"\n\
       y=\"244\"\n\
       id=\"tspan3430\"\n\
       style=\"font-size:12px;font-family:Bitstream Vera Sans\">"

    data15 = \
"</tspan>\n\
  </text>\n\
  <path\n\
     d=\"M 90.23,116.21 L 101.285,116.21 L 101.285,120.23 L 98.605,120.23 L 98.605,118.22 L 91.57,118.22\"\n\
     id=\"path2561\"\n\
     style=\"fill:#e00000;fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 90.23,134.635 L 101.285,134.635 L 101.285,130.615 L 98.605,130.615 L 98.605,132.625 L 91.57,132.625\"\n\
     id=\"path12\"\n\
     style=\"fill:#e00000;fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 75.49,112.86 C 86.21,112.86 86.21,112.86 86.21,112.86 C 86.21,112.86 88.978305,114.52599 89.895,115.54 C 90.831306,116.5757 92.24,119.56 92.24,119.56 L 92.24,132.29 C 92.24,132.29 90.754576,134.76475 89.895,135.64 C 88.937195,136.61527 86.21,138.32 86.21,138.32 L 74.82,138.32 L 74.82,138.32 L 74.82,141 L 61.42,141 L 61.42,138.32 L 50.03,138.32 C 50.03,138.32 47.302806,136.61527 46.345,135.64 C 45.485423,134.76475 44,132.29 44,132.29 L 44,119.56 C 44,119.56 45.408694,116.5757 46.345,115.54 C 47.261695,114.52599 50.03,112.86 50.03,112.86 L 60.75,112.86 L 60.75,116.21 L 75.49,116.21 L 75.49,112.86 z\"\n\
     id=\"path14\"\n\
     style=\"fill:url(#linearGradient3338);fill-opacity:1;stroke:#a00000;stroke-width:1.29999995;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n\
  <path\n\
     d=\"M 66.803117,120.0391 C 66.144861,120.19978 65.524624,120.46491 64.953796,120.79702 C 65.160095,121.08611 65.28728,121.44601 65.28728,121.82779 C 65.28728,122.80548 64.476052,123.58616 63.498592,123.58616 C 63.109286,123.58616 62.760028,123.46628 62.467823,123.25267 C 62.17102,123.75763 61.930135,124.3119 61.770538,124.88978 C 62.604971,125.03181 63.225742,125.7723 63.225742,126.64815 C 63.225742,127.53198 62.588886,128.24635 61.740221,128.3762 C 61.900827,129.03728 62.16321,129.6556 62.49814,130.22552 C 62.786736,130.02041 63.118086,129.89204 63.498592,129.89204 C 64.476043,129.89204 65.28728,130.70223 65.28728,131.68073 C 65.28728,132.06218 65.159048,132.39259 64.953796,132.68118 C 65.523779,133.01579 66.143425,133.27764 66.803117,133.4391 C 66.932795,132.58989 67.644283,131.92326 68.531172,131.92326 C 69.394719,131.92327 70.105343,132.55808 70.259226,133.37847 C 70.847303,133.21703 71.412232,132.98092 71.926647,132.68118 C 71.721405,132.39241 71.593162,132.03141 71.593162,131.65041 C 71.593162,130.67445 72.375606,129.89204 73.351534,129.89204 C 73.733699,129.89204 74.093047,130.01912 74.382302,130.22552 C 74.716476,129.65801 74.979954,129.03588 75.140221,128.3762 C 74.287782,128.24958 73.624384,127.50571 73.624384,126.61783 C 73.624384,125.75199 74.256874,125.04224 75.079587,124.88978 C 74.917362,124.30479 74.681386,123.76451 74.382302,123.25267 C 74.093047,123.45908 73.733699,123.58616 73.351534,123.58616 C 72.375606,123.58615 71.593162,122.80375 71.593162,121.82779 C 71.593162,121.44561 71.72025,121.08628 71.926647,120.79702 C 71.405635,120.48805 70.859235,120.23235 70.259226,120.06942 C 70.116664,120.90272 69.404885,121.55494 68.531172,121.55494 C 67.646941,121.55493 66.933115,120.88718 66.803117,120.0391 z M 68.440221,124.67756 C 69.573369,124.67755 70.471443,125.60479 70.471443,126.7391 C 70.471433,127.87178 69.573359,128.80064 68.440221,128.80064 C 67.309877,128.80063 66.378683,127.87179 66.378683,126.7391 C 66.378683,125.60534 67.310353,124.67756 68.440221,124.67756 z\"\n\
     id=\"circle2615\" />\n\
  <g>\n\
    <path\n\
       d=\"M 37.998271,350.82011 L 41.331771,350.82011 L 41.331771,353.4869 L 45.998671,353.4869 L 45.998671,350.82011 L 107.00173,350.82011 L 107.00173,364.1541 L 45.998671,364.1541 L 45.998671,361.4873 L 41.331771,361.4873 L 41.331771,364.1541 L 37.998271,364.1541 L 37.998271,350.82011 z\"\n\
       id=\"path2476\"\n\
       style=\"fill:url(#linearGradient3510);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72\"\n\
         y=\"360.5\"\n\
         id=\"tspan2480\"\n\
         style=\"font-size:11px\">"

    data16 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g>\n\
    <path\n\
       d=\"M 37.998271,372.688 L 41.33177,372.688 L 41.33177,375.3548 L 45.998671,375.3548 L 45.998671,372.688 L 107.00173,372.688 L 107.00173,386.022 L 45.998671,386.022 L 45.998671,383.3552 L 41.33177,383.3552 L 41.33177,386.022 L 37.998271,386.022 L 37.998271,372.688 z\"\n\
       id=\"path2484\"\n\
       style=\"fill:url(#linearGradient3516);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72.5\"\n\
         y=\"382.5\"\n\
         id=\"tspan2488\"\n\
         style=\"font-size:11px\">"

    data17 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g>\n\
    <path\n\
       d=\"M 37.998271,394.34238 L 41.331771,394.34238 L 41.331771,397.00916 L 45.998671,397.00916 L 45.998671,394.34238 L 107.00173,394.34238 L 107.00173,407.67636 L 45.998671,407.67636 L 45.998671,405.00956 L 41.331771,405.00956 L 41.331771,407.67636 L 37.998271,407.67636 L 37.998271,394.34238 z\"\n\
       id=\"path2496\"\n\
       style=\"fill:url(#linearGradient3514);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72\"\n\
         y=\"404.25\"\n\
         id=\"tspan2500\"\n\
         style=\"font-size:11px\">"

    data18 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
  <g>\n\
    <path\n\
       d=\"M 37.998271,416.21026 L 41.33177,416.21026 L 41.33177,418.87707 L 45.998671,418.87707 L 45.998671,416.21026 L 107.00173,416.21026 L 107.00173,429.54426 L 45.998671,429.54426 L 45.998671,426.87747 L 41.33177,426.87747 L 41.33177,429.54426 L 37.998271,429.54426 L 37.998271,416.21026 z\"\n\
       id=\"path2504\"\n\
       style=\"fill:url(#linearGradient3512);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" />\n\
    <text\n\
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n\
      <tspan\n\
         x=\"72.5\"\n\
         y=\"425.5\"\n\
         id=\"tspan2508\"\n\
         style=\"font-size:11px\">"

    data19 = \
"</tspan>\n\
    </text>\n\
  </g>\n\
</svg> \n"


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring1.encode("utf-8"))
    FILE.write(data1)
    strings = mystring2.split(" ",2)
    if len(strings) == 1:
        FILE.write(data2a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data2b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data3b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data4)
    FILE.write(s3lower.encode("utf-8"))
    FILE.write(data5)
    FILE.write(mystring4.encode("utf-8"))
    FILE.write(data6)
    FILE.write(mystring5.encode("utf-8"))
    FILE.write(data7)
    FILE.write(mystring6.encode("utf-8"))
    FILE.write(data8)
    strings = mystring7.split(" ",2)
    if len(strings) == 1:
        FILE.write(data9a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data9b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data10b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data11)
    strings = mystring8.split(" ",2)
    if len(strings) == 1:
        FILE.write(data12a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data12b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data13b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data14)
    FILE.write(mystring9.encode("utf-8"))
    FILE.write(data15)
    FILE.write(mystring10.encode("utf-8"))
    FILE.write(data16)
    FILE.write(mystring11.encode("utf-8"))
    FILE.write(data17)
    FILE.write(mystring12.encode("utf-8"))
    FILE.write(data18)
    FILE.write(mystring13.encode("utf-8"))
    FILE.write(data19)
    FILE.close()
    return

if __name__ == "__main__":
    main()





