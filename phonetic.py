#!/usr/bin/env python
#
# phonetic.py - Spell out the input string to the NATO phoentic alphabet,
#               or do the inverse
#
# Copyright (C) 2007 Michael Davies (michael@the-davies.net)
#
# e.g. Encoding example:
# mrda@carbon:~/src/python$ ./phonetic.py vc107
# victor charlie one zero seven
#
# e.g. Decoding example
# mrda@carbon:~/src/python$ ./phonetic.py dec "victor charlie one zero seven"
# vc107
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
import re
import sys
import string

def encode(strings):
    # nested string comprehension, I love python :-)
    return " space ".join([" ".join([_enc(string.lower(ch)) for ch in list(str)]) for str in strings])

def _enc(ch):
    if (ch) == 'a':
        return 'alpha'
    elif (ch) == 'b':
        return 'bravo'
    elif (ch) == 'c':
        return 'charlie'
    elif (ch) == 'd':
        return 'delta'
    elif (ch) == 'e':
        return 'echo'
    elif (ch) == 'f':
        return 'foxtrot'
    elif (ch) == 'g':
        return 'golf'
    elif (ch) == 'h':
        return 'hotel'
    elif (ch) == 'i':
        return 'india'
    elif (ch) == 'j':
        return 'juliet'
    elif (ch) == 'k':
        return 'kilo'
    elif (ch) == 'l':
        return 'lima'
    elif (ch) == 'm':
        return 'mike'
    elif (ch) == 'n':
        return 'november'
    elif (ch) == 'o':
        return 'oscar'
    elif (ch) == 'p':
        return 'papa'
    elif (ch) == 'q':
        return 'quebec'
    elif (ch) == 'r':
        return 'romeo'
    elif (ch) == 's':
        return 'sierra'
    elif (ch) == 't':
        return 'tango'
    elif (ch) == 'u':
        return 'uniform'
    elif (ch) == 'v':
        return 'victor'
    elif (ch) == 'w':
        return 'whiskey'
    elif (ch) == 'x':
        return 'xray'
    elif (ch) == 'y':
        return 'yankee'
    elif (ch) == 'z':
        return 'zulu'
    elif (ch) == '1':
        return 'one'
    elif (ch) == '2':
        return 'two'
    elif (ch) == '3':
        return 'three'
    elif (ch) == '4':
        return 'four'
    elif (ch) == '5':
        return 'five'
    elif (ch) == '6':
        return 'six'
    elif (ch) == '7':
        return 'seven'
    elif (ch) == '8':
        return 'eight'
    elif (ch) == '9':
        return 'nine'
    elif (ch) == '0':
        return 'zero'
    elif (ch) == ' ':
        return 'space'
    else:
        return ch

def decode(strings):
    # nested string comprehension, I love python :-)
    return " ".join(["".join([_dec(atom) for atom in str.split()]) for str in strings])

def _dec(ch):
    if (ch) == 'alpha':
        return 'a'
    elif (ch) == 'bravo':
        return 'b'
    elif (ch) == 'charlie':
        return 'c'
    elif (ch) == 'delta':
        return 'd'
    elif (ch) == 'echo':
        return 'e'
    elif (ch) == 'foxtrot':
        return 'f'
    elif (ch) == 'golf':
        return 'g'
    elif (ch) == 'hotel':
        return 'h'
    elif (ch) == 'india':
        return 'i'
    elif (ch) == 'juliet':
        return 'j'
    elif (ch) == 'kilo':
        return 'k'
    elif (ch) == 'lima':
        return 'l'
    elif (ch) == 'mike':
        return 'm'
    elif (ch) == 'november':
        return 'n'
    elif (ch) == 'oscar':
        return 'o'
    elif (ch) == 'papa':
        return 'p'
    elif (ch) == 'quebec':
        return 'q'
    elif (ch) == 'romeo':
        return 'r'
    elif (ch) == 'sierra':
        return 's'
    elif (ch) == 'tango':
        return 't'
    elif (ch) == 'uniform':
        return 'u'
    elif (ch) == 'victor':
        return 'v'
    elif (ch) == 'whiskey':
        return 'w'
    elif (ch) == 'xray':
        return 'x'
    elif (ch) == 'yankee':
        return 'y'
    elif (ch) == 'zulu':
        return 'z'
    elif (ch) == 'one':
        return '1'
    elif (ch) == 'two':
        return '2'
    elif (ch) == 'three':
        return '3'
    elif (ch) == 'four':
        return '4'
    elif (ch) == 'five':
        return '5'
    elif (ch) == 'six':
        return '6'
    elif (ch) == 'seven':
        return '7'
    elif (ch) == 'eight':
        return '8'
    elif (ch) == 'nine':
        return '9'
    elif (ch) == 'zero':
        return '0'
    elif (ch) == 'space':
        return ' '
    else:
        return ch

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        pass
    elif (sys.argv[1] == "enc") or (sys.argv[1] == "encode"):
        print encode(sys.argv[2:])
    elif (sys.argv[1] == "dec") or (sys.argv[1] == "decode"):
        print decode(sys.argv[2:])
    elif (sys.argv[0] == "deimify.py"):
        print decode(sys.argv[1:])
    else:
        print encode(sys.argv[1:])
