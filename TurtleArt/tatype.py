# Copyright (c) 2013 Marion Zepf
# Copyright (c) 2014 Walter Bender

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

""" type system for Primitives and their arguments """

import ast

from .tablock import Media
from .taconstants import (Color, ColorObj, Vector)


class Type(object):

    """ A type in the type hierarchy. """

    def __init__(self, constant_name, value):
        """ constant_name -- the name of the constant that points to this Type
            object
        value -- an arbitrary integer that is different from the values of
            all other Types. The order of the integers doesn't matter. """
        self.constant_name = constant_name
        self.value = value

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Type):
            return False
        return self.value == other.value

    def __str__(self):
        return str(self.constant_name)
    __repr__ = __str__

    def __hash__(self):
        return self.value


class TypeDisjunction(tuple, Type):

    """ Disjunction of two or more Types (from the type hierarchy) """

    def __init__(self, iterable):
        tuple(iterable)

    def __str__(self):
        s = ["("]
        for disj in self:
            s.append(str(disj))
            s.append(" or ")
        s.pop()
        s.append(")")
        return "".join(s)


# individual types
TYPE_OBJECT = Type('TYPE_OBJECT', 0)
TYPE_CHAR = Type('TYPE_CHAR', 1)
TYPE_COLOR = Type('TYPE_COLOR', 2)
TYPE_FLOAT = Type('TYPE_FLOAT', 3)
TYPE_INT = Type('TYPE_INT', 4)
TYPE_BOOL = Type('TYPE_BOOL', 5)
# shortcut to avoid a TypeDisjunction between TYPE_FLOAT and TYPE_INT
TYPE_NUMBER = Type('TYPE_NUMBER', 6)
TYPE_NUMERIC_STRING = Type('TYPE_NUMERIC_STRING', 7)
TYPE_BOX = Type('TYPE_BOX', 8)  # special type for the unknown content of a box
TYPE_STRING = Type('TYPE_STRING', 9)
TYPE_MEDIA = Type('TYPE_MEDIA', 10)
# An array of numbers used by the food plugin et al.
TYPE_VECTOR = Type('TYPE_VECTOR', 11)

# groups/ classes of types
TYPES_NUMERIC = (TYPE_FLOAT, TYPE_INT, TYPE_NUMBER)

BOX_AST = ast.Name(id='BOX', ctx=ast.Load)
ACTION_AST = ast.Name(id='ACTION', ctx=ast.Load)


def get_type(x):
    """ Return the most specific type in the type hierarchy that applies to x
    and a boolean indicating whether x is an AST. If the type cannot be
    determined, return TYPE_OBJECT as the type. """
    # non-AST types
    if isinstance(x, int):
        return (TYPE_INT, False)
    elif isinstance(x, float):
        return (TYPE_FLOAT, False)
    elif isinstance(x, str):
        if len(x) == 1:
            return (TYPE_CHAR, False)
        try:
            float(x)
        except ValueError:
            return (TYPE_STRING, False)
        else:
            return (TYPE_NUMERIC_STRING, False)
    elif isinstance(x, Color):
        return (TYPE_COLOR, False)
    elif isinstance(x, Media):
        return (TYPE_MEDIA, False)
    elif isinstance(x, Vector):
        return (TYPE_VECTOR, False)
    elif hasattr(x, "return_type"):
        return (x.return_type, False)

    # AST types
    elif isinstance(x, ast.Num):
        return (get_type(x.n)[0], True)
    elif isinstance(x, ast.Str):
        return (get_type(x.s)[0], True)
    elif isinstance(x, ast.Name):
        try:
            # we need to have imported CONSTANTS for this to work
            value = eval(x.id)
        except NameError:
            return (TYPE_OBJECT, True)
        else:
            return (get_type(value)[0], True)
    elif isinstance(x, ast.Subscript):
        if x.value == BOX_AST:
            return (TYPE_BOX, True)
    elif isinstance(x, ast.Call):
        if isinstance(x.func, ast.Name):
            if x.func.id == 'float':
                return (TYPE_FLOAT, True)
            elif x.func.id in ('int', 'ord'):
                return (TYPE_INT, True)
            elif x.func.id == 'chr':
                return (TYPE_CHAR, True)
            elif x.func.id in ('repr', 'str'):
                return (TYPE_STRING, True)
            elif x.func.id == 'Color':
                return (TYPE_COLOR, True)
            elif x.func.id == 'Media':
                return (TYPE_MEDIA, True)
    # unary operands never change the type of their argument
    elif isinstance(x, ast.UnaryOp):
        if issubclass(x.op, ast.Not):
            # 'not' always returns a boolean
            return (TYPE_BOOL, True)
        else:
            return get_type(x.operand)
    # boolean and comparison operators always return a boolean
    if isinstance(x, (ast.BoolOp, ast.Compare)):
        return (TYPE_BOOL, True)
    # other binary operators
    elif isinstance(x, ast.BinOp):
        type_left = get_type(x.left)[0]
        type_right = get_type(x.right)[0]
        if type_left == TYPE_STRING or type_right == TYPE_STRING:
            return (TYPE_STRING, True)
        if type_left == type_right == TYPE_INT:
            return (TYPE_INT, True)
        else:
            return (TYPE_FLOAT, True)

    return (TYPE_OBJECT, isinstance(x, ast.AST))


