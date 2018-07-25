#!/usr/bin/env python
#
# pert - calculate a PERT estimate from 3 estimates
#           * best case,
#           * most optimistic, and
#           * worst case
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
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


def calculate_pert(optimistic, most_likely, worst):
    return (optimistic + (4 * most_likely) + worst) / 6.0


def exit_with_usage(code=1):
    progname = os.path.basename(__file__)
    sys.stderr.write("Usage: {} optimistic most_likely worst\n"
                     .format(progname))
    sys.exit(code)


if __name__ == '__main__':
    try:
        if len(sys.argv) != 4:
            exit_with_usage(1)

        optimistic = float(sys.argv[1])
        most_likely = float(sys.argv[2])
        worst = float(sys.argv[3])

        if (most_likely < optimistic) or (worst < most_likely):
            exit_with_usage(2)

        print("{:.2f}".format(calculate_pert(optimistic, most_likely, worst)))

    except ValueError:
        exit_with_usage(3)
