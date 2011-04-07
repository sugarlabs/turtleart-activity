#Copyright (c) 2008-11, Walter Bender

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

try:
    from sugar.datastore import datastore
except:
    pass

from TurtleArt.tapalette import logo_commands, logo_functions

def save_logo(tw):
    """ Set up the Turtle Art color palette and color processing. """

    color_processing = '\
to tasetpalette :i :r :g :b :myshade \r\
make "s ((:myshade - 50) / 50) \r\
ifelse lessp :s 0 [ \r\
make "s (1 + (:s *0.8)) \r\
make "r (:r * :s) \r\
make "g (:g * :s) \r\
make "b (:b * :s) \r\
] [ \
make "s (:s * 0.9) \r\
make "r (:r + ((99-:r) * :s)) \r\
make "g (:g + ((99-:g) * :s)) \r\
make "b (:b + ((99-:b) * :s)) \r\
] \
setpalette :i (list :r :g :b) \r\
end \r\
\
to rgb :myi :mycolors :myshade \r\
make "myr first :mycolors \r\
make "mycolors butfirst :mycolors \r\
make "myg first :mycolors \r\
make "mycolors butfirst :mycolors \r\
make "myb first :mycolors \r\
make "mycolors butfirst :mycolors \r\
tasetpalette :myi :myr :myg :myb :myshade \r\
output :mycolors \r\
end \r\
\
to processcolor :mycolors :myshade \r\
if emptyp :mycolors [stop] \r\
make "i :i + 1 \r\
processcolor (rgb :i :mycolors :myshade) :myshade \r\
end \r\
\
to tasetshade :shade \r\
make "myshade modulo :shade 200 \r\
if greaterp :myshade 99 [make "myshade (199-:myshade)] \r\
make "i 7 \r\
make "mycolors :colors \r\
processcolor :mycolors :myshade \r\
end \r\
\
to tasetpencolor :c \r\
make "color (modulo (round :c) 100) \r\
setpencolor :color + 8 \r\
end \r\
\
make "colors [ \
99  0  0 99  5  0 99 10  0 99 15  0 99 20  0 \
99 25  0 99 30  0 99 35  0 99 40  0 99 45  0 \
99 50  0 99 55  0 99 60  0 99 65  0 99 70  0 \
99 75  0 99 80  0 99 85  0 99 90  0 99 95  0 \
99 99  0 90 99  0 80 99  0 70 99  0 60 99  0 \
50 99  0 40 99  0 30 99  0 20 99  0 10 99  0 \
 0 99  0  0 99  5  0 99 10  0 99 15  0 99 20 \
 0 99 25  0 99 30  0 99 35  0 99 40  0 99 45 \
 0 99 50  0 99 55  0 99 60  0 99 65  0 99 70 \
 0 99 75  0 99 80  0 99 85  0 99 90  0 99 95 \
 0 99 99  0 95 99  0 90 99  0 85 99  0 80 99 \
 0 75 99  0 70 99  0 65 99  0 60 99  0 55 99 \
 0 50 99  0 45 99  0 40 99  0 35 99  0 30 99 \
 0 25 99  0 20 99  0 15 99  0 10 99  0  5 99 \
 0  0 99  5  0 99 10  0 99 15  0 99 20  0 99 \
25  0 99 30  0 99 35  0 99 40  0 99 45  0 99 \
50  0 99 55  0 99 60  0 99 65  0 99 70  0 99 \
75  0 99 80  0 99 85  0 99 90  0 99 95  0 99 \
99  0 99 99  0 90 99  0 80 99  0 70 99  0 60 \
99  0 50 99  0 40 99  0 30 99  0 20 99  0 10] \r\
make "shade  50 \r\
tasetshade :shade \r'

    # We need to catch several special cases: stacks, boxes, labels, etc.
    dispatch_table = {
        'label': _add_label,
        'to action': _add_named_stack,
        'action': _add_reference_to_stack,
        'storeinbox': _add_named_box,
        'box': _add_reference_to_box
        }
    constants_table = {
        'lpos': _lpos,
        'tpos': _tpos,
        'rpos': _rpos,
        'bpos': _bpos,
        }

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
            if type(blk) == type((1, 2)):
                (blk, _blk_no) = blk
            if blk in logo_commands:
                logo_command = logo_commands[blk]
            else:
                logo_command = None
            if i == 0 and not logo_command in ['to stack1\r', 'to stack2\r',
                                               'to action', 'to start\r']:
                this_stack = 'to turtleblocks_%d\r' % (stack_count)
                stack_count += 1
            if logo_command in dispatch_table:
                if i + 1 < len(psuedocode):
                    this_stack += dispatch_table[logo_command](
                        psuedocode[i + 1])
                    skip = True
                else:
                    print 'missing arg to %s' % (logo_command)
            elif logo_command in constants_table:
                this_stack += constants_table[logo_command](tw)
            elif logo_command is not None:
                this_stack += logo_command
            else:  # assume it is an argument
                if not blk in ['nop', 'nop1', 'nop2', 'nop3']:
                    if type(blk) == str and blk[0:2] == '#s':
                        this_stack += str(blk[2:]).replace(' ', '_')
                    else:
                        this_stack += str(blk).replace(' ', '_')
            this_stack += ' '

        logocode += this_stack
        logocode += '\rend\r'

    # We may need to prepend some additional procedures.
    for key in logo_functions.iterkeys():
        if key in logocode:
            logocode = logo_functions[key] + logocode

    if 'tasetshade' in logocode or 'tasetcolor' in logocode or \
       'tasetbackground' in logocode:
        logocode = color_processing + logocode

    logocode = 'window\r' + logocode
    return logocode