def is_instancemethod(method):
    # FIXME: a way to identify an instance method in python 3
    # until then, assume everything is an instance method
    return True


def is_bound_method(method):
    return type(method).__name__ == 'method' and \
        hasattr(method, '__self__') and \
        method.__self__ is not None


def is_staticmethod(method):
    # TODO how to access the type `staticmethod` directly?
    return type(method).__name__ == "staticmethod"


def identity(x):
    return x


TYPE_CONVERTERS = {
    # Type hierarchy: If there is a converter A -> B, then A is a subtype of B.
    # The converter from A to B is stored under TYPE_CONVERTERS[A][B].
    # The relation describing the type hierarchy must be transitive, i.e.
    # converting A -> C must yield the same result as converting A -> B -> C.
    # TYPE_OBJECT is the supertype of everything.
    TYPE_BOX: {
        TYPE_COLOR: ColorObj,  # FIXME: should be Color.name
        TYPE_VECTOR: Vector,
        TYPE_FLOAT: float,
        TYPE_INT: int,
        TYPE_NUMBER: float,
        TYPE_STRING: str},
    TYPE_CHAR: {
        TYPE_INT: ord,
        TYPE_STRING: identity},
    TYPE_COLOR: {
        TYPE_FLOAT: float,
        TYPE_INT: int,
        TYPE_NUMBER: int,
        TYPE_STRING: Color.get_number_string},
    TYPE_FLOAT: {
        TYPE_INT: int,
        TYPE_NUMBER: identity,
        TYPE_STRING: str},
    TYPE_INT: {
        TYPE_FLOAT: float,
        TYPE_NUMBER: identity,
        TYPE_STRING: str},
    TYPE_NUMBER: {
        TYPE_FLOAT: float,
        TYPE_INT: int,
        TYPE_STRING: str},
    TYPE_NUMERIC_STRING: {
        TYPE_FLOAT: float,
        TYPE_STRING: identity}
}


class TATypeError(BaseException):

    """ TypeError with the types from the hierarchy, not with Python types """

    def __init__(self, bad_value, bad_type=None, req_type=None, message=''):
        """ bad_value -- the mis-typed value that caused the error
        bad_type -- the type of the bad_value
        req_type -- the type that the value was expected to have
        message -- short statement about the cause of the error. It is
            not shown to the user, but may appear in debugging output. """
        self.bad_value = bad_value
        self.bad_type = bad_type
        self.req_type = req_type
        self.message = message

    def __str__(self):
        msg = []
        if self.message:
            msg.append(self.message)
            msg.append(" (")
        msg.append("bad value: ")
        msg.append(repr(self.bad_value))
        if self.bad_type is not None:
            msg.append(", bad type: ")
            msg.append(repr(self.bad_type))
        if self.req_type is not None:
            msg.append(", req type: ")
            msg.append(repr(self.req_type))
        if self.message:
            msg.append(")")
        return "".join(msg)
    __repr__ = __str__


def get_converter(old_type, new_type):
    """ If there is a converter old_type -> new_type, return it. Else return
    None. If a chain of converters is necessary, return it as a tuple or
    list (starting with the innermost, first-to-apply converter). """
    # every type can be converted to TYPE_OBJECT
    if new_type == TYPE_OBJECT:
        return identity
    # every type can be converted to itself
    if old_type == new_type:
        return identity

    # is there a converter for this pair of types?
    converters_from_old = TYPE_CONVERTERS.get(old_type)
    if converters_from_old is None:
        return None
    converter = converters_from_old.get(new_type)
    if converter is not None:
        return converter
    else:
        # form the transitive closure of all types that old_type can be
        # converted to, and look for new_type there
        backtrace = converters_from_old.copy()
        new_backtrace = backtrace.copy()
        break_all = False
        while True:
            newest_backtrace = {}
            for t in new_backtrace:
                for new_t in TYPE_CONVERTERS.get(t, {}):
                    if new_t not in backtrace:
                        newest_backtrace[new_t] = t
                        backtrace[new_t] = t
                        if new_t == new_type:
                            break_all = True
                            break
                if break_all:
                    break
            if break_all or not newest_backtrace:
                break
            new_backtrace = newest_backtrace
        # use the backtrace to find the path from old_type to new_type
        if new_type in backtrace:
            converter_chain = []
            t = new_type
            while t in backtrace and isinstance(backtrace[t], Type):
                converter_chain.insert(0, TYPE_CONVERTERS[backtrace[t]][t])
                t = backtrace[t]
            converter_chain.insert(0, TYPE_CONVERTERS[old_type][t])
            return converter_chain
    return None


