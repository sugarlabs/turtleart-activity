# Copyright (c) 2007-8, Playful Invention Company.
# Copyright (c) 2008-11, Walter Bender
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

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

import cairo
import os

from math import pi

from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import PangoCairo
from .tautils import get_path
from .taconstants import (Color, TMP_SVG_PATH, DEFAULT_PEN_COLOR,
                          DEFAULT_BACKGROUND_COLOR, DEFAULT_FONT)


def wrap100(n):
    ''' A variant on mod... 101 -> 99; 199 -> 1 '''
    n = int(n)
    n %= 200
    if n > 99:
        n = 199 - n
    return n


def calc_shade(c, s, invert=False):
    ''' Convert a color to the current shade (lightness/darkness). '''
    # Assumes 16 bit input values
    if invert:
        if s == -1:
            return int(c)
        elif s < 0:
            return int(c / (1 + s))
        return int((c - 65536 * s) / (1 - s))
    else:
        if s < 0:
            return int(c * (1 + s))
        return int(c + (65536 - c) * s)


def calc_gray(c, g, invert=False):
    ''' Gray is a psuedo saturation calculation. '''
    # Assumes 16 bit input values
    if g == 100:
        return int(c)
    if invert:
        if g == 0:
            return int(c)
        else:
            return int(((c * 100) - (32768 * (100 - g))) / g)
    else:
        return int(((c * g) + (32768 * (100 - g))) / 100)


colors = {}
DEGTOR = pi / 180.
RTODEG = 180. / pi

COLOR_TABLE = (
    0xFF0000, 0xFF0D00, 0xFF1A00, 0xFF2600, 0xFF3300,
    0xFF4000, 0xFF4D00, 0xFF5900, 0xFF6600, 0xFF7300,
    0xFF8000, 0xFF8C00, 0xFF9900, 0xFFA600, 0xFFB300,
    0xFFBF00, 0xFFCC00, 0xFFD900, 0xFFE600, 0xFFF200,
    0xFFFF00, 0xE6FF00, 0xCCFF00, 0xB3FF00, 0x99FF00,
    0x80FF00, 0x66FF00, 0x4DFF00, 0x33FF00, 0x1AFF00,
    0x00FF00, 0x00FF0D, 0x00FF1A, 0x00FF26, 0x00FF33,
    0x00FF40, 0x00FF4D, 0x00FF59, 0x00FF66, 0x00FF73,
    0x00FF80, 0x00FF8C, 0x00FF99, 0x00FFA6, 0x00FFB3,
    0x00FFBF, 0x00FFCC, 0x00FFD9, 0x00FFE6, 0x00FFF2,
    0x00FFFF, 0x00F2FF, 0x00E6FF, 0x00D9FF, 0x00CCFF,
    0x00BFFF, 0x00B3FF, 0x00A6FF, 0x0099FF, 0x008CFF,
    0x0080FF, 0x0073FF, 0x0066FF, 0x0059FF, 0x004DFF,
    0x0040FF, 0x0033FF, 0x0026FF, 0x001AFF, 0x000DFF,
    0x0000FF, 0x0D00FF, 0x1A00FF, 0x2600FF, 0x3300FF,
    0x4000FF, 0x4D00FF, 0x5900FF, 0x6600FF, 0x7300FF,
    0x8000FF, 0x8C00FF, 0x9900FF, 0xA600FF, 0xB300FF,
    0xBF00FF, 0xCC00FF, 0xD900FF, 0xE600FF, 0xF200FF,
    0xFF00FF, 0xFF00E6, 0xFF00CC, 0xFF00B3, 0xFF0099,
    0xFF0080, 0xFF0066, 0xFF004D, 0xFF0033, 0xFF001A)


