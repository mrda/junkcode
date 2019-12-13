#!/bin/bash
#
# report-outages.sh - Report in a human-friendly way the outages
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

INPUT_FILE=${HOME}/.poll-internet.sh.log

show_time ()
{
    SECS=$1
    printf "%0dd %0dh %0dm %0ds\n" $(($SECS/86400)) $(($SECS%86400/3600)) $(($SECS%3600/60)) $(($SECS%60))
}

printf "Detected outages are:\n"
while IFS="," read -ra LINE; do

    # Skip comments
    [[ ${LINE[0]:0:1} == "#" ]] && continue

    START=$(date -d @${LINE[0]})
    END=$(date -d @${LINE[1]})
    DURATION=$(show_time ${LINE[2]})
    printf "%s\t%s\t%s\n" "$START" "$END" "$DURATION"

done < "$INPUT_FILE"
