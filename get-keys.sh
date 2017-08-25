#!/bin/sh
#
# get-keys.sh - retrieve the Github keys for a user
#
# Copyright (C) 2016 Michael Davies <michael@the-davies.net>
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
USAGE="$(basename $0): <GitHub User(s)>"

if [ "$#" -eq 0 ]; then
  echo ${USAGE}
  exit 2
fi

for ACCOUNT in "$@"; do
    echo "User account is ${ACCOUNT}"
    KEYNAME="${ACCOUNT}.keys"
    curl -O https://github.com/${KEYNAME}
    echo "$1's GitHub keys have been saved as ${KEYNAME}"
done
