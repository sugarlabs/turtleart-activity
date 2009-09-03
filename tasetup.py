#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-9, Walter Bender

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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
class taProto: pass
import time

from gettext import gettext as _

from tasprites import *

def numcheck(new, old):
    if new in ['-', '.', '-.']: return new
    if new=='.': return '0.'
    try: float(new); return new
    except ValueError,e : return old

def strcheck(new, old):
    try: str(new); return new
    except ValueError,e : return old

# proto name, primitive name, dock details, arguments
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
     ('show','show','onesarg',_('text')),
     ('setscale','setscale','onearg',33),
     ('show','show','onecarg','None'),
     ('xcor','xcor','num'),
     ('ycor','ycor','num'),
     ('heading','heading','num'),
     ('scale','scale','num'),
     # not selectable, but here for backward compatability 
     ('container','container','container','None'),
     ('image','insertimage','image','None'),
     ('write','write','1sarg',_('text'),32))),
  ('pen', 55,
    (('penup','penup','noarg'),
     ('pendown','pendown','noarg'),
     ('setpensize','setpensize','1arg',5),
     ('setcolor','setcolor','1arg',0),
     ('setshade','setshade','1arg',50),
     ('fillscreen','fillscreen','twoargs',60,80),
     ('settextsize','settextsize','1arg',32),
     ('settextcolor','settextcolor','1arg',0),
     ('pensize','pensize','num'),
     ('color','color','num'),
     ('shade','shade','num'),
     ('textcolor','textcolor','num'),
     ('textsize','textsize','num'))),
  ('numbers', 55,
    (('number','','num',100,float,numcheck),
     ('plus2','plus','newari'),
     ('minus2','minus','newari2'),
     ('product2','product','newari'),
     ('division2','division','newari2'),
     ('remainder2','mod','newari2'),
     ('sqrt','sqrt','sqrt',100),
     ('identity','id','id'),
     ('identity2','id','id2'),
     ('random','random','random',0,100),
     ('greater','greater?','comp'),
     ('less','less?','comp'),
     ('equal','equal?','comp'),
     ('and','and','and'),
     ('or','or','and'),
     ('not','not','not'),
     ('print','print','onearg'),
     # not selectable, but here for backward compatability 
     ('minus','-','ari'),
     ('product','*','ari'),
     ('division','/','ari'),
     ('remainder','%','ari2'),
     ('plus','+','ari'))),
  ('sensors', 55,
    (('kbinput','kbinput','noarg2'),
     ('keyboard','keyboard','num'),
     ('nop','userdefined','onearg',100),
     ('myfunc','myfunc','myfunc',_('x'),100),
     ('hres','hres','num'),
     ('vres','vres','num'),
     ('push','push','onearg'),
     ('pop','pop','num'),
     ('printheap','heap','noarg2'),
     ('clearheap','emptyheap','noarg2'),
     ('leftpos','leftpos','num'),
     ('toppos','toppos','num'),
     ('rightpos','rightpos','num'),
     ('bottompos','bottompos','num'))),
  ('flow', 55,
    (('wait','wait','onearg',10),
     ('forever','forever','forever'),
     ('repeat','repeat','repeat',4),
     ('if','if','if'),
     ('stopstack','stopstack','stop'),
     ('ifelse','ifelse','ifelse'),
     ('hspace','nop','hspace'),
     ('vspace','nop','vspace'),
     # not selectable, but here for backward compatability 
     ('lock','nop','lock'))),
   ('myblocks', 55,
    (('start','start','start'),
     ('hat1','nop1','start'),
     ('stack1','stack1','noarg'),
     ('hat2','nop2','start'),
     ('stack2','stack2','noarg'),
     ('hat','nop3','starts',_('stack')),
     ('stack','stack','sarg',_('stack')),
     ('storeinbox1','storeinbox1','1arg'),
     ('box1','box1','num'),
     ('storeinbox2','storeinbox2','1arg'),
     ('box2','box2','num'),
     ('storein','storeinbox','1varg',_('box'),100),
     ('box','box','nfuncs',_('box')),
     ('string','','string',_('name'),str,strcheck),
     # not selectable, but here for backward compatability 
     ('storeinbox','storeinbox','1sarg',_('box'),100))),
  ('templates',55,
    (('journal','','media','','',''),
     ('audiooff','','audio','','',''),
     ('descriptionoff','','text','','',''),
     ('template1','tp1','tp1',_('title'),'None'),
     ('template6','tp6','tp6',_('title'),'None','None'),
     ('template2','tp2','tp2',_('title'),'None','None'),
     ('template7','tp7','tp7',_('title'),'None','None','None','None'),
     ('template3','tp3','tp3',_('title'),'','','','','','',''),
     ('template4','tp8','tp1',_('title'),'None'),
     ('hideblocks','hideblocks','noarg2'),
     # not selectable, but here for backward compatability
     ('sound','sound','sound','None'))))

