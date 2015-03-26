#!/usr/bin/env python
#
# pyfinddefs.py - find all the classes and methods in a file or directory
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

import re
import sys
import os


def _check_file(filename):
    match = '^\s*(def\s)|(class\s)'
    anymatch = False
    print '*** {0} ***\n'.format(filename)
    for line in open(filename):
        if re.match(match, line):
            anymatch = True
            print line,
    if anymatch:
        print('')


def find_defs(things):
    file_match = '.*\.py$'
    for thing in things:
        if os.path.isdir(thing):
            thing = thing.strip('/')
            find_defs(['{0}/{1}'.format(thing, i) for i in os.listdir(thing)])
        else:
            file_result = re.match(file_match, thing)
            if file_result:
                _check_file(thing)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        filelist = '.'
    else:
        filelist = sys.argv[1:]
    find_defs(filelist)
