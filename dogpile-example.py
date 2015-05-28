#!/usr/bin/env python
#
# dogpile-example.py - An example of how to use dogpile.cache
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
import appdirs
import dogpile.cache
import sys


AUTHOR = 'openstack'
PROGNAME = 'python-ironicclient'

dirname = appdirs.user_cache_dir(PROGNAME, AUTHOR)


if __name__ == '__main__':

    region = dogpile.cache.make_region().configure(
        'dogpile.cache.dbm',
        expiration_time=10,
        arguments={
            "filename": dirname + "/version-cache.dbm"
        }
    )

    if len(sys.argv) == 1:
        print "You need to provide one of get, set or delete"
        sys.exit(1)

    if sys.argv[1] == 'get':
        if len(sys.argv) != 3:
            print "You need 2 arguments for get"
            sys.exit(1)
        val = region.get(sys.argv[2])
        if val == dogpile.cache.api.NO_VALUE:
            print "No value stored for %s" % sys.argv[2]
        else:
            print "%s == %s" % (sys.argv[2], val)

    elif sys.argv[1] == 'set':
        if len(sys.argv) != 4:
            print "You need 3 arguments for set"
            sys.exit(1)
        region.set(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == 'delete':
        if len(sys.argv) != 3:
            print "You need 2 arguments for set"
            sys.exit(1)
        region.delete(sys.argv[2])
