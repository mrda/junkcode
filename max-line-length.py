#!/bin/env python
#
# max-line-length.py - find the maximum line length from a text file of strings
#
# Copyright (C) Michael Davies <michael@the-davies.net>
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

def find_longest_string(filename):
    max_len = 0
    with open(filename,'r') as f:
        for line in f:
            length = len(line)
            if length > max_len:
                max_len = length
    return max_len

if __name__ == '__main__':
    for file in sys.argv[1:]:
        print '{} {}'.format(file, find_longest_string(file))
