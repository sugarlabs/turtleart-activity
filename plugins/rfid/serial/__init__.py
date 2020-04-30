#!/usr/bin/env python
# portable serial port access with python
# this is a wrapper module for different platform implementations
#
# (C)2001-2002 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

VERSION = '2.4'

import sys

if sys.platform == 'cli':
    import serialcli
else:
    import os
    # chose an implementation, depending on os
    if os.name == 'nt':  # sys.platform == 'win32':
        import serialwin32
    elif os.name == 'posix':
        from . import serialposix
    elif os.name == 'java':
        import serialjava
    else:
        raise Exception(
            "Sorry: no implementation for your platform ('%s') available" %
            os.name)
