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

    myname = "numbersgroup"
    mystring1 = "Numbers"
    mystring2 = "random"
    mystring3 = "and"
    mystring4 = "or"
    mystring5 = "not"
    mystring6 = "print"
    mystring7 = "number"
    mystring8 = "min"
    mystring9 = "max"
    mystring10 = "mod"
    mygroup = "numbers"

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
    print _(mystring6)
    print _(mystring7)
    print _(mystring8)
    print _(mystring9)
    print _(mystring10)

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<!-- Created with Inkscape (http://www.inkscape.org/) --> \n \
<svg \n \
   xmlns:svg=\"http://www.w3.org/2000/svg\" \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   version=\"1.0\" \n \
   width=\"145\" \n \
   height=\"500\" \n \
   id=\"svg2\"> \n \
  <defs \n \
     id=\"defs94\"> \n \
    <linearGradient \n \
       id=\"linearGradient3405\"> \n \
      <stop \n \
         id=\"stop3407\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3409\" \n \
         style=\"stop-color:#ffff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       id=\"linearGradient3241\"> \n \
      <stop \n \
         id=\"stop3243\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3245\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"37.499828\" \n \
       y1=\"41.5\" \n \
       x2=\"107.50017\" \n \
       y2=\"41.5\" \n \
       id=\"linearGradient3247\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"20.764166\" \n \
       y1=\"80.032402\" \n \
       x2=\"47.264164\" \n \
       y2=\"80.032402\" \n \
       id=\"linearGradient3255\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"86.115639\" \n \
       y1=\"80.032402\" \n \
       x2=\"122.24064\" \n \
       y2=\"80.032402\" \n \
       id=\"linearGradient3263\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"20.764162\" \n \
       y1=\"121.53331\" \n \
       x2=\"47.264164\" \n \
       y2=\"121.53331\" \n \
       id=\"linearGradient3271\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"86.115639\" \n \
       y1=\"121.53331\" \n \
       x2=\"122.24064\" \n \
       y2=\"121.53331\" \n \
       id=\"linearGradient3279\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"15.95166\" \n \
       y1=\"163.03423\" \n \
       x2=\"52.07666\" \n \
       y2=\"163.03423\" \n \
       id=\"linearGradient3287\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.511383\" \n \
       y1=\"168.49895\" \n \
       x2=\"116.8449\" \n \
       y2=\"168.49895\" \n \
       id=\"linearGradient3295\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.511383\" \n \
       y1=\"168.49895\" \n \
       x2=\"116.8449\" \n \
       y2=\"168.49895\" \n \
       id=\"linearGradient3297\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.511383\" \n \
       y1=\"168.49895\" \n \
       x2=\"116.8449\" \n \
       y2=\"168.49895\" \n \
       id=\"linearGradient3299\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.511383\" \n \
       y1=\"168.49895\" \n \
       x2=\"116.8449\" \n \
       y2=\"168.49895\" \n \
       id=\"linearGradient3301\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.511383\" \n \
       y1=\"168.49895\" \n \
       x2=\"116.8449\" \n \
       y2=\"168.49895\" \n \
       id=\"linearGradient3307\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(6,-5.464714)\" /> \n \
    <linearGradient \n \
       x1=\"10.111029\" \n \
       y1=\"240.50002\" \n \
       x2=\"134.88898\" \n \
       y2=\"240.50002\" \n \
       id=\"linearGradient3315\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"1.0548444\" \n \
       y1=\"277\" \n \
       x2=\"143.94516\" \n \
       y2=\"277\" \n \
       id=\"linearGradient3323\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"1.0548444\" \n \
       y1=\"304.5\" \n \
       x2=\"143.94516\" \n \
       y2=\"304.5\" \n \
       id=\"linearGradient3331\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"1.0548444\" \n \
       y1=\"332\" \n \
       x2=\"143.94516\" \n \
       y2=\"332\" \n \
       id=\"linearGradient3339\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"8.1665154\" \n \
       y1=\"372\" \n \
       x2=\"69.833488\" \n \
       y2=\"372\" \n \
       id=\"linearGradient3347\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"77.666512\" \n \
       y1=\"371.5\" \n \
       x2=\"139.33348\" \n \
       y2=\"371.5\" \n \
       id=\"linearGradient3355\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"12.999865\" \n \
       y1=\"402.5\" \n \
       x2=\"68.000137\" \n \
       y2=\"402.5\" \n \
       id=\"linearGradient3363\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"12.999865\" \n \
       y1=\"402.5\" \n \
       x2=\"68.000137\" \n \
       y2=\"402.5\" \n \
       id=\"linearGradient3365\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"12.999865\" \n \
       y1=\"402.5\" \n \
       x2=\"68.000137\" \n \
       y2=\"402.5\" \n \
       id=\"linearGradient3367\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"12.999865\" \n \
       y1=\"402.5\" \n \
       x2=\"68.000137\" \n \
       y2=\"402.5\" \n \
       id=\"linearGradient3371\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(32,8)\" /> \n \
    <linearGradient \n \
       x1=\"12.999865\" \n \
       y1=\"402.5\" \n \
       x2=\"68.000137\" \n \
       y2=\"402.5\" \n \
       id=\"linearGradient3374\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(32,8)\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3382\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3384\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3386\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3388\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3390\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3394\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-36.520584,50.43926)\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3397\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-36.520584,50.43926)\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3400\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-36.520584,50.43926)\" /> \n \
    <linearGradient \n \
       x1=\"80.020439\" \n \
       y1=\"401.94131\" \n \
       x2=\"138.02074\" \n \
       y2=\"401.94131\" \n \
       id=\"linearGradient3403\" \n \
       xlink:href=\"#linearGradient3241\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-36.520584,50.43926)\" /> \n \
    <linearGradient \n \
       x1=\"20.764162\" \n \
       y1=\"201.22266\" \n \
       x2=\"47.264164\" \n \
       y2=\"201.22266\" \n \
       id=\"linearGradient3411\" \n \
       xlink:href=\"#linearGradient3405\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"90.928139\" \n \
       y1=\"201.22266\" \n \
       x2=\"117.42814\" \n \
       y2=\"201.22266\" \n \
       id=\"linearGradient3419\" \n \
       xlink:href=\"#linearGradient3405\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 0.5594301,0.5 L 0.49711997,486.41023 L 3.6209793,493.14297 L 8.494839,497.1072 L 15.156388,499.50288 L 128.9813,499.50288 L 135.82978,496.93866 L 141.77903,492.04729 L 144.50288,483.79171 L 144.54057,0.5 L 0.5594301,0.5 z\" \n \
     id=\"path25\" \n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1px;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"221.19794\" \n \
     id=\"rect27\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"222.31435\" \n \
     id=\"rect29\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"223.29239\" \n \
     id=\"rect31\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"55.382996\" \n \
     id=\"rect33\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"56.499405\" \n \
     id=\"rect35\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"57.477448\" \n \
     id=\"rect37\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-28.931932\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect39\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-27.815523\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect41\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-472.77127\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect43\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-471.43195\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect45\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 79.5,438.375 C 79.5,442.86231 75.750385,446.5 71.125,446.5 C 66.499615,446.5 62.75,442.86231 62.75,438.375 C 62.75,433.88769 66.499615,430.25 71.125,430.25 C 75.750385,430.25 79.5,433.88769 79.5,438.375 L 79.5,438.375 z\" \n \
     transform=\"translate(1.375,47.250977)\" \n \
     id=\"path47\" \n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text49\" \n \
     style=\"font-size:12px;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:1px;stroke-opacity:1;font-family:Bitstream Vera Sans;-inkscape-font-specification:Bitstream Vera Sans Bold\"> \n \
    <tspan \n \
       x=\"67.879883\" \n \
       y=\"490\" \n \
       id=\"tspan51\" \n \
       style=\"font-size:12px\">X</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text53\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"21.5\" \n \
       id=\"tspan2796\" \n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"258.883\" \n \
     id=\"rect56\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"259.99942\" \n \
     id=\"rect58\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"260.97745\" \n \
     id=\"rect60\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"347.883\" \n \
     id=\"rect62\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"348.99939\" \n \
     id=\"rect64\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"349.97745\" \n \
     id=\"rect66\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"429.883\" \n \
     id=\"rect68\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"430.99939\" \n \
     id=\"rect70\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137\" \n \
     height=\"0.2\" \n \
     x=\"4\" \n \
     y=\"431\" \n \
     id=\"rect72\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 37.99983,34.8333 L 41.33318,34.8333 L 41.33318,37.49998 L 45.99987,37.49998 L 45.99987,34.8333 L 107.00017,34.8333 L 107.00017,48.1667 L 45.99987,48.1667 L 45.99987,45.50002 L 41.33318,45.50002 L 41.33318,48.1667 L 37.99983,48.1667 L 37.99983,34.8333 z\" \n \
     id=\"path74\" \n \
     style=\"fill:url(#linearGradient3247);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 122.3449,151.03208 L 100.67812,151.03208 L 97.986426,152.47502 L 96.340697,154.12075 L 95.011426,156.36544 L 95.011426,158.31578 L 89.956942,158.38161 L 89.956942,156.36544 L 86.011381,156.36544 L 86.011381,169.69884 L 90.011401,169.69884 L 90.011401,167.3655 L 95.011426,167.3655 L 95.011426,172.13991 L 96.276543,173.98313 L 98.975539,175.03639 L 122.3449,174.97056 L 122.3449,168.3655 L 118.79012,168.3655 L 118.79012,170.42835 L 113.19464,170.42835 L 113.01152,155.36544 L 119.01155,155.36544 L 119.01155,157.36545 L 122.3449,157.36545 L 122.3449,151.03208 z\" \n \
     id=\"path106\" \n \
     style=\"fill:url(#linearGradient3307);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <g \n \
     transform=\"translate(1.9359525,12.535286)\" \n \
     id=\"g108\" \n \
     style=\"fill:#000000;fill-opacity:1\"> \n \
    <text \n \
       id=\"text110\" \n \
       style=\"font-size:8px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"102\" \n \
         y=\"157\" \n \
         id=\"tspan112\" \n \
         style=\"font-size:16px;fill:#000000;fill-opacity:1\">√</tspan> \n \
    </text> \n \
  </g> \n \
  <path \n \
     d=\"M 125.54364,230.16802 L 20.202678,230.44265 L 18.649745,231.26928 L 17.553556,232.00407 L 16.548717,233.65733 L 16.548717,239.5356 L 13.260151,239.62745 L 13.168802,238.06603 L 10.611029,237.97418 L 10.793727,247.34268 L 13.077453,247.34268 L 13.168802,245.41387 L 16.548717,245.50572 L 16.457368,248.99594 L 17.370858,249.82257 L 18.923792,250.55736 L 129.09073,250.8329 L 128.81668,247.06713 L 134.38897,246.88344 L 134.29762,238.52527 L 129.09073,238.52527 L 128.99938,233.38178 L 127.81184,231.72852 L 125.98486,230.16711 L 125.54364,230.16802 L 125.54364,230.16802\" \n \
     id=\"path114\" \n \
     style=\"fill:url(#linearGradient3315);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 23.057444,238.07932 L 25.310631,238.07932 L 25.310631,240.02538 L 28.465092,240.02538 L 28.465092,238.07932 L 69.698412,238.07932 L 69.698412,247.80963 L 28.465092,247.80963 L 28.465092,245.86356 L 25.310631,245.86356 L 25.310631,247.80963 L 23.057444,247.80963 L 23.057444,238.07932 z\" \n \
     id=\"path116\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 77.813595,238.07932 L 80.066783,238.07932 L 80.066783,240.02538 L 83.221245,240.02538 L 83.221245,238.07932 L 124.45457,238.07932 L 124.45457,247.80963 L 83.221245,247.80963 L 83.221245,245.86356 L 80.066783,245.86356 L 80.066783,247.80963 L 77.813595,247.80963 L 77.813595,238.07932 z\" \n \
     id=\"path118\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"48\" \n \
     id=\"text120\" \n \
     style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"237\" \n \
       id=\"tspan122\" \n \
       style=\"font-size:7px\">"

    data2 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 131.00059,323.49992 L 13.110516,323.61103 L 9.9993735,324.49993 L 5.4437723,326.61106 L 2.9993033,328.72219 L 1.7770688,331.05555 L 1.5548444,331.94445 L 1.5548444,333.38891 L 2.4437422,334.94448 L 4.8882111,336.83339 L 7.777129,338.38896 L 10.554935,339.50008 L 13.221628,340.38898 L 131.44504,340.50009 L 135.6673,338.94452 L 139.55623,337.38895 L 142.0007,335.38893 L 143.33404,333.38891 L 143.44516,332.05556 L 142.77848,329.61109 L 140.33401,326.9444 L 137.00065,325.61105 L 134.00062,324.38882 L 131.00059,323.49992 z\" \n \
     id=\"path124\" \n \
     style=\"fill:url(#linearGradient3339);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 15.779593,327.30152 L 18.03278,327.30152 L 18.03278,329.24758 L 21.187242,329.24758 L 21.187242,327.30152 L 62.420561,327.30152 L 62.420561,337.03183 L 21.187242,337.03183 L 21.187242,335.08577 L 18.03278,335.08577 L 18.03278,337.03183 L 15.779593,337.03183 L 15.779593,327.30152 z\" \n \
     id=\"path126\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 82.091416,327.30152 L 84.344603,327.30152 L 84.344603,329.24758 L 87.499066,329.24758 L 87.499066,327.30152 L 128.73239,327.30152 L 128.73239,337.03183 L 87.499066,337.03183 L 87.499066,335.08577 L 84.344603,335.08577 L 84.344603,337.03183 L 82.091416,337.03183 L 82.091416,327.30152 z\" \n \
     id=\"path128\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"14\" \n \
     id=\"text130\" \n \
     style=\"font-size:5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"337\" \n \
       id=\"tspan132\" \n \
       style=\"font-size:14px\">=</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 131.00059,295.99992 L 13.110516,296.11103 L 9.9993735,296.99993 L 5.4437723,299.11106 L 2.9993033,301.22219 L 1.7770688,303.55555 L 1.5548444,304.44445 L 1.5548444,305.88891 L 2.4437422,307.44448 L 4.8882111,309.33339 L 7.777129,310.88896 L 10.554935,312.00008 L 13.221628,312.88898 L 131.44504,313.00009 L 135.6673,311.44452 L 139.55623,309.88895 L 142.0007,307.88893 L 143.33404,305.88891 L 143.44516,304.55556 L 142.77848,302.11109 L 140.33401,299.4444 L 137.00065,298.11105 L 134.00062,296.88882 L 131.00059,295.99992 z\" \n \
     id=\"path134\" \n \
     style=\"fill:url(#linearGradient3331);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 15.779593,299.80152 L 18.03278,299.80152 L 18.03278,301.74758 L 21.187242,301.74758 L 21.187242,299.80152 L 62.420561,299.80152 L 62.420561,309.53183 L 21.187242,309.53183 L 21.187242,307.58577 L 18.03278,307.58577 L 18.03278,309.53183 L 15.779593,309.53183 L 15.779593,299.80152 z\" \n \
     id=\"path136\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 82.091416,299.80152 L 84.344603,299.80152 L 84.344603,301.74758 L 87.499066,301.74758 L 87.499066,299.80152 L 128.73239,299.80152 L 128.73239,309.53183 L 87.499066,309.53183 L 87.499066,307.58577 L 84.344603,307.58577 L 84.344603,309.53183 L 82.091416,309.53183 L 82.091416,299.80152 z\" \n \
     id=\"path138\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text140\" \n \
     style=\"font-size:5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"309\" \n \
       id=\"tspan142\" \n \
       style=\"font-size:14px\">&lt;</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 131.00059,268.49992 L 13.110516,268.61103 L 9.9993735,269.49993 L 5.4437723,271.61106 L 2.9993033,273.72219 L 1.7770688,276.05555 L 1.5548444,276.94445 L 1.5548444,278.38891 L 2.4437422,279.94448 L 4.8882111,281.83339 L 7.777129,283.38896 L 10.554935,284.50008 L 13.221628,285.38898 L 131.44504,285.50009 L 135.6673,283.94452 L 139.55623,282.38895 L 142.0007,280.38893 L 143.33404,278.38891 L 143.44516,277.05556 L 142.77848,274.61109 L 140.33401,271.9444 L 137.00065,270.61105 L 134.00062,269.38882 L 131.00059,268.49992 z\" \n \
     id=\"path144\" \n \
     style=\"fill:url(#linearGradient3323);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 15.779593,272.30152 L 18.03278,272.30152 L 18.03278,274.24758 L 21.187242,274.24758 L 21.187242,272.30152 L 62.420561,272.30152 L 62.420561,282.03183 L 21.187242,282.03183 L 21.187242,280.08577 L 18.03278,280.08577 L 18.03278,282.03183 L 15.779593,282.03183 L 15.779593,272.30152 z\" \n \
     id=\"path146\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 82.091416,272.30152 L 84.344603,272.30152 L 84.344603,274.24758 L 87.499066,274.24758 L 87.499066,272.30152 L 128.73239,272.30152 L 128.73239,282.03183 L 87.499066,282.03183 L 87.499066,280.08577 L 84.344603,280.08577 L 84.344603,282.03183 L 82.091416,282.03183 L 82.091416,272.30152 z\" \n \
     id=\"path148\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"42\" \n \
     id=\"text150\" \n \
     style=\"font-size:5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"281\" \n \
       id=\"tspan152\" \n \
       style=\"font-size:14px\">&gt;</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 8.666515,356.99992 L 69.333485,356.99992 L 69.333485,359.33327 L 63.66679,359.99994 L 59.66677,361.33328 L 56.666755,362.99995 L 53.333405,365.66663 L 51.66673,368.33331 L 50.933393,371.33333 L 51.533396,374.13334 L 53.00007,377.33336 L 55.333415,379.33337 L 58.666765,381.33338 L 62.000115,382.66672 L 65.6668,383.66672 L 69.333485,384.66673 L 69.333485,387.00007 L 8.666515,387.00007 L 8.666515,384.66673 L 13.333205,383.66672 L 17.866561,382.53339 L 21.66658,380.66671 L 24.33326,378.6667 L 25.999935,376.40002 L 26.99994,373.66667 L 26.99994,371.33333 L 26.866606,369.19999 L 25.999935,367.33331 L 23.999925,364.66663 L 21.266578,362.86662 L 17.799894,361.13328 L 13.66654,359.99994 L 8.666515,359.33327 L 8.666515,356.99992 z\" \n \
     id=\"path154\" \n \
     style=\"fill:url(#linearGradient3347);fill-opacity:1;stroke:#a000a0;stroke-width:1px;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"12\" \n \
     id=\"text156\" \n \
     style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"39\" \n \
       y=\"376\" \n \
       id=\"tspan158\" \n \
       style=\"font-size:11px\">"

    data3 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 78.166515,356.49992 L 138.83348,356.49992 L 138.83348,358.83327 L 133.16679,359.49994 L 129.16677,360.83328 L 126.16675,362.49995 L 122.8334,365.16663 L 121.16673,367.83331 L 120.43339,370.83333 L 121.0334,373.63334 L 122.50007,376.83336 L 124.83342,378.83337 L 128.16676,380.83338 L 131.50011,382.16672 L 135.1668,383.16672 L 138.83348,384.16673 L 138.83348,386.50007 L 78.166515,386.50007 L 78.166515,384.16673 L 82.833205,383.16672 L 87.366561,382.03339 L 91.16658,380.16671 L 93.83326,378.1667 L 95.499935,375.90002 L 96.49994,373.16667 L 96.49994,370.83333 L 96.366606,368.69999 L 95.499935,366.83331 L 93.499925,364.16663 L 90.766578,362.36662 L 87.299894,360.63328 L 83.16654,359.49994 L 78.166515,358.83327 L 78.166515,356.49992 z\" \n \
     id=\"path160\" \n \
     style=\"fill:url(#linearGradient3355);fill-opacity:1;stroke:#a000a0;stroke-width:1px;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"12\" \n \
     id=\"text162\" \n \
     style=\"font-size:8px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"108\" \n \
       y=\"375\" \n \
       id=\"tspan164\" \n \
       style=\"font-size:11px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 99.500135,395.83326 L 78.833365,395.83326 L 69.702859,396.44907 L 62.143743,397.72303 L 55.213278,399.78601 L 50.406084,402.468 L 47.325727,405.47844 L 45.951693,407.83392 L 45.499865,410.16667 L 45.919619,412.35053 L 47.033217,414.70602 L 49.52085,417.32195 L 53.508882,419.61136 L 59.067239,421.53834 L 64.471011,422.78601 L 71.035993,424.12797 L 78.833365,425.16674 L 99.500135,425.16674 L 99.500135,423.16674 L 95.613222,422.45565 L 91.400679,421.11754 C 90.25565,420.5941 90.749423,420.81081 88.295954,419.41507 L 84.756944,416.90114 L 82.529748,413.7265 L 81.544442,410.25163 L 82.727965,406.28797 L 86.032833,402.82659 L 90.902247,400.17859 L 95.382932,398.79878 L 99.500135,397.83328 L 99.500135,395.83326\" \n \
     id=\"path166\" \n \
     style=\"fill:url(#linearGradient3374);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"0\" \n \
     y=\"8\" \n \
     id=\"text168\" \n \
     style=\"font-size:8px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"414\" \n \
       id=\"tspan170\" \n \
       style=\"font-size:11px;fill:#000000;fill-opacity:1\">"

    data5 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 90.000086,441.71384 L 101.00015,441.71384 L 101.00015,445.71386 L 98.333456,445.71386 L 98.333456,443.71385 L 91.333426,443.71385\" \n \
     id=\"path172\" \n \
     style=\"fill:url(#linearGradient3403);fill-opacity:1;stroke:#800080;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.000086,460.04726 L 101.00015,460.04726 L 101.00015,456.04724 L 98.333456,456.04724 L 98.333456,458.04726 L 91.333426,458.04726\" \n \
     id=\"path174\" \n \
     style=\"fill:url(#linearGradient3400);fill-opacity:1;stroke:#800080;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.333346,438.38049 C 86.000066,438.38049 86.000066,438.38049 86.000066,438.38049 L 89.666746,441.04717 L 92.000096,445.04719 L 92.000096,457.71392 L 89.666746,461.04727 L 86.000066,463.71395 L 74.666676,463.71395 L 74.666676,463.71395 L 74.666676,466.38063 L 61.333274,466.38063 L 61.333274,463.71395 L 49.999884,463.71395 L 46.333199,461.04727 L 43.999854,457.71392 L 43.999854,445.04719 L 46.333199,441.04717 L 49.999884,438.38049 L 60.666604,438.38049 L 60.666604,441.71384 L 75.333346,441.71384 L 75.333346,438.38049 z\" \n \
     id=\"path176\" \n \
     style=\"fill:url(#linearGradient3397);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"-0.083335772\" \n \
     y=\"3.8805556\" \n \
     id=\"text178\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"69.916664\" \n \
       y=\"454.88055\" \n \
       id=\"tspan180\" \n \
       style=\"font-size:11px;fill:#000000;fill-opacity:1\">"

    data6 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text182\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"46\" \n \
       id=\"tspan184\" \n \
       style=\"font-size:11px\">"

    data7 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"48\" \n \
     id=\"text186\" \n \
     style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"46\" \n \
       y=\"247\" \n \
       id=\"tspan188\" \n \
       style=\"font-size:10.5px\">"

    data8 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"48\" \n \
     id=\"text190\" \n \
     style=\"font-size:10px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"100\" \n \
       y=\"247\" \n \
       id=\"tspan192\" \n \
       style=\"font-size:10.5px\">"

    data9 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 35.889163,215.16016 L 46.764163,215.16016 L 46.764163,210.66016 L 44.764163,210.66016 L 44.764163,212.16016 L 40.264163,212.16016 L 40.264163,200.66016 L 44.764163,200.66016 L 44.764163,202.16016 L 46.764163,202.16016 L 46.764163,197.78516 L 40.264163,197.78516 L 26.264163,189.28516 L 24.014163,189.28516 L 24.014163,187.28516 L 21.264163,187.28516 L 21.264163,197.53516 L 24.014163,197.53516 L 24.014163,195.53516 L 26.264163,195.53516 L 35.889163,201.53516 L 35.889163,215.16016 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient3411);fill-opacity:1;stroke:#a97513;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 106.05314,187.28516 L 116.92814,187.28516 L 116.92814,191.78516 L 114.92814,191.78516 L 114.92814,190.28516 L 110.42814,190.28516 L 110.42814,201.78516 L 114.92814,201.78516 L 114.92814,200.28516 L 116.92814,200.28516 L 116.92814,204.66016 L 110.42814,204.66016 L 96.428141,213.16016 L 94.178141,213.16016 L 94.178141,215.16016 L 91.428141,215.16016 L 91.428141,204.91016 L 94.178141,204.91016 L 94.178141,206.91016 L 96.428141,206.91016 L 106.05314,200.91016 L 106.05314,187.28516 z\" \n \
     id=\"path2796\" \n \
     style=\"fill:url(#linearGradient3419);fill-opacity:1;stroke:#a97513;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 26.264165,62.7824 L 46.764165,62.7824 L 46.764165,67.2824 L 44.764165,67.2824 L 44.764165,65.7824 L 40.264165,65.7824 L 40.264165,77.2824 L 44.764165,77.2824 L 44.764165,75.7824 L 46.764165,75.7824 L 46.764165,83.7824 L 44.764165,83.7824 L 44.764165,82.2824 L 40.264165,82.2824 L 40.264165,93.8869 L 44.764165,93.8869 L 44.764165,92.2824 L 46.764165,92.2824 L 46.764165,97.2824 L 26.264165,97.2824 L 26.264165,83.0324 L 24.014165,83.0324 L 24.014165,85.0324 L 21.264165,85.0324 L 21.264165,74.7824 L 24.014165,74.7824 L 24.014165,76.7824 L 26.264165,76.7824 L 26.264165,62.7824 z\" \n \
     id=\"path3132\" \n \
     style=\"fill:url(#linearGradient3255);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"21.014164\" \n \
     y=\"70.794121\" \n \
     id=\"text3134\" \n \
     style=\"font-size:6px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"34.014164\" \n \
       y=\"83.794121\" \n \
       id=\"tspan3136\" \n \
       style=\"font-size:11px\">+</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 26.264163,104.28331 L 46.764163,104.28331 L 46.764163,108.78331 L 44.764163,108.78331 L 44.764163,107.28331 L 40.264163,107.28331 L 40.264163,118.78331 L 44.764163,118.78331 L 44.764163,117.28331 L 46.764163,117.28331 L 46.764163,125.28331 L 44.764163,125.28331 L 44.764163,123.78331 L 40.264163,123.78331 L 40.264163,135.38781 L 44.764163,135.38781 L 44.764163,133.78331 L 46.764163,133.78331 L 46.764163,138.78331 L 26.264163,138.78331 L 26.264163,124.53331 L 24.014163,124.53331 L 24.014163,126.53331 L 21.264163,126.53331 L 21.264163,116.28331 L 24.014163,116.28331 L 24.014163,118.28331 L 26.264163,118.28331 L 26.264163,104.28331 z\" \n \
     id=\"path3441\" \n \
     style=\"fill:url(#linearGradient3271);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"21.014164\" \n \
     y=\"112.29504\" \n \
     id=\"text3443\" \n \
     style=\"font-size:6px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"34.014164\" \n \
       y=\"125.29504\" \n \
       id=\"tspan3445\" \n \
       style=\"font-size:11px\">x</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 91.61564,62.7824 L 112.24064,62.7824 L 112.24064,67.2824 L 110.11564,67.2824 L 110.11564,65.7824 L 105.61564,65.7824 L 105.61564,77.2824 L 110.11564,77.2824 L 110.11564,75.7824 L 112.24064,75.7824 L 112.24064,79.7824 L 121.74064,79.7824 L 121.74064,83.7824 L 119.74064,83.7824 L 119.74064,82.2824 L 115.24064,82.2824 L 115.24064,93.8869 L 119.74064,93.8869 L 119.74064,92.2824 L 121.74064,92.2824 L 121.74064,97.2824 L 91.61564,97.2824 L 91.61564,83.0324 L 89.36564,83.0324 L 89.36564,85.0324 L 86.61564,85.0324 L 86.61564,74.7824 L 89.36564,74.7824 L 89.36564,76.7824 L 91.61564,76.7824 L 91.61564,62.7824 z\" \n \
     id=\"path4413\" \n \
     style=\"fill:url(#linearGradient3263);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"90.365639\" \n \
     y=\"70.794121\" \n \
     id=\"text4415\" \n \
     style=\"font-size:6px;text-align:center;text-anchor:middle;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"103.36564\" \n \
       y=\"91.407402\" \n \
       id=\"tspan4417\" \n \
       style=\"font-size:11px;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none\">–</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 91.61564,104.28331 L 112.24064,104.28331 L 112.24064,108.78331 L 110.11564,108.78331 L 110.11564,107.28331 L 105.61564,107.28331 L 105.61564,118.78331 L 110.11564,118.78331 L 110.11564,117.28331 L 112.24064,117.28331 L 112.24064,121.28331 L 121.74064,121.28331 L 121.74064,125.28331 L 119.74064,125.28331 L 119.74064,123.78331 L 115.24064,123.78331 L 115.24064,135.38781 L 119.74064,135.38781 L 119.74064,133.78331 L 121.74064,133.78331 L 121.74064,138.78331 L 91.61564,138.78331 L 91.61564,124.53332 L 89.36564,124.53332 L 89.36564,126.53332 L 86.61564,126.53332 L 86.61564,116.28331 L 89.36564,116.28331 L 89.36564,118.28331 L 91.61564,118.28331 L 91.61564,104.28331 z\" \n \
     id=\"path4435\" \n \
     style=\"fill:url(#linearGradient3279);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"90.365639\" \n \
     y=\"112.29504\" \n \
     id=\"text4437\" \n \
     style=\"font-size:6px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"103.36564\" \n \
       y=\"132.90833\" \n \
       id=\"tspan4439\" \n \
       style=\"font-size:11px\">/</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 21.45166,145.78423 L 42.07666,145.78423 L 42.07666,150.28423 L 39.95166,150.28423 L 39.95166,148.78423 L 35.45166,148.78423 L 35.45166,160.28423 L 39.95166,160.28423 L 39.95166,158.78423 L 42.07666,158.78423 L 42.07666,162.78423 L 51.57666,162.78423 L 51.57666,166.78423 L 49.57666,166.78423 L 49.57666,165.28423 L 45.07666,165.28423 L 45.07666,176.88873 L 49.57666,176.88873 L 49.57666,175.28423 L 51.57666,175.28423 L 51.57666,180.28423 L 21.45166,180.28423 L 21.45166,166.03423 L 19.20166,166.03423 L 19.20166,168.03423 L 16.45166,168.03423 L 16.45166,157.78423 L 19.20166,157.78423 L 19.20166,159.78423 L 21.45166,159.78423 L 21.45166,145.78423 z\" \n \
     id=\"path4445\" \n \
     style=\"fill:url(#linearGradient3287);fill-opacity:1;stroke:#a000a0;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"20.449238\" \n \
     y=\"153.79596\" \n \
     id=\"text4447\" \n \
     style=\"font-size:6px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"33.449238\" \n \
       y=\"174.40924\" \n \
       id=\"tspan4449\" \n \
       style=\"font-size:10px\">"

    data10 = \
"</tspan> \n \
  </text> \n \
</svg> \n"

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname+".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring1).encode("utf-8"))
    FILE.write(data1)
    FILE.write(_(mystring2).encode("utf-8"))
    FILE.write(data2)
    FILE.write(_(mystring3).encode("utf-8"))
    FILE.write(data3)
    FILE.write(_(mystring4).encode("utf-8"))
    FILE.write(data4)
    FILE.write(_(mystring5).encode("utf-8"))
    FILE.write(data5)
    FILE.write(_(mystring6).encode("utf-8"))
    FILE.write(data6)
    FILE.write(_(mystring7).encode("utf-8"))
    FILE.write(data7)
    FILE.write(_(mystring8).encode("utf-8"))
    FILE.write(data8)
    FILE.write(_(mystring9).encode("utf-8"))
    FILE.write(data9)
    FILE.write(_(mystring10).encode("utf-8"))
    FILE.write(data10)
    FILE.close()
    return

if __name__ == "__main__":
    main()
