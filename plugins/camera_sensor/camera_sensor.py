#!/usr/bin/env python
# Copyright (c) 2011, 2012 Walter Bender
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


from gi.repository import Gst

Gst.init(None)
from fcntl import ioctl
import os

from gettext import gettext as _

from plugins.camera_sensor.tacamera import Camera
from plugins.camera_sensor.v4l2 import v4l2_control, V4L2_CID_AUTOGAIN, \
    VIDIOC_G_CTRL, VIDIOC_S_CTRL

from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import media_blocks_dictionary
from TurtleArt.tautils import debug_output, power_manager_off
from TurtleArt.taconstants import MEDIA_SHAPES, NO_IMPORT, SKIN_PATHS, \
    BLOCKS_WITH_SKIN
from TurtleArt.taprimitive import (ConstantArg, Primitive)
from TurtleArt.tatype import TYPE_NUMBER


class Camera_sensor(Plugin):

    def __init__(self, parent):
        Plugin.__init__(self)
        ''' Make sure there is a camera device '''
        self._parent = parent
        self._status = False
        self._ag_control = None
        self.devices = []
        self.cameras = []
        self.luminance = 0

        if os.path.exists('/dev/video0'):
            self.devices.append('/dev/video0')
        if os.path.exists('/dev/video1'):
            self.devices.append('/dev/video1')
        if len(self.devices) > 0:
            self._status = True
        else:
            self._status = False

    def setup(self):
        ''' Set up the palettes '''
        sensors_palette = make_palette('sensor',
                                       colors=["#FF6060", "#A06060"],
                                       help_string=_(
                                           'Palette of sensor blocks'),
                                       position=6)
        media_palette = make_palette('media',
                                     colors=["#A0FF00", "#80A000"],
                                     help_string=_('Palette of media objects'),
                                     position=7)

        # set up camera-specific blocks
        media_blocks_dictionary['camera'] = self.prim_take_picture0
        media_blocks_dictionary['camera1'] = self.prim_take_picture1

        SKIN_PATHS.append('plugins/camera_sensor/images')

        hidden = True
        second_cam = False
        if self._status:
            hidden = False
            if len(self.devices) > 1:
                second_cam = True

        sensors_palette.add_block('luminance',
                                  hidden=hidden,
                                  style='box-style',
                                  label=_('brightness'),
                                  help_string=_(
                                      'light level detected by camera'),
                                  value_block=True,
                                  prim_name='luminance')
        self._parent.lc.def_prim(
            'luminance', 0,
            Primitive(self.prim_read_camera,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'luminance_only': ConstantArg(True)},
                      call_afterwards=self.after_luminance))

        media_palette.add_block('camera',
                                hidden=hidden,
                                style='box-style-media',
                                label=' ',
                                default='CAMERA',
                                help_string=_('camera output'),
                                content_block=True)

        media_palette.add_block('camera1',
                                hidden=not (second_cam),
                                style='box-style-media',
                                label=' ',
                                default='CAMERA',
                                help_string=_('camera output'),
                                content_block=True)

        # Depreciated block
        sensors_palette.add_block(
            'read_camera',
            hidden=True,
            style='box-style',
            label=_('brightness'),
            help_string=_(
                'Average RGB color from camera is pushed to the stack'),
            value_block=True,
            prim_name='read_camera')
        self._parent.lc.def_prim(
            'read_camera', 0,
            Primitive(self.prim_read_camera,
                      return_type=TYPE_NUMBER,
                      kwarg_descs={'luminance_only': ConstantArg(False)}))

        NO_IMPORT.append('camera')
        BLOCKS_WITH_SKIN.append('camera')
        NO_IMPORT.append('camera1')
        BLOCKS_WITH_SKIN.append('camera1')
        MEDIA_SHAPES.append('camerasmall')
        MEDIA_SHAPES.append('cameraoff')
        MEDIA_SHAPES.append('camera1small')
        MEDIA_SHAPES.append('camera1off')

    def start(self):
        ''' Initialize the camera if there is an camera block in use '''
        camera_blocks = len(self._parent.block_list.get_similar_blocks(
            'block', ['camera', 'camera1', 'read_camera', 'luminance']))
        if not self._parent.running_turtleart or camera_blocks > 0:
            if self._status and len(self.cameras) == 0:
                for device in self.devices:
                    self.cameras.append(Camera(device))
                power_manager_off(True)

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
        if self._status and len(self.cameras) > 0:
            for i, camera in enumerate(self.cameras):
                camera.stop_camera_input()
                self._set_autogain(1, camera=i)  # enable AUTOGAIN
            power_manager_off(False)

    def _status_report(self):
        debug_output('Reporting camera status: %s' % (str(self._status)),
                     self._parent.running_sugar)
        return self._status

    # Block primitives used in talogo

    def prim_take_picture0(self):
        self._take_picture(camera=0)

    def prim_take_picture1(self):
        self._take_picture(camera=1)

    def _take_picture(self, camera=0):
        ''' method called by media block '''
        self._set_autogain(1, camera)  # enable AUTOGAIN
        self._get_pixbuf_from_camera(camera)
        self._parent.lc.pixbuf = self.cameras[camera].pixbuf

    def prim_read_camera(self, luminance_only=False, camera=0):
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
        self._set_autogain(0, camera=camera)  # disable AUTOGAIN
        self._get_pixbuf_from_camera(camera=camera)
        self.calc_luminance(camera=camera)
        if self.luminance_only:
            return int(self.luminance)
        else:
            self._parent.lc.heap.append(self.b)
            self._parent.lc.heap.append(self.g)
            self._parent.lc.heap.append(self.r)
            return

    def calc_luminance(self, camera=0):
        array = self.cameras[camera].pixbuf.get_pixels()
        width = self.cameras[camera].pixbuf.get_width()
        height = self.cameras[camera].pixbuf.get_height()

        if array is not None:
            length = int(len(array) / 3)
            if length != width * height:
                debug_output('array length != width x height (%d != %dx%d)' %
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

    def after_luminance(self, luminance_only=False):
        if self._parent.lc.update_values and luminance_only:
            self._parent.lc.update_label_value('luminance', self.luminance)

    def _set_autogain(self, state, camera=0):
        ''' 0 is off; 1 is on '''
        if self._ag_control is not None and self._ag_control.value == state:
            return
        try:
            video_capture_device = open(self.devices[camera], 'rw')
        except BaseException:
            video_capture_device = None
            debug_output('video capture device not available',
                         self._parent.running_sugar)
            return
        self._ag_control = v4l2_control(V4L2_CID_AUTOGAIN)
        try:
            ioctl(video_capture_device, VIDIOC_G_CTRL, self._ag_control)
            self._ag_control.value = state
            ioctl(video_capture_device, VIDIOC_S_CTRL, self._ag_control)
        except BaseException:
            pass
        video_capture_device.close()

    def _get_pixbuf_from_camera(self, camera):
        ''' Regardless of how we get it, we want to return a pixbuf '''
        self._parent.lc.pixbuf = None
        if self._status:
            self.cameras[camera].start_camera_input()
