#Copyright (c) 2013 Marion Zepf

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

import ast
from gettext import gettext as _

#from ast_pprint import * # only used for debugging, safe to comment out

from tacanvas import TurtleGraphics
from taconstants import (Color, CONSTANTS)
from talogo import LogoCode
from taturtle import (Turtle, Turtles)
from tautils import debug_output
from tawindow import (global_objects, TurtleArtWindow)


class PyExportError(BaseException):
    """ Error that is raised when something goes wrong while converting the
    blocks to python code """

    def __init__(self, message, block=None):
        """ message -- the error message
        block -- the block where the error occurred """
        self.message = message
        self.block = block

    def __str__(self):
        if self.block is not None:
            return _("error in highlighted block") + ": " + str(self.message)
        else:
            return _("error") + ": " + str(self.message)


class Primitive(object):
    """ Something that can be called when the block code is executed in TA, 
    but that can also be transformed into a Python AST.
    """

    STANDARD_OPERATORS = {'plus': (ast.UAdd, ast.Add),
                          'minus': (ast.USub, ast.Sub),
                          'multiply': ast.Mult,
                          'divide': ast.Div,
                          'modulo': ast.Mod,
                          'power': ast.Pow,
                          'integer_division': ast.FloorDiv,
                          'bitwise_and': ast.BitAnd,
                          'bitwise_or': ast.BitOr,
                          'and_': ast.And,
                          'or_': ast.Or,
                          'not_': ast.Not,
                          'equals': ast.Eq,
                          'less': ast.Lt,
                          'greater': ast.Gt}

    def __init__(self, func, constant_args=None, slot_wrappers=None,
                 call_afterwards=None, call_me=True, export_me=True):
        """ constant_args -- A dictionary containing constant arguments to be
            passed to the function. It uses the same key scheme as
            slot_wrappers, except that argument ranges are not supported.
            The constant args and kwargs are added to the runtime args and
            kwargs before the slot wrappers are called.
        slot_wrappers -- A dictionary mapping from the index of an
            argument in the args list to another Primitive that should be
            wrapped around the actual argument value (e.g., to convert a
            positive number to a negative one). For keyword arguments, the
            key in slot_wrappers should be the same as the kwargs key. To pass
            multiple arguments to the slot wrapper, use a tuple of the first
            and last argument number (the latter increased by 1) as a key.
            Negative argument indices are not supported.
        call_afterwards -- Code to call after this Primitive has been called
            (e.g., for updating labels in LogoCode) (not used for creating
            AST)
        call_me -- True if this Primitive should be called (default), False
            if it should be passed on as a Primitive object
        export_me -- True iff this Primitive should be exported to Python
            code (the default case) """
        self.func = func

        if constant_args is None:
            self.constant_args = {}
        else:
            self.constant_args = constant_args

        if slot_wrappers is None:
            self.slot_wrappers = {}
        else:
            # check for duplicate argument indices
            msg = ("argument at index %d is associated with multiple slot "
                   "wrappers")
            nums = set()
            tuples = []
            for k in slot_wrappers.keys():
                if isinstance(k, int):
                    nums.add(k)
                elif isinstance(k, tuple):
                    tuples.append(k)
            tuples.sort()
            prev_tuple = (0, 0)
            for tuple_ in tuples:
                if prev_tuple[1] > tuple_[0]:
                    raise KeyError(msg % (tuple_[0]))
                for i in range(*tuple_):
                    if i in nums:
                        raise KeyError(msg % (i))
                prev_tuple = tuple_
            self.slot_wrappers = slot_wrappers

        self.call_afterwards = call_afterwards
        self.call_me = call_me
        self.export_me = export_me

    def __repr__(self):
        return "Primitive(" + repr(self.func) + ")"

    def _apply_wrappers(self, runtime_args, runtime_kwargs, 
                        convert_to_ast=False):
        """ Apply the slot wrappers """
        # make a map from the start indices of all ranges to their ends
        range_ends = {}
        for range_tuple in sorted(self.slot_wrappers.keys()):
            if isinstance(range_tuple, tuple):
                (start, end) = range_tuple
                range_ends[start] = end

        new_args = []
        i = 0
        while i < len(runtime_args):
            arg = runtime_args[i]
            wrapper = self.slot_wrappers.get(i)
            if wrapper is None:
                (start, end) = (i, range_ends.get(i))
                if end is None:
                    # no slot wrapper found
                    # convert to AST, but don't call
                    if convert_to_ast and isinstance(arg, Primitive):
                        new_args.append(arg.get_ast())
                    else:
                        new_args.append(arg)
                    i += 1
                else:
                    # range -> slot wrapper around a range of arguments
                    wrapper = self.slot_wrappers.get((start, end))
                    args_for_wrapper = runtime_args[start:end]
                    if not convert_to_ast and call_me(wrapper):
                        wrapper_output = wrapper(*args_for_wrapper)
                    elif convert_to_ast and export_me(wrapper):
                        wrapper_output = value_to_ast(wrapper,
                                                      *args_for_wrapper)
                    else:
                        # apply all contained wrappers, but skip this one
                        (all_args, unused) = wrapper._add_constant_args(
                            args_for_wrapper, runtime_kwargs={},
                            convert_to_ast=convert_to_ast)
                        (my_new_args, unused) = wrapper._apply_wrappers(
                            all_args, runtime_kwargs={},
                            convert_to_ast=convert_to_ast)
                        wrapper_output = my_new_args
                    new_args.append(wrapper_output)
                    i += end - start
            else:
                # number -> slot wrapper around one argument
                if not convert_to_ast and call_me(wrapper):
                    new_arg = wrapper(arg)
                elif convert_to_ast and export_me(wrapper):
                    new_arg = value_to_ast(wrapper, arg)
                else:
                    # apply all contained wrappers, but skip this one
                    (all_args, unused) = wrapper._add_constant_args([arg],
                        runtime_kwargs={}, convert_to_ast=convert_to_ast)
                    (my_new_args, unused) = wrapper._apply_wrappers(all_args,
                        runtime_kwargs={}, convert_to_ast=convert_to_ast)
                    new_arg = my_new_args[0]
                new_args.append(new_arg)
                i += 1

        new_kwargs = {}
        for (key, value) in runtime_kwargs.iteritems():
            wrapper = self.slot_wrappers.get(key)
            if wrapper is not None:
                if not convert_to_ast and call_me(wrapper):
                    new_value = wrapper(value)
                elif convert_to_ast and export_me(wrapper):
                    new_value = value_to_ast(wrapper, value)
                else:
                    # apply all contained wrappers, but skip this one
                    (unused, all_kwargs) = wrapper._add_constant_args([],
                        runtime_kwargs={key: value},
                        convert_to_ast=convert_to_ast)
                    (unused, my_new_kwargs) = wrapper._apply_wrappers([],
                        runtime_kwargs={key: all_kwargs[key]},
                        convert_to_ast=convert_to_ast)
                    new_value = my_new_kwargs[key]
                new_kwargs[key] = new_value
            else:
                new_kwargs[key] = value

        return (new_args, new_kwargs)

    def _add_constant_args(self, runtime_args, runtime_kwargs,
            convert_to_ast=False):
        """ Add the constant args and kwargs to the given runtime args and
        kwargs. Return a list containing all args and a dictionary with all
        kwargs.
        convert_to_ast -- convert all constant arguments to ASTs? """
        all_args = []
        all_kwargs = runtime_kwargs.copy()

        # args
        i = 0
        def _insert_c_args(i):
            while i in self.constant_args:
                c_arg = self.constant_args[i]
                if not convert_to_ast and call_me(c_arg):
                    all_args.append(c_arg())
                elif convert_to_ast:
                    if export_me(c_arg):
                        all_args.append(value_to_ast(c_arg))
                else:
                    all_args.append(c_arg)
                i += 1
            return i
        for arg in runtime_args:
            i = _insert_c_args(i)
            all_args.append(arg)
            i += 1
        i = _insert_c_args(i)

        # kwargs
        for (key, value) in self.constant_args.iteritems():
            if isinstance(key, basestring):
                if not convert_to_ast and call_me(value):
                    all_kwargs[key] = value()
                elif convert_to_ast:
                    if export_me(value):
                        all_kwargs[key] = value_to_ast(value)
                else:
                    all_kwargs[key] = value

        return (all_args, all_kwargs)

    def __call__(self, *runtime_args, **runtime_kwargs):
        """ Execute the function, passing it the arguments received at 
        runtime. Also call the function in self.call_afterwards and pass it
        all runtime_args and runtime_kwargs.
        If the very first argument is a LogoCode instance, it may be
        replaced with the active turtle, the canvas, or nothing (depending 
        on what this primitive wants as its first arg). This argument is 
        also exempt from the slot wrappers. """

        # remove the first argument if it is a LogoCode instance
        if runtime_args and isinstance(runtime_args[0], LogoCode):
            runtime_args = runtime_args[1:]

        runtime_args_copy = runtime_args[:]
        runtime_args = []
        for arg in runtime_args_copy:
            if isinstance(arg, tuple) and arg and callable(arg[0]):
                runtime_args.append(arg[0](*arg[1:]))
            else:
                runtime_args.append(arg)

        # what does this primitive want as its first argument?
        if self.wants_turtle():
            first_arg = global_objects["turtles"].get_active_turtle()
        elif self.wants_turtles():
            first_arg = global_objects["turtles"]
        elif self.wants_canvas():
            first_arg = global_objects["canvas"]
        elif self.wants_logocode():
            first_arg = global_objects["logo"]
        elif self.wants_tawindow():
            first_arg = global_objects["window"]
        else:
            first_arg = None

        # constant arguments
        (all_args, all_kwargs) = self._add_constant_args(runtime_args,
                                                         runtime_kwargs)
        
        # slot wrappers
        (new_args, new_kwargs) = self._apply_wrappers(all_args, all_kwargs)

        # execute the actual function
        if first_arg is None or is_bound_instancemethod(self.func):
            return_value = self.func(*new_args, **new_kwargs)
        else:
            return_value = self.func(first_arg, *new_args, **new_kwargs)
        
        if self.call_afterwards is not None:
            self.call_afterwards(*new_args, **new_kwargs)
        
        return return_value

    def get_ast(self, *arg_asts, **kwarg_asts):
        """ Transform this object into a Python AST. When serialized and 
        executed, the AST will do exactly the same as calling this object. """

        # constant arguments
        (all_arg_asts, all_kwarg_asts) = self._add_constant_args(arg_asts,
                                             kwarg_asts, convert_to_ast=True)

        # slot wrappers
        (new_arg_asts, new_kwarg_asts) = self._apply_wrappers(all_arg_asts,
                                             all_kwarg_asts,
                                             convert_to_ast=True)

        # SPECIAL HANDLING #

        # loops
        if self == LogoCode.prim_loop:
            controller = self._get_loop_controller()
            if controller == Primitive.controller_repeat:
                # 'repeat' loop
                num_repetitions = new_arg_asts[0]
                if num_repetitions.func.id == 'controller_repeat':
                    num_repetitions = num_repetitions.args[0]
                repeat_iter = get_call_ast("range", [num_repetitions])
                # TODO use new variable name in nested loops
                loop_ast = ast.For(target=ast.Name(id="i", ctx=ast.Store),
                                   iter=repeat_iter,
                                   body=new_arg_asts[1],
                                   orelse=[])
                return loop_ast
            else:
                if controller == Primitive.controller_forever:
                    condition_ast = ast.Name(id="True", ctx=ast.Load)
                elif controller == Primitive.controller_while:
                    condition_ast = new_arg_asts[0].args[0]
                elif controller == Primitive.controller_until:
                    condition_ast = ast.UnaryOp(op=ast.Not,
                                              operand=new_arg_asts[0].args[0])
                else:
                    raise ValueError("unknown loop controller: " +
                                     repr(controller))
                loop_ast = ast.While(test=condition_ast,
                                     body=new_arg_asts[1],
                                     orelse=[])
                return loop_ast

        # conditionals
        elif self in (LogoCode.prim_if, LogoCode.prim_ifelse):
            test = new_arg_asts[0]
            body = new_arg_asts[1]
            if len(new_arg_asts) > 2:
                orelse = new_arg_asts[2]
            else:
                orelse = []
            if_ast = ast.If(test=test, body=body, orelse=orelse)
            return if_ast

        # boxes
        elif self == LogoCode.prim_set_box:
            id_str = 'BOX[%s]' % (repr(ast_to_value(new_arg_asts[0])))
            target_ast = ast.Name(id=id_str, ctx=ast.Store)
            value_ast = new_arg_asts[1]
            assign_ast = ast.Assign(targets=[target_ast], value=value_ast)
            return assign_ast
        elif self == LogoCode.prim_get_box:
            id_str = 'BOX[%s]' % (repr(ast_to_value(new_arg_asts[0])))
            return ast.Name(id=id_str, ctx=ast.Load)

        # action stacks
        elif self == LogoCode.prim_define_stack:
            return
        elif self == LogoCode.prim_invoke_stack:
            stack_name = ast_to_value(new_arg_asts[0])
            stack_func_name = 'ACTION[%s]' % (repr(stack_name))
            stack_func = ast.Name(id=stack_func_name, ctx=ast.Load)
            return get_call_ast('logo.icall', [stack_func])

        # standard operators
        elif self.func.__name__ in Primitive.STANDARD_OPERATORS:
            op = Primitive.STANDARD_OPERATORS[self.func.__name__]
            # BEGIN hack for 'plus': unpack tuples
            if (self == Primitive.plus and len(new_arg_asts) == 1 and
                    isinstance(new_arg_asts[0], (list, tuple)) and
                    len(new_arg_asts[0]) == 2):
                new_arg_asts = new_arg_asts[0]
            # END hack for 'plus'
            if len(new_arg_asts) == 1:
                if isinstance(op, tuple):
                    op = op[0]
                return ast.UnaryOp(op=op, operand=new_arg_asts[0])
            elif len(new_arg_asts) == 2:
                if isinstance(op, tuple):
                    op = op[1]
                (left, right) = new_arg_asts
                if issubclass(op, ast.boolop):
                    return ast.BoolOp(op=op, values=[left, right])
                elif issubclass(op, ast.cmpop):
                    return ast.Compare(left=left, ops=[op],
                                       comparators=[right])
                else:
                    return ast.BinOp(op=op, left=left, right=right)
            else:
                raise ValueError(("operator Primitive.%s got unexpected"
                                  " number of arguments (%d)")
                                 % (str(self.func.__func__.__name__),
                                    len(new_arg_asts)))

        # type conversion
        elif self in (Primitive.convert_for_cmp, Primitive.convert_to_number,
                      Primitive.convert_for_plus):
            return self.func(*new_arg_asts, **new_kwarg_asts)

        # identity
        elif self == Primitive.identity:
            if len(new_arg_asts) == 1:
                return new_arg_asts[0]
            else:
                raise ValueError("Primitive.identity got unexpected number "
                                 "of arguments (%d)" % (len(new_arg_asts)))

        # tuples
        elif self == Primitive.make_tuple:
            if not new_kwarg_asts:
                return ast.Tuple(elts=new_arg_asts, ctx=ast.Load)
            else:
                raise ValueError("tuple constructor (Primitive.make_tuple) "
                                 "got unexpected arguments: " +
                                 repr(new_kwarg_asts))

        # group of Primitives
        elif self == Primitive.group:
            return new_arg_asts[0].elts

        # NORMAL FUNCTION CALL #

        else:
            func_name = ""
            if self.wants_turtle():
                func_name = "turtle."
            elif self.wants_turtles():
                func_name = "turtles."
            elif self.wants_canvas():
                func_name = "canvas."
            elif self.wants_logocode():
                func_name = "logo."
            elif self.wants_tawindow():
                func_name = "tw."
            # get the name of the function directly from the function itself
            func_name += self.func.__name__

            return get_call_ast(func_name, new_arg_asts, new_kwarg_asts)

    def __eq__(self, other):
        """ Two Primitives are equal iff their all their properties are equal.
        Consider bound and unbound methods equal. """
        # other is a Primitive
        if isinstance(other, Primitive):
            return (self == other.func and
                    self.constant_args == other.constant_args and
                    self.slot_wrappers == other.slot_wrappers and
                    self.call_afterwards == other.call_afterwards and
                    self.export_me == other.export_me)

        # other is a callable
        elif callable(other):
            if is_instancemethod(self.func) != is_instancemethod(other):
                return False
            elif is_instancemethod(self.func): # and is_instancemethod(other):
                return (self.func.im_class == other.im_class and
                        self.func.im_func == other.im_func)
            else:
                return self.func == other

        elif is_staticmethod(other):
            return self.func == other.__func__

        # other is neither a Primitive nor a callable
        else:
            return False

    def wants_turtle(self):
        """ Does this Primitive want to get the active turtle as its first 
        argument? """
        return self._wants(Turtle)

    def wants_turtles(self):
        """ Does this Primitive want to get the Turtles instance as its
        first argument? """
        return self._wants(Turtles)

    def wants_canvas(self):
        """ Does this Primitive want to get the canvas as its first
        argument? """
        return self._wants(TurtleGraphics)

    def wants_logocode(self):
        """ Does this Primitive want to get the LogoCode instance as its
        first argument? """
        return self._wants(LogoCode)

    def wants_tawindow(self):
        """ Does this Primitive want to get the TurtleArtWindow instance
        as its first argument? """
        return self._wants(TurtleArtWindow)

    def wants_nothing(self):
        """ Does this Primitive want nothing as its first argument? I.e. does 
        it want to be passed all the arguments of the block and nothing 
        else? """
        return not is_instancemethod(self.func)

    def _wants(self, theClass):
        if is_instancemethod(self.func):
            return self.func.im_class == theClass
        else:
            return False

    # treat the following methods in a special way when converting the
    # Primitive to an AST

    @staticmethod
    def make_tuple(*values):
        """ This method corresponds to a Python tuple consisting of the given 
        values. """
        return tuple(values)

    @staticmethod
    def controller_repeat(num):
        """ Loop controller for the 'repeat' block """
        for i in range(num):
            yield True
        yield False

    @staticmethod
    def controller_forever():
        """ Loop controller for the 'forever' block """
        while True:
            yield True

    @staticmethod
    def controller_while(boolean):
        """ Loop controller for the 'while' block """
        while boolean:
            yield True
        yield False

    @staticmethod
    def controller_until(boolean):
        """ Loop controller for the 'until' block """
        while not boolean:
            yield True
        yield False

    LOOP_CONTROLLERS = [controller_repeat, controller_forever,
                        controller_while, controller_until]

    def _get_loop_controller(self):
        """ Return the controller for this loop Primitive. Raise a
        ValueError if no controller was found. """
        def _is_loop_controller(candidate):
            return (callable(candidate)
                    and candidate in Primitive.LOOP_CONTROLLERS)

        # look at the first constant argument
        first_const = self.constant_args.get(0, None)
        if _is_loop_controller(first_const):
            return first_const

        # look at the first slot wrapper
        first_wrapper = self.slot_wrappers.get(0, None)
        if _is_loop_controller(first_wrapper):
            return first_wrapper

        # no controller found
        raise ValueError("found no loop controller for " + repr(self))

    @staticmethod
    def do_nothing():
        pass

    @staticmethod
    def identity(arg):
        """ Return the argument unchanged """
        return arg

    @staticmethod
    def group(prim_list):
        """ Group together multiple Primitives into one. Treat each Primitive
        as a separate line of code. """
        return_val = None
        for prim in prim_list:
            return_val = prim()
        return return_val

    @staticmethod
    def convert_for_plus(value1, value2):
        """ If at least one value is a string, convert both to a string.
        Otherwise, convert both to a number. (Colors are converted to an
        integer before they are converted to a string.) """
        convert_to_ast = False
        (value1_ast, value2_ast) = (None, None)

        if isinstance(value1, ast.AST):
            convert_to_ast = True
            value1_ast = value1
            value1 = ast_to_value(value1_ast)
        if isinstance(value2, ast.AST):
            value2_ast = value2
            value2 = ast_to_value(value2_ast)

        def _to_string(val, val_ast):
            """ Return strings as they are, convert Colors to an integer and
            then to a string, and convert everything else directly to a
            string. """
            val_conv = val
            val_conv_ast = val_ast
            if not isinstance(val, basestring):
                if isinstance(val, Color):
                    conv_prim = Primitive(str, slot_wrappers={
                                    0: Primitive(int)})
                else:
                    conv_prim = Primitive(str)
                if not convert_to_ast:
                    val_conv = conv_prim(val)
                else:
                    val_conv_ast = conv_prim.get_ast(val_ast)
            return (val_conv, val_conv_ast)

        def _to_number(val, val_ast):
            """ Return numbers as they are, and convert everything else to an
            integer. """
            val_conv = val
            val_conv_ast = val_ast
            if not isinstance(val, (float, int, long)):
                conv_prim = Primitive(int)
                if not convert_to_ast:
                    val_conv = conv_prim(val)
                else:
                    val_conv_ast = conv_prim.get_ast(val_ast)
            return (val_conv, val_conv_ast)

        if isinstance(value1, basestring) or isinstance(value2, basestring):
            # convert both to strings
            (value1_conv, value1_conv_ast) = _to_string(value1, value1_ast)
            (value2_conv, value2_conv_ast) = _to_string(value2, value2_ast)
        else:
            # convert both to numbers
            (value1_conv, value1_conv_ast) = _to_number(value1, value1_ast)
            (value2_conv, value2_conv_ast) = _to_number(value2, value2_ast)

        if convert_to_ast:
            return (value1_conv_ast, value2_conv_ast)
        else:
            return (value1_conv, value2_conv)

    @staticmethod
    def plus(arg1, arg2=None):
        """ If only one argument is given, prefix it with '+'. If two
        arguments are given, add the second to the first. If the first
        argument is a tuple of length 2 and the second is None, use the
        values in the tuple as arg1 and arg2. """
        if isinstance(arg1, (list, tuple)) and len(arg1) == 2 and arg2 is None:
            (arg1, arg2) = arg1
        if arg2 is None:
            return + arg1
        else:
            return arg1 + arg2

    @staticmethod
    def convert_to_number(value, decimal_point='.'):
        """ Convert value to a number. If value is an AST, another AST is
        wrapped around it to represent the conversion, e.g.,
            Str(s='1.2') -> Call(func=Name('float'), args=[Str(s='1.2')])
        1. Return all numbers (float, int, long) unchanged.
        2. Convert a string containing a number into a float.
        3. Convert a single character to its ASCII integer value.
        4. Extract the first element of a list and convert it to a number.
        5. Convert a Color to a float.
        If the value cannot be converted to a number and the value is not
        an AST, return None. If it is an AST, return an AST representing
        `float(value)'. """ # TODO find a better solution
        # 1. number
        if isinstance(value, (float, int, long, ast.Num)):
            return value

        converted = None
        conversion_ast = None
        convert_to_ast = False
        if isinstance(value, ast.AST):
            convert_to_ast = True
            value_ast = value
            value = ast_to_value(value_ast)
        if isinstance(decimal_point, ast.AST):
            decimal_point = ast_to_value(decimal_point)

        # 2./3. string
        if isinstance(value, basestring):
            if convert_to_ast:
                conversion_ast = Primitive.convert_for_cmp(value_ast,
                                                           decimal_point)
                if not isinstance(conversion_ast, ast.Num):
                    converted = None
            else:
                converted = Primitive.convert_for_cmp(value, decimal_point)
                if not isinstance(converted, (float, int, long)):
                    converted = None
        # 4. list
        elif isinstance(value, list):
            if value:
                number = Primitive.convert_to_number(value[0])
                if convert_to_ast:
                    conversion_ast = number
                else:
                    converted = number
            else:
                converted = None
                if convert_to_ast:
                    conversion_ast = get_call_ast('float', [value_ast])
        # 5. Color
        elif isinstance(value, Color):
            converted = float(value)
            if convert_to_ast:
                conversion_ast = get_call_ast('float', [value_ast])
        else:
            converted = None
            if convert_to_ast:
                conversion_ast = get_call_ast('float', [value_ast])

        if convert_to_ast:
            if conversion_ast is None:
                return value_ast
            else:
                return conversion_ast
        else:
            if converted is None:
                return value
            else:
                return converted

    @staticmethod
    def minus(arg1, arg2=None):
        """ If only one argument is given, change its sign. If two
        arguments are given, subtract the second from the first. """
        if arg2 is None:
            return - arg1
        else:
            return arg1 - arg2

    @staticmethod
    def multiply(arg1, arg2):
        """ Multiply the two arguments """
        return arg1 * arg2

    @staticmethod
    def divide(arg1, arg2):
        """ Divide the first argument by the second """
        return arg1 / arg2

    @staticmethod
    def modulo(arg1, arg2):
        """ Return the remainder of dividing the first argument by the second.
        If the first argument is a string, format it with the value(s) in
        the second argument. """
        return arg1 % arg2

    @staticmethod
    def power(arg1, arg2):
        """ Raise the first argument to the power given by the second """
        return arg1 ** arg2

    @staticmethod
    def integer_division(arg1, arg2):
        """ Divide the first argument by the second and return the integer
        that is smaller than or equal to the result """
        return arg1 // arg2

    @staticmethod
    def bitwise_and(arg1, arg2):
        """ Return the bitwise AND of the two arguments """
        return arg1 & arg2

    @staticmethod
    def bitwise_or(arg1, arg2):
        """ Return the bitwise OR of the two arguments """
        return arg1 | arg2

    @staticmethod
    def and_(arg1, arg2):
        """ Logcially conjoin the two arguments (using short-circuting) """
        return arg1 and arg2

    @staticmethod
    def or_(arg1, arg2):
        """ Logically disjoin the two arguments (using short-circuting) """
        return arg1 or arg2

    @staticmethod
    def not_(arg):
        """ Return True if the argument evaluates to False, and False
        otherwise. """
        return not arg

    @staticmethod
    def convert_for_cmp(value, decimal_point='.'):
        """ Convert value such that it can be compared to something else. If
        value is an AST, another AST is wrapped around it to represent the
        conversion, e.g.,
            Str(s='a') -> Call(func=Name('ord'), args=[Str(s='a')])
        1. Convert a string containing a number into a float.
        2. Convert a single character to its ASCII integer value.
        3. Return all other values unchanged. """
        converted = None
        conversion_ast = None
        convert_to_ast = False
        if isinstance(value, ast.AST):
            convert_to_ast = True
            value_ast = value
            value = ast_to_value(value_ast)
        if isinstance(decimal_point, ast.AST):
            decimal_point = ast_to_value(decimal_point)

        if isinstance(value, basestring):
            # 1. string containing a number
            replaced = value.replace(decimal_point, '.')
            try:
                converted = float(replaced)
            except ValueError:
                pass
            else:
                if convert_to_ast:
                    conversion_ast = get_call_ast('float', [value_ast])

            # 2. single character
            if converted is None:
                try:
                    converted = ord(value)
                except TypeError:
                    pass
                else:
                    if convert_to_ast:
                        conversion_ast = get_call_ast('ord', [value_ast])

        # 3. normal string or other type of value (nothing to do)

        if convert_to_ast:
            if conversion_ast is None:
                return value_ast
            else:
                return conversion_ast
        else:
            if converted is None:
                return value
            else:
                return converted

    @staticmethod
    def equals(arg1, arg2):
        """ Return arg1 == arg2 """
        return arg1 == arg2

    @staticmethod
    def less(arg1, arg2):
        """ Return arg1 < arg2 """
        return arg1 < arg2

    @staticmethod
    def greater(arg1, arg2):
        """ Return arg1 > arg2 """
        return arg1 > arg2



