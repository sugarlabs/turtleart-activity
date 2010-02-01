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
        _old_Sugar_system = True

from StringIO import StringIO
import os.path

def json_load(text):
    if _old_Sugar_system is True:
        listdata = json.read(text)
    else:
        io = StringIO(text)
        listdata = jload(io)
    # json converts tuples to lists, so we need to convert back,
    return _tuplify(listdata) 

def _tuplify(t):
    if type(t) is not list:
        return t
    return tuple(map(_tuplify, t))

def get_id(c):
    if c is None:
        return None
    return c.id

def json_dump(data):
    if _old_Sugar_system is True:
        return json.write(data)
    else:
        io = StringIO()
        jdump(data,io)
        return io.getvalue()

def get_load_name(suffix, load_save_folder):
    print "get_load_name: %s %s" % (suffix, load_save_folder)
    dialog = gtk.FileChooserDialog("Load...", None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    return do_dialog(dialog, suffix, load_save_folder)
    
#
# We try to maintain read-compatibility with all versions of Turtle Art.
# Try pickle first; then selfo different versions of json.
#
def data_from_file(ta_file):
    # Just open the .ta file, ignoring any .png file that might be present.
    f = open(ta_file, "r")
    try:
        data = pickle.load(f)
    except:
        # Rewind necessary because of failed pickle.load attempt
        f.seek(0)
        text = f.read()
        data = json_load(text)
    f.close()
    return data

def do_dialog(dialog, suffix, load_save_folder):
    print "do_dialog: %s %s" % (suffix, load_save_folder)
    result = None
    filter = gtk.FileFilter()
    filter.add_pattern('*'+suffix)
    filter.set_name("Turtle Art")
    dialog.add_filter(filter)
    dialog.set_current_folder(load_save_folder)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        result = dialog.get_filename()
        load_save_folder = dialog.get_current_folder()
    dialog.destroy()
    return result, load_save_folder

