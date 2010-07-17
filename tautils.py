#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-10, Walter Bender

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

import gtk
import pickle
import subprocess
try:
    OLD_SUGAR_SYSTEM = False
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
        OLD_SUGAR_SYSTEM = True
from taconstants import STRING_OR_NUMBER_ARGS, HIDE_LAYER, CONTENT_ARGS, \
                        COLLAPSIBLE, BLOCK_LAYER, CONTENT_BLOCKS
from StringIO import StringIO
import os.path
from gettext import gettext as _
import logging
_logger = logging.getLogger('turtleart-activity')

class pythonerror(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

'''
The strategy for mixing numbers and strings is to first try
converting the string to a float; then if the string is a single
character, try converting it to an ord; finally, just treat it as a
string. Numbers appended to strings are first trreated as ints, then
floats.
'''
def convert(x, fn, try_ord=True):
    try:
        return fn(x)
    except ValueError:
        if try_ord:
            xx, flag = chr_to_ord(x)
            if flag:
                return fn(xx)
        return x

def chr_to_ord(x):
    """ Try to comvert a string to an ord """
    if strtype(x) and len(x) == 1:
        try:
            return ord(x[0]), True
        except ValueError:
            return x, False
    return x, False

def strtype(x):
    """ Is x a string type? """
    if type(x) == str:
        return True
    if type(x) == unicode:
        return True
    return False

def magnitude(pos):
    """ Calculate the magnitude of the distance between to blocks. """
    x, y = pos
    return x*x+y*y

def json_load(text):
    """ Load JSON data using what ever resources are available. """
    if OLD_SUGAR_SYSTEM is True:
        _listdata = json.read(text)
    else:
        # strip out leading and trailing whitespace, nulls, and newlines
        text = text.lstrip()
        text = text.replace('\12','')
        text = text.replace('\00','')
        _io = StringIO(text.rstrip())
        _listdata = jload(_io)
    # json converts tuples to lists, so we need to convert back,
    return _tuplify(_listdata) 

def _tuplify(tup):
    """ Convert to tuples """
    if type(tup) is not list:
        return tup
    return tuple(map(_tuplify, tup))

def get_id(connection):
    """ Get a connection block ID. """
    if connection is None:
        return None
    return connection.id

def json_dump(data):
    """ Save data using available JSON tools. """
    if OLD_SUGAR_SYSTEM is True:
        return json.write(data)
    else:
        _io = StringIO()
        jdump(data, _io)
        return _io.getvalue()

def get_load_name(suffix, load_save_folder):
    """ Open a load file dialog. """
    _dialog = gtk.FileChooserDialog("Load...", None,
                                    gtk.FILE_CHOOSER_ACTION_OPEN,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    _dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(_dialog, suffix, load_save_folder)
    
def get_save_name(suffix, load_save_folder, save_file_name):
    """ Open a save file dialog. """
    _dialog = gtk.FileChooserDialog("Save...", None,
                                    gtk.FILE_CHOOSER_ACTION_SAVE,
                                    (gtk.STOCK_CANCEL,
                                     gtk.RESPONSE_CANCEL,
                                     gtk.STOCK_SAVE,
                                     gtk.RESPONSE_OK))
    _dialog.set_default_response(gtk.RESPONSE_OK)
    if save_file_name is not None:
        _dialog.set_current_name(save_file_name+suffix)
    return do_dialog(_dialog, suffix, load_save_folder)

#
# We try to maintain read-compatibility with all versions of Turtle Art.
# Try pickle first; then different versions of json.
#
def data_from_file(ta_file):
    """ Open the .ta file, ignoring any .png file that might be present. """
    file_handle = open(ta_file, "r")
    try:
        _data = pickle.load(file_handle)
    except:
        # Rewind necessary because of failed pickle.load attempt
        file_handle.seek(0)
        _text = file_handle.read()
        _data = data_from_string(_text)
    file_handle.close()
    return _data

def data_from_string(text):
    """ JSON load data from a string. """
    return json_load(text)

def data_to_file(data, ta_file):
    """ Write data to a file. """
    file_handle = file(ta_file, "w")
    file_handle.write(data_to_string(data))
    file_handle.close()

def data_to_string(data):
    """ JSON dump a string. """
    return json_dump(data)

def do_dialog(dialog, suffix, load_save_folder):
    """ Open a file dialog. """
    _result = None
    file_filter = gtk.FileFilter()
    file_filter.add_pattern('*'+suffix)
    file_filter.set_name("Turtle Art")
    dialog.add_filter(file_filter)
    dialog.set_current_folder(load_save_folder)
    _response = dialog.run()
    if _response == gtk.RESPONSE_OK:
        _result = dialog.get_filename()
        load_save_folder = dialog.get_current_folder()
    dialog.destroy()
    return _result, load_save_folder

def save_picture(canvas, file_name=''):
    """ Save the canvas to a file. """
    _pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, canvas.width,
                             canvas.height)
    _pixbuf.get_from_drawable(canvas.canvas.images[0],
                              canvas.canvas.images[0].get_colormap(),
                              0, 0, 0, 0, canvas.width, canvas.height)
    if file_name != '':
        _pixbuf.save(file_name, 'png')
    return _pixbuf

def save_svg(string, file_name):
    """ Write a string to a file. """
    file_handle = file(file_name, "w")
    file_handle.write(string)
    file_handle.close()

def get_pixbuf_from_journal(dsobject, w, h):
    """ Load a pixbuf from a Journal object. """
    try:
        _pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(dsobject.file_path,
                                                       int(w), int(h))
    except:
        try:
            _pixbufloader = \
                gtk.gdk.pixbuf_loader_new_with_mime_type('image/png')
            _pixbufloader.set_size(min(300, int(w)), min(225, int(h)))
            _pixbufloader.write(dsobject.metadata['preview'])
            _pixbufloader.close()
            _pixbuf = _pixbufloader.get_pixbuf()
        except:
            _pixbuf = None
    return _pixbuf

def get_path(activity, subpath ):
    """ Find a Rainbow-approved place for temporary files. """
    try:
        return(os.path.join(activity.get_activity_root(), subpath))
    except:
        # Early versions of Sugar didn't support get_activity_root()
        return(os.path.join(os.environ['HOME'], ".sugar/default",
                            "org.laptop.TurtleArtActivity", subpath))

def image_to_base64(pixbuf, activity):
    """ Convert an image to base64 """
    _file_name = os.path.join(get_path(activity, 'instance'), 'imagetmp.png')
    if pixbuf != None:
        pixbuf.save(_file_name, "png")
    _base64 = os.path.join(get_path(activity, 'instance'), 'base64tmp')
    _cmd = "base64 <" + _file_name + " >" + _base64
    subprocess.check_call(_cmd, shell=True)
    _file_handle = open(_base64, 'r')
    _data = _file_handle.read()
    _file_handle.close()
    return _data

def movie_media_type(name):
    """ Is it movie media? """
    return name.endswith(('.ogv', '.vob', '.mp4', '.wmv', '.mov', '.mpeg'))

def audio_media_type(name): 
    """ Is it audio media? """
    return name.endswith(('.ogg', '.oga', '.m4a'))

def image_media_type(name):
    """ Is it image media? """
    return name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.tif',
                          '.svg'))
