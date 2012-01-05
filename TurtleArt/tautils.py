#Copyright (c) 2007-8, Playful Invention Company.
#Copyright (c) 2008-11, Walter Bender

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
import cairo
import pickle
import subprocess
import os
from gettext import gettext as _

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
from StringIO import StringIO

from taconstants import COLLAPSIBLE, HIT_HIDE, HIT_SHOW, XO1, XO15, XO175, \
    XO30, UNKNOWN

SANDWICHES = ['sandwichtop', 'sandwichtop_no_label', 'sandwichtop_no_arm',
              'sandwichtop_no_arm_no_label']

import logging
_logger = logging.getLogger('turtleart-activity')


def debug_output(message_string, running_sugar=False):
    ''' unified debugging output '''
    if running_sugar:
        _logger.debug(message_string)
    else:
        print(message_string)


def error_output(message_string, running_sugar=False):
    ''' unified debugging output '''
    if running_sugar:
        _logger.error(message_string)
    else:
        print(message_string)


class pythonerror(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def convert(x, fn, try_ord=True):
    '''
    The strategy for mixing numbers and strings is to first try
    converting the string to a float; then if the string is a single
    character, try converting it to an ord; finally, just treat it as a
    string. Numbers appended to strings are first treated as ints, then
    floats.
    '''
    try:
        return fn(x)
    except ValueError:
        if try_ord:
            xx, flag = chr_to_ord(x)
            if flag:
                return fn(xx)
        return x


def chr_to_ord(x):
    ''' Try to comvert a string to an ord '''
    if strtype(x) and len(x) == 1:
        try:
            return ord(x[0]), True
        except ValueError:
            return x, False
    return x, False


def strtype(x):
    ''' Is x a string type? '''
    if type(x) == str:
        return True
    if type(x) == unicode:
        return True
    return False


def magnitude(pos):
    ''' Calculate the magnitude of the distance between to blocks. '''
    x, y = pos
    return x * x + y * y


def json_load(text):
    ''' Load JSON data using what ever resources are available. '''
    if OLD_SUGAR_SYSTEM is True:
        listdata = json.read(text)
    else:
        # Strip out leading and trailing whitespace, nulls, and newlines
        clean_text = text.lstrip()
        clean_text = clean_text.replace('\12', '')
        clean_text = clean_text.replace('\00', '')
        clean_text = clean_text.rstrip()
        # Look for missing ']'s
        left_count = clean_text.count('[')
        right_count = clean_text.count(']')
        while left_count > right_count:
            clean_text += ']'
            right_count = clean_text.count(']')
        io = StringIO(clean_text)
        try:
            listdata = jload(io)
        except ValueError:
            # Assume that text is ascii list
            listdata = text.split()
            for i, value in enumerate(listdata):
                listdata[i] = convert(value, float)
    # json converts tuples to lists, so we need to convert back,
    return _tuplify(listdata)


def _tuplify(tup):
    ''' Convert to tuples '''
    if type(tup) is not list:
        return tup
    return tuple(map(_tuplify, tup))


def get_id(connection):
    ''' Get a connection block ID. '''
    if connection is not None and hasattr(connection, 'id'):
        return connection.id
    return None


def json_dump(data):
    ''' Save data using available JSON tools. '''
    if OLD_SUGAR_SYSTEM is True:
        return json.write(data)
    else:
        io = StringIO()
        jdump(data, io)
        return io.getvalue()


def get_load_name(suffix, load_save_folder):
    ''' Open a load file dialog. '''
    dialog = gtk.FileChooserDialog(
        _('Load...'), None,
        gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(dialog, suffix, load_save_folder)


def get_save_name(suffix, load_save_folder, save_file_name):
    ''' Open a save file dialog. '''
    dialog = gtk.FileChooserDialog(
        _('Save...'), None,
        gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    if save_file_name is not None:
        dialog.set_current_name(save_file_name + suffix)
    return do_dialog(dialog, suffix, load_save_folder)


def chooser(parent_window, filter, action):
    ''' Choose an object from the datastore and take some action '''
    from sugar.graphics.objectchooser import ObjectChooser

    chooser = None
    try:
        chooser = ObjectChooser(parent=parent_window, what_filter=filter)
    except TypeError:
        chooser = ObjectChooser(None, parent_window,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
    if chooser is not None:
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                dsobject = chooser.get_selected_object()
                action(dsobject)
                dsobject.destroy()
        finally:
            chooser.destroy()
            del chooser


def data_from_file(ta_file):
    ''' Open the .ta file, ignoring any .png file that might be present. '''
    file_handle = open(ta_file, 'r')
    #
    # We try to maintain read-compatibility with all versions of Turtle Art.
    # Try pickle first; then different versions of json.
    #
    try:
        data = pickle.load(file_handle)
    except:
        # Rewind necessary because of failed pickle.load attempt
        file_handle.seek(0)
        text = file_handle.read()
        data = data_from_string(text)
    file_handle.close()
    return data


def data_from_string(text):
    ''' JSON load data from a string. '''
    return json_load(text.replace(']],\n', ']], '))


def data_to_file(data, ta_file):
    ''' Write data to a file. '''
    file_handle = file(ta_file, 'w')
    file_handle.write(data_to_string(data))
    file_handle.close()


def data_to_string(data):
    ''' JSON dump a string. '''
    return json_dump(data).replace(']], ', ']],\n')


def do_dialog(dialog, suffix, load_save_folder):
    ''' Open a file dialog. '''
    result = None
    file_filter = gtk.FileFilter()
    file_filter.add_pattern('*' + suffix)
    file_filter.set_name('Turtle Art')
    dialog.add_filter(file_filter)
    dialog.set_current_folder(load_save_folder)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        result = dialog.get_filename()
        load_save_folder = dialog.get_current_folder()
    dialog.destroy()
    return result, load_save_folder


def save_picture(canvas, file_name):
    ''' Save the canvas to a file '''
    x_surface = canvas.canvas.get_target()
    img_surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                     canvas.width, canvas.height)
    cr = cairo.Context(img_surface)
    cr.set_source_surface(x_surface)
    cr.paint()
    img_surface.write_to_png(file_name)


def get_canvas_data(canvas):
    ''' Get pixel data from the turtle canvas '''
    x_surface = canvas.canvas.get_target()
    img_surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                     canvas.width, canvas.height)
    cr = cairo.Context(img_surface)
    cr.set_source_surface(x_surface)
    cr.paint()
    return img_surface.get_data()


def save_svg(string, file_name):
    ''' Write a string to a file. '''
    file_handle = file(file_name, 'w')
    file_handle.write(string)
    file_handle.close()


def get_pixbuf_from_journal(dsobject, w, h):
    ''' Load a pixbuf from a Journal object. '''
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(dsobject.file_path,
                                                      int(w), int(h))
    except:
        try:
            pixbufloader = \
                gtk.gdk.pixbuf_loader_new_with_mime_type('image/png')
            pixbufloader.set_size(min(300, int(w)), min(225, int(h)))
            pixbufloader.write(dsobject.metadata['preview'])
            pixbufloader.close()
            pixbuf = pixbufloader.get_pixbuf()
        except:
            pixbuf = None
    return pixbuf


def get_path(activity, subpath):
    ''' Find a Rainbow-approved place for temporary files. '''
    try:
        return(os.path.join(activity.get_activity_root(), subpath))
    except:
        # Early versions of Sugar didn't support get_activity_root()
        return(os.path.join(os.environ['HOME'], '.sugar/default',
                            'org.laptop.TurtleArtActivity', subpath))


def image_to_base64(image_path, tmp_path):
    ''' Convert an image to base64-encoded data '''
    base64 = os.path.join(tmp_path, 'base64tmp')
    cmd = 'base64 <' + image_path + ' >' + base64
    subprocess.check_call(cmd, shell=True)
    file_handle = open(base64, 'r')
    data = file_handle.read()
    file_handle.close()
    os.remove(base64)
    return data


def base64_to_image(data, path_name):
    ''' Convert base64-encoded data to an image '''
    base64 = os.path.join(path_name, 'base64tmp')
    file_handle = open(base64, 'w')
    file_handle.write(data)
    file_handle.close()
    file_name = os.path.join(path_name, 'imagetmp.png')
    cmd = 'base64 -d <' + base64 + '>' + file_name
    subprocess.check_call(cmd, shell=True)
    return file_name


def movie_media_type(name):
    ''' Is it movie media? '''
    return name.lower().endswith(('.ogv', '.vob', '.mp4', '.wmv', '.mov',
                                  '.mpeg', '.ogg', '.webm'))


def audio_media_type(name):
    ''' Is it audio media? '''
    return name.lower().endswith(('.oga', '.m4a'))


def image_media_type(name):
    ''' Is it image media? '''
    return name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tiff',
                                  '.tif', '.svg'))


