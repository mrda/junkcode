#!/usr/bin/env python3
#
# simple_text_encoder.py - just an example of how a simple encoding
#                          mechanism could work.
#
# For example, "aaaaabccc" could be encoded "a5b1c3"
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
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
# 02111-1307, USA.#
#

import os
import string
import sys


def encode(s):
    lastchar = None
    count = 0
    output = ""
    for i, ch in enumerate(s):
        if lastchar is None:
            lastchar = ch
            count = 1
            continue
        if ch != lastchar:
            output += lastchar + str(count)
            lastchar = ch
            count = 1
        else:
            count += 1
    output += lastchar + str(count)
    return output


def decode(s):
    lastchar = None
    last_char_was_digit = False
    output = ""
    num = 0
    for c in s:
        if c in string.ascii_letters:
            if last_char_was_digit:
                output += lastchar * num
                num = 0
            lastchar = c
            last_char_was_digit = False
        elif c in string.digits:
            if last_char_was_digit:
                num *= 10
            num += int(c)
            last_char_was_digit = True
    output += lastchar * num
    return output


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        progname = os.path.basename(__file__)
        sys.exit('Usage: %s [encode|decode] <data>' % progname)
    elif sys.argv[1] == "encode":
        print(encode(sys.argv[2]))
    elif sys.argv[1] == "decode":
        print(decode(sys.argv[2]))
    else:
        print(encode(sys.argv[1]))
