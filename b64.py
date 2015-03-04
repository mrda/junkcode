#!/usr/bin/env python
#
# b64.py - Base64 encode or decode
#
# Copyright (C) 2015 Michael Davies (michael@the-davies.net)
#
# e.g. Encoding example:
# mrda@carbon:~/src/python$ ./b64.py "Hello There"
# SGVsbG8gVGhlcmU=
#
# e.g. Decoding example
# mrda@carbon:~/src/python$ ./b64.py dec SGVsbG8gVGhlcmU=
# Hello There
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
import base64
import os
import sys


def encode(strings):
    return base64.b64encode(' '.join(s for s in strings))


def decode(strings):
    final = []
    for s in strings:
        final.append(base64.b64decode(s))
    return final


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        progname = os.path.basename(__file__)
        sys.exit('Usage: %s [enc|encode|dec|decode] string(s)' % progname)
    elif (sys.argv[1] == "enc") or (sys.argv[1] == "encode"):
        print encode(sys.argv[2:])
    elif (sys.argv[1] == "dec") or (sys.argv[1] == "decode"):
        print ' '.join(s for s in decode(sys.argv[2:]))
    else:
        print encode(sys.argv[1:])
