import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import os.path
class taWindow: pass

WIDTH=1200
HEIGHT=780

from math import atan2, pi
DEGTOR = 2*pi/360

from tasetup import *
from tasprites import *
from talogo import *
from taturtle import *
from taproject import *

#
# Setup
#

def twNew(win, path, parent=None):
    tw = taWindow()
    tw.window = win
    tw.path=path
    win.set_flags(gtk.CAN_FOCUS)
    win.set_size_request(WIDTH, HEIGHT)
    if parent is None: win.show_all()
    else: parent.show_all()
    win.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    win.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
    win.add_events(gtk.gdk.POINTER_MOTION_MASK)
    win.add_events(gtk.gdk.KEY_PRESS_MASK)
    win.connect("expose-event", expose_cb, tw)
    win.connect("button-press-event", buttonpress_cb, tw)
    win.connect("button-release-event", buttonrelease_cb, tw)
    win.connect("motion-notify-event", move_cb, tw)
    win.connect("key_press_event", keypress_cb, tw)
    tw.area = win.window
    tw.gc = tw.area.new_gc()
    tw. cm = tw.gc.get_colormap()
    tw.bgcolor = tw.cm.alloc_color('#fff8de')
    tw.textcolor = tw.cm.alloc_color('black')
    tw.sprites = []
    tw.selected_block = None
    tw.draggroup = None
    setup_selectors(tw)
    setup_toolbar(tw)
    select_category(tw, tw.selbuttons[0])
    tw.turtle = tNew(tw,WIDTH,HEIGHT)
    tw.lc = lcNew(tw)
    tw.load_save_folder = os.path.join(path,'samples')
    tw.save_file_name = None
    return tw


#
# Button Press
#

def buttonpress_cb(win, event, tw):
    win.grab_focus()
    tw.block_operation = 'click'
    if tw.selected_block!=None: unselect(tw)
    setlayer(tw.status_spr,400)
    pos = xy(event)
    x,y = pos
    spr = findsprite(tw,pos)
    if spr==None: return True
    if spr.type == 'selbutton':
        select_category(tw,spr)
    elif spr.type == 'tool':
        tooldispatch(tw, spr)
    elif spr.type == 'category':
        block_selector_pressed(tw,x,y)
    elif spr.type == 'block':
        block_pressed(tw,event,x,y,spr)
    elif spr.type == 'turtle':
        turtle_pressed(tw,x,y)
    return True


def block_selector_pressed(tw,x,y):
    if tw.category_spr.image==tw.hidden_palette_icon:
        for i in tw.selbuttons: setlayer(i,800)
        select_category(tw,tw.selbuttons[0])
    else:
        proto = get_proto_from_category(tw,x,y)
        if proto==None: return
        if proto!='hide': new_block_from_category(tw,proto,x,y)
        else:
            for i in tw.selbuttons: hide(i)
            setshape(tw.category_spr, tw.hidden_palette_icon)

def get_proto_from_category(tw,x,y):
    dx,dy = x-tw.category_spr.x, y-tw.category_spr.y,
    pixel = getpixel(tw.current_category.mask,dx,dy)
    index = ((pixel%256)>>3)-1
    if index==0: return 'hide'
    index-=1
    if index>len(tw.current_category.blockprotos): return None
    return tw.current_category.blockprotos[index]

def select_category(tw, spr):
    if hasattr(tw, 'current_category'):
        setshape(tw.current_category, tw.current_category.offshape)
    setshape(spr, spr.onshape)
    tw.current_category = spr
    setshape(tw.category_spr,spr.group)

def new_block_from_category(tw,proto,x,y):
    tw.block_operation = 'new'
    if proto == None: return True
    newspr = sprNew(tw,x-20,y-20,proto.image)
    setlayer(newspr,2000)
    tw.dragpos = 20,20
    newspr.type = 'block'
    newspr.proto = proto
    if newspr.proto.name == 'number': newspr.label=100
    newspr.connections = [None]*len(proto.docks)
    for i in range(len(proto.defaults)):
        dock = proto.docks[i+1]
        numproto = tw.protodict['number']
        numdock = numproto.docks[0]
        nx,ny = newspr.x+dock[2]-numdock[2],newspr.y+dock[3]-numdock[3]
        argspr = sprNew(tw,nx,ny,numproto.image)
        argspr.type = 'block'
        argspr.proto = numproto
        argspr.label = str(proto.defaults[i])
        setlayer(argspr,2000)
        argspr.connections = [newspr,None]
        newspr.connections[i+1] = argspr
    tw.draggroup = findgroup(newspr)

