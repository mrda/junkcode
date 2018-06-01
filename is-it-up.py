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

from __future__ import print_function
import dns.resolver
import getopt
import os
import sys
import urllib2


debug = False


def get_ip_addresses(host, record_type):
    answers = dns.resolver.query(host, record_type)
    ips = []
    for rdata in answers:
        ips.append(str(rdata))
    return sorted(ips)


def verify_ip_address_assignments(first, second):
    if debug:
        print("Verifying {} and {} point to the same servers: "
              .format(first, second), end='')
    # Everything is as it should be if all the IP addresses for 'first'
    # are in the list of IP addresses for 'second'
    first_answers = get_ip_addresses(first, 'A')
    second_answers = get_ip_addresses(second, 'A')
    failure = False
    for ip in first_answers:
        if ip not in second_answers:
            failure = True
    if failure:
        if debug:
            print("MISMATCH")
        print("{:<40} IP addresses: {}".format(first, first_answers))
        print("{:<40} IP addresses: {}".format(second, second_answers))
        sys.exit(66)
    else:
        if debug:
            print("AOK")


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
    if debug:
        print("Checking {} is up: ".format(url), end='')

    code = get_url_nofollow(url)
    if code in [200]:
        interpretation = "AOK"
    else:
        interpretation = "ERROR"

    if debug:
        print("{} {}".format(code, interpretation))
    else:
        if interpretation == "ERROR":
            print("Unexpected HTTP code retrieved from {}: {}"
                  .format(url, code))


valid_opts = ['help', 'verbose']


def exit_with_usage(code=1):
    sys.stderr.write("Usage: {0} [{1}] public-hostname target-hostname\n"
                     .format(os.path.basename(sys.argv[0]),
                             '|'.join('--'+opt for opt in valid_opts)))
    sys.exit(code)


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], '', valid_opts)
    except getopt.error:
        exit_with_usage()

    if len(sys.argv) < 3 or (not opts and len(sys.argv) > 3):
        exit_with_usage()

    opt_flags = [flag for (flag, val) in opts]

    for opt in opt_flags:
        if opt == '--verbose':
            debug = True
        elif opt == '--help':
            exit_with_usage(code=0)

    # First verify that the main website IP address matches
    # the actual entry point website IP address
    verify_ip_address_assignments(args[0], args[1])

    # Now verify that we're getting a sensible HTTP return code
    verify_website_up("https://{}".format(args[0]))
