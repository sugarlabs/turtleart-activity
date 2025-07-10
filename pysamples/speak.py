# Copyright (c) 2009-11, Walter Bender, Tony Forster

# This procedure is invoked when the user-definable block on the
# "extras" palette is selected.

# Usage: Import this code into a Python (user-definable) block and
# pass a string to be read by the voice synthesizer. If a second
# argument is passed, by expanding the Python block, it is used to specify
# the pitch level of the speaker. Valid range is 0 to 99.


def myblock(tw, arg):
    ''' Text to speech '''

    TABLE = {'af': 'afrikaans', 'cy': 'welsh-test', 'el': 'greek',
             'es': 'spanish', 'hi': 'hindi-test', 'hy': 'armenian',
             'ku': 'kurdish', 'mk': 'macedonian-test', 'pt': 'brazil',
             'sk': 'slovak', 'sw': 'swahili', 'bs': 'bosnian', 'da': 'danish',
             'en': 'english', 'fi': 'finnish', 'hr': 'croatian',
             'id': 'indonesian-test', 'la': 'latin', 'nl': 'dutch-test',
             'sq': 'albanian', 'ta': 'tamil', 'vi': 'vietnam-test',
             'ca': 'catalan', 'de': 'german', 'eo': 'esperanto',
             'fr': 'french', 'hu': 'hungarian', 'is': 'icelandic-test',
             'lv': 'latvian', 'no': 'norwegian', 'ro': 'romanian',
             'sr': 'serbian', 'zh': 'Mandarin', 'cs': 'czech', 'it': 'italian',
             'pl': 'polish', 'ru': 'russian_test', 'sv': 'swedish',
             'tr': 'turkish'}
    import os

    pitch = None
    if len(arg) > 1:
        text = arg[0]
        if len(arg) > 1:
            pitch = int(arg[1])
            if pitch > 99:
                pitch = 99
            elif pitch < 0:
                pitch = 0
    else:
        text = arg[0]

    # Turtle Art numbers are passed as float,
    # but they may be integer values.
    if isinstance(text, float) and int(text) == text:
        text = int(text)

    lang = os.environ['LANG'][0:2]
    if lang in TABLE:
        language_option = '-v ' + TABLE[lang]
    else:
        language_option = ''
    if pitch is None:
        os.system('espeak %s "%s" --stdout | aplay' % (language_option,
                                                       text))
    else:
        os.system('espeak %s "%s" -p "%s" --stdout | aplay' % (
            language_option, text, pitch))
