#!/bin/bash
#
# check-internet.sh - Basic internet connectivity test
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

if [ -z ${INTERNET_HOST+x} ]; then
    INTERNET_HOST=8.8.8.8
fi

START="$(date +%s)"

FIRST=0
while true; do
    ping -c1 $INTERNET_HOST >& /dev/null
    if [ $? -eq 0 ]; then
        echo "Internet is up"
        break
    fi
    if [ $FIRST -eq 0 ]; then
        echo "Internet is currently down, waiting for it to come back"
        FIRST=1
    fi
    echo -n "."
    sleep 1
done

END="$(date +%s)"
DIFF=$(echo "$END-$START" | bc)
if [ $DIFF -gt 0 ]; then
    echo "Internet was down for $DIFF seconds"
fi
