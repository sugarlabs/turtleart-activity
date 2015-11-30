#!/usr/bin/env python

import sys

if len(sys.argv) > 1 and '--no-sugar' == sys.argv[1]:
    # Remove the argument from the stack so we don't cause problems
    # for distutils
    sys.argv.pop(1)

    import os
    import glob
    import shutil
    import subprocess
    from distutils.core import setup
    from distutils.command.install import install

    class post_install(install):
        def run(self):
            install.run(self)
            print "Running post_install"

            # Create a simple module that allows the app where to discover
            # its lib and share content.
            dst = os.path.join(self.install_purelib, "TurtleArt")
            fd = open(os.path.join(dst, "installinfo.py"), "w")
            fd.write("INSTALL_PREFIX='%s'\n" % self.prefix)
            fd.close()

            # distutils doesn't offer a nice way to do recursive install of
            # a directory tree, so we install the remaining parts here.
            libdir = os.path.join(self.root + self.install_base, "lib",
                                  "TurtleBlocks")
            if not os.path.isdir(libdir):
                os.makedirs(libdir)

            sharedir = os.path.join(self.root + self.install_base, "share",
                                    "TurtleBlocks")
            if not os.path.isdir(sharedir):
                os.makedirs(sharedir)

            shutil.copytree("plugins", os.path.join(libdir, "plugins"))
            shutil.copytree("samples", os.path.join(sharedir, "samples"))

            localedir = os.path.join(self.root + self.install_base, "share",
                                     "locale")
            for f in os.listdir('po'):
                if not f.endswith('.po') or f == 'pseudo.po':
                    continue

                file_name = os.path.join('po', f)
                lang = f[:-3]

                mo_path = os.path.join(localedir, lang, 'LC_MESSAGES')
                if not os.path.isdir(mo_path):
                    os.makedirs(mo_path)

                mo_file = os.path.join(mo_path, 'org.laptop.TurtleArtActivity.mo')
                retcode = subprocess.call(['msgfmt', '--output-file=%s' % mo_file, file_name])
                if retcode:
                    print 'ERROR - msgfmt failed with return code %i.' % retcode

    DATA_FILES = [
        ('activity', glob.glob('activity/*')),
        ('icons', glob.glob('icons/*')),
        ('images', glob.glob('images/*')),
        ('/usr/share/applications', ['turtleblocks.desktop'])
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
    from sugar.activity import bundlebuilder

    if __name__ == "__main__":
        bundlebuilder.start()
