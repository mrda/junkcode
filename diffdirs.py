#!/usr/bin/env python
#
# diffdirs.py - find files that are missing between directories. This is for
#               verifying backups. Note that it's directional, we only
#               care about files in <sourcedir> that's not in <targetdir>.
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

from find_content import find_files
import find_content
import os
import sys

debug = False


def print_usage():
    progname = os.path.basename(__file__)
    print "%s <sourcedir> <destdir>" % progname


def diff_dirs(debug, source_dir, target_dir):
    if debug:
        print("Verifying that all the content files in \"" +
              source_dir + "\" is in \"" + target_dir + "\"")
    sdir = []
    sdir.append(source_dir)
    tdir = []
    tdir.append(target_dir)

    source_filelist = find_files(sdir,
                                 find_content.DEFAULT_EXCLUDE_DIRS,
                                 find_content.DEFAULT_EXTENSIONS,
                                 False)

    target_filelist = find_files(tdir,
                                 find_content.DEFAULT_EXCLUDE_DIRS,
                                 find_content.DEFAULT_EXTENSIONS,
                                 True)

    missing_files = []

    for elem in source_filelist:
        found = False
        if debug:
            sys.stdout.write('.')

        for dest in target_filelist:
            if dest == elem[1]:
                found = True

        if not found:
            missing_files.append(elem)

    return missing_files


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
    else:
        missing = diff_dirs(debug, sys.argv[1], sys.argv[2])
        if debug:
            print("")
            print("Missing files are:")
        if missing:
            for e in missing:
                print os.path.join(e[0], e[1])
