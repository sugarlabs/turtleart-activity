#!/usr/bin/env python
import os
import sys

if len(sys.argv) > 1 and '--no-sugar' == sys.argv[1]:
    # Remove the argument from the stack so we don't cause problems
    # for distutils
    sys.argv.pop(1)
    
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
else: 
    from sugar.activity import bundlebuilder

    if __name__ == "__main__":
        bundlebuilder.start()
