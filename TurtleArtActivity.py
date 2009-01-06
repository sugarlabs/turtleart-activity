#Copyright (c) 2007-9, Playful Invention Company.

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

    from taexport import *

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
