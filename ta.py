import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import os.path
import pickle
from math import atan2, pi
import sys

from sprites import *
from turtlesetup import *
import logo
import turtle

from sugar.datastore import datastore

WIDTH=1200
HEIGHT=780

DEGTOR = 2*pi/360

gc = None
area = None
window = None
draggroup = None
dragpos = (0,0)
current_category = None
category_spr = None
bgcolor = None
block_operation = None
selected_block = None
select_mask = None
firstkey = False
turtlecanvas = None
status_spr = None
turtle_spr = None
hidden_palette_icon = None
selbuttons = None

load_save_folder = None
save_file_name = None

#
# Button Press
#

def buttonpress_cb(win, event):
    global draggroup, dragpos, block_operation, selected_block
    window.grab_focus()
    block_operation = 'click'
    if selected_block!=None: unselect()
    status_spr.setlayer(400)
    pos = xy(event)
    x,y = pos
    spr = findsprite(pos)
    if spr==None: return True 
    if spr.type == 'selbutton':
        select_category(spr)
    elif spr.type == 'tool':
        tooldispatch(spr)
    elif spr.type == 'category':
        block_selector_pressed(x,y)
    elif spr.type == 'block':
        block_pressed(event,x,y,spr)
    elif spr.type == 'turtle':
        turtle_pressed(x,y)
    return True

def block_pressed(event,x,y,spr):
    global draggroup, dragpos, block_operation
    dragpos = x-spr.x,y-spr.y
    draggroup = findgroup(spr)
    for b in draggroup:
        b.setlayer(2000)
    disconnect(spr)

def turtle_pressed(x,y):
    global draggroup, dragpos, block_operation
    dx,dy = x-turtle_spr.x-30,y-turtle_spr.y-30
    if dx*dx+dy*dy > 200: dragpos = ('turn', turtle.heading-atan2(dy,dx)/DEGTOR,0)
    else: dragpos = ('move', x-turtle_spr.x,y-turtle_spr.y)
    draggroup = [turtle_spr]

def block_selector_pressed(x,y):
    if category_spr.image==hidden_palette_icon:
        for i in selbuttons: i.setlayer(800)
        select_category(selbuttons[0])
    else:
        proto = get_proto_from_category(x,y)
        if proto==None: return
        if proto!='hide': new_block_from_category(proto,x,y)
        else: 
            for i in selbuttons: i.hide()
            category_spr.setshape(hidden_palette_icon)
    
  
def new_block_from_category(proto,x,y):
    global draggroup, dragpos, block_operation
    block_operation = 'new'
    if proto == None: return True
    newspr = Sprite(x-20,y-20,proto.image)
    newspr.setlayer(2000)
    dragpos = 20,20
    newspr.type = 'block'
    newspr.proto = proto
    if newspr.proto.name == 'number': newspr.label=100
    newspr.connections = [None]*len(proto.docks)
    for i in range(len(proto.defaults)):
        dock = proto.docks[i+1]
        numproto = blockproto('number')
        numdock = numproto.docks[0]
        nx,ny = newspr.x+dock[2]-numdock[2],newspr.y+dock[3]-numdock[3]
        argspr = Sprite(nx,ny,numproto.image)
        argspr.type = 'block'
        argspr.proto = numproto
        argspr.label = str(proto.defaults[i])
        argspr.setlayer(2000)
        argspr.connections = [newspr,None]
        newspr.connections[i+1] = argspr
    draggroup = findgroup(newspr)
   
def get_proto_from_category(x,y):
#    if current_category.mask == None: return current_category.blockprotos[(y-100)/30]
    dx,dy = x-category_spr.x, y-category_spr.y,
    pixel = getpixel(current_category.mask,dx,dy)
    index = ((pixel%256)>>3)-1
#    print hex(pixel),index
    if index==0: return 'hide'
    index-=1
    if index>len(current_category.blockprotos): return None
    return current_category.blockprotos[index]
    
def select_category(spr):
    global current_category
    if current_category != None: 
        current_category.setshape(current_category.offshape)
    spr.setshape(spr.onshape)
    current_category = spr
    category_spr.setshape(spr.group)

#
# Mouse move
#

def move_cb(win, event): 
    global block_operation
    if draggroup == None: return True
    block_operation = 'move'
    spr = draggroup[0]
    x,y = xy(event)
    if spr.type=='block':
        dragx, dragy = dragpos
        dx,dy = x-dragx-spr.x,y-dragy-spr.y
        for b in draggroup:
            b.move((b.x+dx, b.y+dy))
    elif spr.type=='turtle':
        type,dragx,dragy = dragpos
        if type == 'move':
            dx,dy = x-dragx-spr.x,y-dragy-spr.y
            spr.move((spr.x+dx, spr.y+dy))        
        else:
            dx,dy = x-spr.x-30,y-spr.y-30
            turtle.seth(int(dragx+atan2(dy,dx)/DEGTOR+5)/10*10)
    return True


