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

    myname = "myblocksgroup"
    mystring1 = "My Blocks"
    mystring2 = "stack 1"
    mystring3 = "stack 2"
    mystring4 = "store in box 1"
    mystring5 = "box 1"
    mystring6 = "store in box 2"
    mystring7 = "box 2"
    mystring8 = "push"
    mystring9 = "pop"
    mystring10 = "show heap"
    mystring11 = "clear heap"
    mystring12 = "name"
    mystring13 = "start"
    mygroup = "myblocks"

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
    print _(mystring11)
    print _(mystring12)
    print _(mystring13)

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
     id=\"defs92\"> \n \
    <linearGradient \n \
       id=\"linearGradient3239\"> \n \
      <stop \n \
         id=\"stop3241\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3243\" \n \
         style=\"stop-color:#ffff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"47.499626\" \n \
       y1=\"46.558704\" \n \
       x2=\"97.500374\" \n \
       y2=\"46.558704\" \n \
       id=\"linearGradient3245\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"3.8948069\" \n \
       y1=\"74.402542\" \n \
       x2=\"70.231407\" \n \
       y2=\"74.402542\" \n \
       id=\"linearGradient3253\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"81.979385\" \n \
       y1=\"74.402542\" \n \
       x2=\"130.98178\" \n \
       y2=\"74.402542\" \n \
       id=\"linearGradient3261\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"3.8948069\" \n \
       y1=\"115.66337\" \n \
       x2=\"70.231407\" \n \
       y2=\"115.66337\" \n \
       id=\"linearGradient3269\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"81.979385\" \n \
       y1=\"115.66337\" \n \
       x2=\"130.98178\" \n \
       y2=\"115.66337\" \n \
       id=\"linearGradient3277\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"35.25\" \n \
       y1=\"145.67612\" \n \
       x2=\"109.75\" \n \
       y2=\"145.67612\" \n \
       id=\"linearGradient3285\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"40\" \n \
       y1=\"180.0162\" \n \
       x2=\"105\" \n \
       y2=\"180.0162\" \n \
       id=\"linearGradient3293\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"7.6595821\" \n \
       y1=\"226.22649\" \n \
       x2=\"56.661983\" \n \
       y2=\"226.22649\" \n \
       id=\"linearGradient3301\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"70.022545\" \n \
       y1=\"226.22649\" \n \
       x2=\"140.026\" \n \
       y2=\"226.22649\" \n \
       id=\"linearGradient3309\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"7.6595821\" \n \
       y1=\"272.65366\" \n \
       x2=\"56.661983\" \n \
       y2=\"272.65366\" \n \
       id=\"linearGradient3317\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"70.022545\" \n \
       y1=\"272.65366\" \n \
       x2=\"140.026\" \n \
       y2=\"272.65366\" \n \
       id=\"linearGradient3325\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"37.0625\" \n \
       y1=\"311.59515\" \n \
       x2=\"102.0625\" \n \
       y2=\"311.59515\" \n \
       id=\"linearGradient3333\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"36.24942\" \n \
       y1=\"341.4375\" \n \
       x2=\"100.37442\" \n \
       y2=\"341.4375\" \n \
       id=\"linearGradient3341\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"37.495003\" \n \
       y1=\"367.91702\" \n \
       x2=\"107.84001\" \n \
       y2=\"367.91702\" \n \
       id=\"linearGradient3349\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3357\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3359\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3361\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3363\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3365\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3367\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3371\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-1.571244,4.74717)\" /> \n \
    <linearGradient \n \
       x1=\"9.8133535\" \n \
       y1=\"399.42288\" \n \
       x2=\"67.875931\" \n \
       y2=\"399.42288\" \n \
       id=\"linearGradient3374\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(-1.571244,4.74717)\" /> \n \
    <linearGradient \n \
       x1=\"64.812042\" \n \
       y1=\"396.17004\" \n \
       x2=\"134.81549\" \n \
       y2=\"396.17004\" \n \
       id=\"linearGradient3385\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"64.812042\" \n \
       y1=\"396.17004\" \n \
       x2=\"134.81549\" \n \
       y2=\"396.17004\" \n \
       id=\"linearGradient3387\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"64.812042\" \n \
       y1=\"396.17004\" \n \
       x2=\"134.81549\" \n \
       y2=\"396.17004\" \n \
       id=\"linearGradient3389\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"64.812042\" \n \
       y1=\"396.17004\" \n \
       x2=\"134.81549\" \n \
       y2=\"396.17004\" \n \
       id=\"linearGradient3393\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(5.210508,8)\" /> \n \
    <linearGradient \n \
       x1=\"64.812042\" \n \
       y1=\"396.17004\" \n \
       x2=\"134.81549\" \n \
       y2=\"396.17004\" \n \
       id=\"linearGradient3396\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(5.210508,8)\" /> \n \
    <linearGradient \n \
       x1=\"8.2421103\" \n \
       y1=\"444.33197\" \n \
       x2=\"57.244511\" \n \
       y2=\"444.33197\" \n \
       id=\"linearGradient3404\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"81.979385\" \n \
       y1=\"444.33197\" \n \
       x2=\"130.9818\" \n \
       y2=\"444.33197\" \n \
       id=\"linearGradient3412\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 0.4344301,0.5 L 0.37211997,486.41023 L 3.4959793,493.14297 L 8.369839,497.1072 L 15.031388,499.50288 L 128.8563,499.50288 L 135.70478,496.93866 L 141.65403,492.04729 L 144.37788,483.79171 L 144.41557,0.5 L 0.4344301,0.5 z\" \n \
     id=\"path23\" \n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1px;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.5\" \n \
     height=\"0.14\" \n \
     x=\"10.691486\" \n \
     y=\"197.35913\" \n \
     id=\"rect25\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.5\" \n \
     height=\"0.14\" \n \
     x=\"10.691486\" \n \
     y=\"198.49942\" \n \
     id=\"rect27\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.5\" \n \
     height=\"0.14\" \n \
     x=\"10.691486\" \n \
     y=\"199.49832\" \n \
     id=\"rect29\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-28.931932\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect31\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-27.815523\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect33\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-384.77127\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect35\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-383.43195\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect37\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 79.5,438.375 C 79.5,442.86231 75.750385,446.5 71.125,446.5 C 66.499615,446.5 62.75,442.86231 62.75,438.375 C 62.75,433.88769 66.499615,430.25 71.125,430.25 C 75.750385,430.25 79.5,433.88769 79.5,438.375 L 79.5,438.375 z\" \n \
     transform=\"translate(1.375,47.250977)\" \n \
     id=\"path39\" \n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text41\" \n \
     style=\"font-size:12px;font-variant:normal;font-weight:bold;text-align:start;text-anchor:start;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:1px;stroke-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"490\" \n \
       id=\"tspan43\" \n \
       style=\"font-size:12px\">X</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text45\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"21.5\" \n \
       id=\"tspan47\" \n \
       style=\"font-size:18px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 69.731407,74.40254 L 69.731407,74.40254 L 43.730107,89.73664 L 43.730107,89.73664 L 43.730107,92.40344 L 30.396107,92.40344 L 30.396107,89.73664 C 30.396107,89.73664 4.3948068,74.40254 4.3948068,74.40254 C 4.3948068,74.40254 37.063107,56.40164 37.063107,56.40164 C 37.063107,56.40164 69.731407,74.40254 69.731407,74.40254 z\" \n \
     id=\"path49\" \n \
     style=\"fill:url(#linearGradient3253);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"18\" \n \
     id=\"text51\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"79\" \n \
       id=\"tspan53\" \n \
       style=\"font-size:10.5px\">"

    data2 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 113.81428,60.40184 C 124.48148,60.40184 124.48148,60.40184 124.48148,60.40184 C 124.48148,60.40184 127.23615,62.059625 128.14833,63.06864 C 129.08003,64.099241 130.48178,67.06884 130.48178,67.06884 L 130.48178,79.73614 C 130.48178,79.73614 129.00368,82.198699 128.14833,83.06964 C 127.19525,84.040108 124.48148,85.73644 124.48148,85.73644 L 113.14758,85.73644 L 113.14758,85.73644 L 113.14758,88.40324 L 99.813583,88.40324 L 99.813583,85.73644 L 88.479683,85.73644 C 88.479683,85.73644 85.765921,84.040108 84.812833,83.06964 C 83.95749,82.198699 82.479383,79.73614 82.479383,79.73614 L 82.479383,67.06884 C 82.479383,67.06884 83.881139,64.099241 84.812833,63.06864 C 85.725013,62.059625 88.479683,60.40184 88.479683,60.40184 L 99.146883,60.40184 L 99.146883,63.73534 L 113.81428,63.73534 L 113.81428,60.40184 z\" \n \
     id=\"path55\" \n \
     style=\"fill:url(#linearGradient3261);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"18\" \n \
     id=\"text57\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"107\" \n \
       y=\"77\" \n \
       id=\"tspan59\" \n \
       style=\"font-size:10.5px\">"

    data3 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 69.731407,115.66337 L 69.731407,115.66337 L 43.730107,130.99747 L 43.730107,130.99747 L 43.730107,133.66427 L 30.396107,133.66427 L 30.396107,130.99747 C 30.396107,130.99747 4.3948068,115.66337 4.3948068,115.66337 C 4.3948068,115.66337 37.063107,97.662473 37.063107,97.662473 C 37.063107,97.662473 69.731407,115.66337 69.731407,115.66337 z\" \n \
     id=\"path61\" \n \
     style=\"fill:url(#linearGradient3269);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"16\" \n \
     id=\"text63\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"120\" \n \
       id=\"tspan65\" \n \
       style=\"font-size:10.5px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 113.81428,101.66267 C 124.48148,101.66267 124.48148,101.66267 124.48148,101.66267 C 124.48148,101.66267 127.23615,103.32046 128.14833,104.32947 C 129.08003,105.36007 130.48178,108.32967 130.48178,108.32967 L 130.48178,120.99697 C 130.48178,120.99697 129.00368,123.45953 128.14833,124.33047 C 127.19525,125.30094 124.48148,126.99727 124.48148,126.99727 L 113.14758,126.99727 L 113.14758,126.99727 L 113.14758,129.66407 L 99.813583,129.66407 L 99.813583,126.99727 L 88.479683,126.99727 C 88.479683,126.99727 85.765921,125.30094 84.812833,124.33047 C 83.95749,123.45953 82.479383,120.99697 82.479383,120.99697 L 82.479383,108.32967 C 82.479383,108.32967 83.881139,105.36007 84.812833,104.32947 C 85.725013,103.32046 88.479683,101.66267 88.479683,101.66267 L 99.146883,101.66267 L 99.146883,104.99617 L 113.81428,104.99617 L 113.81428,101.66267 z\" \n \
     id=\"path67\" \n \
     style=\"fill:url(#linearGradient3277);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"16\" \n \
     id=\"text69\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"107\" \n \
       y=\"120\" \n \
       id=\"tspan71\" \n \
       style=\"font-size:10.5px\">"

    data5 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 72.25,127.42612 L 35.75,145.67612 L 67.25,161.92612 L 67.25,163.92612 L 77.25,163.92612 L 77.25,161.92612 L 109.25,145.67612 L 72.25,127.42612 z\" \n \
     id=\"path6722\" \n \
     style=\"fill:url(#linearGradient3285);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 78,169.5162 C 86,169.5162 100,169.5162 100,169.5162 C 100,169.5162 102.0659,170.75948 102.75,171.5162 C 103.44873,172.28911 104.5,174.5162 104.5,174.5162 L 104.5,184.0162 C 104.5,184.0162 103.39147,185.86303 102.75,186.5162 C 102.03522,187.24401 100,188.5162 100,188.5162 L 77.5,188.5162 L 77.5,188.5162 L 77.5,190.5162 L 67.5,190.5162 L 67.5,188.5162 L 45,188.5162 C 45,188.5162 42.96478,187.24401 42.25,186.5162 C 41.608525,185.86303 40.5,184.0162 40.5,184.0162 L 40.5,174.5162 C 40.5,174.5162 41.551264,172.28911 42.25,171.5162 C 42.934101,170.75948 45,169.5162 45,169.5162 L 67,169.5162 L 67,172.0162 L 78,172.0162 L 78,169.5162 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient3293);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.161882,216.05931 L 65.162432,216.05931 L 65.162432,220.05951 L 62.495632,220.05951 L 62.495632,218.05941 L 55.495282,218.05941\" \n \
     id=\"path87\" \n \
     style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.161882,234.39356 L 65.162432,234.39356 L 65.162432,230.39336 L 62.495632,230.39336 L 62.495632,232.39346 L 55.495282,232.39346\" \n \
     id=\"path89\" \n \
     style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 39.494482,206.89218 C 50.161682,206.89218 50.161682,206.89218 50.161682,206.89218 L 53.828532,209.55898 L 56.161982,213.55918 L 56.161982,236.22698 L 53.828532,240.22718 L 50.161682,242.89398 L 38.827782,242.89398 L 38.827782,242.89398 L 38.827782,245.56078 L 25.493782,245.56078 L 25.493782,242.89398 L 14.159882,242.89398 L 10.493032,240.22718 L 8.1595819,236.22698 L 8.1595819,213.55918 L 10.493032,209.55898 L 14.159882,206.89218 L 24.827082,206.89218 L 24.827082,210.22568 L 39.494482,210.22568 L 39.494482,206.89218 z\" \n \
     id=\"path91\" \n \
     style=\"fill:url(#linearGradient3301);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n "

    data6a = \
