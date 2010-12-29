# -*- coding: utf-8 -*-
#Copyright (c) 2010, Walter Bender
#Copyright (c) 2010, Tony Forster

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

import gst, time

GST_PIPE = ['v4l2src', 'ffmpegcolorspace', 'pngenc']

class Camera():
    """ A class for representing the video camera """

    def __init__(self, imagepath):
       GST_PIPE.append('filesink location=%s' % imagepath)
       self.pipe = gst.parse_launch('!'.join(GST_PIPE))
       self.bus = self.pipe.get_bus()

    def save_camera_input_to_file(self):
        """ Grab a frame from the camera """
        self.pipe.set_state(gst.STATE_PLAYING)
        self.bus.poll(gst.MESSAGE_EOS, -1)

    def stop_camera_input(self):
        self.pipe.set_state(gst.STATE_NULL)

