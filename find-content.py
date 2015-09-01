#!/usr/bin/env python
#
# find-content.py - find files specified, specify --help to
#                   get usage information
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

import argparse
import fnmatch
import os
import six
import sys


# Defaults

# Note(mrda): The motivation here is iTunes library scraping :)
DEFAULT_EXTENSIONS = ['jpg', 'png', 'cr2', 'mov']
DEFAULT_DIRS = ['.']
DEFAULT_EXCLUDE_DIRS = ['Previews', 'Thumbnails']

# End Defaults

debug = True


def find_files(directories, exclude_dirs, exts, files_only):
    matches = []
    extensions = []
    for ex in exts:
        extensions.append(ex)
        extensions.append(ex.upper())

    for directory in directories:
        for root, dirnames, filenames in os.walk(directory, topdown=True):
            prune = False
            for excl_dir in exclude_dirs:
                if excl_dir in dirnames:
                    dirnames.remove(excl_dir)
                    prune = True
            if not prune:
                for extension in extensions:
                    for filename in fnmatch.filter(filenames, '*.'+extension):
                        if files_only:
                            result = filename
                        else:
                            result = (root, filename)
                        matches.append(result)
    if matches is not None:
        matches.sort()
    return matches

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        help='Internal debugging flag',
                        action='store_true',
                        default=False)

    parser.add_argument('--files-only',
                        help='Only return files found, not full path',
                        action='store_true',
                        default=False)

    parser.add_argument('-x', '--exclude-dir',
                        help='Directories to exclude in searching',
                        action='append',
                        nargs=1)

    parser.add_argument('-e', '--extension',
                        help='Extension to look for',
                        action='append',
                        nargs=1)

    args, rest = parser.parse_known_args(sys.argv)

    if len(rest) == 1:
        directories = DEFAULT_DIRS
    else:
        directories = rest[1:]

    if args.exclude_dir is None or args.exclude_dir == [[]]:
        exclude_dirs = DEFAULT_EXCLUDE_DIRS
    else:
        exclude_dirs = []
        for d in args.exclude_dir:
                for elem in d:
                    if os.sep not in elem:
                        exclude_dirs.append(elem)

    if args.extension is None or args.extension == [[]]:
        extensions = DEFAULT_EXTENSIONS
    else:
        extensions = []
        for e in args.extension:
            for elem in e:
                if os.sep not in elem:
                    extensions.append(elem)

    if args.debug:
        print "Looking in directories " + str(directories)
        print "But not in directories that match " + str(exclude_dirs)
        print "For files with extenstions " + str(extensions)
        print "and we're looking for files only? " + str(args.files_only)

    matches = find_files(directories, exclude_dirs, extensions,
                         args.files_only)
    for match in matches:
        if isinstance(match, six.string_types):
            print match
        else:
            print os.path.join(match[0], match[1])