"  <text \n \
     y=\"26\" \n \
     id=\"text93\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"230\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:10.5px\">"

    data6b = \
"  <text \n \
     y=\"26\" \n \
     id=\"text93\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"224\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:10px\">"

    data6c = \
"  <text \n \
     y=\"26\" \n \
     id=\"text93\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"220\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:10px\">"


    data7b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text97\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"236\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:10.5px\">"

    data7c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text97\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"229\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:10px\">"

    data8c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text97\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"238\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:10px\">"

    data9 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 70.522547,219.55948 L 73.856047,219.55948 L 73.856047,222.22628 L 78.522947,222.22628 L 78.522947,219.55948 L 139.526,219.55948 L 139.526,232.89348 L 78.522947,232.89348 L 78.522947,230.22668 L 73.856047,230.22668 L 73.856047,232.89348 L 70.522547,232.89348 L 70.522547,219.55948 z\" \n \
     id=\"path101\" \n \
     style=\"fill:url(#linearGradient3309);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text103\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"106\" \n \
       y=\"229.5\" \n \
       id=\"tspan105\" \n \
       style=\"font-size:10.5px\">"

    data10 = \
"</tspan> \n \
  </text> \n \
  <g \n \
     transform=\"matrix(0.6667,0,0,0.6667,7.4928819,258.48628)\" \n \
     id=\"g107\"> \n \
    <path \n \
       d=\"M 70,6 L 86.5,6 L 86.5,12 L 82.5,12 L 82.5,9 L 72,9\" \n \
       id=\"path109\" \n \
       style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.5;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 70,33.5 L 86.5,33.5 L 86.5,27.5 L 82.5,27.5 L 82.5,30.5 L 72,30.5\" \n \
       id=\"path111\" \n \
       style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.5;stroke-opacity:1\" /> \n \
  </g> \n \
  <path \n \
     d=\"M 39.494482,253.31936 C 50.161682,253.31936 50.161682,253.31936 50.161682,253.31936 L 53.828532,255.98616 L 56.161982,259.98636 L 56.161982,282.65416 L 53.828532,286.65436 L 50.161682,289.32116 L 38.827782,289.32116 L 38.827782,289.32116 L 38.827782,291.98796 L 25.493782,291.98796 L 25.493782,289.32116 L 14.159882,289.32116 L 10.493032,286.65436 L 8.1595819,282.65416 L 8.1595819,259.98636 L 10.493032,255.98616 L 14.159882,253.31936 L 24.827082,253.31936 L 24.827082,256.65286 L 39.494482,256.65286 L 39.494482,253.31936 z\" \n \
     id=\"path113\" \n \
     style=\"fill:url(#linearGradient3317);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n "

    data11a = \
