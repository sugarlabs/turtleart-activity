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

    myname = "sound"
    mystring1 = "sound"
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
   xmlns:dc=\"http://purl.org/dc/elements/1.1/\" \n \
   xmlns:cc=\"http://creativecommons.org/ns#\" \n \
   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" \n \
   xmlns:svg=\"http://www.w3.org/2000/svg\" \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\" \n \
   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\" \n \
   version=\"1.0\" \n \
   width=\"137\" \n \
   height=\"55\" \n \
   id=\"svg2\" \n \
   sodipodi:version=\"0.32\" \n \
   inkscape:version=\"0.46\" \n \
   sodipodi:docname=\"template5.svg\" \n \
   inkscape:output_extension=\"org.inkscape.output.svg.inkscape\"> \n \
  <metadata \n \
     id=\"metadata36\"> \n \
    <rdf:RDF> \n \
      <cc:Work \n \
         rdf:about=\"\"> \n \
        <dc:format>image/svg+xml</dc:format> \n \
        <dc:type \n \
           rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" /> \n \
      </cc:Work> \n \
    </rdf:RDF> \n \
  </metadata> \n \
  <sodipodi:namedview \n \
     inkscape:window-height=\"975\" \n \
     inkscape:window-width=\"1680\" \n \
     inkscape:pageshadow=\"2\" \n \
     inkscape:pageopacity=\"0.0\" \n \
     guidetolerance=\"10.0\" \n \
     gridtolerance=\"10.0\" \n \
     objecttolerance=\"10.0\" \n \
     borderopacity=\"1.0\" \n \
     bordercolor=\"#666666\" \n \
     pagecolor=\"#ffffff\" \n \
     id=\"base\" \n \
     showgrid=\"false\" \n \
     inkscape:zoom=\"3.9708029\" \n \
     inkscape:cx=\"36.894301\" \n \
     inkscape:cy=\"27.5\" \n \
     inkscape:window-x=\"0\" \n \
     inkscape:window-y=\"25\" \n \
     inkscape:current-layer=\"svg2\" /> \n \
  <defs \n \
     id=\"defs5\"> \n \
    <inkscape:perspective \n \
       sodipodi:type=\"inkscape:persp3d\" \n \
       inkscape:vp_x=\"0 : 27.5 : 1\" \n \
       inkscape:vp_y=\"0 : 1000 : 0\" \n \
       inkscape:vp_z=\"137 : 27.5 : 1\" \n \
       inkscape:persp3d-origin=\"68.5 : 18.333333 : 1\" \n \
       id=\"perspective38\" /> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         id=\"stop3168\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3170\" \n \
         style=\"stop-color:#ffff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0.94254935\" \n \
       y1=\"-31.669659\" \n \
       x2=\"104.37702\" \n \
       y2=\"20.434471\" \n \
       id=\"linearGradient3172\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.7083638,0,0,1.0012565,0.1338084,32.632067)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient4342\"> \n \
      <stop \n \
         id=\"stop3259\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop4345\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"0\" \n \
       x2=\"104\" \n \
       y2=\"21\" \n \
       id=\"linearGradient4340\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(1.0139238,0,0,1.0946487,31.741439,7.7561892)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"19.625\" \n \
       x2=\"320.75\" \n \
       y2=\"19.625\" \n \
       id=\"linearGradient3170\" \n \
       xlink:href=\"#linearGradient3164\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient3164\"> \n \
      <stop \n \
         id=\"stop3166\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop4336\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:0\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"66.800423\" \n \
       y1=\"23.707363\" \n \
       x2=\"203.4543\" \n \
       y2=\"23.237999\" \n \
       id=\"linearGradient4362\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.9988658,0,0,1.0058014,-66.475849,-58.253309)\" /> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient4488\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient4482\"> \n \
      <stop \n \
         id=\"stop4484\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop4486\" \n \
         style=\"stop-color:#ff00ff;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient2512\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2506\"> \n \
      <stop \n \
         id=\"stop2508\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2510\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       id=\"linearGradient3383\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
    <linearGradient \n \
       id=\"linearGradient3377\"> \n \
      <stop \n \
         id=\"stop3379\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop3381\" \n \
         style=\"stop-color:#00ff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       x1=\"0.94254935\" \n \
       y1=\"-31.669659\" \n \
       x2=\"94.577461\" \n \
       y2=\"20.434471\" \n \
       id=\"linearGradient2541\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.7750554,0,0,0.9997979,0.8784441,32.623865)\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2535\"> \n \
      <stop \n \
         id=\"stop2537\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1\" \n \
         offset=\"0\" /> \n \
      <stop \n \
         id=\"stop2539\" \n \
         style=\"stop-color:#ffff00;stop-opacity:1\" \n \
         offset=\"1\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       y2=\"22\" \n \
       x2=\"74\" \n \
       y1=\"22\" \n \
       x1=\"0\" \n \
       id=\"linearGradient2529\" \n \
       xlink:href=\"#linearGradient3166\" /> \n \
    <linearGradient \n \
       id=\"linearGradient2523\"> \n \
      <stop \n \
         id=\"stop2525\" \n \
         offset=\"0\" \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" /> \n \
      <stop \n \
         id=\"stop2527\" \n \
         offset=\"1\" \n \
         style=\"stop-color:#ffff00;stop-opacity:1;\" /> \n \
    </linearGradient> \n \
    <inkscape:perspective \n \
       id=\"perspective2520\" \n \
       inkscape:persp3d-origin=\"43.5 : 20 : 1\" \n \
       inkscape:vp_z=\"87 : 30 : 1\" \n \
       inkscape:vp_y=\"0 : 1000 : 0\" \n \
       inkscape:vp_x=\"0 : 30 : 1\" \n \
       sodipodi:type=\"inkscape:persp3d\" /> \n \
    <linearGradient \n \
       inkscape:collect=\"always\" \n \
       xlink:href=\"#linearGradient3166\" \n \
       id=\"linearGradient2543\" \n \
       gradientUnits=\"userSpaceOnUse\" \n \
       gradientTransform=\"matrix(0.7083638,0,0,1.0012565,-21.252221,77.527288)\" \n \
       x1=\"0.94254935\" \n \
       y1=\"-31.669659\" \n \
       x2=\"104.37702\" \n \
       y2=\"20.434471\" /> \n \
  </defs> \n \
  <path \n \
     d=\"M 63.5,0.75 L 47.75,0.75 L 47.75,4.75 L 25.75,4.75 L 25.75,0.75 L 10,0.75 C 10,0.75 6.1158487,1.358664 4.75,2.75 C 3.665741,3.85449 1,6.75 1,6.75 L 1,43.99 C 1,43.99 1.6401315,47.31861 2.4999613,47.995 C 3.3305948,48.64842 6.999845,50.25 6.999845,50.25 L 27,50.25 L 27,54 L 47,54 L 47,50.25 L 126.99673,50.25 L 127,38.75 L 136,38.75 L 136,33.25 L 127,33.25 L 127,24.25 L 136,24.25 L 136,18.75 L 127,18.75 L 127,6.75 L 69,6.75 L 66.463507,2.75 L 63.5,0.75 z\" \n \
     id=\"path2480\" \n \
     style=\"opacity:1;fill:url(#linearGradient4362);fill-opacity:1;fill-rule:evenodd;stroke:#c0a000;stroke-width:2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\" /> \n \
  <text \n \
     style=\"font-size:18px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans\" \n \
     id=\"text2509\" \n \
     x=\"31.82959\" \n \
     y=\"7.2104545\"> \n \
    <tspan \n \
       x=\"68.82959\" \n \
       y=\"34.210449\" \n \
       style=\"font-size:18px\" \n \
       id=\"tspan2511\">"

    data1 = \
"</tspan> \n \
  </text> \n \
</svg> \n "


    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(_(mystring1).encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()
