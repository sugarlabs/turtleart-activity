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
    mystring1 = "Keyboard"
    mystring2 = "read key"
    mystring3 = "keyboard"
    mystring4 = "hres"
    mystring5 = "vres"
    mygroup = "sensors"

    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    print _(mystring1)
    print _(mystring2)
    print _(mystring3)
    print _(mystring4)
    print _(mystring5)

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<!-- Created with Inkscape (http://www.inkscape.org/) --> \n \
<svg \n \
   xmlns:svg=\"http://www.w3.org/2000/svg\" \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   version=\"1.0\" \n \
   width=\"145\" \n \
   height=\"404\" \n \
   id=\"svg2\"> \n \
  <defs \n \
     id=\"defs4\"> \n \
    <linearGradient \n \
       id=\"linearGradient3712\"> \n \
      <stop \n \
         id=\"stop3714\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3716\" \n \
         style=\"stop-color:#ff0000;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2487\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.50255,109.49499)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"174.22649\" \n \
       x2=\"140.1927\" \n \
       y2=\"174.22649\" \n \
       id=\"linearGradient2494\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.50255,109.25224)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2501\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.502549,135.82996)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"174.22649\" \n \
       x2=\"140.1927\" \n \
       y2=\"174.22649\" \n \
       id=\"linearGradient2508\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.502549,135.5872)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3172\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
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
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2431\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.524281,-133.82775)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3208\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.67,0,0,0.67,47.71,36.248183)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2441\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.524276,132.44905)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2443\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.524278,106.11408)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"64\" \n \
       y2=\"0\" \n \
       id=\"linearGradient2540\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(34.404412,58.027574)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2504\"> \n \
      <stop \n \
         id=\"stop2506\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2508\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"64\" \n \
       y2=\"0\" \n \
       id=\"linearGradient2510\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,4.96875)\" /> \n \
    <linearGradient \n \
       x1=\"210\" \n \
       y1=\"10.5\" \n \
       x2=\"0\" \n \
       y2=\"10.5\" \n \
       id=\"linearGradient2512\" \n \
       xlink:href=\"#linearGradient3886\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2514\"> \n \
      <stop \n \
         id=\"stop2516\" \n \
         style=\"stop-color:#0000ff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2518\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"210\" \n \
       y1=\"10.5\" \n \
       x2=\"0\" \n \
       y2=\"10.5\" \n \
       id=\"linearGradient2520\" \n \
       xlink:href=\"#linearGradient3886\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"64\" \n \
       y2=\"0\" \n \
       id=\"linearGradient2522\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,4.96875)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"104\" \n \
       y2=\"21\" \n \
       id=\"linearGradient2524\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,5.4999997)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2492\"> \n \
      <stop \n \
         id=\"stop2494\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2496\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"104\" \n \
       y2=\"21\" \n \
       id=\"linearGradient2493\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2486\"> \n \
      <stop \n \
         id=\"stop2488\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2490\" \n \
         style=\"stop-color:#0000ff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       id=\"linearGradient2509\"> \n \
      <stop \n \
         id=\"stop2511\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2513\" \n \
         style=\"stop-color:#ffff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2515\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"128.68382\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2623\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2595\"> \n \
      <stop \n \
         id=\"stop2597\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2599\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2601\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2473\"> \n \
      <stop \n \
         id=\"stop2475\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2477\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"64\" \n \
       y2=\"0\" \n \
       id=\"linearGradient4238\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,4.96875)\" /> \n \
    <linearGradient \n \
       x1=\"210\" \n \
       y1=\"10.5\" \n \
       x2=\"0\" \n \
       y2=\"10.5\" \n \
       id=\"linearGradient4211\" \n \
       xlink:href=\"#linearGradient3886\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient3886\"> \n \
      <stop \n \
         id=\"stop3888\" \n \
         style=\"stop-color:#0000ff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3890\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"210\" \n \
       y1=\"10.5\" \n \
       x2=\"0\" \n \
       y2=\"10.5\" \n \
       id=\"linearGradient2496\" \n \
       xlink:href=\"#linearGradient3886\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"64\" \n \
       y2=\"0\" \n \
       id=\"linearGradient2608\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,4.96875)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"128.68382\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2606\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(11.5,0)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2600\"> \n \
      <stop \n \
         id=\"stop2602\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2604\" \n \
         style=\"stop-color:#ff0000;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3432\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.5,0,0,0.5,34.1875,291.59109)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2502\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.5,0,0,0.5,34.1875,291.59109)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2505\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.524278,106.11408)\" /> \n \
    <linearGradient \n \
       x1=\"69.85585\" \n \
       y1=\"226.65366\" \n \
       x2=\"140.1927\" \n \
       y2=\"226.65366\" \n \
       id=\"linearGradient2507\" \n \
       xlink:href=\"#linearGradient3712\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-32.524276,132.44905)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2616\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2610\"> \n \
      <stop \n \
         id=\"stop2612\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2614\" \n \
         style=\"stop-color:#ff0000;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3398\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.5,0,0,0.5,54,116.57443)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2543\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.5,0,0,0.5,34.0625,146.60834)\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 0.5594301,0.5 L 0.49711997,390.41023 L 3.6209793,397.14297 L 8.494839,401.1072 L 15.156388,403.50288 L 128.9813,403.50288 L 135.82978,400.93866 L 141.77903,396.04729 L 144.50288,387.79171 L 144.54057,0.5 L 0.5594301,0.5 z\" \n \
     id=\"path13\" \n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1px;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-28.931932\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect15\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-27.815523\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect17\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-376.77127\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect19\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-375.43195\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect4001\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 79.5,438.375 C 79.5,442.86231 75.750385,446.5 71.125,446.5 C 66.499615,446.5 62.75,442.86231 62.75,438.375 C 62.75,433.88769 66.499615,430.25 71.125,430.25 C 75.750385,430.25 79.5,433.88769 79.5,438.375 L 79.5,438.375 z\" \n \
     transform=\"translate(1.375,-48.749023)\" \n \
     id=\"path22\" \n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text24\" \n \
     style=\"font-size:12px;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"394\" \n \
       id=\"tspan26\" \n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff\">X</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text28\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"21.5\" \n \
       id=\"tspan30\" \n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 79.87,36.918183 C 90.59,36.918183 90.59,36.918183 90.59,36.918183 L 94.275,39.598183 L 96.62,43.618183 L 96.62,66.398183 L 94.275,70.418183 L 90.59,73.098183 L 79.2,73.098183 L 79.2,73.098183 L 79.2,75.778183 L 65.8,75.778183 L 65.8,73.098183 L 54.41,73.098183 L 50.725,70.418183 L 48.38,66.398183 L 48.38,43.618183 L 50.725,39.598183 L 54.41,36.918183 L 65.13,36.918183 L 65.13,40.268183 L 79.87,40.268183 L 79.87,36.918183 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient3208);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n "

    data2a = \