"  <text \n \
     y=\"26\" \n \
     id=\"text115\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"277\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:10.5px\">"

    data11b = \
"  <text \n \
     y=\"26\" \n \
     id=\"text115\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"271\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:10.5px\">"

    data11c = \
"  <text \n \
     y=\"26\" \n \
     id=\"text115\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"267\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:10px\">"

    data12b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text119\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"283\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:10.5px\">"

    data12c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text119\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"276\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:10px\">"

    data13c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text119\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"285\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:10px\">"

    data14 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 70.522547,265.98666 L 73.856047,265.98666 L 73.856047,268.65346 L 78.522947,268.65346 L 78.522947,265.98666 L 139.526,265.98666 L 139.526,279.32066 L 78.522947,279.32066 L 78.522947,276.65386 L 73.856047,276.65386 L 73.856047,279.32066 L 70.522547,279.32066 L 70.522547,265.98666 z\" \n \
     id=\"path123\" \n \
     style=\"fill:url(#linearGradient3325);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"26\" \n \
     id=\"text125\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"106\" \n \
       y=\"276\" \n \
       id=\"tspan127\" \n \
       style=\"font-size:10.5px\">"

    data15 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 99.4375,303.72014 L 107.6875,303.72014 L 107.6875,306.72014 L 105.6875,306.72014 L 105.6875,305.22014 L 100.4375,305.22014\" \n \
     id=\"path2493\" \n \
     style=\"fill:#e0e000;fill-opacity:1;stroke:#a08000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 99.4375,317.47014 L 107.6875,317.47014 L 107.6875,314.47014 L 105.6875,314.47014 L 105.6875,315.97014 L 100.4375,315.97014\" \n \
     id=\"path2495\" \n \
     style=\"fill:#e0e000;fill-opacity:1;stroke:#908000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.0625,301.09514 C 83.0625,301.09514 97.0625,301.09514 97.0625,301.09514 C 97.0625,301.09514 99.1284,302.33842 99.8125,303.09514 C 100.51123,303.86805 101.5625,306.09514 101.5625,306.09514 L 101.5625,315.59514 C 101.5625,315.59514 100.45397,317.44197 99.8125,318.09514 C 99.09772,318.82295 97.0625,320.09514 97.0625,320.09514 L 74.5625,320.09514 L 74.5625,320.09514 L 74.5625,322.09514 L 64.5625,322.09514 L 64.5625,320.09514 L 42.0625,320.09514 C 42.0625,320.09514 40.02728,318.82295 39.3125,318.09514 C 38.671025,317.44197 37.5625,315.59514 37.5625,315.59514 L 37.5625,306.09514 C 37.5625,306.09514 38.613764,303.86805 39.3125,303.09514 C 39.996601,302.33842 42.0625,301.09514 42.0625,301.09514 L 64.0625,301.09514 L 64.0625,303.59514 L 75.0625,303.59514 L 75.0625,301.09514 z\" \n \
     id=\"path3067\" \n \
     style=\"fill:url(#linearGradient3333);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <g \n \
     transform=\"matrix(0.6667,0,0,0.6667,8.135112,390.2883)\" \n \
     id=\"g159\" \n \
     style=\"fill:#f0e000;fill-opacity:1\"> \n \
    <path \n \
       d=\"M 70,6 L 86.5,6 L 86.5,12 L 82.5,12 L 82.5,9 L 72,9\" \n \
       id=\"path161\" \n \
       style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.5;stroke-opacity:1\" /> \n \
    <path \n \
       d=\"M 70,33.5 L 86.5,33.5 L 86.5,27.5 L 82.5,27.5 L 82.5,30.5 L 72,30.5\" \n \
       id=\"path163\" \n \
       style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.5;stroke-opacity:1\" /> \n \
  </g> \n \
  <path \n \
     d=\"M 40.077007,390.16934 C 50.744207,390.16934 50.744207,390.16934 50.744207,390.16934 C 50.744207,390.16934 53.498877,391.82712 54.411057,392.83614 C 55.342757,393.86674 56.744507,396.83634 56.744507,396.83634 L 56.744507,409.50364 C 56.744507,409.50364 55.266407,411.9662 54.411057,412.83714 C 53.457977,413.80761 50.744207,415.50394 50.744207,415.50394 L 39.410307,415.50394 L 39.410307,415.50394 L 39.410307,418.17074 L 26.07631,418.17074 L 26.07631,415.50394 L 14.74241,415.50394 C 14.74241,415.50394 12.028648,413.80761 11.07556,412.83714 C 10.220217,411.9662 8.74211,409.50364 8.74211,409.50364 L 8.74211,396.83634 C 8.74211,396.83634 10.143866,393.86674 11.07556,392.83614 C 11.98774,391.82712 14.74241,390.16934 14.74241,390.16934 L 25.40961,390.16934 L 25.40961,393.50284 L 40.077007,393.50284 L 40.077007,390.16934 z\" \n \
     id=\"path165\" \n \
     style=\"fill:url(#linearGradient3374);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"-1.571244\" \n \
     y=\"4.74717\" \n \
     id=\"text167\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32.428757\" \n \
       y=\"405.74716\" \n \
       id=\"tspan169\" \n \
       style=\"font-size:10.5px;fill:#000000;fill-opacity:1\">"

    data16 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 70.522547,397.50304 L 73.856047,397.50304 L 73.856047,400.16984 L 78.522947,400.16984 L 78.522947,397.50304 L 139.526,397.50304 L 139.526,410.83704 L 78.522947,410.83704 L 78.522947,408.17024 L 73.856047,408.17024 L 73.856047,410.83704 L 70.522547,410.83704 L 70.522547,397.50304 z\" \n \
     id=\"path173\" \n \
     style=\"fill:url(#linearGradient3396);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"5.2105079\" \n \
     y=\"8\" \n \
     id=\"text175\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"105.21051\" \n \
       y=\"407\" \n \
       id=\"tspan177\" \n \
       style=\"font-size:10.5px;fill:#000000;fill-opacity:1\">"

    data17 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 40.07701,424.99768 C 50.74421,424.99768 50.74421,424.99768 50.74421,424.99768 L 54.41106,427.66448 L 56.74451,431.66468 L 56.74451,454.33248 L 54.41106,458.33268 L 50.74421,460.99948 L 39.41031,460.99948 L 39.41031,460.99948 L 39.41031,463.66628 L 26.07631,463.66628 L 26.07631,460.99948 L 14.74241,460.99948 L 11.07556,458.33268 L 8.74211,454.33248 L 8.74211,431.66468 L 11.07556,427.66448 L 14.74241,424.99768 L 25.40961,424.99768 L 25.40961,428.33118 L 40.07701,428.33118 L 40.07701,424.99768 z\" \n \
     id=\"path179\" \n \
     style=\"fill:url(#linearGradient3404);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <g \n \
     transform=\"translate(-0.5838651,1.9663391)\" \n \
     id=\"g181\"> \n \
    <text \n \
       id=\"text183\" \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"33\" \n \
         y=\"441\" \n \
         id=\"tspan185\" \n \
         style=\"font-size:10.5px\">"

    data18 = \
