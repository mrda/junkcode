#!/usr/bin/env python
#
# is_hostname_safe - determine whether a supplied string is hostname safe.
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
#
# By "hostname safe" we mean the whether the hostname part of a FQDN
# follows the approporiate standards for a hostname.  Specifically:
#    * http://en.wikipedia.org/wiki/Hostname
#    * http://tools.ietf.org/html/rfc952
#    * http://tools.ietf.org/html/rfc1123
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


def is_hostname_safe(hostname):
    regex = '^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9]|[a-z0-9]{0,62})?$'
    p = re.compile(regex)
    return p.match(hostname) is not None

if __name__ == '__main__':

    if len(sys.argv) == 2:
        print is_hostname_safe(sys.argv[1])
    else:
        # Otherwise just run the tests

        tests = {
            'spam': True,
            '-spam': False,
            'spam-': False,
            'spam-eggs': True,
            'spam eggs': False,
            '9spam': True,
            'spam7': True,
            'br34kf4st': True,
            '$pam': False,
            'egg$': False,
            'spam#eggs': False,
            ' eggs': False,
            'spam ': False,
            '': False,
            's': True,
            's' * 63: True,
            's' * 64: False,
        }

        print "\nTesting is_hostname_safe()\n"
        final_result = True
        for id, name in enumerate(tests):
            result = is_hostname_safe(name)
            test_result = result == tests[name]
            if test_result:
                print "Test %s: PASSED  Testing '%s', got '%s'" % \
                    (id, name, tests[name])
            else:
                print "Test %s: *** FAILED '%s' != '%s' got '%s'" % \
                    (id, name, tests[name], result)
            final_result = final_result and test_result

        print "\nAll tests passed? %s\n" % final_result