"  <text \n \
     style=\"font-size:8.03999996px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"60\" \n \
       id=\"tspan14\" \n \
       style=\"font-size:12.06000042px\">"

    data2b = \
"  <text \n \
     style=\"font-size:8.03999996px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"54\" \n \
       id=\"tspan14\" \n \
       style=\"font-size:12.06000042px\">"

    data3b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:8.03999996px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"67\" \n \
       id=\"tspan18\" \n \
       style=\"font-size:12.06000042px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.998269,86.158913 L 41.33177,86.158913 L 41.33177,88.825713 L 45.998669,88.825713 L 45.998669,86.158913 L 107.00173,86.158913 L 107.00173,99.492913 L 45.998669,99.492913 L 45.998669,96.826113 L 41.33177,96.826113 L 41.33177,99.492913 L 37.998269,99.492913 L 37.998269,86.158913 z\" \n \
     id=\"path2425\" \n \
     style=\"fill:url(#linearGradient2431);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"74\" \n \
       y=\"96\" \n \
       id=\"tspan2429\" \n \
       style=\"font-size:11px\">"

    data5 = \
"</tspan> \n \
  </text> \n \
  <g \n \
     transform=\"translate(-5e-7,-155.92557)\" \n \
     id=\"g2497\"> \n \
    <path \n \
       d=\"M 37.998271,352.4357 L 41.331771,352.4357 L 41.331771,355.1025 L 45.998671,355.1025 L 45.998671,352.4357 L 107.00173,352.4357 L 107.00173,365.7697 L 45.998671,365.7697 L 45.998671,363.1029 L 41.331771,363.1029 L 41.331771,365.7697 L 37.998271,365.7697 L 37.998271,352.4357 z\" \n \
       id=\"path2429\" \n \
       style=\"fill:url(#linearGradient2507);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" /> \n \
    <text \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"74\" \n \
         y=\"362.5\" \n \
         id=\"tspan2433\" \n \
         style=\"font-size:11px\">"

    data6 = \