"</tspan> \n \
    </text> \n \
    <text \n \
       id=\"text187\" \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"33\" \n \
         y=\"453\" \n \
         id=\"tspan189\" \n \
         style=\"font-size:10.5px\">"

    data19 = \
"</tspan> \n \
    </text> \n \
  </g> \n \
  <path \n \
     d=\"M 113.81429,424.99768 C 124.48149,424.99768 124.48149,424.99768 124.48149,424.99768 L 128.14834,427.66448 L 130.48179,431.66468 L 130.48179,454.33248 L 128.14834,458.33268 L 124.48149,460.99948 L 113.14759,460.99948 L 113.14759,460.99948 L 113.14759,463.66628 L 99.813592,463.66628 L 99.813592,460.99948 L 88.479683,460.99948 L 84.812833,458.33268 L 82.479383,454.33248 L 82.479383,431.66468 L 84.812833,427.66448 L 88.479683,424.99768 L 99.146892,424.99768 L 99.146892,428.33118 L 113.81429,428.33118 L 113.81429,424.99768 z\" \n \
     id=\"path191\" \n \
     style=\"fill:url(#linearGradient3412);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <g \n \
     transform=\"translate(1.1422305,0)\" \n \
     id=\"g193\"> \n \
    <text \n \
       id=\"text195\" \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"105\" \n \
         y=\"441\" \n \
         id=\"tspan197\" \n \
         style=\"font-size:10.5px\">"

    data20 = \
