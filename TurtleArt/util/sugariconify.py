# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Copyright (C) 2008 Eben Eliason
# Copyright (C) 2013 Jorge Alberto Gómez López

#  This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import xml.dom.minidom
import getopt
import re
import os
import string

HELP = '''\nUsage: sugar-iconify.py [options] input.svg\n
Options:\n
 -c\t\tApply default color entities (#666666, #ffffff) to output
 -d directory\tThe preferred output directory
 -e\t\tDo not insert entities for strokes and fills
 -f hex\t\tHex value to replace with fill entity
 -g\t\tAutomatically accept guesses for stroke and fill entities
 -h\t\tDisplay this help message
 -i\t\tInsert "isolated stroke" entities
 -m\t\tMultiple export; export top level groups as separate icons
 -o\t\tOverwrite the input file; overridden by -m
 -p pattern\tOnly export icons whose name matches pattern; for use with -m
 -s hex\t\tHex value to replace with stroke entity
 -x\t\tOutput example SVGs, for previewing their appearance in Sugar;
   \t\tignored with -m
 -v\t\tverbose'''


class SugarIconify():

    def __init__(self, command_line=False):
        # Declare variables and constants
        self.default_stroke_color = '#666666'
        self.default_fill_color = '#ffffff'
        self.transparent_color = '#00000000'
        self.stroke_color = self.default_stroke_color
        self.fill_color = self.default_fill_color
        self._target_stroke = None
        self._target_fill = None
        self.stroke_entity = 'stroke_color'
        self.fill_entity = 'fill_color'
        self.iso_stroke_entity = 'iso_stroke_color'

        self.output_path = ''
        self.pattern = ''
        self.entities_passed = 0
        self.use_default_colors = False
        self.confirm_guess = True
        self.use_entities = True
        self.multiple = False
        self.verbose = False
        self.overwrite_input = False
        self.output_examples = False
        self.use_iso_strokes = False

        if command_line:
            self._parse_command_line()

    def usage(self):
        # Define help output
        print(HELP)

    def _parse_command_line(self):
        ''' Try to make sense of the command-line arguments. '''
        try:
            opts, arg = getopt.getopt(sys.argv[1:], 's:f:gcd:imp:oehvx',
                                      ['stroke=', 'fill=', 'guess', 'help',
                                       'overwrite', 'verbose'])
        except BaseException:
            self.usage()
            sys.exit(2)

        if len(arg) < 1:
            self.usage()
            sys.exit(2)

        # Interpret arguments
        for o, a in opts:
            if o in ['-s', '--stroke']:
                self.set_stroke_color(a)
            elif o in ['-f', '--fill']:
                self.set_fill_color(a)
            elif o in ['-g', '--guess']:
                self.set_confirm_guess(False)
            elif o == '-c':
                self.set_use_default_colors(True)
            elif o in ['-o', '--overwrite']:
                self.set_overwrite_input(True)
            elif o == '-d':
                self.set_output_path(a)
            elif o == '-e':
                self.set_use_entities(False)
            elif o in ['-v', 'verbose']:
                self.set_verbose(True)
            elif o == '-p':
                self.set_pattern(a)
            elif o in ['-h', '--help']:
                usage()
                sys.exit(2)
            elif o == '-m':
                self.set_multiple(True)
            elif o == '-x':
                self.set_output_examples(True)
            elif o == '-i':
                self.set_use_iso_strokes(True)

        self.iconify(arg[0])

    def rgb_to_hex(self, rgb_str):
        s = re.sub(r'.*rgb\(([^)]*).*', r'\1', rgb_str)
        percent_list = s.split(',')
        hex_str = '#'
        for value in percent_list:
            hex_str += self.percent_to_hex(value)
        return hex_str

    def percent_to_hex(self, num):
        number = float(num.strip()[:-1])
        decimal = (number * 255) / 100
        decimal = int(round(decimal, 0))
        hex_val = hex(decimal).split('x')[1]
        if len(hex_val) == 1:
            hex_val = '0' + hex_val
        return hex_val

    def set_stroke_color(self, s=None):
        if s is not None:
            if 'rgb' in s.lower():
                self.stroke_color = self.rgb_to_hex(s)
                self._target_stroke = s
            else:
                self.stroke_color = '#' + s.lstrip('#').lower()
            self.entities_passed += 1

    def set_fill_color(self, f=None):
        if f is not None:
            if 'rgb' in f.lower():
                self.fill_color = self.rgb_to_hex(f)
                self._target_fill = f
            else:
                self.fill_color = '#' + f.lstrip('#').lower()
            self.entities_passed += 1

    def set_confirm_guess(self, g=False):
        self.confirm_guess = g

    def set_use_default_colors(self, c=False):
        self.use_default_colors = c

    def set_overwrite_input(self, o=False):
        self.overwrite_input = o

    def set_output_path(self, d=None):
        if d is not None:
            self.output_path = d.rstrip('/') + '/'

    def set_use_entity(self, e=False):
        self.use_entities = e

    def set_verbose(self, v=False):
        self.verbose = v

    def set_pattern(self, p=None):
        if p is not None:
            self.pattern = p

    def set_multiple(self, m=False):
        self.multiple = m

    def set_output_examples(self, x=False):
        self.output_examples = x

    def set_use_iso_strokes(self, i=False):
        self.use_iso_strokes = i

    def iconify(self, file_path):
        # Isolate important parts of the input path
        self.svgfilepath = file_path
        self.svgdirpath, self.sep, self.svgfilename = \
            self.svgfilepath.rpartition('/')
        svgbasename = re.sub(r'(.*)\.([^.]+)', r'\1', self.svgfilename)

        # Load the SVG as text
        try:
            self.svgfile = open(self.svgfilepath, 'r')
        except BaseException:
            sys.exit('Error: Could not locate ' + self.svgfilepath)

        try:
            self.svgtext = self.svgfile.read()
            self.svgfile.close()
        except BaseException:
            self.svgfile.close()
            sys.exit('Error: Could not read ' + self.svgfilepath)

        # Determine the creator of the SVG (we only care about
        # Inkscape and Illustrator)
        self.creator = 'unknown'

        if re.search('illustrator', self.svgtext, re.I):
            self.creator = 'illustrator'
        elif re.search('inkscape', self.svgtext, re.I):
            self.creator = 'inkscape'

        if self.verbose:
            print('The self.creator of this svg is ' + self.creator + '.')

        # Hack the entities into the readonly DTD
        if self.use_entities:

            # Before replacing them, we read the stroke/fill values
            # out, should they have previously been defined, to prevent
            # needing to make guesses for them later
            self.stroke_match = re.search(r'stroke_color\s*\"([^"]*)\"',
                                          self.svgtext)
            self.fill_match = re.search(r'fill_color\s*\"([^"]*)\"',
                                        self.svgtext)

            if self.stroke_match is not None:
                self.stroke_color = self.stroke_match.group(1).lower()
                self.entities_passed += 1
            if self.fill_match is not None:
                self.fill_color = self.fill_match.group(1).lower()
                self.entities_passed += 1

            # Define the entities
            if self.fill_match and self.stroke_match:
                self.entities = '\t<!ENTITY ' + self.stroke_entity + ' "' + \
                    self.stroke_color + '">\n'
                self.entities += '\t<!ENTITY ' + self.fill_entity + ' "' + \
                                 self.fill_color + '">\n'
                if self.use_iso_strokes:
                    self.entities += '\t<!ENTITY ' + self.iso_stroke_entity + \
                                     ' "' + self.stroke_color + '">\n'
            else:
                self.entities = '\t<!ENTITY ' + self.stroke_entity + ' "' + \
                    self.default_stroke_color + '">\n'
                self.entities += '\t<!ENTITY ' + self.fill_entity + ' "' + \
                                 self.default_fill_color + '">\n'
                if self.use_iso_strokes:
                    self.entities += '\t<!ENTITY ' + self.iso_stroke_entity + \
                                     ' "' + self.default_stroke_color + '">\n'

            # For simplicity, we simply replace the entire entity
            # declaration block; this obviously would remove any other
            # custom self.entities declared within the SVG, but we
            # assume that's an extreme edge case

            self.svgtext, self.n = \
                re.subn(r'(<!DOCTYPE[^>\[]*)(\[[^\]]*\])*\>',
                        r'\1 \n[\n' + self.entities + ']>\n', self.svgtext)

            # Add a doctype if none already exists, adding the
            # appropriate self.entities as well
            if self.n == 0:
                self.svgtext, self.n = \
                    re.subn('<svg',
                            "<!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.1//EN' \
'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd' [\n" +
                            self.entities + "]>\n<svg", self.svgtext)
                if self.n == 0:
                    sys.exit('Error: Could not insert self.entities into DTD')

        # Convert self.entities to references
        self.stroke_entity = '&' + self.stroke_entity + ';'
        self.fill_entity = '&' + self.fill_entity + ';'

        # Create the SVG DOM
        try:
            self.svgxml = xml.dom.minidom.parseString(self.svgtext)
        except Exception as e:
            sys.exit('Error: Could not parse ' + self.svgfilename + str(e))

        # Extract top-level nodes
        self.i = 0
        self.svgindex = 0
        self.docindex = 0
        for element in self.svgxml.childNodes:
            if element.nodeType == 10:
                self.docindex = self.i
            elif element.localName == 'svg':
                self.svgindex = self.i
                break
            self.i += 1

        self.doctype = self.svgxml.childNodes[self.docindex]
        self.svg = self.svgxml.childNodes[self.svgindex]
        icons = self.svg.childNodes

        # Validate canvas size
        self.w = self.svg.getAttribute('width')
        self.h = self.svg.getAttribute('height')

        if self.w != '55px' or self.h != '55px':
            print('Warning: invalid canvas size (%s, %s); \
Should be (55px, 55px)' % (self.w, self.h))

        # Guess the entity values, if they aren't passed in
        if self.use_entities:
            print('entities_passed ==', self.entities_passed)

            if self.entities_passed < 2:
                self.stroke_color, self.fill_color = \
                    self.guessEntities(self.svg)

            if self.confirm_guess or self.verbose:
                print('\nentity definitions:')
                print('     self.stroke_entity = ' + self.stroke_color)
                print('     self.fill_entity = ' + self.fill_color)

            '''if self.entities_passed < 2:
                if self.confirm_guess:
                    response = raw_input('\nAre these self.entities correct? [y/n] ')
                    if response.lower() != 'y':
                        print 'Please run this script again, passing the proper colors with the -s and -f flags.'
                        sys.exit(1)'''

        # Define the HTML for preview output
        self.previewHTML = "\
        <!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\"\n\
        \t\"http://www.w3.org/TR/html4/strict.dtd\">\n\
        <html>\n\
        <head>\n\
        \t<meta http-equiv=\"Content-type\" content=\"text/html; charset=utf-8\">\n\
        \t<title>Sugar Icon Preview: ~~~</title>\n\
        \t<script type=\"text/javascript\" charset=\"utf-8\">\n\
        \t\tvar bordered = false;\n\
        \t\tvar bgcolor = \"#FFF\"\n\
        \n\
        \t\tfunction toggleIconBorder(reset)\n\
        \t\t{\n\
        \t\t\tif(!reset) bordered = !bordered;\n\
        \t\t\t\n\
        \t\t\tvar objects = document.getElementsByTagName('object')\n\
        \t\t\tfor(var i = 0; i < objects.length; i++)\n\
        \t\t\t{\n\
        \t\t\t\tif(bordered) objects[i].style.border = 'solid 1px gray';\n\
        \t\t\t\telse objects[i].style.border = 'solid 1px ' + bgcolor;\n\
        \t\t\t}\n\
        \t\t}\n\
        \t\tfunction setBackgroundColor(color)\n\
        \t\t{\n\
        \t\t\tbgcolor = color;\n\
        \t\t\tvar objects = document.getElementsByTagName('div');\n\
        \t\t\tfor(var i = 0; i < objects.length; i++)\n\
        \t\t\t\tif(objects[i].className == 'cell')\n\
        \t\t\t\t\tobjects[i].style.backgroundColor = color;\n\
        \t\t\t\n\
        \t\t\ttoggleIconBorder(true)\n\
        \t\t}\n\
        \t</script>\n\
        \t<style type=\"text/css\" media=\"screen\">\n\
        \t\thtml, body {\n\
        \t\t\tmargin: 0px;\n\
        \t\t\tborder: 0px;\n\
        \t\t\tbackground-color: white;\n\
        \t\t\t\n\
        \t\t\tfont: 14px Helvetica;\n\
        \t\t\tcolor: gray;\n\
        \t\t}\n\
        \t\t.cell {\n\
        \t\t\twidth: 57px;\n\
        \t\t\theight: 57px;\n\
        \t\t\tpadding: 8px;\n\
        \t\t\tborder: solid 1px gray;\n\
        \t\t}\n\
        \t\t.icon {\n\
        \t\t\tmargin: 0px;\n\
        \t\t\tpadding: 0px;\n\
        \t\t\tborder: solid 1px #FFF;\n\
        \t\t\twidth: 55px;\n\
        \t\t\theight: 55px;\n\
        \t\t}\n\
        \t\t#icons {\n\
        \t\t\tmargin-top: 30px;\n\
        \t\t}\n\
        \n\
        \t\t#icons > li {\n\
        \t\t\tdisplay: block;\n\
        \t\t\tmargin: 0px;\n\
        \t\t\tmargin-bottom: 20px;\n\
        \t\t}\n\
        \t\t#description {\n\
        \t\t\twidth: 300px;\n\
        \t\t\tposition: absolute;\n\
        \t\t\ttop: 0px;\n\
        \t\t\tleft: 200px;\n\
        \t\t\tborder-left: solid 1px gray;\n\
        \t\t\tmargin-top: 30px;\n\
        \t\t\tpadding-left: 30px;\n\
        \t\t\tfont-size: 11px;\n\
        \t\t}\n\
        \t\t#description ul {\n\
        \t\t\tmargin: 0px;\n\
        \t\t\tpadding: 0px;\n\
        \t\t\tdisplay: block;\n\
        \t\t\tlist-style: square;\n\
        \t\t}\n\
        \t\tli { margin-bottom: 10px; }\n\
        \t\ta, a:visited { color: gray; }\n\
        \t\ta:hover { color: black; }\n\
        \t</style>\n\
        </head>\n\
        <body>\n\
        \t\t<ul id='icons'>\n\
        \t\t<li><div class='cell'><object class='icon' id='stroke' data=\"~~~.stroke.self.svg\" type=\"image/self.svg+xml\"></object></div><br>stroke\n\
        \t\t<li><div class='cell'><object class='icon' id='fill' data=\"~~~.fill.self.svg\" type=\"image/self.svg+xml\"></object></div><br>fill\n\
        \t\t<li><div class='cell'><object class='icon' id='both' data=\"~~~.both.self.svg\" type=\"image/self.svg+xml\"></object></div><br>both\n\
        \t\t</ul>\n\
        \t\t<div id='description'>\n\
        \t\t\t<h3>Icon Validation</h3>\n\
        \t\t\t<ul>\n\
        \t\t\t\t<li>Ensure that your icons appear to be centered within their boxes.\n\
        \t\t\t\t\tIf they appear off-center or cropped, you may have created your icon on canvas other than the required 55px square.\n\
        \t\t\t\t\tClick to <a href='javascript:toggleIconBorder();'>toggle</a> the 55px canvas border.\n\
        \t\t\t\t<li>If your icon appears off-center but has the correct 55px canvas, it may simply have uneven visual balance.\n\
        \t\t\t\t\tThis means, though it may be technically centered, differences in the distribution of \"mass\" cause it to appear otherwise.  \n\
        \t\t\t\t\tTry shifting the icon slightly on your canvas, while ensuring that you don't accidentally exceed the 55px boundary.\n\
        \t\t\t\t<!--li>Click to see your icon on <a href=\"javascript:setBackgroundColor('#000');\">black</a>, \n\
        \t\t\t\t\t<a href=\"javascript:setBackgroundColor('#FFF');\">white</a>, <a href=\"javascript:setBackgroundColor('#282828');\">gray</a>.<!-->\n\
        \t\t\t\t<li>Ensure that the first two icons appear entirely in gray, and that all of the third icon is colored blue and green, with the latter being the fill color.\n\
        \t\t\t\t\tIf any fail to meet these requirements, your icon does not have proper stroke and/or fill self.entities defined.\n\
        \t\t\t\t\tInvestigate the <b>-s</b> and <b>-f</b> options of sugar-iconify, and be sure that your input self.svg doesn't have extra colors in its palette.\n\
        \t\t\t\t<li>Ensure that your icon reads clearly when viewed only as strokes.\n\
        \t\t\t\t\tThis visual style will be used to represent activities/objects which are inactive, or uninstantiated.\n\
        \t\t\t\t\tConsider applying outlining strokes to any filled shapes that do not already have them.\n\
        \t\t\t\t<li>Ensure that your icon reads clearly when viewed only as fills.\n\
        \t\t\t\t\tThis visual style will be used for representing activity types within other icons, such as invitations, transfers, and objects.  \n\
        \t\t\t\t\tIf you have strokes which are isolated from fills, neither outlining them nor sitting against a filled background, please \n\
        \t\t\t\t\tinvestigate the <b>-i</b> option of the sugar-iconify script.\n\
        \t\t\t</ul>\n\
        \t\t\t<i>For more information, please see the OLPC wiki page on <a href='http://wiki.laptop.org/go/Making_Sugar_Icons' target='_blank'>making sugar icons</a>.</i>\n\
        \t\t</div>\n\
        </body>\n\
        </html>\n\
        "

        # Finally, do the icon conversion and export
        if self.multiple:
            # Export each icon as a separate file by top level group
            n_icons_exported = 0
            n_warnings = 0
            for icon in icons:

                try:
                    # Skip whitespace and unnamed icons
                    if icon.localName == 'g' and icon.attributes:

                        icon_name = ''
                        try:
                            if self.creator == 'inkscape' and \
                               icon.attributes.getNamedItem('inkscape:label'):
                                icon_name = icon.attributes.getNamedItem(
                                    'inkscape:label').nodeValue
                            else:
                                icon_name = icon.attributes.getNamedItem(
                                    'id').nodeValue
                        except BaseException:
                            pass

                        # Skip the template layers
                        if not icon_name.startswith('_'):

                            # Skip non-matches
                            if self.pattern == '' or \
                               re.search(self.pattern, icon_name):

                                if self.verbose:
                                    print('\nExporting ' + icon_name + \
                                        '.self.svg...')
                                icon_xml = xml.dom.minidom.Document()

                                # Construct the self.svg
                                icon_xml.appendChild(doctype)
                                icon_xml.appendChild(self.svg.cloneNode(0))

                                icon_xml.childNodes[1].appendChild(icon)
                                icon_xml.childNodes[1].childNodes[
                                    0].setAttribute('display', 'block')

                                if self.use_entities:
                                    strokes_replaced, fills_replaced = \
                                        self.replaceEntities(
                                            icon_xml.childNodes[1])

                                    if not strokes_replaced and not fills_replaced:
                                        print('Warning: no entity replacements were made in %s' % icon_name)
                                    elif not strokes_replaced:
                                        print('Warning: no stroke entity replacements were made in %s' % icon_name)
                                    elif not fills_replaced:
                                        print('Warning: no fill entity replacements were made in %s' % icon_name)

                                    if not strokes_replaced or not fills_replaced:
                                        n_warnings += 1

                                # Write the file
                                try:
                                    f = open(self.output_path + icon_name +
                                             '.self.svg', 'w')
                                except BaseException:
                                    sys.exit(
                                        'Error: Could not locate directory ' +
                                        self.output_path)

                                try:
                                    # Had to hack here to remove the
                                    # automatic encoding of '&' by
                                    # toxml() in entity refs I'm sure
                                    # there is a way to prevent need
                                    # for this if I knew the XML DOM
                                    # better
                                    icon_svgtext = icon_xml.toxml()
                                    icon_svgtext = re.sub('&amp;', '&',
                                                          icon_svgtext)
                                    if not self.use_default_colors:
                                        icon_svgtext = re.sub(
                                            r'ENTITY self.stroke_color "[^"]*"',
                                            r'ENTITY self.stroke_color "' +
                                            self.stroke_color + '"',
                                            icon_svgtext)
                                        icon_svgtext = re.sub(
                                            r'ENTITY self.fill_color "[^"]*"',
                                            r'ENTITY self.fill_color "' +
                                            self.fill_color +
                                            '"',
                                            icon_svgtext)
                                    f.write(icon_svgtext)
                                    f.close()
                                except BaseException:
                                    sys.exit(
                                        'Error: Could not write file ' +
                                        icon_name +
                                        '.self.svg')

                                n_icons_exported += 1
                except BaseException:
                    # Catch any errors we may have missed, so the rest
                    # of the icons can export normally
                    if(icon_name):
                        print('Error: Could not export' + icon_name + \
                            '.self.svg')

            if self.verbose:
                if n_icons_exported == 1:
                    print('Successfully exported 1 icon')
                else:
                    print('Successfully exported %d icons' % n_icons_exported)

                if n_warnings == 1:
                    print('Warnings were reported for 1 icon')
                elif n_warnings > 1:
                    print('Warnings were reported for %d icons' % n_warnings)

        else:
            # Output a single converted icon
            if not self.overwrite_input:
                outfilename = re.sub(r'(.*\.)([^.]+)', r'\1sugar.\2',
                                     self.svgfilename)
                if self.verbose:
                    print('Exporting ' + outfilename + ' ...')
            else:
                outfilename = self.svgfilename
                if self.verbose:
                    print('Overwriting ' + outfilename + ' ...')

            # Remove the template layers
            for node in self.svg.childNodes:

                # Only check named nodes
                if node.localName == 'g' and node.attributes:
                    try:
                        if self.creator == 'inkscape' and \
                           node.attributes.getNamedItem('inkscape:label'):
                            node_name = node.attributes.getNamedItem(
                                'inkscape:label').nodeValue
                        else:
                            node_name = node.attributes.getNamedItem(
                                'id').nodeValue

                        if node_name.startswith('_'):
                            node.parentNode.removeChild(node)
                    except BaseException:
                        pass

            if self.use_entities:
                strokes_replaced, fills_replaced = \
                    self.replaceEntities(self.svgxml)
                if not strokes_replaced and not fills_replaced:
                    print('Warning: no entity replacements were made')
                elif not strokes_replaced:
                    print('Warning: no stroke entity replacements were made')
                elif not fills_replaced:
                    print('Warning: no fill entity replacements were made')

                if self.use_iso_strokes:
                    strokes_fixed = self.fix_isolated_strokes(self.svgxml)
                    if strokes_fixed > 0 and self.verbose:
                        print("%d isolated strokes fixed" % strokes_fixed)

            # Create the output file(s)
            if self.output_examples:

                example_path = self.output_path + \
                    re.sub(r'(.*\.)([^.]+)', r'\1preview',
                           self.svgfilename) + '/'
                try:
                    os.mkdir(example_path)
                except BaseException:
                    pass

                try:
                    f = open(example_path + 'preview.html', 'w')
                except BaseException:
                    print("Error: could not create HTML preview file")

                try:
                    f.write(re.sub(r'~~~', svgbasename, self.previewHTML))
                    f.close()
                except BaseException:
                    sys.exit('Error: could not write to HTML preview file')

                example_colors = [(self.default_stroke_color, '#FFFFFF',
                                   self.default_stroke_color),
                                  ('#FFFFFF', self.default_stroke_color,
                                   self.default_stroke_color),
                                  ('#0000AA', '#00DD00', '#0000AA')]
                example_filenames = [re.sub(r'(.*\.)([^.]+)', r'\1stroke.\2',
                                            self.svgfilename),
                                     re.sub(r'(.*\.)([^.]+)', r'\1fill.\2',
                                            self.svgfilename),
                                     re.sub(r'(.*\.)([^.]+)', r'\1both.\2',
                                            self.svgfilename)]

                icon_svgtext = self.svgxml.toxml()
                icon_svgtext = re.sub('&amp;', '&', icon_svgtext)

                for i in range(0, len(example_filenames)):
                    try:
                        f = open(example_path + example_filenames[i], 'w')
                    except BaseException:
                        sys.exit('Error: Could not save to ' + example_path +
                                 example_filenames[i])
                    try:
                        icon_svgtext = re.sub(
                            r'ENTITY self.stroke_color "[^"]*"',
                            r'ENTITY self.stroke_color "' +
                            example_colors[i][0] +
                            '"',
                            icon_svgtext)
                        icon_svgtext = re.sub(
                            r'ENTITY self.fill_color "[^"]*"',
                            r'ENTITY self.fill_color "' +
                            example_colors[i][1] +
                            '"',
                            icon_svgtext)
                        if self.use_iso_strokes:
                            icon_svgtext = re.sub(
                                r'ENTITY iso_stroke_color "[^"]*"',
                                r'ENTITY iso_stroke_color "' +
                                example_colors[i][2] +
                                '"',
                                icon_svgtext)
                        f.write(icon_svgtext)
                        f.close()
                    except BaseException:
                        sys.exit('Error: Could not write file ' +
                                 self.output_path + example_filenames[i])

            try:
                f = open(self.output_path + outfilename, 'w')
            except BaseException:
                sys.exit('Error: Could not save to ' + self.output_path +
                         outfilename)

            try:
                icon_svgtext = self.svgxml.toxml()
                icon_svgtext = re.sub('&amp;', '&', icon_svgtext)
                if not self.use_default_colors:
                    icon_svgtext = re.sub(
                        r'ENTITY self.stroke_color "[^"]*"',
                        r'ENTITY self.stroke_color "' +
                        self.stroke_color +
                        '"',
                        icon_svgtext)
                    icon_svgtext = re.sub(
                        r'ENTITY self.fill_color "[^"]*"',
                        r'ENTITY self.fill_color "' +
                        self.fill_color +
                        '"',
                        icon_svgtext)
                    if self.use_iso_strokes:
                        icon_svgtext = re.sub(
                            r'ENTITY iso_stroke_color "[^"]*"',
                            r'ENTITY iso_stroke_color "' +
                            self.stroke_color +
                            '"',
                            icon_svgtext)
                f.write(icon_svgtext)
                f.close()

            except BaseException:
                sys.exit('Error: Could not write file ' + self.output_path +
                         outfilename)

    # Define utility functions
    def getStroke(self, node):
        s = node.getAttribute('stroke')
        if s:
            return s.lower()
        else:
            if re.search(r'stroke:', node.getAttribute('style')):
                s = re.sub(
                    r'.*stroke:\s*(#*[^;]*).*',
                    r'\1',
                    node.getAttribute('style'))
                s2 = re.sub(
                    r'.*stroke:\s*rgb\(([^)]*).*',
                    r'\1',
                    node.getAttribute('style'))
                if 'rgb' not in s:
                    return s.lower()
                else:
                    percent_list = s2.split(',')
                    hex_str = '#'
                    for value in percent_list:
                        hex_str += self.percent_to_hex(value)
                    return hex_str
            else:
                return 'none'

    def setStroke(self, node, value):
        s = node.getAttribute('stroke')
        if s:
            node.setAttribute('stroke', value)
        else:
            s = re.sub(r'stroke:\s*[^;]*', 'stroke:' + value,
                       node.getAttribute('style'))
            node.setAttribute('style', s)

    def getFill(self, node):
        f = node.getAttribute('fill')
        if f:
            return f.lower()
        else:
            if re.search(r'fill:', node.getAttribute('style')):
                f = re.sub(r'.*fill:\s*(#*[^;]*).*', r'\1',
                           node.getAttribute('style'))
                f2 = re.sub(r'.*fill:\s*rgb\(([^)]*).*', r'\1',
                            node.getAttribute('style'))
                if 'rgb' not in f:
                    return f.lower()
                else:
                    percent_list = f2.split(',')
                    hex_str = '#'
                    for value in percent_list:
                        hex_str += self.percent_to_hex(value)
                    return hex_str
            else:
                return 'none'

    def setFill(self, node, value):
        f = node.getAttribute('fill')
        if f:
            node.setAttribute('fill', value)
        else:
            s = re.sub(r'fill:\s*[^;]*', 'fill:' + value,
                       node.getAttribute('style'))
            node.setAttribute('style', s)

    def replaceEntities(self, node, indent=''):

        strokes_replaced = 0
        fills_replaced = 0

        if node.localName:
            str = indent + node.localName

        if node.nodeType == 1:  # Only element nodes have attrs

            # Replace self.entities for matches
            if self.getStroke(node) == self.stroke_color:
                self.setStroke(node, self.stroke_entity)
                strokes_replaced += 1

            if self.getStroke(node) == self.fill_color:
                self.setStroke(node, self.fill_entity)
                strokes_replaced += 1

            if self.getFill(node) == self.fill_color:
                self.setFill(node, self.fill_entity)
                fills_replaced += 1

            if self.getFill(node) == self.stroke_color:
                self.setFill(node, self.stroke_entity)
                fills_replaced += 1

            str = str + " (" + self.getStroke(node) + ", " + \
                self.getFill(node) + ")"
            if self.verbose:
                print(str)

        # Recurse on DOM
        for n in node.childNodes:
            sr, fr = self.replaceEntities(n, indent + "   ")
            strokes_replaced += sr
            fills_replaced += fr

        # Return the number of replacements made
        return (strokes_replaced, fills_replaced)

    def fix_isolated_strokes(self, node):
        strokes_fixed = 0
        # Recurse on DOM
        last_n = None
        for n in node.childNodes:
            sf = self.fix_isolated_strokes(n)
            strokes_fixed += sf

        if node.nodeType == 1:  # Only element nodes have attrs

            # Find strokes with no associated fill
            if self.getStroke(node) != 'none' and self.getFill(node) == 'none':
                strokes_fixed += 1
                self.setStroke(node, "&iso_stroke_color;")

        # Return the number of strokes fixed
        return strokes_fixed

    # These functions attempt to guess the hex values for the stroke
    # and fill self.entities

    def getColorPairs(self, node, pairs=[]):
        if node.nodeType == 1:

            # Skip masks
            if node.localName == 'mask':
                return pairs

            node_name = ''
            try:
                if self.creator == 'inkscape' and \
                   node.attributes.getNamedItem('inkscape:label'):
                    node_name = node.attributes.getNamedItem(
                        'inkscape:label').nodeValue
                else:
                    node_name = node.attributes.getNamedItem('id').nodeValue
            except BaseException:
                pass

            # Skip the template layers
            if node_name.startswith('_'):
                return pairs

            pair = (self.getStroke(node), self.getFill(node))
            if pair[0] != pair[1]:
                pairs.append(pair)

        # Recurse on DOM
        for n in node.childNodes:
            self.getColorPairs(n, pairs)

        return pairs

    def guessEntities(self, node):
        guesses = self.getColorPairs(node)

        if self.stroke_color is not None:
            stroke_guess = self.stroke_color
        else:
            stroke_guess = 'none'

        if self.stroke_color is not None:
            fill_guess = self.fill_color
        else:
            fill_guess = 'none'

        for guess in guesses:
            if stroke_guess == 'none':
                stroke_guess = guess[0]
            if fill_guess == 'none' and stroke_guess != guess[1]:
                fill_guess = guess[1]
            if guess[0] == fill_guess and guess[1] != 'none':
                fill_guess = stroke_guess
                stroke_guess = guess[0]
                if fill_guess == 'none':
                    fill_guess = guess[1]

        return (stroke_guess, fill_guess)


if __name__ == '__main__':
    SugarIconify(command_line=True)
