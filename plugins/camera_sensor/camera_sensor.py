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
import os
from time import time

from gettext import gettext as _

from plugins.camera_sensor.tacamera import Camera
from plugins.camera_sensor.v4l2 import v4l2_control, V4L2_CID_AUTOGAIN, \
    VIDIOC_G_CTRL, VIDIOC_S_CTRL

from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import media_blocks_dictionary, primitive_dictionary
from TurtleArt.tautils import get_path, debug_output
from TurtleArt.taconstants import MEDIA_SHAPES, NO_IMPORT, SKIN_PATHS, \
    BLOCKS_WITH_SKIN


class Camera_sensor(Plugin):

    def __init__(self, parent):
        ''' Make sure there is a camera device '''
        self._parent = parent
        self._status = False
        self._ag_control = None
        self.camera = None

        v4l2src = gst.element_factory_make('v4l2src')
        if v4l2src.props.device_name is not None:
            self._status = True

    def setup(self):
        ''' Set up the palettes '''
        palette = make_palette('sensor',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of sensor blocks'))

        # set up camera-specific blocks
        primitive_dictionary['read_camera'] = self.prim_read_camera
        media_blocks_dictionary['camera'] = self.prim_take_picture

        SKIN_PATHS.append('plugins/camera_sensor/images')

        if self._status:
            palette.add_block('luminance',
                              style='box-style',
                              label=_('brightness'),
                              help_string=_('light level detected by camera'),
                              value_block=True,
                              prim_name='luminance')
            self._parent.lc.def_prim('luminance', 0,
                lambda self: primitive_dictionary['read_camera'](
                    luminance_only=True))

            # Depreciated block
            palette.add_block('read_camera',
                              hidden=True,
                              style='box-style',
                              label=_('brightness'),
                              help_string=_('Average RGB color from camera \
is pushed to the stack'),
                              value_block=True,
                              prim_name='read_camera')
            self._parent.lc.def_prim('read_camera', 0,
                lambda self: primitive_dictionary['read_camera']())

            palette.add_block('camera',
                              style='box-style-media',
                              label=' ',
                              default='CAMERA',
                              help_string=_('camera output'),
                              content_block=True)
        else:  # No camera, so blocks should do nothing
            palette.add_block('luminance',
                              hidden=True,
                              style='box-style',
                              label=_('brightness'),
                              help_string=\
                                  _('light level detected by camera'),
                              value_block=True,
                              prim_name='read_camera')
            self._parent.lc.def_prim('luminance', 0,
                lambda self: primitive_dictionary['read_camera'](
                    luminance_only=True))

            # Depreciated block
            palette.add_block('read_camera',
                              hidden=True,
                              style='box-style',
                              label=_('brightness'),
                              help_string=_('Average RGB color from camera \
is pushed to the stack'),
                              value_block=True,
                              prim_name='read_camera')
            self._parent.lc.def_prim('read_camera', 0,
                lambda self: primitive_dictionary['read_camera']())

            palette.add_block('camera',
                              hidden=True,
                              style='box-style-media',
                              label=' ',
                              default='CAMERA',
                              help_string=_('camera output'),
                              content_block=True)

        NO_IMPORT.append('camera')
        BLOCKS_WITH_SKIN.append('camera')
        MEDIA_SHAPES.append('camerasmall')
        MEDIA_SHAPES.append('cameraoff')

    def start(self):
        ''' Initialize the camera if there is an camera block in use '''
        if len(self._parent.block_list.get_similar_blocks('block',
            ['camera', 'read_camera', 'luminance'])) > 0:
            if self._status and self.camera is None:
                self.camera = Camera()

    def quit(self):
        ''' This gets called when the activity quits '''
        self._reset_the_camera()

    def stop(self):
        ''' This gets called by the stop button '''
        self._reset_the_camera()

    def clear(self):
        ''' This gets called by the clean button and erase button '''
        self._reset_the_camera()

    def _reset_the_camera(self):
        if self._status and self.camera is not None:
            self.camera.stop_camera_input()
            self._set_autogain(1)  # enable AUTOGAIN

    def _status_report(self):
        debug_output('Reporting camera status: %s' % (str(self._status)),
                     self._parent.running_sugar)
        return self._status

    # Block primitives used in talogo

    def prim_take_picture(self):
        ''' method called by media block '''
        self._set_autogain(1)  # enable AUTOGAIN
        self._get_pixbuf_from_camera()
        self._parent.lc.pixbuf = self.camera.pixbuf

    def prim_read_camera(self, luminance_only=False):
        """ Read average pixel from camera and push b, g, r to the stack """
        self.luminance_only = luminance_only
        if not self._status:
            if self.luminance_only:
                return -1
            else:
                self._parent.lc.heap.append(-1)
                self._parent.lc.heap.append(-1)
                self._parent.lc.heap.append(-1)
            return

        array = None
        self._set_autogain(0)  # disable AUTOGAIN
        self._get_pixbuf_from_camera()
        self.calc_luminance()
        if self.luminance_only:
            self._parent.lc.update_label_value('luminance', self.luminance)
            return self.luminance
        else:
            self._parent.lc.heap.append(self.b)
            self._parent.lc.heap.append(self.g)
            self._parent.lc.heap.append(self.r)

    def calc_luminance(self):
        array = self.camera.pixbuf.get_pixels()
        width = self.camera.pixbuf.get_width()
        height = self.camera.pixbuf.get_height()

        if array is not None:
            length = int(len(array) / 3)
            if length != width * height:
                debug_output('array length != width x height (%d != %dx%d)' % \
                                 (length, width, height),
                             self._parent.running_sugar)

            # Average the 100 pixels in the center of the screen
            r, g, b = 0, 0, 0
            row_offset = int((height / 2 - 5) * width * 3)
            column_offset = int(width / 2 - 5) * 3
            for y in range(10):
                i = row_offset + column_offset
                for x in range(10):
                    r += ord(array[i])
                    i += 1
                    g += ord(array[i])
                    i += 1
                    b += ord(array[i])
                    i += 1
                row_offset += width * 3
            if self.luminance_only:
                self.luminance = int((r * 0.3 + g * 0.6 + b * 0.1) / 100)
            else:
                self.r = int(r / 100)
                self.g = int(g / 100)
                self.b = int(b / 100)
        else:
            if self.luminance_only:
                self.luminance = -1
            else:
                self.r = -1
                self.g = -1
                self.b = -1

    def _set_autogain(self, state):
        ''' 0 is off; 1 is on '''
        if self._ag_control is not None and self._ag_control.value == state:
            return
        try:
            video_capture_device = open('/dev/video0', 'rw')
        except:
            video_capture_device = None
            debug_output('video capture device not available',
                         self._parent.running_sugar)
            return
        self._ag_control = v4l2_control(V4L2_CID_AUTOGAIN)
        try:
            ioctl(video_capture_device, VIDIOC_G_CTRL, self._ag_control)
            self._ag_control.value = state
            ioctl(video_capture_device, VIDIOC_S_CTRL, self._ag_control)
        except:
            pass
        video_capture_device.close()

    def _get_pixbuf_from_camera(self):
        ''' Regardless of how we get it, we want to return a pixbuf '''
        self._parent.lc.pixbuf = None
        if self._status:
            self.camera.start_camera_input()
