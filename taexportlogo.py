#Copyright (c) 2007-9, Playful Invention Company.

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

import tawindow
import talogo
import math

def save_logo(self, tw):
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
make \"r (:r + ((100-:r) * :s)) \r\
make \"g (:g + ((100-:g) * :s)) \r\
make \"b (:b + ((100-:b) * :s)) \r\
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
100 0 0 100 5 0 100 10 0 100 15 0 100 20 0 100 25 0 100 30 0 100 35 0 100 40 0 100 45 0 \
100 50 0 100 55 0 100 60 0 100 65 0 100 70 0 100 75 0 100 80 0 100 85 0 100 90 0 100 95 0 \
100 100 0 90 100 0 80 100 0 70 100 0 60 100 0 50 100 0 40 100 0 30 100 0 20 100 0 10 100 0 \
0 100 0 0 100 5 0 100 10 0 100 15 0 100 20 0 100 25 0 100 30 0 100 35 0 100 40 0 100 45 \
0 100 50 0 100 55 0 100 60 0 100 65 0 100 70 0 100 75 0 100 80 0 100 85 0 100 90 0 100 95 \
0 100 100 0 95 100 0 90 100 0 85 100 0 80 100 0 75 100 0 70 100 0 65 100 0 60 100 0 55 100 \
0 50 100 0 45 100 0 40 100 0 35 100 0 30 100 0 25 100 0 20 100 0 15 100 0 10 100 0 5 100 \
0 0 100 5 0 100 10 0 100 15 0 100 20 0 100 25 0 100 30 0 100 35 0 100 40 0 100 45 0 100 \
50 0 100 55 0 100 60 0 100 65 0 100 70 0 100 75 0 100 80 0 100 85 0 100 90 0 100 95 0 100 \
100 0 100 100 0 90 100 0 80 100 0 70 100 0 60 100 0 50 100 0 40 100 0 30 100 0 20 100 0 10] \r\
make \"shade 50 \r\
tasetshade :shade \r"

    bs = tawindow.blocks(tw)
    code = ""
    # these flags are used to trigger the prepending of additional procedures
    random = 0
    fillscreen = 0
    setcolor = 0
    setxy = 0
    pensize = 0
    tastack = 0
    arc = 0
    heap = 0
    write = 0
    minus = 0
    image = 0
    for b in bs:
         this_stack = ""
         data = walk_stack(self, tw, b)
         # need to catch several special cases:
         # stacks, random, setshade, et al.
         stack = 0
         namedstack = 0
         namedbox = 0
         refstack = 0
         refbox = 0
         myvar = ""
         for d in data:
             if type(d) is float:
                 if namedbox == 1:
                     myvar += str(d)
                     myvar += " "
                 elif write == 1:
                     this_stack += "labelsize "
                     this_stack += str(d)
                 else:
                     this_stack += str(d)
             else:
                 # transalate some TA terms into UCB Logo
                 if namedstack == 1:
                     this_stack += "to "
                     this_stack += d[2:].replace(" ","_")
                     this_stack += "\r"
                     stack = 1
                     namedstack = 0
                 elif namedbox == 1:
                     if d[0:2] == "#s":
                         this_stack += "make \""
                         this_stack += d[2:].replace(" ","_")
                         this_stack += " " 
                         this_stack += myvar 
                         namedbox = 0
                         myvar = ""
                     else:
                         myvar += d
                 elif refstack == 1:
                     this_stack += d[2:].replace(" ","_")
                     this_stack += " "
                     refstack = 0
                 elif refbox == 1:
                     this_stack += ":" 
                     this_stack += d[2:].replace(" ","_")
                     refbox = 0
                 elif d == "stack":
                     refstack = 1
                 elif d == "box":
                     refbox = 1
                 elif d == "storeinbox":
                     namedbox = 1
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
                     setcolor = 1
                     this_stack += "tasetshade"
                 elif d == "color":
                     this_stack += "pencolor"
                 elif d == "nop":
                     this_stack += " "
                 elif d == "nop1":
                     this_stack += "to stack1\r"
                     stack = 1
                 elif d == "nop2":
                     this_stack += "to stack2\r"
                     stack = 1
                 elif d == "nop3":
                     namedstack = 1
                 elif d == "stopstack":
                     this_stack += "stop"
                 elif d == "clean":
                     this_stack += "clearscreen"
                 elif d == "setxy":
                     setxy = 1
                     this_stack += "tasetxy"
                 elif d == "color":
                     this_stack += ":color"
                 elif d == "setcolor":
                     setcolor = 1
                     this_stack += "tasetpencolor"
                 elif d == "fillscreen":
                     fillscreen = 1
                     this_stack += "tasetbackground"
                 elif d == "random":
                     random = 1
                     this_stack += "tarandom"
                 elif d == "pensize":
                     pensize = 1
                     this_stack += "tapensize"
                 elif d == "arc":
                     arc = 1
                     this_stack += "taarc"
                 elif d == "pop":
                     heap = 1
                     this_stack += "tapop"
                 elif d == "push":
                     heap = 1
                     this_stack += "tapush"
                 elif d == "heap":
                     heap = 1
                     this_stack += "taprintheap"
                 elif d == "emptyheap":
                     heap = 1
                     this_stack += "taclearheap"
                 elif d == "kbinput":
                     this_stack += "make \"keyboard readchar"
                 elif d == "keyboard":
                     this_stack += ":keyboard"
                 elif d == 'insertimage':
                     image = 1
                 elif image == 1:
                     # skip this arg
                     image = 2
                 elif image == 2:
                     # skip this arg
                     image = 0
                 elif d[0:1] == "#s":
                     # output single characters as a string
                     if len(d[2:]) == 1:
                         this_stack += "\""
                         this_stack += d[2:]
                     # make a sentence out of everything else
                     else:
                         this_stack += "sentence "
                         this_stack += re.sub("\s"," \"",d[2:])
                         this_stack += "\r"
                 elif d == "write":
                     this_stack == "label"
                     write = 1
                 elif d == "minus":
                     this_stack == "taminus"
                     minus = 1
                 elif d == "hideblocks":
                     this_stack += " "
                 # need to handle templates somehow
                 else:
                     this_stack += d
             this_stack += " "
         if stack:
             stack = 0
         # if it is not a stack, we need to add a "to ta#" label
         elif len(data) > 0:
             this_stack = "to ta" + str(tastack) + "\r" + this_stack
             tastack += 1
         if len(data) > 0:
             code += this_stack
             code += "\rend\r"
    # need to define some procedures
    if minus: # minus only takes on arg
        code = "to taminus :y :x\routput sum :x minus :y\rend\r" + code
    if random: # to avoid negative numbers
         code = "to tarandom :min :max\routput (random (:max - :min)) + :min\rend\r" + code
    if fillscreen: # set shade than background color
         code = "to tasetbackground :color :shade\rtasetshade :shade\rsetbackground :color\rend\r" + code
    if setcolor: # load palette
         code = color_processing + code
    if pensize: # return only first argument
         code = "to tapensize\routput first round pensize\rend\r" + code
    if setxy: # swap args and round args
         code = "to tasetxy :x :y\rpenup\rsetxy :x :y\rpendown\rend\r" + code
    if arc: # need to redefine this one all together
         c = (2 * math.pi)/360
         code = "to taarc :a :r\rrepeat round :a [right 1 forward (" + str(c) + " * :r)]\rend\r" + code
    if heap: # add psuedo push and pop
         code = "to tapush :foo\routput fput :foo :taheap\rend\r" + \
             "to tapop\rif emptyp :taheap [stop]\rmake \"tmp first :taheap\r" + \
             "make \"taheap butfirst :taheap\routput :tmp\rend\r" + \
             "to taclearheap\rmake \"taheap []\rend\r" + \
             "to taprintheap \rprint :taheap\rend\r" + \
             "make \"taheap []\r" + code
    code = "window\r" + code
#    print code
    return code

def walk_stack(self, tw, spr):
    top = tawindow.find_top_block(spr)
    if spr == top:
        # only walk the stack if the block is the top block
        code = talogo.run_blocks(tw.lc, top, tawindow.blocks(tw), False)
        print ">> " 
        print code 
        print " <<"
        return code
    else:
        # not top of stack, then return empty list
        return []


