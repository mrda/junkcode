#!/usr/bin/env python
#
# to_bin.py - A very simple script to turn strings into
#             an 8-bit ASCII binary representation
#
# Copyright (C) 2014 Michael Davies (michael@the-davies.net)
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
import sys

def to_bin(strings):
    result = ""
    for strng in strings:
        result += (' '.join(format(ord(x), '08b') for x in strng))
        result += ' '
    return result

if __name__ == "__main__":
    print to_bin(sys.argv[1:])
