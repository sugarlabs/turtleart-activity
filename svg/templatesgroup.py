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
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring1 = _("Templates")
    mystring2 = _("hide blocks")
    mygroup = "templates"

    print mystring1
    print mystring2


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
       id=\"linearGradient3245\">\n \
      <stop\n \
         id=\"stop3247\"\n \
         style=\"stop-color:#ffffff;stop-opacity:1\"\n \
         offset=\"0\" />\n \
      <stop\n \
         id=\"stop3249\"\n \
         style=\"stop-color:#ffff00;stop-opacity:0\"\n \
         offset=\"1\" />\n \
    </linearGradient>\n \
    <linearGradient\n \
       x1=\"47\"\n \
       y1=\"445\"\n \
       x2=\"97\"\n \
       y2=\"445\"\n \
       id=\"linearGradient3291\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"11\"\n \
       y1=\"109\"\n \
       x2=\"63\"\n \
       y2=\"109\"\n \
       id=\"linearGradient3251\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"4\"\n \
       y1=\"188\"\n \
       x2=\"70\"\n \
       y2=\"188\"\n \
       id=\"linearGradient3259\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"13\"\n \
       y1=\"270\"\n \
       x2=\"61\"\n \
       y2=\"270\"\n \
       id=\"linearGradient3267\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"75\"\n \
       y1=\"188\"\n \
       x2=\"141\"\n \
       y2=\"188\"\n \
       id=\"linearGradient3323\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"82\"\n \
       y1=\"248\"\n \
       x2=\"134\"\n \
       y2=\"248\"\n \
       id=\"linearGradient3315\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"12\"\n \
       y1=\"392\"\n \
       x2=\"80\"\n \
       y2=\"392\"\n \
       id=\"linearGradient3275\"\n \
       xlink:href=\"#linearGradient3245\" />\n \
    <linearGradient\n \
       x1=\"47\"\n \
       y1=\"52\"\n \
       x2=\"97\"\n \
       y2=\"52\"\n \
       id=\"linearGradient3283\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"82\"\n \
       y1=\"392\"\n \
       x2=\"132\"\n \
       y2=\"392\"\n \
       id=\"linearGradient3307\"\n \
       xlink:href=\"#linearGradient3245\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"-31\"\n \
       x2=\"104\"\n \
       y2=\"20\"\n \
       id=\"linearGradient3172\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"0\"\n \
       y1=\"-31\"\n \
       x2=\"104\"\n \
       y2=\"20\"\n \
       id=\"linearGradient2698\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"82\"\n \
       y1=\"119\"\n \
       x2=\"134\"\n \
       y2=\"119\"\n \
       id=\"linearGradient3331\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"47\"\n \
       y1=\"52\"\n \
       x2=\"97\"\n \
       y2=\"52\"\n \
       id=\"linearGradient2803\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"47.393524\"\n \
       y1=\"52.893875\"\n \
       x2=\"97.606476\"\n \
       y2=\"52.893875\"\n \
       id=\"linearGradient2686\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(-39.41375,0)\" />\n \
    <linearGradient\n \
       x1=\"82.928017\"\n \
       y1=\"119.21875\"\n \
       x2=\"134.55301\"\n \
       y2=\"119.21875\"\n \
       id=\"linearGradient2684\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,94)\" />\n \
    <linearGradient\n \
       x1=\"0.94254935\"\n \
       y1=\"-31.669659\"\n \
       x2=\"104.37702\"\n \
       y2=\"20.434471\"\n \
       id=\"linearGradient2682\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"matrix(0.7083638,0,0,1.0012565,0.1338084,32.632067)\" />\n \
    <linearGradient\n \
       x1=\"0.94254935\"\n \
       y1=\"-31.669659\"\n \
       x2=\"104.37702\"\n \
       y2=\"20.434471\"\n \
       id=\"linearGradient2680\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"matrix(0.7083638,0,0,1.0012565,0.1338084,32.632067)\" />\n \
    <linearGradient\n \
       x1=\"82.356911\"\n \
       y1=\"392.34818\"\n \
       x2=\"132.61295\"\n \
       y2=\"392.34818\"\n \
       id=\"linearGradient2678\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"47.393524\"\n \
       y1=\"52.893875\"\n \
       x2=\"97.606476\"\n \
       y2=\"52.893875\"\n \
       id=\"linearGradient2676\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(-39.41375,0)\" />\n \
    <linearGradient\n \
       x1=\"12.124999\"\n \
       y1=\"392.34818\"\n \
       x2=\"80.875\"\n \
       y2=\"392.34818\"\n \
       id=\"linearGradient2674\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"82.928009\"\n \
       y1=\"248.60938\"\n \
       x2=\"134.55301\"\n \
       y2=\"248.60938\"\n \
       id=\"linearGradient2672\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,94)\" />\n \
    <linearGradient\n \
       x1=\"75.990517\"\n \
       y1=\"188.5\"\n \
       x2=\"141.49051\"\n \
       y2=\"188.5\"\n \
       id=\"linearGradient2670\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,94)\" />\n \
    <linearGradient\n \
       x1=\"13.33134\"\n \
       y1=\"270.5\"\n \
       x2=\"61.206341\"\n \
       y2=\"270.5\"\n \
       id=\"linearGradient2668\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,94)\" />\n \
    <linearGradient\n \
       x1=\"4.5188398\"\n \
       y1=\"188.5\"\n \
       x2=\"70.018837\"\n \
       y2=\"188.5\"\n \
       id=\"linearGradient2666\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,94)\" />\n \
    <linearGradient\n \
       x1=\"11.45634\"\n \
       y1=\"109.14062\"\n \
       x2=\"63.081341\"\n \
       y2=\"109.14062\"\n \
       id=\"linearGradient2664\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\"\n \
       gradientTransform=\"translate(0,94)\" />\n \
    <linearGradient\n \
       x1=\"47.715\"\n \
       y1=\"445.94196\"\n \
       x2=\"97.284996\"\n \
       y2=\"445.94196\"\n \
       id=\"linearGradient2662\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       id=\"linearGradient2656\">\n \
      <stop\n \
         id=\"stop2658\"\n \
         style=\"stop-color:#ffffff;stop-opacity:1\"\n \
         offset=\"0\" />\n \
      <stop\n \
         id=\"stop2660\"\n \
         style=\"stop-color:#ffff00;stop-opacity:0\"\n \
         offset=\"1\" />\n \
    </linearGradient>\n \
    <linearGradient\n \
       x1=\"47.393524\"\n \
       y1=\"54.202423\"\n \
       x2=\"97.606476\"\n \
       y2=\"54.202423\"\n \
       id=\"linearGradient3338\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"47.415104\"\n \
       y1=\"99.202805\"\n \
       x2=\"97.584892\"\n \
       y2=\"99.202805\"\n \
       id=\"linearGradient3372\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
    <linearGradient\n \
       x1=\"47.269257\"\n \
       y1=\"146.11281\"\n \
       x2=\"97.730743\"\n \
       y2=\"146.11281\"\n \
       id=\"linearGradient3388\"\n \
       xlink:href=\"#linearGradient3245\"\n \
       gradientUnits=\"userSpaceOnUse\" />\n \
  </defs>\n \
  <path\n \
     d=\"M 0.5,0.5 L 0.5,486 C 1.5,488.5 2.5,490.5 3.5,493 C 5,494.5 6.5,495.5 8.5,497 C 10.5,497.5 13,498.5 15,499 L 129,499 C 131,498.5 133.5,497.5 135.5,497 C 137.5,495.5 139.5,494.5 141.5,493 C 142.5,490.5 143.5,488.5 144.5,486 L 144.5,0.5 L 0.5,0.5 z\"\n \
     id=\"path22\"\n \
     style=\"fill:#ffd000;fill-opacity:1;fill-rule:evenodd;stroke:#e0a000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123\"\n \
     height=\"0.14\"\n \
     x=\"10\"\n \
     y=\"173\"\n \
     id=\"rect3987\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123\"\n \
     height=\"0.14\"\n \
     x=\"10\"\n \
     y=\"174\"\n \
     id=\"rect3989\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123\"\n \
     height=\"0.14\"\n \
     x=\"10\"\n \
     y=\"175\"\n \
     id=\"rect3991\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#ffffc4;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3\"\n \
     y=\"-28\"\n \
     transform=\"scale(1,-1)\"\n \
     id=\"rect3993\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3\"\n \
     y=\"-27\"\n \
     transform=\"scale(1,-1)\"\n \
     id=\"rect3995\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3\"\n \
     y=\"-474\"\n \
     transform=\"scale(1,-1)\"\n \
     id=\"rect3999\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"137\"\n \
     height=\"0.14\"\n \
     x=\"3\"\n \
     y=\"-473\"\n \
     transform=\"scale(1,-1)\"\n \
     id=\"rect4001\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 80,487 C 80,491 77,495 72,495 C 67,495 64,491 64,487 C 64,482 67,479 72,479 C 77,479 80,482 80,487 L 80,487 z\"\n \
     id=\"path4003\"\n \
     style=\"fill:#ff4040;fill-opacity:1;fill-rule:nonzero;stroke:#ff4040;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <text\n \
     id=\"text32\"\n \
     xml:space=\"preserve\"\n \
     style=\"font-size:12px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:start;line-height:125%;writing-mode:lr-tb;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Bitstream Vera Sans;-inkscape-font-specification:Bitstream Vera Sans Bold\"><tspan\n \
       x=\"67\"\n \
       y=\"491\"\n \
       id=\"tspan4007\"\n \
       style=\"font-size:12px;font-weight:bold;fill:#ffffff;font-family:Bitstream Vera Sans\">X</tspan></text>\n \
  <text\n \
     id=\"text35\"\n \
     style=\"font-size:12px;font-style:normal;font-weight:normal;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"22\"\n \
       y=\"21\"\n \
       id=\"tspan2796\"\n \
       style=\"font-size:20px\">"

    data1 = \
