# A Turtle Block based on the Speak Activity interface to AIML
# Copyright 2012 Walter Bender, Sugar Labs
#
# Copyright (C) 2008 Sebastian Silva Fundacion FuenteLibre
# sebastian@fuentelibre.org
#
# Style and structure taken from Speak.activity Copyright (C) Joshua Minor
#
#     HablarConSara.activity is free software: you can redistribute it
#     and/or modify it under the terms of the GNU General Public
#     License as published by the Free Software Foundation, either
#     version 3 of the License, or (at your option) any later version.
#
#     HablarConSara.activity is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public
#     License along with HablarConSara.activity.  If not, see
#     <http://www.gnu.org/licenses/>.


def myblock(tw, args):
    ''' Dialog with AIML library: Usage: Load this code into a Python
        Block. Pass text as an argument and the robot's response will
        be pushed to the stack. Use a Pop Block to pop the response
        off the the stack.'''

    # The AIML library is bundled with the Speak activity
    SPEAKPATHS = ['/home/olpc/Activities/Speak.activity',
                  '/home/liveuser/Activities/Speak.activity',
                  '/usr/share/sugar/activities/Speak.activity']
    import os
    from gettext import gettext as _
    speakpath = None
    for sp in SPEAKPATHS:
        if os.path.exists(sp):
            speakpath = sp
            break
    if speakpath is None:
        tw.showlabel(
            'status', _('Please install the Speak Activity and try again.'))
        return
    import sys
    sys.path.append(speakpath)

    import aiml
    import voice

    BOTS = {
        _('Spanish'): {'name': 'Sara',
                       'brain': os.path.join(speakpath, 'bot', 'sara.brn'),
                       'predicates': {'nombre_bot': 'Sara',
                                      'botmaster': 'La comunidad Azucar'}},
        _('English'): {'name': 'Alice',
                       'brain': os.path.join(speakpath, 'bot', 'alice.brn'),
                       'predicates': {'name': 'Alice',
                                      'master': 'The Sugar Community'}}}

    def get_mem_info(tag):
        meminfo = open('/proc/meminfo').readlines()
        mem_list = int([i for i in meminfo if i.startswith(tag)][0].split()[1])
        meminfo.close()
        return mem_list

    # load Standard AIML set for restricted systems
    if get_mem_info('MemTotal:') < 524288:
        mem_free = get_mem_info('MemFree:') + get_mem_info('Cached:')
        if mem_free < 102400:
            BOTS[_('English')]['brain'] = None
        else:
            BOTS[_('English')]['brain'] = os.path.join(speakpath, 'bot',
                                                       'alisochka.brn')

    def get_default_voice():
        default_voice = voice.defaultVoice()
        if default_voice.friendlyname not in BOTS:
            return voice.allVoices()[_('English')]
        else:
            return default_voice

    def brain_respond(kernel, text):
        if kernel is not None:
            text = kernel.respond(text)
        if kernel is None or not text:
            text = ''
            tw.showlabel(
                'status',
                _("Sorry, I can't understand what you are asking about."))
        return text

    def brain_load(kernel, voice):
        brain = BOTS[voice.friendlyname]
        kernel = aiml.Kernel()

        if brain['brain'] is None:
            tw.showlabel(
                'status', _('Sorry, there is no free memory to load my brain. \
Close other activities and try once more.'))
            return kernel

        kernel.loadBrain(brain['brain'])
        for name, value in list(brain['predicates'].items()):
            kernel.setBotPredicate(name, value)

        return kernel

    text = args[0]
    if not hasattr(tw, 'aiml_kernel'):
        tw.aiml_kernel = brain_load(tw, get_default_voice())
    response_text = brain_respond(tw.aiml_kernel, text)
    tw.lc.heap.append(response_text)
    return
