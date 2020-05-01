# Copyright (c) 2008-13, Walter Bender

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from sugar3.datastore import datastore
from TurtleArt.tapalette import (logo_commands, logo_functions)
from TurtleArt.taconstants import (TITLEXY, CONSTANTS)


def save_logo(tw):
    """ Set up the Turtle Art color palette and color processing. """

    # We need to catch several special cases: stacks, boxes, labels, etc.
    dispatch_table = {
        'label': _add_label,
        'to action': _add_named_stack,
        'action': _add_reference_to_stack,
        'storeinbox': _add_named_box,
        'box': _add_reference_to_box}
    constants_table = {
        'lpos': _lpos,
        'tpos': _tpos,
        'rpos': _rpos,
        'bpos': _bpos,
        'red': _red,
        'orange': _orange,
        'yellow': _yellow,
        'green': _green,
        'cyan': _cyan,
        'blue': _blue,
        'purple': _purple,
        'white': _white,
        'black': _black,
        'titlex': _titlex,
        'titley': _titley,
        'leftx': _leftx,
        'topy': _topy,
        'rightx': _rightx,
        'bottomy': _bottomy,
        'width': _width,
        'height': _height}

    stacks_of_blocks = tw.just_blocks()
    stack_count = 0

    logocode = ''

    """
    Walk through the code, substituting UCB Logo for Turtle Art primitives.
    """
    for stack in stacks_of_blocks:
        this_stack = ''
        psuedocode = _walk_stack(tw, stack)
        if psuedocode == []:
            continue

        skip = False
        for i in range(len(psuedocode)):
            if skip:
                skip = False
                continue
            blk = psuedocode[i]
            if isinstance(blk, tuple):
                (blk, _blk_no) = blk
            if blk in logo_commands:
                logo_command = logo_commands[blk]
            else:
                logo_command = None
            if i == 0 and logo_command not in ['to stack1\n', 'to stack2\n',
                                               'to action', 'to start\n']:
                this_stack = 'to turtleblocks_%d\n' % (stack_count)
                stack_count += 1
            if logo_command in dispatch_table:
                if i + 1 < len(psuedocode):
                    this_stack += dispatch_table[logo_command](
                        psuedocode[i + 1])
                    skip = True
                else:
                    print('missing arg to %s' % (logo_command))
            elif logo_command in constants_table:
                this_stack += str(constants_table[logo_command](tw))
            elif logo_command is not None:
                this_stack += logo_command
            else:  # assume it is an argument
                if blk not in ['nop', 'nop1', 'nop2', 'nop3']:
                    if isinstance(blk, str) and blk[0:2] == '#s':
                        this_stack += str(blk[2:]).replace(' ', '_')
                    else:
                        this_stack += str(blk).replace(' ', '_')
            this_stack += ' '

        logocode += this_stack
        logocode += '\nend\n'

    # We may need to prepend some additional procedures.
    for key in list(logo_functions.keys()):
        if key in logocode:
            logocode = logo_functions[key] + logocode

    if 'tasetshade' in logocode or 'tasetpencolor' in logocode or \
       'tasetbackground' in logocode:
        logocode = logo_functions['tacolor'] + logocode

    logocode = 'window\n' + logocode
    return logocode


def _add_label(string):
    if isinstance(string, str) and string[0:8] in ['#smedia_', '#saudio_',
                                                   '#svideo_', '#sdescr_']:
        string = string[8:]
        dsobject = datastore.get(string[8:])
        if 'title' in dsobject.metadata:
            string = dsobject.metadata['title']
    else:
        string = str(string)
    if string[0:2] == '#s':
        string = string[2:]
        string = '"' + string
    if string.count(' ') > 0:
        return 'label sentence %s\n' % (string.replace(' ', ' "'))
    else:
        return 'label %s' % (string.replace(' ', '_'))


def _add_named_stack(action):
    if isinstance(action, str) and action[0:2] == '#s':
        return 'to %s\n' % (str(action[2:]).replace(' ', '_'))
    else:
        return 'to %s\n' % (str(action).replace(' ', '_'))


def _add_reference_to_stack(action):
    if isinstance(action, str) and action[0:2] == '#s':
        return '%s' % (str(action[2:]).replace(' ', '_'))
    else:
        return '%s' % (str(action).replace(' ', '_'))


def _add_named_box(box_name):
    if isinstance(box_name, str) and box_name[0:2] == '#s':
        return 'make "%s' % (str(box_name[2:]).replace(' ', '_'))
    else:
        return 'make "%s' % (str(box_name).replace(' ', '_'))


def _add_reference_to_box(box_name):
    if isinstance(box_name, str) and box_name[0:2] == '#s':
        return ':%s' % (str(box_name[2:]).replace(' ', '_'))
    else:
        return ':%s' % (str(box_name).replace(' ', '_'))


def _lpos(tw):
    return int(-tw.canvas.width / (tw.coord_scale * 2))


def _tpos(tw):
    return int(tw.canvas.height / (tw.coord_scale * 2))


def _rpos(tw):
    return int(tw.canvas.width / (tw.coord_scale * 2))


def _bpos(tw):
    return int(-tw.canvas.height / (tw.coord_scale * 2))


def _width(tw):
    return int(tw.canvas.width / tw.coord_scale)


def _height(tw):
    int(tw.canvas.height / tw.coord_scale)


def _titlex(tw):
    return int(-(tw.canvas.width * TITLEXY[0]) / (tw.coord_scale * 2))


def _titley(tw):
    return int((tw.canvas.height * TITLEXY[1]) / (tw.coord_scale * 2))


def _leftx(tw):
    return int(-(tw.canvas.width * TITLEXY[0]) / (tw.coord_scale * 2))


def _topy(tw):
    return int((tw.canvas.height * (
        TITLEXY[1] - 0.125)) / (tw.coord_scale * 2))


def _rightx(tw):
    return 0


def _bottomy(tw):
    return 0


def _red(tw):
    return CONSTANTS['red']


def _orange(tw):
    return CONSTANTS['orange']


def _yellow(tw):
    return CONSTANTS['yellow']


def _green(tw):
    return CONSTANTS['green']


def _cyan(tw):
    return CONSTANTS['cyan']


def _blue(tw):
    return CONSTANTS['blue']


def _purple(tw):
    return CONSTANTS['purple']


def _white(tw):
    return 1


def _black(tw):
    return 0


def _walk_stack(tw, blk_in_stack):
    """ Convert blocks to logo psuedocode. """
    from .tautils import find_top_block

    top = find_top_block(blk_in_stack)
    if blk_in_stack == top:
        return tw.lc.generate_code(top, tw.just_blocks())
    else:
        return []
