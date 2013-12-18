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
import gobject

from TurtleArt.tautils import debug_output


class Camera():
    ''' Sets up a pipe from the camera to a pixbuf and emits a signal
    when the image is ready. '''

    def __init__(self, device='/dev/video0'):
        ''' Prepare camera pipeline to pixbuf and signal watch '''
        self.pipe = gst.Pipeline('pipeline')
        v4l2src = gst.element_factory_make('v4l2src', None)
        v4l2src.props.device = device
        self.pipe.add(v4l2src)
        ffmpegcolorspace = gst.element_factory_make('ffmpegcolorspace', None)
        self.pipe.add(ffmpegcolorspace)
        gdkpixbufsink = gst.element_factory_make('gdkpixbufsink', None)
        self.pipe.add(gdkpixbufsink)
        gst.element_link_many(v4l2src, ffmpegcolorspace, gdkpixbufsink)
        if self.pipe is not None:
            self.bus = self.pipe.get_bus()
            self.bus.add_signal_watch()
            self.bus.connect('message', self._on_message)
            status = True
        else:
            status = False

    def _on_message(self, bus, message):
        ''' We get a message if a pixbuf is available '''
        if message.structure is not None:
            if message.structure.get_name() == 'pixbuf':
                self.pixbuf = message.structure['pixbuf']
                self.image_ready = True

    def start_camera_input(self):
        ''' Start grabbing '''
        self.pixbuf = None
        self.image_ready = False
        self.pipe.set_state(gst.STATE_PLAYING)
        while not self.image_ready:
            self.bus.poll(gst.MESSAGE_ANY, -1)

    def stop_camera_input(self):
        ''' Stop grabbing '''
        self.pipe.set_state(gst.STATE_NULL)
