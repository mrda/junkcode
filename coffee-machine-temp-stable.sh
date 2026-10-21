#!/bin/sh
#
# coffee-machine-temp-stable.sh - Check power usage of coffee
#                                 machine, if stable, then the
#                                 temperature must be stable.
#
# Copyright (C) 2026 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html

# Include bash library
command -v bashlib.sh &> /dev/null || \
{ echo >&2 "$(basename $0): Can't find bashlib.sh.  Aborting."; exit 1; }
. bashlib.sh

DEBUG=0
lastval=-1
repeated=0
ten="10"

checkinterval=10 # seconds
stablecurrent=2000
stablecount=10
firsttime=1

# Arrows
# See https://unicode-explorer.com/list/arrows
UPARROW='\u2934'
DOWNARROW='\u2935'
STABLEARROW='\u2933'

round()
{
    echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
}

print_current()
{
    w=$(echo "$1 / 10" | bc)
    echo $w
}


get_current() {
  temp=$(ha sensor.coffee_machine_current_consumption 2> /dev/null)
  RET=$?
  val=0
  if [[ $RET -eq 0 ]]; then
    val=$(echo $temp | jq '.state')
    # remove excess quotes
    val="${val//\"/}"
  else
    echo "***********************\nReturn code was $RET"
    #echo $(date) $val
    #val="0.0"
    val="0"
  fi
  echo $val
}

CONTINUE=1
while [ $CONTINUE -eq 1 ]; do
    current=$(get_current)

    if [[ "${current}" = "0" ]]; then
        echo "Error reading current"
        continue
    fi

    # convert to int
    current=$(round $current 0)
    result=$(echo "scale=0;(${current}*${ten})/1" | bc)

    if [[ DEBUG -eq 1 ]]; then
        echo $(date) $result
    fi
    current=$result

    # Check for bad readings first
    if [[ $current -eq -1 ]]; then
        echo "***********************\nReturn code was $RET"
        echo $(date) $current
        continue
    fi

    # Here's where the magic happens

    # If the wattage is less than $stablecurrent for $stablecount
    # times (sleeping for $checkinterval} inbetween, then the coffee
    # machine should be at the right temperature

    if [[ $current -le ${stablecurrent} ]]; then
        echo -ne $DOWNARROW
    elif [[ $current -ge ${stablecurrent} ]]; then
        echo -ne $UPARROW
        if [[ $firsttime -eq 1 ]]; then
            ppcurrent=$( print_current $current )
            echo "Warming coffee machine! Current usage is $ppcurrent watts."
            firsttime=0
        fi
        repeated=0
    else
        echo -ne $STABLEARROW
        #if [[ $repeated -eq 0 ]]; then
            #echo "Approaching target temperature"
        #    echo -ne $STABLEARROW
        #fi
        ((repeated++))
        # echo -n "."
        if [[ $repeated -ge ${stablecount} ]]; then
            echo -n "Heating is using less than "
            watts=$(echo "$stablecurrent / 10" | bc)
            echo "$watts Watts (checked ${stablecount} times and is stable)."
            echo "Coffee machine temperature is ready!"
            CONTINUE=0
        fi
    fi

    sleep ${checkinterval}
done



