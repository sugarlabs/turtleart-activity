#Copyright (c) 2007-8, Playful Invention Company.

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
from math import sin,cos,pi
class taTurtle: pass

from tasprites import *
from tasetup import load_image

colors = {}
DEGTOR = 2*pi/360

color_table = (
    0xFF0000,0xFF0D00,0xFF1A00,0xFF2600,0xFF3300,0xFF4000,0xFF4D00,0xFF5900,0xFF6600,0xFF7300,
    0xFF8000,0xFF8C00,0xFF9900,0xFFA600,0xFFB300,0xFFBF00,0xFFCC00,0xFFD900,0xFFE600,0xFFF200,
    0xFFFF00,0xE6FF00,0xCCFF00,0xB3FF00,0x99FF00,0x80FF00,0x66FF00,0x4DFF00,0x33FF00,0x1AFF00,
    0x00FF00,0x00FF0D,0x00FF1A,0x00FF26,0x00FF33,0x00FF40,0x00FF4D,0x00FF59,0x00FF66,0x00FF73,
    0x00FF80,0x00FF8C,0x00FF99,0x00FFA6,0x00FFB3,0x00FFBF,0x00FFCC,0x00FFD9,0x00FFE6,0x00FFF2,
    0x00FFFF,0x00F2FF,0x00E6FF,0x00D9FF,0x00CCFF,0x00BFFF,0x00B3FF,0x00A6FF,0x0099FF,0x008CFF,
    0x0080FF,0x0073FF,0x0066FF,0x0059FF,0x004DFF,0x0040FF,0x0033FF,0x0026FF,0x001AFF,0x000DFF,
    0x0000FF,0x0D00FF,0x1A00FF,0x2600FF,0x3300FF,0x4000FF,0x4D00FF,0x5900FF,0x6600FF,0x7300FF,
    0x8000FF,0x8C00FF,0x9900FF,0xA600FF,0xB300FF,0xBF00FF,0xCC00FF,0xD900FF,0xE600FF,0xF200FF,
    0xFF00FF,0xFF00E6,0xFF00CC,0xFF00B3,0xFF0099,0xFF0080,0xFF0066,0xFF004D,0xFF0033,0xFF001A)

def tNew(tw,w,h):
    t = taTurtle()
    t.tw, t.width, t.height = tw, w, h
    t.canvas = sprNew(tw,0,0,gtk.gdk.Pixmap(tw.area,w,h,-1))
    t.canvas.type = 'canvas'
    setlayer(t.canvas,600)
    t.shapelist = [load_image(tw.path, 'shapes','t'+str(i)) for i in range(36)]
    t.spr = sprNew(tw,100,100,t.shapelist[0])
    t.spr.type = 'turtle'
    setlayer(t.spr, 630)
    t.gc = t.canvas.image.new_gc()
    t.shade = 0
    clearscreen(t)
    return t

def clearscreen(t):
    t.xcor, t.ycor, t.heading = 0,0,0
    rect = gtk.gdk.Rectangle(0,0,t.width,t.height)
    t.gc.set_foreground(t.tw.bgcolor)
    t.canvas.image.draw_rectangle(t.gc, True, *rect)
    invalt(t,0,0,t.width,t.height)
    setpensize(t,5)
    setcolor(t,0)
    setshade(t,50)
    t.pendown = True
    move_turtle(t)
    turn_turtle(t)
    return None

def forward(t, n):
    t.gc.set_foreground(t.fgcolor)
    oldx, oldy = t.xcor, t.ycor
    t.xcor += n*sin(t.heading*DEGTOR)
    t.ycor += n*cos(t.heading*DEGTOR)
    if t.pendown: draw_line(t,oldx,oldy,t.xcor,t.ycor)
    move_turtle(t)
    return None

def seth(t,n):
    t.heading=n
    t.heading%=360
    turn_turtle(t)
    return None

def right(t,n):
    t.heading+=n
    t.heading%=360
    turn_turtle(t)
    return None

def arc(t,a,r):
    t.gc.set_foreground(t.fgcolor)
    if a<0: larc(t,-a,r)
    else: rarc(t,a,r)
    move_turtle(t)
    turn_turtle(t)