#
# Button release
#

def buttonrelease_cb(win, event):
    global draggroup, selected_block,firstkey
    if draggroup == None: return True
    spr = draggroup[0]
    x,y = xy(event)
    if spr.type == 'turtle':
        turtle.xcor = turtle_spr.x-turtlecanvas.x-turtle.width/2+30
        turtle.ycor = turtle.height/2-turtle_spr.y+turtlecanvas.y-30
        turtle.move_turtle()
        draggroup = None
        return True
    if block_operation=='move' and category_spr.hit((x,y)):
        for b in draggroup: b.hide()
        draggroup = None
        return True
    snap_to_dock(draggroup)
    for b in draggroup: b.setlayer(650)
    draggroup = None
    if block_operation=='click': 
        if spr.proto.name=='number':
            selected_block = spr
            select_mask.move((spr.x-6,spr.y-6))
            select_mask.setlayer(660)
            firstkey = True
        else: run_stack(spr)
    return True

def snap_to_dock(group):
    d=200
    me = draggroup[0]
    for mydockn in range(len(me.proto.docks)):
        for you in blocks():
            if you in group: continue
            for yourdockn in range(len(you.proto.docks)):
                thisxy = dock_dx_dy(you,yourdockn,me,mydockn)
                if magnitude(thisxy)>d: continue
                d=magnitude(thisxy)
                bestxy=thisxy
                bestyou=you
                bestyourdockn=yourdockn
                bestmydockn=mydockn
    if d<200:
        for b in group: b.move((b.x+bestxy[0],b.y+bestxy[1]))
        me.connections[bestmydockn]=bestyou
        bestyou.connections[bestyourdockn]=me

def dock_dx_dy(block1,dock1n,block2,dock2n):
    if block1.connections[dock1n] != None: return (100,100)
    if block2.connections[dock2n] != None: return (100,100)
    dock1 = block1.proto.docks[dock1n]
    dock2 = block2.proto.docks[dock2n]
    d1type,d1dir,d1x,d1y=dock1[0:4]
    d2type,d2dir,d2x,d2y=dock2[0:4]
    if block1==block2: return (100,100)
    if d1type!=d2type: return (100,100)
    if d1dir==d2dir: return (100,100)
    return (block1.x+d1x)-(block2.x+d2x),(block1.y+d1y)-(block2.y+d2y)


#
# Repaint
#

def expose_cb(win, event):
#    gc.set_foreground(bgcolor)
#    area.draw_rectangle(gc, True, category_spr.x, 0, category_spr.width, HEIGHT)
#    area.draw_rectangle(gc, True, 100, 100, 100, 100)

    redrawsprites()
    return True


#
# Keyboard, new, load, save
#

def keypress_cb(area, event):
    global firstkey
    keyname = gtk.gdk.keyval_name(event.keyval)
#    print keyname
    if (event.get_state()&gtk.gdk.CONTROL_MASK):
        if keyname=="s": save_file()
        if keyname=="k": clear_journal()
        return True
    if selected_block==None: return False
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname in ['minus', 'period']: keyname = {'minus': '-', 'period': '.'}[keyname]
    if len(keyname)>1: return True
    oldnum = selected_block.label
    if firstkey: newnum = numcheck(keyname,'0')
    else: newnum = oldnum+keyname
    selected_block.setlabel(numcheck(newnum,oldnum))
    firstkey = False
    return True

def numcheck(new, old):
    if new in ['-', '.', '-.']: return new
    if new=='.': return '0.'
    try: float(new); return new
    except ValueError,e : return old

def unselect():
    global selected_block
    if selected_block.label in ['-', '.', '-.']: select_block.setlabel('0')
    select_mask.hide()
    selected_block = None

def new_project():
    global save_file_name
    for b in blocks(): b.hide()
    turtlecanvas.setlayer(600)
    toolsprite('hideshow').setshape(toolsprs['hideshow'].offshape)
    turtle.clearscreen()
    save_file_name = None

def load_file():
    '''Pop a load file dialog to allow the user to pick a .ta file to load. Guess that a .png file with the same name resides in the same directory and try to load that too.'''
    global save_file_name
    fname = get_load_name()
    if fname==None: return
    if fname[-3:]=='.ta': fname=fname[0:-3]
    load_files(fname+'.ta', fname+'.png')
    save_file_name = os.path.basename(fname)

