import tawindow
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
from sugar.activity import registry
from sugar.graphics.toolbutton import ToolButton
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
        toolbox.add_toolbar( ('Project'), self.projectToolbar )
        toolbox.show()

#        toolbox._activity_toolbar.keep.connect('clicked', self._keep_clicked_cb) # patch

        canvas = gtk.EventBox()

        sugar.graphics.window.Window.set_canvas(self, canvas)
        toolbox._activity_toolbar.title.grab_focus()
        toolbox._activity_toolbar.title.select_region(0,0)

        lang = locale.getdefaultlocale()[0]
        if not lang: lang = 'en'
        lang = lang[0:2]
        if not os.path.isdir(os.path.join(activity.get_bundle_path(),'images',lang)):
            lang = 'en'

        self.tw = tawindow.twNew(canvas, activity.get_bundle_path(),lang,self)
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
        self.sampb.set_tooltip("samples")
        self.sampb.props.sensitive = True
        self.sampb.connect('clicked', self.do_samples)
        self.insert(self.sampb, -1)
        self.sampb.show()


    def do_samples(self, button):
        tawindow.load_file(self.activity.tw)
#        self.activity.jobject_new_patch()

