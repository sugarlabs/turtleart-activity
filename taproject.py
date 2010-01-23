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
    _old_Sugar_system = False
    import json
    json.dumps
    from json import load as jload
    from json import dump as jdump
except (ImportError, AttributeError):
    try:
        import simplejson as json
        from simplejson import load as jload
        from simplejson import dump as jdump
    except:
        # use pickle on old systems
        _old_Sugar_system = True
        # will try json.read and .write too

from StringIO import StringIO
import os.path

# from tasprites import *
from taturtle import *
from talogo import stop_logo
from talogo import get_pixbuf_from_journal
try:
    from sugar.datastore import datastore
except:
    pass
import block
import sprites
from constants import *
from gettext import gettext as _

nolabel = ['audiooff', 'descriptionoff', 'journal']
shape_dict = {'journal':'texton', \
              'descriptionoff':'decson', \
              'audiooff':'audioon'}

def new_project(tw):
    stop_logo(tw)
    for b in blocks(tw): b.hide()
    tw.turtle.canvas.set_layer(CANVAS_LAYER)
    clearscreen(tw.turtle)
    tw.save_file_name = None

def load_file(tw, create_new_project=True):
    fname = get_load_name(tw)
    if fname==None: return
    if fname[-3:]=='.ta': fname=fname[0:-3]
    load_files(tw,fname+'.ta', create_new_project)
    if create_new_project is True:
        tw.save_file_name = os.path.basename(fname)

def load_files(tw, ta_file, create_new_project=True):
    # ignoring the png_file even if it is present
    f = open(ta_file, "r")
    try:
        data = pickle.load(f) # old-style data format
    except:
        # print "reading saved json data"
        f.seek(0) # rewind necessary because of pickle.load
        text = f.read()
        if _old_Sugar_system is True:
            listdata = json.read(text)
        else:
            io = StringIO(text)
            listdata = jload(io)
        print "load files: %s" % (listdata)
        # listdata = jdecode(text)
        data = tuplify(listdata) # json converts tuples to lists
    f.close()
    if create_new_project is True:
        new_project(tw)
    read_data(tw,data)