def text_media_type(name):
    ''' Is it text media? '''
    return name.lower().endswith(('.txt', '.py', '.lg', '.rtf'))


def round_int(num):
    ''' Remove trailing decimal places if number is an int '''
    try:
        float(num)
    except TypeError:
        raise pythonerror('#syntaxerror')

    if int(float(num)) == num:
        return int(num)
    else:
        if float(num) < 0:
            nn = int((float(num) - 0.005) * 100) / 100.
        else:
            nn = int((float(num) + 0.005) * 100) / 100.
        if int(float(nn)) == nn:
            return int(nn)
        return nn


def calc_image_size(spr):
    ''' Calculate the maximum size for placing an image onto a sprite. '''
    return int(max(spr.label_safe_width(), 1)), \
           int(max(spr.label_safe_height(), 1))


# Collapsible stacks live between 'sandwichtop' and 'sandwichbottom' blocks


def reset_stack_arm(top):
    ''' When we undock, retract the 'arm' that extends from 'sandwichtop'. '''
    if top is not None and top.name in ['sandwichtop', 'sandwichtop_no_label']:
        if top.ey > 0:
            top.reset_y()
        top.svg.set_hide(False)
        top.refresh()


def grow_stack_arm(top):
    ''' When we dock, grow an 'arm' from 'sandwichtop'. '''
    if top is not None and top.name in ['sandwichtop', 'sandwichtop_no_label']:
        bot = find_sandwich_bottom(top)
        if bot is None:
            return
        if top.ey > 0:
            top.reset_y()
        ty = top.spr.get_xy()[1]
        th = top.spr.get_dimensions()[1]
        by = bot.spr.get_xy()[1]
        dy = by - (ty + th)
        if dy > 0:
            top.expand_in_y(dy / top.scale)
            top.svg.set_hide(True)
            top.refresh()


