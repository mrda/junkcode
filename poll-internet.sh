#!/bin/bash
#
# poll-internet.sh - Continuous loop to see if the internet is staying up,
#                    use blink to tll people we have an outage
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
HOSTS_TO_CHECK=( google.com facebook.com twitter.com )
POLL_NORMAL=300 # seconds
POLL_OUTAGE=60  # seconds

BLINK=blink1-tool
HAVEBLINK=0
if hash $BLINK &> /dev/null; then
    HAVEBLINK=1
fi

show_time ()
{
    # Display the number of seconds supplied in a user friendly
    # format of "d h m s"
    SECS=$1
    printf "%0dd %0dh %0dm %0ds\n" $(($SECS/86400)) $(($SECS%86400/3600)) $(($SECS%3600/60)) $(($SECS%60))
}

blink ()
{
    if [[ $HAVEBLINK -eq 1 ]]; then
        $BLINK --blue >& /dev/null
    fi
}

clear_blink ()
{
    if [[ $HAVEBLINK -eq 1 ]]; then
        $BLINK --off >& /dev/null
    fi
}

declare -a IP_ADDR_LIST
build_ip_addresses ()
{
    for NAME in ${HOSTS_TO_CHECK[*]}; do
        IP_ADDR_LIST+=( $(dig +short $NAME | head -n 1) )
    done
}
build_ip_addresses

is_internet_up ()
{
    ANY_OK=0
    for IP_ADDR in ${IP_ADDR_LIST[*]}; do
        ping -c1 $IP_ADDR >& /dev/null
        if [ $? -eq 0 ]; then
            ANY_OK=1
        fi
    done

    if [ $ANY_OK -eq 1 ]; then
        return 0
    fi
    return 1
}


while true; do

    OUTAGE=0
    while true; do
        is_internet_up
        if [ $? -eq 0 ]; then
            break
        fi
        if [ $OUTAGE -eq 0 ]; then
            OUTAGE=1
            START="$(date +%s)"
            echo -n Outage: $(date +"%Y%m%d %H:%M:%S ")
            blink
        fi
        echo -n "."
        sleep $POLL_OUTAGE
    done

    if [ $OUTAGE -eq 1 ]; then
        clear_blink
        END="$(date +%s)"
        DIFF=$(echo "$END-$START" | bc)
        if [ $DIFF -gt 0 ]; then
            echo -n " Down for "
            show_time $DIFF
        fi
    fi

    sleep $POLL_NORMAL

done
