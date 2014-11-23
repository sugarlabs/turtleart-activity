#!/usr/bin/env python

import sys

if len(sys.argv) > 1 and '--no-sugar' == sys.argv[1]:
    # Remove the argument from the stack so we don't cause problems
    # for distutils
    sys.argv.pop(1)
    
    import glob
    from distutils.core import setup
    
    DATA_FILES = [
        ('icons', glob.glob('icons/*')),
        ('images', glob.glob('images/*')),
        ('/usr/share/applications', ['turtleblocks.desktop'])
        ]

    setup (name = 'Turtle Art',
           description = "A LOGO-like tool for teaching programming",
           author = "Walter Bender",
           author_email = "walter.bender@gmail.com",
           version = '2.0.9',
           packages = ['TurtleArt', 'util'],
           scripts = ['turtleart'],
           data_files = DATA_FILES,
           )
else: 
    from sugar.activity import bundlebuilder

    if __name__ == "__main__":
        bundlebuilder.start()
