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
    mystring8 = "name"
    mystring9 = "start"
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
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,4.441294)\" /> \n \
    <linearGradient \n \
       x1=\"3.8948069\" \n \
       y1=\"74.402542\" \n \
       x2=\"70.231407\" \n \
       y2=\"74.402542\" \n \
       id=\"linearGradient3253\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,17.83573)\" /> \n \
    <linearGradient \n \
       x1=\"81.979385\" \n \
       y1=\"74.402542\" \n \
       x2=\"130.98178\" \n \
       y2=\"74.402542\" \n \
       id=\"linearGradient3261\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,17.83573)\" /> \n \
    <linearGradient \n \
       x1=\"3.8948069\" \n \
       y1=\"115.66337\" \n \
       x2=\"70.231407\" \n \
       y2=\"115.66337\" \n \
       id=\"linearGradient3269\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,17.83573)\" /> \n \
    <linearGradient \n \
       x1=\"81.979385\" \n \
       y1=\"115.66337\" \n \
       x2=\"130.98178\" \n \
       y2=\"115.66337\" \n \
       id=\"linearGradient3277\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,17.83573)\" /> \n \
    <linearGradient \n \
       x1=\"35.25\" \n \
       y1=\"145.67612\" \n \
       x2=\"109.75\" \n \
       y2=\"145.67612\" \n \
       id=\"linearGradient3285\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,41.9838)\" /> \n \
    <linearGradient \n \
       x1=\"40\" \n \
       y1=\"180.0162\" \n \
       x2=\"105\" \n \
       y2=\"180.0162\" \n \
       id=\"linearGradient3293\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,41.9838)\" /> \n \
    <linearGradient \n \
       x1=\"7.6595821\" \n \
       y1=\"226.22649\" \n \
       x2=\"56.661983\" \n \
       y2=\"226.22649\" \n \
       id=\"linearGradient3301\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
    <linearGradient \n \
       x1=\"70.022545\" \n \
       y1=\"226.22649\" \n \
       x2=\"140.026\" \n \
       y2=\"226.22649\" \n \
       id=\"linearGradient3309\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
    <linearGradient \n \
       x1=\"7.6595821\" \n \
       y1=\"272.65366\" \n \
       x2=\"56.661983\" \n \
       y2=\"272.65366\" \n \
       id=\"linearGradient3317\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
    <linearGradient \n \
       x1=\"70.022545\" \n \
       y1=\"272.65366\" \n \
       x2=\"140.026\" \n \
       y2=\"272.65366\" \n \
       id=\"linearGradient3325\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
    <linearGradient \n \
       x1=\"37.0625\" \n \
       y1=\"311.59515\" \n \
       x2=\"102.0625\" \n \
       y2=\"311.59515\" \n \
       id=\"linearGradient3333\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
    <linearGradient \n \
       x1=\"36.24942\" \n \
       y1=\"341.4375\" \n \
       x2=\"100.37442\" \n \
       y2=\"341.4375\" \n \
       id=\"linearGradient3341\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
    <linearGradient \n \
       x1=\"37.495003\" \n \
       y1=\"367.91702\" \n \
       x2=\"107.84001\" \n \
       y2=\"367.91702\" \n \
       id=\"linearGradient3349\" \n \
       xlink:href=\"#linearGradient3239\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,64.88299)\" /> \n \
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
     y=\"249.35913\" \n \
     id=\"rect25\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.5\" \n \
     height=\"0.14\" \n \
     x=\"10.691486\" \n \
     y=\"250.49942\" \n \
     id=\"rect27\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.5\" \n \
     height=\"0.14\" \n \
     x=\"10.691486\" \n \
     y=\"251.49832\" \n \
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
     y=\"-468.77127\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect35\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7153397\" \n \
     y=\"-467.43195\" \n \
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
     style=\"font-size:12px;font-weight:bold;text-align:center;text-anchor:middle;fill:#ffffff;fill-opacity:1;stroke:none;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"490\" \n \
       style=\"font-size:12px\">X</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"21\" \n \
       id=\"tspan47\" \n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 69.731407,92.23827 L 69.731407,92.23827 L 43.730107,107.57237 L 43.730107,107.57237 L 43.730107,110.23917 L 30.396107,110.23917 L 30.396107,107.57237 C 30.396107,107.57237 4.3948068,92.23827 4.3948068,92.23827 C 4.3948068,92.23827 37.063107,74.23737 37.063107,74.23737 C 37.063107,74.23737 69.731407,92.23827 69.731407,92.23827 z\" \n \
     id=\"path49\" \n \
     style=\"fill:url(#linearGradient3253);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"96\" \n \
       id=\"tspan53\" \n \
       style=\"font-size:11px\">"

    data2 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 113.81428,78.23757 C 124.48148,78.23757 124.48148,78.23757 124.48148,78.23757 C 124.48148,78.23757 127.23615,79.895355 128.14833,80.90437 C 129.08003,81.934971 130.48178,84.90457 130.48178,84.90457 L 130.48178,97.57187 C 130.48178,97.57187 129.00368,100.03443 128.14833,100.90537 C 127.19525,101.87584 124.48148,103.57217 124.48148,103.57217 L 113.14758,103.57217 L 113.14758,103.57217 L 113.14758,106.23897 L 99.813583,106.23897 L 99.813583,103.57217 L 88.479683,103.57217 C 88.479683,103.57217 85.765921,101.87584 84.812833,100.90537 C 83.95749,100.03443 82.479383,97.57187 82.479383,97.57187 L 82.479383,84.90457 C 82.479383,84.90457 83.881139,81.934971 84.812833,80.90437 C 85.725013,79.895355 88.479683,78.23757 88.479683,78.23757 L 99.146883,78.23757 L 99.146883,81.57107 L 113.81428,81.57107 L 113.81428,78.23757 z\" \n \
     id=\"path55\" \n \
     style=\"fill:url(#linearGradient3261);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"107\" \n \
       y=\"94\" \n \
       id=\"tspan59\" \n \
       style=\"font-size:11px\">"

    data3 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 69.731407,133.4991 L 69.731407,133.4991 L 43.730107,148.8332 L 43.730107,148.8332 L 43.730107,151.5 L 30.396107,151.5 L 30.396107,148.8332 C 30.396107,148.8332 4.3948068,133.4991 4.3948068,133.4991 C 4.3948068,133.4991 37.063107,115.4982 37.063107,115.4982 C 37.063107,115.4982 69.731407,133.4991 69.731407,133.4991 z\" \n \
     id=\"path61\" \n \
     style=\"fill:url(#linearGradient3269);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"37\" \n \
       y=\"137\" \n \
       id=\"tspan65\" \n \
       style=\"font-size:11px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 113.81428,119.4984 C 124.48148,119.4984 124.48148,119.4984 124.48148,119.4984 C 124.48148,119.4984 127.23615,121.15619 128.14833,122.1652 C 129.08003,123.1958 130.48178,126.1654 130.48178,126.1654 L 130.48178,138.8327 C 130.48178,138.8327 129.00368,141.29526 128.14833,142.1662 C 127.19525,143.13667 124.48148,144.833 124.48148,144.833 L 113.14758,144.833 L 113.14758,144.833 L 113.14758,147.4998 L 99.813583,147.4998 L 99.813583,144.833 L 88.479683,144.833 C 88.479683,144.833 85.765921,143.13667 84.812833,142.1662 C 83.95749,141.29526 82.479383,138.8327 82.479383,138.8327 L 82.479383,126.1654 C 82.479383,126.1654 83.881139,123.1958 84.812833,122.1652 C 85.725013,121.15619 88.479683,119.4984 88.479683,119.4984 L 99.146883,119.4984 L 99.146883,122.8319 L 113.81428,122.8319 L 113.81428,119.4984 z\" \n \
     id=\"path67\" \n \
     style=\"fill:url(#linearGradient3277);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"107\" \n \
       y=\"137\" \n \
       id=\"tspan71\" \n \
       style=\"font-size:11px\">"

    data5 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 72.25,169.40992 L 35.75,187.65992 L 67.25,203.90992 L 67.25,205.90992 L 77.25,205.90992 L 77.25,203.90992 L 109.25,187.65992 L 72.25,169.40992 z\" \n \
     id=\"path6722\" \n \
     style=\"fill:url(#linearGradient3285);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 78,211.5 C 86,211.5 100,211.5 100,211.5 C 100,211.5 102.0659,212.74328 102.75,213.5 C 103.44873,214.27291 104.5,216.5 104.5,216.5 L 104.5,226 C 104.5,226 103.39147,227.84683 102.75,228.5 C 102.03522,229.22781 100,230.5 100,230.5 L 77.5,230.5 L 77.5,230.5 L 77.5,232.5 L 67.5,232.5 L 67.5,230.5 L 45,230.5 C 45,230.5 42.96478,229.22781 42.25,228.5 C 41.608525,227.84683 40.5,226 40.5,226 L 40.5,216.5 C 40.5,216.5 41.551264,214.27291 42.25,213.5 C 42.934101,212.74328 45,211.5 45,211.5 L 67,211.5 L 67,214 L 78,214 L 78,211.5 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient3293);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.161882,280.9423 L 65.162432,280.9423 L 65.162432,284.9425 L 62.495632,284.9425 L 62.495632,282.9424 L 55.495282,282.9424\" \n \
     id=\"path87\" \n \
     style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.161882,299.27655 L 65.162432,299.27655 L 65.162432,295.27635 L 62.495632,295.27635 L 62.495632,297.27645 L 55.495282,297.27645\" \n \
     id=\"path89\" \n \
     style=\"fill:#f0e000;fill-opacity:1;stroke:#a08000;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 39.494482,271.77517 C 50.161682,271.77517 50.161682,271.77517 50.161682,271.77517 L 53.828532,274.44197 L 56.161982,278.44217 L 56.161982,301.10997 L 53.828532,305.11017 L 50.161682,307.77697 L 38.827782,307.77697 L 38.827782,307.77697 L 38.827782,310.44377 L 25.493782,310.44377 L 25.493782,307.77697 L 14.159882,307.77697 L 10.493032,305.11017 L 8.1595819,301.10997 L 8.1595819,278.44217 L 10.493032,274.44197 L 14.159882,271.77517 L 24.827082,271.77517 L 24.827082,275.10867 L 39.494482,275.10867 L 39.494482,271.77517 z\" \n \
     id=\"path91\" \n \
     style=\"fill:url(#linearGradient3301);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n"

    data6a = \
