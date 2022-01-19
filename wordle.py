#!/usr/bin/env python
#
# wordle.py - find possible wordle matches
#
# Copyright (C) 2022.  All Rights Reserved.
# Michael Davies <michael@the-davies.net>
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
""" Display Wordle matches """

import argparse

thedict = []

def load_dict():
    """Load up the system dictionary"""
    with open('/usr/share/dict/words', 'r', encoding="utf-8") as dictfile:
        for line in dictfile:
            word = line.strip().lower()
            if len(word) == 5:
                thedict.append(word)

def contains_all(strng, setofchars):
    """Does strng contain all of the chars in setofchars?"""
    for char in setofchars:
        if char not in strng:
            return 0
    return 1

parser = argparse.ArgumentParser(
    description='Find possible matches for wordle.',
    epilog='You can find Wordle here: https://www.powerlanguage.co.uk/wordle/')
parser.add_argument('--letters', type=str, dest='letters', help="The known letters")
args = parser.parse_args()

load_dict()
thedict = list(set(thedict))  # Remove dups because there's a bug in my code
MATCHES = 0

if args.letters is None:
    for entry in thedict:
        print(entry)
        MATCHES = MATCHES + 1
else:
    for entry in thedict:
        if contains_all(entry, args.letters):
            print(entry)
            MATCHES = MATCHES + 1
print(f"There are a total of {MATCHES} matches")
