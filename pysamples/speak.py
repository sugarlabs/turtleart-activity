#Copyright (c) 2009-10, Walter Bender, Tony Forster

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#
# This procedure is invoked when the user-definable block on the "extras"
# palette is selected.

# Usage: Import this code into a Python (user-definable) block and
# pass a string to be read by the voice synthesizer. If a second
# argument is passed, by expanding the Python block, it is used to specify
# the pitch level of the speaker. Valid range is 0 to 99.


def myblock(tw, arg):

    ###########################################################################
    #
    # Text to speech
    #
    ###########################################################################

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