def block_pressed(tw,event,x,y,spr):
    if event.get_state()&gtk.gdk.CONTROL_MASK:
        newspr = clone_stack(tw,x-spr.x-20,y-spr.y-20, spr)
        tw.dragpos = x-newspr.x,y-newspr.y
        tw.draggroup = findgroup(newspr)
    else:
        tw.dragpos = x-spr.x,y-spr.y
        tw.draggroup = findgroup(spr)
        for b in tw.draggroup: setlayer(b,2000)
        disconnect(spr)

def clone_stack(tw,dx,dy,spr):
    newspr = sprNew(tw,spr.x+dx,spr.y+dy,spr.proto.image)
    newspr.type = spr.type
    newspr.proto = spr.proto
    newspr.label = spr.label
    newspr.connections = [None]*len(spr.proto.docks)
    for i in range(1,len(spr.connections)):
        if(spr.connections[i]==None): continue
        clonearg=clone_stack(tw,dx,dy,spr.connections[i])
        newspr.connections[i]=clonearg
        clonearg.connections[0]=newspr
    setlayer(newspr,2000)
    return newspr

def turtle_pressed(tw,x,y):
    dx,dy = x-tw.turtle.spr.x-30,y-tw.turtle.spr.y-30
    if dx*dx+dy*dy > 200: tw.dragpos = ('turn', tw.turtle.heading-atan2(dy,dx)/DEGTOR,0)
    else: tw.dragpos = ('move', x-tw.turtle.spr.x,y-tw.turtle.spr.y)
    tw.draggroup = [tw.turtle.spr]


#
# Mouse move
#

def move_cb(win, event, tw):
    if tw.draggroup == None: return True
    tw.block_operation = 'move'
    spr = tw.draggroup[0]
    x,y = xy(event)
    if spr.type=='block':
        dragx, dragy = tw.dragpos
        dx,dy = x-dragx-spr.x,y-dragy-spr.y
        for b in tw.draggroup:
            move(b,(b.x+dx, b.y+dy))
    elif spr.type=='turtle':
        type,dragx,dragy = tw.dragpos
        if type == 'move':
            dx,dy = x-dragx-spr.x,y-dragy-spr.y
            move(spr, (spr.x+dx, spr.y+dy))
        else:
            dx,dy = x-spr.x-30,y-spr.y-30
            seth(tw.turtle, int(dragx+atan2(dy,dx)/DEGTOR+5)/10*10)
    return True


#
# Button release
#

def buttonrelease_cb(win, event, tw):
    if tw.draggroup == None: return True
    spr = tw.draggroup[0]
    x,y = xy(event)
    if spr.type == 'turtle':
        tw.turtle.xcor = tw.turtle.spr.x-tw.turtle.canvas.x-tw.turtle.canvas.width/2+30
        tw.turtle.ycor = tw.turtle.canvas.height/2-tw.turtle.spr.y+tw.turtle.canvas.y-30
        move_turtle(tw.turtle)
        tw.draggroup = None
        return True
    if tw.block_operation=='move' and hit(tw.category_spr, (x,y)):
        for b in tw.draggroup: hide(b)
        tw.draggroup = None
        return True
    snap_to_dock(tw)
    for b in tw.draggroup: setlayer(b,650)
    tw.draggroup = None
    if tw.block_operation=='click':
        if spr.proto.name=='number':
            tw.selected_block = spr
            move(tw.select_mask, (spr.x-6,spr.y-6))
            setlayer(tw.select_mask, 660)
            tw.firstkey = True
        else: run_stack(tw, spr)
    return True

