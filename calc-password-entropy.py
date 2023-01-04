#!/usr/bin/env python
#
# calc-password-entropy.py [password] - calculate password entropy for a
#                                       supplied password
#
# Copyright (C) 2023 Michael Davies <michael@the-davies.net>
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
import math
import os
import string
import sys


min_entropy = 100  # Seems like a reasonable value in 2023


def calc_entropy(pw):
    used_lower = False
    used_upper = False
    used_digits = False
    used_punctuation = False
    poolsize = 0

    extended_punctuation = string.punctuation + " " + "\t"

    # TODO: Need to reduce the entropy pool for common letter<->number
    #       substitutions and first word capitals to give a more realistic
    #       idea of entropy
    for ch in pw:
        if ch in string.ascii_lowercase:
            if not used_lower:
                poolsize += len(string.ascii_lowercase)
                used_lower = True
        elif ch in string.ascii_uppercase:
            if not used_upper:
                poolsize += len(string.ascii_uppercase)
                used_upper = True
        elif ch in string.digits:
            if not used_digits:
                poolsize += len(string.digits)
                used_digits = True
        elif ch in extended_punctuation:
            if not used_punctuation:
                poolsize += len(extended_punctuation)
                used_punctuation = True
        else:
            print(f"BUG: This software can't handle a '{ch}' character")
            return 0

    entropy = len(pw) * math.log2(poolsize)
    return entropy


if __name__ == '__main__':

    if len(sys.argv) == 1:
        # No arguments, prompt for password
        pw = input("Enter the password to calculate entropy for: ")

    elif len(sys.argv) == 2:
        # One argument - the password
        pw = sys.argv[1]

    else:
        print(f"Usage: {os.path.basename(sys.argv[0])} [password]")
        sys.exit(1)

    entropy = calc_entropy(pw)

    print(f"Password length is {len(pw)}")
    print(f"Calculated entropy is {entropy:.2f}")
    if entropy < min_entropy:
        print("WARNING: Your password hasn't enough entropy. "
              "Choose a longer, more random password")
