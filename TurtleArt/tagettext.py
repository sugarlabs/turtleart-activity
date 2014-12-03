# -*- coding: utf-8 -*-
# Copyright (c) 2010-11 Walter Bender, Martin Langhoff
# License: GPLv2

# Defines the magic global _() with the right params so all modules
# can use it.
#
# Plugins that want to override MUST use a different technique. See
# the developer notes in the TA wikipage.
#
import gettext
import os

# In a git checkout, locale is in the root of the project
# so one dir "up" from tagettext.py
localedir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'locale')

if os.path.exists(localedir):
    # works from a git checkout
    gettext.install('org.laptop.TurtleArtActivity', localedir)
else:
    # fallback for packaged TA (rpm, xo)
    gettext.install('org.laptop.TurtleArtActivity')
