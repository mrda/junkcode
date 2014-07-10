#!/usr/bin/env python
#
# fibonacci.py - standard fibonacci number generator
# Copyright (C) 2005 Michael Davies <michael@the-davies.net>
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
import sys
from os.path import basename

def fibonacci(n):
    results = []
    x, y = 0, 1
    for i in range(n):
        results.append(x)
        x, y = y, x+y
    return results

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("%s: Please specify the number of fibonacci numbers "
               "you require" % basename(sys.argv[0]))
    else:
        print(" ".join(str(x) for x in fibonacci(int(sys.argv[1]))))
