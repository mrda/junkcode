#!/usr/bin/env python
#
# is-it-up.py - verify the DNS entries for a wesite are still valid
#               and as an added bonus, verify that the website is up
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

import dns.resolver
import os
import sys
import urllib2


def get_ip_addresses(host, record_type):
    answers = dns.resolver.query(host, record_type)
    ips = []
    for rdata in answers:
        ips.append(str(rdata))
    return sorted(ips)


def verify_ip_address_assignments(first, second):
    # Everything is as it should be if all the IP addresses for 'first'
    # are in the list of IP addresses for 'second'
    first_answers = get_ip_addresses(first, 'A')
    second_answers = get_ip_addresses(second, 'A')
    failure = False
    for ip in first_answers:
        if ip not in second_answers:
            failure = True
    if failure:
        print "{:<40} IP addresses: {}".format(first, first_answers)
        print "{:<40} IP addresses: {}".format(second, second_answers)
        sys.exit(66)


def get_url_nofollow(url):
    try:
        response = urllib2.urlopen(url)
        code = response.getcode()
        return code
    except urllib2.HTTPError as e:
        return e.code
    except e:
        return 0


def verify_website_up(url):
    # Quick summary of HTTP return codes:
    #   1xx Hold On
    #   2xx Here you go
    #   3xx Go Away
    #   4xx You Stuffed Up
    #   5xx I Stuffed Up
    code = get_url_nofollow(url)
    if code not in [200]:
        print "Unexpected HTTP code retrieved from {}: {}".format(url, code)
        sys.exit(67)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("{}: public-hostname actual-hostname".format
              (os.path.basename(sys.argv[0])))
        sys.exit(1)

    # First verify that the main website IP address matches
    # the actual entry point website IP address
    verify_ip_address_assignments(sys.argv[1], sys.argv[2])

    # Now verify that we're getting a sensible HTTP return code
    verify_website_up("https://{}".format(sys.argv[1]))
