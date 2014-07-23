#!/usr/bin/env python
#
# from_bin.py - A very simple script to turn 8-bit binary
#               strings into ACSII strings
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


def from_bin(strings):
    inp = ' '.join(strings)
    return ''.join(chr(int(inp[i:i+8], 2)) for i in xrange(0, len(inp), 8))

if __name__ == "__main__":
    print from_bin(sys.argv[1:])
