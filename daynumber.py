#!/usr/bin/python
#
# daynumber.py - Display the current day number
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
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
import datetime
import os
import sys

if len(sys.argv) == 1:
    current_date = datetime.date.today()
elif len(sys.argv) != 4:
    sys.exit("Usage: {} [<year> <month> <day>]".format
             (os.path.basename(sys.argv[0])))
else:
    current_date = datetime.date(int(sys.argv[1]),
                                 int(sys.argv[2]),
                                 int(sys.argv[3]))

print((current_date - datetime.date(current_date.year, 1, 1)).days + 1)
