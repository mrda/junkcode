#!/usr/bin/env python
#
# fizzbuzz8.py - standard interview question solution from
#   "Coding Horror" - See
#   http://blog.codinghorror.com/why-cant-programmers-program/
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
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
        mod3 = i % 3 == 0
        mod5 = i % 5 == 0
        if mod3 or mod5:
            if mod3:
                print("Fizz", end="")
            if mod5:
                print("Buzz")
            else:
                print()
        else:
            print(i)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    else:
        start = 1
        end = 100
    fizzbuzz(start, end)
