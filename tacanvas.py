#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-10, Walter Bender

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

import gtk
from math import sin, cos, pi
from sprites import Sprite
import pango

from taconstants import *

def wrap100(n):
    n = int(n)
    n %= 200
    if n>99: n=199-n
    return n

def calc_shade(c,s):
    if s<0: return int(c*(1+s*.8))
    return int(c+(65536-c)*s*.9)

colors = {}
DEGTOR = 2*pi/360

color_table = (
    0xFF0000,0xFF0D00,0xFF1A00,0xFF2600,0xFF3300,
    0xFF4000,0xFF4D00,0xFF5900,0xFF6600,0xFF7300,
    0xFF8000,0xFF8C00,0xFF9900,0xFFA600,0xFFB300,
    0xFFBF00,0xFFCC00,0xFFD900,0xFFE600,0xFFF200,
    0xFFFF00,0xE6FF00,0xCCFF00,0xB3FF00,0x99FF00,
    0x80FF00,0x66FF00,0x4DFF00,0x33FF00,0x1AFF00,
    0x00FF00,0x00FF0D,0x00FF1A,0x00FF26,0x00FF33,
    0x00FF40,0x00FF4D,0x00FF59,0x00FF66,0x00FF73,
    0x00FF80,0x00FF8C,0x00FF99,0x00FFA6,0x00FFB3,
    0x00FFBF,0x00FFCC,0x00FFD9,0x00FFE6,0x00FFF2,
    0x00FFFF,0x00F2FF,0x00E6FF,0x00D9FF,0x00CCFF,
    0x00BFFF,0x00B3FF,0x00A6FF,0x0099FF,0x008CFF,
    0x0080FF,0x0073FF,0x0066FF,0x0059FF,0x004DFF,
    0x0040FF,0x0033FF,0x0026FF,0x001AFF,0x000DFF,
    0x0000FF,0x0D00FF,0x1A00FF,0x2600FF,0x3300FF,
    0x4000FF,0x4D00FF,0x5900FF,0x6600FF,0x7300FF,
    0x8000FF,0x8C00FF,0x9900FF,0xA600FF,0xB300FF,
    0xBF00FF,0xCC00FF,0xD900FF,0xE600FF,0xF200FF,
    0xFF00FF,0xFF00E6,0xFF00CC,0xFF00B3,0xFF0099,
    0xFF0080,0xFF0066,0xFF004D,0xFF0033,0xFF001A)

