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

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<!-- Created with Inkscape (http://www.inkscape.org/) --> \n \
<svg \n \
   xmlns:svg=\"http://www.w3.org/2000/svg\" \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   version=\"1.0\" \n \
   width=\"145\" \n \
   height=\"452\" \n \
   id=\"svg2\"> \n \
  <defs \n \
     id=\"defs103\"> \n \
    <linearGradient \n \
       id=\"linearGradient3250\"> \n \
      <stop \n \
         id=\"stop3252\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3254\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3256\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3258\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3260\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3264\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.66667,0,0,0.66667,47.83321,34.333281)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3267\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.66667,0,0,0.66667,47.83321,34.333281)\" /> \n \
    <linearGradient \n \
       x1=\"7.4165211\" \n \
       y1=\"90.000023\" \n \
       x2=\"56.750099\" \n \
       y2=\"90.000023\" \n \
       id=\"linearGradient3333\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"7.4165211\" \n \
       y1=\"130.66669\" \n \
       x2=\"56.750099\" \n \
       y2=\"130.66669\" \n \
       id=\"linearGradient3341\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.416519\" \n \
       y1=\"90.000023\" \n \
       x2=\"128.75011\" \n \
       y2=\"90.000023\" \n \
       id=\"linearGradient3349\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.416519\" \n \
       y1=\"130.66669\" \n \
       x2=\"128.75011\" \n \
       y2=\"130.66669\" \n \
       id=\"linearGradient3357\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"43.416519\" \n \
       y1=\"181.66669\" \n \
       x2=\"92.750099\" \n \
       y2=\"181.66669\" \n \
       id=\"linearGradient3365\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"7.4165211\" \n \
       y1=\"251.00002\" \n \
       x2=\"56.750099\" \n \
       y2=\"251.00002\" \n \
       id=\"linearGradient3373\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"79.416519\" \n \
       y1=\"238.66663\" \n \
       x2=\"128.75011\" \n \
       y2=\"238.66663\" \n \
       id=\"linearGradient3381\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"6.5625\" \n \
       y1=\"303.5\" \n \
       x2=\"72.5625\" \n \
       y2=\"303.5\" \n \
       id=\"linearGradient3389\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"89.083481\" \n \
       y1=\"314.81985\" \n \
       x2=\"137.58348\" \n \
       y2=\"314.81985\" \n \
       id=\"linearGradient3397\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"37.333157\" \n \
       y1=\"359.00003\" \n \
       x2=\"107.66684\" \n \
       y2=\"359.00003\" \n \
       id=\"linearGradient3405\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"37.333157\" \n \
       y1=\"382.66669\" \n \
       x2=\"107.66684\" \n \
       y2=\"382.66669\" \n \
       id=\"linearGradient3413\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"37.333157\" \n \
       y1=\"406.33334\" \n \
       x2=\"107.66684\" \n \
       y2=\"406.33334\" \n \
       id=\"linearGradient3421\" \n \
       xlink:href=\"#linearGradient3250\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 0.5594301,0.5199639 L 0.49711997,438.41023 L 3.6209793,445.14297 L 8.494839,449.1072 L 15.156388,451.50288 L 128.9813,451.50288 L 135.82978,448.93866 L 141.77903,444.04729 L 144.50288,435.79171 L 144.54057,0.4971203 L 0.5594301,0.5199639 z\" \n \
     id=\"path30\" \n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"215.19794\" \n \
     id=\"rect32\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"216.31435\" \n \
     id=\"rect34\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"217.29239\" \n \
     id=\"rect36\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"67.382996\" \n \
     id=\"rect38\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"68.499405\" \n \
     id=\"rect40\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"69.477448\" \n \
     id=\"rect42\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-28.931932\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect50\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-27.815523\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect52\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-424.77127\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect54\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"-423.43195\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect56\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 12,428.5 C 12,429.32843 11.328427,430 10.5,430 C 9.6715729,430 9,429.32843 9,428.5 C 9,427.67157 9.6715729,427 10.5,427 C 11.328427,427 12,427.67157 12,428.5 z\" \n \
     transform=\"translate(122.16407,15.40625)\" \n \
     id=\"path58\" \n \
     style=\"fill:#fff080;fill-opacity:1;stroke:none;stroke-width:1;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 79.5,438.375 C 79.5,442.86231 75.750385,446.5 71.125,446.5 C 66.499615,446.5 62.75,442.86231 62.75,438.375 C 62.75,433.88769 66.499615,430.25 71.125,430.25 C 75.750385,430.25 79.5,433.88769 79.5,438.375 L 79.5,438.375 z\" \n \
     transform=\"translate(1.375,-0.749023)\" \n \
     id=\"path60\" \n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text42\" \n \
     style=\"font-size:12px;font-weight:bold;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"442\" \n \
       id=\"tspan44\" \n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\">X</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 79.83337,34.999951 C 90.50009,34.999951 90.50009,34.999951 90.50009,34.999951 L 94.166775,37.666631 L 96.50012,41.666651 L 96.50012,54.333381 L 94.166775,57.666731 L 90.50009,60.333411 L 79.1667,60.333411 L 79.1667,60.333411 L 79.1667,63.000091 L 65.8333,63.000091 L 65.8333,60.333411 L 54.49991,60.333411 L 50.833225,57.666731 L 48.49988,54.333381 L 48.49988,41.666651 L 50.833225,37.666631 L 54.49991,34.999951 L 65.16663,34.999951 L 65.16663,38.333301 L 79.83337,38.333301 L 79.83337,34.999951 z\" \n \
     id=\"path48\" \n \
     style=\"fill:url(#linearGradient3267);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"51.5\" \n \
       id=\"tspan52\" \n \
       style=\"font-size:12px;fill:#000000;fill-opacity:1\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 54.083421,79.3333 L 65.083476,79.3333 L 65.083476,83.33332 L 62.416796,83.33332 L 62.416796,81.33331 L 55.416761,81.33331\" \n \
     id=\"path76\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.083421,97.666725 L 65.083476,97.666725 L 65.083476,93.666705 L 62.416796,93.666705 L 62.416796,95.666715 L 55.416761,95.666715\" \n \
     id=\"path78\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 39.416681,75.99995 C 50.083401,75.99995 50.083401,75.99995 50.083401,75.99995 L 53.750086,78.66663 L 56.083431,82.66665 L 56.083431,95.33338 L 53.750086,98.66673 L 50.083401,101.33341 L 38.750011,101.33341 L 38.750011,101.33341 L 38.750011,104.00009 L 25.416611,104.00009 L 25.416611,101.33341 L 14.083221,101.33341 L 10.416536,98.66673 L 8.083191,95.33338 L 8.083191,82.66665 L 10.416536,78.66663 L 14.083221,75.99995 L 24.749941,75.99995 L 24.749941,79.3333 L 39.416681,79.3333 L 39.416681,75.99995 z\" \n \
     id=\"path80\" \n \
     style=\"fill:url(#linearGradient3333);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"92.5\" \n \
       id=\"tspan84\" \n \
       style=\"font-size:12px\">"

    data2 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 126.08342,79.3333 L 137.08348,79.3333 L 137.08348,83.33332 L 134.4168,83.33332 L 134.4168,81.33331 L 127.41676,81.33331\" \n \
     id=\"path88\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 126.08342,97.666725 L 137.08348,97.666725 L 137.08348,93.666705 L 134.4168,93.666705 L 134.4168,95.666715 L 127.41676,95.666715\" \n \
     id=\"path90\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 111.41668,75.99995 C 122.0834,75.99995 122.0834,75.99995 122.0834,75.99995 L 125.75009,78.66663 L 128.08343,82.66665 L 128.08343,95.33338 L 125.75009,98.66673 L 122.0834,101.33341 L 110.75001,101.33341 L 110.75001,101.33341 L 110.75001,104.00009 L 97.416611,104.00009 L 97.416611,101.33341 L 86.083221,101.33341 L 82.416536,98.66673 L 80.083191,95.33338 L 80.083191,82.66665 L 82.416536,78.66663 L 86.083221,75.99995 L 96.749941,75.99995 L 96.749941,79.3333 L 111.41668,79.3333 L 111.41668,75.99995 z\" \n \
     id=\"path92\" \n \
     style=\"fill:url(#linearGradient3349);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"92.5\" \n \
       id=\"tspan96\" \n \
       style=\"font-size:12px\">"

    data3 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 54.083421,119.99997 L 65.083476,119.99997 L 65.083476,123.99999 L 62.416796,123.99999 L 62.416796,121.99998 L 55.416761,121.99998\" \n \
     id=\"path100\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.083421,138.33339 L 65.083476,138.33339 L 65.083476,134.33337 L 62.416796,134.33337 L 62.416796,136.33338 L 55.416761,136.33338\" \n \
     id=\"path102\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 39.416681,116.66662 C 50.083401,116.66662 50.083401,116.66662 50.083401,116.66662 L 53.750086,119.3333 L 56.083431,123.33332 L 56.083431,136.00005 L 53.750086,139.3334 L 50.083401,142.00008 L 38.750011,142.00008 L 38.750011,142.00008 L 38.750011,144.66676 L 25.416611,144.66676 L 25.416611,142.00008 L 14.083221,142.00008 L 10.416536,139.3334 L 8.083191,136.00005 L 8.083191,123.33332 L 10.416536,119.3333 L 14.083221,116.66662 L 24.749941,116.66662 L 24.749941,119.99997 L 39.416681,119.99997 L 39.416681,116.66662 z\" \n \
     id=\"path104\" \n \
     style=\"fill:url(#linearGradient3341);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"133\" \n \
       id=\"tspan108\" \n \
       style=\"font-size:12px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 126.08342,119.99997 L 137.08348,119.99997 L 137.08348,123.99999 L 134.4168,123.99999 L 134.4168,121.99998 L 127.41676,121.99998\" \n \
     id=\"path112\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 126.08342,138.33339 L 137.08348,138.33339 L 137.08348,134.33337 L 134.4168,134.33337 L 134.4168,136.33338 L 127.41676,136.33338\" \n \
     id=\"path114\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 111.41668,116.66662 C 122.0834,116.66662 122.0834,116.66662 122.0834,116.66662 L 125.75009,119.3333 L 128.08343,123.33332 L 128.08343,136.00005 L 125.75009,139.3334 L 122.0834,142.00008 L 110.75001,142.00008 L 110.75001,142.00008 L 110.75001,144.66676 L 97.416611,144.66676 L 97.416611,142.00008 L 86.083221,142.00008 L 82.416536,139.3334 L 80.083191,136.00005 L 80.083191,123.33332 L 82.416536,119.3333 L 86.083221,116.66662 L 96.749941,116.66662 L 96.749941,119.99997 L 111.41668,119.99997 L 111.41668,116.66662 z\" \n \
     id=\"path116\" \n \
     style=\"fill:url(#linearGradient3357);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"133\" \n \
       id=\"tspan120\" \n \
       style=\"font-size:12px\">"

    data5 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 89.916753,183.16669 L 100.91681,183.16669 L 100.91681,187.33338 L 98.250129,187.33338 L 98.250129,185.1667 L 91.250094,185.1667\" \n \
     id=\"path124\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 89.916753,201.50012 L 100.91681,201.50012 L 100.91681,197.5001 L 98.250129,197.5001 L 98.250129,199.50011 L 91.250094,199.50011\" \n \
     id=\"path126\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.083421,158.66657 L 101.08348,158.66657 L 101.08348,162.66659 L 98.416796,162.66659 L 98.416796,160.66658 L 91.416761,160.66658\" \n \
     id=\"path128\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.083421,177 L 101.08348,177 L 101.08348,172.99998 L 98.416796,172.99998 L 98.416796,174.99999 L 91.416761,174.99999\" \n \
     id=\"path130\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.416681,155.33322 C 86.083401,155.33322 86.083401,155.33322 86.083401,155.33322 L 89.750086,157.9999 L 92.083431,161.99992 L 92.083431,199.33344 L 89.750086,202.66679 L 86.083401,205.33347 L 74.750011,205.33347 L 74.750011,205.33347 L 74.750011,208.00015 L 61.416611,208.00015 L 61.416611,205.33347 L 50.083221,205.33347 L 46.416536,202.66679 L 44.083191,199.33344 L 44.083191,161.99992 L 46.416536,157.9999 L 50.083221,155.33322 L 60.749941,155.33322 L 60.749941,158.66657 L 75.416681,158.66657 L 75.416681,155.33322 z\" \n \
     id=\"path132\" \n \
     style=\"fill:url(#linearGradient3365);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"183\" \n \
       id=\"tspan136\" \n \
       style=\"font-size:12px\">"

    data6 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"90\" \n \
       y=\"169\" \n \
       id=\"tspan140\" \n \
       style=\"font-size:9px\">"

    data7 = \
"</tspan> \n \
    <tspan \n \
       x=\"90\" \n \
       y=\"198.5\" \n \
       id=\"tspan142\" \n \
       style=\"font-size:9px\">"

    data8 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 53.916753,252.50002 L 64.916809,252.50002 L 64.916809,256.66671 L 62.250129,256.66671 L 62.250129,254.50003 L 55.250093,254.50003\" \n \
     id=\"path146\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 53.916753,270.83345 L 64.916809,270.83345 L 64.916809,266.83343 L 62.250129,266.83343 L 62.250129,268.83344 L 55.250093,268.83344\" \n \
     id=\"path148\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.083421,227.9999 L 65.083476,227.9999 L 65.083476,231.99992 L 62.416796,231.99992 L 62.416796,229.99991 L 55.416761,229.99991\" \n \
     id=\"path150\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 54.083421,246.33333 L 65.083476,246.33333 L 65.083476,242.3333 L 62.416796,242.3333 L 62.416796,244.33331 L 55.416761,244.33331\" \n \
     id=\"path152\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 39.416681,224.66655 C 50.083401,224.66655 50.083401,224.66655 50.083401,224.66655 L 53.750086,227.33323 L 56.083431,231.33325 L 56.083431,268.66677 L 53.750086,272.00012 L 50.083401,274.6668 L 38.750011,274.6668 L 38.750011,274.6668 L 38.750011,277.33348 L 25.416611,277.33348 L 25.416611,274.6668 L 14.083221,274.6668 L 10.416536,272.00012 L 8.083191,268.66677 L 8.083191,231.33325 L 10.416536,227.33323 L 14.083221,224.66655 L 24.749941,224.66655 L 24.749941,227.9999 L 39.416681,227.9999 L 39.416681,224.66655 z\" \n \
     id=\"path154\" \n \
     style=\"fill:url(#linearGradient3373);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:12.00006008px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"32\" \n \
       y=\"252\" \n \
       id=\"tspan158\" \n \
       style=\"font-size:12px\">"

    data9 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:9.33337975px;text-align:end;text-anchor:end;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"54\" \n \
       y=\"238\" \n \
       id=\"tspan162\" \n \
       style=\"font-size:9px\">"

    data10 = \
"</tspan> \n \
    <tspan \n \
       x=\"54\" \n \
       y=\"268\" \n \
       id=\"tspan164\" \n \
       style=\"font-size:9px\">"

    data11 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 126.08342,227.9999 L 137.08348,227.9999 L 137.08348,231.99992 L 134.4168,231.99992 L 134.4168,229.99991 L 127.41676,229.99991\" \n \
     id=\"path168\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 126.08342,246.33333 L 137.08348,246.33333 L 137.08348,242.3333 L 134.4168,242.3333 L 134.4168,244.33331 L 127.41676,244.33331\" \n \
     id=\"path170\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.00000501;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 111.41668,224.66655 C 122.0834,224.66655 122.0834,224.66655 122.0834,224.66655 L 125.75009,227.33323 L 128.08343,231.33325 L 128.08343,243.99998 L 125.75009,247.33333 L 122.0834,250.00001 L 110.75001,250.00001 L 110.75001,250.00001 L 110.75001,252.66669 L 97.416611,252.66669 L 97.416611,250.00001 L 86.083221,250.00001 L 82.416536,247.33333 L 80.083191,243.99998 L 80.083191,231.33325 L 82.416536,227.33323 L 86.083221,224.66655 L 96.749941,224.66655 L 96.749941,227.9999 L 111.41668,227.9999 L 111.41668,224.66655 z\" \n \
     id=\"path172\" \n \
     style=\"fill:url(#linearGradient3381);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n"

    data12a = \
"  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"241\" \n \
       id=\"tspan176\" \n \
       style=\"font-size:12px\">"

    data12b = \
"  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"236\" \n \
       id=\"tspan176\" \n \
       style=\"font-size:10.5px\">"

    data13b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"104\" \n \
       y=\"247\" \n \
       id=\"tspan176\" \n \
       style=\"font-size:10.5px\">"

    data14 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.999828,352.33333 L 41.333178,352.33333 L 41.333178,355.00001 L 45.999868,355.00001 L 45.999868,352.33333 L 107.00017,352.33333 L 107.00017,365.66673 L 45.999868,365.66673 L 45.999868,363.00005 L 41.333178,363.00005 L 41.333178,365.66673 L 37.999828,365.66673 L 37.999828,352.33333 z\" \n \
     id=\"path180\" \n \
     style=\"fill:url(#linearGradient3405);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"362\" \n \
       id=\"tspan184\" \n \
       style=\"font-size:10.5px\">"

    data15 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.999827,375.99998 L 41.333177,375.99998 L 41.333177,378.66667 L 45.999867,378.66667 L 45.999867,375.99998 L 107.00017,375.99998 L 107.00017,389.33339 L 45.999867,389.33339 L 45.999867,386.6667 L 41.333177,386.6667 L 41.333177,389.33339 L 37.999827,389.33339 L 37.999827,375.99998 z\" \n \
     id=\"path188\" \n \
     style=\"fill:url(#linearGradient3413);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"386\" \n \
       id=\"tspan192\" \n \
       style=\"font-size:10.5px\">"

    data16 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.999827,399.66664 L 41.333177,399.66664 L 41.333177,402.33333 L 45.999867,402.33333 L 45.999867,399.66664 L 107.00017,399.66664 L 107.00017,413.00005 L 45.999867,413.00005 L 45.999867,410.33336 L 41.333177,410.33336 L 41.333177,413.00005 L 37.999827,413.00005 L 37.999827,399.66664 z\" \n \
     id=\"path196\" \n \
     style=\"fill:url(#linearGradient3421);fill-opacity:1;stroke:#00a000;stroke-width:1.33334005;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:8.00004005px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"409.5\" \n \
       id=\"tspan200\" \n \
       style=\"font-size:10.5px\">"

    data17 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text202\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"21.5\" \n \
       id=\"tspan204\" \n \
       style=\"font-size:20px\">"

    data18 = \
"</tspan> \n \
  </text> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"282.6077\" \n \
     id=\"rect2582\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"283.72412\" \n \
     id=\"rect2584\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"284.70215\" \n \
     id=\"rect2586\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"342.55103\" \n \
     id=\"rect2588\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"343.66745\" \n \
     id=\"rect2590\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.56932\" \n \
     height=\"0.13955142\" \n \
     x=\"3.7153397\" \n \
     y=\"344.64548\" \n \
     id=\"rect2592\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 69.4375,295.875 L 77.6875,295.875 L 77.6875,298.875 L 75.6875,298.875 L 75.6875,297.375 L 70.4375,297.375\" \n \
     id=\"path2493\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 69.4375,309.625 L 77.6875,309.625 L 77.6875,306.625 L 75.6875,306.625 L 75.6875,308.125 L 70.4375,308.125\" \n \
     id=\"path2495\" \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 45.0625,293 C 53.0625,293 67.0625,293 67.0625,293 C 67.0625,293 69.1284,294.24328 69.8125,295 C 70.511235,295.77291 71.5625,298 71.5625,298 L 71.5625,307.5 C 71.5625,307.5 70.453975,309.34683 69.8125,310 C 69.09772,310.72781 67.0625,312 67.0625,312 L 44.5625,312 L 44.5625,312 L 44.5625,314 L 34.5625,314 L 34.5625,312 L 12.0625,312 C 12.0625,312 10.02728,310.72781 9.3125,310 C 8.6710249,309.34683 7.5625,307.5 7.5625,307.5 L 7.5625,298 C 7.5625,298 8.6137641,295.77291 9.3125,295 C 9.9966011,294.24328 12.0625,293 12.0625,293 L 34.0625,293 L 34.0625,295.5 L 45.0625,295.5 L 45.0625,293 z\" \n \
     id=\"path10\" \n \
     style=\"fill:url(#linearGradient3389);fill-opacity:1;stroke:#00a000;stroke-width:1.33299994;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 121.83348,293.01471 L 113.45848,293.01471 L 113.45848,295.01471 L 102.45848,295.01471 L 102.45848,293.01471 L 94.583478,293 C 94.583478,293 92.641402,294.31904 91.958478,295.01471 C 91.416348,295.56696 90.083478,298.01471 90.083478,298.01471 L 90.083478,331.63471 C 90.083478,331.63471 90.403544,333.29901 90.833459,333.63721 C 91.248775,333.96392 93.0834,334.76471 93.0834,334.76471 L 103.08348,334.76471 L 103.08348,336.63971 L 113.08348,336.63971 L 113.08348,334.76471 L 136.58348,334.76471 L 136.58348,297.01471 L 124.58348,297.01471 L 123.33348,294.51471 L 121.83348,293.01471 z\" \n \
     id=\"path2480\" \n \
     style=\"fill:url(#linearGradient3397);fill-opacity:1;fill-rule:evenodd;stroke:#00a000;stroke-width:1.33299994;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 94.958478,303.04092 L 131.48577,303.04092 L 131.48577,329.26471 L 94.958478,329.26471 L 94.958478,303.04092 z\" \n \
     id=\"path3264\" \n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#00a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 13,298.5 L 15.5,298.5 L 15.5,300.5 L 19,300.5 L 19,298.5 L 64.75,298.5 L 64.75,308.5 L 19,308.5 L 19,306.5 L 15.5,306.5 L 15.5,308.5 L 13,308.5 L 13,298.5 z\" \n \
     id=\"path9\" \n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#00a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
</svg> \n "


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
    FILE.close()
    return

if __name__ == "__main__":
    main()