def is_instancemethod(method):
    # TODO how to access the type `instancemethod` directly?
    return type(method).__name__ == "instancemethod"

def is_bound_instancemethod(method):
    return is_instancemethod(method) and method.im_self is not None

def is_unbound_instancemethod(method):
    return is_instancemethod(method) and method.im_self is None

def is_staticmethod(method):
    # TODO how to access the type `staticmethod` directly?
    return type(method).__name__ == "staticmethod"


def value_to_ast(value, *args_for_prim, **kwargs_for_prim):
    """ Turn a value into an AST. Supported types: Primitive, int, float,
    bool, basestring, list
    If the value is already an AST, return it unchanged.
    If the value is a non-exportable Primitive, return None. """
    # TODO media
    if isinstance(value, ast.AST):
        return value
    elif isinstance(value, Primitive):
        if value.export_me:
            return value.get_ast(*args_for_prim, **kwargs_for_prim)
        else:
            return None
    elif isinstance(value, bool):
        return ast.Name(id=str(value), ctx=ast.Load)
    elif isinstance(value, (int, float)):
        return ast.Num(n=value)
    elif isinstance(value, basestring):
        return ast.Str(value)
    elif isinstance(value, list):
        ast_list = []
        for item in value:
            item_ast = value_to_ast(item)
            if item_ast is not None:
                ast_list.append(item_ast)
        return ast.List(elts=ast_list, ctx=ast.Load)
    elif isinstance(value, Color):
        if str(value) in CONSTANTS:
            # repr(str(value)) is necessary; it first converts the Color to a
            # string and then adds appropriate quotes around that string
            return ast.Name(id='CONSTANTS[%s]' % repr(str(value)),
                            ctx=ast.Load)
        else:
            # call to the Color constructor with this object's values,
            # e.g., Color('red', 0, 50, 100)
            return get_call_ast('Color', [value.name, value.color,
                                          value.shade, value.gray])
    else:
        raise ValueError("unknown type of raw value: " + repr(type(value)))

def ast_to_value(ast_object):
    """ Retrieve the value out of a value AST. Supported AST types:
    Num, Str, Name, List, Tuple, Set
    If no value can be extracted, return None. """
    if isinstance(ast_object, ast.Num):
        return ast_object.n
    elif isinstance(ast_object, ast.Str):
        return ast_object.s
    elif isinstance(ast_object, (ast.List, ast.Tuple, ast.Set)):
        return ast_object.elts
    elif (isinstance(ast_object, ast.Name)):
        try:
            return eval(ast_object.id)
        except NameError:
            return None
    else:
        return None


def get_call_ast(func_name, args=[], keywords={}):
    return ast.Call(func=ast.Name(id=func_name,
                                  ctx=ast.Load),
                    args=args,
                    keywords=keywords,
                    starargs=None,
                    kwargs=None)


def call_me(something):
    """ Return True iff this is a Primitive and its call_me attribute is
    True, i.e. nothing is callable except for Primitives with
    call_me == True """
    return isinstance(something, Primitive) and something.call_me

def export_me(something):
    """ Return True iff this is not a Primitive or its export_me attribute
    is True, i.e. everything is exportable except for Primitives with
    export_me == False """
    return not isinstance(something, Primitive) or something.export_me