class TurtleGraphics:

    ''' A class for the Turtle graphics canvas '''

    def __init__(self, turtle_window, width, height):
        ''' Create a sprite to hold the canvas. '''
        self.turtle_window = turtle_window
        self.width = width
        self.height = height
        self.textsize = 48
        self._fgrgb = DEFAULT_PEN_COLOR
        self._bgrgb = DEFAULT_BACKGROUND_COLOR
        self._font = DEFAULT_FONT
        self._shade = 0
        self._color = 0
        self._gray = 100
        self.cr_svg = None  # Surface used for saving to SVG

        # Build a cairo.Context from a cairo.XlibSurface
        self.canvas = cairo.Context(self.turtle_window.turtle_canvas)
        self.set_pen_size(5)

    def setup_svg_surface(self):
        ''' Set up a surface for saving to SVG '''
        svg_surface = cairo.SVGSurface(self.get_svg_path(),
                                       self.width, self.height)
        self.svg_surface = svg_surface
        self.cr_svg = cairo.Context(svg_surface)
        self.cr_svg.set_line_cap(1)  # Set the line cap to be round

    def get_svg_path(self):
        '''We use a separate file for the svg used for generating Sugar icons
        '''
        if self.turtle_window.running_sugar:
            return os.path.join(get_path(self.turtle_window.activity,
                                         'instance'), 'output.svg')
        else:
            return TMP_SVG_PATH

    def fill_polygon(self, poly_points):
        ''' Draw the polygon... '''
        def _fill_polygon(cr, poly_points):
            cr.new_path()
            for i, p in enumerate(poly_points):
                if p[0] == 'move':
                    if i == len(poly_points) - 1 or \
                       poly_points[i + 1][0] not in ['rarc', 'larc']:
                        cr.move_to(p[1], p[2])
                elif p[0] == 'rarc':
                    cr.arc(p[1], p[2], p[3], p[4], p[5])
                elif p[0] == 'larc':
                    cr.arc_negative(p[1], p[2], p[3], p[4], p[5])
                else:  # line
                    cr.line_to(p[1], p[2])
            cr.close_path()
            cr.fill()

        _fill_polygon(self.canvas, poly_points)
        self.inval()
        if self.cr_svg is not None:
            _fill_polygon(self.cr_svg, poly_points)

    def clearscreen(self):
        '''Clear the canvas and reset most graphics attributes to defaults.'''

        def _clearscreen(cr):
            cr.move_to(0, 0)
            self._bgrgb = DEFAULT_BACKGROUND_COLOR
            cr.set_source_rgb(self._bgrgb[0] / 255.,
                              self._bgrgb[1] / 255.,
                              self._bgrgb[2] / 255.)
            cr.rectangle(0, 0, self.width * 2, self.height * 2)
            cr.fill()

        _clearscreen(self.canvas)
        self.inval()
        if self.cr_svg is not None:
            _clearscreen(self.cr_svg)

    def rarc(self, x, y, r, a, heading):
        ''' draw a clockwise arc '''
        def _rarc(cr, x, y, r, a, h):
            cr.arc(x, y, r, (h - 180) * DEGTOR, (h - 180 + a) * DEGTOR)
            cr.stroke()

        _rarc(self.canvas, x, y, r, a, heading)
        self.inval()

        if self.cr_svg is not None:
            _rarc(self.cr_svg, x, y, r, a, heading)

    def larc(self, x, y, r, a, heading):
        ''' draw a counter-clockwise arc '''
        def _larc(cr, x, y, r, a, h):
            cr.arc_negative(x, y, r, h * DEGTOR, (h - a) * DEGTOR)
            cr.stroke()

        _larc(self.canvas, x, y, r, a, heading)
        self.inval()
        if self.cr_svg is not None:
            _larc(self.cr_svg, x, y, r, a, heading)

    def set_pen_size(self, pen_size):
        ''' Set the pen size '''
        self.canvas.set_line_width(pen_size)
        if self.cr_svg is not None:
            self.cr_svg.set_line_width(pen_size)

    def fillscreen(self, c, s):
        ''' Deprecated method: Fill screen with color/shade '''
        self.fillscreen_with_gray(c, s, self._gray)

    def fillscreen_with_gray(self, color, shade, gray):
        ''' Fill screen with color/shade/gray and reset to defaults '''

        save_rgb = self._fgrgb[:]

        # Special case for color blocks
        if isinstance(color, Color):
            if color.color is None:
                self._shade = color.shade
            else:
                self._color = color.color
        else:
            self._color = color
        if isinstance(shade, Color):
            self._shade = shade.shade
        else:
            self._shade = shade
        if isinstance(gray, Color):
            self._gray = gray.gray
        else:
            self._gray = gray

        if self._gray < 0:
            self._gray = 0
        if self._gray > 100:
            self._gray = 100

        self.set_fgcolor(shade=self._shade, gray=self._gray, color=self._color)
        self._bgrgb = self._fgrgb[:]

        def _fillscreen(cr, rgb, w, h):
            cr.set_source_rgb(rgb[0] / 255., rgb[1] / 255., rgb[2] / 255.)
            cr.rectangle(0, 0, w * 2, h * 2)
            cr.fill()

        _fillscreen(self.canvas, self._fgrgb, self.width, self.height)
        self.inval()
        if self.cr_svg is not None:
            _fillscreen(self.cr_svg, self._fgrgb, self.width, self.height)

        self._fgrgb = save_rgb[:]

    def set_fgcolor(self, shade=None, gray=None, color=None):
        ''' Set the foreground color '''
        if shade is not None:
            self._shade = shade
        if gray is not None:
            self._gray = gray
        if color is not None:
            self._color = color
        sh = (wrap100(self._shade) - 50) / 50.0
        rgb = COLOR_TABLE[wrap100(self._color)]
        r = (rgb >> 8) & 0xff00
        r = calc_gray(r, self._gray)
        r = calc_shade(r, sh)
        g = rgb & 0xff00
        g = calc_gray(g, self._gray)
        g = calc_shade(g, sh)
        b = (rgb << 8) & 0xff00
        b = calc_gray(b, self._gray)
        b = calc_shade(b, sh)
        self._fgrgb = [r >> 8, g >> 8, b >> 8]

    def draw_surface(self, surface, x, y, w, h):
        ''' Draw a surface '''

        def _draw_surface(cc, surface, x, y, w, h):
            cc.set_source_surface(surface, x, y)
            cc.rectangle(x, y, w, h)
            cc.fill()

        _draw_surface(self.canvas, surface, x, y, w, h)
        self.inval()
        if self.cr_svg is not None:
            _draw_surface(self.cr_svg, surface, x, y, w, h)

    def draw_pixbuf(self, pixbuf, a, b, x, y, w, h, heading):
        ''' Draw a pixbuf '''

        def _draw_pixbuf(cc, pixbuf, a, b, x, y, w, h, heading):
            # Build a Gdk.CairoContext from a cairo.Context to access
            # the set_source_pixbuf attribute.
            cc.save()
            # center the rotation on the center of the image
            cc.translate(x + w / 2., y + h / 2.)
            cc.rotate(heading * DEGTOR)
            cc.translate(-x - w / 2., -y - h / 2.)
            Gdk.cairo_set_source_pixbuf(cc, pixbuf, x, y)
            cc.rectangle(x, y, w, h)
            cc.fill()
            cc.restore()

        _draw_pixbuf(self.canvas, pixbuf, a, b, x, y, w, h, heading)
        self.inval()
        if self.cr_svg is not None:
            _draw_pixbuf(self.cr_svg, pixbuf, a, b, x, y, w, h, heading)

    def set_font(self, font_name):
        ''' Set font used by draw_text '''
        self._font = str(font_name)

    def draw_text(self, label, x, y, size, width, heading, scale):
        ''' Draw text '''

        def _draw_text(cc, label, x, y, size, width, scale, heading, rgb,
                       wrap=False):
            import textwrap

            final_scale = int(size * scale) * Pango.SCALE
            label = str(label)
            if wrap:
                label = '\n'.join(textwrap.wrap(label, int(width / scale)))

            pl = PangoCairo.create_layout(cc)
            fd = Pango.FontDescription(self._font)
            fd.set_size(final_scale)
            pl.set_font_description(fd)
            if isinstance(label, str):
                text = label.replace('\0', ' ')
            elif isinstance(label, (float, int)):
                text = str(label)
            else:
                text = label

            pl.set_text(text, -1)
            pl.set_width(int(width) * Pango.SCALE)
            cc.save()
            cc.translate(x, y)
            cc.rotate(heading * DEGTOR)
            cc.set_source_rgb(rgb[0] / 255., rgb[1] / 255., rgb[2] / 255.)
            PangoCairo.update_layout(cc, pl)
            PangoCairo.show_layout(cc, pl)
            cc.restore()

        width *= scale
        _draw_text(self.canvas, label, x, y, size, width, scale, heading,
                   self._fgrgb)
        self.inval()
        if self.cr_svg is not None:  # and self.pendown:
            _draw_text(self.cr_svg, label, x, y, size, width, scale, heading,
                       self._fgrgb, wrap=True)

    def set_source_rgb(self):
        r = self._fgrgb[0] / 255.
        g = self._fgrgb[1] / 255.
        b = self._fgrgb[2] / 255.
        self.canvas.set_source_rgb(r, g, b)
        if self.cr_svg is not None:
            self.cr_svg.set_source_rgb(r, g, b)

    def draw_line(self, x1, y1, x2, y2):
        ''' Draw a line '''

        def _draw_line(cr, x1, y1, x2, y2):
            cr.set_line_cap(1)  # Set the line cap to be round
            cr.move_to(x1, y1)
            cr.line_to(x2, y2)
            cr.stroke()

        _draw_line(self.canvas, x1, y1, x2, y2)
        if self.cr_svg is not None:
            _draw_line(self.cr_svg, x1, y1, x2, y2)
        self.inval()

    def get_color_index(self, r, g, b, a=0):
        ''' Find the closest palette entry to the rgb triplet '''
        if self._shade != 50 or self._gray != 100:
            r <<= 8
            g <<= 8
            b <<= 8
            if self._shade != 50:
                sh = (wrap100(self._shade) - 50) / 50.
                r = calc_shade(r, sh, True)
                g = calc_shade(g, sh, True)
                b = calc_shade(b, sh, True)
            if self._gray != 100:
                r = calc_gray(r, self._gray, True)
                g = calc_gray(g, self._gray, True)
                b = calc_gray(b, self._gray, True)
            r >>= 8
            g >>= 8
            b >>= 8
        min_distance = 1000000
        closest_color = -1
        for i, c in enumerate(COLOR_TABLE):
            cr = int((c & 0xff0000) >> 16)
            cg = int((c & 0x00ff00) >> 8)
            cb = int((c & 0x0000ff))
            distance_squared = \
                ((cr - r) ** 2) + ((cg - g) ** 2) + ((cb - b) ** 2)
            if distance_squared == 0:
                return i
            if distance_squared < min_distance:
                min_distance = distance_squared
                closest_color = i
        return closest_color

    def get_pixel(self, x, y):
        ''' Read the pixel at x, y '''
        if self.turtle_window.interactive_mode:
            x = int(x)
            y = int(y)
            w = self.turtle_window.turtle_canvas.get_width()
            h = self.turtle_window.turtle_canvas.get_height()
            if x < 0 or x > (w - 1) or y < 0 or y > (h - 1):
                return(-1, -1, -1, -1)
            # create a new 1x1 cairo surface
            cs = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
            cr = cairo.Context(cs)
            cr.set_source_surface(self.turtle_window.turtle_canvas, -x, -y)
            cr.rectangle(0, 0, 1, 1)
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.fill()
            cs.flush()  # ensure all writing is done
            pixels = cs.get_data()  # Read the pixel
            return (pixels[2], pixels[1], pixels[0], 0)
        else:
            return(-1, -1, -1, -1)

    def svg_close(self):
        ''' Close current SVG graphic '''
        self.cr_svg.show_page()
        self.svg_surface.flush()
        self.svg_surface.finish()

    def svg_reset(self):
        ''' Reset svg flags '''
        self.cr_svg = None

    def inval(self):
        ''' Invalidate a region for gtk '''
        self.turtle_window.inval_all()