"  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"294\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:11px\">"

    data6b = \
"  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"288\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:10.5px\">"

    data6c = \
"  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"284\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:10px\">"

    data7b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"300\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:10.5px\">"

    data7c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"294\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:10px\">"

    data8c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"304\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:10px\">"

    data9 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 70.522547,284.44247 L 73.856047,284.44247 L 73.856047,287.10927 L 78.522947,287.10927 L 78.522947,284.44247 L 139.526,284.44247 L 139.526,297.77647 L 78.522947,297.77647 L 78.522947,295.10967 L 73.856047,295.10967 L 73.856047,297.77647 L 70.522547,297.77647 L 70.522547,284.44247 z\" \n \
     id=\"path101\" \n \
     style=\"fill:url(#linearGradient3309);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"106\" \n \
       y=\"294\" \n \
       id=\"tspan105\" \n \
       style=\"font-size:11px\">"

    data10 = \
"</tspan> \n \
  </text> \n \
  <g \n \
     transform=\"matrix(0.6667,0,0,0.6667,7.4928819,323.36927)\" \n \
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
     d=\"M 39.494482,318.20235 C 50.161682,318.20235 50.161682,318.20235 50.161682,318.20235 L 53.828532,320.86915 L 56.161982,324.86935 L 56.161982,347.53715 L 53.828532,351.53735 L 50.161682,354.20415 L 38.827782,354.20415 L 38.827782,354.20415 L 38.827782,356.87095 L 25.493782,356.87095 L 25.493782,354.20415 L 14.159882,354.20415 L 10.493032,351.53735 L 8.1595819,347.53715 L 8.1595819,324.86935 L 10.493032,320.86915 L 14.159882,318.20235 L 24.827082,318.20235 L 24.827082,321.53585 L 39.494482,321.53585 L 39.494482,318.20235 z\" \n \
     id=\"path113\" \n \
     style=\"fill:url(#linearGradient3317);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n"

    data11a = \
