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

    myname = "templatesgroup"
    mystring1 = "Templates"
    mystring2 = "hide blocks"
    mystring3 = "sound"
    mygroup = "templates"

    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    print _(mystring1)


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
     id=\"defs98\"> \n \
    <linearGradient \n \
       id=\"linearGradient3245\"> \n \
      <stop \n \
         id=\"stop3247\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3249\" \n \
         style=\"stop-color:#ffff00;stop-opacity:0\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"11.45634\" \n \
       y1=\"109.14062\" \n \
       x2=\"63.081341\" \n \
       y2=\"109.14062\" \n \
       id=\"linearGradient3251\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"4.5188398\" \n \
       y1=\"188.5\" \n \
       x2=\"70.018837\" \n \
       y2=\"188.5\" \n \
       id=\"linearGradient3259\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"13.33134\" \n \
       y1=\"270.5\" \n \
       x2=\"61.206341\" \n \
       y2=\"270.5\" \n \
       id=\"linearGradient3267\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"12.124999\" \n \
       y1=\"392.34818\" \n \
       x2=\"80.875\" \n \
       y2=\"392.34818\" \n \
       id=\"linearGradient3275\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"47.393524\" \n \
       y1=\"52.893875\" \n \
       x2=\"97.606476\" \n \
       y2=\"52.893875\" \n \
       id=\"linearGradient3283\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"47.715\" \n \
       y1=\"445.94196\" \n \
       x2=\"97.284996\" \n \
       y2=\"445.94196\" \n \
       id=\"linearGradient3291\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"82.356911\" \n \
       y1=\"392.34818\" \n \
       x2=\"132.61295\" \n \
       y2=\"392.34818\" \n \
       id=\"linearGradient3307\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"82.928009\" \n \
       y1=\"248.60938\" \n \
       x2=\"134.55301\" \n \
       y2=\"248.60938\" \n \
       id=\"linearGradient3315\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"75.990517\" \n \
       y1=\"188.5\" \n \
       x2=\"141.49051\" \n \
       y2=\"188.5\" \n \
       id=\"linearGradient3323\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"82.928017\" \n \
       y1=\"119.21875\" \n \
       x2=\"134.55301\" \n \
       y2=\"119.21875\" \n \
       id=\"linearGradient3331\" \n \
       xlink:href=\"#linearGradient3245\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 0.5594301,0.5 L 0.49711997,486 C 1.5384064,488.33333 2.5796929,490.66667 3.6209793,493 C 5.2455992,494.33333 6.8702191,495.66667 8.494839,497 C 10.715355,497.66667 12.935872,498.33333 15.156388,499 L 128.9813,499 C 131.26413,498.33333 133.54695,497.66667 135.82978,497 C 137.81286,495.66667 139.79595,494.33333 141.77903,493 C 142.68698,490.66667 143.59493,488.33333 144.50288,486 L 144.54057,0.5 L 0.5594301,0.5 z\" \n \
     id=\"path3201\" \n \
     style=\"fill:#ffd000;fill-opacity:1;fill-rule:evenodd;stroke:#e0a000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.61703\" \n \
     height=\"0.14253192\" \n \
     x=\"10.691486\" \n \
     y=\"77.359131\" \n \
     id=\"rect3987\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.61703\" \n \
     height=\"0.14253192\" \n \
     x=\"10.691486\" \n \
     y=\"78.49942\" \n \
     id=\"rect3989\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.61703\" \n \
     height=\"0.14253192\" \n \
     x=\"10.691486\" \n \
     y=\"79.498322\" \n \
     id=\"rect3991\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#ffffc4;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-28.931932\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect3993\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-27.815523\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect3995\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7341847\" \n \
     y=\"-474.77127\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect3999\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7341847\" \n \
     y=\"-473.43195\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect4001\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 80.875,487.375 C 80.875,491.86231 77.125385,495.5 72.5,495.5 C 67.874615,495.5 64.125,491.86231 64.125,487.375 C 64.125,482.88769 67.874615,479.25 72.5,479.25 C 77.125385,479.25 80.875,482.88769 80.875,487.375 L 80.875,487.375 z\" \n \
     id=\"path4003\" \n \
     style=\"fill:#ff4040;fill-opacity:1;fill-rule:nonzero;stroke:#ff4040;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     xml:space=\"preserve\" \n \
     style=\"font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Bitstream Vera Sans;-inkscape-font-specification:Bitstream Vera Sans Bold\"><tspan \n \
       x=\"68\" \n \
       y=\"492\" \n \
       id=\"tspan4007\" \n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\">X</tspan></text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-style:normal;font-weight:normal;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"21.5\" \n \
       id=\"tspan2796\" \n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 48.060226,35.454452 L 96.939774,35.454452 L 96.939774,70.3333 L 48.060226,70.3333 L 48.060226,35.454452 z\" \n \
     id=\"path2685\" \n \
     style=\"fill:url(#linearGradient3283);fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1.33340001;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 89.277448,374.93417 L 132.02606,374.93417 L 132.02606,409.7622 L 89.277448,409.7622 L 89.277448,404.01542 L 82.943798,404.01542 L 82.943798,400.01522 L 89.277448,400.01522 L 89.277448,394.34827 L 82.943798,394.34827 L 82.943798,390.34807 L 89.277448,390.34807 L 89.277448,384.68113 L 82.943798,384.68113 L 82.943798,380.68093 L 89.277448,380.68093 L 89.277448,374.93417 z\" \n \
     id=\"path3254\" \n \
     style=\"fill:url(#linearGradient3307);fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1.17376971;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <g \n \
     transform=\"matrix(0.6667,0,0,0.6667,90.489602,374.01326)\" \n \
     id=\"g3256\" \n \
     style=\"display:block\"> \n \
    <g \n \
       id=\"g3258\" \n \
       style=\"display:inline\"> \n \
      <g \n \
         id=\"g3260\"> \n \
        <polygon \n \
           points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \" \n \
           id=\"polygon3262\" \n \
           style=\"fill:#ffffff;stroke:#010101;stroke-width:3.5\" /> \n \
        <polyline \n \
           id=\"polyline3264\" \n \
           points=\"43.818,18.027 31.874,18.027 31.874,6.088    \" \n \
           style=\"fill:none;stroke:#010101;stroke-width:3.5\" /> \n \
      </g> \n \
    </g> \n \
    <path \n \
       d=\"M 28.325,39.697 C 27.814,38.24 25.115,38.624 23.915,39.627 C 21.515,41.636 23.491,44.023 26.239,42.904 C 27.803,42.266 28.835,41.156 28.325,39.697 z\" \n \
       id=\"path3266\" \n \
       style=\"fill:#010101;stroke:#010101;stroke-width:3.5;display:inline\" /> \n \
    <line \n \
       id=\"line3268\" \n \
       y2=\"26.966999\" \n \
       y1=\"39.806\" \n \
       x2=\"28.941\" \n \
       x1=\"28.941\" \n \
       display=\"inline\" \n \
       style=\"fill:none;stroke:#010101;stroke-width:2.25;display:inline\" /> \n \
    <polygon \n \
       points=\"35.047,25.036 27.838,28.595 27.838,24.728 35.047,21.166 35.047,25.036 \" \n \
       id=\"polygon3270\" \n \
       style=\"fill:#010101;display:inline\" /> \n \
  </g> \n \
  <path \n \
     d=\"M 79.869997,426.51197 C 90.589997,426.51197 90.589997,426.51197 90.589997,426.51197 L 94.274998,429.19197 L 96.619998,433.21197 L 96.619998,455.99197 L 94.274998,460.01197 L 90.589997,462.69197 L 79.199997,462.69197 L 79.199997,462.69197 L 79.199997,465.37197 L 65.800008,465.37197 L 65.800008,462.69197 L 54.410003,462.69197 L 50.725003,460.01197 L 48.380002,455.99197 L 48.380002,433.21197 L 50.725003,429.19197 L 54.410003,426.51197 L 65.130007,426.51197 L 65.130007,429.86197 L 79.869997,429.86197 L 79.869997,426.51197 z\" \n \
     id=\"path2714\" \n \
     style=\"fill:url(#linearGradient3291);fill-opacity:1;stroke:#c0a000;stroke-width:1.33000004;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n"

    data2a = \
