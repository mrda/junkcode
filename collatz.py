#!/usr/bin/env python
#
# collatz.py - Test the Collatz conjecture
#              See http://en.wikipedia.org/wiki/Collatz_conjecture
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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
import os


def collatz(n, dump=False):
    if dump:
        print n,
    if (n <= 1):
        return True
    elif (n % 2 == 0):
        return collatz(n/2, dump)
    else:
        return collatz(3*n + 1, dump)


if __name__ == '__main__':
    usage = False
    if len(sys.argv) == 1:
        n = range(1, 10)
    elif len(sys.argv) == 2:
        try:
            n = [int(sys.argv[1])]
        except ValueError:
            usage = True
    else:
        usage = True

    if usage:
        exit("Usage: %s [n]" % os.path.basename(__file__))

    for i in n:
        print(collatz(i, True))
