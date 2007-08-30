import ta
import pygtk
pygtk.require('2.0')
import gtk

from socket import *
import sys
import gobject

serverHost = '192.168.1.101'
serverPort = 5647

import sugar
from sugar.activity import activity
from sugar.activity import registry
from sugar.graphics.toolbutton import ToolButton
from sugar.datastore import datastore
from sugar import profile
from gettext import gettext as _


class TurtleArtActivity(activity.Activity):
    def __init__(self, handle):
        super(TurtleArtActivity,self).__init__(handle)
#        self.debug_init()

        self.gamename = 'turtleart'
        self.set_title("TurtleArt")

        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        self.projectToolbar = ProjectToolbar(self)
        toolbox.add_toolbar( ('Project'), self.projectToolbar )
        toolbox.show()

        toolbox._activity_toolbar.keep.connect('clicked', self._keep_clicked_cb) # patch

        self.connect('destroy', self._cleanup_cb)

        canvas = gtk.EventBox()

        sugar.graphics.window.Window.set_canvas(self, canvas)

        ta.init(canvas, activity.get_bundle_path(),self)

        if self._jobject and self._jobject.file_path:
            self.read_file(self._jobject.file_path)

    def _cleanup_cb(self, data=None):
        return

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
            ta.save_data(tafile)
            ta.save_pict(pngfile)
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
            ta.load_files(os.path.join(tmpdir, 'ta_code.ta'), os.path.join(tmpdir, 'ta_image.png'))

        finally:
            shutil.rmtree(tmpdir)
            tar_fd.close()

    def debug_init(self):
        s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
        s.connect((serverHost, serverPort)) # connect to server on the port
        sys.stdout = s.makefile()
        sys.stderr = sys.stdout
        gobject.timeout_add(100, self.debug_tick)

    def debug_tick(self):
        sys.stdout.flush()
        return True

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
        ta.load_file()
#        self.activity.jobject_new_patch()

