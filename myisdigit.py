#!/usr/bin/env python
#
# myisdigit.py - naive reimplementation of isdigit(), with unit tests and
#                timing tests for demo purposes
#
# Copyright (C) 2020 Michael Davies <michael@the-davies.net>
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

# Predefine what characters are considered digits
_ok_chars = " ".join(str(n) for n in range(0, 10))


def myisdigit(strng):
    global _ok_chars
    for i in strng:
        if i not in _ok_chars:
            return False
    return True


if __name__ == '__main__':

    import prettytable
    import random
    import string
    import timeit

    print("--- Unit test for myisdigit")
    test_data = ['0', '1', '5', '9', 'a', 'm', 'z', '-', '.', '%', '"',
                 '+', '\u03B2', '\u00B1', '\u1f4a9']

    pt = prettytable.PrettyTable()
    pt.field_names = ['character', 'isdigit()', 'myisdigit()', 'agree?']
    for f in pt.field_names:
        pt.align[f] = 'l'

    for j in test_data:
        isdigit_result = j.isdigit()
        myisdigit_result = myisdigit(j)
        pt.add_row([j, isdigit_result, myisdigit_result,
                    isdigit_result == myisdigit_result])
    print(pt)

    # Now let's do some timing tests comparing this reimplementation
    # with the library function
    print("--- Timing tests for myisdigit")

    # We don't do this as setup code, as we want the sample_data to
    # be the same for both timeit tests
    sample_data = "".join(random.choice(string.ascii_lowercase +
                                        string.digits))

    myisdigit_test_code = '''
from __main__ import myisdigit
from __main__ import sample_data
for k in sample_data:
    result = myisdigit(k)
    '''

    isdigit_test_code = '''
from __main__ import sample_data
for k in sample_data:
    result = k.isdigit()
    '''

    repeat = 3
    number = 10000
    myisdigit_time = timeit.repeat(setup="",
                                   stmt=myisdigit_test_code,
                                   repeat=repeat,
                                   number=number)
    isdigit_time = timeit.repeat(setup="",
                                 stmt=isdigit_test_code,
                                 repeat=repeat,
                                 number=number)

    quickest_myisdigit_time = min(myisdigit_time)
    quickest_isdigit_time = min(isdigit_time)
    print("myisdigit time: {}".format(quickest_myisdigit_time))
    print("isdigit time: {}".format(quickest_isdigit_time))
    print("myisdigit() is about {}x slower than isdigit()".format(
        int(quickest_myisdigit_time / quickest_isdigit_time)))
