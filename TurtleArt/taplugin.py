# Copyright (c) 2013 Walter Bender
# Copyright (c) 2013 Daniel Francis

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

import ConfigParser
from gettext import gettext as _
import os
import shutil
import subprocess
from TurtleArt.tapalette import (palette_names, help_strings)


def cancel_plugin_install(self, tmp_dir):
    ''' If we cancel, just cleanup '''
    shutil.rmtree(tmp_dir)


def complete_plugin_install(self, tmp_dir, tmp_path, plugin_path,
                            plugin_name, file_info):
    ''' We complete the installation directly or from ConfirmationAlert '''
    status = subprocess.call(['cp', '-r', tmp_path, plugin_path + '/'])
    if status == 0:
        # Save the plugin.info file in the plugin directory
        subprocess.call(['cp', os.path.join(tmp_dir, 'plugin.info'),
                         os.path.join(plugin_path, plugin_name) + '/'])
        if self.has_toolbarbox:
            palette_name_list = []
            if file_info.has_option('Plugin', 'palette'):
                palette_name_list = file_info.get(
                    'Plugin', 'palette').split(',')
                create_palette = []
                for palette_name in palette_name_list:
                    if not palette_name.strip() in palette_names:
                        create_palette.append(True)
                    else:
                        create_palette.append(False)
            self.tw.init_plugin(plugin_name)
            self.tw.turtleart_plugins[-1].setup()
            self.tw.load_media_shapes()
            for i, palette_name in enumerate(palette_name_list):
                if create_palette[i]:
                    j = len(self.palette_buttons)
                    self.palette_buttons.append(
                        self._radio_button_factory(
                            palette_name.strip() + 'off',
                            self._palette_toolbar,
                            self.do_palette_buttons_cb,
                            j - 1,
                            help_strings[palette_name.strip()],
                            self.palette_buttons[0]))
                    self._overflow_buttons.append(
                        self._add_button(
                            palette_name.strip() + 'off',
                            None,
                            self.do_palette_buttons_cb,
                            None,
                            arg=j - 1))
                    self._overflow_box.pack_start(
                        self._overflow_buttons[j - 1])
                    self.tw.palettes.insert(j - 1, [])
                    self.tw.palette_sprs.insert(j - 1, [None, None])
                else:
                    # We need to change the index associated with the
                    # Trash Palette Button.
                    j = len(palette_names)
                    pidx = palette_names.index(palette_name.strip())
                    self.palette_buttons[pidx].connect(
                        'clicked', self.do_palette_buttons_cb, j - 1)
                    self._overflow_buttons[pidx].connect(
                        'clicked', self.do_palette_buttons_cb, j - 1)
                    self._setup_palette_toolbar()
        else:
            l = _('Please restart %s in order to use the plugin.') % self.name
            self.tw.showlabel('status', l)
    else:
        self.tw.showlabel('status', _('Plugin could not be installed.'))
    status = subprocess.call(['rm', '-r', tmp_path])
    shutil.rmtree(tmp_dir)


def load_a_plugin(self, tmp_dir):
    ''' Load a plugin from the Journal and initialize it '''
    plugin_path = os.path.join(tmp_dir, 'plugin.info')
    file_info = ConfigParser.ConfigParser()
    if len(file_info.read(plugin_path)) == 0:
        self.tw.showlabel('status', _('Plugin could not be installed.'))
    elif not file_info.has_option('Plugin', 'name'):
        self.tw.showlabel('status', _('Plugin could not be installed.'))
    else:
        plugin_name = file_info.get('Plugin', 'name')
        tmp_path = os.path.join(tmp_dir, plugin_name)
        plugin_path = os.path.join(self.bundle_path, 'plugins')
        if os.path.exists(os.path.join(plugin_path, plugin_name)):
            self._reload_plugin_alert(tmp_dir, tmp_path, plugin_path,
                                      plugin_name, file_info)
        else:
            complete_plugin_install(self, tmp_dir, tmp_path, plugin_path,
                                    plugin_name, file_info)
