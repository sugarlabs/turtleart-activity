# Copyright (c) 2013 Marion Zepf

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

""" Python export tool """

import ast
from gettext import gettext as _
from os import linesep
from os import path, pardir
import re
import traceback
from .util import codegen

# from ast_pprint import * # only used for debugging, safe to comment out

from .talogo import LogoCode
from .taprimitive import (ast_yield_true, Primitive, PyExportError,
                          value_to_ast)
from .tautils import (find_group, find_top_block, get_stack_name)
from .tawindow import plugins_in_use


_SETUP_CODE_START = """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

_INSTALL_PATH = '/usr/share/sugar/activities/TurtleArt.activity'
_ALTERNATIVE_INSTALL_PATH = \\
    '/usr/local/share/sugar/activities/TurtleArt.activity'

import os, sys, dbus
paths = []

paths.append('../%s.activity')
paths.append(os.path.expanduser('~') + '/Activities/%s.activity')
paths.append('/usr/share/sugar/activities/%s.activity')
paths.append('/usr/local/share/sugar/activities/%s.activity')
paths.append(
    '/home/broot/sugar-build/build/install/share/sugar/activities/%s.activity')
""" + \
    "paths.append('%s')" % \
    path.abspath(path.join(path.dirname(__file__), pardir)) + \
    """\

flag = False
for path in paths:
    for activity in ['TurtleBots', 'TurtleBlocks']:
        p = (path % activity) if "%" in path else path

        if os.path.exists(p) and p not in sys.path:
            flag = True
            sys.path.insert(0, p)

if not flag:
    print('This code require the Turtle Blocks/Bots activity to be installed.')
    exit(1)

from time import *
from random import uniform
from math import *

from pyexported.window_setup import *


tw = get_tw()

BOX = {}
ACTION = {}

global_objects = None
turtles = None
canvas = None
logo = None
"""

_SETUP_CODE_END = """\

if __name__ == '__main__':
    tw.lc.start_time = time()
    tw.lc.icall(start)
    GObject.idle_add(tw.lc.doevalstep)
    Gtk.main()
"""
_ACTION_STACK_START = """\
def %s():
"""
_START_STACK_START_ADD = """\
    tw.start_plugins()
    global global_objects,turtles,canvas,logo
    global_objects = tw.get_global_objects()
    turtles = tw.turtles
    canvas = tw.canvas
    logo = tw.lc
    logo.boxes = BOX
"""
_ACTION_STACK_PREAMBLE = """\
    turtle = turtles.get_active_turtle()
"""
_ACTION_STACK_END = """\
ACTION["%s"] = %s
"""
# character that is illegal in a Python identifier
PAT_IDENTIFIER_ILLEGAL_CHAR = re.compile("[^A-Za-z0-9_]")


def save_python(tw):
    """ Find all the action stacks and turn each into Python code """
    all_blocks = tw.just_blocks()
    blocks_name = []
    for block in all_blocks:
        blocks_name.append(block.name)

    if 'start' not in blocks_name:
        return None

    blocks_covered = set()
    tops_of_stacks = []
    for block in all_blocks:
        if block not in blocks_covered:
            top = find_top_block(block)
            tops_of_stacks.append(top)
            block_stack = find_group(top)
            blocks_covered.update(set(block_stack))

    snippets = [_SETUP_CODE_START]

    for k in plugins_in_use:
        snippets.append('%s = None\n' % (k.lower(),))

    snippets.append('\n')

    for block in tops_of_stacks:
        stack_name = get_stack_name(block)
        if stack_name:
            pythoncode = _action_stack_to_python(block, tw, name=stack_name)
            snippets.append(pythoncode)
            snippets.append(linesep)
    snippets.append(_SETUP_CODE_END)
    return ''.join(snippets)


def _action_stack_to_python(block, tw, name='start'):
    """ Turn a stack of blocks into Python code
    name -- the name of the action stack (defaults to "start") """

    if isinstance(name, int):
        name = float(name)
    if not isinstance(name, str):
        name = str(name)

    # traverse the block stack and get the AST for every block
    ast_list = _walk_action_stack(block, tw.lc)
    if not ast_list or not isinstance(ast_list[-1], ast.Yield):
        ast_list.append(ast_yield_true())
    action_stack_ast = ast.Module(body=ast_list)

    # serialize the ASTs into python code
    generated_code = codegen.to_source(action_stack_ast)

    # wrap the action stack setup code around everything
    name_id = _make_identifier(name)
    if name == 'start':
        pre_preamble = _START_STACK_START_ADD
        for k in plugins_in_use:
            pre_preamble += '    global %s\n' % (k.lower(),)
            pre_preamble += "    %s = global_objects['%s']\n" % (k.lower(), k)
    else:
        pre_preamble = ''
    generated_code = _indent(generated_code, 1)
    if generated_code.endswith(linesep):
        newline = ''
    else:
        newline = linesep
    snippets = [_ACTION_STACK_START % (name_id),
                pre_preamble,
                _ACTION_STACK_PREAMBLE,
                generated_code,
                newline,
                _ACTION_STACK_END % (name, name_id)]
    return ''.join(snippets)


