#!/usr/bin/env python
#Copyright (c) 2011 Walter Bender
#Copyright (c) 2010 Jamie Boisture
#Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

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

#!/usr/bin/python

try:
    import pycurl
    import xmlrpclib
    _UPLOAD_AVAILABLE = True
except ImportError, e:
    print "Import Error: %s. Project upload is disabled." % (e)
    _UPLOAD_AVAILABLE = False

import os
import gtk

from plugin import Plugin
from util.menubuilder import MenuBuilder

from gettext import gettext as _


class Uploader_plugin(Plugin):
    MAX_FILE_SIZE = 950000
    UPLOAD_SERVER = 'http://turtleartsite.appspot.com'

    def __init__(self, parent, upload_server=None, max_file_size=None):
        self._parent = parent
        self.uploading = False

        if upload_server is None:
            self._upload_server = self.UPLOAD_SERVER

        if max_file_size is None:
            self._max_file_size = self.MAX_FILE_SIZE
        else:
            self._max_file_size = max_file_size

    def set_tw(self, turtleart_window):
        self.tw = turtleart_window

    def get_menu(self):
        menu = gtk.Menu()
        MenuBuilder.make_menu_item(menu, _('Upload to Web'),
                                   self.do_upload_to_web)
        upload_menu = MenuBuilder.make_sub_menu(menu, _('Upload'))
        return upload_menu

    def enabled(self):
        return _UPLOAD_AVAILABLE

    def do_upload_to_web(self, widget=None):
        if self.uploading:
            return

        self.uploading = False
        self.pop_up = gtk.Window()
        self.pop_up.set_default_size(600, 400)
        self.pop_up.connect('delete_event', self._stop_uploading)
        table = gtk.Table(8, 1, False)
        self.pop_up.add(table)

        login_label = gtk.Label(_('You must have an account at \
http://turtleartsite.sugarlabs.org to upload your project.'))
        table.attach(login_label, 0, 1, 0, 1)
        self.login_message = gtk.Label('')
        table.attach(self.login_message, 0, 1, 1, 2)

        self.Hbox1 = gtk.HBox()
        table.attach(self.Hbox1, 0, 1, 2, 3, xpadding=5, ypadding=3)
        self.username_entry = gtk.Entry()
        username_label = gtk.Label(_('Username:') + ' ')
        username_label.set_size_request(150, 25)
        username_label.set_alignment(1.0, 0.5)
        self.username_entry.set_size_request(450, 25)
        self.Hbox1.add(username_label)
        self.Hbox1.add(self.username_entry)

        self.Hbox2 = gtk.HBox()
        table.attach(self.Hbox2, 0, 1, 3, 4, xpadding=5, ypadding=3)
        self.password_entry = gtk.Entry()
        password_label = gtk.Label(_('Password:') + ' ')
        self.password_entry.set_visibility(False)
        password_label.set_size_request(150, 25)
        password_label.set_alignment(1.0, 0.5)
        self.password_entry.set_size_request(450, 25)
        self.Hbox2.add(password_label)
        self.Hbox2.add(self.password_entry)

        self.Hbox3 = gtk.HBox()
        table.attach(self.Hbox3, 0, 1, 4, 5, xpadding=5, ypadding=3)
        self.title_entry = gtk.Entry()
        title_label = gtk.Label(_('Title:') + ' ')
        title_label.set_size_request(150, 25)
        title_label.set_alignment(1.0, 0.5)
        self.title_entry.set_size_request(450, 25)
        self.Hbox3.add(title_label)
        self.Hbox3.add(self.title_entry)

        self.Hbox4 = gtk.HBox()
        table.attach(self.Hbox4, 0, 1, 5, 6, xpadding=5, ypadding=3)
        self.description_entry = gtk.TextView()
        description_label = gtk.Label(_('Description:') + ' ')
        description_label.set_size_request(150, 25)
        description_label.set_alignment(1.0, 0.5)
        self.description_entry.set_wrap_mode(gtk.WRAP_WORD)
        self.description_entry.set_size_request(450, 50)
        self.Hbox4.add(description_label)
        self.Hbox4.add(self.description_entry)

        self.Hbox5 = gtk.HBox()
        table.attach(self.Hbox5, 0, 1, 6, 7, xpadding=5, ypadding=3)
        self.submit_button = gtk.Button(_('Submit to Web'))
        self.submit_button.set_size_request(300, 25)
        self.submit_button.connect('pressed', self._do_remote_logon)
        self.Hbox5.add(self.submit_button)
        self.cancel_button = gtk.Button(_('Cancel'))
        self.cancel_button.set_size_request(300, 25)
        self.cancel_button.connect('pressed', self._stop_uploading)
        self.Hbox5.add(self.cancel_button)

        self.pop_up.show_all()

    def _stop_uploading(self, widget, event=None):
        """ Hide the popup when the upload is complte """
        self.uploading = False
        self.pop_up.hide()

    def _do_remote_logon(self, widget):
        """ Log into the upload server """
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()
        server = xmlrpclib.ServerProxy(self._upload_server + '/call/xmlrpc')
        logged_in = server.login_remote(username, password)
        if logged_in:
            upload_key = logged_in
            self._do_submit_to_web(upload_key)
        else:
            self.login_message.set_text(_('Login failed'))

    def _do_submit_to_web(self, key):
        """ Submit project to the server """
        title = self.title_entry.get_text()
        description = self.description_entry.get_buffer().get_text(
            *self.description_entry.get_buffer().get_bounds())
        tafile, imagefile = self.tw.save_for_upload(title)

        # Set a maximum file size for image to be uploaded.
        if int(os.path.getsize(imagefile)) > self._max_file_size:
            import Image
            while int(os.path.getsize(imagefile)) > self._max_file_size:
                big_file = Image.open(imagefile)
                smaller_file = big_file.resize(int(0.9 * big_file.size[0]),
                                               int(0.9 * big_file.size[1]),
                                               Image.ANTIALIAS)
                smaller_file.save(imagefile, quality=100)

        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.URL, self._upload_server + '/upload')
        c.setopt(c.HTTPHEADER, ["Expect:"])
        c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, tafile)),
                              ('newimage', (c.FORM_FILE, imagefile)),
                              ('small_image', (c.FORM_FILE, imagefile)),
                              ('title', title),
                              ('description', description),
                              ('upload_key', key), ('_formname',
                                                   'image_create')])
        c.perform()
        error_code = c.getinfo(c.HTTP_CODE)
        c.close
        os.remove(imagefile)
        os.remove(tafile)
        if error_code == 400:
            self.login_message.set_text(_('Failed to upload!'))
        else:
            self.pop_up.hide()
            self.uploading = False

if __name__ == "__main__":
    # TODO: create test data...
    u = Uploader(None)
    if u.enabled():
        print "Uploader is enabled... trying to upload"
        u.do_upload_to_web()
        gtk.main()
    else:
        print "Uploader is not enabled... exiting"
