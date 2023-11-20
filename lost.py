#!/usr/bin/env python
#
# lost.py [nth] - return the nth number in the number sequence
#                 from the TV Show 'Lost'.
#
#                 See also https://oeis.org/A104101 and
#                 https://oeis.org/A122115
#
# Copyright (C) 2023 Michael Davies <michael@the-davies.net>
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

import sys
import os


def lost(n):
    return lost_num(n+2)


def lost_num(n):
    if n <= 0:
        return 0
    elif n == 1:
        return -3
    elif n == 2:
        return -1
    elif n == 3:
        return 4
    elif n == 4:
        return 8
    elif n == 5:
        return 15
    else:
        return lost_num(n-1) + lost_num(n-3) + lost_num(n-5)


def exit_with_usage():
    sys.exit(f"Usage: {os.path.basename(sys.argv[0])} [nth]"
             f" - return the nth lost number.")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        for i in range(1, 7):
            print(lost(i), end=' ')
    elif len(sys.argv) == 2:
        try:
            print(lost(int(sys.argv[1])))
        except ValueError:
            exit_with_usage()
    else:
        exit_with_usage()
