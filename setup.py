#!/usr/bin/env python

import sys
from configparser import ConfigParser
import xml.etree.cElementTree as ET


def get_files(path):
    files = []
    for name in os.listdir(path):
        files.append(os.path.join(path, name))
    return files


def generate_appdata(prefix, bundle_id):
    info = ConfigParser()
    info.read(os.path.join('activity', 'activity.info'))

    required_fields = ['metadata_license', 'license', 'name', 'icon',
                       'description']
    for name in required_fields:
        if not info.has_option('Activity', name):
            print('[WARNING] Activity needs more metadata for AppStream '
                  'file')
            print('  Without an AppStream file, the activity will NOT '
                  'show in software stores!')
            print('  Please `pydoc sugar3.activity.bundlebuilder` for'
                  'more info')
            return

    # See https://www.freedesktop.org/software/appstream/docs/
    root = ET.Element('component', type='desktop-application')
    ET.SubElement(root, 'translation', type='gettext').text = \
        bundle_id
    ET.SubElement(root, 'id').text = bundle_id
    ET.SubElement(root, 'launchable', type='desktop-id').text = \
        bundle_id + ".desktop"
    desc = ET.fromstring('<description><p>{}</p></description>'.format(
        info.get('Activity', 'description')))
    root.append(desc)

    ET.SubElement(root, 'content_rating', type='oars-1.1')

    release_pairs = [('220', '2019-09-28'),
                     ('218', '2018-05-22'),
                     ('216', '2017-06-24'),
                     ('215', '2017-04-19')]
    releases_root = ET.SubElement(root, 'releases')
    for version, date in release_pairs:
        ET.SubElement(releases_root, 'release', date=date, version=version)

    license_map = {
      'GPLv2+': 'GPL-2.0-or-later',
      'GPLv3+': 'GPL-3.0-or-later',
      'LGPLv2+': 'LGPL-2.0-or-later',
      'LGPLv2.1+': 'LGPL-2.1-or-later',
    }
    licenses = info.get('Activity', 'license').split(';')
    spdx_licenses = [license_map.get(x, x) for x in licenses]
    ET.SubElement(root, 'project_license').text = " AND ".join(spdx_licenses)

    copy_pairs = [('metadata_license', 'metadata_license'),
                  ('summary', 'summary'),
                  ('name', 'name')]
    for key, ename in copy_pairs:
        ET.SubElement(root, ename).text = info.get('Activity', key)

    if info.has_option('Activity', 'screenshots'):
        screenshots = info.get('Activity', 'screenshots').split(',')
        ss_root = ET.SubElement(root, 'screenshots')
        for i, screenshot in enumerate(screenshots):
            e = ET.SubElement(ss_root, 'screenshot')
            if i == 0:
                e.set('type', 'default')
            ET.SubElement(e, 'image').text = screenshot.strip()

    if info.has_option('Activity', 'url'):
        ET.SubElement(root, 'url', type='homepage').text = \
            info.get('Activity', 'url')
    if info.has_option('Activity', 'repository_url'):
        ET.SubElement(root, 'url', type='bugtracker').text = \
            info.get('Activity', 'repository_url')
    elif info.has_option('Activity', 'repository'):
        ET.SubElement(root, 'url', type='bugtracker').text = \
            info.get('Activity', 'repository')

    path = os.path.join(prefix, 'share', 'metainfo',
                        bundle_id + '.appdata.xml')
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    tree = ET.ElementTree(root)
    tree.write(path, encoding='UTF-8')


if len(sys.argv) > 1 and '--no-sugar' == sys.argv[1]:
    # Remove the argument from the stack so we don't cause problems
    # for distutils
    sys.argv.pop(1)

    import os
    import shutil
    import subprocess
    from distutils.core import setup
    from distutils.command.install import install

    class post_install(install):
        def run(self):
            install.run(self)
            print("Running post_install")

            generate_appdata(self.prefix,
                             'org.laptop.TurtleArtActivity')

            # Create a simple module that allows the app where to discover
            # its lib and share content.
            dst = os.path.join(self.install_purelib, "TurtleArt")
            fd = open(os.path.join(dst, "installinfo.py"), "w")
            fd.write("INSTALL_PREFIX='%s'\n" % self.prefix)
            fd.close()

            root = self.root or ''

            # distutils doesn't offer a nice way to do recursive install of
            # a directory tree, so we install the remaining parts here.
            libdir = os.path.join(root + self.install_base, "lib",
                                  "TurtleBlocks")
            if not os.path.isdir(libdir):
                os.makedirs(libdir)

            sharedir = os.path.join(root + self.install_base, "share",
                                    "TurtleBlocks")
            if not os.path.isdir(sharedir):
                os.makedirs(sharedir)

            shutil.copytree("plugins", os.path.join(libdir, "plugins"))
            shutil.copytree("samples", os.path.join(sharedir, "samples"))

            localedir = os.path.join(root + self.install_base, "share",
                                     "locale")
            for f in os.listdir('po'):
                if not f.endswith('.po') or f == 'pseudo.po':
                    continue

                file_name = os.path.join('po', f)
                lang = f[:-3]

                mo_path = os.path.join(localedir, lang, 'LC_MESSAGES')
                if not os.path.isdir(mo_path):
                    os.makedirs(mo_path)

                mo_file = os.path.join(
                    mo_path, 'org.laptop.TurtleArtActivity.mo')
                retcode = subprocess.call(
                    ['msgfmt', '--output-file=%s' % mo_file, file_name])
                if retcode:
                    print('ERROR - msgfmt failed with return code %i.'
                          % retcode)

    DATA_FILES = [
        ('activity', get_files('activity/')),
        ('icons', get_files('icons/')),
        ('images', get_files('images/')),
        ('/usr/share/applications', ['turtleblocks.desktop']),
        ('org.laptop.TurtleArtActivity.gschema.xml')
    ]

    setup(name='Turtle Art',
          description="A LOGO-like tool for teaching programming",
          author="Walter Bender",
          author_email="walter.bender@gmail.com",
          version='0.9.4',
          packages=['TurtleArt', 'TurtleArt.util'],
          scripts=['turtleblocks'],
          data_files=DATA_FILES,
          cmdclass={"install": post_install}
          )
else:
    from sugar3.activity import bundlebuilder

    if __name__ == "__main__":
        bundlebuilder.start()