def get_load_name(tw):
    dialog = gtk.FileChooserDialog("Load...", None, 
        gtk.FILE_CHOOSER_ACTION_OPEN,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(tw,dialog)

# unpack serialized data sent across a share
def load_string(tw,text):
    if _old_Sugar_system is True:
        listdata = json.read(text)
    else:
        io = StringIO(text)
        listdata = jload(io)
    data = tuplify(listdata) # json converts tuples to lists
    new_project(tw)
    read_data(tw,data)

# unpack sserialized data from the clipboard
def clone_stack(tw,text):
    if _old_Sugar_system is True:
        listdata = json.read(text)
    else:
        io = StringIO(text)
        listdata = jload(io)
    data = tuplify(listdata) # json converts tuples to lists
    # read_stack(tw,data)
    read_data(tw,data)

# paste stack from the clipboard
# TODO: rebase on read data 
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
    sprs = []
    for b in data:
        if b[1]=='turtle':
            load_turtle(tw,b)
        else: spr = load_spr(tw, b); sprs.append(spr)
    for i in range(len(sprs)):
        cons=[]
        for c in data[i][4]:
            if c==None: cons.append(None)
            else: cons.append(sprs[c])
        sprs[i].connections = cons # phasing out
        tw.block_list.spr_to_block(sprs[i]).connections = cons

def load_spr(tw,b):
    media = None
    btype, label = b[1],None
    if type(btype) == type((1,2)): 
        btype, label = btype
    if btype == 'title':  # for backward compatibility
        btype = 'string'
    if btype == 'journal' or btype == 'audiooff' or btype == 'descriptionoff':
        media = label
        label = None
    try:
        proto = tw.protodict[btype]
    except KeyError:
        print "swapping in a forward block for %s" % (btype)
        proto = tw.protodict['forward']
    blk = block.Block(tw.block_list, tw.sprite_list, 
                      btype, b[2]+tw.turtle.cx,
                      b[3]+tw.turtle.cy, [label])
    spr = blk.spr
    spr.type = 'block' # phasing out
    spr.proto = proto  # phasing out
    # if label is not None: spr.set_label(label) # phasing out
    if media is not None and media not in nolabel:
        try:
            dsobject = datastore.get(media)
            spr.ds_id = dsobject.object_id
            setimage(spr, tw.media_shapes[shape_dict[spr.proto.name]])
            if spr.proto.name == 'journal':
                pixbuf = get_pixbuf_from_journal(dsobject,
                                                 spr.width,spr.height)
                if pixbuf is not None:
                    setimage(spr, pixbuf)
            dsobject.destroy()
        except:
            if hasattr(spr,"ds_id"):
                print "couldn't open dsobject (" + str(spr.ds_id) + ")"
    spr.set_layer(BLOCK_LAYER)
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
    dialog = gtk.FileChooserDialog("Save...", None,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL,
                                    gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_SAVE,
                                    gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    if tw.save_file_name is not None:
        dialog.set_current_name(tw.save_file_name+'.ta')
    return do_dialog(tw,dialog)

def save_data(tw,fname):
    f = file(fname, "w")
    data = assemble_data_to_save(tw)
    if _old_Sugar_system is True:
        # use pickle here to maintain compatibility with TA 10
        pickle.dump(data,f)
    else:
        io = StringIO()
        jdump(data,io)
        text = io.getvalue()
        print "save data: %s" % (text)
        # text = jencode(data)
        f.write(text)
    f.close()

# Used to send data across a shared session
def save_string(tw,save_turtle=True):
    data = assemble_data_to_save(tw,save_turtle)
    if _old_Sugar_system is True:
        text = json.write(data)
    else:
        io = StringIO()
        jdump(data,io)
        text = io.getvalue()
    return text

def assemble_data_to_save(tw,save_turtle=True):
    data = []
    for i, b in enumerate(tw.block_list.list):
         b.id = i
    for b in tw.block_list.list:
        name = (b.name, b.spr.labels[0])
        if tw.defdict.has_key(name) or name in nolabel:
            if hasattr(b,"ds_id") and b.ds_id != None:
                name=(name, str(b.ds_id))
            else:
                name=(name, b.spr.labels[0])
        if hasattr(b,'connections'):
            connections = [get_id(tw.block_list, x) for x in b.connections]
        else:
            connections = None
        (sx, sy) = b.spr.get_xy()
        data.append((b.id, name, sx-tw.turtle.cx,
                     sy-tw.turtle.cy, connections))
    if save_turtle is True:
        data.append((-1,'turtle',
                    tw.turtle.xcor,tw.turtle.ycor,tw.turtle.heading,
                    tw.turtle.color,tw.turtle.shade,tw.turtle.pensize))
    return data

# serialize a stack to save to the clipboard
def serialize_stack(tw):
    data = assemble_stack_to_clone(tw)
    if data == []:
        return None
    if _old_Sugar_system is True:
        text = json.write(data)
    else:
        io = StringIO()
        jdump(data,io)
        text = io.getvalue()
    return text

# find the stack under the cursor and serialize it
# TODO: rebase on assemble data to save
# This code is broken
def assemble_stack_to_clone(tw):
    if tw.spr is None or tw.spr.type is not "block":
        (x,y) = tw.window.get_pointer()
        spr = tw.sprite_list.find_sprite((x,y))
        if spr is not None:
            print "found block of type " + spr.type
    else:
        print "already selected block of type " + tw.spr.type
        spr = tw.spr
    data = []
    blk = tw.block_list.spr_to_block(spr)
    if blk is not None:
        bs = findgroup(find_top_block(blk, tw.block_list), tw.block_list)
        for i in range(len(bs)): bs[i].id=i
        for b in bs:
            name = b.proto.name
            if tw.defdict.has_key(name) or name in nolabel:
                if hasattr(b, "ds_id") and b.ds_id is not None:
                    name=(name,str(b.ds_id))
                else:
                    name=(name,b.labels[0])
            if hasattr(b,'connections') and b.connections is not None:
                connections = [get_id(x) for x in b.connections]
            else:
                connections = None
            (sx, sy) = b.get_xy()
            data.append((b.id,name,sx-tw.turtle.cx+20,
                         sy-tw.turtle.cy+20,connections))
    return data

def save_pict(tw,fname):
    tc = tw.turtle.canvas
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, tc.width,
                            tc.height)
    pixbuf.get_from_drawable(tc.image, tc.image.get_colormap(), 0, 0, 0, 0,
                             tc.width, tc.height)
    pixbuf.save(fname, 'png')

def get_id(blocks, x):
    if x==None: return None
    return blocks.spr_to_block(x).id

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

# phasing out
def blocks(tw): return [spr for spr in tw.sprite_list.list \
                        if spr.type == 'block']

def findgroup(blk, block_list):
    group=[blk.spr]
    for spr2 in blk.connections[1:]:
        if spr2 is not None:
            group.extend(findgroup(block_list.spr_to_block(spr2), block_list))
    return group

def find_top_block(blk, block_list):
    while blk.connections[0]!=None:
        blk = block_list.spr_to_block(blk.connections[0])
    return blk

# start a new project with a start brick
def load_start(tw):
    clone_stack(tw,"%s%s%s" % ("[[0,[\"start\",\"", _("start"),
                               "\"],250,30,[null,null]]]"))

