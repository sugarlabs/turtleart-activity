#Copyright (c) 2011, Walter Bender

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

#
# This procedure is invoked when the user-definable block on the "extras"
# palette is selected.

def myblock(lc, arg):
    ''' Add a uturn block to the 'turtle' palette '''
    from TurtleArt.tapalette import make_palette
    from TurtleArt.talogo import primitive_dictionary
    from gettext import gettext as _
    palette = make_palette('turtle')

    palette.add_block('uturn',
                      style='basic-style-extended-vertical',
                      label=_('uturn'),
                      prim_name='uturn',
                      help_string=_('make a uturn'))
    lc.tw.lc.def_prim('uturn', 0,
                     lambda self: primitive_dictionary['set'](
            'heading', lc.tw.canvas.seth,
            lc.tw.canvas.heading + 180))

    lc.tw.show_toolbar_palette(0, regenerate=True)
