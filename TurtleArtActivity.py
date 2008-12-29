#Copyright (c) 2007-8, Playful Invention Company.

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

import tawindow
import talogo

import pygtk
pygtk.require('2.0')
import gtk

from socket import *
import sys
import gobject

serverHost = '192.168.1.102'
serverPort = 5647

def debug_init():
    s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
    s.connect((serverHost, serverPort)) # connect to server on the port
    sys.stdout = s.makefile()
    sys.stderr = sys.stdout
    gobject.timeout_add(100, debug_tick)

def debug_tick():
    sys.stdout.flush()
    return True

#debug_init()

import sugar
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.datastore import datastore
from sugar import profile
from gettext import gettext as _
import locale
import os.path
import os

class TurtleArtActivity(activity.Activity):
    def __init__(self, handle):
        super(TurtleArtActivity,self).__init__(handle)

        self.gamename = 'turtleart'
#        self.set_title("TurtleArt...")

        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        self.projectToolbar = ProjectToolbar(self)
        toolbox.add_toolbar( _('Project'), self.projectToolbar )
        toolbox.show()

#        toolbox._activity_toolbar.keep.connect('clicked', self._keep_clicked_cb) # patch

        canvas = gtk.EventBox()

        sugar.graphics.window.Window.set_canvas(self, canvas)
        toolbox._activity_toolbar.title.grab_focus()
        toolbox._activity_toolbar.title.select_region(0,0)
        tboxh = toolbox._activity_toolbar.size_request()[1]

        version = os.environ['SUGAR_BUNDLE_VERSION']

        lang = locale.getdefaultlocale()[0]
        if not lang: lang = 'en'
        lang = lang[0:2]
        if not os.path.isdir(os.path.join(activity.get_bundle_path(),'images',lang)):
            lang = 'en'

        # test to see if lang or version has changed since last time
        # if so, remove any old png files as they will need to be regenerated
        filename = "version.dat"
        versiondata = []

        try:
            FILE = open(os.path.join(activity.get_activity_root(),"data",filename),"r")
            if FILE.readline() == lang + version:
                print "the version data hasn't changed"
            else:
                print "out with the old version data",
                os.system("rm " + os.path.join(activity.get_activity_root(),"data",'*.png'))
        except:
            print "writing new version data"
        versiondata.append(lang + version)
        FILE = open(os.path.join(activity.get_activity_root(),"data",filename),"w")
        FILE.writelines(versiondata)
        FILE.close()

        self.tw = tawindow.twNew(canvas,activity.get_bundle_path(),lang,tboxh,self)
        self.tw.activity = self
        self.tw.window.grab_focus()
        self.tw.save_folder = os.path.join(os.environ['SUGAR_ACTIVITY_ROOT'],'data')

#        toolbox._activity_toolbar._update_title_sid = True
#        toolbox._activity_toolbar.title.connect('focus-out-event', self.update_title_cb, toolbox) # patch

        if self._jobject and self._jobject.file_path:
            self.read_file(self._jobject.file_path)

    def update_title_cb(self, widget, event, toolbox):
        toolbox._activity_toolbar._update_title_cb()
        toolbox._activity_toolbar._update_title_sid = True

    def _keep_clicked_cb(self, button):
        self.jobject_new_patch()

    def write_file(self, file_path):
        print "Writing file %s" % file_path
        self.metadata['mime_type'] = 'application/x-tar'
        import tarfile,os,tempfile
        tar_fd = tarfile.open(file_path, 'w')
        pngfd, pngfile = tempfile.mkstemp(".png")
        tafd, tafile = tempfile.mkstemp(".ta")
        del pngfd, tafd

        try:
            tawindow.save_data(self.tw,tafile)
            tawindow.save_pict(self.tw,pngfile)
            tar_fd.add(tafile, "ta_code.ta")
            tar_fd.add(pngfile, "ta_image.png")

        finally:
            tar_fd.close()
            os.remove(pngfile)
            os.remove(tafile)

    def read_file(self, file_path):
        # Better be a tar file.
        import tarfile,os,tempfile,shutil

        print "Reading file %s" %  file_path
        tar_fd = tarfile.open(file_path, 'r')
        tmpdir = tempfile.mkdtemp()

        try:
            # We'll get 'ta_code.ta' and 'ta_image.png'
            tar_fd.extractall(tmpdir)
            tawindow.load_files(self.tw, os.path.join(tmpdir, 'ta_code.ta'), os.path.join(tmpdir, 'ta_image.png'))

        finally:
            shutil.rmtree(tmpdir)
            tar_fd.close()

    def jobject_new_patch(self):
        oldj = self._jobject
        self._jobject = datastore.create()
        self._jobject.metadata['title'] = oldj.metadata['title']
        self._jobject.metadata['title_set_by_user'] = oldj.metadata['title_set_by_user']
        self._jobject.metadata['activity'] = self.get_service_name()
        self._jobject.metadata['activity_id'] = self.get_id()
        self._jobject.metadata['keep'] = '0'
        #self._jobject.metadata['buddies'] = ''
        self._jobject.metadata['preview'] = ''
        self._jobject.metadata['icon-color'] = profile.get_color().to_string()
        self._jobject.file_path = ''
        datastore.write(self._jobject,
                reply_handler=self._internal_jobject_create_cb,
                error_handler=self._internal_jobject_error_cb)

    def clear_journal(self):
        jobjects, total_count = datastore.find({'activity': 'org.laptop.TurtleArtActivity'})
        print 'found', total_count, 'entries'
        for jobject in jobjects[:-1]:
            print jobject.object_id
            datastore.delete(jobject.object_id)

