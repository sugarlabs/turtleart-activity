import gtk
from math import sin,cos,pi

colors = {}
buffer = None
gc = None
window = None
width = 0
height = 0
sprite = None
cm = None
bgcolor = None
fgcolor = None
color = 0
shade = 50
pensize = 5
pendown = True
turtle = None

DEGTOR = 2*pi/360

xcor = 0
ycor = 0
heading = 0

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

def init(win, spr, tspr, bg):
    global buffer, gc, window, sprite, width, height, bgcolor, fgcolor, cm, turtle
    window, sprite, buffer, turtle, bgcolor = win.window, spr, spr.image, tspr, bg
    width, height = buffer.get_size()
    gc = win.window.new_gc() 
    cm = gc.get_colormap()
    gc = buffer.new_gc()
    clearscreen()
    
def clearscreen():
    global xcor,ycor,heading, pendown
    xcor, ycor, heading = 0,0,0
    rect = gtk.gdk.Rectangle(0,0,width,height)
    gc.set_foreground(bgcolor)
    buffer.draw_rectangle(gc, True, *rect)
    inval(0,0,width,height)
    setpensize(5)
    setcolor(0)
    setshade(50)
    pendown = True
    move_turtle()
    turn_turtle()
    return None
    
def forward(n):
    global xcor,ycor
    gc.set_foreground(fgcolor)
    oldx, oldy = xcor, ycor
    xcor += n*sin(heading*DEGTOR)
    ycor += n*cos(heading*DEGTOR)
    if pendown: draw_line(oldx,oldy,xcor,ycor)
    move_turtle()
    return None

def seth(n):
    global heading
    heading=n
    heading%=360
    turn_turtle()
    return None

def right(n):
    global heading
    heading+=n
    heading%=360
    turn_turtle()
    return None

def arc(a,r):
    gc.set_foreground(fgcolor)
    if a<0: larc(-a,r)
    else: rarc(a,r)
    move_turtle()
    turn_turtle()
    
def rarc(a,r):
    global xcor,ycor
    if r<0: r=-r; a=-a
    cx = xcor+r*cos(heading*DEGTOR)
    cy = ycor-r*sin(heading*DEGTOR)
    x,y,w,h=width/2+int(cx-r),height/2-int(cy+r),int(2*r),int(2*r)
    buffer.draw_arc(gc,False,x,y,w,h,int(180-heading-a)*64,int(a)*64)
    inval(x-pensize/2-3,y-pensize/2-3,w+pensize+6,h+pensize+6)
    right(a)
    xcor=cx-r*cos(heading*DEGTOR)
    ycor=cy+r*sin(heading*DEGTOR)

def larc(a,r):
    global xcor,ycor
    if r<0: r=-r; a=-a
    cx = xcor-r*cos(heading*DEGTOR)
    cy = ycor+r*sin(heading*DEGTOR)
    x,y,w,h=width/2+int(cx-r),height/2-int(cy+r),int(2*r),int(2*r)
    buffer.draw_arc(gc,False,x,y,w,h,int(360-heading)*64,int(a)*64)
    inval(x-pensize/2-3,y-pensize/2-3,w+pensize+6,h+pensize+6)
    right(-a)
    xcor=cx+r*cos(heading*DEGTOR)
    ycor=cy-r*sin(heading*DEGTOR)

def setxy(x,y):
    global xcor,ycor
    xcor,ycor = x,y
    move_turtle()

def setpensize(ps):
    global pensize
    pensize = ps
    gc.set_line_attributes(int(pensize),gtk.gdk.LINE_SOLID,gtk.gdk.CAP_ROUND,gtk.gdk.JOIN_MITER)
    return None

def setcolor(c):
    global color
    color = c
    set_fgcolor()
    return None

def setshade(s):
    global shade
    shade = s
    set_fgcolor()
    return None

def fillscreen(c,s):
    oldc, olds = color,shade
    setcolor(c); setshade(s)
    rect = gtk.gdk.Rectangle(0,0,width,height)
    gc.set_foreground(fgcolor)
    buffer.draw_rectangle(gc, True, *rect)
    inval(0,0,width,height)
    setcolor(oldc); setshade(olds)
    return None
    
def set_fgcolor():
    global fgcolor
    sh = (wrap100(shade)-50)/50.0
    rgb = color_table[wrap100(color)]
    r,g,b = (rgb>>8)&0xff00,rgb&0xff00,(rgb<<8)&0xff00
    r,g,b = calc_shade(r,sh),calc_shade(g,sh),calc_shade(b,sh)
    fgcolor = cm.alloc_color(r,g,b)

def wrap100(n):
    n = int(n)
    n %= 200
    if n>99: n=199-n
    return n

def calc_shade(c,s):
    if s<0: return int(c*(1+s*.8))
    return int(c+(65536-c)*s*.9)

def setpen(bool):
    global pendown
    pendown = bool

def draw_line(x1,y1,x2,y2):
    x1,y1 = width/2+int(x1), height/2-int(y1)
    x2,y2 = width/2+int(x2), height/2-int(y2)
    if x1<x2: minx,maxx=x1,x2
    else: minx,maxx=x2,x1
    if y1<y2: miny,maxy=y1,y2
    else: miny,maxy=y2,y1
    w,h=maxx-minx,maxy-miny
    buffer.draw_line(gc,x1,y1,x2,y2)
    inval(minx-pensize/2-3,miny-pensize/2-3,w+pensize+6,h+pensize+6)

def turn_turtle():
    turtle.setshape(shapelist[(int(heading+5)%360)/10])

def move_turtle():
    x,y = width/2+int(xcor), height/2-int(ycor)
    turtle.move((sprite.x+x-30,sprite.y+y-30))
    inval(x-30,y-30,60,60)

def inval(x,y,w,h):
    rect = gtk.gdk.Rectangle(int(x+sprite.x),int(y+sprite.y),int(w),int(h))
    window.invalidate_rect(rect, False)