def text_media_type(name):
    """ Is it text media? """
    return name.endswith(('.txt', '.py', '.lg', '.doc', '.rtf'))

def round_int(num):
    """ Remove trailing decimal places if number is an int """
    try:
        float(num)
    except TypeError:
        _logger.debug("error trying to convert %s to number" % (str(num)))
        raise pythonerror("#syntaxerror")

    if int(float(num)) == num:
        return int(num)
    else:
        if float(num)<0:
            _nn = int((float(num)-0.005)*100)/100.
        else:
            _nn = int((float(num)+0.005)*100)/100.
        if int(float(_nn)) == _nn:
            return int(_nn)
        return _nn

def calc_image_size(spr):
    """ Calculate the maximum size for placing an image onto a sprite. """
    return spr.label_safe_width(), spr.label_safe_height()



# Collapsible stacks live between 'sandwichtop' and 'sandwichbottom' blocks

def reset_stack_arm(top):
    """ When we undock, retract the 'arm' that extends from 'sandwichtop'. """
    if top is not None and top.name == 'sandwichtop':
        if top.ey > 0:
            top.reset_y()

def grow_stack_arm(top):
    """ When we dock, grow an 'arm' from 'sandwichtop'. """
    if top is not None and top.name == 'sandwichtop':
        _bot = find_sandwich_bottom(top)
        if _bot is None:
            return
        if top.ey > 0:
            top.reset_y()
        _ty = top.spr.get_xy()[1]
        _th = top.spr.get_dimensions()[1]
        _by = _bot.spr.get_xy()[1]
        _dy = _by-(_ty + _th)
        if _dy > 0:
            top.expand_in_y(_dy/top.scale)
            top.refresh()

