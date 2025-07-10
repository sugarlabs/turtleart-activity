#!/usr/bin/env python3
#
# Copyright (c) 2012 Raul Gutierrez S. - rgs@itevenworks.net
# Copyright (c) 2013 Alan Aguiar alanjas@hotmail.com

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

# NOTE: This is a plugin to enable uploading of Turtle Art projects to
# Facebook. It currently works for the GTK3 version of Turtle Blocks and
# only from the GNOME desktop.
# USAGE: Download this file into the gnome_plugin directory; make sure the
# filename is fb_plugin.py (Mediawiki capitalizes the first letter of files).
# When you launch TA from the GNOME desktop by running turtleblocks.py
# you should see a new menu, Facebook, which allows you to upload your
# project. Please report any problems to rgs and walter.


import pycurl
import urllib.parse

from gi.repository import Gtk

try:
    from gi.repository import WebKit
    HAS_WEBKIT = True
except BaseException:
    pass
    HAS_WEBKIT = False
from .plugin import Plugin
from TurtleArt.util.menubuilder import make_menu_item, make_sub_menu, MENUBAR
from gettext import gettext as _


class FbUploader():
    UPLOAD_URL = "https://graph.facebook.com/me/photos?access_token=%s"

    def __init__(self, image_path, access_token):
        self._image_path = image_path
        self._access_token = access_token

    def doit(self):
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.URL, self._get_url())
        c.setopt(c.HTTPPOST, self._get_params(c))
        c.perform()
        print(c.getinfo(c.HTTP_CODE))

    def _get_url(self):
        return self.UPLOAD_URL % (self._access_token)

    def _get_params(self, c):
        params = []
        params.append(('source', (c.FORM_FILE, self._image_path)))

        return params


class Fb_plugin(Plugin):
    APP_ID = "172917389475707"
    REDIRECT_URI = "http://www.sugarlabs.org"

    def __init__(self, parent):
        self._access_token = ""
        self._auth_win = None

    def get_menu(self):
        if _('Upload') in MENUBAR:
            menu, upload_menu = MENUBAR[_('Upload')]
        else:
            upload_menu = None
            menu = Gtk.Menu()

        make_menu_item(menu, _('Facebook wall post'), self._post_menu_cb)
        if upload_menu is not None:
            return None  # We don't have to add it since it already exists
        else:
            upload_menu = make_sub_menu(menu, _('Upload'))
            return upload_menu

    def set_tw(self, turtleart_window):
        self.tw = turtleart_window

    def enabled(self):
        return True

    def _post_menu_cb(self, widget):

        if self._access_token == "":
            self._grab_fb_app_token()
            return

        try:
            self._post_to_fb()
        except Exception as e:
            print('error while posting to Facebook:', e)

    def _grab_fb_app_token(self):
        url = self._get_auth_url()
        w = Gtk.Window()
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.show()
        w.move(200, 200)
        w.set_size_request(800, 400)
        wkv = WebKit.WebView()
        wkv.load_uri(url)
        wkv.grab_focus()
        wkv.connect('navigation-policy-decision-requested',
                    self._nav_policy_cb)
        sw.add_with_viewport(wkv)
        w.add(sw)
        w.show_all()
        self._auth_win = w

    def _get_auth_url(self):
        url = "http://www.facebook.com/dialog/oauth?client_id=%s" % (
            self.APP_ID)
        url += "&redirect_uri=%s" % (self.REDIRECT_URI)
        url += "&response_type=token&scope=publish_stream"

        return url

    def _nav_policy_cb(self, view, frame, req, action, param):
        uri = req.get_uri()
        if uri:
            url_o = urllib.parse.urlparse(uri)
            params = urllib.parse.parse_qs(url_o.fragment)
            if 'access_token' in params:
                self._access_token = params['access_token'][0]
                self._auth_win.hide()
                self._post_to_fb()

    def _post_to_fb(self):
        ta_file, image_file = self.tw.save_for_upload("ta fb")
        uploader = FbUploader(image_file, self._access_token)
        uploader.doit()
