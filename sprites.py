import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango

sprites = []
gc = None
window = None
black = None

class Sprite:
    def __init__(self,x,y,image,altlabel=False):
        self.x = x
        self.y = y
        self.setimage(image)
        self.label = None
        if altlabel: self.draw_label = self.draw_label2
        else: self.draw_label = self.draw_label1

    def setimage(self,image):
        self.image = image
        if isinstance(image,gtk.gdk.Pixbuf):
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else: self.width,self.height=image.get_size()
        
        
    def move(self,pos):
        self.inval()
        self.x,self.y = pos
        self.inval()

    def setshape(self,image):
        self.inval()
        self.setimage(image)
        self.inval()

    def setlayer(self, layer):
        if self in sprites: sprites.remove(self)
        self.layer = layer
        for i in range(len(sprites)):
            if layer < sprites[i].layer: sprites.insert(i, self); self.inval(); return
        sprites.append(self)
        self.inval()
        
    def hide(self):
        if self not in sprites: return
        self.inval()
        sprites.remove(self)

    def setlabel(self,label):
        self.label = label
        self.inval()
 
    def inval(self): 
        area.invalidate_rect(gtk.gdk.Rectangle(self.x,self.y,self.width,self.height), False)
        
    def draw(self):
        if isinstance(self.image,gtk.gdk.Pixbuf): area.draw_pixbuf(gc, self.image, 0, 0, self.x, self.y)
        else: area.draw_drawable(gc,self.image,0,0,self.x,self.y,-1,-1)
        if self.label!=None: self.draw_label(self.label)
        
    def hit(self,pos):
        x,y = pos
        if x<self.x: return False
        if x>self.x+self.width: return False
        if y<self.y: return False
        if y>self.y+self.height: return False
        if isinstance(self.image,gtk.gdk.Pixmap): return True 
        dx,dy = x-self.x, y-self.y
        return ord(self.image.get_pixels()[(dy*self.width+dx)*4+3]) == 255

    def draw_label1(self, label):
        fd = pango.FontDescription('Sans')
        fd.set_size(7*pango.SCALE)
        pl = window.create_pango_layout(str(label))
        pl.set_font_description(fd)
        swidth = pl.get_size()[0]/pango.SCALE
        sheight = pl.get_size()[1]/pango.SCALE
        centerx = self.x+self.width/2
        centery = self.y+self.height/2
        gc.set_foreground(black)
        area.draw_layout(gc,centerx-swidth/2,centery-sheight/2,pl)

    def draw_label2(self, label):
        fd = pango.FontDescription('Sans')
        fd.set_size(9*pango.SCALE)
        pl = window.create_pango_layout(str(label))
        pl.set_font_description(fd)
        sheight = pl.get_size()[1]/pango.SCALE
        centery = self.y+self.height/2
        gc.set_foreground(black)
        area.draw_layout(gc,self.x+50,centery-sheight/2,pl)


def findsprite(pos):
    list = sprites[:]
    list.reverse()
    for s in list:
        if s.hit(pos): return s
    return None

def redrawsprites(): 
    for s in sprites: s.draw()

def getpixel(image,x,y):
    array = image.get_pixels()
    offset = (y*image.get_width()+x)*4
    r,g,b,a = ord(array[offset]),ord(array[offset+1]),ord(array[offset+2]),ord(array[offset+3])
    return (a<<24)+(b<<16)+(g<<8)+r
        
def setspritecontext(w,a,g):
    global window,area,gc,black
    window=w
    area =a
    gc = g
    black = gc.get_colormap().alloc_color('black')
    
def spritelist(): return sprites