# Copyright (c) 2010-11, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block and
# pass a frequency in Hertz to the Python block. A tone will play over
# the speaker at the specified frequency.


def myblock(tw, args):
    ''' Plays a sound at frequency frequency '''

    import os
    frequency = args[0]
    os.system('speaker-test -t sine -l 1 -f %d' % (int(frequency)))
