#!/usr/bin/env python
#
# fizzbuzz11.py - standard interview question solution from
#   "Coding Horror" - See
#   http://blog.codinghorror.com/why-cant-programmers-program/
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#
from __future__ import print_function
import sys


def fizzbuzz(start, end):
    for i in range(start, end):
        divthree = i % 3 == 0
        divfive = i % 5 == 0
        if not divthree and not divfive:
            print(i)
            continue
        if divthree:
            print("Fizz", end="")
        if divfive:
            print("Buzz", end="")
        print()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    else:
        start = 1
        end = 100
    fizzbuzz(start, end)
