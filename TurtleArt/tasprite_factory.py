# self program is free software you can redistribute it and/or
# modify it under the terms of the The GNU Affero General Public
# License as published by the Free Software Foundation either
# version 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public
# License along with self library if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

# Borrowing loosely from tasprite_factory.py in the Python version.

import pygtk
pygtk.require('2.0')

import gtk
import os


class SVG:

    """ Interface to the graphical representation of blocks, turtles,
    palettes, etc. on screen.
    Terms used here:
    docks -- list of connection points of a block to other blocks
    innies -- right hand side docks of a block, argument slots
    outie -- left hand side dock of a block
    slot -- top dock of a block that can be attached to other blocks
    cap -- top dock of a block that cannot be attached to other blocks
    tab -- bottom dock of a block if other blocks can be attached
    tail -- bottom dock of a block if no other blocks can be attached
    arm -- connection point of a branching block (if-then, loops) where
        inner blocks are attached
    else -- optional second `arm' for if-then-else blocks """

    def __init__(self):

        self._x = 0
        self._y = 0
        self._min_x = 10000
        self._min_y = 10000
        self._max_x = -10000
        self._max_y = -10000
        self._width = 0
        self._height = 0
        self.docks = []
        self._scale = 1
        self._orientation = 0
        self._radius = 8
        self._stroke_width = 1
        self._innies = []
        self._outie = False
        self._innie_x1 = (9 - self._stroke_width) / 2
        self._innie_y1 = 3
        self._innie_x2 = (9 - self._stroke_width) / 2
        self._innie_y2 = (9 - self._stroke_width) / 2
        self._innies_spacer = 9
        self._padding = self._innie_y1 + self._stroke_width
        self._slot = True
        self._cap = False
        self._tab = True
        self._bool = False
        self._slot_x = 10
        self._slot_y = 2
        self._tail = False
        self._porch = False
        self._porch_x = self._innie_x1 + self._innie_x2 + 4 * self._stroke_width
        self._porch_y = self._innie_y2
        self._expand_x = 30
        self._expand_x2 = 0
        self._expand_y = 0
        self._expand_y2 = 0
        self._clamp_count = 1
        self._clamp_slots = [1]
        self._slot_size = 21  # TODO: Compute self.
        self._arm = True
        self._else = False
        self._draw_inniess = True
        self._fill = 'fill_color'
        self._stroke = 'stroke_color'
        self.margins = [0, 0, 0, 0]
        self._font_size = 10

    # Attribute functions

    def setfont_size(font_size):
        self._font_size = font_size

    def set_draw_inniess(flag):
        self._draw_inniess = flag

    def get_width():
        return self._width

    def get_height():
        return self._height

    def clear_docks():
        self.docks = []

    def set_scale(scale):
        self._scale = scale

    def set_orientation(orientation):
        self._orientation = orientation

    def set_clamp_count(number):
        self._clamp_count = number

        n = self._clamp_slots.length
        if n < number:
            for i in range(0, number - n):
                self._clamp_slots.append(1)

    def set_clamp_slots(clamp, number):
        if clamp > self._clamp_count.length - 1:
            self.set_clamp_count(clamp + 1)

        self._clamp_slots[clamp] = number

    def set_expand(w, h, w2, h2):
        # TODO: make this a list
        self._expand_x = w
        self._expand_y = h
        self._expand_x2 = w2
        self._expand_y2 = h2

    def set_stroke_width(stroke_width):
        self._stroke_width = stroke_width
        self._calc_porch_params()

    def set_colors(colors):
        self._fill = colors[0]
        self._stroke = colors[1]

    def set_fill_color(color):
        self._fill = color

    def set_stroke_color(color):
        self._stroke = color

    def set_innies(innies_array):
        for i in range(0, len(inniesArray)):
            self._innies.append(inniesArray[i])

    def set_outie(flag):
        # Only one outie.
        self._outie = flag

    def set_slot(flag):
        self._slot = flag
        if flag:
            self._clap = False

    def set_cap(flag):
        self._cap = flag
        if flag:
            self._slot = False

    def set_tab(flag):
        self._tab = flag
        if flag:
            self._tail = False

    def set_tail(flag):
        self._tail = flag
        if flag:
            self._tab = False

    def set_porch(flag):
        self._porch = flag

    def set_boolean(flag):
        self._bool = flag

    def set_else(flag):
        self._else = flag

    def set_arm(flag):
        self._arm = flag

    # SVG-related helper functions
    def _reset_min_max():
        self._min_x = 10000
        self._min_y = 10000
        self._max_x = -10000
        self._max_y = -10000
    
    def _check_min_max():
        if self._x < self._min_x:
            self._min_x = self._x

        if self._y < self._min_y:
            self._min_y = self._y

        if self._x > self._max_x:
            self._max_x = self._x

        if self._y > self._max_y:
            self._max_y = self._y

    def _calculate_x_y():
        x = self._stroke_width / 2.0
        y = self._stroke_width / 2.0 + self._radius
        self.margins[0] = x + self._stroke_width + 0.5
        self.margins[1] = self._stroke_width + 0.5

        if self._outie:
            x += self._innie_x1 + self._innie_x2
            self.margins[0] += self._innie_x1 + self._innie_x2
        
        if self._cap:
            y += self._slot_y * 3.0
            self.margins[1] += self._slot_y * 3.0

        elif self._slot:
            self.margins[1] += self._slot_y
        
        self.margins[0] *= self._scale
        self.margins[1] *= self._scale

        return [x, y]
    
    def _calculate_w_h(addstrokeWidth):
        if addstrokeWidth:
            self._width = (self._max_x - self._min_x + self._stroke_width) * self._scale

        else:
            self._width = (self._max_x - self._min_x) * self._scale

        if self.margins[2] == 0:
            self.margins[2] = (self._stroke_width + 0.5) * self._scale

        else:
            self.margins[2] = self._width - self.margins[2]
        

        if addstrokeWidth:
            self._height = (self._max_y - self._min_y + self._stroke_width) * self._scale

        else:
            self._height = (self._max_y - self._min_y) * self._scale
        
        if self.margins[3] == 0:
            if self._tab:
                self.margins[3] = (self._slot_y + self._stroke_width + 0.5) * self._scale

            else:
                self.margins[3] = (self._slot_y * 2 + self._stroke_width + 0.5) * self._scale
            
        else:
            self.margins[3] = self._height - self.margins[3]

    def _new_path(x, y):
        self._x = x
        self._y = y

        return '<path d="m{0} {1} '.format(x, y)
    
    def _close_path():
        return 'z" '
    
    def text(x, y, font_size, width, alignment, string):
        self._x = x
        self._y = y
        self._check_min_max()
        self._x = x + width
        self._y = y - font_size
        self._check_min_max()

        # writing-mode:lr'
        if alignment == 'left':
            pass

        elif alignment == 'start':
            align = 'start'

        elif alignment == 'middle':
            pass

        elif alignment == 'center':
            align = 'middle'

        elif alignment == 'right':
            pass

        elif 'end':
            align = 'end'

        yy = y
        tspans = string.split('\n')
        text = '<text style="font-size:' + font_size + 'pxfill:#000000font-family:sans-seriftext-anchor:' + align + '">'
        
        for i in range(0, len(tspans)):
            text += '<tspan x="' + x + '" y="' + yy + '">' + tspans[i] + '</tspan>'
            yy += font_size

        text += '</text>'

        return text
    
    def _line_to(x, y):
        self._check_min_max()
        if self._x == x and self._y == y:
            return ''

        else:
            self._x = x
            self._y = y
            self._check_min_max()

            return 'L ' + x + ' ' + y + ' '

    def _rline_to(dx, dy):
        if dx == 0 and dy == 0:
            return ''

        else:
            return self._line_to(self._x + dx, self._y + dy)

    def _arc_to(x, y, r, a, l, s):
        self._check_min_max()

        if r == 0:
            return self._line_to(x, y)

        else:
            self._x = x
            self._y = y
            self._check_min_max()

            return 'A ' + r + ' ' + r + ' ' + a + ' ' + l + ' ' + s + ' ' + x + ' ' + y + ' '

    def _rarc_to(sign_x, sign_y, a, l, s):
        if self._radius == 0:
            return ''

        else:
            x = self._x + sign_x * self._radius
            y = self._y + sign_y * self._radius

            return self._arc_to(x, y, self._radius, a, l, s)
        
    
    def _corner(sign_x, sign_y, a, l, s, start, end, skip):
        svg_str = ''
        
        if self._radius > 0:
            r2 = self._radius / 2.0
            
            if start:
                if sign_x * sign_y == 1:
                    svg_str += self._rline_to(sign_x * r2, 0)
                 
                elif not skip:
                    svg_str += self._rline_to(0, sign_y * r2)

            x = self._x + sign_x * r2
            y = self._y + sign_y * r2
            svg_str += self._arc_to(x, y, r2, a, l, s)

            if end:
                if sign_x * sign_y == 1:
                    svg_str += self._rline_to(0, sign_y * r2)
                 
                elif not skip:
                    svg_str += self._rline_to(sign_x * r2, 0)

        return svg_str

    def _icorner(sign_x, sign_y, a, l, s, start, end):
        r2 = self._stroke_width + self._radius / 2.0

        if start:
            if sign_x * sign_y == -1:
                svg_str = self._rline_to(sign_x * (r2 - self._stroke_width), 0)

            else:
                svg_str = self._rline_to(0, sign_y * (r2 - self._stroke_width))

        else:
            svg_str = ''
        
        x = self._x + sign_x * r2
        y = self._y + sign_y * r2
        svg_str += self._arc_to(x, y, r2, a, l, s)

        if end:
            if sign_x * sign_y == -1:
                svg_str += self._rline_to(0, sign_y * (r2 - self._stroke_width))

            else:
                svg_str += self._rline_to(sign_x * (r2 - self._stroke_width), 0)
            
        
        return svg_str

    def _do_innie():
        self.docks.append([(self._x + self._stroke_width) * self._scale,
                         (self._y + self._innie_y2) * self._scale])

        if self.margins[2] == 0:
            self.margins[1] = (self._y - self._innie_y1) * self._scale
            self.margins[2] = (self._x - self._innie_x1 - self._innie_x2 - self._stroke_width * 2) * self._scale

        self.margins[3] = (self._y + self._innie_y2 + self._innie_y1) * self._scale
        return self._rline_to(-self._innie_x1, 0) + self._rline_to(0, -self._innie_y1) + self._rline_to(-self._innie_x2, 0) + self._rline_to(0, self._innie_y2 + 2 * self._innie_y1) + self._rline_to(self._innie_x2, 0) + self._rline_to(0, -self._innie_y1) + self._rline_to(self._innie_x1, 0)

    def _do_outie():
        if not self._outie:
            return self._rline_to(0, -self._innie_y2)
        
        # Outie needs to be the first dock element.
        self.docks.unshift([(self._x * self._scale), (self._y * self._scale)])
        return self._rline_to(0, -self._stroke_width) + self._rline_to(-self._innie_x1 - 2 * self._stroke_width, 0) + self._rline_to(0, self._innie_y1) + self._rline_to(-self._innie_x2 + 2 * self._stroke_width, 0) + self._rline_to(0, -self._innie_y2 - 2 * self._innie_y1 + 2 * self._stroke_width) + self._rline_to(self._innie_x2 - 2 * self._stroke_width, 0) + self._rline_to(0, self._innie_y1) + self._rline_to(self._innie_x1 + 2 * self._stroke_width, 0) + self._rline_to(0, -self._stroke_width)

    def _do_slot():
        if self._slot:
            x = self._x + self._slot_x / 2.0
            self.docks.append([(x * self._scale), (self._y * self._scale)])

            return self._rline_to(0, self._slot_y) + self._rline_to(self._slot_x, 0) + self._rline_to(0, -self._slot_y)

        elif self._cap:
            x = self._x + self._slot_x / 2.0
            self.docks.append([(x * self._scale), (self._y * self._scale)])

            return self._rline_to(self._slot_x / 2.0, -self._slot_y * 3.0) + self._rline_to(self._slot_x / 2.0, self._slot_y * 3.0)

        else:
            return self._rline_to(self._slot_x, 0)
    
    def _do_tail():
        if self._outie:
            return self._rline_to(-self._slot_x, 0)

        elif self._tail:
            x = self._x + self._slot_x / 2.0
            self.docks.append([(x * self._scale),
                             (self._y * self._scale)])

            return self._rline_to(-self._slot_x / 2.0, self._slot_y * 3.0) + self._rline_to(-self._slot_x / 2.0, -self._slot_y * 3.0)

        else:
            return self._rline_to(-self._slot_x, 0)
        
    
    def _do_tab():
        if self._outie:
            return self._rline_to(-self._slot_x, 0)
        
        x = self._x - self._slot_x / 2.0
        self.docks.append([x * self._scale, (self._y + self._stroke_width) * self._scale])

        return self._rline_to(-self._stroke_width, 0) + self._rline_to(0, self._slot_y) + self._rline_to(-self._slot_x + 2 * self._stroke_width, 0) + self._rline_to(0, -self._slot_y) + self._rline_to(-self._stroke_width, 0)
    
    def _do_porch(flag):
        if flag:
            return self._rline_to(0, self._porch_y + self._innie_y1) + self._rline_to(self._porch_x - self._radius, 0) + self._corner(1, 1, 90, 0, 1, True, True, False)

        else:
            return self._rline_to(0, self._porch_y - self._padding) + self._rline_to(self._porch_x - self._radius, 0) + self._corner(1, 1, 90, 0, 1, True, True, False)

    def _start_boolean(xoffset, yoffset):
        svg = self._new_path(xoffset, yoffset) # - self._radius)
        self._radius -= self._stroke_width
        self.docks.append([self._x * self._scale, self._y * self._scale])
        svg += self._rarc_to(1, -1, 90, 0, 1)
        self._radius += self._stroke_width
        svg += self._rline_to(self._stroke_width, 0)
        svg += self._rline_to(0, -self._expand_y)

        return svg
    
    def _do_boolean():
        self.docks.append([(self._x - self._radius + self._stroke_width) * self._scale, (self._y + self._radius) * self._scale])
        self.margins[2] = (self._x - self._radius - self._stroke_width) * self._scale
        svg = self._rarc_to(-1, 1, 90, 0, 0) + self._rarc_to(1, 1, 90, 0, 0)

        return svg
    
    def _end_boolean(notnot):
        if not notnot:
            svg = self._rline_to(-self._radius * 1.5, 0)

        else:
            svg = ''
        
        svg += self._rline_to(0, -self._stroke_width)
        svg += self._rline_to(-self._stroke_width, 0)
        self._radius -= self._stroke_width
        svg += self._rarc_to(-1, -1, 90, 0, 1)
        self._radius += self._stroke_width
        svg += self._close_path()
        self._calculate_w_h(True)
        svg += self._style()

        return svg
    
    def _header(center):
        # FIXME: Why are our calculations off by 2 x strokeWidth?
        width = self._width + 2 * self._stroke_width
        return '<svg xmlns="http:#www.w3.org/2000/svg" width="' + width * 1.1 + '" height="' + self._height * 1.3 + '">' + self._transform(center) + '<filter id="dropshadow" height="130%">\n' +\
            '  <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>\n' +\
            '  <feOffset dx="2" dy="2" result="offsetblur"/>\n' +\
            '  <feComponentTransfer xmlns="http:#www.w3.org/2000/svg">\n' +\
            '    <feFuncA type="linear" slope="0.2"/>\n' +\
            '  </feComponentTransfer>\n' +\
            '  <feMerge>\n' +\
            '    <feMergeNode/>\n' +\
            '    <feMergeNode in="SourceGraphic"/>\n' +\
            '  </feMerge>\n' +\
            '</filter>'
    
    def _transform(center):
        if self._orientation != 0:
            w = self._width / 2.0
            h = self._height / 2.0
            orientation = '<g transform = "rotate(' + self._orientation + ' ' + w + ' ' + h + ')">'

        else:
            orientation = ''
        
        if center:
            x = -self._min_x
            y = -self._min_y

            return '<g transform="translate(' + x + ', ' + y + ')">'

        else:
            return '<g transform="scale(' + self._scale + ', ' + self._scale + ')">' + orientation

    def _footer():
        if self._orientation != 0:
            return '</g></g></svg>'

        else:
            return '</g></svg>'

    def _style():
        return 'style="fill:' + self._fill + 'fill-opacity:1stroke:' + self._stroke + 'stroke-width:' + self._stroke_width + 'stroke-linecap:roundstroke-opacity:1filter:url(#dropshadow)" />'

    """
    The block construction methods typically start on the upper-left side
    of a block and proceed clockwise around the block, first constructing
    a corner (1, -1), a slot or hat on along the top, a corner (1, 1),
    right side connectors ("innies"), possibly a "porch" to suggest an
    order of arguments, another corner (-1, 1), a tab or tail, and the
    fourth corner (-1, -1), and finally, a left-side connector ("outie").
    In addition:
     * Minimum and maximum values are calculated for the SVG bounding box
     * Docking coordinates are calculated for each innies, outie, tab, and slot.
    """

    def basic_block():
        # The most common block type: used for 0, 1, 2, or 3
        # argument commands (forward, setxy, plus, sqrt, etc.)
        self._reset_min_max()

        obj = self._calculate_x_y()
        x = obj[0]
        y = obj[1]

        self.margins[2] = 0
        self.margins[3] = 0

        svg = self._new_path(x, y)
        svg += self._corner(1, -1 , 90, 0, 1, True, True, False)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1 , 90, 0, 1, True, True, False)
        if self._innies.length == 0:
            # To maintain standard block height
            svg += self._rline_to(0, self._padding)
         
        else:
            for i in range(0, len(self._innies)):
                if self._innies[i]:
                    svg += self._do_innie()
                
                if i == 0:
                    svg += self._rline_to(0, self._expand_y)

                elif i == 1 and self._expand_y2 > 0:
                    svg += self._rline_to(0, self._expand_y2)
                
                if i == 0 and self._porch:
                    svg += self._do_porch(False)

                elif self._innies.length - 1 > i:
                    svg += self._rline_to(0, 2 * self._innie_y2 + self._innies_spacer)

        svg += self._corner(-1, 1 , 90, 0, 1, True, True, False)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)

        if self._tab:
            svg += self._do_tab()

        else:
            svg += self._do_tail()
        
        svg += self._corner(-1, -1 , 90, 0, 1, True, True, False)
        svg += self._rline_to(0, -self._expand_y)

        if self._innies.indexOf(True) != -1:
            svg += self._line_to(x, self._radius + self._innie_y2 + self._stroke_width / 2.0)
            svg += self._do_outie()

        self._calculate_w_h(True)
        svg += self._close_path()
        svg += self._style()

        # Add a block label
        tx = self._width - self._scale * (self._innie_x1 + self._innie_x2) - 4 * self._stroke_width
        ty = self._height / 2 + self._font_size / (5 / self._scale)

        # If we have an odd number of innie slots, we need to avoid a
        # collision between the block label and the slot label.
        nInnies = self._innies.length
        if nInnies > 2 and Math.round(nInnies / 2) * 2 != nInnies:
            ty -= 2 * self._font_size

        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'right', 'block_label')

        # Add a label for each innies
        if self._slot or self._outie:
            di = 1  # Skip the first dock since it is a slot.

        else:
            di = 0

        count = 1
        for i in range(0, len(self._innies)):
            if self._innies[i]:
                ty = self.docks[di][1] - (self._font_size / (8 / self._scale))
                svg += self.text(tx / self._scale, ty / self._scale, self._font_size / 1.5, self._width, 'right', 'arg_label_' + count)
                count += 1
                di += 1

        svg += self._footer()

        return self._header(False) + svg
    
    def basic_box():
        # Basic argument style used for numbers, text, media, parameters
        self._reset_min_max()
        self.set_outie(True)

        x = self._stroke_width / 2.0 + self._innie_x1 + self._innie_x2
        self.margins[0] = (x + self._stroke_width + 0.5) * self._scale
        self.margins[1] = (self._stroke_width + 0.5) * self._scale
        self.margins[2] = 0
        self.margins[3] = 0
        
        svg = self._new_path(x, self._stroke_width / 2.0)
        svg += self._rline_to(self._expand_x, 0)
        svg += self._rline_to(0, 2 * self._radius + self._innie_y2 + self._expand_y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._line_to(x, self._radius + self._innie_y2 + self._stroke_width / 2.0)
        svg += self._do_outie()
        svg += self._close_path()
        self._calculate_w_h(True)
        svg += self._style()

        # Add a block label
        tx = 2 * (self._innie_x1 + self._innie_x2) + 4 * self._stroke_width
        ty = self._height / 2 + self._font_size / 2
        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'left', 'block_label')

        svg += self._footer()

        return self._header(False) + svg
    
    def boolean_and_or():
        # Booleans are in a class of their own
        self._reset_min_max()
        svg = self._start_boolean(self._stroke_width / 2.0, self._radius * 5.5 + self._stroke_width / 2.0 + self._innie_y2 + self._innies_spacer + self._expand_y)
        svg += self._rline_to(0, -self._radius * 3.5 - self._innie_y2 - self._innies_spacer - self._stroke_width)

        svg += self._rarc_to(1, -1, 90, 0, 1)
        svg += self._rline_to(self._radius / 2.0 + self._expand_x, 0)
        xx = self._x
        svg += self._rline_to(0, self._radius / 2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0, self._radius * 1.5 + self._innie_y2 + self._innies_spacer)

        svg += self._rline_to(0, self._expand_y)

        svg += self._do_boolean()
        svg += self._rline_to(0, self._radius / 2.0)

        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean(False)
        self.margins[0] = (self._radius + self._stroke_width + 0.5) * self._scale
        self.margins[1] = self._stroke_width * self._scale
        self.margins[2] = self._stroke_width * self._scale
        self.margins[3] = self._stroke_width * self._scale

        # Add a block label
        tx = self._width - self._scale * (self._innie_x1 + self._innie_x2) - 4 * self._stroke_width
        ty = self._height / 2 + self._font_size / 2
        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'right', 'block_label')

        svg += self._footer()

        return self._header(False) + svg
    
    def boolean_not(notnot):
        # Booleans are in a class of their own: not and not not
        self._reset_min_max()
        if self._innies[0]:
            svg = self._start_boolean(self._stroke_width / 2.0, self._radius * 1.25 + self._stroke_width / 2.0)

        elif not notnot:
            svg = self._start_boolean(self._stroke_width / 2.0, self._radius * 2.0 + self._stroke_width / 2.0)

        else:
            svg = self._start_boolean(self._stroke_width / 2.0, self._radius * 1.25 + self._stroke_width / 2.0)
        
        svg += self._rline_to(0, -self._stroke_width)

        if self._innies[0]:
            svg += self._rline_to(0, -self._radius / 4.0)

        elif not notnot:
            svg += self._rarc_to(1, -1, 90, 0, 1)

        else:
            svg += self._rline_to(0, -self._radius / 4.0)
        
        svg += self._rline_to(self._radius / 2.0 + self._expand_x, 0)
        xx = self._x

        if self._innies[0]:
            svg += self._rline_to(0, self._radius)
            svg += self._do_innie()
            svg += self._rline_to(0, self._radius)

        elif not notnot:
            svg += self._rline_to(0, self._radius / 2.0)
            svg += self._do_boolean()
            svg += self._rline_to(0, self._radius / 2.0)

        else:
            svg += self._rline_to(0, self._radius * 2.25)

        svg += self._line_to(xx, self._y)

        # FIXME: Is this in the correct place?
        if self._expand_y2 > 0:
            svg += self._rline_to(0, self._expand_y2)
        

        if self._innies[0]:
            svg += self._rline_to(-self._radius / 2.0 - self._expand_x, 0)
            svg += self._rline_to(0, -self._radius / 4.0)

        elif not notnot:
            svg += self._rline_to(-self._expand_x, 0)

        else:
            svg += self._rline_to(-self._radius / 2.0 - self._expand_x, 0)

        # FIXME: Is this in the correct place?
        if self._expand_y2 > 0:
            svg += self._rline_to(0, -self._expand_y2)

        svg += self._end_boolean(notnot)
        if notnot:
            self.margins[0] = (self._radius + self._stroke_width + 0.5) * self._scale
            self.margins[2] = (self._radius + self._stroke_width + 0.5) * self._scale

        else:
            self.margins[0] = (self._stroke_width + 0.5) * self._scale
            self.margins[2] = (self._stroke_width + 0.5) * self._scale

        self.margins[1] = self._stroke_width * self._scale
        self.margins[3] = self._stroke_width * self._scale

        # Add a block label
        tx = self._width - 2 * (self._innie_x1 + self._innie_x2) - 4 * self._stroke_width
        ty = self._height / 2 + self._font_size / 2
        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'right', 'block_label')

        svg += self._footer()

        return self._header(False) + svg
    
    def boolean_compare():
        # Booleans are in a class of their own (greater than, less than, etc)
        self._reset_min_max()
        yoffset = self._radius * 2 + 2 * self._innie_y2 + self._innies_spacer + self._stroke_width / 2.0 + self._expand_y
        xoffset = self._stroke_width / 2.0

        yoff = self._radius * 2
        svg = '<g transform="matrix(1,0,0,1,0,-' + yoff + ')"> '

        svg += self._new_path(xoffset, yoffset + self._radius)
        self.docks.append([self._x * self._scale, (self._y - 2 * self._radius) * self._scale])
        self._radius -= self._stroke_width
        svg += self._rarc_to(1, -1, 90, 0, 1)
        self._radius += self._stroke_width
        svg += self._rline_to(self._stroke_width, 0)
        svg += self._rline_to(0, -self._expand_y)

        yoffset = -2 * self._innie_y2 - self._innies_spacer - self._stroke_width
        svg += self._rline_to(0, yoffset + self._radius)

        svg += self._rarc_to(1, -1, 90, 0, 1)
        svg += self._rline_to(self._radius / 2.0 + self._expand_x, 0)
        svg += self._rline_to(0, self._radius)
        xx = self._x
        svg += self._do_innie()
        self.docks[1][1] -= self._radius * 2 * self._scale
        svg += self._rline_to(0, self._expand_y)

        if self._porch:
            svg += self._do_porch(False)

        else:
            svg += self._rline_to(0, 2 * self._innie_y2 + self._innies_spacer)

        svg += self._do_innie()
        self.docks[2][1] -= self._radius * 2 * self._scale
        svg += self._rline_to(0, self._radius)
        svg += self._line_to(xx, self._y)

        svg += self._rline_to(-self._expand_x, 0)

        svg += self._rline_to(-self._radius * 1.5, 0)
        svg += self._rline_to(0, -self._radius)
        svg += self._rline_to(0, -self._stroke_width)
        svg += self._rline_to(-self._stroke_width, 0)
        self._radius -= self._stroke_width
        svg += self._rarc_to(-1, -1, 90, 0, 1)
        self._radius += self._stroke_width
        svg += self._close_path()
        self._calculate_w_h(True)
        svg += self._style()
        svg += '</g>'

        self.margins[0] = (self._radius + self._stroke_width) * self._scale
        self.margins[1] = self._stroke_width * self._scale
        self.margins[2] = self._stroke_width * self._scale

        # Add a block label
        tx = self._width - 2 * (self._innie_x1 + self._innie_x2) - 4 * self._stroke_width
        ty = self._height / 2 + self._font_size / 2 # + self._radius * self._scale
        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'right', 'block_label')

        svg += self._footer()

        return self._header(False) + svg
    
    def basic_clamp():
        # Special block for collapsible stacks includes an 'arm'
        # that extends down the left side of a stack and a bottom jaw
        # to clamp the blocks. (Used for start, action, repeat, etc.)
        save_cap = self._cap
        save_slot = self._slot
        self._reset_min_max()
        x = self._stroke_width / 2.0

        if self._cap:
            y = self._stroke_width / 2.0 + self._radius + self._slot_y * 3.0

        else:
            y = self._stroke_width / 2.0 + self._radius

        self.margins[0] = (x + self._stroke_width + 0.5) * self._scale
        self.margins[1] = (self._stroke_width + 0.5) * self._scale
        self.margins[2] = 0
        self.margins[3] = 0

        svg = self._new_path(x, y)
        svg += self._corner(1, -1 , 90, 0, 1, True, True, False)
        svg += self._do_slot()
        if self._cap:
            self._slot = True
            self._cap = False

        svg += self._rline_to(self._radius + self._stroke_width, 0)
        xx = self._x
        svg += self._rline_to(self._expand_x, 0)
        svg += self._corner(1, 1 , 90, 0, 1, True, True, False)

        if self._innies[0]:
            # svg += self._do_innie()
            for i in range(0, len(self._innies)):
                if self._innies[i]:
                    svg += self._do_innie()

                if i == 0:
                    svg += self._rline_to(0, self._expand_y)

                elif i == 1 and self._expand_y2 > 0:
                    svg += self._rline_to(0, self._expand_y2)
                
                if i == 0 and self._porch:
                    svg += self._do_porch(False)

                elif self._innies.length - 1 > i:
                    svg += self._rline_to(0, 2 * self._innie_y2 + self._innies_spacer)

        elif self._bool:
            svg += self._rline_to(0, 2 * self._padding + self._stroke_width)
            svg += self._do_boolean()
            self.margins[2] = (self._x - self._stroke_width + 0.5) * self._scale

        else:
            svg += self._rline_to(0, self._padding)
            self.margins[2] = (self._x - self._stroke_width + 0.5) * self._scale
        

        for clamp in range(0, self._clamp_count):
            if clamp > 0:
                svg += self._rline_to(0, 3 * self._padding)

            svg += self._corner(-1, 1, 90, 0, 1, True, True, False)
            svg += self._line_to(xx, self._y)
            svg += self._do_tab()
            svg += self._icorner(-1, 1, 90, 0, 0, True, True)
            svg += self._rline_to(0, self._padding)

            if self._clamp_slots[clamp] > 1:
                dy = self._slot_size * (self._clamp_slots[clamp] - 1)
                svg += self._rline_to(0, dy)
            
            svg += self._rline_to(0, self._expand_y2)
            svg += self._icorner(1, 1, 90, 0, 0, True, True)
            svg += self._do_slot()

            self.docks.remove(self.docks[-1])  # We don't need this dock.
            svg += self._rline_to(self._radius, 0)
        
        svg += self._rline_to(0, self._innie_y1 * 2)

        # Add a bit of padding to make multiple of standard block height.
        svg += self._rline_to(0, self._innie_y1 + 3 * self._stroke_width)
        svg += self._corner(-1, 1, 90, 0, 1, True, True, False)

        if self._clamp_count == 0:
            svg += self._line_to(xx, self._y)

        svg += self._rline_to(-self._radius - self._stroke_width, 0)

        if self._tail:
            svg += self._do_tail()

        else:
            svg += self._do_tab()

        self._cap = save_cap
        self._slot = save_slot

        svg += self._corner(-1, -1, 90, 0, 1, True, True, False)
        svg += self._close_path()
        self._calculate_w_h(True)
        svg += self._style()

        # Add a block label
        tx = 8 * self._stroke_width
        if self._cap:
            ty = (self._stroke_width / 2.0 + self._radius + self._slot_y) * self._scale

        elif self._innies.length > 1:
            ty = (self._stroke_width / 2.0 + self._radius) * self._scale / 2
            ty += self._font_size
 
        else:
            ty = (self._stroke_width / 2.0 + self._radius) * self._scale / 2

        ty += (self._font_size + 1) * self._scale

        if self._bool:
            ty += self._font_size / 2

        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'left', 'block_label')

        # Booleans get an extra label.
        if self._bool:
            count = 1
            tx = self._width - self._radius
            for clamp in range(0, self._clamp_count):
                ty = self.docks[clamp + 2][1] - self._font_size + 3 * self._stroke_width
                svg += self.text(tx / self._scale, ty / self._scale, self._font_size / 1.5, self._width, 'right', 'arg_label_' + count)
                count += 1

        # Add a label for each innies
        if self._slot or self._outie:
            di = 1  # Skip the first dock since it is a slot.

        else:
            di = 0
        
        count = 1
        tx = self._width - self._scale * (self._innie_x1 + self._innie_x2) - 4 * self._stroke_width
        for i in range(0, len(self._innies)):
            if self._innies[i]:
                ty = self.docks[di][1] - (self._font_size / (8 / self._scale))
                svg += self.text(tx / self._scale, ty / self._scale, self._font_size / 1.5, self._width, 'right', 'arg_label_' + count)
                count += 1
                di += 1

        svg += self._footer()

        return self._header(False) + svg
    
    def arg_clamp():
        # A clamp that contains innies rather than flow blocks
        self._reset_min_max()
        if self._outie:
            x = self._stroke_width / 2.0 + self._innie_x1 + self._innie_x2

        else:
            x = self._stroke_width / 2.0
        
        y = self._stroke_width / 2.0 + self._radius
        self.margins[0] = (x + self._stroke_width + 0.5) * self._scale
        self.margins[1] = (self._stroke_width + 0.5) * self._scale
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._corner(1, -1 , 90, 0, 1, True, True, False)
        svg += self._do_slot()

        svg += self._rline_to(self._radius + self._stroke_width, 0)
        xx = self._x
        svg += self._rline_to(self._expand_x, 0)
        svg += self._corner(1, 1 , 90, 0, 1, True, True, False)

        if self._innies[0]:
            svg += self._do_innie()

        else:
            svg += self._rline_to(0, self._padding)
            self.margins[2] = (self._x - self._stroke_width + 0.5) * self._scale

        svg += self._corner(-1, 1, 90, 0, 1, True, True, False)
        svg += self._line_to(xx, self._y)
        svg += self._icorner(-1, 1, 90, 0, 0, True, True)

        j = 0
        svg += self._do_innie()
        dy = self._slot_size * (self._clamp_slots[0][j] - 1)
        if dy > 0:
            svg += self._rline_to(0, dy)

        j += 1

        ddy = (self._slot_size - self._innie_y2)
        for i in range(0, len(self._clamp_slots[0])):
            svg += self._rline_to(0, ddy)
            svg += self._do_innie()
            dy = self._slot_size * (self._clamp_slots[0][j] - 1)

            if dy > 0:
                svg += self._rline_to(0, dy)
            
            j += 1

        svg += self._rline_to(0, self._expand_y2)
        svg += self._icorner(1, 1, 90, 0, 0, True, True)
        svg += self._rline_to(self._radius, 0)

        svg += self._rline_to(0, self._innie_y1 * 2)

        # Add a bit of padding to make multiple of standard block height.
        svg += self._rline_to(0, self._innie_y1 + 3 * self._stroke_width)

        svg += self._corner(-1, 1, 90, 0, 1, True, True, False)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._radius - self._stroke_width, 0)

        if self._tail:
            svg += self._do_tail()

        else:
            svg += self._do_tab()
        

        svg += self._corner(-1, -1, 90, 0, 1, True, True, False)
        if self._outie:
            svg += self._line_to(x, self._radius + self._innie_y2 + self._stroke_width / 2.0)
            svg += self._do_outie()
        
        svg += self._close_path()
        self._calculate_w_h(True)
        svg += self._style()

        # Add a block label
        if self._outie:
            tx = 10 * self._stroke_width + self._innie_x1 + self._innie_x2
        
        else:
            tx = 8 * self._stroke_width
        
        if self._cap:
            ty = (self._stroke_width / 2.0 + self._radius + self._slot_y) * self._scale

        else:
            ty = (self._stroke_width / 2.0 + self._radius) * self._scale / 2
        
        ty += (self._font_size + 1) * self._scale
        if self._bool:
            ty += self._font_size / 2

        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'left', 'block_label')
        svg += self._footer()

        return self._header(False) + svg
    
    def until_clamp():
        # Until block is like clamp but docks are flipped
        self._reset_min_max()
        x = self._stroke_width / 2.0
        y = self._stroke_width / 2.0 + self._radius
        self.margins[0] = (x + self._stroke_width + 0.5) * self._scale
        self.margins[1] = (self._stroke_width + 0.5) * self._scale
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._corner(1, -1, 90, 0, 1, True, True, False)
        svg += self._do_slot()
        svg += self._rline_to(self._radius + self._stroke_width, 0)
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1, 90, 0, 1, True, True, True)
        svg += self._rline_to(0, 2 * self._innie_y1)
        svg += self._corner(-1, 1, 90, 0, 1, True, True, True)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._do_tab()
        svg += self._icorner(-1, 1, 90, 0, 0, True, True)
        svg += self._rline_to(0, self._expand_y)
        svg += self._icorner(1, 1, 90, 0, 0, True, True)
        svg += self._do_slot()
        self.docks.pop()  # We don't need this dock.
        svg += self._rline_to(self._radius, 0)
        if self._innies[0]:
            svg += self._do_innie()

        else:
            self.margins[2] = (self._x - self._stroke_width + 0.5) * self._scale
        
        svg += self._rline_to(0, self._radius + self._expand_y2)

        if self._bool:
            svg += self._do_boolean()
        
        svg += self._corner(-1, 1, 90, 0, 1, True, True, False)
        svg += self._rline_to(-self._radius - self._stroke_width, 0)
        svg += self._do_tab()
        svg += self._corner(-1, -1, 90, 0, 1, True, True, False)
        svg += self._close_path()
        self._calculate_w_h(True)
        svg += self._style()

        # Add a block label
        tx = 4 * self._stroke_width
        ty = self.docks[2][1]

        svg += self.text(tx / self._scale, ty / self._scale, self._font_size, self._width, 'left', 'block_label')

        if self._bool:
            # Booleans get an extra label.
            tx = self._width - self._radius
            ty = self.docks[1][1] - self._font_size
            svg += self.text(tx / self._scale, ty / self._scale, self._font_size / 1.5, self._width, 'right', 'arg_label_1')
        

        if self._bool:
            # Swap bool and tab args so that the docking behaves like the
            # while block.
            tx = self.docks[1][0]
            ty = self.docks[1][1]
            self.docks[1][0] = self.docks[2][0]
            self.docks[1][1] = self.docks[2][1]
            self.docks[2][0] = tx
            self.docks[2][1] = ty

        svg += self._footer()

        return self._header(False) + svg
    
    def status_block(graphic):
        # Generate a status block
        self._reset_min_max()
        obj = self._calculate_x_y()
        x = obj[0]
        y = obj[1]
        self.margins[2] = 0
        self.margins[3] = 0
        svg = self._new_path(x, y)
        svg += self._corner(1, -1, 90, 0, 1, True, True, False)
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1, 90, 0, 1, True, True, False)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1, 90, 0, 1, True, True, False)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._corner(-1, -1, 90, 0, 1, True, True, False)
        svg += self._rline_to(0, -self._expand_y)
        self._calculate_w_h(True)
        svg += self._close_path()
        svg += self._style()
        svg += self._footer()

        return self._header(False) + svg


#
# Command-line tools for testing
#


def open_file(datapath, filename):
    return file(os.path.join(datapath, filename), "w")


def close_file(f):
    f.close()


def generator(datapath):
    svg = SVG()
    f = open_file(datapath, "start.svg")
    svg.set_scale(2)
    svg.expand(30, 0, 0, 0)
    svg.set_slot(False)
    svg.set_cap(True)
    svg.set_tail(True)
    svg.set_tab(True)
    svg.set_boolean(False)
    svg.second_clamp(False)
    svg_str = svg.clamp()
    f.write(svg_str)
    close_file(f)


def main():
    return 0


if __name__ == "__main__":
    generator(os.path.abspath('.'))
    main()


def svg_str_to_pixbuf(svg_string):
    """ Load pixbuf from SVG string """
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()

    return pixbuf


def svg_str_to_pixmap(svg_string):
    """ Load pixmap from SVG string """
    (pixmap, mask) = svg_str_to_pixbuf(svg_string).render_pixmap_and_mask()

    return pixmap


def svg_from_file(pathname):
    """ Read SVG string from a file """
    f = file(pathname, 'r')
    svg = f.read()
    f.close()

    return svg
