#!/usr/bin/env python3
#
# circletest.py - Hiring assignment test harness
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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
import csv
import json
import os
import requests
import sys


def get_data_files():
    return ["{}/.circle-test".format(os.path.expanduser(x))
            for x in [".", "~"]]


def get_test_data(filename):
    print("\nRunning tests from: {}".format(filename))
    test_data = []
    try:
        with open(filename) as f:
            # Test data format x1, y1, r1, x2, y2, r2, code, x3, y3 [, x4, y4]
            csvfilereader = csv.reader(f, delimiter=',')
            for orig_row in csvfilereader:

                # Allow for comments in test data
                if str(orig_row[0]).startswith('#'):
                    continue

                # Convert numbers into strings
                row = []
                for val in orig_row:
                    try:
                        val = int(val)
                    except ValueError:
                        val = float(val)
                    row.append(val)

                if len(row) == 7:
                    # No solutions
                    test_data.append([row[0], row[1], row[2],  # x1, y1, r1
                                      row[3], row[4], row[5],  # x2, y2, r2
                                      int(row[6])])            # httpcode
                elif len(row) == 9:
                    # One solution
                    test_data.append([row[0], row[1], row[2],  # x1, y1, r1
                                      row[3], row[4], row[5],  # x2, y2, r2
                                      int(row[6]),             # httpcode
                                      row[7], row[8]])         # x3, y3
                else:
                    # Must be two solutions
                    test_data.append([row[0], row[1], row[2],  # x1, y1, r1
                                      row[3], row[4], row[5],  # x2, y2, r2
                                      int(row[6]),             # httpcode
                                      row[7], row[8],          # x3, y3
                                      row[9], row[10]])
        return test_data
    except IOError as err:
        print("Error reading the file {0}: {1}".format(filename, err))


def build_json_request(x1, y1, r1, x2, y2, r2):
    d = {
        'samples': [
            {'x': x1,
             'y': y1,
             'distance': r1},
            {'x': x2,
             'y': y2,
             'distance': r2}
        ]
        }
    return json.dumps(d)


def build_json_response(x1, y1, r1, x2, y2, r2,
                        x3, y3, x4, y4):
    d = {
        'samples': [
            {'x': x1,
             'y': y1,
             'distance': r1},
            {'x': x2,
             'y': y2,
             'distance': r2}
        ]
        }

    d['sources'] = []

    if x3 is not None:
        d['sources'].append({'x': x3, 'y': y3})

    if x4 is not None:
        d['sources'].append({'x': x4, 'y': y4})

    return d


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def make_request(url, request):
    r = requests.post(url, data=request)
    try:
        resp = r.json()
    except:  # noqa
        resp = None
    return resp, r.status_code


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {0} <URL>\n"
                         .format(os.path.basename(sys.argv[0])))
        sys.exit(1)
    else:
        url = sys.argv[1]

    total_tests = 0
    total_fails = 0
    total_pass = 0
    files = get_data_files()
    for filename in files:
        if os.path.isfile(filename):
            test_id = 0
            for td in get_test_data(filename):
                total_tests += 1
                test_id += 1
                if len(td) == 7:
                    x1, y1, r1, x2, y2, r2, code = td
                    x3 = None
                    y3 = None
                    x4 = None
                    y4 = None
                elif len(td) == 9:
                    x1, y1, r1, x2, y2, r2, code, x3, y3 = td
                    x4 = None
                    y4 = None
                elif len(td) == 11:
                    x1, y1, r1, x2, y2, r2, code, x3, y3, x4, y4 = td
                request = build_json_request(x1, y1, r1, x2, y2, r2)
                expected_response = build_json_response(x1, y1, r1,
                                                        x2, y2, r2,
                                                        x3, y3, x4, y4)
                code = int(code)

                print("\n#\n# Running Test {}\n#".format(test_id))
                act_response, act_code = make_request(url, request)
                if act_response is None or act_code is None:
                    print("# Request:  {}".format(request))
                    print("*** TEST FAILED - no response returned")
                    total_fails += 1
                    continue

                if code != act_code:
                    # Not a failure, but worth noting
                    print("? HTTP code mismatch.  Got {} Expected {}".
                          format(act_code, code))

                if ordered(expected_response) != ordered(act_response):
                    print("* HTTP response mismatch.")
                    print("* Got this:")
                    print(json.dumps(act_response, indent=4))
                    print("* Expected:")
                    print(json.dumps(expected_response, indent=4))
                    print("*** TEST FAILED - Response didn't match")
                    total_fails += 1
                else:
                    print("# Request:  {}".format(request))
                    print("# Response: {}".format(act_response))
                    print("# HTTP Response Code: {}".format(act_code))
                    print("--- Test Passed")
                    total_pass += 1
    print("\n+------ Test Summary -------")
    print("| Total tests run: {}".format(total_tests))
    print("| Total passes: {}".format(total_pass))
    print("| Total fails: {}".format(total_fails))
    print("| Success rate: {}%".format(total_pass / total_tests * 100))
    print("+---- End Test Summary -----")
