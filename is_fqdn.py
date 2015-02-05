#!/usr/bin/env python
#
# is_fqdn - determine whether a supplied string is a valid FQDN
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
#
# By "FQDN" we mean the whether the supplied string is valid according
# to RFC1035 (http://tools.ietf.org/html/rfc1035)
#
# For your benefit, I quote:
#
#    "The following syntax will result in fewer problems with many
#    applications that use domain names (e.g., mail, TELNET).
#
#    <domain> ::= <subdomain> | " "
#
#    <subdomain> ::= <label> | <subdomain> "." <label>
#
#    <label> ::= <letter> [ [ <ldh-str> ] <let-dig> ]
#
#    <ldh-str> ::= <let-dig-hyp> | <let-dig-hyp> <ldh-str>
#
#    <let-dig-hyp> ::= <let-dig> | "-"
#
#    <let-dig> ::= <letter> | <digit>
#
#    <letter> ::= any one of the 52 alphabetic characters A through Z in
#    upper case and a through z in lower case
#
#    <digit> ::= any one of the ten digits 0 through 9
#
#    Note that while upper and lower case letters are allowed in domain
#    names, no significance is attached to the case.  That is, two names with
#    the same spelling but different case are to be treated as if identical.
#
#    The labels must follow the rules for ARPANET host names.  They must
#    start with a letter, end with a letter or digit, and have as interior
#    characters only letters, digits, and hyphen.  There are also some
#    restrictions on the length.  Labels must be 63 characters or less."
#
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


def is_fqdn(fqdn):
    regex = '^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9]|[a-z0-9]{0,62})?' \
            '(\.[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9]|[a-z0-9]{0,62})?)+$'
    p = re.compile(regex)
    return p.match(fqdn.lower()) is not None

if __name__ == '__main__':

    if len(sys.argv) == 2:
        print is_hostname_safe(sys.argv[1])
    else:
        # Otherwise just run the tests

        long_valid = 's' * 63
        long_invalid = 's' * 64

        tests = {
            'michaeldavies.org': True,
            '-spam': False,
            'spam-': False,
            'the-davies.net': True,
            'spam eggs': False,
            '9spam.eggs.com': True,
            'www.spam7.info': True,
            'mail.br34kf4st.net': True,
            '$pam': False,
            'egg$': False,
            'spam#eggs': False,
            ' eggs': False,
            'spam ': False,
            '': False,
            'a.b.c.d': True,
            'XX.LCS.MIT.EDU': True,
            'xx.lcs.MIT.edu': True,
            'xX.lCs.mIT.EdU': True,
            'a.' + long_valid: True,
            long_valid + '.' + long_valid: True,
            'a.' + long_invalid: False,
        }

        print "\nTesting is_fqdn()\n"
        final_result = True
        for id, name in enumerate(tests):
            result = is_fqdn(name)
            test_result = result == tests[name]
            if test_result:
                print "Test %s: PASSED  Testing '%s', got '%s'" % \
                    (id, name, tests[name])
            else:
                print "Test %s: *** FAILED '%s' != '%s' got '%s'" % \
                    (id, name, tests[name], result)
            final_result = final_result and test_result

        print "\nAll tests passed? %s\n" % final_result
