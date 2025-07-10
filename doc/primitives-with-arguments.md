How to define Primitive objects for blocks with arguments
=========================================================

The tutorials in this document assume that the reader is able to
add simple blocks without arguments to Turtle Art.  Please refer
to the module documentation  of  ../TurtleArt/tabasics.py  for a
tutorial on that.

Example 1: Block with one Argument
----------------------------------

In this example,   we define the `Primitive` object  for a block
that increases the pen color  by a numeric argument   that comes
from another block. In Turtle Art, the block looks like this:

     ,---.___,---------.
    /                   |
    | increment color |=
    \                   |
     `---.___,---------´

When the block  is executed,   we want it to do the same  as the
following statement:

    Turtle.set_pen_color(plus(Turtle.get_pen_color(), ...))

where `...` stands for the output of the block  connected to the
right hand  dock  of  our block.   For arguments  not  known  in
advance,   we need  to insert  a placeholder  in the form  of an
`ArgSlot` object.  An `ArgSlot` object describes some properties
of  the  argument  it  receives.   It  defines  the type  of the
argument,  it knows whether the argument needs to be called  (if
it is callable),  and it knows which callable  (if any)  it must
wrap around the argument before consuming it.  (For more on slot
wrappers,  please refer to the other examples below.)   For this
example,  we can use the default values for the second and third
property  (`True` and `None`,  respectively).   We only need  to
state the first one, the argument type, explicitly:

    prim_inc_color = Primitive(Turtle.set_pen_color,
        arg_descs=[ConstantArg(Primitive(
            Primitive.plus, return_type=TYPE_NUMBER,
                arg_descs=[ConstantArg(Primitive(
                    Turtle.get_pen_color, return_type=TYPE_NUMBER)),
                ArgSlot(TYPE_NUMBER)]))])

    self.tw.lc.def_prim('inc_color', 0, prim_inc_color)

Turtle Art  uses the same type system for argument types  as for
the return types of Primitive objects. If a value block (such as
the number block)   is attached  to  the right hand dock  of the
'increment color' block,   then Turtle Art  matches the value of
that block against the type requirement of the argument slot. If
the attached block  has a Primitive object  (such as  the 'plus'
block),   then that Primitive's return value  is matched against
the required type. If Turtle Art doesn't know how to convert the
attached value to the required type,  it shows the user an error
message during execution.


Example 2: Block with a Slot Wrapper
------------------------------------

In Turtle Art,  moving the turtle backward by x  is the same  as
moving it forward  by negative x (or -x).   In fact,  the 'back'
block uses the same method  (`Turtle.forward`)  as the 'forward'
block.   But the 'back' block  needs to switch  the sign  of its
argument before passing it to `Turtle.forward`. I.e. it needs to
execute the following statement:

    Turtle.forward(minus(...))

where `...` again  stands for the output of the block  connected
to the right hand dock of the 'back' block.   This is where slot
wrappers come in helpful.  A slot wrapper is a Primitive that is
'wrapped around'  an argument  of its 'parent' Primitive.   Slot
wrappers can only be attached to `ArgSlot` objects,  that is, to
arguments that come from other blocks. In the case of the 'back'
block, this looks as follows:

    Primitive(Turtle.forward,
        arg_descs=[ArgSlot(TYPE_NUMBER,
            wrapper=Primitive(
                Primitive.minus, return_type=TYPE_NUMBER,
                    arg_descs=[ArgSlot(TYPE_NUMBER)]))],
        call_afterwards=self.after_move))

When the 'back' block is called,  it passes the argument that it
gets from its right hand dock to the `ArgSlot` object.  That, in
turn, passes it to its wrapper, and then matches the type of the
return value of the wrapper against its type requirement. If the
types match,  the wrapper's return value  is passed back  to the
function of the main Primitive, `Turtle.forward`.

Note  that  slot wrappers  and  Primitive objects  can be nested
inside each other infinitely deeply.


Example 3: Block with a Group of Primitives
-------------------------------------------

Blocks  like the 'clean' block  need to do  several things  in a
row.  E.g., the 'clean' block needs to tell the plugins that the
screen is being cleared, it needs to stop media execution, clear
the screen, and reset all turtles.  It takes no block arguments,
so it looks like this in Turtle Art:

     ,---.___,---.
    /             \
    |   clean     |
    \             /
     `---.___,---´

To execute a series  of several Primitives,  we need to define a
'group' of Primitives. This 'group' is itself a Primitive, using
the special function `Primitive.group`.   When called,  it loops
over its arguments  and calls them successively.   The Primitive
object for the 'clean' block looks like this:

    Primitive(Primitive.group, arg_descs=[ConstantArg([
        Primitive(self.tw.clear_plugins),
        Primitive(self.tw.lc.prim_clear_helper,
                  export_me=False),
        Primitive(self.tw.canvas.clearscreen),
        Primitive(self.tw.turtles.reset_turtles)])])
