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
""" Provide potential solutions for Wordle """

import argparse
import re
import string
import sys

DEFAULT_WORD_LEN = 5

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

def regex_reduce(mydict, matchstr, antimatch=False):
    """ Return the dictionary based upon the supplied matchstr.
        matchstr is a pseudo-regex, i.e. ..o.. is a 5 letter word with
        an o in the 3rd spot.  antimatch determines whether this is a
        pattern we want or not want"""

    # Sanity check
    if len(matchstr) != args.word_len:
        print(f"Error: Match string must be {args.word_len} chars long. "
              f"Exiting...")
        sys.exit(1)

    # Build up the match string
    match_re = "^"
    for char in matchstr:
        if char == '.':
            match_re += "[a-z]"
        else:
            if antimatch:
                match_re += "[^"
            match_re += char
            if antimatch:
                match_re += "]"
    match_re += "$"

    reduced_words = []
    matches = 0
    for possible_match in mydict:
        if re.match(match_re, possible_match):
            reduced_words.append(possible_match)
            matches += 1
    if args.verbose:
        print(f"Using regular expression '{match_re}' reduces possibile "
              f"matches down to {matches} words.")
    return reduced_words

def load_dict():
    """Load up the system dictionary"""
    num = 0
    thedict = []
    with open('/usr/share/dict/words', 'r', encoding="utf-8") as dictfile:
        for line in dictfile:
            word = line.strip().lower()
            if len(word) == args.word_len and only_az(word):
                thedict.append(word)
                num += 1
    if args.verbose:
        print(f"Initial dictionary has a total of {num} five letter words")
    return thedict

def wordle(mydict, include=None, exclude=None, match=None, antimatch=None):
    """ Find wordle candidate words, using the provided dictionary 'mydict'.
    include is a string of letters that must be in the word
    exclude is a string of letters that must NOT be in the word
    match is a pseudo-regex on letters in the correct places,
      i.e. ..o.. is a 5 letter word with an o in the 3rd spot.
    antimatch is a pseudo-regex on letters that must NOT be in a certain slot.
      i.e. .a... is a 5 letter word that mustn't have an 'a' in the 2nd slot."""

    # Let's remove words with --exclude letters
    if exclude:
        excluded_matches = []
        count = 0
        for entry in mydict:
            if not contains_any(entry, exclude):
                excluded_matches.append(entry)
                count += 1
        mydict = excluded_matches
        if args.verbose:
            print(f"Removing words that contain letters "
                  f"'{exclude}' reduces possible matches down to "
                  f"{count} words.")

    # Remove any entries that don't have all of the --include letters
    if include:
        # Sanity check
        if len(include) > args.word_len:
            print(f"Error: You can't have more than {args.word_len} included "
                  f"letters. Exiting...")
            sys.exit(1)

        restricted_matches = []
        count = 0
        for entry in mydict:
            if contains_all(entry, include):
                restricted_matches.append(entry)
                count += 1
        mydict = restricted_matches
        if args.verbose:
            print(f"Requiring this set of letters '{include}' reduces "
                  f"possible matches down to {count} words.")

    # Try and find a regex --match for correctly positioned letters
    if match:
        mydict = regex_reduce(mydict, match, antimatch=False)

    # Let's remove candidates according to the --antimatch regular expression
    if antimatch:
        mydict = regex_reduce(mydict, antimatch, antimatch=True)

    # Print out the candidates
    if args.verbose:
        print("Candidate words:")
    mydict.sort()
    return mydict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Find possible matches for wordle.',
                epilog='You can find Wordle here: https://www.powerlanguage.co.uk/wordle/')
    parser.add_argument('-e', '--exclude', type=str, dest='exclude',
                        help="letters to be excluded")
    parser.add_argument('-i', '--include', type=str, dest='include',
                        help="letters to be included")
    parser.add_argument('-m', '--match', type=str, dest='match',
                        help="known letter positions, e.g. ....t is a 5 letter"
                        " word ending in 't'")
    parser.add_argument('-a', '--antimatch', type=str, dest='antimatch',
                        help="where certain letters aren't, e.g. ...o. is a 5 letter"
                             " word, and the 4th letter isn't a 'o'")
    parser.add_argument('-n', '--numchars', type=int, dest='word_len',
                        default=DEFAULT_WORD_LEN,
                        help=f"word length to consider, "
                        f"default to {DEFAULT_WORD_LEN}")
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='display extra information')
    args = parser.parse_args()

    if (args.include is None and
        args.match is None and
        args.antimatch is None and
        args.exclude is None):

        parser.print_help()
        sys.exit(0)

    # TODO(mrda): Fix duplicate entry bug in load_dict
    dictionary = list(set(load_dict()))

    for candidate in wordle(dictionary, args.include, args.exclude,
                            args.match, args.antimatch):
        print(candidate)