class ProjectToolbar(gtk.Toolbar):

    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        self.sampb = ToolButton( "stock-open" )
        self.sampb.set_tooltip(_('Samples'))
        self.sampb.props.sensitive = True
        self.sampb.connect('clicked', self.do_samples)
        self.insert(self.sampb, -1)
        self.sampb.show()

        # UCB Logo save source button
        self.savelogo = ToolButton( "UCB-save" )
        self.savelogo.set_tooltip(_('UCB Logo'))
        self.savelogo.props.sensitive = True
        self.savelogo.connect('clicked', self.do_savelogo)
        self.insert(self.savelogo, -1)
        self.savelogo.show()

    def do_samples(self, button):
        tawindow.load_file(self.activity.tw)
#        self.activity.jobject_new_patch()

    def do_savelogo(self, button):
        # write logo code out to datastore
        print "saving logo code"
        # grab code from stacks
        logocode = self.save_logo(self.activity.tw)
        if len(logocode) == 0:
            return
        filename = "logosession.lg"

        # Create a datastore object
        file_dsobject = datastore.create()

        # Write any metadata (here we specifically set the title of the file and
        # specify that this is a plain text file). 
        file_dsobject.metadata['title'] = filename
        file_dsobject.metadata['mime_type'] = 'text/plain'
        file_dsobject.metadata['icon-color'] = profile.get_color().to_string()

        #Write the actual file to the data directory of this activity's root. 
        file_path = os.path.join(self.activity.get_activity_root(), 'instance', filename)
        f = open(file_path, 'w')
        try:
            f.write(logocode)
        finally:
            f.close()

        #Set the file_path in the datastore.
        file_dsobject.set_file_path(file_path)

        datastore.write(file_dsobject)
        return

    def save_logo(self, tw):
        color_processing = "\
to tasetpalette :i :r :g :b :myshade \r\
make \"s ((:myshade - 50) / 50) \r\
ifelse lessp :s 0 [ \r\
make \"s (1 + (:s *0.8)) \r\
make \"r (:r * :s) \r\
make \"g (:g * :s) \r\
make \"b (:b * :s) \r\
] [ \
make \"s (:s * 0.9) \r\
make \"r (:r + ((100-:r) * :s)) \r\
make \"g (:g + ((100-:g) * :s)) \r\
make \"b (:b + ((100-:b) * :s)) \r\
] \
setpalette :i (list :r :g :b) \r\
end \r\
\
to rgb :myi :mycolors :myshade \r\
make \"myr first :mycolors \r\
make \"mycolors butfirst :mycolors \r\
make \"myg first :mycolors \r\
make \"mycolors butfirst :mycolors \r\
make \"myb first :mycolors \r\
make \"mycolors butfirst :mycolors \r\
tasetpalette :myi :myr :myg :myb :myshade \r\
output :mycolors \r\
end \r\
\
to processcolor :mycolors :myshade \r\
if emptyp :mycolors [stop] \r\
make \"i :i + 1 \r\
processcolor (rgb :i :mycolors :myshade) :myshade \r\
end \r\
\
to tasetshade :shade \r\
make \"myshade modulo :shade 200 \r\
if greaterp :myshade 99 [make \"myshade (199-:myshade)] \r\
make \"i 7 \r\
make \"mycolors :colors \r\
processcolor :mycolors :myshade \r\
end \r\
\
to tasetpencolor :c \r\
make \"color (modulo (round :c) 100) \r\
setpencolor :color + 8 \r\
end \r\
\
make \"colors [ \
100 0 0 100 5 0 100 10 0 100 15 0 100 20 0 100 25 0 100 30 0 100 35 0 100 40 0 100 45 0 \
100 50 0 100 55 0 100 60 0 100 65 0 100 70 0 100 75 0 100 80 0 100 85 0 100 90 0 100 95 0 \
100 100 0 90 100 0 80 100 0 70 100 0 60 100 0 50 100 0 40 100 0 30 100 0 20 100 0 10 100 0 \
0 100 0 0 100 5 0 100 10 0 100 15 0 100 20 0 100 25 0 100 30 0 100 35 0 100 40 0 100 45 \
0 100 50 0 100 55 0 100 60 0 100 65 0 100 70 0 100 75 0 100 80 0 100 85 0 100 90 0 100 95 \
0 100 100 0 95 100 0 90 100 0 85 100 0 80 100 0 75 100 0 70 100 0 65 100 0 60 100 0 55 100 \
0 50 100 0 45 100 0 40 100 0 35 100 0 30 100 0 25 100 0 20 100 0 15 100 0 10 100 0 5 100 \
0 0 100 5 0 100 10 0 100 15 0 100 20 0 100 25 0 100 30 0 100 35 0 100 40 0 100 45 0 100 \
50 0 100 55 0 100 60 0 100 65 0 100 70 0 100 75 0 100 80 0 100 85 0 100 90 0 100 95 0 100 \
100 0 100 100 0 90 100 0 80 100 0 70 100 0 60 100 0 50 100 0 40 100 0 30 100 0 20 100 0 10] \r\
make \"shade 50 \r\
tasetshade :shade \r"

        bs = tawindow.blocks(tw)
        code = ""
        random = 0
        fillscreen = 0
        setcolor = 0
        setxy = 0
        pensize = 0
        tastack = 0
        arc = 0
        for b in bs:
             this_stack = ""
             data = self.walk_stack(tw, b)
             # need to catch several special cases:
             # stacks, random, setshade, et al.
             stack = 0
             for d in data:
                 if type(d) is float:
                     this_stack += str(d)
                 else:
                     # transalate some TA terms into UCB Logo
                     if d == "storeinbox1":
                         this_stack += "make \"box1"
                     elif d == "box1":
                         this_stack += ":box1"
                     elif d == "storeinbox2":
                         this_stack += "make \"box2"
                     elif d == "box2":
                         this_stack += ":box2"
                     elif d == "shade":
                         this_stack += ":shade"
                     elif d == "setshade":
                         setcolor = 1
                         this_stack += "tasetshade"
                     elif d == "color":
                         this_stack += "pencolor"
                     elif d == "nop":
                         this_stack += " "
                     elif d == "nop1":
                         this_stack += "to stack1\r"
                         stack = 1
                     elif d == "nop2":
                         this_stack += "to stack2\r"
                         stack = 1
                     elif d == "clean":
                         this_stack += "clearscreen"
                     elif d == "setxy":
                         setxy = 1
                         this_stack += "tasetxy"
                     elif d == "color":
                         this_stack += ":color"
                     elif d == "setcolor":
                         setcolor = 1
                         this_stack += "tasetpencolor"
                     elif d == "fillscreen":
                         fillscreen = 1
                         this_stack += "tasetbackground"
                     elif d == "random":
                         random = 1
                         this_stack += "tarandom"
                     elif d == "pensize":
                         pensize = 1
                         this_stack += "tapensize"
                     elif d == "arc":
                         arc = 1
                         this_stack += "taarc"
                     else:
                         this_stack += d
                 this_stack += " "
             if stack:
                 stack = 0
             # if it is not a stack, we need to add a "to ta#" label
             elif len(data) > 0:
                 this_stack = "to ta" + str(tastack) + "\r" + this_stack
                 tastack += 1
             if len(data) > 0:
                 code += this_stack
                 code += "\rend\r"
        # need to define some procedures
        if random: # to avoid negative numbers
             code = "to tarandom :min :max\routput (random (:max - :min)) + :min\rend\r" + code
        if fillscreen: # set shade than background color
             code = "to tasetbackground :color :shade\rtasetshade :shade\rsetbackground :color\rend\r" + code
        if setcolor: # load palette
             code = color_processing + code
        if pensize: # return only first argument
             code = "to tapensize\routput first round pensize\rend\r" + code
        if setxy: # swap args and round args
             code = "to tasetxy :y :x\rpenup\rsetxy :x :y\rpendown\rend\r" + code
        if arc:
             c = (2 * math.pi)/360
             code = "to taarc :a :r\rrepeat round :a [right 1 forward (" + str(c) + " * :r)]\rend\r" + code
        code = "window\rsetscrunch 2 2\r" + code
        print code
        return code

    def walk_stack(self, tw, spr):
        top = tawindow.find_top_block(spr)
        if spr == top:
            # only walk the stack if the block is the top block
            return talogo.walk_blocks(tw.lc, top, tawindow.blocks(tw))
        else:
            # not top of stack, then return empty list
            return []

