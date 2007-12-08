import pygtk
pygtk.require('2.0')
import gtk
import pickle
import os.path

from tasprites import *
from taturtle import *
from talogo import stop_logo

def new_project(tw):
    stop_logo(tw)
    for b in blocks(tw): hide(b)
    setlayer(tw.turtle.canvas, 600)
    setshape(tw.toolsprs['hideshow'], tw.toolsprs['hideshow'].offshape)
    clearscreen(tw.turtle)
    tw.save_file_name = None

def load_file(tw):
    fname = get_load_name(tw)
    if fname==None: return
    if fname[-3:]=='.ta': fname=fname[0:-3]
    load_files(tw,fname+'.ta', fname+'.png')
    tw.save_file_name = os.path.basename(fname)

def load_files(tw,ta_file, png_file=''):
    f = open(ta_file, "r")
    data = pickle.load(f)
    f.close()
    new_project(tw)
    read_data(tw,data)
    try:
        load_pict(tw,png_file)
    except:
        print "load_files: picture didn't load"
        pass
    inval(tw.turtle.canvas)

def get_load_name(tw):
    dialog = gtk.FileChooserDialog("Load...", None,
               gtk.FILE_CHOOSER_ACTION_OPEN,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(tw,dialog)

def read_data(tw,data):
    blocks = []
    for b in data:
        if b[1]=='turtle': load_turtle(tw,b)
        else: spr = load_spr(tw,b); blocks.append(spr)
    for i in range(len(blocks)):
        cons=[]
        for c in data[i][4]:
            if c==None: cons.append(None)
            else: cons.append(blocks[c])
        blocks[i].connections = cons

def load_spr(tw,b):
    btype, label = b[1],None
    if type(btype)==type((1,2)): btype, label = btype
    proto = tw.protodict[btype]
    spr = sprNew(tw,b[2]+tw.turtle.canvas.x,b[3]+tw.turtle.canvas.y, proto.image)
    spr.type = 'block'
    spr.proto = proto
    if label!=None: spr.label=label
    setlayer(spr,650)
    return spr

def load_turtle(tw,b):
    id, name, xcor, ycor, heading, color, shade, pensize = b
    setxy(tw.turtle, xcor, ycor)
    seth(tw.turtle, heading)
    setcolor(tw.turtle, color)
    setshade(tw.turtle, shade)
    setpensize(tw.turtle, pensize)

def load_pict(tw,fname):
    pict = gtk.gdk.pixbuf_new_from_file(fname)
    tw.turtle.canvas.image.draw_pixbuf(tw.turtle.gc, pict, 0, 0, 0, 0)

def save_file(tw):
    if tw.save_folder != None: tw.load_save_folder = tw.save_folder
    fname = get_save_name(tw)
    if fname==None: return
    if fname[-3:]=='.ta': fname=fname[0:-3]
    save_data(tw,fname+".ta")
    save_pict(tw,fname+".png")
    tw.save_file_name = os.path.basename(fname)

def get_save_name(tw):
    dialog = gtk.FileChooserDialog("Save..", None,
               gtk.FILE_CHOOSER_ACTION_SAVE,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    if tw.save_file_name!=None: dialog.set_current_name(tw.save_file_name+'.ta')
    return do_dialog(tw,dialog)

def save_data(tw,fname):
    f = file(fname, "w")
    bs = blocks(tw)
    data = []
    for i in range(len(bs)): bs[i].id=i
    for b in bs:
        name = b.proto.name
        if name=='number': name=(name,b.label)
        connections = [get_id(x) for x in b.connections]
        data.append((b.id,name,b.x-tw.turtle.canvas.x,b.y-tw.turtle.canvas.y,connections))
    data.append((-1,'turtle',
                  tw.turtle.xcor,tw.turtle.ycor,tw.turtle.heading,
                  tw.turtle.color,tw.turtle.shade,tw.turtle.pensize))
    pickle.dump(data,f)
    f.close()

def save_pict(tw,fname):
    tc = tw.turtle.canvas
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, tc.width, tc.height)
    pixbuf.get_from_drawable(tc.image, tc.image.get_colormap(), 0, 0, 0, 0, tc.width, tc.height)
    pixbuf.save(fname, 'png')

def get_id(x):
    if x==None: return None
    return x.id

def do_dialog(tw,dialog):
    result = None
    filter = gtk.FileFilter()
    filter.add_pattern("*.ta")
    filter.set_name("Turtle Art")
    dialog.add_filter(filter)
    dialog.set_current_folder(tw.load_save_folder)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        result = dialog.get_filename()
        tw.load_save_folder = dialog.get_current_folder()
    dialog.destroy()
    return result

def blocks(tw): return [spr for spr in tw.sprites if spr.type == 'block']
