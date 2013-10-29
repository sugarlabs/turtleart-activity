The TA Type System
==================

Why do we Need a Type System?
-----------------------------

The purpose of the type system is to have a consistent and
standardized way of type-checking and type-converting the
arguments of blocks. For example, the 'minus' block takes two
arguments of type TYPE_NUMBER. But that doesn't mean that only
number blocks can be attached to its argument docks. In fact,
colors, single characters, and numeric strings (like `"-5.2"`)
can easily be converted to numbers. The type system takes care
of this. When e.g., a color is attached to the argument dock of
the 'minus' block, the type system tries to find a converter
from the type TYPE_COLOR (the type of the color block) to the
type TYPE_NUMBER. If it finds one (and in this case it does),
then the converter is applied to the argument. A converter is
simply a callable (usually a function) and applying it simply
means calling it and passing it the value of the argument block
as a parameter. The converter returns the number that cor-
responds to the color, and the number is passed on to the
'minus' block. This way, the 'minus' block does not have to know
about colors, characters, or numeric strings. Likewise, the
color block also does not have to care about how its value can
be converted to a number.

Why do some Blocks Need Return Types?
-------------------------------------

The argument to the 'minus' block (to continue our example) need
not be a simple value block; it can also be the result of a
complex mathematical operation, i.e. the return type of another
block such as 'multiply'. The 'minus' block still demands a
value of type TYPE_NUMBER, so the 'multiply' block must provide
information about its return type. This is why blocks that can
be used as arguments to other blocks must specify a return type.

What if I want to Specify Two Types at the Same Time?
-----------------------------------------------------

You can use the function `or_` (defined in `taprimitive.py`) to
create disjunctions of `Primitive`s, argument lists, `ArgSlot`s,
or types. Simply pass the disjuncts to it as its arguments.
E.g., to create a disjunction between the types TYPE_NUMBER and
TYPE_STRING, call

    or_(TYPE_NUMBER, TYPE_STRING)

The return value of the `or_` function will in this case be a
`TypeDisjunction` object that holds the two types. It means the
same as 'TYPE_NUMBER or TYPE_STRING' in English. The `or_`
function knows automatically from the type of its arguments
which type of object it must return.

What if it is Impossible to Predict the Return Type of a Block?
---------------------------------------------------------------

In the case of the 'box' block, for example, it is impossible to
predict what type it will return at runtime because one cannot
foresee what will be inside the box at runtime. (E.g., the box
contents could depend on input from the keyboard or camera.)
This is where the special type TYPE_BOX comes in handy. It
allows you to postpone the search for a type converter until the
type of the box contents is known. As soon as this is the case,
the type system will automatically apply the appropriate type
converter.

How to Add a New Type
---------------------

To add a new type to the type system, you need to instantiate a
new `Type` object and store it in a constant whose name starts
with `TYPE_`. You would do this in `tatype.py`:

    TYPE_MYTYPE = Type('TYPE_MYTYPE', 99)

The number argument to the `Type` constructor can have an
arbitrary value, as long as it is different from the value of
every other `Type` object.

You also need to tell the type system how to recognize runtime
objects that belong to your type. Add one or several new `elif`
clauses to the `get_type` function. E.g., if you are defining a
new type for dictionaries, you would add the clauses

    elif isinstance(x, dict):
        return (TYPE_DICT, False)
    elif isinstance(x, ast.Dict):
        return (TYPE_DICT, True)

The second item of the tuple that `get_type` returns indicates
whether `x` is an AST (Abstract Syntax Tree) or not. Only
instances of subclasses of `ast.AST` are ASTs.

Optionally, you can add converters for the new type. You can do
so by extending the dictionary `TYPE_CONVERTERS` in `tatype.py`.
The format is quite simple: To add a converter from your type to
e.g., TYPE_FLOAT, add the entry:

    TYPE_CONVERTERS = {
       # ...
       TYPE_MYTYPE: {
           # ...
           TYPE_FLOAT: float
           # ...
       }
       # ...
    }

Note that it is not obligatory to use the function `float` as
the converter to the type TYPE_FLOAT. In fact, you can use any
function or method. Please make sure that the converter accepts
arguments of the source type (here, TYPE_MYTYPE) and returns a
value of the target type (here, TYPE_FLOAT). The converter must
not throw any errors.
