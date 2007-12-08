import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
class taProto: pass

from tasprites import *

selectors = (
  ('turtle', 55,
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
  ('pen', 55,
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
     ('not','not','not'),     ('print','print','onearg'))),
  ('flow', 55,
    (('wait','wait','onearg',10),
     ('forever','forever','forever'),
     ('repeat','repeat','repeat',4),
     ('if','if','if'),
     ('stopstack','stopstack','stop'),
     ('ifelse','ifelse','ifelse'),
     ('hspace','nop','hspace'),
     ('vspace','nop','vspace'))),
   ('myblocks', 55,
    (('hat1','nop','start'),
     ('stack1','stack1','noarg'),
     ('hat2','nop','start'),
     ('stack2','stack2','noarg'),
     ('storeinbox1','storeinbox1','1arg'),
     ('box1','box1','num'),
     ('storeinbox2','storeinbox2','1arg'),
     ('box2','box2','num'))))

toolbaritems = (
    ('hideshow',990),('eraser',75), ('stopit',75))

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


def setup_selectors(tw):
    tw.protodict = {}
    y = 30
    tw.selbuttons = []
    for s in selectors:
        name,dy,blockdescriptions = s
        cat = setup_selector(tw,name,y, blockdescriptions)
        y += dy
        tw.selbuttons.append(cat)
    tw.category_spr = sprNew(tw,0, 0, tw.selbuttons[0].group)
    tw.category_spr.type = 'category'
    setlayer(tw.category_spr,660)
    tw.select_mask = sprNew(tw,100,100,load_image(tw.path, '', 'masknumber'))
    tw.select_mask.type = 'selectmask'
    tw.hidden_palette_icon = load_image(tw.path, 'toolbar','blocks-')
    tw.status_shapes = {}
    tw.status_shapes['status'] = load_image(tw.path, '', 'status')
    tw.status_shapes['nostack'] = load_image(tw.path, '', 'nostack')
    tw.status_shapes['noinput'] = load_image(tw.path, '', 'noinput')
    tw.status_spr = sprNew(tw,0,743,tw.status_shapes['status'],True)
 #   tw.status_spr = sprNew(tw,0,670,tw.status_shapes['status'],True)
    tw.status_spr.type = 'status'
    setlayer(tw.status_spr,400)

def setup_selector(tw,name,y,blockdescriptions):
    offshape = load_image(tw.path,'palette',name+'off')
    onshape = load_image(tw.path,'palette',name+'on')
    who = sprNew(tw,143,y,offshape)
    setlayer(who,800)
    who.offshape = offshape
    who.onshape = onshape
    who.group = load_image(tw.path, name,name+'group')
    who.mask = load_image(tw.path, name,name+'mask')
    who.type = 'selbutton'
    protos = []
    for b in blockdescriptions:
        bname,primname,docktype = b[0:3]
        image = load_image(tw.path, name, bname)
        proto = taProto()
        proto.name = bname
        proto.image = image
        proto.primname=primname
        proto.defaults=b[3:]
        if docktype in dockdetails: proto.docks=dockdetails[docktype]
        else: proto.docks = docktype
        tw.protodict[bname] = proto
        protos.append(proto)
    who.blockprotos = protos
    return who

def setup_toolbar(tw):
    tw.toolsprs = {}
    x,y = 0,10
    for s in toolbaritems:
        name,dx= s
        x += dx
        tw.toolsprs[name]=setup_tool(tw,x,y,name)
    return

def setup_tool(tw,x,y,name):
    offshape = load_image(tw.path, 'toolbar',name+'off')
    onshape = load_image(tw.path, 'toolbar',name+'on')
    who = sprNew(tw,x,y,offshape)
    setlayer(who,800)
    who.offshape = offshape
    who.onshape = onshape
    who.type = 'tool'
    who.blocktype = name
    return who

def load_image(path, dir, file):
    return gtk.gdk.pixbuf_new_from_file(os.path.join(path,dir,file+'.gif'))
