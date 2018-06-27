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
import os
import sys


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


def print_usage():
    print("{}: <roman or arabic number>".format(os.path.basename(__file__)))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
    else:
        print(convert_roman_arabic(sys.argv[1]))
