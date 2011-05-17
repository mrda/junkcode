#!/usr/bin/env python
#
# find-project-name.py - Search the dictionary for words that contain
#                        the characters provided on the command-line
#                        aka "smb" finds "samba".  Useful for finding
#                        new project names from acronyms etc.
#
# Copyright (C) 2008.  All Rights Reserved.
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
import sys
import re
if __name__ == "__main__":
    if (len(sys.argv) == 1):
        pass
    else:
        reg = "(.)*?".join(ch for ch in list(sys.argv[1]))
        regexp = "(.)*?"+reg+"(.)*?"
        p = re.compile(regexp)
        for line in open('/usr/share/dict/words', 'r'):
            m = p.match(line)
            if m:
                line = line.rstrip()
                print line

