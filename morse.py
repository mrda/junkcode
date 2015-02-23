#!/usr/bin/env python
#
# morse.py - Convert the input string to morse code, or do the inverse
#
# Copyright (C) 2015 Michael Davies (michael@the-davies.net)
#
# e.g. Encoding example:
# mrda@carbon:~/src/python$ ./morse.py hello
# . . . .   .   . - . .   . - . .   - - -       -   . . . .   .   . - .   .
#
# e.g. Decoding example
# mrda@carbon:~/src/python$ ./morse.py dec ". . . .   .   . - . .   . - . .   - - -       -   . . . .   .   . - .   ." # noqa
# hello there
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
import os
import sys
import string

LETTER_SPACE = ' ' * 3
WORD_SPACE = ' ' * 7

table = {
    'a': '. -',
    'b': '- . . .',
    'c': '- . - .',
    'd': '- . .',
    'e': '.',
    'f': '. . - .',
    'g': '- - .',
    'h': '. . . .',
    'i': '. .',
    'j': '. - - -',
    'k': '- . -',
    'l': '. - . .',
    'm': '- -',
    'n': '- .',
    'o': '- - -',
    'p': '. - - .',
    'q': '- - . -',
    'r': '. - .',
    's': '. . .',
    't': '-',
    'u': '. . -',
    'v': '. . . -',
    'w': '. - -',
    'x': '- . . -',
    'y': '- . - -',
    'z': '- - . .',
    '1': '. - - - -',
    '2': '. . - - -',
    '3': '. . . - -',
    '4': '. . . . -',
    '5': '. . . . .',
    '6': '- . . . .',
    '7': '- - . . .',
    '8': '- - - . .',
    '9': '- - - - .',
    '0': '- - - - -',
    ' ': WORD_SPACE,
}


def encode(words):
    str = ' '.join(x for x in words)
    encoded = LETTER_SPACE.join(x for x in [table[x.lower()]
                                for x in list(str)])
    # Remove superfluous gaps before a space.
    return string.replace(encoded,
                          LETTER_SPACE + WORD_SPACE + LETTER_SPACE,
                          WORD_SPACE)


def decode(s):
    final = ""
    str = ''.join(x for x in s)
    for word in string.split(str, WORD_SPACE):
        letters = string.split(word, LETTER_SPACE)
        dec_word = ""
        for letter in letters:
            dec_letter = ([key for key, value in table.items()
                          if value == letter][0])
            dec_word += dec_letter
        final += dec_word + " "
    return final.rstrip()


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        progname = os.path.basename(__file__)
        sys.exit('Usage: %s [dec|decode] <data>' % progname)
    elif (sys.argv[1] == "enc") or (sys.argv[1] == "encode"):
        print encode(sys.argv[2:])
    elif (sys.argv[1] == "dec") or (sys.argv[1] == "decode"):
        print decode(sys.argv[2:])
    else:
        print encode(sys.argv[1:])
