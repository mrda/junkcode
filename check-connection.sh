#!/bin/bash
#
# check-connection.sh <host> <port> - verify the network connectivity to a
#                                     host/port combination is working.
#                                     Keep looping until it is available.
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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

USAGE="$(basename $0): Please provide both the host and port to check"

if [ $# -ne 2 ]; then
  echo ${USAGE}
  exit 2
fi

while true; do
    nc -zv "$1" "$2"
    if [ "$?" == "0" ]; then
        break;
    fi;
done