def _add_label(string):
        if type(string) == str and string[0:8] in ['#smedia_', '#saudio_',
                                                   '#svideo_', '#sdescr_']:
            try:
                dsobject = datastore.get(string[8:])
                string = dsobject.metadata['title']
            except:
                print 'failed to get title for %s' % (string)
                string = string[8:]
        else:
            string = str(string)
        if string[0:2] == '#s':
            string = string[2:]
            string = '"' + string
        if string.count(' ') > 0:
            return 'label sentence %s\r' % (string.replace(' ', ' "'))
        else:
            return 'label %s' % (string.replace(' ', '_'))


def _add_named_stack(action):
        if type(action) == str and action[0:2] == '#s':
            return 'to %s\r' % (str(action[2:]).replace(' ', '_'))
        else:
            return 'to %s\r' % (str(action).replace(' ', '_'))


def _add_reference_to_stack(action):
        if type(action) == str and action[0:2] == '#s':
            return '%s' % (str(action[2:]).replace(' ', '_'))
        else:
            return '%s' % (str(action).replace(' ', '_'))


def _add_named_box(box_name):
        if type(box_name) == str and box_name[0:2] == '#s':
            return 'make "%s' % (str(box_name[2:]).replace(' ', '_'))
        else:
            return 'make "%s' % (str(box_name).replace(' ', '_'))


def _add_reference_to_box(box_name):
        if type(box_name) == str and box_name[0:2] == '#s':
            return ':%s' % (str(box_name[2:]).replace(' ', '_'))
        else:
            return ':%s' % (str(box_name).replace(' ', '_'))

# TODO: Add the rest of the constants
def _lpos(tw):
        return str(-tw.canvas.width / (tw.coord_scale * 2))


def _tpos(tw):
        return str(tw.canvas.height / (tw.coord_scale * 2))


def _rpos(tw):
        return str(tw.canvas.width / (tw.coord_scale * 2))


def _bpos(tw):
        return str(-tw.canvas.height / (tw.coord_scale * 2))


def _walk_stack(tw, blk_in_stack):
    """ Convert blocks to logo psuedocode. """
    from tautils import find_top_block

    top = find_top_block(blk_in_stack)
    if blk_in_stack == top:
        psuedocode = tw.lc.run_blocks(top, tw.block_list.list, False)
        return psuedocode
    else:
        return []
