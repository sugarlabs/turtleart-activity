# -*- coding: utf-8 -*-
# Copyright (c) 2013 Jorge Alberto Gómez López

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from .odf.opendocument import OpenDocumentPresentation
from .odf.style import Style, MasterPage, PageLayout, PageLayoutProperties
from .odf.draw import Page, Frame, Image


class TurtleODP:

    def __init__(self):
        self.doc = None
        self.path = None
        self.width = 0
        self.height = 0

    def create_presentation(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height
        # Create memory Open Document Presentation in memory
        self.doc = OpenDocumentPresentation()
        pagelayout = PageLayout(name='MyLayout')
        self.doc.automaticstyles.addElement(pagelayout)
        # Define the basic measures of a page of the presentation
        pagelayout.addElement(PageLayoutProperties(
            margin='0pt', pagewidth='%fpt' % width,
            pageheight='%fpt' % height, printorientation='landscape'))
        self.photostyle = Style(name='MyMaster-photo', family='presentation')
        self.doc.styles.addElement(self.photostyle)
        self.masterpage = MasterPage(name='MyMaster',
                                     pagelayoutname=pagelayout)
        self.doc.masterstyles.addElement(self.masterpage)

    def add_image(self, path):
        page = Page(masterpagename=self.masterpage)
        photoframe = Frame(
            stylename=self.photostyle, width='%fpt' % self.width,
            height='%fpt' % self.height, x='0pt', y='0pt')
        self.doc.presentation.addElement(page)
        page.addElement(photoframe)
        href = self.doc.addPicture(path)
        photoframe.addElement(Image(href=href))
        # print 'added image successfully'

    def save_presentation(self):
        # print self.path
        self.doc.save(self.path)
        # print 'presentation saved successfully'

    def get_output_path(self):
        return self.path
