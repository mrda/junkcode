#!/bin/env python3
#
# report-outages.py - Report in a human-friendly way the outages
#                     we've detected
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
import datetime
import os
import prettytable
import pytz
import tzlocal


home = os.getenv('HOME')
input_file = home + "/.poll-internet.sh.log"


def decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw:
            yield raw


def convert_date(epoch):
    tz = tzlocal.get_localzone()
    dt = datetime.datetime.fromtimestamp(int(epoch), tz)
    return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')


def convert_duration(secs):
    secs = int(secs)
    return "{:2d}d {:2d}h {:2d}m {:2d}s".format(secs // 86400,
                                                secs % 86400 // 3600,
                                                secs % 3600 // 60,
                                                secs % 60)


def process_row(table, row):
    table.add_row([convert_date(row[0]),
                   convert_date(row[1]),
                   convert_duration(row[2])])


x = prettytable.PrettyTable()
x.field_names = ["Outage Detected", "Outage End", "Outage Duration"]

with open(input_file, mode='r') as csvfile:
    reader = csv.reader(decomment(csvfile))
    for row in reader:
        process_row(x, row)

print(x)
