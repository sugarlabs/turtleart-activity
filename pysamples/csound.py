#Copyright (c) 2011 Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block and
# pass a sound name Python block. The sound will play.

# Note: Assumes TamTam suite is installed in ~/Activities


def myblock(tw, sound):
    ''' Plays a sound file '''

    from TurtleArt.tautils import get_path
    import os
    import sys
    from gettext import gettext as _

    dirs = [os.path.join(os.environ['HOME'],
                'Activities/TamTamMini.activity/common/Resources/Sounds/')]
    orchlines = []
    scorelines = []
    instrlist = []
    fnum = [100]

    def finddir():
        for d in dirs:
            if os.path.isdir(d):
                return d

    def playWave(sound='horse', pitch=1, amplitude=1, loop=False, duration=1,
                 starttime=0, pitch_envelope='default',
                 amplitude_envelope='default'):
        """ Create a score to play a wave file. """

        if '/' in sound:
            fullname = sound
        else:
            fullname = finddir() + str(sound)

        if loop == False: lp = 0
        else: lp = 1

        if pitch_envelope == 'default': pitenv = 99
        else: pitenv = pitch_envelope

        if amplitude_envelope == 'default': ampenv = 100
        else: ampenv = amplitude_envelope

        if not 9 in instrlist:
            orchlines.append("instr 9\n") 
            orchlines.append("kpitenv oscil 1, 1/p3, p8\n")
            orchlines.append("aenv oscil 1, 1/p3, p9\n")
            orchlines.append("asig diskin p4, p5*kpitenv, 0, p7\n") 
            orchlines.append("out asig*p6*aenv\n")
            orchlines.append("endin\n\n")
            instrlist.append(9)

        scorelines.append('i9 %f %f "%s" %s %s %s %s %s\n' % (
                float(starttime), float(duration), fullname, str(pitch),
                str(amplitude), str(lp), str(pitenv), str(ampenv)))
    
    def audioWrite(file):
        """ Compile a .csd file. """

        csd = open(file, "w")
        csd.write("<CsoundSynthesizer>\n\n")
        csd.write("<CsOptions>\n")
        csd.write("-+rtaudio=alsa -odevaudio -m0 -d -b256 -B512\n")
        csd.write("</CsOptions>\n\n")
        csd.write("<CsInstruments>\n\n")
        csd.write("sr=16000\n")
        csd.write("ksmps=50\n")
        csd.write("nchnls=1\n\n")
        # csd.write(orchlines.pop())
        for line in orchlines:
            csd.write(line)
        csd.write("\n</CsInstruments>\n\n")
        csd.write("<CsScore>\n\n")
        csd.write("f1 0 2048 10 1\n")
        csd.write("f2 0 2048 10 1 0 .33 0 .2 0 .143 0 .111\n")
        csd.write("f3 0 2048 10 1 .5 .33 .25 .2 .175 .143 .125 .111 .1\n")
        csd.write("f10 0 2048 10 1 0 0 .3 0 .2 0 0 .1\n")
        csd.write("f99 0 2048 7 1 2048 1\n")
        csd.write("f100 0 2048 7 0. 10 1. 1900 1. 132 0.\n")
        csd.write(scorelines.pop())
        csd.write("e\n")
        csd.write("\n</CsScore>\n")
        csd.write("\n</CsoundSynthesizer>")
        csd.close()

    playWave(sound)  # Create a score.
    if tw.running_sugar:
        path = os.path.join(get_path(tw.activity, 'instance'), sound + '.csd')
    else:
        path = os.path.join('/tmp', sound + '.csd')
    audioWrite(path)  # Create a csound file from the score.
    os.system('csound ' + path)  # Play the csound file.
