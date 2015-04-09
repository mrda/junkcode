#!/usr/bin/env python
#
# ski-ramp - print out the strings provided in a ski-ramp.
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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
import argparse
import sys


def build_ski_ramp(strs, reverse=False):
    strs.sort(key=len, reverse=reverse)
    return '\n'.join(x for x in strs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--descending",
                        help="print out the ski-ramp in descending order",
                        action='store_true', default=False)
    parser.add_argument("--skiier",
                        help="adds a skiier",
                        action='store_true', default=False)
    args, rest = parser.parse_known_args(sys.argv)
    if args.skiier:
        print("     _   ")
        print("  __(_)  ")
        print(" / / /\  ")
        print("/  `\\\\ | ")
        print("  \\\// | ")
        print("   \\\\   ")
        print("    \\\\  ")
    print build_ski_ramp(rest[1:], args.descending)
