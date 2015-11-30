#!/usr/bin/env python

import sys

if len(sys.argv) > 1 and '--no-sugar' == sys.argv[1]:
    # Remove the argument from the stack so we don't cause problems
    # for distutils
    sys.argv.pop(1)

    import os
    import glob
    import shutil
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
