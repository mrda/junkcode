#!/usr/bin/env bash
#
# countdown.sh <mins> - Print a second-by-second countdown from <mins> minutes
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
exit_with_usage() {
    printf "Usage: $(basename $0) <mins>, where <mins> is an integer\n"
    exit -1
}

[ $# -ne 1 ] && exit_with_usage
re='^[0-9]+$'
[[ ! $1 =~ $re ]] && exit_with_usage

MINS=$(($1-1))
for m in $(seq $MINS -1 0) ; do
    for s in $(seq 59 -1 0) ; do
        printf "\r%02d:%02d" $m $s
        sleep 1s
    done 
done
echo ""
