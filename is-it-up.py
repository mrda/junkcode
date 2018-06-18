#!/usr/bin/env python
#
# is-it-up.py - verify the DNS entries for a wesite are still valid
#               and as an added bonus, verify that the website is up
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
#

from __future__ import print_function
import csv
import dns.resolver
import getopt
import IPy
import os
import sys
import traceback
import urllib2


debug = False


def get_config_files():
    return ["{}/.dns-hosts-to-check".format(os.path.expanduser(x))
            for x in [".", "~"]]


def get_hosts_from_file(filename):
    hosts = []
    try:
        with open(filename) as f:
            # Hosts as in format <host1>,<host2>
            csvfilereader = csv.reader(f, delimiter=',')
            for row in csvfilereader:
                hosts.append([row[0], row[1]])
        return hosts
    except IOError as err:
        print("Error reading the file {0}: {1}".format(filename, err))


def get_hosts():
    hosts = []
    config_files = get_config_files()
    for filename in config_files:
        if os.path.isfile(filename):
            hosts = get_hosts_from_file(filename)
    if not hosts:
        print("No hosts found")
    return hosts


def get_ip_addresses(host, record_type):
    answers = dns.resolver.query(host, record_type)
    ips = []
    for rdata in answers:
        ips.append(str(rdata))
    return sorted(ips)


def identify_host(host_or_ip):
    result = None
    try:
        IPy.IP(host_or_ip)
        result = [host_or_ip]
    except ValueError:
        result = get_ip_addresses(host_or_ip, 'A')
    return result


def verify_ip_address_assignments(first, second):
    if debug:
        print("Verifying {} and {} point to the same servers: "
              .format(first, second), end='')
    # Everything is as it should be if all the IP addresses for 'first'
    # are in the list of IP addresses for 'second'
    first_answers = identify_host(first)
    second_answers = identify_host(second)
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
    except Exception:
        print("*** Unexpected error")
        print(traceback.format_exc())
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

    opt_flags = [flag for (flag, val) in opts]
    for opt in opt_flags:
        if opt == '--verbose':
            debug = True
        elif opt == '--help':
            exit_with_usage(code=0)

    hosts = []
    if len(sys.argv) < 3:
        # Must have hosts defined in a file
        hosts = get_hosts()

    else:
        # Must be command line options
        hosts.append([args[0], args[1]])

    for hostpair in hosts:
        # First verify that the main website IP address matches
        # the actual entry point website IP address
        verify_ip_address_assignments(hostpair[0], hostpair[1])

        # Now verify that we're getting a sensible HTTP return code
        # Note: We don't want to test https connections, as we'll need
        # to deal with self-signed certificates or Let's Encrypt, and we
        # we just want basic connectivity, so we'll ignore this for now
        verify_website_up("http://{}".format(hostpair[0]))
