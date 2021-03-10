#!/usr/bin/python
#
# rle.py - Run length encoding
#
# Copyright (C) 2021 Michael Davies (michael@the-davies.net)
#
# e.g. Encoding example:
# $ ./rle.py Hello There
# 1H1e2l1o1 1W1o1r1l1d
#
# e.g. Decoding example
# $ ./rle.py dec 5a3t8h
# aaaaattthhhhhhhh
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


def encode(strings):
    encoded = ''
    prev_char = ''
    count = 1

    if not strings: return ''
    data = ' '.join(s for s in strings)

    for char in data:
        if char != prev_char:
            if prev_char:
                encoded += str(count) + prev_char
            count = 1
            prev_char = char
        else:
            count += 1
    else:
        encoded += str(count) + prev_char
        return encoded


def decode(strings):
    data = ' '.join(s for s in strings)
    decoded = ''
    count = ''
    for char in data:
        if char.isdigit():
            count += char
        else:
            decoded += char * int(count)
            count = ''
    return decoded


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        progname = os.path.basename(__file__)
        sys.exit('Usage: %s [enc|encode|dec|decode] string(s)' % progname)
    elif (sys.argv[1] == "enc") or (sys.argv[1] == "encode"):
        print(encode(sys.argv[2:]))
    elif (sys.argv[1] == "dec") or (sys.argv[1] == "decode"):
        print(''.join(s for s in decode(sys.argv[2:])))
    else:
        print(encode(sys.argv[1:]))
