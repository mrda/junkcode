#!/bin/bash
#
# teamtime - Print out the time in places where my team is
#
# Copyright (C) 2025 Michael Davies <michael@the-davies.net>
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

declare -A PLACES
PLACES["Adelaide"]="Australia/Adelaide"
PLACES["Beijing"]="Asia/Shanghai"
PLACES["Raleigh"]="America/New_York"
PLACES["Bengaluru"]="Asia/Kolkata"

# Find the length of the longest place name
MAXLEN=0
for KEY in ${!PLACES[@]} ; do
    LEN=${#KEY} # Length of the KEY
    if [[ ${LEN} -gt ${MAXLEN} ]] ; then
        MAXLEN=$LEN
    fi
done
((MAXLEN+=2)) # for the space and a colon

for KEY in ${!PLACES[@]} ; do
   printf "%-${MAXLEN}s" "${KEY}: "
   TZ=${PLACES[${KEY}]} date "+%Y-%m-%d %I:%M:%S %p %Z"
done |
sort
