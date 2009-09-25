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

import tawindow
import talogo
from sugar.activity import activity
from sugar.datastore import datastore
import os.path
import subprocess
from talogo import get_pixbuf_from_journal
from tahoverhelp import *
from gettext import gettext as _

def save_html(self, tw, embed_flag=True):

    try:
        datapath = os.path.join(activity.get_activity_root(), "instance")
    except:
        # early versions of Sugar (656) didn't support get_activity_root()
        datapath = os.path.join( \
            os.environ['HOME'], \
            ".sugar/default/org.laptop.TurtleArtActivity/instance")

    # dictionary defines the html wrappers around template elements
    # start of block, end of block
    html_glue = {
        'doctype': ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 \
Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">\n", ""),
        'html': ("<http>\n", "</http>\n"),
        'head': ("<head>\n<!-- Created by Turtle Art -->\n", \
             "</head>\n"),
        'meta': ("<meta http-equiv=\"content-type\" content=\"text/html; \
charset=UTF-8\">\n", ""),
        'title': ("<title>", "</title>\n"),
        'style': ("<style type=\"text/css\">\n<!--\n","-->\n</style>\n"),
        'body': ("<body>\n", "\n</body>\n"),
        'div': ("<div>\n", "</div>\n"),
        'slide': ("\n<a name=\"slide", "\"></a>\n"),
        'h1': ("<h1>", "</h1>\n"),
        'table': ("<table cellpadding=\"10\">\n", "</table>\n"),
        'tr': ("<tr>\n", "</tr>\n"),
        'td': ("<td valign=\"top\" width=\"400\" height=\"300\">\n", \
             "\n</td>\n"),
        'img': ("<img width=\"400\" height=\"300\" alt=\"Image\" src=\"image",\
             ".png\" />\n"),
        'img2': ("<img alt=\"Image\" src=\"image", ".png\" />\n"),
        'ul': ("<ul>\n", "</ul>\n"),
        'li': ("<li>", "</li>\n") }

    if embed_flag == True:
        # store images in-line as base64
        html_glue['img'] = ("<img width=\"400\" height=\"300\" alt=\"Image\" \
src=\"data:image/png;base64,\n", " \"/>\n")
        html_glue['img2'] = ("<img alt=\"Image\" \
src=\"data:image/png;base64,\n", " \"/>\n")

    bs = tawindow.blocks(tw)
    code = ""
    imagecount = 0
    slidecount = 0
    for b in bs:
         this_stack = ""
         data = walk_stack(self, tw, b)
         show = 0
         onepic = 0
         twopic = 0
         fourpic = 0
         sevenbullets = 0
         title = 0
         picture = 0
         for d in data:
             if type(d) is float:
                 continue
             else:
                 # transalate some Turtle Art blocks into HTML
                 #     show and template blocks
                 # ignores most turtle graphics
                 if d == "show":
                     show = 1
                 elif d == "container":
                     show = 2
                 elif show > 0:
                     if show == 1:
                         try: # is it media or a string?
                             tmp = d[0:8]
                         except:
                             tmp = ""
                         if tmp == '#smedia_': # show media
                             show = 2
                         else:  # show a string
                             this_stack += d[2:]
                             show = 0
                     if show == 2:
                         # show an image
                         if d[8:] != None:
                             try:
                                 dsobject = datastore.get(d[8:])
                                 pixbuf = \
                                     get_pixbuf_from_journal(dsobject,400,300)
                             except:
                                 pixbuf = None
                             if pixbuf != None:
                                 filename = os.path.join(datapath, 'image' + \
                                            str(imagecount) + ".png")
                                 pixbuf.save(filename, "png")
                                 # if the embed flag is True
                                 # embed base64 into the html
                                 if embed_flag == True:
                                     base64 = \
                                         os.path.join(datapath, 'base64tmp')
                                     cmd = "base64 <" + filename + " >" + base64
                                     subprocess.check_call(cmd, shell=True)
                                     f = open( base64, 'r')
                                     imgdata = f.read()
                                     f.close()
                                 tmp = html_glue['img2'][0]
                                 if embed_flag == True:
                                     tmp = tmp + imgdata
                                 else:
                                     tmp = tmp + str(imagecount)
                                     imagecount += 1
                                 tmp = tmp + html_glue['img2'][1]
                                 this_stack += tmp
                         show = 0
                 elif d == "tp1" or d == 'tp8':
                     onepic = 1
                 elif d == "tp2" or d == 'tp6':
                     twopic = 1
                 elif d == "tp7":
                     fourpic = 1
                 elif d == "tp3":
                     sevenbullets = 8
                 elif sevenbullets > 0:
                     if sevenbullets == 8:
                         tmp = html_glue['slide'][0] + str(slidecount) +\
                         html_glue['slide'][1] + \
                         html_glue['div'][0] + html_glue['h1'][0] + \
                         d[2:] + html_glue['h1'][1] + html_glue['ul'][0]
                     elif d[2:] != "":
                         tmp = html_glue['li'][0] + d[2:] + html_glue['li'][1]
                     this_stack += tmp
                     tmp = ""
                     sevenbullets -= 1
                     if sevenbullets == 0:
                         this_stack += html_glue['ul'][1]
                 elif onepic == 1 or twopic == 1 or fourpic == 1:
                     tmp = html_glue['slide'][0] + str(slidecount) + \
                         html_glue['slide'][1] + \
                         html_glue['div'][0] + html_glue['h1'][0] + d[2:] + \
                         html_glue['h1'][1] + html_glue['table'][0]
                     this_stack += tmp
                     if onepic > 0: onepic += 1
                     elif twopic > 0: twopic += 1
                     elif fourpic > 0: fourpic += 1
                     slidecount += 1
                 elif onepic > 1 or twopic > 1 or fourpic > 1:
                     # Need filename to copy it into instance directory
                     # if it is not an image, save the preview 
                     # save the description too.
                     if d[8:] != None:
                         try:
                             dsobject = datastore.get(d[8:])
                             pixbuf = get_pixbuf_from_journal(dsobject,400,300)
                         except:
                             pixbuf = None
                         if pixbuf != None:
                             filename = os.path.join(datapath, 'image' + \
                                 str(imagecount) + ".png")
                             pixbuf.save(filename, "png")
                             # if the embed flag is True
                             # embed base64 into the html
                             if embed_flag == True:
                                 base64 = os.path.join(datapath, 'base64tmp')
                                 cmd = "base64 <" + filename + " >" + base64
                                 subprocess.check_call(cmd, shell=True)
                                 f = open( base64, 'r')
                                 imgdata = f.read()
                                 f.close()
                         if onepic == 2 or twopic == 2 or twopic == 4 or\
                             fourpic == 2 or fourpic == 4:
                             tmp = html_glue['tr'][0]
                         else:
                             tmp = ""
                         if pixbuf != None:
                             tmp = tmp + html_glue['td'][0] + \
                                 html_glue['img'][0]
                             if embed_flag == True:
                                 tmp = tmp + imgdata
                             else:
                                 tmp = tmp + str(imagecount)
                             tmp = tmp + html_glue['img'][1] + \
                                 html_glue['td'][1]
                         if fourpic == 0:
                             try:
                                 description = dsobject.metadata['description']
                             except:
                                 description = ""
                             tmp = tmp + html_glue['td'][0] + description + \
                                 html_glue['td'][1]
                         if onepic == 2 or twopic == 3 or fourpic == 3 or \
                             fourpic == 5:
                             tmp = tmp + html_glue['tr'][1]
                         imagecount += 1
                         this_stack += tmp
                     if onepic > 1:
                         this_stack += html_glue['table'][1] + \
                             html_glue['div'][1] 
                         onepic = 0
                     elif twopic > 1:
                         if twopic == 3:
                             this_stack += html_glue['table'][1] + \
                                 html_glue['div'][1]
                             twopic = 0
                         else: twopic += 1
                     elif fourpic > 1: 
                         if fourpic == 5:
                             this_stack += html_glue['table'][1] + \
                                 html_glue['div'][1]
                             fourpic = 0
                         else: fourpic += 1
             this_stack += " "
         if len(data) > 0:
             code += this_stack

    """
    if no show or template blocks were present, we've got no slides,
    so save a screendump instead
    """
    if slidecount == 0:
        # save a screen dump instead
        filename = os.path.join(datapath, 'image.png')
        tawindow.save_pict(self.tw,filename)
        # if the embed flag is True
        # embed base64 into the html
        if embed_flag == True:
            base64 = os.path.join(datapath, 'base64tmp')
            cmd = "base64 <" + filename + " >" + base64
            subprocess.check_call(cmd, shell=True)
            f = open( base64, 'r')
            imgdata = f.read()
            f.close()
            code = html_glue['img'][0] + \
                   imgdata + \
                   html_glue['img'][1]
            for b in bs: # "show me the code"
                code = code + html_glue['div'][0]
                data = walk_stack(self, tw, b)
                for d in data:
                    if type(d) is not float:
                        if d[0:2] == "#s":
                            d = d[2:]
                        elif d[0:3] == "nop":
                            stack = {"nop" :"",\
                                     "nop1":"stack1",\
                                     "nop2":"stack2",\
                                     "nop3":"stack"}
                            d = stack[d]
                        # translate block name if it is in the dictionary
                        if d in blocks_dict:
                            d = _(blocks_dict[d])
                        else:
                            d = _(d)
                    code = code + str(d) + " "
                code = code + html_glue['div'][1]

    code = html_glue['doctype'][0] + \
           html_glue['html'][0] + \
           html_glue['head'][0] + \
           html_glue['meta'][0] + \
           html_glue['title'][0] + \
           _("Turtle Art") + \
           html_glue['title'][1] + \
           html_glue['style'][0] + \
           html_glue['style'][1] + \
           html_glue['head'][1] + \
           html_glue['body'][0] + \
           code + \
           html_glue['body'][1] + \
           html_glue['html'][1]
    return code

def walk_stack(self, tw, spr):
    top = tawindow.find_top_block(spr)
    if spr == top:
        # only walk the stack if the block is the top block
        return talogo.run_blocks(tw.lc, top, tawindow.blocks(tw), False)
    else:
        # not top of stack, then return empty list
        return []

