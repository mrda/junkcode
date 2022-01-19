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
import string
import sys

thedict = []

def only_az(word):
    """Does word only contain characters in [a..z]?"""
    for char in word:
        if char not in string.ascii_lowercase:
            return False
    return True

def contains_all(strng, setofchars):
    """Does strng contain all of the chars in setofchars?"""
    for char in setofchars:
        if char not in strng:
            return False
    return True

def contains_any(strng, setofchars):
    """Does strng contain any of the chars in setofchars?"""
    for char in setofchars:
        if char in strng:
            return True
    return False

def load_dict():
    """Load up the system dictionary"""
    num = 0
    with open('/usr/share/dict/words', 'r', encoding="utf-8") as dictfile:
        for line in dictfile:
            word = line.strip().lower()
            if len(word) == 5 and only_az(word):
                thedict.append(word)
                num += 1
    if args.verbose:
        print(f"Initial dictionary has a total of {num} five letter words")

parser = argparse.ArgumentParser(
    description='Find possible matches for wordle.',
    epilog='You can find Wordle here: https://www.powerlanguage.co.uk/wordle/')
parser.add_argument('--exclude', type=str, dest='exclude',
                    help="letters to be excluded")
parser.add_argument('--include', type=str, dest='include',
                    help="letters to be included")
parser.add_argument('--match', type=str, dest='match',
                    help="known letter positions, e.g. ....t is a 5 letter"
                         " word ending in 't'")
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    dest='verbose',
                    help='display extra information')
args = parser.parse_args()

load_dict()
thedict = list(set(thedict))  # Remove dups because there's a bug in my code

if (args.include is None and
    args.match is None and
    args.exclude is None):

    thedict.sort()
    for entry in thedict:
        print(entry)
else:

    # Any or all of the --include, --match, and --exclude might be present

    # Let's remove words with --exclude letters
    if args.exclude:
        excluded_matches = []
        COUNT = 0
        for entry in thedict:
            if not contains_any(entry, args.exclude):
                excluded_matches.append(entry)
                COUNT += 1
        thedict = excluded_matches
        if args.verbose:
            print(f"Removing words that contain letters "
                  f"'{args.exclude}' reduces possible matches down to "
                  f"{COUNT} words.")

    # Remove any entries that don't have all of the --include letters
    if args.include:

        # Sanity check
        if len(args.include) > 5:
            print("Error: You can't have more than 5 included letters. Exiting...")
            sys.exit(1)

        restricted_matches = []
        COUNT = 0
        for entry in thedict:
            if contains_all(entry, args.include):
                restricted_matches.append(entry)
                COUNT += 1
        thedict = restricted_matches
        if args.verbose:
            print(f"Requiring this set of letters '{args.include}' reduces "
                  f"possible matches down to {COUNT} words.")

    # Try and find a regex match for correctly positioned letters
    if args.match:

        # Sanity check
        if len(args.match) != 5:
            print("Error: Match string must be 5 chars long. Exiting...")
            sys.exit(1)

        # Build up the match string
        MATCH_RE = "^"
        for ch in args.match:
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
                  f"matches down to {COUNT} words.")
        thedict = reduced_words

    # Print out the candidates
    if args.verbose:
        print("Candidate words:")
    thedict.sort()
    for possibility in thedict:
        print(possibility)