"</tspan> \n \
    </text> \n \
    <text \n \
       id=\"text199\" \n \
       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
         x=\"105\" \n \
         y=\"453\" \n \
         id=\"tspan201\" \n \
         style=\"font-size:10.5px\">"

    data21 = \
"</tspan> \n \
    </text> \n \
  </g> \n \
  <path \n \
     d=\"M 43.524995,306.8 L 46.024995,306.8 L 46.024995,308.8 L 49.524995,308.8 L 49.524995,306.8 L 95.275005,306.8 L 95.275005,316.8 L 49.524995,316.8 L 49.524995,314.8 L 46.024995,314.8 L 46.024995,316.8 L 43.524995,316.8 L 43.524995,306.8 z\" \n \
     id=\"path3478\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 46.749995,175 L 49.249995,175 L 49.249995,177 L 52.749995,177 L 52.749995,175 L 98.5,175 L 98.5,185 L 52.749995,185 L 52.749995,183 L 49.249995,183 L 49.249995,185 L 46.749995,185 L 46.749995,175 z\" \n \
     id=\"path3491\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 46.124998,140.375 L 48.624998,140.375 L 48.624998,142.375 L 52.124998,142.375 L 52.124998,140.375 L 97.875,140.375 L 97.875,150.375 L 52.124998,150.375 L 52.124998,148.375 L 48.624998,148.375 L 48.624998,150.375 L 46.124998,150.375 L 46.124998,140.375 z\" \n \
     id=\"path3499\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 37.995002,361.21701 L 41.345002,361.21701 L 41.345002,363.89701 L 46.035002,363.89701 L 46.035002,361.21701 L 107.34001,361.21701 L 107.34001,374.61701 L 46.035002,374.61701 L 46.035002,371.93701 L 41.345002,371.93701 L 41.345002,374.61701 L 37.995002,374.61701 L 37.995002,361.21701 z\" \n \
     id=\"path2709\" \n \
     style=\"fill:url(#linearGradient3349);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"-0.0188425\" \n \
     y=\"8\" \n \
     id=\"text153\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.481155\" \n \
       y=\"372\" \n \
       id=\"tspan155\" \n \
       style=\"font-size:10.5px\">"

    data22 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 42.749422,333.875 L 42.749422,338.375 L 39.374422,338.375 L 39.374422,336.375 L 36.749422,336.375 L 36.749422,346.375 L 39.374422,346.375 L 39.374422,344.375 L 42.749422,344.375 L 42.749422,349 L 99.874422,348.875 L 99.874422,333.875 L 42.749422,333.875 z\" \n \
     id=\"path2718\" \n \
     style=\"fill:url(#linearGradient3341);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 45.874422,336.375 L 48.374422,336.375 L 48.374422,338.375 L 51.874422,338.375 L 51.874422,336.375 L 97.624427,336.375 L 97.624427,346.375 L 51.874422,346.375 L 51.874422,344.375 L 48.374422,344.375 L 48.374422,346.375 L 45.874422,346.375 L 45.874422,336.375 z\" \n \
     id=\"path2720\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 97,45.558706 C 97.09921,52.349516 77.5,58.058706 77.5,58.058706 L 77.5,58.058706 L 77.5,60.058706 L 67.5,60.058706 L 67.5,58.058706 C 67.5,58.058706 47.90079,52.349516 48,45.558706 C 48.12259,37.167636 64.10804,33.058706 72.5,33.058706 C 80.89196,33.058706 96.87741,37.167636 97,45.558706 z\" \n \
     id=\"path2715\" \n \
     style=\"fill:url(#linearGradient3245);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text87\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"49\" \n \
       id=\"tspan89\" \n \
       style=\"font-size:10.5px\">"

    data23 = \