#
# A class for the Turtle graphics canvas
#
class TurtleGraphics:
    def __init__(self, tw, width, height):
        self.tw = tw
        self.width = width
        self.height = height
        self.canvas = Sprite(tw.sprite_list, 0, 0, 
            gtk.gdk.Pixmap(self.tw.area, self.width, self.height, -1))
        (self.cx, self.cy) = self.canvas.get_xy()
        self.canvas.type = 'canvas'
        self.canvas.set_layer(CANVAS_LAYER)
        self.gc = self.canvas.images[0].new_gc()
        self.tw.active_turtle.show()
        self.shade = 0
        self.clearscreen()

    def clearscreen(self):
        rect = gtk.gdk.Rectangle(0, 0, self.width, self.height)
        self.gc.set_foreground(self.tw.bgcolor)
        self.canvas.images[0].draw_rectangle(self.gc, True, *rect)
        self.invalt(0, 0, self.width, self.height)
        self.setpensize(5)
        self.setcolor(0)
        self.settextcolor(70)
        self.settextsize(32)
        self.setshade(50)
        self.pendown = True
        for turtle_key in iter(self.tw.turtles.dict):
            self.set_turtle(turtle_key)
            self.tw.active_turtle.set_color(0)
            self.tw.active_turtle.set_shade(50)
            self.tw.active_turtle.set_pen_size(5)
            self.tw.active_turtle.set_pen_state(True)
            self.xcor, self.ycor, self.heading = 0, 0, 0
            self.move_turtle()
            self.turn_turtle()
        self.set_turtle(1) # default turtle has key 1

    def forward(self, n):
        n *= self.tw.coord_scale
        self.gc.set_foreground(self.tw.fgcolor)
        oldx, oldy = self.xcor, self.ycor
        try:
            self.xcor += n*sin(self.heading*DEGTOR)
            self.ycor += n*cos(self.heading*DEGTOR)
        except:
            pass
        if self.pendown:
            self.draw_line(oldx, oldy, self.xcor, self.ycor)
        self.move_turtle()

    def seth(self, n):
        try:
             self.heading = n
        except:
            pass
        self.heading%=360
        self.turn_turtle()

    def right(self, n):
        try:
            self.heading += n
        except:
            pass
        self.heading%=360
        self.turn_turtle()

    def arc(self,a,r):
        self.gc.set_foreground(self.tw.fgcolor)
        r *= self.tw.coord_scale
        try:
            if a<0:
                self.larc(-a, r)
            else:
                self.rarc(a, r)
        except:
            pass
        self.move_turtle()
        self.turn_turtle()

    def rarc(self, a, r):
        if r<0:
             r=-r; a=-a
        cx = self.xcor+r*cos(self.heading*DEGTOR)
        cy = self.ycor-r*sin(self.heading*DEGTOR)
        x,y = self.width/2+int(cx-r), self.height/2-int(cy+r)
        w,h = int(2*r), int(2*r)
        if self.pendown:
            self.canvas.images[0].draw_arc(self.gc, False, x, y, w, h,
                                int(180-self.heading-a)*64, int(a)*64)
            self.invalt(x-self.pensize*self.tw.coord_scale/2-3,
                        y-self.pensize*self.tw.coord_scale/2-3,
                        w+self.pensize*self.tw.coord_scale+6,
                        h+self.pensize*self.tw.coord_scale+6)
        self.right(a)
        self.xcor=cx-r*cos(self.heading*DEGTOR)
        self.ycor=cy+r*sin(self.heading*DEGTOR)

    def larc(self, a, r):
        if r<0:
            r=-r; a=-a
        cx = self.xcor-r*cos(self.heading*DEGTOR)
        cy = self.ycor+r*sin(self.heading*DEGTOR)
        x,y = self.width/2+int(cx-r), self.height/2-int(cy+r)
        w,h = int(2*r), int(2*r)
        if self.pendown:
            self.canvas.images[0].draw_arc(self.gc,False, x, y, w, h,
                                       int(360-self.heading)*64, int(a)*64)
            self.invalt(x-self.pensize*self.tw.coord_scale/2-3,
                        y-self.pensize*self.tw.coord_scale/2-3,
                        w+self.pensize*self.tw.coord_scale+6,
                        h+self.pensize*self.tw.coord_scale+6)
        self.right(-a)
        self.xcor=cx+r*cos(self.heading*DEGTOR)
        self.ycor=cy-r*sin(self.heading*DEGTOR)

    def setxy(self, x, y):
        x *= self.tw.coord_scale
        y *= self.tw.coord_scale
        try:
            self.xcor,self.ycor = x,y
        except:
            pass
        self.move_turtle()

    def setpensize(self,ps):
        try:
            if ps<0:
                ps=0;
            self.pensize = ps
        except:
            pass
        self.tw.active_turtle.set_pen_size(ps)
        self.gc.set_line_attributes(int(self.pensize*self.tw.coord_scale),
                     gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_MITER)

    def setcolor(self,c):
        try:
            self.color = c
            self.tcolor = c
        except:
            pass
        self.tw.active_turtle.set_color(c)
        self.set_fgcolor()
        self.set_textcolor()

    def settextcolor(self,c):
        try:
            self.tcolor = c
        except:
            pass
        self.set_textcolor()

    def settextsize(self,c):
        try:
            self.tw.textsize = c
        except:
            pass

    def setshade(self,s):
        try:
            self.shade = s
        except:
            pass
        self.tw.active_turtle.set_shade(s)
        self.set_fgcolor()
        self.set_textcolor()

    def fillscreen(self,c,s):
        oldc, olds = self.color,self.shade
        self.setcolor(c); self.setshade(s)
        rect = gtk.gdk.Rectangle(0,0,self.width,self.height)
        self.gc.set_foreground(self.tw.fgcolor)
        self.canvas.images[0].draw_rectangle(self.gc, True, *rect)
        self.invalt(0,0,self.width,self.height)
        self.setcolor(oldc); self.setshade(olds)

    def set_fgcolor(self):
        sh = (wrap100(self.shade)-50)/50.0
        rgb = color_table[wrap100(self.color)]
        r,g,b = (rgb>>8)&0xff00,rgb&0xff00,(rgb<<8)&0xff00
        r,g,b = calc_shade(r,sh),calc_shade(g,sh),calc_shade(b,sh)
        self.tw.rgb = [r>>8,g>>8,b>>8]
        self.tw.fgcolor = self.tw.cm.alloc_color(r,g,b)

    def set_textcolor(self):
        sh = (wrap100(self.shade)-50)/50.0
        rgb = color_table[wrap100(self.tcolor)]
        r,g,b = (rgb>>8)&0xff00,rgb&0xff00,(rgb<<8)&0xff00
        r,g,b = calc_shade(r,sh),calc_shade(g,sh),calc_shade(b,sh)
        self.tw.textcolor = self.tw.cm.alloc_color(r,g,b)

    def setpen(self,bool):
        self.pendown = bool

    def draw_pixbuf(self,pixbuf,a,b,x,y,w,h):
        w *= self.tw.coord_scale
        h *= self.tw.coord_scale
        self.canvas.images[0].draw_pixbuf(self.gc, pixbuf, a, b, x, y)
        self.invalt(x,y,w,h)

    def draw_text(self, label, x, y, size, w):
        w *= self.tw.coord_scale
        self.gc.set_foreground(self.tw.textcolor)
        fd = pango.FontDescription('Sans')
        try:
            fd.set_size(int(size*self.tw.coord_scale)*pango.SCALE)
        except:
            print "set size (%d) failed" % (int(size*self.tw.coord_scale))
            pass
        if type(label) == str or type(label) == unicode:
            pl = self.tw.window.create_pango_layout(label.replace("\0"," "))
        elif type(label) == float or type(label) == int:
            pl = self.tw.window.create_pango_layout(str(label))
        else:
            print "draw text: Type Error: %s" % (type(label))
            pl = self.tw.window.create_pango_layout(str(label))
        pl.set_font_description(fd)
        pl.set_width(int(w)*pango.SCALE)
        self.canvas.images[0].draw_layout(self.gc,int(x),int(y),pl)
        w,h = pl.get_pixel_size()
        self.invalt(x,y,w,h)

    def draw_line(self,x1,y1,x2,y2):
        x1,y1 = self.width/2+int(x1), self.height/2-int(y1)
        x2,y2 = self.width/2+int(x2), self.height/2-int(y2)
        if x1<x2: minx,maxx=x1,x2
        else: minx,maxx=x2,x1
        if y1<y2: miny,maxy=y1,y2
        else: miny,maxy=y2,y1
        w,h=maxx-minx,maxy-miny
        self.canvas.images[0].draw_line(self.gc,x1,y1,x2,y2)
        self.invalt(minx-self.pensize*self.tw.coord_scale/2-3,
                    miny-self.pensize*self.tw.coord_scale/2-3,
                    w+self.pensize*self.tw.coord_scale+6,
                    h+self.pensize*self.tw.coord_scale+6)

    def turn_turtle(self):
        self.tw.active_turtle.set_heading(self.heading)

    def move_turtle(self):
        x, y = self.width/2+int(self.xcor), self.height/2-int(self.ycor)
        self.tw.active_turtle.move((self.cx+x-30, self.cy+y-30))
        # self.invalt(x-30,y-30,60,60)

    def invalt(self, x, y, w, h):
        rect = gtk.gdk.Rectangle(int(x+self.cx), int(y+self.cy), int(w),int(h))
        self.tw.area.invalidate_rect(rect, False)

    def set_turtle(self, k):
        if not self.tw.turtles.dict.has_key(k):
            # if it is a new turtle, start it in the center of the screen
            self.tw.active_turtle = self.tw.turtles.get_turtle(k, True)
            self.xcor = 0
            self.ycor = 0
            self.heading = 0
            self.move_turtle()
            self.turn_turtle()
            self.tw.active_turtle.set_pen_state(True)
        self.tw.active_turtle = self.tw.turtles.get_turtle(k, False)
        tx, ty = self.tw.active_turtle.get_xy()
        self.xcor = tx+30-self.width/2
        self.ycor = self.height/2-ty-30
        self.heading = self.tw.active_turtle.get_heading()
        self.setcolor(self.tw.active_turtle.get_color())
        self.setshade(self.tw.active_turtle.get_shade())
        self.setpensize(self.tw.active_turtle.get_pen_size())
        self.pendown = self.tw.active_turtle.get_pen_state()
