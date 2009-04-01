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
    mystring11 = _("set text color")
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
     id=\"defs4\"> \n \
    <linearGradient \n \
       id=\"linearGradient3876\"> \n \
      <stop \n \
         id=\"stop3878\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3880\" \n \
         style=\"stop-color:#00ffff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3889\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3913\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3915\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"18.291491\" \n \
       y1=\"48.644657\" \n \
       x2=\"67.627289\" \n \
       y2=\"48.644657\" \n \
       id=\"linearGradient4830\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"77.372711\" \n \
       y1=\"48.644657\" \n \
       x2=\"126.70851\" \n \
       y2=\"48.644657\" \n \
       id=\"linearGradient4838\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"43.415215\" \n \
       y1=\"95.379143\" \n \
       x2=\"92.751015\" \n \
       y2=\"95.379143\" \n \
       id=\"linearGradient4846\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"43.415215\" \n \
       y1=\"147.44724\" \n \
       x2=\"92.751015\" \n \
       y2=\"147.44724\" \n \
       id=\"linearGradient4854\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"43.415215\" \n \
       y1=\"199.5153\" \n \
       x2=\"92.751015\" \n \
       y2=\"199.5153\" \n \
       id=\"linearGradient4862\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"43.415215\" \n \
       y1=\"258.58374\" \n \
       x2=\"92.751015\" \n \
       y2=\"258.58374\" \n \
       id=\"linearGradient4870\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       x1=\"37.331573\" \n \
       y1=\"312.79697\" \n \
       x2=\"107.66842\" \n \
       y2=\"312.79697\" \n \
       id=\"linearGradient4878\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,95.96579)\" /> \n \
    <linearGradient \n \
       x1=\"37.331573\" \n \
       y1=\"337.74872\" \n \
       x2=\"107.66842\" \n \
       y2=\"337.74872\" \n \
       id=\"linearGradient4886\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,95.96579)\" /> \n \
    <linearGradient \n \
       x1=\"37.331573\" \n \
       y1=\"362.7005\" \n \
       x2=\"107.66842\" \n \
       y2=\"362.7005\" \n \
       id=\"linearGradient4894\" \n \
       xlink:href=\"#linearGradient3876\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"translate(0,95.96579)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3172\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.67,0,0,0.67,43.745213,299.47)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         id=\"stop3168\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3170\" \n \
         style=\"stop-color:#00ffff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
  </defs> \n \
  <path \n \
     d=\"M 0.5594301,0.5 L 0.49711997,486 L 3.6209793,492 L 8.494839,496 L 15.156388,499 L 128.9813,499 L 135.82978,496 L 141.77903,492 L 144.50288,486 L 144.54057,0.5 L 0.5594301,0.5 z\" \n \
     id=\"path21\" \n \
     style=\"fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:0.99423993px;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.6\" \n \
     height=\"0.14\" \n \
     x=\"10.7\" \n \
     y=\"391\" \n \
     id=\"rect23\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.08842015;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.6\" \n \
     height=\"0.14\" \n \
     x=\"10.7\" \n \
     y=\"392\" \n \
     id=\"rect25\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.08842015;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"123.6\" \n \
     height=\"0.14\" \n \
     x=\"10.7\" \n \
     y=\"393\" \n \
     id=\"rect27\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#ffffc4;stroke-width:1.08842015;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7\" \n \
     y=\"-29\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect29\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7\" \n \
     y=\"-27.799999\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect31\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7\" \n \
     y=\"-474.79999\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect33\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#e0a000;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <rect \n \
     width=\"137.5\" \n \
     height=\"0.14\" \n \
     x=\"3.7\" \n \
     y=\"-473.5\" \n \
     transform=\"scale(1,-1)\" \n \
     id=\"rect35\" \n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;stroke:#fff080;stroke-width:1.13613331;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 80.875,486.375 C 80.875,490.86231 77.125385,494.5 72.5,494.5 C 67.874615,494.5 64.125,490.86231 64.125,486.375 C 64.125,481.88769 67.874615,478.25 72.5,478.25 C 77.125385,478.25 80.875,481.88769 80.875,486.375 L 80.875,486.375 z\" \n \
     id=\"path37\" \n \
     style=\"fill:#ff4040;fill-opacity:1;stroke:#ff4040;stroke-width:1;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"96.749023\" \n \
     id=\"text39\" \n \
     style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"490.74902\" \n \
       id=\"tspan41\" \n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff\">X</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text43\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"21\" \n \
       id=\"tspan45\" \n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 50.29309,34.643957 C 60.96029,34.643957 60.96029,34.643957 60.96029,34.643957 L 64.62714,37.310757 L 66.96059,41.310957 L 66.96059,53.978257 L 64.62714,57.311757 L 60.96029,59.978557 L 49.62639,59.978557 L 49.62639,59.978557 L 49.62639,62.645357 L 36.29239,62.645357 L 36.29239,59.978557 L 24.95849,59.978557 L 21.29164,57.311757 L 18.95819,53.978257 L 18.95819,41.310957 L 21.29164,37.310757 L 24.95849,34.643957 L 35.62569,34.643957 L 35.62569,37.977457 L 50.29309,37.977457 L 50.29309,34.643957 z\" \n \
     id=\"path47\" \n \
     style=\"fill:url(#linearGradient4830);fill-opacity:1;stroke:#00a0a0;stroke-width:1;stroke-opacity:1\" /> \n "

    data2a = \