"  <text \n \
      style=\"font-size:12.06000042px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"450\" \n \
       id=\"tspan2718\" \n \
       style=\"font-size:12px\">"

    data2b = \
"  <text \n \
      style=\"font-size:12.06000042px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"444\" \n \
       id=\"tspan2718\" \n \
       style=\"font-size:12px\">"

    data3b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12.06000042px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"457\" \n \
       id=\"tspan2722\" \n \
       style=\"font-size:12px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <rect \n \
     width=\"123.61703\" \n \
     height=\"0.14253192\" \n \
     x=\"10.691486\" \n \
     y=\"415.35913\" \n \
     id=\"rect3434\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.61703\" \n \
     height=\"0.14253192\" \n \
     x=\"10.691486\" \n \
     y=\"416.49945\" \n \
     id=\"rect3436\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.61703\" \n \
     height=\"0.14253192\" \n \
     x=\"10.691486\" \n \
     y=\"417.49835\" \n \
     id=\"rect3438\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#ffffc4;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <g \n \
     transform=\"matrix(0.5,0,0,0.5,59.18725,38.91364)\" \n \
     id=\"activity-journal\" \n \
     style=\"stroke:#000000;stroke-width:4;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;display:block\"> \n \
    <path \n \
       d=\"M 45.866,44.669 C 45.866,47.18 44.338,49 41.534,49 L 12.077,49 L 12.077,6 L 41.535,6 C 43.685,6 45.867,8.154 45.867,10.33 L 45.866,44.669 L 45.866,44.669 z\" \n \
       id=\"path3155\" \n \
       style=\"fill:#ffffff;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <line \n \
       id=\"line3157\" \n \
       y2=\"48.881001\" \n \
       y1=\"6.1209998\" \n \
       x2=\"21.341\" \n \
       x1=\"21.341\" \n \
       style=\"fill:none;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 7.384,14.464 C 7.384,14.464 9.468,15.159 11.554,15.159 C 13.64,15.159 15.727,14.464 15.727,14.464\" \n \
       id=\"path3159\" \n \
       style=\"fill:none;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 7.384,28.021 C 7.384,28.021 9.296,28.716 11.729,28.716 C 14.162,28.716 15.728,28.021 15.728,28.021\" \n \
       id=\"path3161\" \n \
       style=\"fill:none;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 7.384,41.232 C 7.384,41.232 9.12,41.927 11.902,41.927 C 14.683,41.927 15.727,41.232 15.727,41.232\" \n \
       id=\"path3163\" \n \
       style=\"fill:none;stroke:#000000;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  </g> \n \
  <path \n \
     d=\"M 35.39384,88.28125 L 29.48759,88.28125 L 29.48759,90.15625 L 21.23759,90.15625 L 21.23759,88.28125 L 15.33134,88.28125 C 15.33134,88.28125 13.87478,89.25949 13.36259,89.78125 C 12.956,90.19543 11.95634,92.03125 11.95634,92.03125 L 11.95634,126.24625 C 11.95634,126.24625 12.196385,127.49447 12.518825,127.74812 C 12.830315,127.99315 14.20628,128.59375 14.20628,128.59375 L 21.70634,128.59375 L 21.70634,130 L 29.20634,130 L 29.20634,128.59375 L 62.58134,128.59375 L 62.58134,89.78125 L 37.45634,89.78125 L 36.50516,89.03529 L 35.39384,88.28125 z\" \n \
     id=\"path4158\" \n \
     style=\"fill:url(#linearGradient3251);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 15.61259,105.37364 L 43.00805,105.37364 L 43.00805,125.04148 L 15.61259,125.04148 L 15.61259,105.37364 z\" \n \
     id=\"path4162\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <polygon \n \
     points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \" \n \
     transform=\"matrix(0.375,0,0,0.375,42.63809,103.40725)\" \n \
     id=\"polygon2963\" \n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" /> \n \
  <polyline \n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" \n \
     points=\"43.818,18.027 31.874,18.027 31.874,6.088    \" \n \
     id=\"polyline2965\" \n \
     transform=\"matrix(0.375,0,0,0.375,42.63809,103.40725)\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"49.341213\" \n \
     x2=\"56.466213\" \n \
     y1=\"113.25099\" \n \
     y2=\"113.25099\" \n \
     id=\"line2967\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"49.341213\" \n \
     x2=\"56.466213\" \n \
     y1=\"115.87599\" \n \
     y2=\"115.87599\" \n \
     id=\"line2969\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"49.341213\" \n \
     x2=\"56.466213\" \n \
     y1=\"118.50099\" \n \
     y2=\"118.50099\" \n \
     id=\"line2971\" /> \n \
  <path \n \
     d=\"M 28.45634,157.5625 L 22.55009,157.5625 L 22.55009,159.4375 L 14.30009,159.4375 L 14.30009,157.5625 L 8.39384,157.5625 C 8.39384,157.5625 6.93728,158.54076 6.42509,159.0625 C 6.0185,159.47668 5.01884,161.3125 5.01884,161.3125 L 5.01884,215.6875 C 5.01884,215.6875 5.258885,217.30885 5.581325,217.5625 C 5.892815,217.80752 7.26878,218.3125 7.26878,218.3125 L 14.76884,218.3125 L 14.76884,219.4375 L 22.26884,219.4375 L 22.26884,218.3125 L 69.51884,218.3125 L 69.51884,159.0625 L 30.51884,159.0625 L 29.56766,158.31653 L 28.45634,157.5625 z\" \n \
     id=\"path4390\" \n \
     style=\"fill:url(#linearGradient3259);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 8.67509,174.65489 L 36.07055,174.65489 L 36.07055,194.32273 L 8.67509,194.32273 L 8.67509,174.65489 z\" \n \
     id=\"path4394\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 38.67509,174.65479 L 66.07055,174.65479 L 66.07055,194.32263 L 38.67509,194.32263 L 38.67509,174.65479 z\" \n \
     id=\"path2418\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <polygon \n \
     points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \" \n \
     transform=\"matrix(0.375,0,0,0.375,4.95059,195.5635)\" \n \
     id=\"polygon4402\" \n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" /> \n \
  <polyline \n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" \n \
     points=\"43.818,18.027 31.874,18.027 31.874,6.088    \" \n \
     id=\"polyline4404\" \n \
     transform=\"matrix(0.375,0,0,0.375,4.95059,195.5635)\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"11.653712\" \n \
     x2=\"18.778713\" \n \
     y1=\"205.40726\" \n \
     y2=\"205.40726\" \n \
     id=\"line4406\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"11.653712\" \n \
     x2=\"18.778713\" \n \
     y1=\"208.03226\" \n \
     y2=\"208.03226\" \n \
     id=\"line4408\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"11.653712\" \n \
     x2=\"18.778713\" \n \
     y1=\"210.65726\" \n \
     y2=\"210.65726\" \n \
     id=\"line4410\" /> \n \
  <polygon \n \
     points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \" \n \
     transform=\"matrix(0.375,0,0,0.375,34.95059,195.5635)\" \n \
     id=\"polygon2582\" \n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" /> \n \
  <polyline \n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" \n \
     points=\"43.818,18.027 31.874,18.027 31.874,6.088    \" \n \
     id=\"polyline2584\" \n \
     transform=\"matrix(0.375,0,0,0.375,34.95059,195.5635)\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"41.653713\" \n \
     x2=\"48.778713\" \n \
     y1=\"205.40726\" \n \
     y2=\"205.40726\" \n \
     id=\"line2586\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"41.653713\" \n \
     x2=\"48.778713\" \n \
     y1=\"208.03226\" \n \
     y2=\"208.03226\" \n \
     id=\"line2588\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"41.653713\" \n \
     x2=\"48.778713\" \n \
     y1=\"210.65726\" \n \
     y2=\"210.65726\" \n \
     id=\"line2590\" /> \n \
  <path \n \
     d=\"M 37.26884,227.75 L 31.36259,227.75 L 31.36259,229.4375 L 23.11259,229.4375 L 23.11259,227.75 L 17.20634,227.75 C 17.20634,227.75 15.749783,228.72825 15.23759,229.25 C 14.830993,229.66418 13.83134,231.5 13.83134,231.5 L 13.83134,309.125 C 13.83134,309.125 14.071389,310.93385 14.393825,311.1875 C 14.705314,311.43252 16.081282,312.125 16.081282,312.125 L 23.58134,312.125 L 23.58134,313.25 L 31.08134,313.25 L 31.08134,312.125 L 60.70634,312.125 L 60.70634,229.25 L 39.33134,229.25 L 38.380155,228.50404 L 37.26884,227.75 z\" \n \
     id=\"path4690\" \n \
     style=\"fill:url(#linearGradient3267);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 106.86551,88.28124 L 100.95927,88.28124 L 100.95927,90.15625 L 92.709265,90.15625 L 92.709265,88.28124 L 86.803015,88.28124 C 86.803015,88.28124 85.346455,89.2595 84.834265,89.78124 C 84.427675,90.19543 83.428015,92.03124 83.428015,92.03124 L 83.428015,146.40625 C 83.428015,146.40625 83.66806,147.6526 83.9905,147.90625 C 84.30199,148.15129 85.677955,148.65625 85.677955,148.65625 L 93.178015,148.65625 L 93.178015,150.15625 L 100.67802,150.15625 L 100.67802,148.65625 L 134.05301,148.65625 L 134.05301,89.78124 L 108.92802,89.78124 L 107.97684,89.03528 L 106.86551,88.28124 z\" \n \
     id=\"path5171\" \n \
     style=\"fill:url(#linearGradient3331);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 87.084265,105.37364 L 114.47973,105.37364 L 114.47973,125.04147 L 87.084265,125.04147 L 87.084265,105.37364 z\" \n \
     id=\"path5175\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <polygon \n \
     points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \" \n \
     transform=\"matrix(0.375,0,0,0.375,114.10977,103.40724)\" \n \
     id=\"polygon5183\" \n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" /> \n \
  <polyline \n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" \n \
     points=\"43.818,18.027 31.874,18.027 31.874,6.088    \" \n \
     id=\"polyline5185\" \n \
     transform=\"matrix(0.375,0,0,0.375,114.10977,103.40724)\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"120.81288\" \n \
     x2=\"127.93788\" \n \
     y1=\"113.25101\" \n \
     y2=\"113.25101\" \n \
     id=\"line5187\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"120.81288\" \n \
     x2=\"127.93788\" \n \
     y1=\"115.87601\" \n \
     y2=\"115.87601\" \n \
     id=\"line5189\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"120.81288\" \n \
     x2=\"127.93788\" \n \
     y1=\"118.50101\" \n \
     y2=\"118.50101\" \n \
     id=\"line5191\" /> \n \
  <path \n \
     d=\"M 87.084265,126.83216 L 114.47973,126.83216 L 114.47973,146.49999 L 87.084265,146.49999 L 87.084265,126.83216 z\" \n \
     id=\"path2425\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <polygon \n \
     points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \" \n \
     transform=\"matrix(0.375,0,0,0.375,113.96295,125.10807)\" \n \
     id=\"polygon2433\" \n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" /> \n \
  <polyline \n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" \n \
     points=\"43.818,18.027 31.874,18.027 31.874,6.088    \" \n \
     id=\"polyline2435\" \n \
     transform=\"matrix(0.375,0,0,0.375,113.96295,125.10807)\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"120.66608\" \n \
     x2=\"127.79108\" \n \
     y1=\"134.95181\" \n \
     y2=\"134.95181\" \n \
     id=\"line2437\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"120.66608\" \n \
     x2=\"127.79108\" \n \
     y1=\"137.57681\" \n \
     y2=\"137.57681\" \n \
     id=\"line2439\" /> \n \
  <line \n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\" \n \
     display=\"inline\" \n \
     x1=\"120.66608\" \n \
     x2=\"127.79108\" \n \
     y1=\"140.20181\" \n \
     y2=\"140.20181\" \n \
     id=\"line2441\" /> \n \
  <path \n \
     d=\"M 99.928015,157.5625 L 94.021765,157.5625 L 94.021765,159.4375 L 85.771765,159.4375 L 85.771765,157.5625 L 79.865515,157.5625 C 79.865515,157.5625 78.408955,158.54075 77.896765,159.0625 C 77.490175,159.47668 76.490515,161.3125 76.490515,161.3125 L 76.490515,215.6875 C 76.490515,215.6875 76.73056,216.93385 77.053,217.1875 C 77.36449,217.43253 78.740455,217.9375 78.740455,217.9375 L 86.240515,217.9375 L 86.240515,219.4375 L 93.740515,219.4375 L 93.740515,217.9375 L 140.99051,217.9375 L 140.99051,159.0625 L 101.99051,159.0625 L 101.03934,158.31654 L 99.928015,157.5625 z\" \n \
     id=\"path5376\" \n \
     style=\"fill:url(#linearGradient3323);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 80.146765,174.65489 L 107.54223,174.65489 L 107.54223,194.32273 L 80.146765,194.32273 L 80.146765,174.65489 z\" \n \
     id=\"path5380\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 110.14676,174.65478 L 137.54223,174.65478 L 137.54223,194.32262 L 110.14676,194.32262 L 110.14676,174.65478 z\" \n \
     id=\"path5382\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 80.146765,196.1134 L 107.54223,196.1134 L 107.54223,215.78125 L 80.146765,215.78125 L 80.146765,196.1134 z\" \n \
     id=\"path2410\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 110.14676,196.1133 L 137.54223,196.1133 L 137.54223,215.78114 L 110.14676,215.78114 L 110.14676,196.1133 z\" \n \
     id=\"path2412\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 106.86551,227.75 L 100.95926,227.75 L 100.95926,229.625 L 92.70926,229.625 L 92.70926,227.75 L 86.80301,227.75 C 86.80301,227.75 85.34645,228.72824 84.83426,229.25 C 84.42767,229.66418 83.42801,231.5 83.42801,231.5 L 83.42801,265.71499 C 83.42801,265.71499 83.668055,266.96322 83.990495,267.21687 C 84.301985,267.4619 85.67795,268.0625 85.67795,268.0625 L 93.17801,268.0625 L 93.17801,269.46875 L 100.67801,269.46875 L 100.67801,268.0625 L 134.05301,268.0625 L 134.05301,229.25 L 108.92801,229.25 L 107.97683,228.50404 L 106.86551,227.75 z\" \n \
     id=\"path3036\" \n \
     style=\"fill:url(#linearGradient3315);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 87.08426,244.84239 L 114.47972,244.84239 L 114.47972,264.51023 L 87.08426,264.51023 L 87.08426,244.84239 z\" \n \
     id=\"path3040\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 43.999999,379.03568 L 36.124999,379.03568 L 36.124999,381.03568 L 25.124999,381.03568 L 25.124999,379.03568 L 17.249999,379.03568 C 17.249999,379.03568 15.307923,379.34001 14.624999,380.03568 C 14.082869,380.58793 12.749999,382.03568 12.749999,382.03568 L 12.749999,400.65568 C 12.749999,400.65568 13.070065,402.31999 13.49998,402.65818 C 13.915296,402.98489 15.749921,403.78568 15.749921,403.78568 L 25.749999,403.78568 L 25.749999,405.66068 L 35.749999,405.66068 L 35.749999,403.78568 L 75.74837,403.78568 L 75.75,398.03568 L 80.25,398.03568 L 80.25,395.28568 L 75.75,395.28568 L 75.75,390.78568 L 80.25,390.78568 L 80.25,388.03568 L 75.75,388.03568 L 75.75,382.03568 L 46.749999,382.03568 L 45.481752,380.03568 L 43.999999,379.03568 z\" \n \
     id=\"path3037\" \n \
     style=\"fill:url(#linearGradient3275);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1.25;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12.06000042px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"47\" \n \
       y=\"396\" \n \
       id=\"tspan3043\" \n \
       style=\"font-size:12px\">"

    data5 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 87.75,93.55 L 89.425,93.55 L 89.425,94.89 L 91.77,94.89 L 91.77,93.55 L 122.4225,93.55 L 122.4225,100.25 L 91.77,100.25 L 91.77,98.91 L 89.425,98.91 L 89.425,100.25 L 87.75,100.25 L 87.75,93.55 z\" \n \
     id=\"path9\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,291.78471 L 19.425,291.78471 L 19.425,293.12471 L 21.77,293.12471 L 21.77,291.78471 L 52.4225,291.78471 L 52.4225,298.48471 L 21.77,298.48471 L 21.77,297.14471 L 19.425,297.14471 L 19.425,298.48471 L 17.75,298.48471 L 17.75,291.78471 z\" \n \
     id=\"path3323\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,282.01942 L 19.425,282.01942 L 19.425,283.35942 L 21.77,283.35942 L 21.77,282.01942 L 52.4225,282.01942 L 52.4225,288.71942 L 21.77,288.71942 L 21.77,287.37942 L 19.425,287.37942 L 19.425,288.71942 L 17.75,288.71942 L 17.75,282.01942 z\" \n \
     id=\"path3325\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,272.25413 L 19.424999,272.25413 L 19.424999,273.59413 L 21.769999,273.59413 L 21.769999,272.25413 L 52.422499,272.25413 L 52.422499,278.95413 L 21.769999,278.95413 L 21.769999,277.61413 L 19.424999,277.61413 L 19.424999,278.95413 L 17.75,278.95413 L 17.75,272.25413 z\" \n \
     id=\"path3327\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,262.48884 L 19.425,262.48884 L 19.425,263.82884 L 21.77,263.82884 L 21.77,262.48884 L 52.4225,262.48884 L 52.4225,269.18884 L 21.77,269.18884 L 21.77,267.84884 L 19.425,267.84884 L 19.425,269.18884 L 17.75,269.18884 L 17.75,262.48884 z\" \n \
     id=\"path3329\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,242.95827 L 19.425,242.95827 L 19.425,244.29827 L 21.77,244.29827 L 21.77,242.95827 L 52.4225,242.95827 L 52.4225,249.65827 L 21.77,249.65827 L 21.77,248.31827 L 19.425,248.31827 L 19.425,249.65827 L 17.75,249.65827 L 17.75,242.95827 z\" \n \
     id=\"path3331\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 8.75,163.55 L 10.425,163.55 L 10.425,164.89 L 12.77,164.89 L 12.77,163.55 L 43.4225,163.55 L 43.4225,170.25 L 12.77,170.25 L 12.77,168.91 L 10.425,168.91 L 10.425,170.25 L 8.75,170.25 L 8.75,163.55 z\" \n \
     id=\"path3333\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 15.75,93.55 L 17.425,93.55 L 17.425,94.89 L 19.77,94.89 L 19.77,93.55 L 50.4225,93.55 L 50.4225,100.25 L 19.77,100.25 L 19.77,98.91 L 17.425,98.91 L 17.425,100.25 L 15.75,100.25 L 15.75,93.55 z\" \n \
     id=\"path3335\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 80.75,163.55 L 82.425,163.55 L 82.425,164.89 L 84.77,164.89 L 84.77,163.55 L 115.4225,163.55 L 115.4225,170.25 L 84.77,170.25 L 84.77,168.91 L 82.425,168.91 L 82.425,170.25 L 80.75,170.25 L 80.75,163.55 z\" \n \
     id=\"path3337\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,233.19298 L 19.425,233.19298 L 19.425,234.53298 L 21.77,234.53298 L 21.77,233.19298 L 52.4225,233.19298 L 52.4225,239.89298 L 21.77,239.89298 L 21.77,238.55298 L 19.425,238.55298 L 19.425,239.89298 L 17.75,239.89298 L 17.75,233.19298 z\" \n \
     id=\"path3339\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,301.55 L 19.425,301.55 L 19.425,302.89 L 21.77,302.89 L 21.77,301.55 L 52.4225,301.55 L 52.4225,308.25 L 21.77,308.25 L 21.77,306.91 L 19.425,306.91 L 19.425,308.25 L 17.75,308.25 L 17.75,301.55 z\" \n \
     id=\"path3341\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 17.75,252.72355 L 19.425,252.72355 L 19.425,254.06355 L 21.77,254.06355 L 21.77,252.72355 L 52.4225,252.72355 L 52.4225,259.42355 L 21.77,259.42355 L 21.77,258.08355 L 19.425,258.08355 L 19.425,259.42355 L 17.75,259.42355 L 17.75,252.72355 z\" \n \
     id=\"path3343\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 87.25,233.55 L 88.925,233.55 L 88.925,234.89 L 91.27,234.89 L 91.27,233.55 L 121.9225,233.55 L 121.9225,240.25 L 91.27,240.25 L 91.27,238.91 L 88.925,238.91 L 88.925,240.25 L 87.25,240.25 L 87.25,233.55 z\" \n \
     id=\"path3345\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
</svg> \n "

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
    FILE.close()
    return

if __name__ == "__main__":
    main()

