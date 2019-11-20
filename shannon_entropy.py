#!/usr/bin/env python
#
# shannon_entropy.py - calculate the Shannon Entropy for a given string
#
# See https://en.wikipedia.org/wiki/Entropy_(information_theory)
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

import math
import sys


def entropy(s):
    "Calculates the Shannon entropy of a string."

    # Calculate the probability of each char in string
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]

    # Calculate the entropy
    e = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return e


def ideal_entropy(s):
    "Calculates the ideal Shannon entropy of a string with given length"
    length = len(s)
    prob = 1.0 / length
    return (-1.0 * length * prob * math.log(prob) / math.log(2.0))


if __name__ == '__main__':
    for s in sys.argv[1:]:
        shannon = entropy(s)
        ideal = ideal_entropy(s)
        goodness = 100 * shannon / ideal
        print("{}: {:.2f} (ideal: {:.2f} {:.0f}%)".
              format(s, shannon, ideal, goodness))
