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
import os
import re
import string
import sys

DEFAULT_WORD_LEN = 5
DEFAULT_DICT_FILE = "/usr/share/dict/words"
MY_DICT_FILE = ".wordle/words"

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

def regex_reduce(mydict, matchstr, antimatch=False, verbose=False):
    """ Return the dictionary based upon the supplied matchstr.
        matchstr is a pseudo-regex, i.e. ..o.. is a 5 letter word with
        an o in the 3rd spot.  antimatch determines whether this is a
        pattern we want or not want"""

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
    if verbose:
        print(f"Using regex '{match_re}' reduces possibilities "
              f"to {matches} words.")
    return reduced_words

def load_dict(word_len, use_system_dict, verbose):
    """Load up the dictionary.  Use ~/.wordle/words if exists,
    otherwise use the system dictionary, unless use_system_dict
    is specified."""

    # Prefer the user's private dictionary, unless overriden
    dictionary_filename = DEFAULT_DICT_FILE
    if not use_system_dict:
        home = os.environ.get('HOME')
        if home:
            fname = f"{home}/{MY_DICT_FILE}"
            if os.path.isfile(fname) and os.access(fname, os.R_OK):
                dictionary_filename = fname

    num = 0
    thedict = []
    with open(dictionary_filename, 'r', encoding="utf-8") as dictfile:
        for line in dictfile:
            word = line.strip().lower()
            if len(word) == word_len and only_az(word):
                thedict.append(word)
                num += 1
    if verbose:
        print(f"Using dictionary '{dictionary_filename}'.")
        print(f"Dictionary has a total of {num} five letter words")
    return thedict

def build_freqtable(mydict):
    """Build and return a sorted frequency table for the supplied dictionary"""
    ftable = {}
    for word in mydict:
        for char in word:
            if char in ftable:
                ftable[char] += 1
            else:
                ftable[char] = 1
    return ftable

def wordle(mydict, include=None, exclude=None, match=None, antimatch=None, verbose=False):
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
        if verbose:
            print(f"Removing words that contain any of "
                  f"[{exclude}] reduces candidates to "
                  f"{count} words.")

    # Remove any entries that don't have all of the --include letters
    if include:
        restricted_matches = []
        count = 0
        for entry in mydict:
            if contains_all(entry, include):
                restricted_matches.append(entry)
                count += 1
        mydict = restricted_matches
        if verbose:
            print(f"Only including words that contain [{include}] reduces "
                  f"candidates to {count} words.")

    # Try and find a regex --match for correctly positioned letters
    if match:
        mydict = regex_reduce(mydict, match, antimatch=False, verbose=verbose)

    # Let's remove candidates according to the --antimatch regular expression
    if antimatch:
        mydict = regex_reduce(mydict, antimatch, antimatch=True,
                              verbose=verbose)

    # Print out the candidates
    if verbose:
        print("Candidate words:")
    mydict.sort()
    return mydict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Find possible matches for wordle.',
                epilog='You can find Wordle here: https://www.powerlanguage.co.uk/wordle/')
    parser.add_argument('-f', '--frequency',
                        action='store_true',
                        dest='frequency_table',
                        help="display a frequency table for your dictionary, then exit")
    parser.add_argument('-g', '--guess',
                        action='store_true',
                        dest='guess',
                        help="display a  good starting guess, then exit")
    parser.add_argument('-D', '--system-dict',
                        action='store_true',
                        dest='use_system_dict',
                        help="Use the system dictionary instead of ~/.wordle/words")
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='display extra information')
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
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)


    # Sanity checks

    # If match and antimatch are provided, they need to be args.word_len long
    if (args.match and len(args.match) != args.word_len or
        args.antimatch and len(args.antimatch) != args.word_len):
        print(f"Error: Match string must be {args.word_len} chars long. "
              f"Exiting...")
        sys.exit(1)

    # Included letters must be shorter than args.word_len
    if args.include and len(args.include) > args.word_len:
        print(f"Error: You can't have more than {args.word_len} included "
              f"letters. Exiting...")
        sys.exit(1)

    # Included letters and excluded letters must not overlap
    if (args.include and args.exclude
        and list(set(args.include) & set(args.exclude))):

        print(f"Error: Included letters [{args.include}] and excluded "
              f"letters [{args.exclude}] must not overlap. Exiting...")
        sys.exit(1)

    # TODO(mrda): Fix duplicate entry bug in load_dict
    dictionary = list(set(load_dict(args.word_len, args.use_system_dict,
                                    args.verbose)))
    freqtable = build_freqtable(dictionary)

    # Print a frequency table and exit
    if args.frequency_table:
        if args.verbose:
            print("Dictionary frequency table:")
        total = 0
        for fchar in freqtable:
            total += int(freqtable[fchar])
        for fchar in sorted(freqtable, key=freqtable.get, reverse=True):
            print(f"'{fchar}' appears {freqtable[fchar]} times ({freqtable[fchar]/total:.2%})")
        sys.exit(0)

    # print a good starting guess and exit
    NUMTOPLETTERS = 4
    if args.guess:
        if args.verbose:
            print(f"Starting words based on the {NUMTOPLETTERS} highest "
                  f"frequency letters in your dictionary:")
        sfreqtable = sorted(freqtable, key=freqtable.get, reverse=True)
        TOPLETTERS = "".join(x for x in sfreqtable)[0:NUMTOPLETTERS]
        for guessword in wordle(dictionary, TOPLETTERS, None, None, None, False):
            print(guessword)
        sys.exit(0)

    # Find matching wordle words
    for candidate in wordle(dictionary, args.include, args.exclude,
                            args.match, args.antimatch, args.verbose):
        print(candidate)