def snap_to_dock(tw):
    d=200
    me = tw.draggroup[0]
    for mydockn in range(len(me.proto.docks)):
        for you in blocks(tw):
            if you in tw.draggroup: continue
            for yourdockn in range(len(you.proto.docks)):
                thisxy = dock_dx_dy(you,yourdockn,me,mydockn)
                if magnitude(thisxy)>d: continue
                d=magnitude(thisxy)
                bestxy=thisxy
                bestyou=you
                bestyourdockn=yourdockn
                bestmydockn=mydockn
    if d<200:
        for b in tw.draggroup: move(b,(b.x+bestxy[0],b.y+bestxy[1]))
        blockindock=bestyou.connections[bestyourdockn]
        if blockindock!=None:
            for b in findgroup(blockindock): hide(b)
        bestyou.connections[bestyourdockn]=me
        me.connections[bestmydockn]=bestyou

def dock_dx_dy(block1,dock1n,block2,dock2n):
    dock1 = block1.proto.docks[dock1n]
    dock2 = block2.proto.docks[dock2n]
    d1type,d1dir,d1x,d1y=dock1[0:4]
    d2type,d2dir,d2x,d2y=dock2[0:4]
    if (d2type!='num') or (dock2n!=0):
        if block1.connections[dock1n] != None: return (100,100)
        if block2.connections[dock2n] != None: return (100,100)
    if block1==block2: return (100,100)
    if d1type!=d2type: return (100,100)
    if d1dir==d2dir: return (100,100)
    return (block1.x+d1x)-(block2.x+d2x),(block1.y+d1y)-(block2.y+d2y)

def magnitude(pos):
    x,y = pos
    return x*x+y*y


#
# Repaint
#

def expose_cb(win, event, tw):
#    tw.gc.set_foreground(tw.bgcolor)
#    tw.area.draw_rectangle(tw.gc, True, 0, 0, WIDTH, HEIGHT)
    redrawsprites(tw)
    return True


#
# Keyboard
#

def keypress_cb(area, event,tw):
    keyname = gtk.gdk.keyval_name(event.keyval)
#    print keyname
    if (event.get_state()&gtk.gdk.CONTROL_MASK):
        if keyname=="n": new_project(tw)
        if keyname=="o": load_file(tw)
        if keyname=="s": save_file(tw)
        if keyname=="k": tw.activity.clear_journal()
        return True
    if tw.selected_block==None: return False
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname in ['minus', 'period']: keyname = {'minus': '-', 'period': '.'}[keyname]
    if len(keyname)>1: return True
    oldnum = tw.selected_block.label
    if tw.firstkey: newnum = numcheck(keyname,'0')
    else: newnum = oldnum+keyname
    setlabel(tw.selected_block, numcheck(newnum,oldnum))
    tw.firstkey = False
    return True

def numcheck(new, old):
    if new in ['-', '.', '-.']: return new
    if new=='.': return '0.'
    try: float(new); return new
    except ValueError,e : return old

def unselect(tw):
    if tw.selected_block.label in ['-', '.', '-.']: select_block.setlabel('0')
    hide(tw.select_mask)
    tw.selected_block = None


#
# Block utilities
#

def disconnect(b):
    if b.connections[0]==None: return
    b2=b.connections[0]
    b2.connections[b2.connections.index(b)] = None
    b.connections[0] = None

def run_stack(tw,spr):
    top = find_top_block(spr)
    run_blocks(tw.lc, top, blocks(tw))
    gobject.idle_add(doevalstep, tw.lc)

def findgroup(b):
    group=[b]
    for b2 in b.connections[1:]:
        if b2!=None: group.extend(findgroup(b2))
    return group

def find_top_block(spr):
    while spr.connections[0]!=None: spr=spr.connections[0]
    return spr


def tooldispatch(tw, spr):
    if spr.blocktype == 'hideshow': hideshow_blocks(tw,spr)
    elif spr.blocktype == 'eraser': runtool(tw, spr, clearscreen, tw.turtle)
    elif spr.blocktype == 'stopit': stop_logo(tw)

def runtool(tw, spr, cmd, *args):
    setshape(spr,spr.onshape)
    cmd(*(args))
    gobject.timeout_add(250,setshape,spr,spr.offshape)

def hideshow_blocks(tw,spr):
    if spr.image==spr.offshape:
        for b in blocks(tw): setlayer(b,100)
        setshape(spr,spr.onshape)
    else:
        for b in blocks(tw): setlayer(b,650)
        setshape(spr,spr.offshape)
    inval(tw.turtle.canvas)


def blocks(tw): return [spr for spr in tw.sprites if spr.type == 'block']
def xy(event): return map(int, event.get_coords())

