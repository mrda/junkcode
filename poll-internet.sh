#!/bin/bash
#
# poll-internet.sh - Continuous loop to see if the internet is staying up,
#                    use blink to tell people we have an outage
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
SECS_PER_MIN=60
SECS_PER_HOUR=3600
SECS_PER_DAY=86400

HOSTS_TO_CHECK=( google-public-dns-a.google.com
                 google-public-dns-b.google.com
                 one.one.one.one
                 ns1.telstra.net
                 facebook.com
                 twitter.com
                 akamai.com )

POLL_NORMAL=300 # seconds
POLL_OUTAGE=60  # seconds

POLL_HOURLY_INTERVAL=$((${SECS_PER_HOUR}/${POLL_NORMAL}))
POLL_DAILY_INTERVAL=24

OUTAGE_FILE=${HOME}/.$(basename $0).log

# Use DEBUG from the environment, but ensure that we don't error if it's not
[[ -z "$DEBUG" ]] && DEBUG=0

# USB notification dongle https://blink1.thingm.com/blink1-tool/
BLINK=blink1-tool
HAVEBLINK=0
if hash $BLINK &> /dev/null; then
    HAVEBLINK=1
fi

blink ()
{
    [[ $HAVEBLINK -eq 1 ]] && $BLINK --blue >& /dev/null
}

clear_blink ()
{
    [[ $HAVEBLINK -eq 1 ]] && $BLINK --off >& /dev/null
}

# Display the number of seconds supplied in a user friendly format of "d h m s"
show_time ()
{
    SECS=$1
    printf "%0dd %0dh %0dm %0ds\n" $(($SECS/${SECS_PER_DAY})) $(($SECS%${SECS_PER_DAY}/${SECS_PER_HOUR})) $(($SECS%${SECS_PER_HOUR}/${SECS_PER_MIN})) $(($SECS%${SECS_PER_MIN}))
}


# Check a list of HA internet sites via a single ICMP packet, seeing if
# _any_ of them are reachable. If at least one is, our internet must be ok.
is_internet_up ()
{
    ANY_OK=0
    for IP_ADDR in ${IP_ADDR_LIST[*]}; do
        [[ $DEBUG -eq 1 ]] && echo $(date +"%Y%m%d %H:%M:%S ") Checking $IP_ADDR
        ping -c1 $IP_ADDR >& /dev/null
        if [ $? -eq 0 ]; then
            ANY_OK=1
            break
        fi
    done

    return $ANY_OK
}

# Shuffle an array, call like this:
# array_shuffle ARRAY_TO_SHUFFLE ${ARRAY_TO_SHUFFLE[@]}
array_shuffle ()
{
    local OUTPUT=$1
    local INPUT=("${@:2}")

    local NUM=$(( ${#INPUT[@]} -1 ))
    local NEWSEQ=$( shuf -i 0-$NUM )
    declare -a NEWARR
    for i in $NEWSEQ; do
        NEWARR+=( ${INPUT[$i]} )
    done

    eval unset $OUTPUT
    eval $OUTPUT="'${NEWARR[*]}'"
}

#
# Main
#
printf "# Restarting %s at %s\n" $(basename $0) "$(date +'%Y%m%d %H:%M:%S')" >> $OUTAGE_FILE

# Translate hostnames into IP addresses, and perform IP address lookup once
declare -a IP_ADDR_LIST
for NAME in ${HOSTS_TO_CHECK[*]}; do
    IP_ADDR=( $(dig +short $NAME | head -n 1) )
    if [[ -z ${IP_ADDR} ]]; then
        printf "%s: Unable to resolve hostname. Exiting...\n" $(basename $0)
        exit 1
    fi
    IP_ADDR_LIST+=( $IP_ADDR )

    [[ $DEBUG -eq 1 ]] && printf "%s has IP Address %s\n" $NAME $IP_ADDR
done

POLL_COUNT=0
POLL_HOURS=$(date +'%H' | sed 's/^0//')  # Start at the right point in the day

printf "$(date +'%Y%m%d %H:%M:%S ')"
printf %0${POLL_HOURS}s | tr " " "x"

while true; do

    # Shuffle IP_ADDR_LIST so we don't hit the same host all the time
    array_shuffle IP_ADDR_LIST ${IP_ADDR_LIST[@]}

    OUTAGE=0
    while true; do
        is_internet_up || break
        if [ $OUTAGE -eq 0 ]; then
            OUTAGE=1
            START="$(date +%s)"
            printf "\n  Outage: %s %s " $(date +"%Y%m%d %H:%M:%S ")
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
            printf "%s,%s,%s\n" $START $END $DIFF >> $OUTAGE_FILE
        fi
    fi

    # Visual indication that we're still running, if we're not in debug mode
    [[ $DEBUG -eq 0 ]] && [[ $POLL_COUNT -ge $POLL_HOURLY_INTERVAL ]] && printf "." && POLL_COUNT=0 && POLL_HOURS=$(($POLL_HOURS + 1))
    [[ $DEBUG -eq 0 ]] && [[ $POLL_HOURS -ge $POLL_DAILY_INTERVAL ]] && printf "\n$(date +'%Y%m%d %H:%M:%S ')" && POLL_HOURS=0
    [[ $DEBUG -eq 0 ]] && POLL_COUNT=$(($POLL_COUNT + 1))

    sleep $POLL_NORMAL

done
