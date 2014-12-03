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


""" Extend the `ast` module to include comments """

import ast


class ExtraCode(ast.stmt):

    """Adds extra content to a primitive needed in Python code, e.g.,
    changes to the turtle (e.g., prim_turtle) require the addition of
    turtle = turtles.get_active_turtle()
    Extends the Python abstract grammar by the following: stmt
    = ExtraContent(string text) | ... """

    _fields = ('text')

    def __init__(self, text="", lineno=1, col_offset=0):
        """ text -- the textual content of the comment, i.e. everything
            directly following the hashtag until the next newline """
        self.text = text
        self.lineno = lineno
        self.col_offset = col_offset


class Comment(ast.stmt):

    """ An inline comment, starting with a hashtag (#).
    Extends the Python abstract grammar by the following:
    stmt = Comment(string text) | ... """

    _fields = ('text')

    def __init__(self, text="", lineno=1, col_offset=0):
        """ text -- the textual content of the comment, i.e. everything
            directly following the hashtag until the next newline """
        self.text = text
        self.lineno = lineno
        self.col_offset = col_offset


class LambdaWithStrBody(ast.Lambda):

    """ Lambda AST whose body is a simple string (not ast.Str).
    Extends the Python abstract grammar by the following:
    expr = LambdaWithStrBody(string body_str, expr* args) | ... """

    def __init__(self, body_str="", args=[], lineno=1, col_offset=0):
        self.body_str = body_str
        self.args = args
        self.lineno = lineno
        self.col_offset = col_offset