dockdetails = {
  'noarg':   (('flow',True,37,5),('flow',False,37,44)),
  'noarg2':  (('flow',True,37,5),('flow',False,37,59)),
  'onearg':  (('flow',True,37,5),('num',False,74,21),('flow',False,37,44)),
  'onesarg':  (('flow',True,37,5),('string',False,74,21),('flow',False,37,44)),
  'onecarg':  (('flow',True,37,5),('media',False,74,21),('flow',False,37,44)),
  '1arg':    (('flow',True,37,5),('num',False,74,29),('flow',False,37,59)),
  'twoargs': (('flow',True,37,5),('num',False,74,21),('num',False,74,58), \
        ('flow',False,37,81)),
  'forever': (('flow',True,37,5),('flow',False,118,19,'['), \
        ('unavailable',False,0,0,']')),
  'repeat':  (('flow',True,37,5),('num',False,86,21), \
        ('flow',False,132,54,'['),('flow',False,37,95,']')),
  'num':     (('num',True,0,12),('numend',False,105,12)),
  'if':      (('flow',True,37,5),('logi+',False,80,31),
        ('flow',False,132,79,'['),('flow',False,37,120,']')),
  'ifelse':  (('flow',True,37,5),('logi+',False,80,31), \
        ('flow',False,132,79,'['),('flow',False,217,79,']['), \
        ('flow',False,37,120,']')),
  'ari':     (('numend',True,12,20),('num',False,39,20)),
  'newari':  (('num',True,0,36),('num',False,40,20),('num',False,40,53)),
  'newari2':  (('num',True,0,36),('num',False,40,20),('num',False,59,53)),
  'ari2':    (('numend',True,12,20),('num',False,51,20)),
  'sqrt':    (('num',True,0,20),('num',False,42,20)),
  'stop':    (('flow',True,37,5),('unavailable',False,0,0)),
  'comp':    (('logi+',True,0,21,'('),('num',False,32,21), \
        ('num',False,181,21),('logi-',False,320,21,')')),
  'random':  (('num',True,0,31,'('),('num',False,28,31), \
        ('num',False,150,31),('numend',False,279,31,')')),
  'and':     (('logi-',True,28,24),('logi+',False,64,24)),
  'vspace':  (('flow',True,37,5),('flow',False,37,74)),
  'hspace':  (('flow',True,37,14),('flow',False,128,13)),
  'id':      (('num',True,0,12),('num',False,40,40)),
  'id2':     (('num',True,0,48),('num',False,40,19)),
  'lock':    (('flow',True,37,514),('flow',False,235,13)),
  'not':     (('logi+',True,0,24),('unavailable',False,0,0), \
        ('logi+',False,55,24)),
  'start':   (('start',True,50,0),('flow',False,49,55)),
  'string':  (('string',True,0,11),('stringend',False,105,11)),
  'nfuncs':  (('num',True,0,17),('string',False,18,16), \
        ('numend',False,128,17)), 
  'starts':  (('start',True,50,0),('string',False,21,38), \
        ('flow',False,75,75)), 
  'sarg':    (('flow',True,37,5),('string',False,12,23), \
        ('flow',False,37,44)),  
  '1sarg':   (('flow',True,37,5),('string',False,12,22), \
        ('num',False,130,23),('flow',False,37,44)),
  '1varg':   (('flow',True,37,5),('string',False,12,38), \
        ('num',False,130,30),('flow',False,37,59)),
  'myfunc':   (('num',True,0,22),('string',False,24,22), \
        ('num',False,142,22)),
  'media':   (('media',True,0,27),('mediaend',False,75,27)),
  'text':   (('media',True,0,27),('mediaend',False,75,27)),
  'audio':   (('media',True,0,27),('mediaend',False,75,27)),
  'container':     (('num',True,0,33),('media',False,19,33), \
        ('numend',False,100,33)),
  'tp1':     (('flow',True,37,5),('string',False,10,26), \
        ('media',False,10,73),('flow',False,37,113)),
  'tp2':     (('flow',True,37,5),('string',False,10,26), \
        ('media',False,10,73),('media',False,90,73),('flow',False,37,167)),
  'tp3':     (('flow',True,37,5),('string',False,10,25), \
        ('string',False,10,51),('string',False,10,77), \
        ('string',False,10,103),('string',False,10,129), \
        ('string',False,10,155), ('string',False,10,181), \
        ('string',False,10,207),('flow',False,37,230)),
  'image':     (('flow',True,37,5),('media',False,10,48), \
        ('flow',False,37,89)),
  'sound':     (('flow',True,37,5),('audio',False,128,29), \
        ('flow',False,37,55)),
  'tp6':     (('flow',True,37,5),('string',False,10,26), \
        ('media',False,10,73),('media',False,10,130),('flow',False,37,167)),
  'tp7':     (('flow',True,37,5),('string',False,10,26), \
        ('media',False,10,73),('media',False,90,73),('media',False,10,130), \
        ('media',False,90,130),('flow',False,37,167)),
  'string1': (('flow',True,37,5),('string',False,10,29),('flow',False,37,55))
}

def count_up(self):
    time.sleep(1)
    return True

