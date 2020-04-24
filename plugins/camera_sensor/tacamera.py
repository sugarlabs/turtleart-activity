# -*- coding: utf-8 -*-
# Copyright (c) 2010, Walter Bender
# Copyright (c) 2010, Tony Forster

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

from gi.repository import Gst
Gst.init(None)


class Camera():
    ''' Sets up a pipe from the camera to a pixbuf and emits a signal
    when the image is ready. '''

    def __init__(self, device='/dev/video0'):
        ''' Prepare camera pipeline to pixbuf and signal watch '''
        self.pipe = Gst.Pipeline()
        v4l2src = Gst.ElementFactory.make('v4l2src', None)
        v4l2src.props.device = device
        self.pipe.add(v4l2src)
        videoconvert = Gst.ElementFactory.make('videoconvert', None)
        self.pipe.add(videoconvert)
        self.gdkpixbufsink = Gst.ElementFactory.make('gdkpixbufsink', None)
        self.pipe.add(self.gdkpixbufsink)
        v4l2src.link(videoconvert)
        videoconvert.link(self.gdkpixbufsink)
        if self.pipe is not None:
            self.bus = self.pipe.get_bus()
            self.bus.add_signal_watch()
            self.bus.connect('message', self._on_message)

    def _on_message(self, bus, message):
        ''' We get a message if a pixbuf is available '''
        if message.get_structure() is not None:
            if message.get_structure().get_name() == 'pixbuf':
                self.pixbuf = self.gdkpixbufsink.get_property("last-pixbuf")
                self.image_ready = True

    def start_camera_input(self):
        ''' Start grabbing '''
        self.pixbuf = None
        self.image_ready = False
        self.pipe.set_state(Gst.State.PLAYING)
        while not self.image_ready:
            self.bus.poll(Gst.MessageType.ANY, 1)

    def stop_camera_input(self):
        ''' Stop grabbing '''
        self.pipe.set_state(Gst.State.NULL)
