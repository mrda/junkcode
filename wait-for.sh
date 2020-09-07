#!/usr/bin/env bash
#
# wait-for.sh <mins> - Print a  progress bar, waiting for <mins> minutes
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

waitfor() {

    # Allow the subshell to cause program exit
    set -E
    trap '[ "$?" -ne 66 ] || exit 66' ERR

    (
        exit_with_usage() {
            printf "Error: $(basename $0):wait for <mins>, where <mins> is an integer\n"
            exit 66
        }
        [ $# -ne 1 ] && exit_with_usage
        re='^[0-9]+$'
        [[ ! $1 =~ $re ]] && exit_with_usage
    )

    TOTSECS=$(( $1 * 60 ))
    MINS=$(($1-1))
    LEN=30

    for m in $(seq $MINS -1 0) ; do
        for s in $(seq 59 -1 0) ; do

            SECS_REMAINING=$(( $m*60 + $s ))
            PERCENT=$(bc <<< "scale=0; ($TOTSECS - $SECS_REMAINING) * 100 / $TOTSECS")
            NUMHASHES=$( bc <<< "scale=0; (($LEN * $PERCENT) / 100)" )
            NUMDOTS=$( bc <<< "scale=0; $LEN - $NUMHASHES" )

            HASHES=""
            if [ $NUMHASHES -ne 0 ]; then
                HASHES=$( printf "%-${NUMHASHES}s" "#" )
                HASHES=${HASHES// /#}
            fi

            DOTS=""
            if [ $NUMDOTS -ne 0 ]; then
                DOTS=$( printf "%-${NUMDOTS}s" "." )
                DOTS=${DOTS// /.}
            fi

            printf "\rTime Remaining: %02d:%02d [ %s%s ] %01d%% " $m $s "$HASHES" "$DOTS" $PERCENT
            sleep 1s
        done
    done
    echo ""
}

# Only call waitfor if this script isn't being sourced
[[ "${BASH_SOURCE[0]}" == "${0}" ]] && waitfor $1
