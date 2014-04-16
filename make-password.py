#!/usr/bin/env python
#
# make-password.py - generate a human-readable password
#                    Inspired by "correct horse battery staple"
#                    (ref http://xkcd.com/936/)
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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
from __future__ import print_function

import os
import random
import sys


def find_words(num_words, max_length):
    # Get a bunch of words from the system
    f = open('/usr/share/dict/words')
    words = [x.strip() for x in f.readlines()]
    f.close()
    # Only include words that aren't too long
    # since my memory isn't that good :)
    candidates = []
    for word in words:
        if len(word) <= max_length:
            candidates.append(word)
    chosen = []
    # Choose the number of words required
    for i in range(num_words):
        chosen.append(random.choice(candidates))
    return chosen


def generate_password(num_words, max_word_len, max_digits):
    # Generate a password consisting of words separated by hyphens
    password = '-'.join(find_words(num_words, max_word_len)).capitalize()
    # Remove pesky aprostrophes
    password = password.replace("'", "")
    # Add a random number to the end
    password += str(random.randint(1, max_digits))
    return password


def _print_usage_and_exit(code):
        msg = ("Usage: %s [number-of-passwords-to-be-generated]"
               % os.path.basename(sys.argv[0]))
        print(msg, file=sys.stderr)
        sys.exit(code)


if __name__ == '__main__':

    # Default number of passwords to generate
    num_passwds = 10

    # Default number of words to include in password
    num_words = 3

    # Default word length to include in password
    word_length = 7

    # Default maximum integer to append to the end
    max_number = 999

    # Allow number of passwords to be generated to be overwritten
    if len(sys.argv) == 2:
        try:
            num_passwds = int(sys.argv[1])
        except:
            _print_usage_and_exit(1)
    elif len(sys.argv) > 2:
        _print_usage_and_exit(2)

    for i in xrange(num_passwds):
        print(generate_password(num_words, word_length, max_number))