"</tspan> \n \
  </text> \n \
</svg> \n"

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname+".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring1).encode("utf-8"))
    FILE.write(data1)
    FILE.write(_(mystring2).encode("utf-8"))
    FILE.write(data2)
    FILE.write(_(mystring2).encode("utf-8"))
    FILE.write(data3)
    FILE.write(_(mystring3).encode("utf-8"))
    FILE.write(data4)
    FILE.write(_(mystring3).encode("utf-8"))
    FILE.write(data5)
    strings = _(mystring4).split(" ",3)
    if len(strings) == 1:
        FILE.write(data6a)
        FILE.write(strings[0].encode("utf-8"))
    elif len(strings) == 2:
        FILE.write(data6b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data7b)
        FILE.write(strings[1].encode("utf-8"))
    else:
        FILE.write(data6c)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data7c)
        FILE.write(strings[1].encode("utf-8"))
        FILE.write(data8c)
        FILE.write(strings[2].encode("utf-8"))
        if len(strings) == 4:
            FILE.write(" " + strings[3].encode("utf-8"))
    FILE.write(data9)
    FILE.write(_(mystring5).encode("utf-8"))
    FILE.write(data10)
    strings = _(mystring6).split(" ",3)
    if len(strings) == 1:
        FILE.write(data11a)
        FILE.write(strings[0].encode("utf-8"))
    elif len(strings) == 2:
        FILE.write(data11b)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data12b)
        FILE.write(strings[1].encode("utf-8"))
    else:
        FILE.write(data11c)
        FILE.write(strings[0].encode("utf-8"))
        FILE.write(data12c)
        FILE.write(strings[1].encode("utf-8"))
        FILE.write(data13c)
        FILE.write(strings[2].encode("utf-8"))
        if len(strings) == 4:
            FILE.write(" " + strings[3].encode("utf-8"))
    FILE.write(data14)
    FILE.write(_(mystring7).encode("utf-8"))
    FILE.write(data15)
    FILE.write(_(mystring8).encode("utf-8"))
    FILE.write(data16)
    FILE.write(_(mystring9).encode("utf-8"))
    FILE.write(data17)
    strings = _(mystring10).split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data18)
    if len(strings) == 2:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data19)
    strings = _(mystring11).split(" ",2)
    FILE.write(strings[0].encode("utf-8"))
    FILE.write(data20)
    if len(strings) == 2:
        FILE.write(strings[1].encode("utf-8"))
    FILE.write(data21)
    FILE.write(_(mystring12).encode("utf-8"))
    FILE.write(data22)
    FILE.write(_(mystring13).encode("utf-8"))
    FILE.write(data23)
    FILE.close()
    return

if __name__ == "__main__":
    main()
