#!/usr/bin/env python
#
# select-name.py - select a name using a stupid but well-defined algorithm
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
import collections
import hashlib
import operator
import os
import random
import sys


def _get_names():
    home = os.environ.get('HOME')
    if not home:
        print "%s: ${HOME} not defined" % os.path.basename(sys.argv[0])
        print "Exiting..."
        sys.exit(1)
    filename = home + "/.names"
    try:
        fd = open(filename, 'r')
        return [line.rstrip() for line in fd]
    except (OSError, IOError) as e:
        print "%s: %s" % (os.path.basename(sys.argv[0]), e)
        print "Exiting..."
        sys.exit(2)


def shortest_item(items):
    return (sorted(items, key=len), "Sorting by shortest item first")


def longest_item(items):
    return (sorted(items, key=len, reverse=True),
            "Sorting by longest item first")


def alphabetical(items):
    return (sorted(items), "Sorting alphabetical")


def reverse_alphabetical(items):
    return (sorted(items, reverse=True), "Sorting reverse alphabetical")


def sorted_sha1_hash(items):
    temp = {}
    for item in items:
        temp[item] = hashlib.sha1(item).hexdigest()
    return (sorted(temp, key=temp.get), "Sorting by SHA-1 hash")


def sorted_md5_hash(items):
    temp = {}
    for item in items:
        temp[item] = hashlib.md5(item).hexdigest()
    return (sorted(temp, key=temp.get), "Sorting by MD5 hash")


def reverse_item_sort(items):
    temp = {}
    for item in items:
        temp[item] = item[::-1]  # string reverse
    return (sorted(temp, key=temp.get),
            "Sorting by reverse item alphabetical")


_algorithms = {'shortest_item': shortest_item,
               'longest_item': longest_item,
               'alphabetical': alphabetical,
               'reverse_alphabetical': reverse_alphabetical,
               'sorted_sha1_hash': sorted_sha1_hash,
               'sorted_md5_hash': sorted_md5_hash,
               'reverse_item_sort': reverse_item_sort}


if __name__ == '__main__':
    if len(sys.argv) == 1:
        #algorithm = random.randint(0, len(_algorithms)-1)
        algorithm = random.sample(_algorithms, 1)[0]
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'list':
            print("Available algorithms are:")
            for alg in _algorithms.keys():
                print("  %s" % alg)
            sys.exit(0)
        elif sys.argv[1] == 'help':
            algorithm = 'help'
        else:
            algorithm = sys.argv[1]
    else:
        algorithm = 'help'

    try:
        names, display = _algorithms[algorithm](_get_names())
    except KeyError:
        algorithm = 'help'

    if algorithm == 'help':
        progname = os.path.basename(__file__)
        sys.exit('usage: %s [help | list | <algorithm>]' % progname)

    print('<<<< %s >>>>' % display)
    for name in names:
        print(name)