def find_sandwich_top(blk):
    """ Find the sandwich top above this block. """
    # Always follow the main branch of a flow: the first connection.
    _blk = blk.connections[0]
    while _blk is not None:
        if _blk.name in COLLAPSIBLE:
            return None
        if _blk.name in ['repeat', 'if', 'ifelse', 'forever', 'while']:
            if blk != _blk.connections[len(_blk.connections) - 1]:
                return None
        if _blk.name == 'sandwichtop' or _blk.name == 'sandwichtop2':
            return _blk
        blk = _blk
        _blk = _blk.connections[0]
    return None

def find_sandwich_bottom(blk):
    """ Find the sandwich bottom below this block. """
    # Always follow the main branch of a flow: the last connection.
    _blk = blk.connections[len(blk.connections) - 1]
    while _blk is not None:
        if _blk.name == 'sandwichtop' or _blk.name == 'sandwichtop2':
            return None
        if _blk.name in COLLAPSIBLE:
            return _blk
        _blk = _blk.connections[len(_blk.connections) - 1]
    return None

def find_sandwich_top_below(blk):
    """ Find the sandwich top below this block. """
    if blk.name == 'sandwichtop' or blk.name == 'sandwichtop2':
        return blk
    # Always follow the main branch of a flow: the last connection.
    _blk = blk.connections[len(blk.connections) - 1]
    while _blk is not None:
        if _blk.name == 'sandwichtop' or _blk.name == 'sandwichtop2':
            return _blk
        _blk = _blk.connections[len(_blk.connections) - 1]
    return None

def restore_stack(top):
    """ Restore the blocks between the sandwich top and sandwich bottom. """
    _group = find_group(top.connections[len(top.connections) - 1])
    _hit_bottom = False
    _bot = find_sandwich_bottom(top)
    for _blk in _group:
        if not _hit_bottom and _blk == _bot:
            _hit_bottom = True
            if len(_blk.values) == 0:
                _blk.values.append(0)
            else:
                _blk.values[0] = 0
            _olddx = _blk.docks[1][2]
            _olddy = _blk.docks[1][3]
            # Replace 'sandwichcollapsed' shape with 'sandwichbottom' shape
            _blk.name = 'sandwichbottom'
            _blk.spr.set_label(' ')
            _blk.svg.set_show(False)
            _blk.svg.set_hide(True)
            _blk.refresh()
             # Redock to previous block in group
            _you = _blk.connections[0]
            (_yx, _yy) = _you.spr.get_xy()
            _yd = _you.docks[len(_you.docks) - 1]
            (_bx, _by) = _blk.spr.get_xy()
            _dx = _yx + _yd[2] - _blk.docks[0][2] - _bx
            _dy = _yy + _yd[3] - _blk.docks[0][3] - _by
            _blk.spr.move_relative((_dx, _dy))
             # Since the shapes have changed, the dock positions have too.
            _newdx = _blk.docks[1][2]
            _newdy = _blk.docks[1][3]
            _dx += _newdx - _olddx
            _dy += _newdy - _olddy
        else:
            if not _hit_bottom:
                _blk.spr.set_layer(BLOCK_LAYER)
                _blk.status = None
            else:
                _blk.spr.move_relative((_dx, _dy))
     # Add 'sandwichtop' arm
    top.name = 'sandwichtop'
    top.refresh()
    grow_stack_arm(top)