def rarc(t,a,r):
    if r<0: r=-r; a=-a
    cx = t.xcor+r*cos(t.heading*DEGTOR)
    cy = t.ycor-r*sin(t.heading*DEGTOR)
    x,y,w,h=t.width/2+int(cx-r),t.height/2-int(cy+r),int(2*r),int(2*r)
    t.canvas.image.draw_arc(t.gc,False,x,y,w,h,int(180-t.heading-a)*64,int(a)*64)
    invalt(t,x-t.pensize/2-3,y-t.pensize/2-3,w+t.pensize+6,h+t.pensize+6)
    right(t,a)
    t.xcor=cx-r*cos(t.heading*DEGTOR)
    t.ycor=cy+r*sin(t.heading*DEGTOR)

def larc(t,a,r):
    if r<0: r=-r; a=-a
    cx = t.xcor-r*cos(t.heading*DEGTOR)
    cy = t.ycor+r*sin(t.heading*DEGTOR)
    x,y,w,h=t.width/2+int(cx-r),t.height/2-int(cy+r),int(2*r),int(2*r)
    t.canvas.image.draw_arc(t.gc,False,x,y,w,h,int(360-t.heading)*64,int(a)*64)
    invalt(t,x-t.pensize/2-3,y-t.pensize/2-3,w+t.pensize+6,h+t.pensize+6)
    right(t,-a)
    t.xcor=cx+r*cos(t.heading*DEGTOR)
    t.ycor=cy-r*sin(t.heading*DEGTOR)

def setxy(t,x,y):
    t.xcor,t.ycor = x,y
    move_turtle(t)

def setpensize(t,ps):
    if ps<0: ps=0;
    t.pensize = ps
    t.gc.set_line_attributes(int(t.pensize),gtk.gdk.LINE_SOLID,gtk.gdk.CAP_ROUND,gtk.gdk.JOIN_MITER)
    return None

def setcolor(t,c):
    t.color = c
    set_fgcolor(t)
    return None

def setshade(t,s):
    t.shade = s
    set_fgcolor(t)
    return None

def fillscreen(t,c,s):
    oldc, olds = t.color,t.shade
    setcolor(t,c); setshade(t,s)
    rect = gtk.gdk.Rectangle(0,0,t.width,t.height)
    t.gc.set_foreground(t.fgcolor)
    t.canvas.image.draw_rectangle(t.gc, True, *rect)
    invalt(t,0,0,t.width,t.height)
    setcolor(t,oldc); setshade(t,olds)
    return None

def set_fgcolor(t):
    sh = (wrap100(t.shade)-50)/50.0
    rgb = color_table[wrap100(t.color)]
    r,g,b = (rgb>>8)&0xff00,rgb&0xff00,(rgb<<8)&0xff00
    r,g,b = calc_shade(r,sh),calc_shade(g,sh),calc_shade(b,sh)
    t.fgcolor = t.tw.cm.alloc_color(r,g,b)

def wrap100(n):
    n = int(n)
    n %= 200
    if n>99: n=199-n
    return n

def calc_shade(c,s):
    if s<0: return int(c*(1+s*.8))
    return int(c+(65536-c)*s*.9)

def setpen(t,bool):
    t.pendown = bool

def draw_line(t,x1,y1,x2,y2):
    x1,y1 = t.width/2+int(x1), t.height/2-int(y1)
    x2,y2 = t.width/2+int(x2), t.height/2-int(y2)
    if x1<x2: minx,maxx=x1,x2
    else: minx,maxx=x2,x1
    if y1<y2: miny,maxy=y1,y2
    else: miny,maxy=y2,y1
    w,h=maxx-minx,maxy-miny
    t.canvas.image.draw_line(t.gc,x1,y1,x2,y2)
    invalt(t,minx-t.pensize/2-3,miny-t.pensize/2-3,w+t.pensize+6,h+t.pensize+6)

def turn_turtle(t):
    setshape(t.spr, t.shapelist[(int(t.heading+5)%360)/10])

def move_turtle(t):
    x,y = t.width/2+int(t.xcor), t.height/2-int(t.ycor)
    move(t.spr, (t.canvas.x+x-30,t.canvas.y+y-30))
    invalt(t,x-30,y-30,60,60)

def invalt(t,x,y,w,h):
    rect = gtk.gdk.Rectangle(int(x+t.canvas.x),int(y+t.canvas.y),int(w),int(h))
    t.tw.area.invalidate_rect(rect, False)