"  <text \n \
     id=\"text49\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"43\" \n \
       y=\"51.5\" \n \
       id=\"tspan51\" \n \
       style=\"font-size:11px\">"

    data2b = \
"  <text \n \
     id=\"text49\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"43\" \n \
       y=\"45\" \n \
       id=\"tspan51\" \n \
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
       id=\"tspan51\" \n \
       style=\"font-size:10px\">"

    data4 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 109.37431,34.643957 C 120.04151,34.643957 120.04151,34.643957 120.04151,34.643957 L 123.70836,37.310757 L 126.04181,41.310957 L 126.04181,53.978257 L 123.70836,57.311757 L 120.04151,59.978557 L 108.70761,59.978557 L 108.70761,59.978557 L 108.70761,62.645357 L 95.373609,62.645357 L 95.373609,59.978557 L 84.039709,59.978557 L 80.372859,57.311757 L 78.039409,53.978257 L 78.039409,41.310957 L 80.372859,37.310757 L 84.039709,34.643957 L 94.706909,34.643957 L 94.706909,37.977457 L 109.37431,37.977457 L 109.37431,34.643957 z\" \n \
     id=\"path53\" \n \
     style=\"fill:url(#linearGradient4838);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n "

    data5a = \
"  <text \n \
     id=\"text55\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"101\" \n \
       y=\"51.5\" \n \
       id=\"tspan57\" \n \
       style=\"font-size:11px\">"

    data5b = \
"  <text \n \
     id=\"text55\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"101\" \n \
       y=\"45\" \n \
       id=\"tspan57\" \n \
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
       id=\"tspan57\" \n \
       style=\"font-size:10px\">"

    data7 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 90.084213,85.211967 L 101.08476,85.211967 L 101.08476,89.212167 L 98.417963,89.212167 L 98.417963,87.212067 L 91.417613,87.212067\" \n \
     id=\"path59\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.084213,103.54622 L 101.08476,103.54622 L 101.08476,99.546017 L 98.417963,99.546017 L 98.417963,101.54612 L 91.417613,101.54612\" \n \
     id=\"path61\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.416813,76.044842 C 86.084013,76.044842 86.084013,76.044842 86.084013,76.044842 L 89.750863,78.711642 L 92.084313,82.711842 L 92.084313,105.37964 L 89.750863,109.37984 L 86.084013,112.04664 L 74.750113,112.04664 L 74.750113,112.04664 L 74.750113,114.71344 L 61.416113,114.71344 L 61.416113,112.04664 L 50.082213,112.04664 L 46.415363,109.37984 L 44.081913,105.37964 L 44.081913,82.711842 L 46.415363,78.711642 L 50.082213,76.044842 L 60.749413,76.044842 L 60.749413,79.378342 L 75.416813,79.378342 L 75.416813,76.044842 z\" \n \
     id=\"path63\" \n \
     style=\"fill:url(#linearGradient4846);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n "

    data8a = \
"  <text \n \
     id=\"text65\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"99\" \n \
       id=\"tspan67\" \n \
       style=\"font-size:11px\">"

    data8b = \
"  <text \n \
     id=\"text65\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"93\" \n \
       id=\"tspan67\" \n \
       style=\"font-size:11px\">"

    data8c = \
"  <text \n \
     id=\"text65\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"88\" \n \
       id=\"tspan67\" \n \
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
       id=\"tspan71\" \n \
       style=\"font-size:11px\">"

    data9c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text69\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"97\" \n \
       id=\"tspan71\" \n \
       style=\"font-size:10px\">"

    data10c = \
