#!/usr/bin/env python
#
# phonetic.py - Spell out the input string to the NATO phoentic alphabet,
#               or do the inverse
#
# Copyright (C) 2007,2019 Michael Davies (michael@the-davies.net)
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
    return " space ".join([" ".join([_enc(ch) for ch in list(str)]) for str in strings])

def _enc(ch):
    phon = __enc(ch.lower())
    if ch in string.ascii_uppercase:
        return "capital-" + phon
    return phon

def __enc(ch):
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
    return "".join(["".join([_dec(atom) for atom in str.split()]) for str in strings])

def _dec(s):
    splits = s.split('-')
    if len(splits) == 2:
        return __dec(splits[1]).upper()
    return __dec(s)

def __dec(s):
    if (s) == 'alpha':
        return 'a'
    elif (s) == 'bravo':
        return 'b'
    elif (s) == 'charlie':
        return 'c'
    elif (s) == 'delta':
        return 'd'
    elif (s) == 'echo':
        return 'e'
    elif (s) == 'foxtrot':
        return 'f'
    elif (s) == 'golf':
        return 'g'
    elif (s) == 'hotel':
        return 'h'
    elif (s) == 'india':
        return 'i'
    elif (s) == 'juliet':
        return 'j'
    elif (s) == 'kilo':
        return 'k'
    elif (s) == 'lima':
        return 'l'
    elif (s) == 'mike':
        return 'm'
    elif (s) == 'november':
        return 'n'
    elif (s) == 'oscar':
        return 'o'
    elif (s) == 'papa':
        return 'p'
    elif (s) == 'quebec':
        return 'q'
    elif (s) == 'romeo':
        return 'r'
    elif (s) == 'sierra':
        return 's'
    elif (s) == 'tango':
        return 't'
    elif (s) == 'uniform':
        return 'u'
    elif (s) == 'victor':
        return 'v'
    elif (s) == 'whiskey':
        return 'w'
    elif (s) == 'xray':
        return 'x'
    elif (s) == 'yankee':
        return 'y'
    elif (s) == 'zulu':
        return 'z'
    elif (s) == 'one':
        return '1'
    elif (s) == 'two':
        return '2'
    elif (s) == 'three':
        return '3'
    elif (s) == 'four':
        return '4'
    elif (s) == 'five':
        return '5'
    elif (s) == 'six':
        return '6'
    elif (s) == 'seven':
        return '7'
    elif (s) == 'eight':
        return '8'
    elif (s) == 'nine':
        return '9'
    elif (s) == 'zero':
        return '0'
    elif (s) == 'space':
        return ' '
    else:
        return s

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        pass
    elif (sys.argv[1] == "enc") or (sys.argv[1] == "encode"):
        print(encode(sys.argv[2:]))
    elif (sys.argv[1] == "dec") or (sys.argv[1] == "decode"):
        print(decode(sys.argv[2:]))
    elif (sys.argv[0] == "phonetic.py"):
        print(decode(sys.argv[1:]))
    else:
        print(encode(sys.argv[1:]))
