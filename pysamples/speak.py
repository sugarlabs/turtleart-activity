#Copyright (c) 2009-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block and
# pass a string to be read by the voice synthesizer. If a second
# argument is passed, by expanding the Python block, it is used to specify
# the pitch level of the speaker. Valid range is 0 to 99.


def myblock(tw, arg):
    ''' Text to speech '''

    import os

    pitch = None
    if type(arg) == type([]):
        text = arg[0]
        if len(arg) > 1:
            pitch = int(arg[1])
            if pitch > 99:
                pitch = 99
            elif pitch < 0:
                pitch = 0
    else:
        text = arg

    # Turtle Art numbers are passed as float,
    # but they may be integer values.
    if type(text) == float and int(text) == text:
        text = int(text)

    if pitch is None:
        os.system('espeak "%s" --stdout | aplay' % (text))
    else:
        os.system('espeak "%s" -p "%s" --stdout | aplay' % (text, pitch))
