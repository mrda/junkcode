#!/usr/bin/env python
#
# roman.py - Convert to/from Roman Digits.  Another little programming
#            hiring challenge.
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#
from __future__ import print_function
import getopt
import os
import sys
import unittest


valid_opts = ['help', 'self-test', 'verbose']


roman_numbers = {
    'I': 1,
    'IV': 4,
    'V': 5,
    'IX': 9,
    'X': 10,
    'XL': 40,
    'L': 50,
    'XC': 90,
    'C': 100,
    'CD': 400,
    'D': 500,
    'CM': 900,
    'M': 1000,
}

roman_numbers_by_value = sorted(roman_numbers.items(),
                                key=lambda v: v[1],
                                reverse=True)


def convert_arabic(number):
    result = ""
    number = int(number)
    for idx in roman_numbers_by_value:
        rnum = idx[0]
        anum = int(idx[1])
        while number >= anum:
            result += rnum
            number -= anum
    return result


def is_subtraction_digit(digit):
    return digit in ['I', 'X', 'C']


def follow_on_digit(number, idx):
    return idx != len(number)-1


def convert_roman(number):
    # TODO(mrda): Add invalid number check
    result = 0
    skip = False
    for idx, roman_digit in enumerate(number):
        if skip:
            skip = False
            continue
        if is_subtraction_digit(roman_digit) and follow_on_digit(number, idx):
            rdig = roman_digit + number[idx+1]
            if rdig in roman_numbers:
                converted_digit = roman_numbers[rdig]
                skip = True
            else:
                converted_digit = roman_numbers[roman_digit]
                skip = False
        else:
            converted_digit = roman_numbers[roman_digit]
            skip = False
        result = result + converted_digit
    return result


def is_roman(number):
    # TODO(mrda): Add invalid number check
    for digit in number:
        if digit not in roman_numbers:
            return False
    return True


def is_arabic(number):
    return number.isdigit()


def convert_roman_arabic(number):
    if is_roman(number):
        return convert_roman(number)
    elif is_arabic(number):
        return convert_arabic(number)
    else:
        return "Unknown number format"


def exit_with_usage(code=1):
    sys.stderr.write("Usage: {0} [{1}] <roman or arabic number>\n"
                     .format(os.path.basename(sys.argv[0]),
                             '|'.join('--'+opt for opt in valid_opts)))
    sys.exit(code)


#
# Tests
#

class TestRoman(unittest.TestCase):

    def test_roman_simple(self):
        self.assertEqual(1, convert_roman('I'))
        self.assertEqual(4, convert_roman('IV'))
        self.assertEqual(5, convert_roman('V'))
        self.assertEqual(9, convert_roman('IX'))
        self.assertEqual(10, convert_roman('X'))
        self.assertEqual(40, convert_roman('XL'))
        self.assertEqual(50, convert_roman('L'))
        self.assertEqual(90, convert_roman('XC'))
        self.assertEqual(100, convert_roman('C'))
        self.assertEqual(400, convert_roman('CD'))
        self.assertEqual(500, convert_roman('D'))
        self.assertEqual(900, convert_roman('CM'))
        self.assertEqual(1000, convert_roman('M'))

    def test_roman_tricky(self):
        self.assertEqual(99, convert_roman('XCIX'))
        self.assertEqual(999, convert_roman('CMXCIX'))

    def test_symmetric(self):
        for i in range(1, 5000):
            first = convert_arabic(i)
            second = convert_roman(first)
            self.assertEqual(i, second)

    def test_roman_years(self):
        self.assertEqual(1982, convert_roman('MCMLXXXII'))
        self.assertEqual(2000, convert_roman('MM'))

    def test_arabic_years(self):
        self.assertEqual('LVI', convert_arabic(56))
        self.assertEqual('MMXVIII', convert_arabic(2018))

    def test_identity(self):
        self.assertFalse(is_arabic('XXX'))
        self.assertFalse(is_roman('1979'))
        self.assertTrue(is_roman('XXX'))
        self.assertTrue(is_arabic('1979'))

    def test_incorrect_roman(self):
        self.assertFalse(is_roman('IC'))
        self.assertEqual("Unknown number format", convert_roman('IC'))


if __name__ == '__main__':

    runtests = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', valid_opts)
    except getopt.error:
        exit_with_usage()

    opt_flags = [flag for (flag, val) in opts]
    for opt in opt_flags:
        if opt == '--verbose':
            print("verbsoing")
            debug = True
        elif opt == '--help':
            exit_with_usage(code=0)
        elif opt == '--self-test':
            runtests = True

    if runtests:
        del sys.argv[1:]
        if args:
            print("Ignoring arguments, and just running tests")
        unittest.main()
        sys.exit(0)

    if len(args) != 1:
        exit_with_usage()
    else:
        print(convert_roman_arabic(args[0]))