def find_sandwich_top(blk):
    ''' Find the sandwich top above this block. '''
    # Always follow the main branch of a flow: the first connection.
    cblk = blk.connections[0]
    while cblk is not None:
        if cblk.name in COLLAPSIBLE:
            return None
        if cblk.name in ['repeat', 'if', 'ifelse', 'forever', 'while']:
            if blk != cblk.connections[len(cblk.connections) - 1]:
                return None
        if cblk.name in SANDWICHES:
            return cblk
        blk = cblk
        cblk = cblk.connections[0]
    return None


def find_sandwich_bottom(blk):
    ''' Find the sandwich bottom below this block. '''
    # Always follow the main branch of a flow: the last connection.
    cblk = blk.connections[len(blk.connections) - 1]
    while cblk is not None:
        if cblk.name in SANDWICHES:
            return None
        if cblk.name in COLLAPSIBLE:
            return cblk
        cblk = cblk.connections[len(cblk.connections) - 1]
    return None


def find_sandwich_top_below(blk):
    ''' Find the sandwich top below this block. '''
    if blk.name in SANDWICHES:
        return blk
    # Always follow the main branch of a flow: the last connection.
    cblk = blk.connections[len(blk.connections) - 1]
    while cblk is not None:
        if cblk.name in SANDWICHES:
            return cblk
        cblk = cblk.connections[len(cblk.connections) - 1]
    return None