def load_files(ta_file, png_file=''):
    '''Load the given TA code file and optional starting image as png file into a new project.'''
    f = open(ta_file, "r")
    data = pickle.load(f)
    f.close()
    new_project()
    read_data(data)
    try:
        load_pict(png_file)
    except:
        '''the picture not loading is OK'''
        print "load_files: picture didn't load"
        pass
    turtlecanvas.inval()

def get_load_name():
    dialog = gtk.FileChooserDialog("Load...", None,
               gtk.FILE_CHOOSER_ACTION_OPEN,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(dialog)

def read_data(data):
    blocks = []
    for b in data: 
        if b[1]=='turtle': load_turtle(b)
        else: spr = load_spr(b); blocks.append(spr)
    for i in range(len(blocks)):
        cons=[]
        for c in data[i][4]:
            if c==None: cons.append(None)
            else: cons.append(blocks[c])
        blocks[i].connections = cons

def load_spr(b):
    btype, label = b[1],None
    if type(btype)==type((1,2)): btype, label = btype
    proto = blockproto(btype)
    spr = Sprite(b[2]+turtlecanvas.x,b[3]+turtlecanvas.y, proto.image)
    spr.type = 'block'
    spr.proto = proto
    if label!=None: spr.label=label
    spr.setlayer(650)
    return spr

def load_turtle(b):
    id, name, xcor, ycor, heading, color, shade, pensize = b
    turtle.setxy(xcor, ycor)
    turtle.seth(heading)
    turtle.setcolor(color)
    turtle.setshade(shade)
    turtle.setpensize(pensize)

def load_pict(fname):
    pict = gtk.gdk.pixbuf_new_from_file(fname)
    turtlecanvas.image.draw_pixbuf(gc, pict, 0, 0, 0, 0)

def save_file():
    '''Pop a save file dialog to allow the user to pick a filename to save their project. Also saves the current art as a .png file with the same name.'''
    global save_file_name
    fname = get_save_name()
    if fname==None: return
    if fname[-3:]=='.ta': fname=fname[0:-3]
    save_data(fname+".ta")
    save_pict(fname+".png")
    save_file_name = os.path.basename(fname)

def get_save_name():
    dialog = gtk.FileChooserDialog("Save..", None,
               gtk.FILE_CHOOSER_ACTION_SAVE,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    if save_file_name!=None: dialog.set_current_name(save_file_name+'.ta')
    return do_dialog(dialog)

def save_data(fname):
    '''Writes the TurtleArt code to the given filename.'''
    f = file(fname, "w")
    bs = blocks()
    data = []
    for i in range(len(bs)): bs[i].id=i
    for b in bs:
        name = b.proto.name
        if name=='number': name=(name,b.label)
        connections = [get_id(x) for x in b.connections]
        data.append((b.id,name,b.x-turtlecanvas.x,b.y-turtlecanvas.y,connections))
    data.append((-1,'turtle',
                  turtle.xcor,turtle.ycor,turtle.heading,
                  turtle.color,turtle.shade,turtle.pensize))
    pickle.dump(data,f)
    f.close()

def save_pict(fname):
    '''Writes the current art to the given filename.'''
    tc = turtlecanvas
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, tc.width, tc.height)
    pixbuf.get_from_drawable(tc.image, tc.image.get_colormap(), 0, 0, 0, 0, tc.width, tc.height)   
    pixbuf.save(fname, 'png')

def get_id(x): 
    if x==None: return None
    return x.id

def do_dialog(dialog):
    global load_save_folder
    result = None
    filter = gtk.FileFilter()
    filter.add_pattern("*.ta")
    filter.set_name("Turtle Art")
    dialog.add_filter(filter)
    dialog.set_current_folder(load_save_folder)
    response = dialog.run()
    if response == gtk.RESPONSE_OK: 
        result = dialog.get_filename()
        load_save_folder = dialog.get_current_folder()
    dialog.destroy()
    return result

def clear_journal():
    jobjects, total_count = datastore.find({'activity': 'org.laptop.TurtleArtActivity'})
    print 'found', total_count, 'entries'
    for jobject in jobjects[:-1]:
        print jobject.object_id
        datastore.delete(jobject.object_id)


#
# Block utilities
#

def run_stack(spr):
    top = find_top_block(spr)
    logo.run_blocks(top, blocks())
    gobject.idle_add(logo.doevalstep)


def disconnect(b):
    if b.connections[0]==None: return
    b2=b.connections[0]
    b2.connections[b2.connections.index(b)] = None
    b.connections[0] = None


def findgroup(b):
    group=[b]
    for b2 in b.connections[1:]:
        if b2!=None: group.extend(findgroup(b2))
    return group

def find_top_block(spr):
    while spr.connections[0]!=None: spr=spr.connections[0]
    return spr

def magnitude(pos):
    x,y = pos
    return x*x+y*y

def xy(event): return map(int, event.get_coords())
def blocks(): return [spr for spr in spritelist() if spr.type == 'block']


#
# Toolbar
#

def tooldispatch(spr):
    if spr.blocktype == 'hideshow': hideshow_blocks(spr)
    elif spr.blocktype == 'eraser': runtool(spr,turtle.clearscreen)
    elif spr.blocktype == 'stopit': logo.step = just_stop()    

def just_stop(): yield False    

def runtool(spr,cmd):
    spr.setshape(spr.onshape)
    cmd()
    gobject.timeout_add(250,spr.setshape,spr.offshape) 
    
def hideshow_blocks(spr):
    if spr.image==spr.offshape:
        for b in blocks(): b.setlayer(100)
        spr.setshape(spr.onshape)
    else:
        for b in blocks(): b.setlayer(650)
        spr.setshape(spr.offshape)
    turtlecanvas.inval()


#
# Startup
#

def init(top_window, path, parentwindow=None):
    global gc, area, category_spr, bgcolor,turtlecanvas, select_mask
    global status_spr, turtle_spr, selbuttons, hidden_palette_icon
    global base_path, load_save_folder, window
    window = top_window
    base_path = path
    if parentwindow is None:
        parentwindow = top_window

    # remove any children of the window that Sugar may have added
    #for widget in window.get_children(): window.remove(widget)
    
    #window.set_title("TurteArt")
    window.connect("destroy", lambda w: gtk.main_quit())
    window.set_flags(gtk.CAN_FOCUS)
    window.set_size_request(WIDTH, HEIGHT)
    window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
    window.add_events(gtk.gdk.POINTER_MOTION_MASK)
    window.add_events(gtk.gdk.KEY_PRESS_MASK)
    window.connect("expose-event", expose_cb)
    window.connect("button-press-event", buttonpress_cb)
    window.connect("button-release-event", buttonrelease_cb)
    window.connect("motion-notify-event", move_cb)
    window.connect("key_press_event", keypress_cb)
    window.show()
    parentwindow.show_all()
    area = window.window
    cursor_pix = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'arrow.gif'))
    cursor = gtk.gdk.Cursor(area.get_display(), cursor_pix, 10, 0)
    area.set_cursor(cursor)
    gc = area.new_gc() 

    setspritecontext(window,area,gc)
    cm = gc.get_colormap()
    bgcolor = cm.alloc_color('#fff8de')

