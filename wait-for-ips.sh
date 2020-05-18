#!/usr/bin/env bash
#
# wait-for-ips.sh <list of ip addresses> - Wait for IPs to respond via ICMP
#
# Copyright (C) 2020 Michael Davies <michael@the-davies.net>
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

# Check that each command line argument looks roughly like an IP address
for ARG in $*; do
    re='^(((25[0-5])|(2[0-4][0-9])|([01]?[0-9]?[0-9]))\.)?'
    re+='(((25[0-5])|(2[0-4][0-9])|([01]?[0-9]?[0-9]))\.)?'
    re+='(((25[0-5])|(2[0-4][0-9])|([01]?[0-9]?[0-9]))\.)?'
    re+='(((25[0-5])|(2[0-4][0-9])|([01]?[0-9]?[0-9])))'
    re+='$'
    if [[ ! $ARG =~ $re ]] ; then
        printf "Usage: $(basename $0) <list of ip addresses>\n"
        printf "\"$ARG\" is not a valid IP address. Exiting...\n"
        exit 2
    fi
done

# Wait for IPs to become available
for IP in $*; do
    echo -n "Waiting for $IP to come alive: "
    while true ; do
        ping -c1 $IP >& /dev/null
        if [[ $? -eq 0 ]] ; then
            break
        else
            echo -n '.'
            sleep 1
        fi
    done
    echo "OK"
done
