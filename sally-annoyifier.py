#!/usr/bin/env python
#
# sally-annoyifier.py - randomise a time reporting string, for Sally
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
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
import os
import random
import sys


def _get_project_names():
    home = os.environ.get('HOME')
    if not home:
        print("%s: ${HOME} not defined" % os.path.basename(sys.argv[0]))
        print("Exiting...")
        sys.exit(1)
    filename = home + "/.project-names"
    try:
        fd = open(filename, 'r')
        return [line.rstrip() for line in fd]
    except (OSError, IOError) as e:
        print("%s: %s" % (os.path.basename(sys.argv[0]), e))
        print("Please create this file, with one project name per line")
        print("Exiting...")
        sys.exit(2)

if __name__ == '__main__':
    pn = _get_project_names()
    random.shuffle(pn)
    print("COP-29: %s standup" % ','.join(pn))
