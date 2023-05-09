#!/usr/bin/env python
#
# xkcd213.py - determine the 'acceptable' age range of people you can date
#              See https://xkcd.com/314/
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


def exit_with_usage():
    sys.exit(f"Usage: {os.path.basename(sys.argv[0])} [age]")


if len(sys.argv) == 1:
    age = int(input("Enter your age: "))
elif len(sys.argv) == 2:
    if sys.argv[1].isdigit():
        age = int(sys.argv[1])
try:
    age
except NameError:
    exit_with_usage()

youngest = int((age / 2) + 7)
oldest = (age - 7) * 2

print(f"As a {age} year-old, you can date people between {youngest}"
      f" and {oldest} without it being creepy")
