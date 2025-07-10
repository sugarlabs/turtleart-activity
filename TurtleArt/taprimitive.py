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

import ast
from gettext import gettext as _
from math import sqrt
from random import uniform
import traceback
import inspect

# from ast_pprint import * # only used for debugging, safe to comment out


from .tablock import Media

from .tacanvas import TurtleGraphics
from .taconstants import (Color, CONSTANTS, ColorObj, Vector)
from .talogo import (LogoCode, logoerror, NegativeRootError)
from .taturtle import (Turtle, Turtles)
from TurtleArt.tatype import (TYPE_CHAR, TYPE_INT, TYPE_FLOAT, TYPE_OBJECT,
                              TYPE_MEDIA, TYPE_COLOR, BOX_AST, ACTION_AST,
                              TYPE_VECTOR,
                              Type, TypeDisjunction, TATypeError, get_type,
                              TypedSubscript, TypedName, is_bound_method,
                              is_instancemethod, is_staticmethod,
                              identity, get_converter, convert, get_call_ast)
from .tautils import debug_output
from .tawindow import (TurtleArtWindow, global_objects, plugins_in_use)
from .util import ast_extensions


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
    but that can also be transformed into a Python AST."""

    _DEBUG = False

    STANDARD_OPERATORS = {'plus': (ast.UAdd, ast.Add),
                          'minus': (ast.USub, ast.Sub),
                          'multiply': ast.Mult,
                          'divide': ast.Div,
                          'modulo': ast.Mod,
                          'power': ast.Pow,
                          'and_': ast.And,
                          'or_': ast.Or,
                          'not_': ast.Not,
                          'equals': ast.Eq,
                          'less': ast.Lt,
                          'greater': ast.Gt}

    def __init__(self, func, return_type=TYPE_OBJECT, arg_descs=None,
                 kwarg_descs=None, call_afterwards=None, export_me=True):
        """ return_type -- the type (from the type hierarchy) that this
            Primitive will return
        arg_descs, kwarg_descs -- a list of argument descriptions and
            a dictionary of keyword argument descriptions. An argument
            description can be either an ArgSlot or a ConstantArg.
        call_afterwards -- Code to call after this Primitive has been called
            (e.g., for updating labels in LogoCode) (not used for creating
            AST)
        export_me -- True iff this Primitive should be exported to Python
            code (the default case) """
        self.func = func
        self.return_type = return_type

        if arg_descs is None:
            self.arg_descs = []
        else:
            self.arg_descs = arg_descs

        if kwarg_descs is None:
            self.kwarg_descs = {}
        else:
            self.kwarg_descs = kwarg_descs

        self.call_afterwards = call_afterwards
        self.export_me = export_me

    def copy(self):
        """ Return a Primitive object with the same attributes as this one.
        Shallow-copy the arg_descs and kwarg_descs attributes. """
        arg_descs_copy = self.arg_descs[:]
        if isinstance(self.arg_descs, ArgListDisjunction):
            arg_descs_copy = ArgListDisjunction(arg_descs_copy)
        return Primitive(self.func,
                         return_type=self.return_type,
                         arg_descs=arg_descs_copy,
                         kwarg_descs=self.kwarg_descs.copy(),
                         call_afterwards=self.call_afterwards,
                         export_me=self.export_me)

    def __repr__(self):
        return "Primitive(%s -> %s)" % (repr(self.func), str(self.return_type))

    @property
    def __name__(self):
        return self.func.__name__

    def get_name_for_export(self):
        """ Return the expression (as a string) that represents this Primitive
        in the exported Python code, e.g., 'turtle.forward'. """
        func_name = ""
        if self.wants_turtle():
            func_name = "turtle."
        elif self.wants_turtles():
            func_name = "turtles."
        elif self.wants_canvas():
            func_name = "canvas."
        elif self.wants_logocode():
            func_name = "logo."
        elif self.wants_heap():
            func_name = "logo.heap."
        elif self.wants_tawindow():
            func_name = "tw."
        else:
            results, plugin = self.wants_plugin()
            if results:
                for k in list(global_objects.keys()):
                    if k == plugin:
                        if k not in plugins_in_use:
                            plugins_in_use.append(k)
                        func_name = k.lower() + '.'
                        break

        # get the name of the function directly from the function itself
        func_name += self.func.__name__
        return func_name

    def are_slots_filled(self):
        """ Return True iff none of the arg_descs or kwarg_descs is an
        ArgSlot. """
        for arg_desc in self.arg_descs:
            if isinstance(arg_desc, ArgSlot):
                return False
        for key in self.kwarg_descs:
            if isinstance(self.kwarg_descs[key], ArgSlot):
                return False
        return True

    def fill_slots(self, arguments=None, keywords=None, convert_to_ast=False,
                   call_my_args=True):
        """ Return a copy of this Primitive whose ArgSlots are filled with
        the given arguments, turned into ConstantArgs. Call the arguments,
        apply their wrappers, and check their types as appropriate. """
        if arguments is None:
            arguments = []
        if keywords is None:
            keywords = {}

        new_prim = self.copy()

        if isinstance(new_prim.arg_descs, ArgListDisjunction):
            slot_list_alternatives = list(new_prim.arg_descs)
        else:
            slot_list_alternatives = [new_prim.arg_descs]

        # arguments
        error = None
        filler = None
        for slot_list in slot_list_alternatives:
            error = None
            new_slot_list = []
            filler_list = list(arguments[:])
            for slot in slot_list:
                if isinstance(slot, ArgSlot):
                    filler = filler_list.pop(0)
                    try:
                        const = slot.fill(filler,
                                          convert_to_ast=convert_to_ast,
                                          call_my_args=call_my_args)
                    except TATypeError as e:
                        error = e
                        if Primitive._DEBUG:
                            traceback.print_exc()
                        break
                    else:
                        new_slot_list.append(const)
                else:
                    new_slot_list.append(slot)
            if error is None:
                new_prim.arg_descs = new_slot_list
                break
        if error is not None:
            raise error

        # keyword arguments
        for key in keywords:
            kwarg_desc = new_prim.kwarg_descs[key]
            if isinstance(kwarg_desc, ArgSlot):
                const = kwarg_desc.fill(keywords[key],
                                        convert_to_ast=convert_to_ast,
                                        call_my_args=call_my_args)
                new_prim.kwarg_descs[key] = const

        return new_prim

    def get_values_of_filled_slots(self, exportable_only=False):
        """ Return the values of all filled argument slots as a list, and
        the values of all filled keyword argument slots as a dictionary.
        Ignore all un-filled (keyword) argument slots.
        exportable_only -- return only exportable values and convert values
            to ASTs instead of calling them """
        new_args = []
        for c_arg in self.arg_descs:
            if isinstance(c_arg, ConstantArg) and \
                    (not exportable_only or export_me(c_arg.value)):
                new_args.append(c_arg.get(convert_to_ast=exportable_only))
        new_kwargs = {}
        for key in self.kwarg_descs:
            if isinstance(self.kwarg_descs[key], ConstantArg) and \
                    (not exportable_only or export_me(
                        self.kwarg_descs[key].value)):
                new_kwargs[key] = self.kwarg_descs[key].get(
                    convert_to_ast=exportable_only)
        return new_args, new_kwargs

    def allow_call_args(self, recursive=False):
        """ Set call_args attribute of all argument descriptions to True
        recursive -- recursively call allow_call_args on all constant args
            that are Primitives """
        for arg_desc in self.arg_descs:
            arg_desc.call_arg = True
            if recursive and isinstance(arg_desc, ConstantArg) and \
                    isinstance(arg_desc.value, Primitive):
                arg_desc.value.allow_call_args(recursive=True)
        for kwarg_desc in self.kwarg_descs:
            kwarg_desc.call_arg = True
            if recursive and isinstance(kwarg_desc, ConstantArg) and \
                    isinstance(kwarg_desc.value, Primitive):
                kwarg_desc.value.allow_call_args(recursive=True)

    def __call__(self, *runtime_args, **runtime_kwargs):
        """ Execute the function, passing it the arguments received at
        runtime. Also call the function in self.call_afterwards and pass it
        all runtime_args and runtime_kwargs.
        If the very first argument is a LogoCode instance, it is removed.
        The active turtle, the Turtles object, the canvas, the LogoCode
        object, or the TurtleArtWindow object will be prepended to the
        arguments (depending on what this Primitive wants). """

        # remove the first argument if it is a LogoCode instance
        if runtime_args and isinstance(runtime_args[0], LogoCode):
            runtime_args = runtime_args[1:]

        if Primitive._DEBUG:
            debug_output(repr(self))
            debug_output("  runtime_args: " + repr(runtime_args))
        # fill the ArgSlots with the runtime arguments
        new_prim = self.fill_slots(runtime_args, runtime_kwargs,
                                   convert_to_ast=False)
        if not new_prim.are_slots_filled():
            raise logoerror("#syntaxerror")
        if Primitive._DEBUG:
            debug_output("  new_prim.arg_descs: " + repr(new_prim.arg_descs))

        # extract the actual values from the (now constant) arguments
        (new_args, new_kwargs) = new_prim.get_values_of_filled_slots()
        if Primitive._DEBUG:
            debug_output("  new_args: " + repr(new_args))
            debug_output("end " + repr(self))

        # what does this primitive want as its first argument?
        first_arg = None
        if not is_bound_method(new_prim.func):
            if new_prim.wants_turtle():
                first_arg = global_objects["turtles"].get_active_turtle()
            elif new_prim.wants_turtles():
                first_arg = global_objects["turtles"]
            elif new_prim.wants_canvas():
                first_arg = global_objects["canvas"]
            elif new_prim.wants_logocode():
                first_arg = global_objects["logo"]
            elif new_prim.wants_heap():
                first_arg = global_objects["logo"].heap
            elif new_prim.wants_tawindow():
                first_arg = global_objects["window"]
            else:
                result, plugin = new_prim.wants_plugin()
                if result:
                    first_arg = plugin

        # execute the actual function
        if first_arg is None:
            return_value = new_prim.func(*new_args, **new_kwargs)
        else:
            return_value = new_prim.func(first_arg, *new_args, **new_kwargs)

        if new_prim.call_afterwards is not None:
            new_prim.call_afterwards(*new_args, **new_kwargs)

        return return_value

    def get_ast(self, *arg_asts, **kwarg_asts):
        """Transform this object into a Python AST. When serialized and
        executed, the AST will do exactly the same as calling this
        object."""

        if Primitive._DEBUG:
            debug_output(repr(self))
            debug_output("  arg_asts: " + repr(arg_asts))
        new_prim = self.fill_slots(arg_asts, kwarg_asts, convert_to_ast=True)
        if not new_prim.are_slots_filled():
            raise PyExportError("not enough arguments")
        if Primitive._DEBUG:
            debug_output("  new_prim.arg_descs: " + repr(new_prim.arg_descs))

        # extract the actual values from the (now constant) arguments
        (new_arg_asts, new_kwarg_asts) = new_prim.get_values_of_filled_slots(
            exportable_only=True)
        if Primitive._DEBUG:
            debug_output("  new_arg_asts: " + repr(new_arg_asts))
            debug_output("end " + repr(self))

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
                    pos_cond_ast = new_arg_asts[0].args[0]
                    condition_ast = ast.UnaryOp(op=ast.Not,
                                                operand=pos_cond_ast)
                else:
                    raise PyExportError("unknown loop controller: " + repr(
                        controller))
                loop_ast = ast.While(test=condition_ast,
                                     body=new_arg_asts[1],
                                     orelse=[])
                # Until always executes its body once.
                if controller == Primitive.controller_until:
                    loop_list = []
                    for arg_ast in new_arg_asts[1]:
                        loop_list.append(arg_ast)
                    loop_list.append(loop_ast)
                    return loop_list
                else:
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
            target_ast = ast.Subscript(value=BOX_AST,
                                       slice=ast.Index(value=new_arg_asts[0]),
                                       ctx=ast.Store)
            return ast.Assign(targets=[target_ast], value=new_arg_asts[1])
        elif self == LogoCode.prim_get_box:
            return ast.Subscript(value=BOX_AST,
                                 slice=ast.Index(value=new_arg_asts[0]),
                                 ctx=ast.Load)

        # action stacks
        elif self == LogoCode.prim_define_stack:
            return
        elif self == LogoCode.prim_invoke_stack:
            stack_func = ast.Subscript(
                value=ACTION_AST,
                slice=ast.Index(value=new_arg_asts[0]), ctx=ast.Load)
            call_ast = get_call_ast('logo.icall', [stack_func])
            return [call_ast, ast_yield_true()]
        elif self == LogoCode.prim_invoke_return_stack:
            # FIXME: Need to return value
            stack_func = ast.Subscript(
                value=ACTION_AST,
                slice=ast.Index(value=new_arg_asts[0]), ctx=ast.Load)
            call_ast = get_call_ast('logo.icall', [stack_func])
            return [call_ast, ast_yield_true()]

        # stop stack
        elif self == LogoCode.prim_stop_stack:
            return ast.Return()

        # sleep/ wait
        elif self == LogoCode.prim_wait:
            return [get_call_ast('sleep', new_arg_asts), ast_yield_true()]

        # standard operators
        elif self.func.__name__ in Primitive.STANDARD_OPERATORS:
            op = Primitive.STANDARD_OPERATORS[self.func.__name__]
            # 'divide': prevent unwanted integer division
            if self == Primitive.divide:
                def _is_float(x):
                    return get_type(x)[0] == TYPE_FLOAT
                if not _is_float(new_arg_asts[0]) and \
                        not _is_float(new_arg_asts[1]):
                    new_arg_asts[0] = get_call_ast('float', [new_arg_asts[0]],
                                                   return_type=TYPE_FLOAT)
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

        # f(x)
        elif self == LogoCode.prim_myfunction:
            param_asts = []
            for id_ in ['x', 'y', 'z'][:len(new_arg_asts) - 1]:
                param_asts.append(ast.Name(id=id_, ctx=ast.Param))
            func_ast = ast_extensions.LambdaWithStrBody(
                body_str=new_arg_asts[0].s, args=param_asts)
            return get_call_ast(func_ast, new_arg_asts[1:],
                                return_type=self.return_type)

        # square root
        elif self == Primitive.square_root:
            return get_call_ast('sqrt', new_arg_asts, new_kwarg_asts,
                                return_type=self.return_type)

        # random
        elif self in (Primitive.random_char, Primitive.random_int):
            uniform_ast = get_call_ast('uniform', new_arg_asts)
            round_ast = get_call_ast('round', [uniform_ast, ast.Num(n=0)])
            int_ast = get_call_ast('int', [round_ast], return_type=TYPE_INT)
            if self == Primitive.random_char:
                chr_ast = get_call_ast('chr', [int_ast], return_type=TYPE_CHAR)
                return chr_ast
            else:
                return int_ast

        # identity
        elif self == Primitive.identity:
            return new_arg_asts[0]

        # constant
        elif self == CONSTANTS.get:
            return TypedSubscript(value=ast.Name(id='CONSTANTS', ctx=ast.Load),
                                  slice_=ast.Index(value=new_arg_asts[0]),
                                  return_type=self.return_type)

        # group of Primitives or sandwich-clamp block
        elif self in (Primitive.group, LogoCode.prim_clamp):
            ast_list = []
            for prim in new_arg_asts[0]:
                if export_me(prim):
                    new_ast = value_to_ast(prim)
                    if isinstance(new_ast, ast.AST):
                        ast_list.append(new_ast)
            return ast_list

        # set turtle
        elif self == LogoCode.prim_turtle:
            text = 'turtle = turtles.get_active_turtle()'
            return [get_call_ast('logo.prim_turtle', new_arg_asts),
                    ast_extensions.ExtraCode(text)]

        elif self == LogoCode.active_turtle:
            text = 'turtle = turtles.get_active_turtle()'
            return ast_extensions.ExtraCode(text)

        # comment
        elif self == Primitive.comment:
            if isinstance(new_arg_asts[0], ast.Str):
                text = ' ' + str(new_arg_asts[0].s)
            else:
                text = ' ' + str(new_arg_asts[0])
            return ast_extensions.Comment(text)

        # print
        elif self == TurtleArtWindow.print_:
            func_name = self.get_name_for_export()
            call_ast = get_call_ast(func_name, new_arg_asts)
            print_ast = ast.Print(values=new_arg_asts[:1], dest=None, nl=True)
            return [call_ast, print_ast]

        # heap
        elif self == LogoCode.get_heap:
            return TypedName(id_='logo.heap', return_type=self.return_type)
        elif self == LogoCode.reset_heap:
            target_ast = ast.Name(id='logo.heap', ctx=ast.Store)
            value_ast = ast.List(elts=[], ctx=ast.Load)
            return ast.Assign(targets=[target_ast], value=value_ast)

        # NORMAL FUNCTION CALL #

        else:
            func_name = self.get_name_for_export()
            return get_call_ast(func_name, new_arg_asts, new_kwarg_asts,
                                return_type=self.return_type)

    def __eq__(self, other):
        """ Two Primitives are equal iff their all their properties are equal.
        Consider bound and unbound methods equal. """
        # other is a Primitive
        if isinstance(other, Primitive):
            return self == other.func and \
                self.return_type == other.return_type and \
                self.arg_descs == other.arg_descs and \
                self.kwarg_descs == other.kwarg_descs and \
                self.call_afterwards == other.call_afterwards and \
                self.export_me == other.export_me

        # other is a callable
        elif callable(other):
            if is_instancemethod(self.func) != is_instancemethod(other):
                return False
            elif is_instancemethod(self.func):  # and is_instancemethod(other):
                return self.func.__self__.__class__ == \
                    other.__self__.__class__ and \
                    self.func.__func__ == other.__func__
            else:
                return self.func == other

        elif is_staticmethod(other):
            return self.func == other.__func__

        # other is neither a Primitive nor a callable
        else:
            return False

    def wants_turtle(self):
        """Does this Primitive want to get the active turtle as its first
        argument?"""
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
        return self.func.__name__ == '<lambda>' or self._wants(LogoCode)

    def wants_heap(self):
        """ Does this Primitive want to get the heap as its first argument? """
        return (hasattr(self.func, '__self__'
                        ) and isinstance(self.func.__self__, list)) or \
            self.func in list(list.__dict__.values())

    def wants_tawindow(self):
        """ Does this Primitive want to get the TurtleArtWindow instance
        as its first argument? """
        return self._wants(TurtleArtWindow)

    def wants_plugin(self):
        """Does this Primitive want to get a plugin instance as its first
        argument? """
        for obj in list(global_objects.keys()):
            if self._wants(global_objects[obj].__class__):
                return True, obj
        return False, None

    def wants_nothing(self):
        """Does this Primitive want nothing as its first argument? I.e. does
        it want to be passed all the arguments of the block and
        nothing else?"""
        return not is_instancemethod(self.func)

    def _wants(self, theClass):
        try:
            return inspect.getattr_static(
                theClass, self.func.__name__).__class__.__name__ == 'function'
        except AttributeError:
            return False

    # treat the following methods in a special way when converting the
    # Primitive to an AST

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
    def controller_while(condition):
        """ Loop controller for the 'while' block
        condition -- Primitive that is evaluated every time through the
            loop """
        condition.allow_call_args(recursive=True)
        while condition():
            yield True
        yield False

    @staticmethod
    def controller_until(condition):
        """ Loop controller for the 'until' block
        condition -- Primitive that is evaluated every time through the
            loop """
        condition.allow_call_args(recursive=True)
        while not condition():
            yield True
        yield False

    LOOP_CONTROLLERS = [controller_repeat, controller_forever,
                        controller_while, controller_until]

    def _get_loop_controller(self):
        """ Return the controller for this loop Primitive. Raise a
        ValueError if no controller was found. """
        def _is_loop_controller(candidate):
            return callable(candidate) and \
                candidate in Primitive.LOOP_CONTROLLERS

        for desc in self.arg_descs:
            if isinstance(desc, ConstantArg):
                value = desc.value
                if _is_loop_controller(value):
                    return value
            elif isinstance(desc, ArgSlot):
                wrapper = desc.wrapper
                if _is_loop_controller(wrapper):
                    return wrapper

        # no controller found
        raise PyExportError("found no loop controller for " + repr(self))

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
    def plus(arg1, arg2=None):
        """ If only one argument is given, prefix it with '+'. If two
        arguments are given, add the second to the first. If the first
        argument is a tuple of length 2 and the second is None, use the
        values in the tuple as arg1 and arg2. """
        if isinstance(arg1, (list, tuple)) and len(arg1) == 2 and arg2 is None:
            (arg1, arg2) = arg1
        if arg2 is None:
            return + arg1
        elif isinstance(arg1, Vector) and isinstance(arg2, Vector):
            vector = []
            for i in range(len(arg1.vector)):
                vector.append(arg1.vector[i] + arg2.vector[i])
            return Vector(arg1.name, vector)
        else:
            return arg1 + arg2

    @staticmethod
    def minus(arg1, arg2=None):
        """ If only one argument is given, change its sign. If two
        arguments are given, subtract the second from the first. """
        if arg2 is None:
            return - arg1
        elif isinstance(arg1, Vector) and isinstance(arg2, Vector):
            vector = []
            for i in range(len(arg1.vector)):
                vector.append(arg1.vector[i] - arg2.vector[i])
            return Vector(arg1.name, vector)
        else:
            return arg1 - arg2

    @staticmethod
    def multiply(arg1, arg2):
        """ Multiply the two arguments """
        if isinstance(arg1, Vector) and isinstance(arg2, (int, float)):
            vector = []
            for i in range(len(arg1.vector)):
                vector.append(arg1.vector[i] * arg2)
            return Vector(arg1.name, vector)
        elif isinstance(arg2, Vector) and isinstance(arg1, (int, float)):
            vector = []
            for i in range(len(arg2.vector)):
                vector.append(arg2.vector[i] * arg1)
            return Vector(arg2.name, vector)
        else:
            return arg1 * arg2

    @staticmethod
    def divide(arg1, arg2):
        """ Divide the first argument by the second """
        if arg2 == 0:
            raise logoerror("#zerodivide")

        if isinstance(arg1, Vector) and isinstance(arg2, (int, float)):
            vector = []
            for i in range(len(arg1.vector)):
                vector.append(arg1.vector[i] / arg2)
            return Vector(arg1.name, vector)
        elif isinstance(arg2, Vector) and isinstance(arg1, (int, float)):
            vector = []
            for i in range(len(arg2.vector)):
                vector.append(arg2.vector[i] / arg1)
            return Vector(arg2.name, vector)
        else:
            return float(arg1) / arg2

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
    def square_root(arg1):
        """ Return the square root of the argument. If it is a negative
        number, raise a NegativeRootError. """
        if arg1 < 0:
            raise NegativeRootError(neg_value=arg1)
        return sqrt(arg1)

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
    def equals(arg1, arg2):
        """ Return arg1 == arg2 """
        # See comment in tatype.py TYPE_BOX -> TYPE_COLOR
        if isinstance(arg1, ColorObj) or isinstance(arg2, ColorObj):
            return str(arg1) == str(arg2)
        else:
            return arg1 == arg2

    @staticmethod
    def less(arg1, arg2):
        """ Return arg1 < arg2 """
        # See comment in tatype.py TYPE_BOX -> TYPE_COLOR
        if isinstance(arg1, ColorObj) or isinstance(arg2, ColorObj):
            return float(arg1) < float(arg2)
        else:
            return arg1 < arg2

    @staticmethod
    def greater(arg1, arg2):
        """ Return arg1 > arg2 """
        # See comment in tatype.py TYPE_BOX -> TYPE_COLOR
        if isinstance(arg1, ColorObj) or isinstance(arg2, ColorObj):
            return float(arg1) > float(arg2)
        else:
            return arg1 > arg2

    @staticmethod
    def comment(text):
        """In 'snail' execution mode, display the comment. Else, do
        nothing."""
        tw = global_objects["window"]
        if not tw.hide and tw.step_time != 0:
            tw.showlabel('print', text)

    @staticmethod
    def random_int(lower, upper):
        """ Choose a random integer between lower and upper, which must be
        integers """
        return int(round(uniform(lower, upper), 0))

    @staticmethod
    def random_char(lower, upper):
        """ Choose a random Unicode code point between lower and upper,
        which must be integers """
        return chr(Primitive.random_int(lower, upper))


class Disjunction(tuple):

    """ Abstract disjunction class (not to be instantiated directly) """

    def __init__(self, iterable):
        tuple(iterable)

    def __repr__(self):
        s = ["("]
        for disj in self:
            s.append(repr(disj))
            s.append(" or ")
        s.pop()
        s.append(")")
        return "".join(s)

    def get_alternatives(self):
        """ Return a tuple of alternatives, i.e. self """
        return self


class PrimitiveDisjunction(Disjunction, Primitive):

    """ Disjunction of two or more Primitives. PrimitiveDisjunctions may not
    be nested. """

    @property
    def return_type(self):
        """ Tuple of the return_types of all disjuncts """
        return TypeDisjunction((prim.return_type for prim in self))

    def __call__(self, *runtime_args, **runtime_kwargs):
        """ Loop over the disjunct Primitives and try to fill their slots
        with the given args and kwargs. Call the first Primitives whose
        slots could be filled successfully. If all disjunct Primitives
        fail, raise the last error that occurred. """

        # remove the first argument if it is a LogoCode instance
        if runtime_args and isinstance(runtime_args[0], LogoCode):
            runtime_args = runtime_args[1:]

        error = None
        for prim in self:
            try:
                new_prim = prim.fill_slots(runtime_args, runtime_kwargs,
                                           convert_to_ast=False)
            except TATypeError:
                # on failure, try the next one
                continue
            else:
                # on success, call this Primitive
                return new_prim()

        # if we get here, all disjuncts failed
        if error is not None:
            raise error


class ArgListDisjunction(Disjunction):

    """ Disjunction of two or more argument lists """
    pass


class ArgSlot(object):

    """ Description of the requirements that a Primitive demands from an
    argument or keyword argument. An ArgSlot is filled at runtime, based
    on the block program structure. """

    def __init__(self, type_, call_arg=True, wrapper=None):
        """
        type_ -- what type of the type hierarchy the argument should have
            (after the wrapper has been applied)
        call_arg -- if this argument is callable, should it be called and
            its return value passed to the parent Primitive (True, the
            default), or should it be passed as it is (False)?
        wrapper -- a Primitive that is 'wrapped around' the argument before
            it gets passed to its parent Primitive. Wrappers can be nested
            infinitely. """
        self.type = type_
        self.call_arg = call_arg
        self.wrapper = wrapper

    def __repr__(self):
        s = ["ArgSlot(type="]
        s.append(repr(self.type))
        if not self.call_arg:
            s.append(", call=")
            s.append(repr(self.call_arg))
        if self.wrapper is not None:
            s.append(", wrapper=")
            s.append(repr(self.wrapper))
        s.append(")")
        return "".join(s)

    def get_alternatives(self):
        """ Return a tuple of slot alternatives, i.e. (self, ) """
        return (self, )

    def fill(self, argument, convert_to_ast=False, call_my_args=True):
        """ Try to fill this argument slot with the given argument. Return
        a ConstantArg containing the result. If there is a type problem,
        raise a TATypeError. """
        if isinstance(argument, ast.AST):
            convert_to_ast = True

        # 1. can the argument be called?
        (func_disjunction, args) = (None, [])
        if isinstance(argument, tuple) and argument and callable(argument[0]):
            func_disjunction = argument[0]
            if len(argument) >= 2 and isinstance(argument[1], LogoCode):
                args = argument[2:]
            else:
                args = argument[1:]
        elif callable(argument):
            func_disjunction = argument

        # make sure we can loop over func_disjunction
        if not isinstance(func_disjunction, PrimitiveDisjunction):
            func_disjunction = PrimitiveDisjunction((func_disjunction, ))

        error = None
        bad_value = argument  # the value that caused the TATypeError
        for func in func_disjunction:
            error = None
            for slot in self.get_alternatives():

                if isinstance(slot.wrapper, PrimitiveDisjunction):
                    wrapper_disjunction = slot.wrapper
                else:
                    wrapper_disjunction = PrimitiveDisjunction((slot.wrapper,))

                for wrapper in wrapper_disjunction:

                    # check if the argument can fill this slot (type-wise)
                    # (lambda functions are always accepted)
                    if getattr(func, '__name__', None) == '<lambda>':
                        converter = identity
                        old_type = TYPE_OBJECT
                        new_type = slot.type
                    else:
                        if wrapper is not None:
                            arg_types = get_type(wrapper)[0]
                            bad_value = wrapper
                        elif func is not None:
                            arg_types = get_type(func)[0]
                            bad_value = func
                        else:
                            arg_types = get_type(argument)[0]
                            bad_value = argument
                        converter = None
                        if not isinstance(arg_types, TypeDisjunction):
                            arg_types = TypeDisjunction((arg_types, ))
                        if isinstance(slot.type, TypeDisjunction):
                            slot_types = slot.type
                        else:
                            slot_types = TypeDisjunction((slot.type, ))
                        for old_type in arg_types:
                            for new_type in slot_types:
                                converter = get_converter(old_type, new_type)
                                if converter is not None:
                                    break
                            if converter is not None:
                                break
                        # unable to convert, try next wrapper/ slot/ func
                        if converter is None:
                            continue

                    # 1. (cont'd) call the argument or pass it on as a callable
                    called_argument = argument
                    if func is not None:
                        func_prim = func
                        if not isinstance(func_prim, Primitive):
                            func_prim = Primitive(
                                func_prim,
                                [ArgSlot(TYPE_OBJECT)] * len(args))
                        try:
                            func_prim = func_prim.fill_slots(
                                args,
                                convert_to_ast=convert_to_ast,
                                call_my_args=(slot.call_arg and call_my_args))
                        except TATypeError as e:
                            error = e
                            if Primitive._DEBUG:
                                traceback.print_exc()
                            # on failure, try next wrapper/ slot/ func
                            bad_value = error.bad_value
                            continue
                        if convert_to_ast:
                            called_argument = func_prim.get_ast()
                        else:
                            if slot.call_arg and call_my_args:
                                # call and pass on the return value
                                called_argument = func_prim()
                            else:
                                # don't call and pass on the callable
                                called_argument = func_prim

                    # 2. apply any wrappers
                    wrapped_argument = called_argument
                    if wrapper is not None:
                        if convert_to_ast:
                            if not hasattr(wrapper, "get_ast"):
                                raise PyExportError(
                                    ("cannot convert callable"
                                     " %s to an AST") % (repr(wrapper)))
                            wrapped_argument = wrapper.get_ast(
                                called_argument)
                        else:
                            if slot.call_arg and call_my_args:
                                wrapped_argument = wrapper(called_argument)
                            else:
                                wrapped_argument = wrapper.fill_slots(
                                    [called_argument], call_my_args=False)

                    # last chance to convert raw values to ASTs
                    # (but not lists of ASTs)
                    if convert_to_ast and not \
                            isinstance(wrapped_argument, ast.AST) and not \
                            (isinstance(wrapped_argument, list
                                        ) and wrapped_argument and isinstance(
                                wrapped_argument[0], ast.AST)):
                        wrapped_argument = value_to_ast(wrapped_argument)

                    # 3. check the type and convert the argument if necessary
                    converted_argument = wrapped_argument
                    if slot.call_arg and call_my_args:
                        try:
                            converted_argument = convert(
                                wrapped_argument,
                                new_type, old_type=old_type,
                                converter=converter)
                        except TATypeError as e:
                            error = e
                            if Primitive._DEBUG:
                                traceback.print_exc()
                            # on failure, try next wrapper/ slot/ func
                            bad_value = wrapped_argument
                            continue
                    elif converter != identity:
                        converted_argument = Primitive(
                            converter,
                            return_type=new_type,
                            arg_descs=[ConstantArg(wrapped_argument,
                                                   value_type=old_type,
                                                   call_arg=False)])
                    # on success, return the result
                    return ConstantArg(
                        converted_argument,
                        value_type=new_type,
                        call_arg=(slot.call_arg and call_my_args))

        # if we haven't returned anything yet, then all alternatives failed
        if error is not None:
            raise error
        else:
            raise TATypeError(bad_value=bad_value, bad_type=old_type,
                              req_type=new_type)


class ArgSlotDisjunction(Disjunction, ArgSlot):

    """ Disjunction of two or more argument slots """
    pass


class ConstantArg(object):

    """ A constant argument or keyword argument to a Primitive. It is
    independent of the block program structure. """

    def __init__(self, value, call_arg=True, value_type=None):
        """ call_arg -- call the value before returning it?
        value_type -- the type of the value (from the TA type system). This
            is useful to store e.g., the return type of call ASTs. """
        self.value = value
        self.call_arg = call_arg
        self.value_type = value_type

    def get(self, convert_to_ast=False):
        """ If call_arg is True and the value is callable, call the value
        and return its return value. Else, return the value unchanged.
        convert_to_ast -- return the equivalent AST instead of a raw value """
        if self.call_arg and callable(self.value):
            if convert_to_ast:
                return value_to_ast(self.value)
            else:
                return self.value()
        else:
            if convert_to_ast and not isinstance(self.value, list):
                return value_to_ast(self.value)
            else:
                return self.value

    def get_value_type(self):
        """ If this ConstantArg has stored the type of its value, return
        that. Else, use get_type(...) to guess the type of the value. """
        if self.value_type is None:
            return get_type(self.value)[0]
        else:
            return self.value_type

    def __repr__(self):
        s = ["ConstantArg("]
        s.append(repr(self.value))
        if not self.call_arg:
            s.append(", call=")
            s.append(repr(self.call_arg))
        s.append(")")
        return "".join(s)


def or_(*disjuncts):
    """ Return a disjunction object of the same type as the disjuncts. If
    the item type cannot be linked to a Disjunction class, return a tuple
    of the disjuncts. """
    if isinstance(disjuncts[0], Primitive):
        return PrimitiveDisjunction(disjuncts)
    elif isinstance(disjuncts[0], (list, ArgListDisjunction)):
        return ArgListDisjunction(disjuncts)
    elif isinstance(disjuncts[0], ArgSlot):
        return ArgSlotDisjunction(disjuncts)
    elif isinstance(disjuncts[0], Type):
        return TypeDisjunction(disjuncts)
    else:
        return tuple(disjuncts)


def value_to_ast(value, *args_for_prim, **kwargs_for_prim):
    """ Turn a value into an AST. Supported types: Primitive, int, float,
    bool, basestring, list
    If the value is already an AST, return it unchanged.
    If the value is a non-exportable Primitive, return None. """
    # already an AST
    if isinstance(value, ast.AST):
        return value
    # Primitive
    elif isinstance(value, Primitive):
        if value.export_me:
            return value.get_ast(*args_for_prim, **kwargs_for_prim)
        else:
            return None
    # boolean
    elif isinstance(value, bool):
        return ast.Name(id=str(value), ctx=ast.Load)
    # number
    elif isinstance(value, (int, float)):
        return ast.Num(n=value)
    # string
    elif isinstance(value, str):
        return ast.Str(value)
    # list (recursively transform to an AST)
    elif isinstance(value, list):
        ast_list = []
        for item in value:
            item_ast = value_to_ast(item)
            if item_ast is not None:
                ast_list.append(item_ast)
        return ast.List(elts=ast_list, ctx=ast.Load)
    # color
    elif isinstance(value, Color):
        # call to the Color constructor with this object's values,
        # e.g., Color('red', 0, 50, 100)
        return get_call_ast('Color', [value.name, value.color,
                                      value.shade, value.gray],
                            return_type=TYPE_COLOR)
    # vector
    elif isinstance(value, Vector):
        # call to the Vector constructor with this object's values,
        # e.g., Vector('banana', [105, 1, 27, 3, 0])
        return get_call_ast('Vector', [value.name, value.vector],
                            return_type=TYPE_VECTOR)
    # media
    elif isinstance(value, Media):
        args = [value_to_ast(value.type), value_to_ast(value.value)]
        return get_call_ast('Media', args, return_type=TYPE_MEDIA)
    # unknown
    else:
        raise PyExportError("unknown type of raw value: " + repr(type(value)))


def ast_yield_true():
    return ast.Yield(value=ast.Name(id='True', ctx=ast.Load))


def export_me(something):
    """ Return True iff this is not a Primitive or its export_me attribute
    is True, i.e. everything is exportable except for Primitives with
    export_me == False """
    return not isinstance(something, Primitive) or something.export_me