#    who = Sprite(0,0,gtk.gdk.pixbuf_new_from_file('fullscreen.gif'))
#    who.type = 'bg'
#    who.setlayer(700)

    
    turtlecanvas = Sprite(0,0,gtk.gdk.Pixmap(area,WIDTH,HEIGHT,-1))
    turtlecanvas.type = 'canvas'
    turtlecanvas.setlayer(600)
    select_mask = Sprite(100,100,gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'masknumber.gif')))
    select_mask.type = 'selectmask'
    status_spr = Sprite(0,790,gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'status.gif')),True)
    status_spr.type = 'status'
    status_spr.setlayer(400)
    turtle.shapelist = [gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'shapes','t'+str(i)+'.gif')) 
                        for i in range(36)]
    turtle_spr = Sprite(100,100,turtle.shapelist[0])
    turtle_spr.type = 'turtle'
    turtle_spr.setlayer(630)
    turtle.init(window,turtlecanvas, turtle_spr, bgcolor)
    hidden_palette_icon = gtk.gdk.pixbuf_new_from_file(os.path.join(base_path, 'toolbar','blocks-.gif'))
    category_spr, selbuttons, default_category = setup_selectors(base_path)
#    select_category(default_category)
    for i in selbuttons: i.hide()
    category_spr.setshape(hidden_palette_icon)
    setup_toolbar()
    logo.turtle = turtle
    logo.turtle_spr = turtle_spr
    logo.stopsign = toolsprite('stopit')
    logo.status = status_spr
    logo.init()
    load_save_folder = os.path.join(base_path,'samples')

def main():
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    init(win, os.path.abspath('.'))
    gtk.main()
    return 0

if __name__ == "__main__":
    main()
