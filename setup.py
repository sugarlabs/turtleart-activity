#!/usr/bin/env python
import os

if 'SUGAR_ACTIVITY_ROOT' in os.environ:
    from sugar.activity import bundlebuilder

    if __name__ == "__main__":
        bundlebuilder.start()
else:
    import glob, os.path, string
    from distutils.core import setup

    DATA_FILES = [
        ('icons', glob.glob('icons/*')),
        ('images', glob.glob('images/*')),
        ('/usr/share/applications', ['turtleart.desktop'])
        ]

    setup (name = 'Turtle Art',
           description = "A LOGO-like tool for teaching programming",
           author = "Walter Bender",
           author_email = "walter.bender@gmail.com",
           version = '0.9.4',
           packages = ['TurtleArt'],
           scripts = ['turtleart'],
           data_files = DATA_FILES,
           )
