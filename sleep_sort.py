#!/usr/bin/env python3
#
# sleep_sort.py - A unique approach to sorting numbers :-)
#                 Usage: sleep_sort.py 6 1 9 7
#                 1
#                 6
#                 7
#                 9
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
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
# 02111-1307, USA.#
#

import os
import sys
import time


def my_child(sec):
    time.sleep(sec)
    print(sec)


def sleep_sort(arr):
    for i in arr:
        try:
            pid = os.fork()
        except OSError:
            exit("Could not create a child process")

        if pid == 0:
            my_child(i)
            exit()

    for i in arr:
        finished = os.waitpid(0, 0)


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        progname = os.path.basename(__file__)
        sys.exit('Usage: %s <array of numbers to sort>' % progname)
    else:
        arr = [int(x) for x in sys.argv[1:]]
        sleep_sort(arr)
