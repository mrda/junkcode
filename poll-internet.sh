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
POLL_NORMAL=300 # seconds
POLL_OUTAGE=60  # seconds

BLINK=blink1-toolz
HAVEBLINK=0
if hash $BLINK &> /dev/null; then
  HAVEBLINK=1
fi

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

if [ -z ${INTERNET_HOST+x} ]; then
    INTERNET_HOST=8.8.8.8
fi

START="$(date +%s)"

while true; do

  OUTAGE=0
  while true; do
      ping -c1 $INTERNET_HOST >& /dev/null
      if [ $? -eq 0 ]; then
          break
      fi
      if [ $OUTAGE -eq 0 ]; then
          OUTAGE=1
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
        echo " Down for $DIFF seconds"
    fi
  fi

  sleep $POLL_NORMAL

done
