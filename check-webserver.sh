#!/bin/bash
#
# check-webserver.sh - see if webserver is serving
#
# Copyright (C) 2017 Michael Davies <michael@the-davies.net>
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
NC="nc"
PORT=80

USAGE="$(basename $0): [hostname or IP address to check] [port]"

__check_cmd_avail ()
{
    if [ z$(which $1) == "z" ]; then
        echo "The command '$1' could not be found, exiting"
        exit 1
    fi
}

# Verify we have the commands we need
__check_cmd_avail ${NC}

if [ "$#" -eq 0 ]; then
  echo ${USAGE}
  exit 2
fi

HOST=$1

if [ "$#" -eq 2 ]; then
  PORT=$2
fi

printf "GET / HTTP/1.1\r\nHost: ${HOST}\r\nConnection: close\r\n\r\n" | ${NC} ${HOST} ${PORT}
