#!/usr/bin/env python3
# Copyright (c) 2011 Walter Bender
# Copyright (c) 2010 Jamie Boisture
# Copyright (c) 2011 Collabora Ltd. <http://www.collabora.co.uk/>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

try:
    import pycurl
    import xmlrpc.client
    _UPLOAD_AVAILABLE = True
except ImportError as e:
    print("Import Error: %s. Project upload is disabled." % (e))
    _UPLOAD_AVAILABLE = False

import os
from gettext import gettext as _

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .plugin import Plugin
from TurtleArt.util.menubuilder import make_menu_item, make_sub_menu, MENUBAR


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
        if _('Upload') in MENUBAR:
            menu, upload_menu = MENUBAR[_('Upload')]
            already_existed = True
        else:
            upload_menu = None
            from gi.repository import Gio
            menu = Gio.Menu()
            already_existed = False
            
        if upload_menu is None:
            upload_menu = make_sub_menu(menu, _('Upload'))
            
        make_menu_item(upload_menu, _('Upload to Web'),
                       self.do_upload_to_web)
                       
        if already_existed:
            return None
        return menu

    def enabled(self):
        return _UPLOAD_AVAILABLE

    def do_upload_to_web(self, widget=None):
        if self.uploading:
            return

        self.uploading = True
        self.pop_up = Gtk.Window()
        self.pop_up.set_default_size(600, 400)
        self.pop_up.connect('close-request', self._stop_uploading)
        grid = Gtk.Grid(row_spacing=6, column_spacing=10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        self.pop_up.set_child(grid)

        login_label = Gtk.Label(label=_('You must have an account at \
http://turtleartsite.sugarlabs.org to upload your project.'))
        grid.attach(login_label, 0, 0, 1, 1)
        self.login_message = Gtk.Label(label='')
        grid.attach(self.login_message, 0, 1, 1, 1)

        self.Hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(self.Hbox1, 0, 2, 1, 1)
        self.username_entry = Gtk.Entry()
        username_label = Gtk.Label(label=_('Username:') + ' ')
        username_label.set_size_request(150, 25)
        username_label.set_halign(Gtk.Align.END)
        username_label.set_valign(Gtk.Align.CENTER)
        self.username_entry.set_size_request(450, 25)
        self.Hbox1.append(username_label)
        self.Hbox1.append(self.username_entry)

        self.Hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(self.Hbox2, 0, 3, 1, 1)
        self.password_entry = Gtk.Entry()
        password_label = Gtk.Label(label=_('Password:') + ' ')
        self.password_entry.set_visibility(False)
        password_label.set_size_request(150, 25)
        password_label.set_halign(Gtk.Align.END)
        password_label.set_valign(Gtk.Align.CENTER)
        self.password_entry.set_size_request(450, 25)
        self.Hbox2.append(password_label)
        self.Hbox2.append(self.password_entry)

        self.Hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(self.Hbox3, 0, 4, 1, 1)
        self.title_entry = Gtk.Entry()
        title_label = Gtk.Label(label=_('Title:') + ' ')
        title_label.set_size_request(150, 25)
        title_label.set_halign(Gtk.Align.END)
        title_label.set_valign(Gtk.Align.CENTER)
        self.title_entry.set_size_request(450, 25)
        self.Hbox3.append(title_label)
        self.Hbox3.append(self.title_entry)

        self.Hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(self.Hbox4, 0, 5, 1, 1)
        self.description_entry = Gtk.TextView()
        description_label = Gtk.Label(label=_('Description:') + ' ')
        description_label.set_size_request(150, 25)
        description_label.set_halign(Gtk.Align.END)
        description_label.set_valign(Gtk.Align.CENTER)
        self.description_entry.set_wrap_mode(Gtk.WrapMode.WORD)
        self.description_entry.set_size_request(450, 50)
        self.Hbox4.append(description_label)
        self.Hbox4.append(self.description_entry)

        self.Hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(self.Hbox5, 0, 6, 1, 1)
        self.submit_button = Gtk.Button(label=_('Submit to Web'))
        self.submit_button.set_size_request(300, 25)
        self.submit_button.connect('clicked', self._do_remote_logon)
        self.Hbox5.append(self.submit_button)
        self.cancel_button = Gtk.Button(label=_('Cancel'))
        self.cancel_button.set_size_request(300, 25)
        self.cancel_button.connect('clicked', self._stop_uploading)
        self.Hbox5.append(self.cancel_button)

        self.pop_up.present()

    def _stop_uploading(self, widget=None, event=None):
        """ Hide the popup when the upload is complte """
        self.uploading = False
        self.pop_up.set_visible(False)
        return False

    def _do_remote_logon(self, widget):
        """ Log into the upload server """
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()
        server = xmlrpc.client.ServerProxy(
            self._upload_server + '/call/xmlrpc')
        logged_in = None
        try:
            logged_in = server.login_remote(username, password)
        except Exception as e:
            print("Login failed %s" % e)
        if logged_in:
            upload_key = logged_in
            self._do_submit_to_web(upload_key)
        else:
            self.login_message.set_text(_('Login failed'))

    def _do_submit_to_web(self, key):
        """ Submit project to the server """
        title = self.title_entry.get_text()
        description = self.description_entry.get_buffer().get_text(
            *self.description_entry.get_buffer().get_bounds(), True)
        tafile, imagefile = self.tw.save_for_upload(title)

        # Set a maximum file size for image to be uploaded.
        if int(os.path.getsize(imagefile)) > self._max_file_size:
            from PIL import Image
            while int(os.path.getsize(imagefile)) > self._max_file_size:
                with Image.open(imagefile) as big_file:
                    smaller_file = big_file.resize(
                        (int(0.9 * big_file.size[0]), int(0.9 * big_file.size[1])),
                        getattr(Image, 'Resampling', Image).LANCZOS)
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
        c.close()
        os.remove(imagefile)
        os.remove(tafile)
        if error_code == 400:
            self.login_message.set_text(_('Failed to upload!'))
        else:
            self.pop_up.set_visible(False)
            self.uploading = False



