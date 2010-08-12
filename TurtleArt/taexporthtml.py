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
from tautils import data_to_string, save_picture, image_to_base64
from gettext import gettext as _
from cgi import escape

def save_html(self, tw, embed_flag=True):
    """ Either: Save canvas and code or pictures to HTML """
    self.embed_images = embed_flag

    # A dictionary to define the HTML wrappers around template elements
    self.html_glue = {
        'doctype': "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 " + \
             "Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">\n",
        'html': ("<html>\n", "</html>\n"),
        'html_svg': ("<html xmlns=\"http://www.w3.org/1999/xhtml\">\n",
                     "</html>\n"),
        'head': ("<head>\n<!-- Created by Turtle Art -->\n", "</head>\n"),
        'meta': "<meta http-equiv=\"content-type\" content=\"text/html; " + \
                "charset=UTF-8\"/>\n",
        'title': ("<title>", "</title>\n"),
        'style': ("<style type=\"text/css\">\n<!--\n", "-->\n</style>\n"),
        'body': ("<body>\n", "\n</body>\n"),
        'div': ("<div>\n", "</div>\n"),
        'slide': ("\n<a name=\"slide", "\"></a>\n"),
        'h1': ("<h1>", "</h1>\n"),
        'table': ("<table cellpadding=\"10\">\n", "</table>\n"),
        'tr': ("<tr>\n", "</tr>\n"),
        'td': ("<td valign=\"top\" width=\"400\" height=\"300\">\n",
               "\n</td>\n"),
        'img': ("<img width=\"400\" height=\"300\" alt=\"Image\" " + \
                "src=\"file://", ".png\" />\n"),
        'img2': ("<img alt=\"Image\" src=\"image", ".png\" />\n"),
        'img3': ("<img alt=\"Image\" src=\"file://", "\" />\n"),
        'ul': ("<table>\n", "</table>\n"),
        'li': ("<tr><td>", "</td></tr>\n") }

    comment = "<!--\n\
<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\" [\n\
	<!ENTITY ns_svg \"http://www.w3.org/2000/svg\">\n\
	<!ENTITY ns_xlink \"http://www.w3.org/1999/xlink\">\n\
]>\n\
-->\n"
    if self.embed_images == True:
        self.html_glue['img'] = ("<img width=\"400\" height=\"300\" alt="+ \
                                 "\"Image\" src=\"data:image/png;base64,\n",
                                 " \"/>\n")
        self.html_glue['img2'] = ("<img alt=\"Image\" src=\"data:image/png;"+ \
                                  "base64,\n", " \"/>\n")

    """
    If there are saved_pictures, put them into a .html; otherwise, save a
    screendump and the turtle project code.
    """
    code = ""
    if len(tw.saved_pictures) > 0:
        for i, p in enumerate(tw.saved_pictures):
            code += self.html_glue['slide'][0] + str(i)
            code += self.html_glue['slide'][1] + \
                    self.html_glue['div'][0] + \
                    self.html_glue['h1'][0]
            if self.embed_images == True:
                f = open(p, "r")
                imgdata = f.read()
                f.close()
                if p.endswith(('.svg')):
                    tmp = imgdata
                else:
                    pixbuf = gtk.gdk.pixbuf_new_from_file(p)
                    imgdata = image_to_base64(pixbuf, tw.activity)
                    tmp =  self.html_glue['img2'][0]
                    tmp += imgdata
                    tmp += self.html_glue['img2'][1]
            else:
                if p.endswith(('.svg')):
                    f = open(p, "r")
                    imgdata = f.read()
                    f.close()
                    tmp = imgdata
                else:
                    tmp = self.html_glue['img3'][0]
                    tmp += p
                    tmp += self.html_glue['img3'][1]
            code += tmp + \
                    self.html_glue['h1'][1] + \
                    self.html_glue['div'][1]
    else:
        if self.embed_images == True:
            imgdata = image_to_base64(save_picture(self.tw.canvas), tw.activity)
        else:
            imgdata = os.path.join(self.tw.load_save_folder, 'image')
            self.tw.save_as_image(imgdata)
        code += (self.html_glue['img'][0] + imgdata + \
                 self.html_glue['img'][1])
        code += self.html_glue['div'][0]
        code += escape(data_to_string(tw.assemble_data_to_save(False, True)))
        code += self.html_glue['div'][1]

    if tw.running_sugar:
        title = _("Turtle Art") + " " + tw.activity.metadata['title']
    else:
        title = _("Turtle Art")

    header = self.html_glue['doctype'] + \
            self.html_glue['html'][0]
    style = self.html_glue['style'][0] + \
            self.html_glue['style'][1]
    if len(tw.saved_pictures) > 0:
        if tw.saved_pictures[0].endswith(('.svg')):
            header = self.html_glue['html_svg'][0]
            style = comment

    code = header + \
           self.html_glue['head'][0] + \
           self.html_glue['meta'] + \
           self.html_glue['title'][0] + \
           title + \
           self.html_glue['title'][1] + \
           style + \
           self.html_glue['head'][1] + \
           self.html_glue['body'][0] + \
           code + \
           self.html_glue['body'][1] + \
           self.html_glue['html'][1]
    return code