"</tspan> \n \
  </text> \n \
  <text \n \
     id=\"text69\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"106\" \n \
       id=\"tspan71\" \n \
       style=\"font-size:10px\">"

    data11 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 90.084213,137.28005 L 101.08476,137.28005 L 101.08476,141.28025 L 98.417963,141.28025 L 98.417963,139.28015 L 91.417613,139.28015\" \n \
     id=\"path73\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.084213,155.6143 L 101.08476,155.6143 L 101.08476,151.6141 L 98.417963,151.6141 L 98.417963,153.6142 L 91.417613,153.6142\" \n \
     id=\"path75\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.416813,128.11293 C 86.084013,128.11293 86.084013,128.11293 86.084013,128.11293 L 89.750863,130.77973 L 92.084313,134.77993 L 92.084313,157.44773 L 89.750863,161.44793 L 86.084013,164.11473 L 74.750113,164.11473 L 74.750113,164.11473 L 74.750113,166.78153 L 61.416113,166.78153 L 61.416113,164.11473 L 50.082213,164.11473 L 46.415363,161.44793 L 44.081913,157.44773 L 44.081913,134.77993 L 46.415363,130.77973 L 50.082213,128.11293 L 60.749413,128.11293 L 60.749413,131.44643 L 75.416813,131.44643 L 75.416813,128.11293 z\" \n \
     id=\"path77\" \n \
     style=\"fill:url(#linearGradient4854);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n "

    data12a = \
"  <text \n \
     id=\"text79\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"151\" \n \
       id=\"tspan81\" \n \
       style=\"font-size:11px\">"

    data12b = \
"  <text \n \
     id=\"text79\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"145\" \n \
       id=\"tspan81\" \n \
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
       id=\"tspan85\" \n \
       style=\"font-size:11px\">"

    data14 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 90.084213,189.34813 L 101.08476,189.34813 L 101.08476,193.34833 L 98.417963,193.34833 L 98.417963,191.34823 L 91.417613,191.34823\" \n \
     id=\"path87\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.084213,207.68238 L 101.08476,207.68238 L 101.08476,203.68218 L 98.417963,203.68218 L 98.417963,205.68228 L 91.417613,205.68228\" \n \
     id=\"path89\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.416813,180.18101 C 86.084013,180.18101 86.084013,180.18101 86.084013,180.18101 L 89.750863,182.84781 L 92.084313,186.84801 L 92.084313,209.51581 L 89.750863,213.51601 L 86.084013,216.18281 L 74.750113,216.18281 L 74.750113,216.18281 L 74.750113,218.84961 L 61.416113,218.84961 L 61.416113,216.18281 L 50.082213,216.18281 L 46.415363,213.51601 L 44.081913,209.51581 L 44.081913,186.84801 L 46.415363,182.84781 L 50.082213,180.18101 L 60.749413,180.18101 L 60.749413,183.51451 L 75.416813,183.51451 L 75.416813,180.18101 z\" \n \
     id=\"path91\" \n \
     style=\"fill:url(#linearGradient4862);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n "

    data15a = \
"  <text \n \
     id=\"text93\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"203\" \n \
       id=\"tspan95\" \n \
       style=\"font-size:11px\">"

    data15b = \
