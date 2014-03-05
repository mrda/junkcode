#!/bin/sh
#
# find-backup - Find the latest version of the files specified from the
#               backup directory
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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
USAGE="$(basename $0): Please specify one search criteria"
BDIR=${HOME}/backup-`date +%Y`

if [ $# -eq 0 ]; then
  echo ${USAGE}
  exit 2
fi

if [ $# -eq 1 ]; then
    find ${BDIR} -print | grep "$@" | tail -1
    exit 0
fi

if [ $# -eq 2 ]; then
    if [ $1 = '-a' ]; then
        shift
        find ${BDIR} -print | grep "$@"
        exit 0
    fi
fi

echo ${USAGE}
exit 2
