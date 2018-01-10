# Copyright (c) 2010, Loic Fejoz
# Copyright (c) 2010, Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


class RtfException(Exception):
    pass


plaintext = 1
control = 2
argument = 3
backslash = 4
escapedChar = 5


class RtfParser(object):

    def __init__(self, unicode=False):
        self.state = plaintext
        self.arg = ''
        self.token = ''
        self.unicode = unicode
        self.par = False
        self.output = ''

    def getChar(self, code):
        """ called when an escaped char is found """
        return chr(code)

    def getNonBreakingSpace(self):
        return ' '

    def pushState(self):
        pass

    def popState(self):
        pass

    def putChar(self):
        pass

    def doControl(self, token, arg):
        pass

    def feed(self, txt):
        for c in txt:
            self.feedChar(c)

    def feedChar(self, char):
        if self.state == plaintext:  # this is just normal user content
            if char == '\\':
                self.state = backslash
            elif char == '{':
                self.pushState()
            elif char == '}':
                self.popState()
            else:
                self.putChar(char)
        elif self.state == backslash:  # a command or escape
            if char == '\\' or char == '{' or char == '}':
                self.putChar(char)
                self.state = plaintext
            else:
                if char.isalpha() or char in ('*', '-', '|'):
                    self.state = control
                    self.token = char
                elif char == "'":
                    self.state = escapedChar
                    self.escapedChar = ''
                elif char in ['\\', '{', '}']:
                    self.putChar(char)
                    self.state = plaintext
                elif char == "~":  # non breaking space
                    self.putChar(self.getNonBreakingSpace())
                    self.state = plaintext
                else:
                    raise RtfException(('unexpected %s after \\' % char))
        elif self.state == escapedChar:
            self.escapedChar = self.escapedChar + char
            if len(self.escapedChar) == 2:
                char = self.getChar(int(self.escapedChar, 16))
                self.putChar(char)
                self.state = plaintext
        elif self.state == control:  # collecting the command token
            if char.isalpha():
                self.token = self.token + char
            elif char.isdigit() or char == '-':
                self.state = argument
                self.arg = char
            else:
                self.doControl(self.token, self.arg)
                self.state = plaintext
                if char == '\\':
                    self.state = backslash
                elif char == '{':
                    self.pushState()
                elif char == '}':
                    self.popState()
                else:
                    if not char.isspace():
                        self.putChar(char)
        elif self.state == argument:  # collecting the optional argument
            if char.isdigit():
                self.arg = self.arg + char
            else:
                self.state = plaintext
                self.doControl(self.token, self.arg)
                if char == '\\':
                    self.state = backslash
                elif char == '{':
                    self.pushState()
                elif char == '}':
                    self.popState()
                else:
                    if not char.isspace():
                        self.putChar(char)


class RtfTextOnly(RtfParser):

    def __init__(self):
        RtfParser.__init__(self)
        self.level = 0

    def pushState(self):
        self.level = self.level + 1

    def popState(self):
        self.level = self.level - 1

    def putChar(self, ch):
        if self.par:
            self.output += ch

    def doControl(self, token, arg):
        if token[0:3] == 'par':
            self.par = True
        pass
