#!/usr/bin/env python
#
# fizzbuzz2.py - standard interview question solution from
#   "Coding Horror" - See
#   http://blog.codinghorror.com/why-cant-programmers-program/
#
# Copyright (C) 2017 Michael Davies <michael@the-davies.net>
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


def fizzbuzz(n):
    for i in range(1, n+1):
        fizz = ((i % 3) == 0)
        buzz = ((i % 5) == 0)
        if fizz:
            print('Fizz', end='')
        if buzz:
            print('Buzz', end='')
        if ((not fizz) and (not buzz)):
            print(i, end='')
        print('')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    else:
        n = 100
    fizzbuzz(n)
