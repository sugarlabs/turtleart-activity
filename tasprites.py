import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
class taSprite: pass

def findsprite(tw,pos):
    list = tw.sprites[:]
    list.reverse()
    for s in list:
        if hit(s,pos): return s
    return None

def redrawsprites(tw):
    for s in tw.sprites: draw(s)


def sprNew(tw,x,y,image,altlabel=False):
    spr = taSprite()
    spr.tw, spr.x, spr.y = tw,x,y
    setimage(spr,image)
    spr.label = None
    if altlabel: spr.draw_label = draw_label2
    else: spr.draw_label = draw_label1
    return spr

def setimage(spr,image):
    spr.image = image
    if isinstance(image,gtk.gdk.Pixbuf):
        spr.width = image.get_width()
        spr.height = image.get_height()
    else: spr.width,spr.height=image.get_size()


def move(spr,pos):
    inval(spr)
    spr.x,spr.y = pos
    inval(spr)

def setshape(spr,image):
    inval(spr)
    setimage(spr,image)
    inval(spr)

def setlayer(spr, layer):
    sprites = spr.tw.sprites
    if spr in sprites: sprites.remove(spr)
    spr.layer = layer
    for i in range(len(sprites)):
        if layer < sprites[i].layer: sprites.insert(i, spr); inval(spr); return
    sprites.append(spr)
    inval(spr)

def hide(spr):
    if spr not in spr.tw.sprites: return
    inval(spr)
    spr.tw.sprites.remove(spr)

def setlabel(spr,label):
    spr.label = label
    inval(spr)

def inval(spr):
    spr.tw.area.invalidate_rect(gtk.gdk.Rectangle(spr.x,spr.y,spr.width,spr.height), False)

def draw(spr):
    if isinstance(spr.image,gtk.gdk.Pixbuf):
        spr.tw.area.draw_pixbuf(spr.tw.gc, spr.image, 0, 0, spr.x, spr.y)
    else: spr.tw.area.draw_drawable(spr.tw.gc,spr.image,0,0,spr.x,spr.y,-1,-1)
    if spr.label!=None: spr.draw_label(spr,spr.label)

def hit(spr,pos):
    x,y = pos
    if x<spr.x: return False
    if x>spr.x+spr.width: return False
    if y<spr.y: return False
    if y>spr.y+spr.height: return False
    if isinstance(spr.image,gtk.gdk.Pixmap): return True
    dx,dy = x-spr.x, y-spr.y
    return ord(spr.image.get_pixels()[(dy*spr.width+dx)*4+3]) == 255

def draw_label1(spr, label):
    fd = pango.FontDescription('Sans')
    fd.set_size(7*pango.SCALE)
    pl = spr.tw.window.create_pango_layout(str(label))
    pl.set_font_description(fd)
    swidth = pl.get_size()[0]/pango.SCALE
    sheight = pl.get_size()[1]/pango.SCALE
    centerx = spr.x+spr.width/2
    centery = spr.y+spr.height/2
    spr.tw.gc.set_foreground(spr.tw.textcolor)
    spr.tw.area.draw_layout(spr.tw.gc,centerx-swidth/2,centery-sheight/2,pl)

def draw_label2(spr, label):
    fd = pango.FontDescription('Sans')
    fd.set_size(9*pango.SCALE)
    pl = spr.tw.window.create_pango_layout(str(label))
    pl.set_font_description(fd)
    sheight = pl.get_size()[1]/pango.SCALE
    centery = spr.y+spr.height/2
    spr.tw.gc.set_foreground(spr.tw.textcolor)
    spr.tw.area.draw_layout(spr.tw.gc,spr.x+50,centery-sheight/2,pl)


def getpixel(image,x,y):
    array = image.get_pixels()
    offset = (y*image.get_width()+x)*4
    r,g,b,a = ord(array[offset]),ord(array[offset+1]),ord(array[offset+2]),ord(array[offset+3])
    return (a<<24)+(b<<16)+(g<<8)+r