def uncollapse_forks(top, looping=False):
    """ From the top, find and restore any collapsible stacks on forks. """
    if top == None:
        return
    if looping and top.name == 'sandwichtop' or top.name == 'sandwichtop2':
        restore_stack(top)
        return 
    if len(top.connections) == 0:
        return
    _blk = top.connections[len(top.connections) - 1]
    while _blk is not None:
        if _blk.name in COLLAPSIBLE:
            return
        if _blk.name == 'sandwichtop' or _blk.name == 'sandwichtop2':
            restore_stack(_blk)            
            return
        # Follow a fork
        if _blk.name in ['repeat', 'if', 'ifelse', 'forever', 'while', 'until']:
            top = find_sandwich_top_below(
                                    _blk.connections[len(_blk.connections) - 2])
            if top is not None:
                uncollapse_forks(top, True)
            if _blk.name == 'ifelse':
                top = find_sandwich_top_below(
                                    _blk.connections[len(_blk.connections) - 3])
                if top is not None:
                    uncollapse_forks(top, True)
        _blk = _blk.connections[len(_blk.connections) - 1]
    return

def collapse_stack(top):
    """ Hide all the blocks between the sandwich top and sandwich bottom. """
    # First uncollapse any nested stacks
    if top == None or top.spr == None:
        return
    uncollapse_forks(top)
    _hit_bottom = False
    _bot = find_sandwich_bottom(top)
    _group = find_group(top.connections[len(top.connections) - 1])
    for _blk in _group:
        if not _hit_bottom and _blk == _bot:
            _hit_bottom = True
             # Replace 'sandwichbottom' shape with 'sandwichcollapsed' shape
            if len(_blk.values) == 0:
                _blk.values.append(1)
            else:
                _blk.values[0] = 1
            _olddx = _blk.docks[1][2]
            _olddy = _blk.docks[1][3]
            _blk.name = 'sandwichcollapsed'
            _blk.svg.set_show(True)
            _blk.svg.set_hide(False)
            _blk._dx = 0
            _blk._ey = 0
            _blk.spr.set_label(' ')
            _blk.resize()
            _blk.spr.set_label(_('click to open'))
            _blk.resize()
             # Redock to sandwich top in group
            _you = find_sandwich_top(_blk)
            (_yx, _yy) = _you.spr.get_xy()
            _yd = _you.docks[len(_you.docks) - 1]
            (_bx, _by) = _blk.spr.get_xy()
            _dx = _yx + _yd[2] - _blk.docks[0][2] - _bx
            _dy = _yy + _yd[3] - _blk.docks[0][3] - _by
            _blk.spr.move_relative((_dx, _dy))
             # Since the shapes have changed, the dock positions have too.
            _newdx = _blk.docks[1][2]
            _newdy = _blk.docks[1][3]
            _dx += _newdx - _olddx
            _dy += _newdy - _olddy
        else:
            if not _hit_bottom:
                _blk.spr.set_layer(HIDE_LAYER)
                _blk.status = 'collapsed'
            else:
                _blk.spr.move_relative((_dx, _dy))
    # Remove 'sandwichtop' arm
    top.name = 'sandwichtop2'
    top.refresh()

