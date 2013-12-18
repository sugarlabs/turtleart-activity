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

import os
from math import pi, sin, cos, sqrt, atan2
from random import uniform

from gettext import gettext as _

from sugar.datastore import datastore
from sugar import profile

from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette
from TurtleArt.tautils import debug_output, json_dump, get_path, round_int
from TurtleArt.taprimitive import (ArgSlot, ConstantArg, Primitive)
from TurtleArt.tatype import TYPE_NUMBER, TYPE_STRING

import logging
_logger = logging.getLogger('turtleart-activity physics plugin')


THRESHOLD = 0.1  # default distance metric for hits


class Physics(Plugin):

    SCALE_FACTOR = 10.
    LINE_SCALE = 24.
    TOOTH_SCALE = 10
    TOOTH_ANGLE = 75 * pi / 180.

    def __init__(self, parent):
        self._tw = parent
        self._status = True
        self._scale = self.SCALE_FACTOR / self._tw.canvas.width
        self._id = 1
        self._density = 1.
        self._friction = 0.5
        self._bounce = 0.15
        self._dynamic = True
        self._polygon = []
        self._dict = {'bodylist': [],
                      'jointlist': [],
                      'controllerlist': [],
                      'additional_vars': {}}
        self._trackinfo = {}
        self.prim_box2d_reset()
        self._gear_radius = 0

    def setup(self):
        # set up physics specific blocks
        palette = make_palette('physics',
                               colors=['#50A000', '#60C020'],
                               help_string=_('Palette of physics blocks'))

        palette.add_block('density',
                          style='basic-style-1arg',
                          label=_('density'),
                          default=100,
                          help_string=_('Set the density property for objects \
(density can be any positive number).'),
                          prim_name='box2ddensity')
        self._tw.lc.def_prim(
            'box2ddensity', 1,
            Primitive(
                self.prim_box2d_density,
                arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('friction',
                          style='basic-style-1arg',
                          label=_('friction'),
                          default=50,
                          help_string=_('Set the friction property for \
objects (value from 0 to 100, where 0 turns friction off and 100 is strong \
friction).'),
                          prim_name='box2dfriction')
        self._tw.lc.def_prim(
            'box2dfriction', 1,
            Primitive(
                self.prim_box2d_friction,
                arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('bounce',
                          style='basic-style-1arg',
                          label=_('bounciness'),
                          default=15,
                          help_string=_('Set the bounciness property for \
objects (a value from 0 to 100, where 0 means no bounce and 100 is very \
bouncy).'),
                          prim_name='box2dbounce')
        self._tw.lc.def_prim(
            'box2dbounce', 1,
            Primitive(
                self.prim_box2d_bounce,
                arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('dynamic',
                          style='basic-style-1arg',
                          label=_('dynamic'),
                          hidden=True,  # hide until we debug it
                          default=1,
                          help_string=_('If dynamic = 1, the object can move; \
if dynamic = 0, it is fixed in position.'),
                          prim_name='box2ddynamic')
        self._tw.lc.def_prim(
            'box2ddynamic', 1,
            Primitive(
                self.prim_box2d_dynamic,
                arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('startpolygon',
                          style='basic-style-extended-vertical',
                          label=_('start polygon'),
                          help_string=_('Begin defining a new polygon based \
on the current Turtle xy position.'),
                          prim_name='box2dstartpolygon')
        self._tw.lc.def_prim(
            'box2dstartpolygon', 0,
            Primitive(self.prim_box2d_start_polygon))

        palette.add_block('addpoint',
                          style='basic-style-extended-vertical',
                          label=_('add point'),
                          help_string=_('Add a new point to the current \
polygon based on the current Turtle xy position.'),
                          prim_name='box2daddpoint')
        self._tw.lc.def_prim(
            'box2daddpoint', 0,
            Primitive(self.prim_box2d_add_point))

        palette.add_block('endpolygon',
                          style='basic-style-extended-vertical',
                          label=_('end polygon'),
                          help_string=_('Define a new polygon.'),
                          prim_name='box2dendpolygon')
        self._tw.lc.def_prim(
            'box2dendpolygon', 0,
            Primitive(self.prim_box2d_end_polygon))

        palette.add_block('endfilledpolygon',
                          style='basic-style-extended-vertical',
                          label=_('end filled polygon'),
                          # hidden=True,  # until it is debugged
                          help_string=_('Define a new flled polygon.'),
                          prim_name='box2dendfilledpolygon')
        self._tw.lc.def_prim(
            'box2dendfilledpolygon', 0,
            Primitive(self.prim_box2d_end_filled_polygon,
                      kwarg_descs={'triangulate': ConstantArg(True)}))

        palette.add_block('triangle',
                          style='basic-style-2arg',
                          label=[_('triangle'), _('base'), _('height')],
                          # make an equilateral triangle by default
                          default=[100, round_int(100 * sin(pi / 3))],
                          help_string=_('Add a triangle object to the \
project.'),
                          prim_name='box2dtriangle')
        self._tw.lc.def_prim(
            'box2dtriangle', 2,
            Primitive(self.prim_box2d_triangle,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)]))

        palette.add_block('circle',
                          style='basic-style-1arg',
                          label=_('circle'),
                          default=100,
                          help_string=_('Add a circle object to the project.'),
                          prim_name='box2dcircle')
        self._tw.lc.def_prim(
            'box2dcircle', 1,
            Primitive(self.prim_box2d_circle,
                      arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('rectangle',
                          style='basic-style-2arg',
                          label=[_('rectangle'), _('width'), _('height')],
                          default=[100, 100],
                          help_string=_('Add a rectangle object to the \
project.'),
                          prim_name='box2drectangle')
        self._tw.lc.def_prim(
            'box2drectangle', 2,
            Primitive(self.prim_box2d_rectangle,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)]))

        palette.add_block('gear',
                          style='basic-style-1arg',
                          label=_('gear'),
                          default=12,
                          help_string=_('Add a gear object to the project.'),
                          prim_name='box2dgear')
        self._tw.lc.def_prim(
            'box2dgear', 1,
            Primitive(self.prim_box2d_gear,
                      arg_descs=[ArgSlot(TYPE_NUMBER)]))

        palette.add_block('gearradius',
                          style='number-style-1arg',
                          label=_('gear radius'),
                          default=12,
                          help_string=_('Return the radius of a gear.'),
                          prim_name='box2dradius')
        self._tw.lc.def_prim(
            'box2dradius', 1,
            Primitive(self.prim_box2d_radius,
                      arg_descs=[ArgSlot(TYPE_NUMBER)],
                      return_type=TYPE_NUMBER))

        palette.add_block('reset',
                          hidden=True,
                          style='basic-style-extended-vertical',
                          label=_('reset'),
                          help_string=_('Reset the project; clear the object \
list.'),
                          prim_name='box2dreset')
        self._tw.lc.def_prim(
            'box2dreset', 0,
            Primitive(self.prim_box2d_reset))

        palette.add_block('motor',
                          style='basic-style-2arg',
                          label=[_('motor'), _('torque'), _('speed')],
                          default=[900, -10],
                          help_string=_('Motor torque and speed range from 0 \
(off) to positive numbers; motor is placed on the most recent object \
created.'),
                          prim_name='box2dmotor')
        self._tw.lc.def_prim(
            'box2dmotor', 2,
            Primitive(self.prim_box2d_motor,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)]))

        palette.add_block('pin',
                          style='basic-style-extended-vertical',
                          label=_('pin'),
                          help_string=_('Pin an object down so that it cannot \
fall.'),
                          prim_name='box2dpin')
        self._tw.lc.def_prim(
            'box2dpin', 0,
            Primitive(self.prim_box2d_pin))

        palette.add_block('pen',
                          style='basic-style-extended-vertical',
                          label=_('pen'),
                          help_string=_('Add a pen to an object so that its \
movements are traced.'),
                          prim_name='box2dpen')
        self._tw.lc.def_prim(
            'box2dpen', 0,
            Primitive(self.prim_box2d_pen))

        palette.add_block('joint',
                          style='basic-style-2arg',
                          label=[_('joint'), _('x'), _('y')],
                          default=[0, 0],
                          help_string=_('Join two objects together (the \
object at the current location and the object at point x, y).'),
                          prim_name='box2djoint')
        self._tw.lc.def_prim(
            'box2djoint', 2,
            Primitive(self.prim_box2d_joint,
                      arg_descs=[ArgSlot(TYPE_NUMBER), ArgSlot(TYPE_NUMBER)]))

        palette.add_block('savebox2d',
                          style='basic-style-1arg',
                          label=_('save as Physics activity'),
                          default='physics project',
                          help_string=_('Save the project to the Journal as \
a Physics activity.'),
                          prim_name='savebox2d')
        self._tw.lc.def_prim(
            'savebox2d', 1,
            Primitive(self.prim_save_box2d,
                      arg_descs=[ArgSlot(TYPE_STRING)]))

    def _status_report(self):
        ''' Required method '''
        debug_output('Reporting physics status: %s' % (str(self._status)))
        return self._status

    def clear(self):
        ''' Erase button pressed or clean block executed '''
        self.prim_box2d_reset()

    # Block primitives used in talogo

    def prim_box2d_reset(self):
        ''' Clear the body list '''
        self._id = 1
        self._density = 1.
        self._friction = 0.5
        self._bounce = 0.15
        self._dynamic = True
        self._polygon = []
        self._dict['bodylist'] = []
        self._dict['jointlist'] = []
        # Always start with a ground plane
        self._dict['bodylist'].append(
            {'userData': {'color': [114, 114, 185], 'saveid': 1},
             'linearVelocity': [0.0, 0.0],
             'dynamic': False,
             'angularVelocity': 0.0,
             'shapes': [{'restitution': 0.15,
                         'type': 'polygon',
                         'vertices': [[-50.0, -0.1],
                                      [50.0, -0.1],
                                      [50.0, 0.1],
                                      [-50.0, 0.1]],
                         'friction': 0.5,
                         'density': 0.0}],
             'position': [-10.0, 0.0],
             'angle': 0.0})

    def prim_box2d_density(self, density):
        ''' set the density to be used when creating box2d objects '''
        try:
            self._density = abs(float(density) / 100.)
        except ValueError:
            debug_output('bad argument to density: must be positive float',
                         self._tw.running_sugar)
            self._density = 1.

    def prim_box2d_friction(self, friction):
        ''' set the friction to be used when creating box2d objects '''
        try:
            self._friction = abs(float(friction) / 100.)
            if self._friction > 1:
                self._friction == 1
                debug_output('max friction value is 100',
                             self._tw.running_sugar)
        except ValueError:
            debug_output('bad argument to friction: must be positive float',
                         self._tw.running_sugar)
            self._friction = 0.5

    def prim_box2d_bounce(self, bounce):
        ''' set the bounce to be used when creating box2d objects '''
        try:
            self._bounce = abs(float(bounce) / 100.)
            if self._bounce > 1.:
                self._bounce == 1.
                debug_output('max bounce value is 100',
                             self._tw.running_sugar)
        except ValueError:
            debug_output('bad argument to bounce: must be a positive float',
                         self._tw.running_sugar)
            self._bounce = 0.5

    def prim_box2d_dynamic(self, value):
        ''' set the dynamic flag to be used when creating box2d objects '''
        if str(value).lower() in [_('false'), _('no'), '0']:
            self._dynamic = False
        else:
            self._dynamic = True

    def prim_box2d_start_polygon(self):
        ''' start of a collection of points to create a polygon '''
        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        self._polygon = [(x + self._tw.canvas.width / 2.,
                          y + self._tw.canvas.height / 2.)]

    def prim_box2d_add_point(self):
        ''' add an point to a collection of points to create a polygon '''
        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        x += self._tw.canvas.width / 2.
        y += self._tw.canvas.height / 2.
        if self._polygon == []:
            self._polygon.append((x, y))
        elif not (x == self._polygon[-1][0] and y == self._polygon[-1][1]):
            self._polygon.append((x, y))

    def prim_box2d_end_polygon(self):
        ''' add a polygon object to box2d dictionary '''
        if not self._status:
            return
        if self._polygon == []:
            return
        else:
            x = self._tw.turtles.get_active_turtle().get_x()
            y = self._tw.turtles.get_active_turtle().get_y()
            x += self._tw.canvas.width / 2.
            y += self._tw.canvas.height / 2.

            # Only append the last point if it is not redundant
            if not self._near((x, y), (self._polygon[-1])):
                self._polygon.append((x, y))

            # Box2d chokes on polygons with just 1 point
            if len(self._polygon) == 1:
                return
            # The overall position will be relative to the first point
            xpos = self._polygon[0][0] * self._scale
            ypos = self._polygon[0][1] * self._scale

            # Create the Physics object...
            self._id += 1
            self._dict['bodylist'].append(
                {'userData': {'color': self._get_rgb(),
                              'saveid': self._id},
                 'linearVelocity': [0.0, 0.0],
                 'dynamic': self._dynamic,
                 'angularVelocity': 0.0,
                 'shapes': [],
                 'position': [xpos, ypos],
                 'angle': 0.0})

            for i, p in enumerate(self._polygon):
                if i == 0:
                    p0 = p[:]
                    continue
                p1 = p[:]
                self._dict['bodylist'][-1]['shapes'].append(
                    {'density': self._density,
                     'friction': self._friction,
                     'type': 'polygon',
                     'vertices': [],
                     'restitution': self._bounce})

                a = atan2(p0[1] - p1[1], p0[0] - p1[0])
                dx = sin(a) / self.LINE_SCALE
                dy = -cos(a) / self.LINE_SCALE
                poly = [[p0[0] * self._scale + dx - xpos,
                         p0[1] * self._scale + dy - ypos],
                        [p1[0] * self._scale + dx - xpos,
                         p1[1] * self._scale + dy - ypos],
                        [p1[0] * self._scale - dx - xpos,
                         p1[1] * self._scale - dy - ypos],
                        [p0[0] * self._scale - dx - xpos,
                         p0[1] * self._scale - dy - ypos]]
                # Make sure points are counter-clockwise
                if self._cross_product_area(poly) < 0:
                    poly = self._reverse_order(poly)[:]
                self._dict['bodylist'][-1]['shapes'][-1][
                    'vertices'].append(poly[0])
                self._dict['bodylist'][-1]['shapes'][-1][
                    'vertices'].append(poly[1])
                self._dict['bodylist'][-1]['shapes'][-1][
                    'vertices'].append(poly[2])
                self._dict['bodylist'][-1]['shapes'][-1][
                    'vertices'].append(poly[3])
                if not (i + 1) == len(self._polygon):
                    self._dict['bodylist'][-1]['shapes'].append(
                        {'localPosition': [p1[0] * self._scale - xpos,
                                           p1[1] * self._scale - ypos],
                         'density': self._density,
                         'friction': self._friction,
                         'radius': 1. / self.LINE_SCALE,
                         'type': 'circle',
                         'restitution': self._bounce})
                p0 = p1[:]

            # ... and draw the polygon on the Turtle canvas
            self._tw.canvas.set_source_rgb()
            self._tw.canvas.canvas.set_line_width(1.)
            for s in self._dict['bodylist'][-1]['shapes']:
                if s['type'] == 'polygon':
                    self._tw.canvas.canvas.new_path()
                    for i, p in enumerate(s['vertices']):
                        x, y = self._tw.turtles.turtle_to_screen_coordinates(
                            ((p[0] + xpos) / self._scale -
                             self._tw.canvas.width / 2.,
                             (p[1] + ypos) / self._scale -
                             self._tw.canvas.height / 2.))
                        if i == 0:
                            self._tw.canvas.canvas.move_to(x, y)
                        else:
                            self._tw.canvas.canvas.line_to(x, y)
                    self._tw.canvas.canvas.close_path()
                    self._tw.canvas.canvas.fill()
                elif s['type'] == 'circle':
                    x, y = self._tw.turtles.turtle_to_screen_coordinates(
                        ((s['localPosition'][0] + xpos) / self._scale -
                         self._tw.canvas.width / 2.,
                         (s['localPosition'][1] + ypos) / self._scale -
                         self._tw.canvas.height / 2.))
                    self._tw.canvas.canvas.set_line_width(
                        2. / (self.LINE_SCALE * self._scale))
                    self._tw.canvas.canvas.move_to(x, y)
                    self._tw.canvas.canvas.line_to(x + 1, y + 1)
                    self._tw.canvas.canvas.stroke()
            self._tw.canvas.canvas.set_line_width(
                self._tw.turtles.get_active_turtle().get_pen_size())
            self._tw.canvas.inval()

            self._polygon = []

    def prim_box2d_end_filled_polygon(self, triangulate=False):
        ''' add a filled-polygon object to box2d dictionary '''
        if not self._status:
            return
        if self._polygon == []:
            return
        else:
            x = self._tw.turtles.get_active_turtle().get_x()
            y = self._tw.turtles.get_active_turtle().get_y()
            x += self._tw.canvas.width / 2.
            y += self._tw.canvas.height / 2.

            # Make sure there are no points too near each other
            poly = []
            p1 = self._polygon[-1]
            for p2 in self._polygon:
                if not self._near(p1, p2):
                    poly.append(p2)
                p1 = p2[:]
            self._polygon = poly[:]

            if len(self._polygon) < 3:
                return

            # Physics requires polygons to be ordered counter clockwise
            if self._cross_product_area(self._polygon) < 0:
                self._polygon = self._reverse_order(self._polygon)[:]

            # Divide the polygon into triangles
            if triangulate:
                triangles = self._triangulate(self._polygon)
                if triangles is None:
                    debug_output(_('Not a simple polygon'),
                                 self._tw.running_sugar)
                    self._tw.showlabel('syntaxerror',
                                       _('Not a simple polygon'))
                    return

            # Create the Physics object...
            xpos = self._polygon[0][0] * self._scale
            ypos = self._polygon[0][1] * self._scale
            self._id += 1
            self._dict['bodylist'].append(
                {'userData': {'color': self._get_rgb(),
                              'saveid': self._id},
                 'linearVelocity': [0.0, 0.0],
                 'dynamic': self._dynamic,
                 'angularVelocity': 0.0,
                 'shapes': [],
                 'position': [xpos, ypos],
                 'angle': 0.0})

            if triangulate:
                for triangle in triangles:
                    self._add_shape(triangle, xpos, ypos)
            else:
                self._add_shape(self._polygon, xpos, ypos)

            # ...and draw it on the Turtle canvas
            self._tw.canvas.set_source_rgb()
            self._tw.canvas.canvas.set_line_width(1.)
            if triangulate:
                for triangle in triangles:
                    # Make each triangle distinct in the TA rendering
                    self._randomize_color()
                    self._draw_polygon(triangle)
                # Restore canvas color
                self._tw.canvas.set_source_rgb()
            else:
                self._draw_polygon(self._polygon)
            self._tw.canvas.canvas.set_line_width(
                self._tw.turtles.get_active_turtle().get_pen_size())
            self._tw.canvas.inval()

            self._polygon = []

    def _bounds_check(self, value):
        ''' Make sure value is between 0 and 1 '''
        if value < 0.:
            value = 0.
        elif value > 1.:
            value = 1
        return value

    def _randomize_color(self):
        ''' Add a bit of noise to the turtle color '''
        dr = uniform(-10, 10) / 100.
        dg = uniform(-10, 10) / 100.
        db = uniform(-10, 10) / 100.
        rgb = self._get_rgb()
        self._tw.canvas.canvas.set_source_rgb(
            self._bounds_check((rgb[0] / 255.) + dr),
            self._bounds_check((rgb[1] / 255.) + dg),
            self._bounds_check((rgb[2] / 255.) + db))

    def _draw_polygon(self, polygon):
        ''' Draw a polygon on the turtle canvas '''
        self._tw.canvas.canvas.new_path()
        for i, p in enumerate(polygon):
            x, y = self._tw.turtles.turtle_to_screen_coordinates(
                (p[0] - self._tw.canvas.width / 2.,
                 p[1] - self._tw.canvas.height / 2.))
            if i == 0:
                self._tw.canvas.canvas.move_to(x, y)
            else:
                self._tw.canvas.canvas.line_to(x, y)
        self._tw.canvas.canvas.close_path()
        self._tw.canvas.canvas.fill()

    def _add_shape(self, polygon, xpos, ypos):
        ''' Add a polygon to the shape list '''
        self._dict['bodylist'][-1]['shapes'].append(
            {'density': self._density,
             'friction': self._friction,
             'type': 'polygon',
             'vertices': [],
             'restitution': self._bounce})
        for i, p in enumerate(polygon):
            self._dict['bodylist'][-1]['shapes'][-1][
                'vertices'].append([p[0] * self._scale - xpos,
                                    p[1] * self._scale - ypos])

    def prim_box2d_triangle(self, base, height):
        ''' add a triangle object to box2d dictionary '''
        try:
            float(base)
            float(height)
        except ValueError:
            debug_output(
                'bad argument to triangle: base, height must be float',
                self._tw.running_sugar)
        self._polygon = []

        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        x += self._tw.canvas.width / 2.
        y += self._tw.canvas.height / 2.
        self._polygon.append([x - base / 2., y - height / 2.])
        self._polygon.append([x, y + height / 2.])
        self._polygon.append([x + base / 2., y - height / 2.])
        h = self._tw.turtles.get_active_turtle().get_heading()
        # if h != 0:
        self._rotate_polygon(x, y, (270 - h) * pi / 180.)
        self.prim_box2d_end_filled_polygon()

    def prim_box2d_rectangle(self, width, height):
        ''' add a rectangle object to box2d dictionary '''
        try:
            float(width)
            float(height)
        except ValueError:
            debug_output(
                'bad argument to rectangle: width, height must be float',
                self._tw.running_sugar)
        self._polygon = []
        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        x += self._tw.canvas.width / 2.
        y += self._tw.canvas.height / 2.
        self._polygon.append([x - width / 2., y - height / 2.])
        self._polygon.append([x + width / 2., y - height / 2.])
        self._polygon.append([x + width / 2., y + height / 2.])
        self._polygon.append([x - width / 2., y + height / 2.])
        h = self._tw.turtles.get_active_turtle().get_heading()
        if h != 0:
            self._rotate_polygon(x, y, (90 - h) * pi / 180.)
        self.prim_box2d_end_filled_polygon()

    def prim_box2d_radius(self, tooth_count):
        ''' calculate gear radius '''
        try:
            if abs(int(tooth_count)) < 2:
                raise ValueError
        except ValueError:
            debug_output('bad argument to gear: tooth count must be int > 1',
                         self._tw.running_sugar)

        points = self._gear(int(tooth_count))
        max_x = 0
        for p in points:
            max_x = max(p[0], max_x)
        radius = int(max(0, max_x - self.TOOTH_SCALE / 4.))
        return radius

    def prim_box2d_gear(self, tooth_count):
        ''' add a gear object to box2d dictionary '''
        try:
            if abs(int(tooth_count)) < 2:
                raise ValueError
        except ValueError:
            debug_output('bad argument to gear: tooth count must be int > 1',
                         self._tw.running_sugar)

        self._polygon = []
        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        x += self._tw.canvas.width / 2.
        y += self._tw.canvas.height / 2.
        points = self._gear(int(tooth_count))
        for p in points:
            self._polygon.append([x + p[0], y + p[1]])
        h = self._tw.turtles.get_active_turtle().get_heading()
        # if h != 0:
        self._rotate_polygon(x, y, (90 - h) * pi / 180.)
        self.prim_box2d_end_filled_polygon(triangulate=True)

    def prim_box2d_circle(self, radius):
        ''' add a circle object to box2d dictionary '''
        try:
            float(radius)
        except ValueError:
            debug_output('bad argument to circle: radius must be float',
                         self._tw.running_sugar)

        # Create the Physics object...
        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        x += self._tw.canvas.width / 2.
        y += self._tw.canvas.height / 2.
        self._id += 1
        self._dict['bodylist'].append(
            {'userData': {'color': self._get_rgb(),
                          'saveid': self._id},
             'linearVelocity': [0.0, 0.0],
             'dynamic': self._dynamic,
             'angularVelocity': 0.0,
             'shapes': [{'localPosition': [0, 0],
                         'density': self._density,
                         'friction': self._friction,
                         'radius': radius * self._scale / 2.,
                         'type': 'circle',
                         'restitution': self._bounce}],
             'position': [x * self._scale, y * self._scale],
             'angle': 0.0})

        # ...and draw it on the Turtle canvas

        x, y = self._tw.turtles.turtle_to_screen_coordinates(
            self._tw.turtles.get_active_turtle().get_xy())
        self._tw.canvas.set_source_rgb()
        self._tw.canvas.canvas.set_line_width(radius)
        self._tw.canvas.canvas.move_to(x, y)
        self._tw.canvas.canvas.line_to(x + 1, y + 1)
        self._tw.canvas.canvas.stroke()
        self._tw.canvas.canvas.set_line_width(
            self._tw.turtles.get_active_turtle().get_pen_size())
        self._tw.canvas.inval()

    def prim_box2d_pin(self):
        self.prim_box2d_motor(0, 0)

    def prim_box2d_motor(self, torque, speed):
        ''' add a motor to an object to box2d dictionary '''
        try:
            float(torque)
            float(speed)
        except ValueError:
            debug_output('bad argument to motor: torque, speed must be float',
                         self._tw.running_sugar)

        # Create the Physics object...
        x = self._tw.turtles.get_active_turtle().get_x()
        y = self._tw.turtles.get_active_turtle().get_y()
        x += self._tw.canvas.width / 2.
        y += self._tw.canvas.height / 2.
        self._dict['jointlist'].append(
            {'userData': None,
             'collideConnected': False,
             'maxMotorTorque': torque,
             'motorSpeed': speed,
             'body1': 0,
             # Assume that the motor is attached to the most recent object
             'body2': self._id,
             'type': 'revolute',
             'anchor': [x * self._scale, y * self._scale],
             'enableMotor': False})
        if speed != 0:
            self._dict['jointlist'][-1]['enableMotor'] = True

        # To do: search for body to attach to...
        id = self._search((x * self._scale, y * self._scale))
        if id is not None:
            # debug_output('found a match for motor body2 (%d)' % (id),
            #              self._tw.running_sugar)
            self._dict['jointlist'][-1]['body2']

        # ...and draw it on the Turtle canvas
        x, y = self._tw.turtles.turtle_to_screen_coordinates(
            self._tw.turtles.get_active_turtle().get_xy())
        if speed == 0:
            self._tw.canvas.canvas.set_source_rgb(0., 0., 0.)
        else:
            self._tw.canvas.canvas.set_source_rgb(1., 1., 1.)
        self._tw.canvas.canvas.set_line_width(3.)
        self._tw.canvas.canvas.move_to(x, y)
        self._tw.canvas.canvas.line_to(x + 1, y + 1)
        self._tw.canvas.canvas.stroke()
        self._tw.canvas.canvas.set_line_width(
            self._tw.turtles.get_active_turtle().get_pen_size())
        self._tw.canvas.inval()

    def prim_box2d_pen(self):
        ''' add a pen onto an object '''

        # Create the Physics object...
        x1 = x2 = self._tw.turtles.get_active_turtle().get_x() + \
            self._tw.canvas.width / 2.
        y1 = y2 = self._tw.turtles.get_active_turtle().get_y() + \
            self._tw.canvas.height / 2.

        # Search for the body to attach to...
        hostid = self._search((x1 * self._scale, y1 * self._scale))
        if hostid is None:
            debug_output('No object found to attach pen',
                         self._tw.running_sugar)
            return

        track_index = len(self._trackinfo.keys())

        # Create a small circle to hold the pen
        radius = 0.01
        self._id += 1
        self._dict['bodylist'].append(
            {'userData': {'color': self._get_rgb(),
                          'saveid': self._id,
                          'track_index': track_index},
             'linearVelocity': [0.0, 0.0],
             'dynamic': self._dynamic,
             'angularVelocity': 0.0,
             'shapes': [{'localPosition': [0, 0],
                         'density': self._density,
                         'friction': self._friction,
                         'radius': radius * self._scale / 2.,
                         'type': 'circle',
                         'restitution': self._bounce}],
             'position': [x1 * self._scale, y1 * self._scale],
             'angle': 0.0})

        # ...and draw it on the Turtle canvas
        x, y = self._tw.turtles.turtle_to_screen_coordinates(
            self._tw.turtles.get_active_turtle().get_xy())
        self._tw.canvas.canvas.set_source_rgb(0.5, 0.5, 0.5)
        self._tw.canvas.canvas.set_line_width(3.0)
        self._tw.canvas.canvas.move_to(x1, y1)
        self._tw.canvas.canvas.line_to(x1 + 1, y1 + 1)
        self._tw.canvas.canvas.stroke()
        self._tw.canvas.canvas.set_line_width(
            self._tw.turtles.get_active_turtle().get_pen_size())
        self._tw.canvas.inval()

        self._dict['jointlist'].append(
            {'userData': None,
             'anchor2': [x1 * self._scale, y1 * self._scale],
             'anchor1': [x2 * self._scale, y2 * self._scale],
             'collideConnected': False,
             'body1': self._id,  # The pen circle
             'body2': hostid, # The host object
             'type': 'distance'})

        self._dict['jointlist'][-1]['body2'] = hostid
        body = self._dict['bodylist'][hostid]['userData']
        if 'track_indices' in body:
            body['track_indices'].append(track_index)
        else:
            body['track_indices'] = [track_index]

        # Finally, add the pen to the trackinfo dictionary.
        self._trackinfo['pen%d' % track_index] = [self._id, hostid,
                                                 body['color'],
                                                 False, track_index]

    def prim_box2d_joint(self, x, y):
        ''' add a joint between two objects '''
        try:
            float(x)
            float(y)
        except ValueError:
            debug_output('bad argument to joint: x, y must be float',
                         self._tw.running_sugar)

        # Create the Physics object...
        x1 = x + self._tw.canvas.width / 2.
        y1 = y + self._tw.canvas.height / 2.
        x2 = self._tw.turtles.get_active_turtle().get_x() + \
            self._tw.canvas.width / 2.
        y2 = self._tw.turtles.get_active_turtle().get_y() + \
            self._tw.canvas.height / 2.
        self._dict['jointlist'].append(
            {'userData': None,
             'anchor2': [x1 * self._scale, y1 * self._scale],
             'anchor1': [x2 * self._scale, y2 * self._scale],
             'collideConnected': True,
             'body1': self._id,  # A reasonable default?
             'body2': 2,  # Assume most recent?
             'type': 'distance'})

        # Search for the body to attach to...
        id = self._search((x1 * self._scale, y1 * self._scale))
        if id is not None:
            # debug_output('found a match for joint body2 (%d)' % (id),
            #              self._tw.running_sugar)
            self._dict['jointlist'][-1]['body2'] = id
        id = self._search((x2 * self._scale, y2 * self._scale))
        if id is not None:
            # debug_output('found a match for joint body1 (%d)' % (id),
            #              self._tw.running_sugar)
            self._dict['jointlist'][-1]['body1'] = id

        # ...and draw it on the Turtle canvas
        x1, y1 = self._tw.turtles.turtle_to_screen_coordinates((x, y))
        x2, y2 = self._tw.turtles.turtle_to_screen_coordinates(
            self._tw.turtles.get_active_turtle().get_xy())
        self._tw.canvas.canvas.set_source_rgb(0., 0., 0.)
        self._tw.canvas.canvas.set_line_width(3.)
        self._tw.canvas.canvas.move_to(x1, y1)
        self._tw.canvas.canvas.line_to(x2, y2)
        self._tw.canvas.canvas.stroke()
        self._tw.canvas.canvas.set_line_width(
            self._tw.turtles.get_active_turtle().get_pen_size())
        self._tw.canvas.inval()

    def prim_save_box2d(self, name):
        ''' Save bodylist to a Physics project '''
        self._dict['additional_vars']['trackinfo'] = self._trackinfo
        self._dict['additional_vars']['full_pos_list'] = []
        data = json_dump(self._dict)
        if not self._tw.running_sugar:
            print data
        else:
            data_path = get_path(self._tw.activity, 'instance')
            tmp_file = os.path.join(data_path, 'tmpfile')
            fd = open(tmp_file, 'w')
            fd.write(data)
            fd.close()
            dsobject = datastore.create()
            dsobject.metadata['title'] = name
            dsobject.metadata['icon-color'] = profile.get_color().to_string()
            dsobject.metadata['mime_type'] = 'application/x-physics-activity'
            dsobject.metadata['activity'] = 'org.laptop.physics'
            dsobject.set_file_path(tmp_file)
            datastore.write(dsobject)
            dsobject.destroy()
            os.remove(tmp_file)

    def _cross_product_area(self, polygon):
        ''' Cross-product area is positive for counter-clockwise polygons '''
        a = 0.
        for i in range(len(polygon)):
            if (i + 1) < len(polygon):
                a += (polygon[i][0] * polygon[i + 1][1]) - \
                    (polygon[i + 1][0] * polygon[i][1])
            else:
                a += (polygon[i][0] * polygon[0][1]) - \
                    (polygon[0][0] * polygon[i][1])
        return a / 2.

    def _reverse_order(self, polygon):
        ''' Turn a clockwise polygon into a counter-clockwise polygon '''
        n = len(polygon)
        for i in range(n / 2):
            tmp = polygon[i][:]
            polygon[i] = polygon[n - 1 - i][:]
            polygon[n - 1 - i] = tmp[:]
        return polygon

    def _rotate_polygon(self, cx, cy, angle):
        ''' Rotate the polygon points around cx,cy '''
        for p in self._polygon:
            h = sqrt((cx - p[0]) * (cx - p[0]) + (cy - p[1]) * (cy - p[1]))
            a = atan2(cx - p[0], cy - p[1])
            p[0] = cx + h * cos(a + angle)
            p[1] = cy + h * sin(a + angle)

    def _near(self, p1, p2, threshold=THRESHOLD):
        ''' Is point 1 near point 2? '''
        if sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) +
                (p1[1] - p2[1]) * (p1[1] - p2[1])) < threshold:
            return True
        return False

    def _search(self, point):
        ''' Return object id of object under point '''
        n = len(self._dict['bodylist'])
        for i in range(n):
            j = n - i - 1  # search in reverse order
            if self._hit(self._dict['bodylist'][j]['shapes'],
                         self._dict['bodylist'][j]['position'], point):
                return self._dict['bodylist'][j]['userData']['saveid']
        return None

    def _hit(self, shapes, position, point):
        ''' Is xy in shape? '''
        for s in shapes:
            if s['type'] == 'circle':
                if self._near((s['localPosition'][0] + position[0],
                               s['localPosition'][1] + position[1]),
                              point, threshold=s['radius']):
                    return True
            else:  # polygon
                if self._point_in_polygon((point[0] - position[0],
                                           point[1] - position[1]),
                                          s['vertices']):
                    return True
        return False

    def _point_in_polygon(self, point, polygon):
        '''Ray-casting method of determing if point is in polygon '''
        inside = False
        p1x, p1y = polygon[0]
        for i in range(len(polygon) + 1):
            p2x, p2y = polygon[i % len(polygon)]
            if point[1] > min(p1y, p2y):
                if point[1] <= max(p1y, p2y):
                    if point[0] <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point[1] - p1y) * (p2x - p1x) \
                                / (p2y - p1y) + p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def _point_in_triangle(self, triangle, point):
        ''' Is the point in the triangle? '''
        return \
            self._cross_product_area(
                (triangle[0], triangle[1], point)) >= 0 and \
            self._cross_product_area(
                (triangle[1], triangle[2], point)) >= 0 and \
            self._cross_product_area(
                (triangle[2], triangle[0], point)) >= 0

    def _triangulate(self, polygon):
        ''' Convert a polygon into triangles '''
        # Variation of an ear-cutting algorithm
        # Based on an algorithm by Gregor Lingl on python.org
        triangles = []
        while len(polygon) > 2:
            found_a_triangle = False
            count = 0
            while not found_a_triangle and count < len(polygon):
                count += 1
                triangle = polygon[:3]
                if self._cross_product_area(triangle) >= 0:
                    for point in polygon[3:]:
                        if self._point_in_triangle(triangle, point):
                            break
                    else:
                        triangles.append(triangle)
                        polygon.remove(triangle[1])
                        found_a_triangle = True
                polygon.append(polygon.pop(0))
            if count == len(polygon):
                return None
        return triangles

    def _gear(self, tooth_count):
        ''' Draw a gear '''
        points = []
        x = 0
        y = 0
        heading = 0
        for i in range(tooth_count):
            tooth, heading = self._gear_tooth(x, y, heading)
            for p in tooth:
                points.append(p)
            x, y = tooth[-1][0], tooth[-1][1]
            heading -= 2. * pi / tooth_count
        minx = 1000
        miny = 1000
        maxx = -1000
        maxy = -1000
        for p in points:
            if p[0] < minx:
                minx = p[0]
            if p[0] > maxx:
                maxx = p[0]
            if p[1] < miny:
                miny = p[1]
            if p[1] > maxy:
                maxy = p[1]
        # Recenter on 0, 0
        cx = (maxx + minx) / 2.
        cy = (maxy + miny) / 2.
        for p in points:
            p[0] -= cx
            p[1] -= cy
        return points

    def _gear_tooth(self, x, y, heading):
        ''' Draw one tooth of a gear '''
        points = []
        half = self.TOOTH_SCALE / 2.
        top = 1.5 * self.TOOTH_SCALE - \
            (cos(self.TOOTH_ANGLE) * self.TOOTH_SCALE * 2.)
        points.append([half * cos(heading) + x,
                       half * sin(heading) + y])
        heading += self.TOOTH_ANGLE
        points.append([self.TOOTH_SCALE * cos(heading) + points[0][0],
                       self.TOOTH_SCALE * sin(heading) + points[0][1]])
        heading -= self.TOOTH_ANGLE
        points.append([top * cos(heading) + points[1][0],
                       top * sin(heading) + points[1][1]])
        heading -= self.TOOTH_ANGLE
        points.append([self.TOOTH_SCALE * cos(heading) + points[2][0],
                       self.TOOTH_SCALE * sin(heading) + points[2][1]])
        heading += self.TOOTH_ANGLE
        points.append([half * cos(heading) + points[3][0],
                       half * sin(heading) + points[3][1]])
        return points, heading

    def _get_rgb(self):
        ''' For backward compatibility '''
        if hasattr(self._tw.canvas, 'get_rgb'):
            return self._tw.canvas.get_rgb()
        else:
            return self._tw.canvas._fgrgb
