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
import re
import sys

thedict = []

def load_dict():
    """Load up the system dictionary"""
    num = 0
    with open('/usr/share/dict/words', 'r', encoding="utf-8") as dictfile:
        for line in dictfile:
            word = line.strip().lower()
            if len(word) == 5:
                thedict.append(word)
                num += 1
    if args.verbose:
        print(f"Initial dictionary has a total of {num} five letter words")

def contains_all(strng, setofchars):
    """Does strng contain all of the chars in setofchars?"""
    for char in setofchars:
        if char not in strng:
            return 0
    return 1

parser = argparse.ArgumentParser(
    description='Find possible matches for wordle.',
    epilog='You can find Wordle here: https://www.powerlanguage.co.uk/wordle/')
parser.add_argument('--letters', type=str, dest='letters',
                    help="Known letters")
parser.add_argument('--matches', type=str, dest='matches',
                    help="Known letter positions, e.g. ....t is a 5 letter"
                         " word ending in 't'")
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    dest='verbose',
                    help='Display extra information')
args = parser.parse_args()

load_dict()
thedict = list(set(thedict))  # Remove dups because there's a bug in my code

if args.letters is None and args.matches is None:
    for entry in thedict:
        print(entry)
else:

    # We have a couple of options:
    #  --letters xyz
    #  --matches ..x..
    #  --letters xyz --matches ..x..

    # Let's try the regex first, from --matches
    if args.matches is not None:

        # Sanity
        if len(args.matches) != 5:
            print("Error: Match string must be 5 chars long. Exiting...")
            sys.exit(1)

        # Build up the match string
        MATCH_RE = "^"
        for ch in args.matches:
            if ch == '.':
                MATCH_RE += "[a-z]"
            else:
                MATCH_RE += "[" + ch + "]"
        MATCH_RE += "$"

        reduced_words = []
        COUNT = 0
        for possibility in thedict:
            if re.match(MATCH_RE, possibility):
                reduced_words.append(possibility)
                COUNT += 1
        if args.verbose:
            print(f"Using regular expression '{MATCH_RE}' reduces possibile "
                  f"matches down to {COUNT}.")
        thedict = reduced_words

    # Now let's remove any entries that don't have all of the --letters
    if args.letters is not None:
        restricted_matches = []
        COUNT = 0
        for entry in thedict:
            if contains_all(entry, args.letters):
                restricted_matches.append(entry)
                COUNT += 1
        thedict = restricted_matches
        if args.verbose:
            print(f"Checking required letters '{args.letters}' reduces possible "
                  f"matches down to {COUNT} matches.")

    if args.verbose:
        print("Candidate words:")
    for possibility in thedict:
        print(possibility)
