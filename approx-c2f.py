#!/usr/bin/env python
#
# approx-c2f.py - approximate Celcius to Fahrenheit conversion
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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

import os
import sys


def approx_celcius_to_fahrenheit(celcius):
    """Approximate Celcius to Fahrenheit conversion.

    1) Double the Celcius value, i.e. 25C -> 50
    2) Subtract the first digit, i.e. 50-5 -> 45
    3) Add 32, i.e. 45 + 32 -> 77F"""

    double = celcius * 2
    s = str(double)
    return float(double - int(s[0]) + 32)


def celcius_to_fahrenheit(celcius):
    return (9.0/5 * celcius) + 32


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("Usage: {} <temp-in-fahrenheit>".format(
                 os.path.basename(sys.argv[0])))

    celcius = int(sys.argv[1])
    approx = approx_celcius_to_fahrenheit(celcius)
    actual = celcius_to_fahrenheit(celcius)

    print("{}C is approximately {}F (actual conversion is {}F)".format(
          celcius, approx, actual))