def collapsed(blk):
    """ Is this stack collapsed? """
    if blk is not None and blk.name in COLLAPSIBLE and\
       len(blk.values) == 1 and blk.values[0] != 0:
        return True
    return False

def collapsible(blk):
    """ Can this stack be collapsed? """
    if blk is None or blk.name not in COLLAPSIBLE:
        return False
    if find_sandwich_top(blk) is None:
        return False
    return True

def hide_button_hit(spr, x, y):
    """ Did the sprite's hide (contract) button get hit? """
    _red, _green, _blue, _alpha = spr.get_pixel((x, y))
    if (_red == 255 and _green == 0) or _green == 255:
        return True
    else:
        return False

def show_button_hit(spr, x, y):
    """ Did the sprite's show (expand) button get hit? """
    _red, _green, _blue, _alpha = spr.get_pixel((x, y))
    if _green == 254:
        return True
    else:
        return False

def numeric_arg(value):
    """ Dock test: looking for a numeric value """
    if type(convert(value, float)) is float:
        return True
    return False

def zero_arg(value):
    """ Dock test: looking for a zero argument """
    if numeric_arg(value):
        if convert(value, float) == 0:
            return True
    return False

def neg_arg(value):
    """ Dock test: looking for a negative argument """
    if numeric_arg(value):
        if convert(value, float) < 0:
            return True
    return False

def dock_dx_dy(block1, dock1n, block2, dock2n):
    """ Find the distance between the dock points of two blocks. """
    _dock1 = block1.docks[dock1n]
    _dock2 = block2.docks[dock2n]
    _d1type, _d1dir, _d1x, _d1y = _dock1[0:4]
    _d2type, _d2dir, _d2x, _d2y = _dock2[0:4]
    if block1 == block2:
        return (100, 100)
    if _d1dir == _d2dir:
        return (100, 100)
    if (_d2type is not 'number') or (dock2n is not 0):
        if block1.connections is not None and \
           dock1n < len(block1.connections) and \
           block1.connections[dock1n] is not None:
            return (100, 100)
        if block2.connections is not None and \
           dock2n < len(block2.connections) and \
           block2.connections[dock2n] is not None:
            return (100, 100)
    if _d1type != _d2type:
        if block1.name in STRING_OR_NUMBER_ARGS:
            if _d2type == 'number' or _d2type == 'string':
                pass
        elif block1.name in CONTENT_ARGS:
            if _d2type in CONTENT_BLOCKS:
                pass
        else:
            return (100, 100)
    (_b1x, _b1y) = block1.spr.get_xy()
    (_b2x, _b2y) = block2.spr.get_xy()
    return ((_b1x + _d1x) - (_b2x + _d2x), (_b1y + _d1y) - (_b2y + _d2y))

