#!/usr/bin/env python3
#
# colorize.py - Colorize a string, which is probably a password.
#               Print a string to STDOUT with per-char ANSI colors.
#               Yes, it would be better to read from STDIN but
#               this isn't really written with security in mind.
#
# Copyright (C) 2026 Michael Davies <michael@the-davies.net>
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
import string
import sys

RED = "\033[31m"
BLUE = "\033[34m"
WHITE = "\033[37m"
GREEN = "\033[32m"
RESET = "\033[0m"


def color_for(char: str) -> str:
    if char.isdigit():
        return RED
    if char in string.punctuation:
        return BLUE
    if "a" <= char <= "z" or "A" <= char <= "Z":
        return WHITE
    return GREEN


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <string>", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    for char in text:
        sys.stdout.write(f"{color_for(char)}{char}")
    sys.stdout.write(f"{RESET}\n")


if __name__ == "__main__":
    main()