"</tspan> \n \
    </text> \n \
  </g> \n \
  <g \n \
     transform=\"translate(-1e-6,-151.4585)\" \n \
     id=\"g2492\"> \n \
    <path \n \
       d=\"M 37.998272,326.10074 L 41.331772,326.10074 L 41.331772,328.76753 L 45.998672,328.76753 L 45.998672,326.10074 L 107.00173,326.10074 L 107.00173,339.43473 L 45.998672,339.43473 L 45.998672,336.76793 L 41.331772,336.76793 L 41.331772,339.43473 L 37.998272,339.43473 L 37.998272,326.10074 z\" \n \
       id=\"path2435\" \n \
       style=\"fill:url(#linearGradient2505);fill-opacity:1;stroke:#c00000;stroke-width:1;stroke-opacity:1\" /> \n \
    <text \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"74\" \n \
         y=\"336\" \n \
         id=\"tspan2439\" \n \
         style=\"font-size:11px\">"

    data7 = \
"</tspan> \n \
    </text> \n \
  </g> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.75\" \n \
     y=\"-109.89137\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect2656\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.75\" \n \
     y=\"-108.77495\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect2658\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <g \n \
     id=\"g2579\"> \n \
    <path \n \
       d=\"M 102.1875,149.98334 L 110.4375,149.98334 L 110.4375,152.98334 L 108.4375,152.98334 L 108.4375,151.48334 L 103.1875,151.48334\" \n \
       id=\"path2493\" \n \
       style=\"fill:#a00000;fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 102.1875,163.73334 L 110.4375,163.73334 L 110.4375,160.73334 L 108.4375,160.73334 L 108.4375,162.23334 L 103.1875,162.23334\" \n \
       id=\"path2495\" \n \
       style=\"fill:#a00000;fill-opacity:1;stroke:#800000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 63.3125,147.10834 C 71.3125,147.10834 99.8125,147.10834 99.8125,147.10834 C 99.8125,147.10834 101.8784,148.35162 102.5625,149.10834 C 103.26124,149.88125 104.3125,152.10834 104.3125,152.10834 L 104.3125,161.60834 C 104.3125,161.60834 103.20397,163.45517 102.5625,164.10834 C 101.84772,164.83615 99.8125,166.10834 99.8125,166.10834 L 63.3125,166.10834 L 63.3125,166.10834 L 53.3125,166.10834 L 44.8125,166.10834 C 44.8125,166.10834 42.777281,165.22627 42.0625,164.49846 C 41.421025,163.84529 40.3125,162.60834 40.3125,162.60834 L 40.181985,160.60834 L 36.8125,160.60834 L 36.8125,162.60834 L 34.5625,162.60834 L 34.5625,152.60834 L 36.8125,152.60834 L 36.8125,154.60834 L 40.3125,154.60834 L 40.3125,152.10834 C 40.3125,152.10834 41.363764,149.88125 42.0625,149.10834 C 42.746601,148.35162 44.8125,147.10834 44.8125,147.10834 L 53.3125,147.10834 L 63.3125,147.10834 z\" \n \
       id=\"path2653\" \n \
       style=\"fill:url(#linearGradient2543);fill-opacity:1;stroke:#a00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 46.3125,152.60834 L 48.8125,152.60834 L 48.8125,154.60834 L 52.3125,154.60834 L 52.3125,152.60834 L 98.062505,152.60834 L 98.062505,162.60834 L 52.3125,162.60834 L 52.3125,160.60834 L 48.8125,160.60834 L 48.8125,162.60834 L 46.3125,162.60834 L 46.3125,152.60834 z\" \n \
       id=\"path9\" \n \
       style=\"fill:#ffffff;fill-opacity:1;stroke:#a00000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <text \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"74\" \n \
         y=\"161\" \n \
         id=\"tspan2696\" \n \
         style=\"font-size:11px\">x</tspan> \n \
    </text> \n \
  </g> \n \
</svg> \n"


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring1).encode("utf-8"))
    FILE.write(data1)
    strings = _(mystring2).split(" ",2)
    if len(strings) == 1:
        FILE.write(data2a)
        FILE.write(strings[0].encode("utf-8"))
    else:
        FILE.write(data2b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data3b)
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data4)
    FILE.write(_(mystring3).encode("utf-8"))
    FILE.write(data5)
    FILE.write(_(mystring4).encode("utf-8"))
    FILE.write(data6)
    FILE.write(_(mystring5).encode("utf-8"))
    FILE.write(data7)
    FILE.close()
    return

if __name__ == "__main__":
    main()