def arithmetic_check(blk1, blk2, dock1, dock2):
    """ Dock strings only if they convert to numbers. Avoid /0 and root(-1)"""
    if blk1 == None or blk2 == None:
        return True
    if blk1.name in ['sqrt', 'number', 'string'] and\
       blk2.name in ['sqrt', 'number', 'string']:
        if blk1.name == 'number' or blk1.name == 'string':
            if not numeric_arg(blk1.values[0]) or neg_arg(blk1.values[0]):
                return False
        elif blk2.name == 'number' or blk2.name == 'string':
            if not numeric_arg(blk2.values[0]) or neg_arg(blk2.values[0]):
                return False
    elif blk1.name in ['division2', 'number', 'string'] and\
         blk2.name in ['division2', 'number', 'string']:
        if blk1.name == 'number' or blk1.name == 'string':
            if not numeric_arg(blk1.values[0]):
                return False
            if dock2 == 2 and zero_arg(blk1.values[0]):
                return False
        elif blk2.name == 'number' or blk2.name == 'string':
            if not numeric_arg(blk2.values[0]):
                return False
            if dock1 == 2 and zero_arg(blk2.values[0]):
                return False
    elif blk1.name in ['product2', 'minus2', 'random', 'remainder2',
                     'string'] and\
         blk2.name in ['product2', 'minus2', 'random', 'remainder2',
                     'string']:
        if blk1.name == 'string':
            if not numeric_arg(blk1.values[0]):
                return False
        elif blk1.name == 'string':
            if not numeric_arg(blk2.values[0]):
                return False
    elif blk1.name in ['greater2', 'less2'] and blk2.name == 'string':
        # Non-numeric stings are OK if only both args are strings;
        # Lots of test conditions...
        if dock1 == 1 and blk1.connections[2] is not None:
            if blk1.connections[2].name == 'number':
                if not numeric_arg(blk2.values[0]):
                    return False
        elif dock1 == 2 and blk1.connections[1] is not None:
            if blk1.connections[1].name == 'number':
                if not numeric_arg(blk2.values[0]):
                    return False
    elif blk2.name in ['greater2', 'less2'] and blk1.name == 'string':
        if dock2 == 1 and blk2.connections[2] is not None:
            if blk2.connections[2].name == 'number':
                if not numeric_arg(blk1.values[0]):
                    return False
        elif dock2 == 2 and blk2.connections[1] is not None:
            if blk2.connections[1].name == 'number':
                if not numeric_arg(blk1.values[0]):
                    return False
    elif blk1.name in ['greater2', 'less2'] and blk2.name == 'number':
        if dock1 == 1 and blk1.connections[2] is not None:
            if blk1.connections[2].name == 'string':
                if not numeric_arg(blk1.connections[2].values[0]):
                    return False
        elif dock1 == 2 and blk1.connections[1] is not None:
            if blk1.connections[1].name == 'string':
                if not numeric_arg(blk1.connections[1].values[0]):
                    return False
    elif blk2.name in ['greater2', 'less2'] and blk1.name == 'number':
        if dock2 == 1 and blk2.connections[2] is not None:
            if blk2.connections[2].name == 'string':
                if not numeric_arg(blk2.connections[2].values[0]):
                    return False
        elif dock2 == 2 and blk2.connections[1] is not None:
            if blk2.connections[1].name == 'string':
                if not numeric_arg(blk2.connections[1].values[0]):
                    return False
    return True

def xy(event):
    """ Where is the mouse event? """
    return map(int, event.get_coords())

"""
Utilities related to finding blocks in stacks.
"""

def find_block_to_run(blk):
    """ Find a stack to run (any stack without a 'def action'on the top). """
    _top = find_top_block(blk)
    if blk == _top and blk.name[0:3] is not 'def':
        return True
    else:
        return False

def find_top_block(blk):
    """ Find the top block in a stack. """
    if blk is None:
        return None
    if len(blk.connections) == 0:
        return blk
    while blk.connections[0] is not None:
        blk = blk.connections[0]
    return blk

def find_start_stack(blk):
    """ Find a stack with a 'start' block on top. """
    if blk is None:
        return False
    if find_top_block(blk).name == 'start':
        return True
    else:
        return False

def find_group(blk):
    """ Find the connected group of block in a stack. """
    if blk is None:
        return []
    _group = [blk]
    if blk.connections is not None:
        for _blk2 in blk.connections[1:]:
            if _blk2 is not None:
                _group.extend(find_group(_blk2))
    return _group

def find_blk_below(blk, name):
    """ Find a specific block below this block. """
    if blk == None or len(blk.connections) == 0:
        return
    _group = find_group(blk)
    for _gblk in _group:
        if _gblk.name == name:
            return _gblk
    return None

def olpc_xo_1():
    """ Is the an OLPC XO-1 or XO-1.5? """
    return os.path.exists('/etc/olpc-release') or \
           os.path.exists('/sys/power/olpc-pm')

def walk_stack(tw, blk):
    """ Convert blocks to logo psuedocode. """
    top = find_top_block(blk)
    if blk == top:
        code = tw.lc.run_blocks(top, tw.block_list.list, False)
        return code
    else:
        return []
