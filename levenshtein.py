#!/usr/bin/env python
#
# levenshtein - calculate the Levenshtein distance between two strings
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
import os
import sys


def levenshtein(first_str, second_str, first_idx=None,
                second_idx=None):
    if first_idx is None:
        first_idx = len(first_str)
    if second_idx is None:
        second_idx = len(second_str)

    if first_idx == 0:
        return second_idx
    if second_idx == 0:
        return first_idx

    if first_str[first_idx-1] == second_str[second_idx-1]:
        cost = 0
    else:
        cost = 1

    return min(levenshtein(first_str, second_str, first_idx-1, second_idx) + 1,
               levenshtein(first_str, second_str, first_idx, second_idx-1) + 1,
               levenshtein(first_str, second_str, first_idx-1,
                           second_idx-1) + cost)


if __name__ == '__main__':

    progname = os.path.basename(__file__)
    if len(sys.argv) == 2 and sys.argv[1] == "test":

        import unittest

        class TestLevenshtein(unittest.TestCase):

            def test_simple(self):
                self.assertEqual(3, levenshtein('Saturday', 'Sunday'))
                self.assertEqual(1, levenshtein('Suzie', 'Susie'))

            def test_symmetry(self):
                self.assertEqual(3, levenshtein('kitten', 'sitting'))
                self.assertEqual(3, levenshtein('sitting', 'kitten'))

            def test_emptyness(self):
                self.assertEqual(4, levenshtein('', 'fred'))
                self.assertEqual(4, levenshtein('fred', ''))

        unittest.main()

    elif len(sys.argv) != 3:
        sys.exit('Usage: %s first-string second-string' % progname)

    print("The Levenshtein distance between '%s' and '%s' is %s" %
          (sys.argv[1], sys.argv[2], levenshtein(sys.argv[1], sys.argv[2])))
