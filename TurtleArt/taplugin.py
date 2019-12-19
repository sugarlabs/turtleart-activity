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

import configparser
from gettext import gettext as _
import os
import shutil
import subprocess
from TurtleArt.tapalette import (palette_names, help_strings)


def cancel_plugin_install(tmp_dir):
    ''' If we cancel, just cleanup '''
    shutil.rmtree(tmp_dir)


def complete_plugin_install(cls, tmp_dir, tmp_path, plugin_path,
                            plugin_name, file_info):
    ''' We complete the installation directly or from ConfirmationAlert '''
    status = subprocess.call(['cp', '-r', tmp_path, plugin_path + '/'])
    if status == 0:
        # Save the plugin.info file in the plugin directory
        subprocess.call(['cp', os.path.join(tmp_dir, 'plugin.info'),
                         os.path.join(plugin_path, plugin_name) + '/'])

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
        cls.tw.init_plugin(plugin_name)
        cls.tw.turtleart_plugins[-1].setup()
        cls.tw.load_media_shapes()
        for i, palette_name in enumerate(palette_name_list):
            if create_palette[i]:
                j = len(cls.palette_buttons)
                cls.palette_buttons.append(
                    cls._radio_button_factory(
                        palette_name.strip() + 'off',
                        cls._palette_toolbar,
                        cls.do_palette_buttons_cb,
                        j - 1,
                        help_strings[palette_name.strip()],
                        cls.palette_buttons[0]))
                cls._overflow_buttons.append(
                    cls._add_button(
                        palette_name.strip() + 'off',
                        None,
                        cls.do_palette_buttons_cb,
                        None,
                        arg=j - 1))
                cls._overflow_box.pack_start(
                    cls._overflow_buttons[j - 1], True, True, 0)
                cls.tw.palettes.insert(j - 1, [])
                cls.tw.palette_sprs.insert(j - 1, [None, None])
            else:
                # We need to change the index associated with the
                # Trash Palette Button.
                j = len(palette_names)
                pidx = palette_names.index(palette_name.strip())
                cls.palette_buttons[pidx].connect(
                    'clicked', cls.do_palette_buttons_cb, j - 1)
                cls._overflow_buttons[pidx].connect(
                    'clicked', cls.do_palette_buttons_cb, j - 1)
                cls._setup_palette_toolbar()
        cls.tw.showlabel(
            'status',
            _('Please restart %s in order to use the plugin.') % cls.name)

    else:
        cls.tw.showlabel('status', _('Plugin could not be installed.'))
    status = subprocess.call(['rm', '-r', tmp_path])
    shutil.rmtree(tmp_dir)


def load_a_plugin(cls, tmp_dir):
    ''' Load a plugin from the Journal and initialize it '''
    plugin_path = os.path.join(tmp_dir, 'plugin.info')
    file_info = configparser.ConfigParser()
    if len(file_info.read(plugin_path)) == 0:
        cls.tw.showlabel('status', _('Plugin could not be installed.'))
    elif not file_info.has_option('Plugin', 'name'):
        cls.tw.showlabel('status', _('Plugin could not be installed.'))
    else:
        plugin_name = file_info.get('Plugin', 'name')
        tmp_path = os.path.join(tmp_dir, plugin_name)
        plugin_path = os.path.join(cls.bundle_path, 'plugins')
        if os.path.exists(os.path.join(plugin_path, plugin_name)):
            cls._reload_plugin_alert(tmp_dir, tmp_path, plugin_path,
                                     plugin_name, file_info)
        else:
            complete_plugin_install(cls, tmp_dir, tmp_path, plugin_path,
                                    plugin_name, file_info)
