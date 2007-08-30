import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
#import os.path

from sprites import *

selectors = (
  ('turtle', 37,
    (('clean','clean','noarg'),
     ('forward','forward','onearg',100),
     ('back','back','onearg',100),
     ('left','left','onearg',90),
     ('right','right','onearg',90),
     ('arc','arc','twoargs',90,100),
     ('setxy','setxy','twoargs',0,0),
     ('seth','seth','onearg',0),
     ('xcor','xcor','num'),
     ('ycor','ycor','num'),
     ('heading','heading','num'))),
  ('pen', 30,
    (('penup','penup','noarg'),
     ('pendown','pendown','noarg'),
     ('setpensize','setpensize','1arg',5),
     ('setcolor','setcolor','1arg',0),
     ('setshade','setshade','1arg',50),
     ('fillscreen','fillscreen','twoargs',60,80),
     ('pensize','pensize','num'),
     ('color','color','num'),
     ('shade','shade','num'))),
  ('numbers', 55,
    (('number','','num'),
     ('plus','+','ari'),
     ('minus','-','ari'),
     ('product','*','ari'),
     ('division','/','ari'),
     ('remainder','%','ari2'),
     ('random','random','random',0,100),
     ('greater','greater?','comp'),
     ('less','less?','comp'),
     ('equal','equal?','comp'),
     ('and','and','and'),
     ('or','or','and'),
     ('not','not','not'),
     ('print','print','onearg'))),
  ('flow', 30,
    (('wait','wait','onearg',10),
     ('forever','forever','forever'),
     ('repeat','repeat','repeat',4),
     ('if','if','if'),
     ('stopstack','stopstack','stop'),
     ('ifelse','ifelse','ifelse'),
     ('hspace','nop','hspace'),
     ('vspace','nop','vspace'))),
   ('myblocks', 46,
    (('hat1','nop','start'),
     ('stack1','stack1','noarg'),
     ('hat2','nop','start'),
     ('stack2','stack2','noarg'),
     ('storeinbox1','storeinbox1','1arg'),
     ('box1','box1','num'),
     ('storeinbox2','storeinbox2','1arg'),
     ('box2','box2','num'))))

toolbaritems = (
#    ('new',0,20),('open',70,20), ('save',70,20),
    ('hideshow',700, 725),('eraser',54,725), ('stopit',54,725))
#    ('hideshow',200, 2),('eraser',54,3), ('stopit',54,2))

dockdetails = {
  'noarg':   (('flow',True,37,5),('flow',False,37,44)),
  'onearg':  (('flow',True,37,5),('num',False,74,21),('flow',False,37,44)),
  '1arg':    (('flow',True,37,5),('num',False,74,29),('flow',False,37,59)),
  'twoargs': (('flow',True,37,5),('num',False,74,21),('num',False,74,58),('flow',False,37,81)),
  'forever': (('flow',True,37,5),('flow',False,118,19,'['),('unavailable',False,0,0,']')),
  'repeat':  (('flow',True,37,5),('num',False,86,21),('flow',False,132,54,'['),('flow',False,37,95,']')),
  'num':     (('num',True,0,12),('numend',False,105,12)),
  'if':      (('flow',True,37,5),('logi+',False,80,31),('flow',False,132,79,'['),('flow',False,37,120,']')),
  'ifelse':  (('flow',True,37,5),('logi+',False,80,31),('flow',False,132,79,'['),('flow',False,217,79,']['),('flow',False,37,120,']')),
  'ari':     (('numend',True,12,20),('num',False,39,20)),
  'ari2':    (('numend',True,12,20),('num',False,51,20)),
  'stop':    (('flow',True,37,5),('unavailable',False,0,0)),
  'comp':    (('logi+',True,0,21,'('),('num',False,32,21),('num',False,181,21),('logi-',False,320,21,')')),
  'random':  (('num',True,0,31,'('),('num',False,28,31),('num',False,150,31),('numend',False,279,31,')')),
  'and':     (('logi-',True,28,24),('logi+',False,64,24)),
  'vspace':  (('flow',True,37,5),('flow',False,37,74)),
  'hspace':  (('flow',True,37,14),('flow',False,128,13)),
  'not':     (('logi+',True,0,24),('unavailable',False,0,0),('logi+',False,55,24)),
  'start':   (('start',True,50,0),('flow',False,49,55))
}

protodict = {}
toolsprs = {}
base_path = None

class BlockProto:
    def __init__(self,name):
        self.name = name


def setup_selectors(path):
    global base_path
    base_path = path
    y = 25
    categories = []
    for s in selectors:
        name,dy,blockdescriptions = s
        cat = setup_selector(name,y, blockdescriptions)
        y += dy*3/2
        categories.append(cat)
    category_spr = Sprite(0, 0, categories[0].group)
    category_spr.type = 'category'
    category_spr.setlayer(660)
    return category_spr, categories, categories[0]

def setup_selector(name,y,blockdescriptions):
    offshape = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'palette',name+'off.gif'))
    onshape = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'palette',name+'on.gif'))
    who = Sprite(140,y,offshape)
    who.setlayer(800)
    who.offshape = offshape
    who.onshape = onshape
    who.group = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, name,name+'group.gif'))
    maskname = os.path.join(base_path, name,name+'mask.gif')
    if os.access(maskname, os.F_OK):
        who.mask = gtk.gdk.pixbuf_new_from_file(maskname)
    else: who.mask = None
    who.type = 'selbutton'
    protos = []
    for b in blockdescriptions:
        bname,primname,docktype = b[0:3]
        image = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, name, bname+'.gif'))
        proto = BlockProto(bname)
        proto.image = image
        proto.primname=primname
        proto.defaults=b[3:]
        if docktype in dockdetails: proto.docks=dockdetails[docktype]
        else: proto.docks = docktype
        protodict[bname] = proto
        protos.append(proto)
    who.blockprotos = protos
    return who

def setup_toolbar():
    x,y = 330,0
    for s in toolbaritems:
        name,dx,dy= s
        x += dx
        setup_tool(x,y + dy,name)
    return

def setup_tool(x,y,name):
    offshape = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'toolbar',name+'off.gif'))
    onshape = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'toolbar',name+'on.gif'))
    who = Sprite(x,y,offshape)
    who.setlayer(800)
    who.offshape = offshape
    who.onshape = onshape
    who.type = 'tool'
    who.blocktype = name
    toolsprs[name] = who

def blockproto(name): return protodict[name]

def toolsprite(name): return toolsprs[name]