def restore_stack(top):
    ''' Restore the blocks between the sandwich top and sandwich bottom. '''
    group = find_group(top.connections[len(top.connections) - 1])
    hit_bottom = False
    bot = find_sandwich_bottom(top)
    for gblk in group:
        if not hit_bottom and gblk == bot:
            hit_bottom = True
            if len(gblk.values) == 0:
                gblk.values.append(0)
            else:
                gblk.values[0] = 0
            olddx = gblk.docks[1][2]
            olddy = gblk.docks[1][3]
            # Replace 'sandwichcollapsed' shape with 'sandwichbottom' shape
            gblk.name = 'sandwichbottom'
            gblk.spr.set_label(' ', 1)
            gblk.svg.set_show(False)
            gblk.svg.set_hide(True)
            gblk.refresh()
            # Redock to previous block in group
            you = gblk.connections[0]
            (yx, yy) = you.spr.get_xy()
            yd = you.docks[len(you.docks) - 1]
            (bx, by) = gblk.spr.get_xy()
            dx = yx + yd[2] - gblk.docks[0][2] - bx
            dy = yy + yd[3] - gblk.docks[0][3] - by
            gblk.spr.move_relative((dx, dy))
            # Since the shapes have changed, the dock positions have too.
            dx += gblk.docks[1][2] - olddx
            dy += gblk.docks[1][3] - olddy
        else:
            if not hit_bottom:
                gblk.spr.restore()
                gblk.status = None
            else:
                gblk.spr.move_relative((dx, dy))
    # Add 'sandwichtop' arm
    if top.name == 'sandwichtop_no_arm':
        top.name = 'sandwichtop'
    else:
        top.name = 'sandwichtop_no_label'
        top.spr.set_label(' ', 1)
        top.resize()
    top.refresh()
    grow_stack_arm(top)


def uncollapse_forks(top, looping=False):
    ''' From the top, find and restore any collapsible stacks on forks. '''
    if top == None:
        return
    if looping and top.name in ['sandwichtop_no_arm',
                                'sandwichtop_no_arm_no_label']:
        restore_stack(top)
        return
    if len(top.connections) == 0:
        return
    cblk = top.connections[len(top.connections) - 1]
    while cblk is not None:
        if cblk.name in COLLAPSIBLE:
            return
        if cblk.name in ['sandwichtop_no_arm', 'sandwichtop_no_arm_no_label']:
            restore_stack(cblk)
            return
        # Follow a fork
        if cblk.name in ['repeat', 'if', 'ifelse', 'forever', 'while',
                         'until']:
            top = find_sandwich_top_below(
                cblk.connections[len(cblk.connections) - 2])
            if top is not None:
                uncollapse_forks(top, True)
            if cblk.name == 'ifelse':
                top = find_sandwich_top_below(
                    cblk.connections[len(cblk.connections) - 3])
                if top is not None:
                    uncollapse_forks(top, True)
        cblk = cblk.connections[len(cblk.connections) - 1]
    return


def collapse_stack(top):
    ''' Hide all the blocks between the sandwich top and sandwich bottom. '''
    # First uncollapse any nested stacks
    if top == None or top.spr == None:
        return
    uncollapse_forks(top)
    hit_bottom = False
    bot = find_sandwich_bottom(top)
    group = find_group(top.connections[len(top.connections) - 1])
    for gblk in group:
        if not hit_bottom and gblk == bot:
            hit_bottom = True
            # Replace 'sandwichbottom' with invisible 'sandwichcollapsed'
            if len(gblk.values) == 0:
                gblk.values.append(1)
            else:
                gblk.values[0] = 1
            olddx = gblk.docks[1][2]
            olddy = gblk.docks[1][3]
            gblk.name = 'sandwichcollapsed'
            gblk.resize()
            you = find_sandwich_top(gblk)
            (yx, yy) = you.spr.get_xy()
            yd = you.docks[len(you.docks) - 1]
            (bx, by) = gblk.spr.get_xy()
            dx = yx + yd[2] - gblk.docks[0][2] - bx
            dy = yy + yd[3] - gblk.docks[0][3] - by
            gblk.spr.move_relative((dx, dy))
            # Since the shapes have changed, the dock positions have too.
            dx += gblk.docks[1][2] - olddx
            dy += gblk.docks[1][3] - olddy
        else:
            if not hit_bottom:
                gblk.spr.hide()
                gblk.status = 'collapsed'
            else:
                gblk.spr.move_relative((dx, dy))
    # Remove 'sandwichtop' arm
    if top.name == 'sandwichtop' or top.name == 'sandwichtop_no_arm':
        top.name = 'sandwichtop_no_arm'
    else:
        top.name = 'sandwichtop_no_arm_no_label'
    top.spr.set_label(' ')
    top.spr.set_label(' ', 1)
    top.resize()
    top.spr.set_label(_('click to open'), 1)
    top.resize()
    top.svg.set_hide(False)
    top.refresh()