def convert(x, new_type, old_type=None, converter=None):
    """ Convert x to the new type if possible.
    old_type -- the type of x. If not given, it is computed. """
    if not isinstance(new_type, Type):
        raise ValueError('%s is not a type in the type hierarchy'
                         % (repr(new_type)))
    # every type can be converted to TYPE_OBJECT
    if new_type == TYPE_OBJECT:
        return x
    if not isinstance(old_type, Type):
        (old_type, is_an_ast) = get_type(x)
    else:
        is_an_ast = isinstance(x, ast.AST)
    # every type can be converted to itself
    if old_type == new_type:
        return x

    # special case: 'box' block (or 'pop' block) as an AST
    if is_an_ast and old_type == TYPE_BOX:
        new_type_ast = ast.Name(id=new_type.constant_name)
        return get_call_ast('convert', [x, new_type_ast], return_type=new_type)

    # if the converter is not given, try to find one
    if converter is None:
        converter = get_converter(old_type, new_type)
        if converter is None:
            # no converter available
            raise TATypeError(
                bad_value=x,
                bad_type=old_type,
                req_type=new_type,
                message=(
                    "found no converter"
                    " for this type combination"))

    def _apply_converter(converter, y):
        try:
            if is_an_ast:
                if converter == identity:
                    return y
                elif is_instancemethod(converter):
                    func = ast.Attribute(value=y,
                                         attr=converter.__func__.__name__,
                                         ctx=ast.Load)
                    return get_call_ast(func)
                else:
                    func_name = converter.__name__
                    return get_call_ast(func_name, [y])
            else:
                return converter(y)
        except BaseException:
            raise TATypeError(bad_value=x, bad_type=old_type,
                              req_type=new_type, message=("error during "
                                                          "conversion"))

    if isinstance(converter, (list, tuple)):
        # apply the converter chain recursively
        result = x
        for conv in converter:
            result = _apply_converter(conv, result)
        return result
    elif converter is not None:
        return _apply_converter(converter, x)


class TypedAST(ast.AST):

    @property
    def return_type(self):
        if self._return_type is None:
            return get_type(self.func)[0]
        else:
            return self._return_type


class TypedCall(ast.Call, TypedAST):

    """ Like a Call AST, but with a return type """

    def __init__(self, func, args=None, keywords=None, starargs=None,
                 kwargs=None, return_type=None):

        if args is None:
            args = []
        if keywords is None:
            keywords = []

        ast.Call.__init__(self, func=func, args=args, keywords=keywords,
                          starargs=starargs, kwargs=kwargs)

        self._return_type = return_type


class TypedSubscript(ast.Subscript, TypedAST):

    """ Like a Subscript AST, but with a type """

    def __init__(self, value, slice_, ctx=ast.Load, return_type=None):

        ast.Subscript.__init__(self, value=value, slice=slice_, ctx=ctx)

        self._return_type = return_type


class TypedName(ast.Name, TypedAST):

    """ Like a Name AST, but with a type """

    def __init__(self, id_, ctx=ast.Load, return_type=None):

        ast.Name.__init__(self, id=id_, ctx=ctx)

        self._return_type = return_type


def get_call_ast(func_name, args=None, kwargs=None, return_type=None):
    """ Return an AST representing the call to a function with the name
    func_name, passing it the arguments args (given as a list) and the
    keyword arguments kwargs (given as a dictionary).
    func_name -- either the name of a callable as a string, or an AST
        representing a callable expression
    return_type -- if this is not None, return a TypedCall object with this
        return type instead """
    if args is None:
        args = []
    # convert keyword argument dict to a list of (key, value) pairs
    keywords = []
    if kwargs is not None:
        for (key, value) in list(kwargs.items()):
            keywords.append(ast.keyword(arg=key, value=value))
    # get or generate the AST representing the callable
    if isinstance(func_name, ast.AST):
        func_ast = func_name
    else:
        func_ast = ast.Name(id=func_name, ctx=ast.Load)
    # if no return type is given, return a simple Call AST
    if return_type is None:
        return ast.Call(func=func_ast, args=args, keywords=keywords,
                        starargs=None, kwargs=None)
    # if a return type is given, return a TypedCall AST
    else:
        return TypedCall(func=func_ast, args=args, keywords=keywords,
                         return_type=return_type)