"</tspan>\n \
  </text>\n \
  <path\n \
     d=\"M 79,426 C 90,426 90,426 90,426 L 94,429 L 96,433 L 96,455 L 94,460 L 90,462 L 79,462 L 79,462 L 79,465 L 65,465 L 65,462 L 54,462 L 50,460 L 48,455 L 48,433 L 50,429 L 54,426 L 65,426 L 65,429 L 79,429 L 79,426 z\"\n \
     id=\"path2714\"\n \
     style=\"fill:url(#linearGradient3291);fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n "

    data2a = \
"  <text\n \
     id=\"text39\"\n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"449\"\n \
       id=\"tspan2718\"\n \
       style=\"font-size:12px\">"

    data2b = \
"  <text\n \
     id=\"text42\"\n \
     style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\">\n \
    <tspan\n \
       x=\"72\"\n \
       y=\"443\"\n \
       id=\"tspan2722\"\n \
       style=\"font-size:12px\">"

    data3b = \
"</tspan> \n \
  </text> \n \
  <text \n \
     style=\"font-size:12.06000042px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\"> \n \
    <tspan \n \
       x=\"72\" \n \
       y=\"456\" \n \
       id=\"tspan2722\" \n \
       style=\"font-size:12px\">"

    data4 = \
"</tspan>\n \
  </text>\n \
  <rect\n \
     width=\"123\"\n \
     height=\"0.14\"\n \
     x=\"10\"\n \
     y=\"415\"\n \
     id=\"rect3434\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#e0a000;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123\"\n \
     height=\"0.14\"\n \
     x=\"10\"\n \
     y=\"416\"\n \
     id=\"rect3436\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#fff080;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <rect\n \
     width=\"123\"\n \
     height=\"0.14\"\n \
     x=\"10\"\n \
     y=\"417\"\n \
     id=\"rect3438\"\n \
     style=\"opacity:1;fill:#ffd000;fill-opacity:1;fill-rule:nonzero;stroke:#ffffc4;stroke-width:1;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 35,182 L 29,182 L 29,184 L 21,184 L 21,182 L 15,182 C 15,182 13,183 13,183 C 12,184 11,186 11,186 L 11,220 C 11,220 12,221 12,221 C 12,221 14,222 14,222 L 21,222 L 21,224 L 29,224 L 29,222 L 62,222 L 62,183 L 37,183 L 36,183 L 35,182 z\"\n \
     id=\"path4158\"\n \
     style=\"fill:url(#linearGradient3251);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 15,199 L 43,199 L 43,219 L 15,219 L 15,199 z\"\n \
     id=\"path4162\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <polygon\n \
     points=\"10,6 31,6 43,18 43,48 10,48 10,6 \"\n \
     transform=\"matrix(0.375,0,0,0.375,42.63809,197.40725)\"\n \
     id=\"polygon2963\"\n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" />\n \
  <polyline\n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\"\n \
     points=\"43,18 31,18 31,6    \"\n \
     id=\"polyline2965\"\n \
     transform=\"matrix(0.375,0,0,0.375,42.63809,197.40725)\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"49\"\n \
     x2=\"56\"\n \
     y1=\"207\"\n \
     y2=\"207\"\n \
     id=\"line2967\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"49\"\n \
     x2=\"56\"\n \
     y1=\"209.5\"\n \
     y2=\"209.5\"\n \
     id=\"line2969\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"49\"\n \
     x2=\"56\"\n \
     y1=\"212\"\n \
     y2=\"212\"\n \
     id=\"line2971\" />\n \
  <path\n \
     d=\"M 28,251 L 22,251 L 22,253 L 14,253 L 14,251 L 8,251 C 8,251 6,252 6,253 C 6,253 5,255 5,255 L 5,309 C 5,309 5,311 5,311 C 5,311 7,312 7,312 L 14,312 L 14,313 L 22,313 L 22,312 L 69,312 L 69,253 L 30,253 L 29,252 L 28,251 z\"\n \
     id=\"path4390\"\n \
     style=\"fill:url(#linearGradient3259);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 8,268 L 36,268 L 36,288 L 8,288 L 8,268 z\"\n \
     id=\"path4394\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 38,268 L 66,268 L 66,288 L 38,288 L 38,268 z\"\n \
     id=\"path2418\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <polygon\n \
     points=\"10,6 31,6 43,18 43,48 10,48 10,6 \"\n \
     transform=\"matrix(0.375,0,0,0.375,4.95059,289.5635)\"\n \
     id=\"polygon4402\"\n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\" />\n \
  <polyline\n \
     style=\"fill:none;stroke:#010101;stroke-width:2.66666675;stroke-miterlimit:4;stroke-dasharray:none\"\n \
     points=\"43,18 31,18 31,6    \"\n \
     id=\"polyline4404\"\n \
     transform=\"matrix(0.375,0,0,0.375,4.95059,289.5635)\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"11\"\n \
     x2=\"18\"\n \
     y1=\"299\"\n \
     y2=\"299\"\n \
     id=\"line4406\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"11\"\n \
     x2=\"18\"\n \
     y1=\"301.5\"\n \
     y2=\"301.5\"\n \
     id=\"line4408\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"11\"\n \
     x2=\"18\"\n \
     y1=\"304\"\n \
     y2=\"304\"\n \
     id=\"line4410\" />\n \
  <polygon\n \
     points=\"10,6 31,6 43,18 43,48 10,48 10,6 \"\n \
     transform=\"matrix(0.375,0,0,0.375,34.95059,289.5635)\"\n \
     id=\"polygon2582\"\n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none\" />\n \
  <polyline\n \
     style=\"fill:none;stroke:#010101;stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none\"\n \
     points=\"43,18 31,18 31,6    \"\n \
     id=\"polyline2584\"\n \
     transform=\"matrix(0.375,0,0,0.375,34.95059,289.5635)\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"41\"\n \
     x2=\"48\"\n \
     y1=\"299\"\n \
     y2=\"299\"\n \
     id=\"line2586\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"41\"\n \
     x2=\"48\"\n \
     y1=\"301.5\"\n \
     y2=\"301.5\"\n \
     id=\"line2588\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"41\"\n \
     x2=\"48\"\n \
     y1=\"304\"\n \
     y2=\"304\"\n \
     id=\"line2590\" />\n \
  <path\n \
     d=\"M 37,321 L 31,321 L 31,323 L 23,323 L 23,321 L 17,321 C 17,321 15,322 15,323 C 14,323 13,325 13,325 L 13,403 C 13,403 14,404 14,405 C 14,405 16,406 16,406 L 23,406 L 23,407 L 31,407 L 31,406 L 60,406 L 60,323 L 39,323 L 38,322 L 37,321 z\"\n \
     id=\"path4690\"\n \
     style=\"fill:url(#linearGradient3267);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 106,182 L 100,182 L 100,184 L 92,184 L 92,182 L 86,182 C 86,182 85,183 84,183 C 84,184 83,186 83,186 L 83,240 C 83,240 83,241 83,241 C 84,242 85,242 85,242 L 93,242 L 93,244 L 100,244 L 100,242 L 134,242 L 134,183 L 108,183 L 107,183 L 106,182 z\"\n \
     id=\"path5171\"\n \
     style=\"fill:url(#linearGradient3331);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 87,199 L 114,199 L 114,219 L 87,219 L 87,199 z\"\n \
     id=\"path5175\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <polygon\n \
     points=\"10,6 31,6 43,18 43,48 10,48 10,6 \"\n \
     transform=\"matrix(0.375,0,0,0.375,114.10977,197.40724)\"\n \
     id=\"polygon5183\"\n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none\" />\n \
  <polyline\n \
     style=\"fill:none;stroke:#010101;stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none\"\n \
     points=\"43,18 31,18 31,6    \"\n \
     id=\"polyline5185\"\n \
     transform=\"matrix(0.375,0,0,0.375,114.10977,197.40724)\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"120\"\n \
     x2=\"127\"\n \
     y1=\"207\"\n \
     y2=\"207\"\n \
     id=\"line5187\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"120\"\n \
     x2=\"127\"\n \
     y1=\"209.5\"\n \
     y2=\"209.5\"\n \
     id=\"line5189\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"120\"\n \
     x2=\"127\"\n \
     y1=\"212\"\n \
     y2=\"212\"\n \
     id=\"line5191\" />\n \
  <path\n \
     d=\"M 87,220 L 114,220 L 114,240 L 87,240 L 87,220 z\"\n \
     id=\"path2425\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <polygon\n \
     points=\"10,6 31,6 43,18 43,48 10,48 10,6 \"\n \
     transform=\"matrix(0.375,0,0,0.375,113.96295,219.10807)\"\n \
     id=\"polygon2433\"\n \
     style=\"fill:#ffffff;stroke:#010101;stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none\" />\n \
  <polyline\n \
     style=\"fill:none;stroke:#010101;stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none\"\n \
     points=\"43,18 31,18 31,6    \"\n \
     id=\"polyline2435\"\n \
     transform=\"matrix(0.375,0,0,0.375,113.96295,219.10807)\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"120\"\n \
     x2=\"127\"\n \
     y1=\"228\"\n \
     y2=\"228\"\n \
     id=\"line2437\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"120\"\n \
     x2=\"127\"\n \
     y1=\"231\"\n \
     y2=\"231\"\n \
     id=\"line2439\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"120\"\n \
     x2=\"127\"\n \
     y1=\"234\"\n \
     y2=\"234\"\n \
     id=\"line2441\" />\n \
  <path\n \
     d=\"M 99,251 L 94,251 L 94,253 L 85,253 L 85,251 L 79,251 C 79,251 78,252 77,253 C 77,253 76,255 76,255 L 76,309 C 76,309 76,310 77,311 C 77,311 78,311 78,311 L 86,311 L 86,313 L 93,313 L 93,311 L 140,311 L 140,253 L 101,253 L 101,252 L 99,251 z\"\n \
     id=\"path5376\"\n \
     style=\"fill:url(#linearGradient3323);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 80,268 L 107,268 L 107,288 L 80,288 L 80,268 z\"\n \
     id=\"path5380\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 110,268 L 137,268 L 137,288 L 110,288 L 110,268 z\"\n \
     id=\"path5382\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 80,290 L 107,290 L 107,309 L 80,309 L 80,290 z\"\n \
     id=\"path2410\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 110,290 L 137,290 L 137,309 L 110,309 L 110,290 z\"\n \
     id=\"path2412\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 106,321 L 100,321 L 100,323 L 92,323 L 92,321 L 86,321 C 86,321 85,322 84,323 C 84,323 83,325 83,325 L 83,359 C 83,359 83,360 83,361 C 84,361 85,362 85,362 L 93,362 L 93,363 L 100,363 L 100,362 L 134,362 L 134,323 L 108,323 L 107,322 L 106,321 z\"\n \
     id=\"path3036\"\n \
     style=\"fill:url(#linearGradient3315);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 87,338 L 114,338 L 114,358 L 87,358 L 87,338 z\"\n \
     id=\"path3040\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 87,187 L 89,187 L 89,188 L 91,188 L 91,187 L 122,187 L 122,194 L 91,194 L 91,192 L 89,192 L 89,194 L 87,194 L 87,187 z\"\n \
     id=\"path9\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,385 L 19,385 L 19,387 L 21,387 L 21,385 L 52,385 L 52,392 L 21,392 L 21,391 L 19,391 L 19,392 L 17,392 L 17,385 z\"\n \
     id=\"path3323\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,376 L 19,376 L 19,377 L 21,377 L 21,376 L 52,376 L 52,382 L 21,382 L 21,381 L 19,381 L 19,382 L 17,382 L 17,376 z\"\n \
     id=\"path3325\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,366 L 19,366 L 19,367 L 21,367 L 21,366 L 52,366 L 52,372 L 21,372 L 21,371 L 19,371 L 19,372 L 17,372 L 17,366 z\"\n \
     id=\"path3327\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,356 L 19,356 L 19,357 L 21,357 L 21,356 L 52,356 L 52,363 L 21,363 L 21,361 L 19,361 L 19,363 L 17,363 L 17,356 z\"\n \
     id=\"path3329\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,336 L 19,336 L 19,338 L 21,338 L 21,336 L 52,336 L 52,343 L 21,343 L 21,342 L 19,342 L 19,343 L 17,343 L 17,336 z\"\n \
     id=\"path3331\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 8,257 L 10,257 L 10,258 L 12,258 L 12,257 L 43,257 L 43,264 L 12,264 L 12,262 L 10,262 L 10,264 L 8,264 L 8,257 z\"\n \
     id=\"path3333\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 15,187 L 17,187 L 17,188 L 19,188 L 19,187 L 50,187 L 50,194 L 19,194 L 19,192 L 17,192 L 17,194 L 15,194 L 15,187 z\"\n \
     id=\"path3335\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 80,257 L 82,257 L 82,258 L 84,258 L 84,257 L 115,257 L 115,264 L 84,264 L 84,262 L 82,262 L 82,264 L 80,264 L 80,257 z\"\n \
     id=\"path3337\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,327 L 19,327 L 19,328 L 21,328 L 21,327 L 52,327 L 52,333 L 21,333 L 21,332 L 19,332 L 19,333 L 17,333 L 17,327 z\"\n \
     id=\"path3339\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,395 L 19,395 L 19,396 L 21,396 L 21,395 L 52,395 L 52,402 L 21,402 L 21,400 L 19,400 L 19,402 L 17,402 L 17,395 z\"\n \
     id=\"path3341\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 17,346 L 19,346 L 19,348 L 21,348 L 21,346 L 52,346 L 52,353 L 21,353 L 21,352 L 19,352 L 19,353 L 17,353 L 17,346 z\"\n \
     id=\"path3343\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 87,327 L 88,327 L 88,328 L 91,328 L 91,327 L 121,327 L 121,334 L 91,334 L 91,332 L 88,332 L 88,334 L 87,334 L 87,327 z\"\n \
     id=\"path3345\"\n \
     style=\"fill:#ffffff;fill-opacity:1;stroke:#c0a000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 48.060226,36.763001 L 96.939774,36.763001 L 96.939774,71.641849 L 48.060226,71.641849 L 48.060226,36.763001 z\"\n \
     id=\"path2685\"\n \
     style=\"fill:url(#linearGradient3338);fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1.33340001;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 82.12025,62.556689 C 82.12025,63.812189 81.35625,64.722189 79.95425,64.722189 L 65.22575,64.722189 L 65.22575,43.222189 L 79.95475,43.222189 C 81.02975,43.222189 82.12075,44.299189 82.12075,45.387189 L 82.12025,62.556689 L 82.12025,62.556689 z\"\n \
     id=\"path3155\"\n \
     style=\"fill:#ffffff;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <line\n \
     style=\"fill:none;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\"\n \
     x1=\"69.85775\"\n \
     x2=\"69.85775\"\n \
     y1=\"43.282688\"\n \
     y2=\"64.662689\"\n \
     id=\"line3157\" />\n \
  <path\n \
     d=\"M 62.87925,47.454189 C 62.87925,47.454189 63.92125,47.801689 64.96425,47.801689 C 66.00725,47.801689 67.05075,47.454189 67.05075,47.454189\"\n \
     id=\"path3159\"\n \
     style=\"fill:none;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 62.87925,54.232689 C 62.87925,54.232689 63.83525,54.580189 65.05175,54.580189 C 66.26825,54.580189 67.05125,54.232689 67.05125,54.232689\"\n \
     id=\"path3161\"\n \
     style=\"fill:none;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 62.87925,60.838189 C 62.87925,60.838189 63.74725,61.185689 65.13825,61.185689 C 66.52875,61.185689 67.05075,60.838189 67.05075,60.838189\"\n \
     id=\"path3163\"\n \
     style=\"fill:none;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 47.939255,128.58707 L 97.060745,128.58707 L 97.060745,163.63855 L 47.939255,163.63855 L 47.939255,128.58707 z\"\n \
     id=\"path2608\"\n \
     style=\"fill:url(#linearGradient3388);fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1.34000003;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 62.115,160.18281 L 62.115,132.04281 L 76.185,132.04281 L 82.885,139.41281 L 82.885,160.18281 L 62.115,160.18281 z\"\n \
     id=\"path3199\"\n \
     style=\"fill:#ffffff;fill-opacity:1;fill-rule:evenodd;stroke:#00000f;stroke-width:2.34500003;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:0.94117647\" />\n \
  <path\n \
     d=\"M 67.6425,148.79281 C 77.3575,148.79281 77.3575,148.79281 77.3575,148.79281\"\n \
     id=\"path2611\"\n \
     style=\"fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.34499979;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 67.6425,152.81281 C 77.3575,152.81281 77.3575,152.81281 77.3575,152.81281\"\n \
     id=\"path3165\"\n \
     style=\"fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.34499979;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 67.6425,144.77281 C 77.3575,144.77281 77.3575,144.77281 77.3575,144.77281\"\n \
     id=\"path3167\"\n \
     style=\"fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.34499979;stroke-linecap:square;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 75.3475,132.54531 L 75.3475,139.41281 L 81.7125,139.41281\"\n \
     id=\"path2615\"\n \
     style=\"fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:2.34500003;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <path\n \
     d=\"M 48.004895,81.702594 L 96.995105,81.702594 L 96.995105,116.70301 L 48.004895,116.70301 L 48.004895,81.702594 z\"\n \
     id=\"path2688\"\n \
     style=\"fill:url(#linearGradient3372);fill-opacity:1;fill-rule:nonzero;stroke:#c0a000;stroke-width:1.17957962;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" />\n \
  <g\n \
     transform=\"matrix(0.67,0,0,0.67,54.118645,80.777134)\"\n \
     id=\"g2758\"\n \
     style=\"display:inline\">\n \
    <g\n \
       id=\"g2760\">\n \
      <polygon\n \
         points=\"10.932,6.088 31.874,6.088 43.818,18.027 43.818,48.914 10.932,48.914 10.932,6.088 \"\n \
         id=\"polygon2762\"\n \
         style=\"fill:#ffffff;stroke:#010101;stroke-width:3.5\" />\n \
      <polyline\n \
         style=\"fill:none;stroke:#010101;stroke-width:3.5\"\n \
         points=\"43.818,18.027 31.874,18.027 31.874,6.088    \"\n \
         id=\"polyline2764\" />\n \
    </g>\n \
  </g>\n \
  <path\n \
     d=\"M 73.096395,107.37412 C 72.754025,106.39793 70.945695,106.65521 70.141695,107.32722 C 68.533695,108.67325 69.857615,110.27254 71.698775,109.52281 C 72.746655,109.09535 73.438095,108.35165 73.096395,107.37412 z\"\n \
     id=\"path2766\"\n \
     style=\"fill:#010101;stroke:#010101;stroke-width:2.34500003;display:inline\" />\n \
  <line\n \
     style=\"fill:none;stroke:#010101;stroke-width:1.50750005;display:inline\"\n \
     display=\"inline\"\n \
     x1=\"73.509117\"\n \
     x2=\"73.509117\"\n \
     y1=\"107.44715\"\n \
     y2=\"98.845024\"\n \
     id=\"line2768\" />\n \
  <polygon\n \
     points=\"35.047,25.036 27.838,28.595 27.838,24.728 35.047,21.166 35.047,25.036 \"\n \
     transform=\"matrix(0.67,0,0,0.67,54.118645,80.777134)\"\n \
     id=\"polygon2770\"\n \
     style=\"fill:#010101;display:inline\" />\n \
</svg>"

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
    FILE.close()
    return

if __name__ == "__main__":
    main()