def collapsed(blk):
    ''' Is this stack collapsed? '''
    if blk is not None and blk.name in COLLAPSIBLE and\
       len(blk.values) == 1 and blk.values[0] != 0:
        return True
    return False


def collapsible(blk):
    ''' Can this stack be collapsed? '''
    if blk is None or blk.name not in COLLAPSIBLE:
        return False
    if find_sandwich_top(blk) is None:
        return False
    return True


def hide_button_hit(spr, x, y):
    ''' Did the sprite's hide (contract) button get hit? '''
    red, green, blue, alpha = spr.get_pixel((x, y))
    if red == HIT_HIDE:
        return True
    else:
        return False


def show_button_hit(spr, x, y):
    ''' Did the sprite's show (expand) button get hit? '''
    red, green, blue, alpha = spr.get_pixel((x, y))
    if green == HIT_SHOW:
        return True
    else:
        return False


def numeric_arg(value):
    ''' Dock test: looking for a numeric value '''
    if type(convert(value, float)) is float:
        return True
    return False


def zero_arg(value):
    ''' Dock test: looking for a zero argument '''
    if numeric_arg(value):
        if convert(value, float) == 0:
            return True
    return False


def neg_arg(value):
    ''' Dock test: looking for a negative argument '''
    if numeric_arg(value):
        if convert(value, float) < 0:
            return True
    return False


def journal_check(blk1, blk2, dock1, dock2):
    ''' Dock blocks only if arg is Journal block '''
    if blk1 == None or blk2 == None:
        return True
    if (blk1.name == 'skin' and dock1 == 1) and blk2.name != 'journal':
        return False
    if (blk2.name == 'skin' and dock2 == 1) and blk1.name != 'journal':
        return False
    return True


def arithmetic_check(blk1, blk2, dock1, dock2):
    ''' Dock strings only if they convert to numbers. Avoid /0 and root(-1)'''
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
        # Non-numeric stings are OK only if both args are strings;
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
    ''' Where is the mouse event? '''
    return map(int, event.get_coords())


# Utilities related to finding blocks in stacks.


def find_block_to_run(blk):
    ''' Find a stack to run (any stack without a 'def action'on the top). '''
    top = find_top_block(blk)
    if blk == top and blk.name[0:3] is not 'def':
        return True
    else:
        return False


def find_top_block(blk):
    ''' Find the top block in a stack. '''
    if blk is None:
        return None
    if len(blk.connections) == 0:
        return blk
    while blk.connections[0] is not None:
        blk = blk.connections[0]
    return blk


def find_start_stack(blk):
    ''' Find a stack with a 'start' block on top. '''
    if blk is None:
        return False
    if find_top_block(blk).name == 'start':
        return True
    else:
        return False


def find_group(blk):
    ''' Find the connected group of block in a stack. '''
    if blk is None:
        return []
    group = [blk]
    if blk.connections is not None:
        for cblk in blk.connections[1:]:
            if cblk is not None:
                group.extend(find_group(cblk))
    return group


def find_blk_below(blk, name):
    ''' Find a specific block below this block. '''
    if blk == None or len(blk.connections) == 0:
        return
    group = find_group(blk)
    for gblk in _group:
        if gblk.name == name:
            return gblk
    return None


def get_hardware():
    ''' Determine whether we are using XO 1.0, 1.5, or 'unknown' hardware '''
    product = _get_dmi('product_name')
    if product is None:
        if os.path.exists('/sys/devices/platform/lis3lv02d/position'):
            return XO175  # FIXME: temporary check for XO 1.75 and XO 3.0
        elif os.path.exists('/etc/olpc-release') or \
           os.path.exists('/sys/power/olpc-pm'):
            return XO1
        else:
            return UNKNOWN
    if product != 'XO':
        return UNKNOWN
    version = _get_dmi('product_version')
    if version == '1':
        return XO1
    elif version == '1.5':
        return XO15
    else:
        return XO175


def _get_dmi(node):
    ''' The desktop management interface should be a reliable source
    for product and version information. '''
    path = os.path.join('/sys/class/dmi/id', node)
    try:
        return open(path).readline().strip()
    except:
        return None
