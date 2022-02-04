#!/usr/bin/env bash
#
# time-progress.sh <mins> - Print a  progress bar for <mins> minutes
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

# Include bash library
command -v bashlib.sh &> /dev/null || \
{ echo >&2 "$(basename $0): Can't find bashlib.sh.  Aborting."; exit 1; }
. bashlib.sh

exit_with_usage() {
    printf "Usage: $(basename $0) <mins>, where <mins> is an integer\n"
    exit -1
}

[ $# -ne 1 ] && exit_with_usage
re='^[0-9]+$'
[[ ! $1 =~ $re ]] && exit_with_usage

timebar $1 "Time Remaining:"