"  <text \n \
     id=\"text93\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68\" \n \
       y=\"197\" \n \
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
       y=\"210\" \n \
       id=\"tspan99\" \n \
       style=\"font-size:11px\">"

    data17 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 89.917538,260.08382 L 100.91809,260.08382 L 100.91809,264.2507 L 98.251288,264.2507 L 98.251288,262.08393 L 91.250938,262.08393\" \n \
     id=\"path101\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 89.917538,278.41807 L 100.91809,278.41807 L 100.91809,274.41787 L 98.251288,274.41787 L 98.251288,276.41797 L 91.250938,276.41797\" \n \
     id=\"path103\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.084213,235.5826 L 101.08476,235.5826 L 101.08476,239.5828 L 98.417963,239.5828 L 98.417963,237.5827 L 91.417613,237.5827\" \n \
     id=\"path105\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.084213,253.91685 L 101.08476,253.91685 L 101.08476,249.91665 L 98.417963,249.91665 L 98.417963,251.91675 L 91.417613,251.91675\" \n \
     id=\"path107\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.00004995;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.416813,232.2491 C 86.084013,232.2491 86.084013,232.2491 86.084013,232.2491 L 89.750863,234.9159 L 92.084313,238.9161 L 92.084313,276.2513 L 89.750863,279.5848 L 86.084013,282.2516 L 74.750113,282.2516 L 74.750113,282.2516 L 74.750113,284.9184 L 61.416113,284.9184 L 61.416113,282.2516 L 50.082213,282.2516 L 46.415363,279.5848 L 44.081913,276.2513 L 44.081913,238.9161 L 46.415363,234.9159 L 50.082213,232.2491 L 60.749413,232.2491 L 60.749413,235.5826 L 75.416813,235.5826 L 75.416813,232.2491 z\" \n \
     id=\"path109\" \n \
     style=\"fill:url(#linearGradient4870);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n \
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
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.998275,402.09575 L 41.331775,402.09575 L 41.331775,404.76255 L 45.998675,404.76255 L 45.998675,402.09575 L 107.00172,402.09575 L 107.00172,415.42975 L 45.998675,415.42975 L 45.998675,412.76295 L 41.331775,412.76295 L 41.331775,415.42975 L 37.998275,415.42975 L 37.998275,402.09575 z\" \n \
     id=\"path127\" \n \
     style=\"fill:url(#linearGradient4878);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text129\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"74\" \n \
       y=\"412\" \n \
       id=\"tspan131\" \n \
       style=\"font-size:10.5px\">"

    data22 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.998275,427.04752 L 41.331775,427.04752 L 41.331775,429.71432 L 45.998675,429.71432 L 45.998675,427.04752 L 107.00172,427.04752 L 107.00172,440.38152 L 45.998675,440.38152 L 45.998675,437.71472 L 41.331775,437.71472 L 41.331775,440.38152 L 37.998275,440.38152 L 37.998275,427.04752 z\" \n \
     id=\"path133\" \n \
     style=\"fill:url(#linearGradient4886);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n \
  <text \n \
     id=\"text135\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"74\" \n \
       y=\"437\" \n \
       id=\"tspan137\" \n \
       style=\"font-size:10.5px\">"

    data23 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 37.998275,451.9993 L 41.331775,451.9993 L 41.331775,454.6661 L 45.998675,454.6661 L 45.998675,451.9993 L 107.00172,451.9993 L 107.00172,465.3333 L 45.998675,465.3333 L 45.998675,462.6665 L 41.331775,462.6665 L 41.331775,465.3333 L 37.998275,465.3333 L 37.998275,451.9993 z\" \n \
     id=\"path139\" \n \
     style=\"fill:url(#linearGradient4894);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33340001;stroke-opacity:1\" /> \n \
  <text \n \
     y=\"95.96579\" \n \
     id=\"text141\" \n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72.5\" \n \
       y=\"461.96579\" \n \
       id=\"tspan143\" \n \
       style=\"font-size:10.5px\">"

    data24 = \
"</tspan> \n \
  </text> \n \
  <path \n \
     d=\"M 90.645213,309.3525 L 101.70021,309.3525 L 101.70021,313.3725 L 99.020213,313.3725 L 99.020213,311.3625 L 91.985213,311.3625\" \n \
     id=\"path2622\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.29999995;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 90.645213,327.7775 L 101.70021,327.7775 L 101.70021,323.7575 L 99.020213,323.7575 L 99.020213,325.7675 L 91.985213,325.7675\" \n \
     id=\"path2624\" \n \
     style=\"fill:#00e0e0;fill-opacity:1;stroke:#008080;stroke-width:1.29999995;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <path \n \
     d=\"M 75.905213,300.14 C 86.625213,300.14 86.625213,300.14 86.625213,300.14 L 90.310213,302.82 L 92.655213,306.84 L 92.655213,329.62 L 90.310213,333.64 L 86.625213,336.32 L 75.235213,336.32 L 75.235213,336.32 L 75.235213,339 L 61.835213,339 L 61.835213,336.32 L 50.445213,336.32 L 46.760213,333.64 L 44.415213,329.62 L 44.415213,306.84 L 46.760213,302.82 L 50.445213,300.14 L 61.165213,300.14 L 61.165213,303.49 L 75.905213,303.49 L 75.905213,300.14 z\" \n \
     id=\"path2626\" \n \
     style=\"fill:url(#linearGradient4886);fill-opacity:1;stroke:#00a0a0;stroke-width:1.33;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     x=\"43.745213\" \n \
     y=\"299.47\" \n \
     id=\"text2628\" \n \
     style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68.53521\" \n \
       y=\"314.20999\" \n \
       id=\"tspan2630\" \n \
       style=\"font-size:10.5px\">"

    data25 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     x=\"43.745213\" \n \
     y=\"299.47\" \n \
     id=\"text2632\" \n \
     style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68.53521\" \n \
       y=\"323.59\" \n \
       id=\"tspan2634\" \n \
       style=\"font-size:10.5px\">"

    data26 = \
"</tspan> \n \
  </text> \n \
  <text \n \
     x=\"43.745213\" \n \
     y=\"299.47\" \n \
     id=\"text2636\" \n \
     style=\"font-size:10.5px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"68.53521\" \n \
       y=\"332.97\" \n \
       id=\"tspan2638\" \n \
       style=\"font-size:10.5px\">"

    data27 = \
"</tspan> \n \
  </text> \n \
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
    FILE.close()
    return

if __name__ == "__main__":
    main()