"  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"341\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:11px\">"

    data11b = \
"  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"335\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:10.5px\">"

    data11c = \
"  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"330\" \n \
       id=\"tspan117\" \n \
       style=\"font-size:10px\">"

    data12b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"347\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:10.5px\">"

    data12c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"340\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:10px\">"

    data13c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"350\" \n \
       id=\"tspan121\" \n \
       style=\"font-size:10px\">"

    data14 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 70.522547,330.86965 L 73.856047,330.86965 L 73.856047,333.53645 L 78.522947,333.53645 L 78.522947,330.86965 L 139.526,330.86965 L 139.526,344.20365 L 78.522947,344.20365 L 78.522947,341.53685 L 73.856047,341.53685 L 73.856047,344.20365 L 70.522547,344.20365 L 70.522547,330.86965 z\" \n \
     id=\"path123\" \n \
     style=\"fill:url(#linearGradient3325);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"106\" \n \
       y=\"341\" \n \
       id=\"tspan127\" \n \
       style=\"font-size:11px\">"

    data15 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 99.4375,368.60313 L 107.6875,368.60313 L 107.6875,371.60313 L 105.6875,371.60313 L 105.6875,370.10313 L 100.4375,370.10313\" \n \
     id=\"path2493\" \n \
     style=\"fill:#e0e000;fill-opacity:1;stroke:#a08000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 99.4375,382.35313 L 107.6875,382.35313 L 107.6875,379.35313 L 105.6875,379.35313 L 105.6875,380.85313 L 100.4375,380.85313\" \n \
     id=\"path2495\" \n \
     style=\"fill:#e0e000;fill-opacity:1;stroke:#908000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.0625,365.97813 C 83.0625,365.97813 97.0625,365.97813 97.0625,365.97813 C 97.0625,365.97813 99.1284,367.22141 99.8125,367.97813 C 100.51123,368.75104 101.5625,370.97813 101.5625,370.97813 L 101.5625,380.47813 C 101.5625,380.47813 100.45397,382.32496 99.8125,382.97813 C 99.09772,383.70594 97.0625,384.97813 97.0625,384.97813 L 74.5625,384.97813 L 74.5625,384.97813 L 74.5625,386.97813 L 64.5625,386.97813 L 64.5625,384.97813 L 42.0625,384.97813 C 42.0625,384.97813 40.02728,383.70594 39.3125,382.97813 C 38.671025,382.32496 37.5625,380.47813 37.5625,380.47813 L 37.5625,370.97813 C 37.5625,370.97813 38.613764,368.75104 39.3125,367.97813 C 39.996601,367.22141 42.0625,365.97813 42.0625,365.97813 L 64.0625,365.97813 L 64.0625,368.47813 L 75.0625,368.47813 L 75.0625,365.97813 z\" \n \
     id=\"path3067\" \n \
     style=\"fill:url(#linearGradient3333);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 43.524995,371.68299 L 46.024995,371.68299 L 46.024995,373.68299 L 49.524995,373.68299 L 49.524995,371.68299 L 95.275005,371.68299 L 95.275005,381.68299 L 49.524995,381.68299 L 49.524995,379.68299 L 46.024995,379.68299 L 46.024995,381.68299 L 43.524995,381.68299 L 43.524995,371.68299 z\" \n \
     id=\"path3478\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 46.749995,216.9838 L 49.249995,216.9838 L 49.249995,218.9838 L 52.749995,218.9838 L 52.749995,216.9838 L 98.5,216.9838 L 98.5,226.9838 L 52.749995,226.9838 L 52.749995,224.9838 L 49.249995,224.9838 L 49.249995,226.9838 L 46.749995,226.9838 L 46.749995,216.9838 z\" \n \
     id=\"path3491\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 46.124998,182.3588 L 48.624998,182.3588 L 48.624998,184.3588 L 52.124998,184.3588 L 52.124998,182.3588 L 97.875,182.3588 L 97.875,192.3588 L 52.124998,192.3588 L 52.124998,190.3588 L 48.624998,190.3588 L 48.624998,192.3588 L 46.124998,192.3588 L 46.124998,182.3588 z\" \n \
     id=\"path3499\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 37.995002,426.1 L 41.345002,426.1 L 41.345002,428.78 L 46.035002,428.78 L 46.035002,426.1 L 107.34001,426.1 L 107.34001,439.5 L 46.035002,439.5 L 46.035002,436.82 L 41.345002,436.82 L 41.345002,439.5 L 37.995002,439.5 L 37.995002,426.1 z\" \n \
     id=\"path2709\" \n \
     style=\"fill:url(#linearGradient3349);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"437\" \n \
       id=\"tspan155\" \n \
       style=\"font-size:11px\">"

    data16 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 42.749422,398.75799 L 42.749422,403.25799 L 39.374422,403.25799 L 39.374422,401.25799 L 36.749422,401.25799 L 36.749422,411.25799 L 39.374422,411.25799 L 39.374422,409.25799 L 42.749422,409.25799 L 42.749422,413.88299 L 99.874422,413.75799 L 99.874422,398.75799 L 42.749422,398.75799 z\" \n \
     id=\"path2718\" \n \
     style=\"fill:url(#linearGradient3341);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 45.874422,401.25799 L 48.374422,401.25799 L 48.374422,403.25799 L 51.874422,403.25799 L 51.874422,401.25799 L 97.624427,401.25799 L 97.624427,411.25799 L 51.874422,411.25799 L 51.874422,409.25799 L 48.374422,409.25799 L 48.374422,411.25799 L 45.874422,411.25799 L 45.874422,401.25799 z\" \n \
     id=\"path2720\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 97,50 C 97.09921,56.79081 77.5,62.5 77.5,62.5 L 77.5,62.5 L 77.5,64.5 L 67.5,64.5 L 67.5,62.5 C 67.5,62.5 47.90079,56.79081 48,50 C 48.12259,41.60893 64.10804,37.5 72.5,37.5 C 80.89196,37.5 96.87741,41.60893 97,50 z\" \n \
     id=\"path2715\" \n \
     style=\"fill:url(#linearGradient3245);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"53.5\" \n \
       id=\"tspan89\" \n \
       style=\"font-size:11px\">"

    data17 = \
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
    FILE.close()
    return

if __name__ == "__main__":
    main()