def _walk_action_stack(top_block, lc, convert_me=True):
    """ Turn a stack of blocks into a list of ASTs
    convert_me -- convert values and Primitives to ASTs or return them
        unconverted? """
    block = top_block

    # value blocks don't have a primitive
    # (but constant blocks (colors, screen dimensions, etc.) do)
    if block.is_value_block():
        raw_value = block.get_value(add_type_prefix=False)
        if convert_me:
            value_ast = value_to_ast(raw_value)
            if value_ast is not None:
                return [value_ast]
            else:
                return []
        else:
            if raw_value is not None:
                return [raw_value]
            else:
                return []

    def _get_prim(block):
        prim = lc.get_prim_callable(block.primitive)
        # fail gracefully if primitive is not a Primitive object
        if not isinstance(prim, Primitive):
            raise PyExportError(_('block is not exportable'), block=block)
        return prim

    prim = _get_prim(block)

    ast_list = []
    arg_asts = []

    def _finish_off(block, prim=None):
        """ Convert block to an AST and add it to the ast_list. Raise a
        PyExportError on failure. """
        if prim is None:
            prim = _get_prim(block)
        if convert_me:
            if prim.export_me:
                try:
                    new_ast = prim.get_ast(*arg_asts)
                except ValueError:
                    traceback.print_exc()
                    raise PyExportError(_('error while exporting block'),
                                        block=block)
                if isinstance(new_ast, (list, tuple)):
                    ast_list.extend(new_ast)
                elif new_ast is not None:
                    ast_list.append(new_ast)
            elif arg_asts:  # TODO do we ever get here?
                new_ast = ast.List(elts=arg_asts, ctx=ast.Load)
                ast_list.append(new_ast)
        else:
            ast_list.append((prim, ) + tuple(arg_asts))

    # skip the very first dock/ connection - it's either the previous block or
    # the return value of this block
    dock_queue = block.docks[1:]
    conn_queue = block.connections[1:]
    while dock_queue and conn_queue:
        dock = dock_queue.pop(0)
        conn = conn_queue.pop(0)
        if conn is None or dock[0] == 'unavailable':
            continue
        elif not dock_queue and dock[0] == 'flow':
            # finish off this block
            _finish_off(block, prim)
            arg_asts = []
            # next block
            block = conn
            prim = _get_prim(block)
            dock_queue = block.docks[1:]
            conn_queue = block.connections[1:]
        else:
            # embedded stack of blocks (body of conditional or loop) or
            # argument block
            if dock[0] == 'flow':
                # body of conditional or loop
                new_arg_asts = _walk_action_stack(conn, lc,
                                                  convert_me=convert_me)
                if prim == LogoCode.prim_loop and not \
                        isinstance(new_arg_asts[-1], ast.Yield):
                    new_arg_asts.append(ast_yield_true())
                arg_asts.append(new_arg_asts)
            else:
                # argument block
                new_arg_asts = _walk_action_stack(conn, lc, convert_me=False)
                arg_asts.append(*new_arg_asts)

    # finish off last block
    _finish_off(block, prim)

    return ast_list


def _make_identifier(name):
    """ Turn name into a Python identifier name by replacing illegal
    characters """
    replaced = re.sub(PAT_IDENTIFIER_ILLEGAL_CHAR, '_', name)
    # TODO find better strategy to avoid number at beginning
    if re.match('[0-9]', replaced):
        replaced = '_' + replaced
    return replaced


def _indent(code, num_levels=1):
    """ Indent each line of code with num_levels * 4 spaces
    code -- some python code as a (multi-line) string """
    indentation = " " * (4 * num_levels)
    line_list = code.split(linesep)
    new_line_list = []
    for line in line_list:
        new_line_list.append(indentation + line)
    return linesep.join(new_line_list)