def prep_selectors(tw):
    tw.protodict = {}
    tw.valdict = {}
    tw.defdict = {}
    tw.y = 30
    tw.selbuttons = []

def setup_selectors(tw,s):
    name,dy,blockdescriptions = s      
    cat = setup_selector(tw, name, tw.y, blockdescriptions)
    tw.y += dy
    tw.selbuttons.append(cat)

def setup_misc(tw):
    tw.category_spr = sprNew(tw,0, 0, tw.selbuttons[0].group)
    tw.category_spr.type = 'category'
    setlayer(tw.category_spr,660)
    # masks get positioned on top of other blocks
    tw.select_mask = sprNew(tw,100,100,load_image(tw.path, '', 'masknumber'))
    tw.select_mask.type = 'selectmask'
    tw.select_mask_string = sprNew(tw,100,100,load_image(tw.path, '', \
        'maskstring'))
    tw.select_mask_string.type = 'selectmask'
    # used to hide the palette
    tw.hidden_palette_icon = load_image(tw.path, '','blocks-')
    # media blocks get positioned into other blocks
    tw.media_shapes = {}
    tw.media_shapes['audioon'] = load_image(tw.path, '', 'audioon')
    tw.media_shapes['texton'] = load_image(tw.path, '', 'texton')
    tw.media_shapes['journalon'] = load_image(tw.path, '', 'journalon')
    tw.media_shapes['decson'] = load_image(tw.path, '', 'descriptionon')
    # media blocks that replace other blocks
    tw.media_shapes['pythonloaded'] = \
        load_image(tw.path_lang, 'sensors', 'nop-loaded')
    # status shapes get positioned at the bottom of the screen
    tw.status_shapes = {}
    tw.status_shapes['status'] = load_image(tw.path, '', 'status')
    tw.status_shapes['info'] = load_image(tw.path, '', 'info')
    tw.status_shapes['nostack'] = load_image(tw.path, '', 'nostack')
    tw.status_shapes['noinput'] = load_image(tw.path, '', 'noinput')
    tw.status_shapes['emptyheap'] = load_image(tw.path, '', 'emptyheap')
    tw.status_shapes['emptybox'] = load_image(tw.path, '', 'emptybox')
    tw.status_shapes['nomedia'] = load_image(tw.path, '', 'nomedia')
    tw.status_shapes['nocode'] = load_image(tw.path, '', 'nocode')
    tw.status_shapes['syntaxerror'] = load_image(tw.path, '', 'syntaxerror')
    tw.status_spr = sprNew(tw,0,(tw.height-175), \
            tw.status_shapes['status'],True)
    tw.status_spr.type = 'status'
    setlayer(tw.status_spr,400)
    # everything should be loaded at this point
    tw.loaded = True

def setup_selector(tw,name,y,blockdescriptions):
    # selector tabs
    offshape = load_image(tw.path, 'palette', name+'off')
    onshape = load_image(tw.path, 'palette', name+'on')
    spr = sprNew(tw,143,y,offshape)
    setlayer(spr,800)
    spr.offshape = offshape
    spr.onshape = onshape
    # print 'setting up selector ' + name
    spr.group = load_image(tw.path_lang, name, name+'group')
    spr.mask = load_image(tw.path, '', name+'mask')
    spr.type = 'selbutton'
    spr.name = name
    # block prototypes
    protos = []
    for b in blockdescriptions:
        bname,primname,docktype = b[0:3]
        image = load_image(tw.path_lang, name, bname)
        proto = taProto()
        proto.name = bname
        proto.image = image
        proto.primname=primname
        if primname=='':
          tw.valdict[docktype]=bname
          tw.defdict[bname]=b[3]
          proto.eval=b[4]
          proto.check=b[5]
          proto.defaults=[]
        else:
          proto.defaults=b[3:]
        if docktype in dockdetails: proto.docks=dockdetails[docktype]
        else: proto.docks = docktype
        tw.protodict[bname] = proto
        protos.append(proto)
    spr.blockprotos = protos
    return spr

def load_image(path, dir, file):
    from sugar.activity import activity
    
    try:
        datapath = os.path.join(activity.get_activity_root(), "data")
    except:
        # early versions of Sugar (656) didn't support get_activity_root()
        datapath = os.path.join( \
            os.environ['HOME'], \
            ".sugar/default/org.laptop.TurtleArtActivity/data")

    # first try to open the cached image
    # then try to open .png file
    # if you fail, open the .svg file and cache the result as png
    try:
        return gtk.gdk.pixbuf_new_from_file(os.path.join(datapath, file+'.png'))
    except:
        try:
            print "trying ... " + os.path.join(path, dir, file+'.png')
            return gtk.gdk.pixbuf_new_from_file(os.path.join(path, dir, \
                                                             file+'.png'))
        except:
            foo = gtk.gdk.pixbuf_new_from_file(os.path.join(path, dir, \
                                                            file +'.svg'))
            foo.save(os.path.join(datapath, file+'.png'), "png")
            return foo

