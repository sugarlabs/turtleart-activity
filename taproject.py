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
import pickle
try:
    import json
    json.dumps
except (ImportError, AttributeError):
    import simplejson as json
from StringIO import StringIO
import os.path

from tasprites import *
from taturtle import *
from talogo import stop_logo
from sugar.datastore import datastore

nolabel = ['audiooff', 'descriptionoff','journal']
shape_dict = {'journal':'texton', \
              'descriptionoff':'decson', \
              'audiooff':'audioon'}

def new_project(tw):
    stop_logo(tw)
    for b in blocks(tw): hide(b)
    setlayer(tw.turtle.canvas, 600)
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
    try:
        data = pickle.load(f) # old-style data format
    except:
        # print "reading saved json data"
        f.seek(0) # rewind necessary because of pickle.load
        text = f.read()
        io = StringIO(text)
        listdata = json.load(io)
        print listdata
        # listdata = json.decode(text)
        data = tuplify(listdata) # json converts tuples to lists
    f.close()
    new_project(tw)
    read_data(tw,data)

def get_load_name(tw):
    dialog = gtk.FileChooserDialog("Load...", None, \
        gtk.FILE_CHOOSER_ACTION_OPEN, \
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(tw,dialog)

# unpack serialized data sent across a share
def load_string(tw,text):
    io = StringIO(text)
    listdata = json.load(io)
    # listdata = json.decode(text)
    data = tuplify(listdata) # json converts tuples to lists
    new_project(tw)
    read_data(tw,data)

# unpack sserialized data from the clipboard
def clone_stack(tw,text):
    io = StringIO(text)
    listdata = json.load(io)
    # listdata = json.decode(text)
    data = tuplify(listdata) # json converts tuples to lists
    read_stack(tw,data)

# paste stack from the clipboard
def read_stack(tw,data):
    clone = []
    for b in data:
        spr = load_spr(tw,b); clone.append(spr)
    for i in range(len(clone)):
        cons=[]
        for c in data[i][4]:
            if c==None: cons.append(None)
            else: cons.append(clone[c])
        clone[i].connections = cons

def tuplify(t):
    if type(t) is not list:
        return t
    return tuple(map(tuplify, t))

def read_data(tw,data):
    blocks = []
    for b in data:
        if b[1]=='turtle':
            load_turtle(tw,b)
        else: spr = load_spr(tw,b); blocks.append(spr)
    for i in range(len(blocks)):
        cons=[]
        for c in data[i][4]:
            if c==None: cons.append(None)
            else: cons.append(blocks[c])
        blocks[i].connections = cons

def load_spr(tw,b):
    media = None
    btype, label = b[1],None
    if type(btype)==type((1,2)): 
        btype, label = btype
    if btype == 'title':  # for backward compatibility
        btype = 'string'
    if btype == 'journal' or btype == 'audiooff':
        media = label
        label = None
    proto = tw.protodict[btype]
    spr = sprNew(tw,b[2]+tw.turtle.canvas.x,b[3]+tw.turtle.canvas.y, \
        proto.image)
    spr.type = 'block'
    spr.proto = proto
    if label is not None: spr.label=label
    if media is not None and \
        media not in nolabel:
        try:
            dsobject = datastore.get(media)
            spr.ds_id = dsobject.object_id
            setimage(spr, tw.media_shapes[shape_dict[spr.proto.name]])
            if spr.proto.name == 'journal':
                from talogo import get_pixbuf_from_journal
                pixbuf = get_pixbuf_from_journal \
                    (dsobject,spr.width,spr.height)
                if pixbuf is not None:
                    setimage(spr, pixbuf)
            dsobject.destroy()
        except:
            print "couldn't open dsobject (" + str(spr.ds_id) + ")"
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
    if tw.save_folder is not None: tw.load_save_folder = tw.save_folder
    fname = get_save_name(tw)
    if fname==None: return
    if fname[-3:]=='.ta': fname=fname[0:-3]
    save_data(tw,fname+".ta")
    save_pict(tw,fname+".png")
    tw.save_file_name = os.path.basename(fname)

def get_save_name(tw):
    dialog = gtk.FileChooserDialog("Save...", None, \
                                   gtk.FILE_CHOOSER_ACTION_SAVE, \
                                   (gtk.STOCK_CANCEL, \
                                    gtk.RESPONSE_CANCEL, \
                                    gtk.STOCK_SAVE, \
                                    gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    if tw.save_file_name is not None:
        dialog.set_current_name(tw.save_file_name+'.ta')
    return do_dialog(tw,dialog)

def save_data(tw,fname):
    f = file(fname, "w")
    data = assemble_data_to_save(tw)
    io = StringIO()
    json.dump(data,io)
    text = io.getvalue()
    # text = json.encode(data)
    f.write(text)
    f.close()

# Used to send data across a shared session
def save_string(tw):
    data = assemble_data_to_save(tw)
    io = StringIO()
    json.dump(data,io)
    text = io.getvalue()
    # text = json.encode(data)
    return text

def assemble_data_to_save(tw):
    bs = blocks(tw)
    data = []
    for i in range(len(bs)): bs[i].id=i
    for b in bs:
        name = b.proto.name
        if tw.defdict.has_key(name) or name in nolabel:
            if b.ds_id != None:
                name=(name,str(b.ds_id))
            else:
                name=(name,b.label)
        if hasattr(b,'connections'):
            connections = [get_id(x) for x in b.connections]
        else:
            connections = None
        data.append((b.id,name,b.x-tw.turtle.canvas.x, \
            b.y-tw.turtle.canvas.y,connections))
    data.append((-1,'turtle',
                  tw.turtle.xcor,tw.turtle.ycor,tw.turtle.heading,
                  tw.turtle.color,tw.turtle.shade,tw.turtle.pensize))
    return data

# serialize a stack to save to the clipboard
def serialize_stack(tw):
    data = assemble_stack_to_clone(tw)
    io = StringIO()
    json.dump(data,io)
    text = io.getvalue()
    # text = json.encode(data)
    return text

# find the stack under the cursor and serialize it
def assemble_stack_to_clone(tw):
    (x,y) = tw.window.get_pointer()
    # print x,y
    spr = findsprite(tw,(x,y))
    bs = findgroup(find_top_block(spr))

    data = []
    for i in range(len(bs)): bs[i].id=i
    for b in bs:
        name = b.proto.name
        if tw.defdict.has_key(name) or name in nolabel:
            if b.ds_id is not None:
                name=(name,str(b.ds_id))
            else:
                name=(name,b.label)
        if hasattr(b,'connections'):
            connections = [get_id(x) for x in b.connections]
        else:
            connections = None
        data.append((b.id,name,b.x-tw.turtle.canvas.x+20, \
            b.y-tw.turtle.canvas.y+20,connections))
    return data

def save_pict(tw,fname):
    tc = tw.turtle.canvas
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, tc.width, \
                            tc.height)
    pixbuf.get_from_drawable(tc.image, tc.image.get_colormap(), 0, 0, 0, 0, \
                             tc.width, tc.height)
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

def findgroup(b):
    group=[b]
    for b2 in b.connections[1:]:
        if b2!=None: group.extend(findgroup(b2))
    return group

def find_top_block(spr):
    b = spr
    while b.connections[0]!=None:
        b=b.connections[0]
    return b

