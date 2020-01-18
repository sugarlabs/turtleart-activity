# Copyright (c) 2011 Walter Bender

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block and
# pass a sound name Python block. The sound will play.
# Alternatively, pass a pitch, amplitude, and duration, e.g., 440, 5000, 1

# Note: Assumes TamTam suite is installed in ~/Activities


def myblock(tw, sound):
    ''' Plays a sound file '''

    from TurtleArt.tautils import get_path
    import os
    import tempfile

    dirs = [os.path.join(
        os.environ['HOME'],
        'Activities/TamTamMini.activity/common/Resources/Sounds/'),
        os.path.join(
        os.environ['HOME'],
        'Activities/TamTamJam.activity/common/Resources/Sounds/'),
        os.path.join(
        os.environ['HOME'],
        'Activities/TamTamEdit.activity/common/Resources/Sounds/')]
    orchlines = []
    scorelines = []
    instrlist = []

    def finddir():
        print(dirs)
        for d in dirs:
            if os.path.isdir(d):
                return d
        return '.'

    def playSine(pitch=1000, amplitude=5000, duration=1, starttime=0,
                 pitch_envelope='default', amplitude_envelope='default'):
        """ Create a score to play a sine wave. """
        _play(pitch, amplitude, duration, starttime, pitch_envelope,
              amplitude_envelope, 1)

    def _play(pitch, amplitude, duration, starttime, pitch_envelope,
              amplitude_envelope, instrument):
        if pitch_envelope == 'default':
            pitenv = 99
        else:
            pitenv = pitch_envelope

        if amplitude_envelope == 'default':
            ampenv = 100
        else:
            ampenv = amplitude_envelope

        if 1 not in instrlist:
            orchlines.append("instr 1\n")
            orchlines.append("kpitenv oscil 1, 1/p3, p6\n")
            orchlines.append("aenv oscil 1, 1/p3, p7\n")
            orchlines.append("asig oscil p5*aenv, p4*kpitenv, p8\n")
            orchlines.append("out asig\n")
            orchlines.append("endin\n\n")
            instrlist.append(1)

        scorelines.append("i1 %s %s %s %s %s %s %s\n" %
                          (str(starttime), str(duration), str(pitch),
                           str(amplitude), str(pitenv), str(ampenv),
                           str(instrument)))

    def playWave(sound='horse', pitch=1, amplitude=1, loop=False, duration=1,
                 starttime=0, pitch_envelope='default',
                 amplitude_envelope='default'):
        """ Create a score to play a wave file. """

        if '/' in sound:
            fullname = sound
        else:
            fullname = finddir() + str(sound)

        if loop:
            lp = 1
        else:
            lp = 0

        if pitch_envelope == 'default':
            pitenv = 99
        else:
            pitenv = pitch_envelope

        if amplitude_envelope == 'default':
            ampenv = 100
        else:
            ampenv = amplitude_envelope

        if 9 not in instrlist:
            orchlines.append("instr 9\n")
            orchlines.append("kpitenv oscil 1, 1/p3, p8\n")
            orchlines.append("aenv oscil 1, 1/p3, p9\n")
            orchlines.append("asig diskin p4, p5*kpitenv, 0, p7\n")
            orchlines.append("out asig*p6*aenv\n")
            orchlines.append("endin\n\n")
            instrlist.append(9)

        scorelines.append('i9 %f %f "%s" %s %s %s %s %s\n' %
                          (float(starttime), float(duration), fullname,
                           str(pitch), str(amplitude), str(lp), str(pitenv),
                           str(ampenv)))

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

    if len(sound) == 1:
        if isinstance(sound[0], float) or isinstance(sound[0], int):
            playSine(pitch=float(sound[0]))
        else:  # Create a score from a prerecorded Wave file.
            playWave(sound[0])
    else:
        if len(sound) == 2:
            playSine(pitch=float(sound[0]), amplitude=float(sound[1]))
        else:
            playSine(pitch=float(sound[0]), amplitude=float(sound[1]),
                     duration=float(sound[2]))
    if tw.running_sugar:
        path = os.path.join(get_path(tw.activity, 'instance'), 'tmp.csd')
    else:
        path = os.path.join(tempfile.gettempdir(), 'tmp.csd')
    audioWrite(path)  # Create a csound file from the score.
    os.system('csound ' + path)  # Play the csound file.
