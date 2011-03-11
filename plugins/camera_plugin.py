#!/usr/bin/env python
#Copyright (c) 2011 Walter Bender
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gst
import gtk
from fcntl import ioctl

from gettext import gettext as _

from lib.camera.tacamera import Camera
from lib.camera.v4l2 import v4l2_control, V4L2_CID_AUTOGAIN, VIDIOC_G_CTRL, \
 VIDIOC_S_CTRL

from plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import media_blocks_dictionary, primitive_dictionary
from TurtleArt.tautils import get_path, debug_output

import logging
_logger = logging.getLogger('turtleart-activity camera plugin')


class Camera_plugin(Plugin):

    def __init__(self, parent):
        self._parent = parent
        self._status = False

        v4l2src = gst.element_factory_make('v4l2src')
        if v4l2src.props.device_name is not None:

            if self._parent.running_sugar:
                self._imagepath = get_path(self._parent.activity,
                                          'data/turtlepic.png')
            else:
                self._imagepath = '/tmp/turtlepic.png'
            self._camera = Camera(self._imagepath)

            self._status = True

    def setup(self):
        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'))

        # set up camera-specific blocks
        if self._status:
            primitive_dictionary['luminance'] = self.prim_read_camera
            palette.add_block('luminance',
                              style='box-style',
                              label=_('brightness'),
                              help_string=_('light level detected by camera'),
                              value_block=True,
                              prim_name='luminance')
            self._parent.lc.def_prim('luminance', 0,
                lambda self: primitive_dictionary['luminance'](True))

            # Depreciated block
            primitive_dictionary['read_camera'] = self.prim_read_camera
            palette.add_block('read_camera',
                              hidden=True,
                              style='box-style',
                              label=_('brightness'),
                              help_string=_('Average RGB color from camera \
is pushed to the stack'),
                              value_block=True,
                              prim_name='luminance')
            self._parent.lc.def_prim('read_camera', 0,
                lambda self: primitive_dictionary['read_camera'](True))

            media_blocks_dictionary['camera'] = self.prim_take_picture
            palette.add_block('camera',
                              style='box-style-media',
                              label=' ',
                              default='CAMERA',
                              help_string=_('camera output'),
                              content_block=True)

    def stop(self):
        # This gets called by the stop button
        if self._status:
            self._camera.stop_camera_input()

    def _status_report(self):
        debug_output('Reporting camera status: %s' % (str(self._status)))
        return self._status

    # Block primitives used in talogo

    def prim_take_picture(self):
        if self._status:
            ''' method called by media block '''
            self._camera.save_camera_input_to_file()
            self._camera.stop_camera_input()
            self._parent.lc.filepath = self._imagepath

    def prim_read_camera(self, luminance_only=False):
        """ Read average pixel from camera and push b, g, r to the stack """
        pixbuf = None
        array = None
        w, h = self._parent.lc._w(), self._parent.lc._h()
        if w > 0 and h > 0 and self._status:
            try:
                self._video_capture_device = open('/dev/video0', 'rw')
            except:
                self._video_capture_device = None
                _logger.debug('video capture device not available')

            if self._video_capture_device is not None:
                self._ag_control = v4l2_control(V4L2_CID_AUTOGAIN)
                try:
                    ioctl(self._video_capture_device, VIDIOC_G_CTRL,
                          self._ag_control)
                    self._ag_control.value = 0  # disable AUTOGAIN
                    ioctl(self._video_capture_device, VIDIOC_S_CTRL,
                          self._ag_control)
                except:
                    _logger.debug('AUTOGAIN control not available')
                    pass

            if self._video_capture_device is not None:
                self._video_capture_device.close()

            self._camera.save_camera_input_to_file()
            self._camera.stop_camera_input()
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self._imagepath,
                                                          w, h)
            try:
                array = pixbuf.get_pixels()
            except:
                array = None

        if array is not None:
            length = len(array) / 3
            r, g, b, i = 0, 0, 0, 0
            for j in range(length):
                r += ord(array[i])
                i += 1
                g += ord(array[i])
                i += 1
                b += ord(array[i])
                i += 1
            if luminance_only:
                lum = int((r * 0.3 + g * 0.6 + b * 0.1) / length)
                self._parent.lc.update_label_value('luminance', lum)
                return lum
            else:
                self._parent.lc.heap.append(int((b / length)))
                self._parent.lc.heap.append(int((g / length)))
                self._parent.lc.heap.append(int((r / length)))
        else:
            if luminance_only:
                return -1
            else:
                self._parent.lc.heap.append(-1)
                self._parent.lc.heap.append(-1)
                self._parent.lc.heap.append(-1)
