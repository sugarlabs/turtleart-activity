#Copyright (c) 2008-10, Walter Bender

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

IGNORE = ["hideblocks", "showblocks", "fullscreen", "polar", "cartesian",
          "sandwichbottom", "id"]

import math
from tautils import walk_stack
try:
    from sugar.datastore import datastore
except:
    pass

def save_logo(tw):
    """ We need to set up the Turtle Art color palette and color processing. """
    color_processing = "\
to tasetpalette :i :r :g :b :myshade \r\
make \"s ((:myshade - 50) / 50) \r\
ifelse lessp :s 0 [ \r\
make \"s (1 + (:s *0.8)) \r\
make \"r (:r * :s) \r\
make \"g (:g * :s) \r\
make \"b (:b * :s) \r\
] [ \
make \"s (:s * 0.9) \r\
make \"r (:r + ((99-:r) * :s)) \r\
make \"g (:g + ((99-:g) * :s)) \r\
make \"b (:b + ((99-:b) * :s)) \r\
] \
setpalette :i (list :r :g :b) \r\
end \r\
\
to rgb :myi :mycolors :myshade \r\
make \"myr first :mycolors \r\
make \"mycolors butfirst :mycolors \r\
make \"myg first :mycolors \r\
make \"mycolors butfirst :mycolors \r\
make \"myb first :mycolors \r\
make \"mycolors butfirst :mycolors \r\
tasetpalette :myi :myr :myg :myb :myshade \r\
output :mycolors \r\
end \r\
\
to processcolor :mycolors :myshade \r\
if emptyp :mycolors [stop] \r\
make \"i :i + 1 \r\
processcolor (rgb :i :mycolors :myshade) :myshade \r\
end \r\
\
to tasetshade :shade \r\
make \"myshade modulo :shade 200 \r\
if greaterp :myshade 99 [make \"myshade (199-:myshade)] \r\
make \"i 7 \r\
make \"mycolors :colors \r\
processcolor :mycolors :myshade \r\
end \r\
\
to tasetpencolor :c \r\
make \"color (modulo (round :c) 100) \r\
setpencolor :color + 8 \r\
end \r\
\
make \"colors [ \
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
make \"shade  50 \r\
tasetshade :shade \r"

    bs = tw.just_blocks()
    code = ""
    stack_count = 0
    show = 0

    # These flags are used to trigger the prepending of additional procedures.
    random = False
    fillscreen = False
    setcolor = False
    setxy = False
    pensize = False
    setpensize = False
    arc = False
    heap = False
    write = False
    minus = False
    division = False
    image = False

    """
    Walk through the code, substituting UCB Logo for Turtle Art primitives.
    """
    for b in bs:
        this_stack = ""
        data = walk_stack(tw, b)
        # We need to catch several special cases: stacks, random, etc.
        stack = False
        namedstack = False
        namedbox = False
        refstack = False
        refbox = False
        myvar = ""
        for d in data:
            if type(d) == type((1, 2)):
                (d, b) = d
            if type(d) is float:
                if namedbox:
                    myvar += str(d)
                    myvar += " "
                elif write:
                    this_stack += "labelsize "
                    this_stack += str(d)
                    write = False
                else:
                    this_stack += str(d)
            elif show == 2:
                # Use title for Journal objects
                if d[0:8] == '#smedia_':
                    try:
                        dsobject = datastore.get(d[8:])
                        this_stack += dsobject.metadata['title']
                        dsobject.destroy()
                    except:
                        this_stack += str(d)
                else:
                    this_stack += str(d)
                show = 0
            else:
                # Translate some Turtle Art primitives into UCB Logo
                if namedstack:
                    this_stack += "to "
                    this_stack += d[2:].replace(" ","_")
                    this_stack += "\r"
                    stack = True
                    namedstack = False
                elif namedbox:
                    if d[0:2] == "#s":
                        this_stack += "make \""
                        this_stack += d[2:].replace(" ","_")
                        this_stack += " " 
                        this_stack += myvar 
                        namedbox = False
                        myvar = ""
                    else:
                        myvar += d
                elif refstack:
                    this_stack += d[2:].replace(" ","_")
                    this_stack += " "
                    refstack = False
                elif refbox:
                    this_stack += ":" 
                    this_stack += d[2:].replace(" ","_")
                    refbox = False
                elif d == "stack":
                    refstack = True
                elif d == "box":
                    refbox = True
                elif d == "storeinbox":
                    namedbox = True
                elif d == "storeinbox1":
                    this_stack += "make \"box1"
                elif d == "box1":
                    this_stack += ":box1"
                elif d == "storeinbox2":
                    this_stack += "make \"box2"
                elif d == "box2":
                    this_stack += ":box2"
                elif d == "shade":
                    this_stack += ":shade"
                elif d == "setshade":
                    setcolor = True
                    this_stack += "tasetshade"
                elif d == "color":
                    this_stack += "pencolor"
                elif d == "nop":
                    this_stack += " "
                elif d == "start":
                    this_stack += "to start\r"
                    stack = True
                elif d == "nop1":
                    this_stack += "to stack1\r"
                    stack = True
                elif d == "nop2":
                    this_stack += "to stack2\r"
                    stack = True
                elif d == "nop3":
                    namedstack = True
                elif d == "stopstack":
                    this_stack += "stop"
                elif d == "clean":
                    this_stack += "clearscreen"
                elif d == "setxy":
                    setxy = True
                    this_stack += "tasetxy"
                elif d == "color":
                    this_stack += ":color"
                elif d == "plus":
                    this_stack += "sum"
                elif d == "setcolor":
                    setcolor = True
                    this_stack += "tasetpencolor"
                elif d == "fillscreen":
                    fillscreen = True
                    setcolor = True
                    this_stack += "tasetbackground"
                elif d == "random":
                    random = True
                    this_stack += "tarandom"
                elif d == "pensize":
                    pensize = True
                    this_stack += "tapensize"
                elif d == "setpensize":
                    setpensize = True
                    this_stack += "tasetpensize"
                elif d == "arc":
                    arc = True
                    this_stack += "taarc"
                elif d == "pop":
                    heap = True
                    this_stack += "tapop"
                elif d == "push":
                    heap = True
                    this_stack += "tapush"
                elif d == "heap":
                    heap = True
                    this_stack += "taprintheap"
                elif d == "emptyheap":
                    heap = True
                    this_stack += "taclearheap"
                elif d == "kbinput":
                    this_stack += "make \"keyboard readchar"
                elif d == "keyboard":
                    this_stack += ":keyboard"
                elif d == 'insertimage':
                    image = True
                elif image:
                    # Skip this arg
                    image = 2
                elif image == 2:
                    # Skip this arg
                    image = False
                elif d[0:2] == "#s":
                    # output single characters as a string
                    if len(d[2:]):
                        this_stack += "\""
                        this_stack += d[2:]
                    # make a sentence out of everything else
                    else:
                        this_stack += "sentence "
                        this_stack += d[2:].replace("\s"," \"")
                        this_stack += "\r"
                elif d == "write":
                    this_stack += "label"
                    write = True
                elif d == 'show' or d == 'showaligned':
                    this_stack += "label"
                    show = 1
                elif d == "minus2":
                    this_stack += "taminus"
                    minus = True
                elif d == "division":
                    this_stack += "quotient"
                elif d == "lpos":
                    this_stack += str(-tw.canvas.width/(tw.coord_scale*2))
                elif d == "rpos":
                    this_stack += str(tw.canvas.width/(tw.coord_scale*2))
                elif d == "bpos":
                    this_stack += str(-tw.canvas.height/(tw.coord_scale*2))
                elif d == "tpos":
                    this_stack += str(tw.canvas.height/(tw.coord_scale*2))
                elif d in IGNORE:
                    this_stack += " "
                elif show == 1 and d[0:2] == "#s":
                    this_stack += d[2:]
                # We don't handle depreciated 'template' blocks
                else:
                    this_stack += d
            this_stack += " "
        if stack:
            stack = False
        # if it is not a stack, we need to add a "to ta#" label
        elif len(data) > 0:
            this_stack = "to ta" + str(stack_count) + "\r" + this_stack
            stack_count += 1
        if len(data) > 0:
            code += this_stack
            code += "\rend\r"

    # We need to define some additional procedures.
    if minus: # Logo minus only takes one argument.
        code = "to taminus :y :x\routput sum :x minus :y\rend\r" + code
    if random: # to avoid negative numbers
        code = "to tarandom :min :max\r" + \
               "output (random (:max - :min)) + :min\rend\r" + code
    if fillscreen: # Set shade than background color
        code = "to tasetbackground :color :shade\r" + \
               "tasetshade :shade\rsetbackground :color\rend\r" + code
    if setcolor: # Load the Turtle Art color palette.
        code = color_processing + code
    if setpensize: # Set int of pensize
        code = "to tasetpensize :a\rsetpensize round :a\rend\r" + code
    if pensize: # Return only the first argument.
        code = "to tapensize\routput first round pensize\rend\r" + code
    if setxy: # Swap and round arguments
        code = "to tasetxy :x :y\rpenup\rsetxy :x :y\rpendown\rend\r" + code
    if arc: # Turtle Art 'arc' needs to be redefined.
        c = (2 * math.pi)/360
        code = "to taarc :a :r\rrepeat round :a [right 1 forward (" + \
               str(c) + " * :r)]\rend\r" + code
    if heap: # Add psuedo 'push' and 'pop'
        code = "to tapush :foo\rmake \"taheap fput :foo :taheap\rend\r" + \
            "to tapop\rif emptyp :taheap [stop]\rmake \"tmp first :taheap\r" + \
            "make \"taheap butfirst :taheap\routput :tmp\rend\r" + \
            "to taclearheap\rmake \"taheap []\rend\r" + \
            "to taprintheap \rprint :taheap\rend\r" + \
            "make \"taheap []\r" + code
    code = "window\r" + code
    return code


