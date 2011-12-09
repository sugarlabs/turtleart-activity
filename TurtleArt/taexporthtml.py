#Copyright (c) 2008-9, Walter Bender

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

import pygtk
pygtk.require('2.0')
import gtk
import os.path
from cgi import escape
from gettext import gettext as _

from tautils import data_to_string, save_picture, image_to_base64, get_path

# A dictionary to define the HTML wrappers around template elements
HTML_GLUE = {
    'doctype': '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 ' + \
        'Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n',
    'html': ('<html>\n', '</html>\n'),
    'html_svg': ('<html xmlns="http://www.w3.org/1999/xhtml">\n',
                 '</html>\n'),
    'head': ('<head>\n<!-- Created by Turtle Art -->\n', '</head>\n'),
    'meta': '<meta http-equiv="content-type" content="text/html; ' + \
        'charset=UTF-8"/>\n',
    'title': ('<title>', '</title>\n'),
    'style': ('<style type="text/css">\n<!--\n', '-->\n</style>\n'),
    'body': ('<body>\n', '\n</body>\n'),
    'div': ('<div>\n', '</div>\n'),
    'slide': ('\n<a name="slide', '"></a>\n'),
    'h1': ('<h1>', '</h1>\n'),
    'table': ('<table cellpadding="10\'>\n', '</table>\n'),
    'tr': ('<tr>\n', '</tr>\n'),
    'td': ('<td valign="top" width="400" height="300">\n',
           '\n</td>\n'),
    'img': ('<img width="400" height="300" alt="Image" ' + \
                'src="file://"', '".png" />\n'),
    'img2': ('<img alt="Image" src="image"', '".png" />\n'),
    'img3': ('<img alt="Image" src="file://"', '"" />\n'),
    'ul': ('<table>\n', '</table>\n'),
    'li': ('<tr><td>', '</td></tr>\n')}

COMMENT = '<!--\n\<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"' + \
    ' "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" [\n\
    <!ENTITY ns_svg "http://www.w3.org/2000/svg">\n\
    <!ENTITY ns_xlink "http://www.w3.org/1999/xlink">\n\
]>\n\
-->\n'


def save_html(self, tw, embed_flag=True):
    """ Either save the canvas and code or pictures to HTML """

    if embed_flag:
        HTML_GLUE['img'] = ('<img width="400" height="300" alt=' + \
                                 '"Image" src="data:image/png;base64,\n',
                                 '"/>\n')
        HTML_GLUE['img2'] = ('<img alt="Image" src="data:image/png;' + \
                                  'base64,\n', '"/>\n')

    """
    If there are saved_pictures, put them into a .html; otherwise,
    save a screendump and the turtle project code.
    """
    htmlcode = ''
    if len(tw.saved_pictures) > 0:
        # saved_picture list is a collection of tuples of either the
        # image_file or the containing dsobject and an SVG flag
        for i, (image, svg_flag) in enumerate(tw.saved_pictures):
            htmlcode += HTML_GLUE['slide'][0] + str(i)
            htmlcode += HTML_GLUE['slide'][1] + \
                    HTML_GLUE['div'][0] + \
                    HTML_GLUE['h1'][0]
            if tw.running_sugar:
                from sugar.datastore import datastore
                dobject = datastore.get(image)  # dsobject.object_id
                image_file = dobject.file_path
            else:
                image_file = image
            if embed_flag:
                f = open(image_file, 'r')
                imgdata = f.read()
                f.close()
                if svg_flag:
                    tmp = imgdata
                else:
                    imgdata = image_to_base64(
                        image_file, get_path(tw.activity, 'instance'))
                    tmp = HTML_GLUE['img2'][0]
                    tmp += imgdata
                    tmp += HTML_GLUE['img2'][1]
            else:
                if svg_flag:
                    f = open(image_file, 'r')
                    imgdata = f.read()
                    f.close()
                    tmp = imgdata
                else:
                    tmp = HTML_GLUE['img3'][0]
                    tmp += image_file
                    tmp += HTML_GLUE['img3'][1]
            htmlcode += tmp + \
                    HTML_GLUE['h1'][1] + \
                    HTML_GLUE['div'][1]
    else:
        if embed_flag:
            tmp_file = os.path.join(get_path(tw.activity, 'instance'),
                                   'tmpfile.png')
            save_picture(self.tw.canvas, tmp_file)
            imgdata = image_to_base64(tmp_file,
                                      get_path(tw.activity, 'instance'))
        else:
            imgdata = os.path.join(self.tw.load_save_folder, 'image')
            self.tw.save_as_image(imgdata)
        htmlcode += (HTML_GLUE['img'][0] + imgdata + \
                 HTML_GLUE['img'][1])
        htmlcode += HTML_GLUE['div'][0]
        htmlcode += escape(data_to_string(
                tw.assemble_data_to_save(False, True)))
        htmlcode += HTML_GLUE['div'][1]

    if tw.running_sugar:
        title = _('Turtle Art') + ' ' + tw.activity.metadata['title']
    else:
        title = _('Turtle Art')

    header = HTML_GLUE['doctype'] + \
            HTML_GLUE['html'][0]
    style = HTML_GLUE['style'][0] + \
            HTML_GLUE['style'][1]
    if len(tw.saved_pictures) > 0:
        if tw.saved_pictures[0][1]:
            header = HTML_GLUE['html_svg'][0]
            style = COMMENT

    return header + \
           HTML_GLUE['head'][0] + \
           HTML_GLUE['meta'] + \
           HTML_GLUE['title'][0] + \
           title + \
           HTML_GLUE['title'][1] + \
           style + \
           HTML_GLUE['head'][1] + \
           HTML_GLUE['body'][0] + \
           htmlcode + \
           HTML_GLUE['body'][1] + \
           HTML_GLUE['html'][1]
