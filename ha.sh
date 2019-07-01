#!/bin/sh
#
# ha.sh - Quick hack to control HA switches from the cmdline
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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

# Things you can modify
declare -a KNOWN_SWITCHES=('switch.lounge_lamp' 'switch.coffee_machine')
declare -a VALID_STATES=('on' 'off')
# End of things you can modify

CREDS=${HOME}/.ha.sh
BASENAME=$(basename $0)

if [ ! -r $CREDS ]; then
  printf "%s: Cannot find required credentials file %s\n" $BASENAME $CREDS
  exit 1
fi

# Bring HA_* env vars into scope
. $CREDS

# Use DEBUG from the environment, but ensure that we don't error if it's not
if [ -z "$DEBUG" ]; then
  DEBUG=0
fi

array_contains () {
  # $1 = Thing to look for
  # $2 = the array to search
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

check_switch() {
  # Check to see if we have a known switch
  # $1 == the switch to check
  # $2 == the array of switches
  local SWITCH=$1
  shift
  local ARR=("$@")
  array_contains $SWITCH "${ARR[@]}"
  local ALLOWED=$?

  if [ $ALLOWED -eq 1 ]; then
    printf "%s: Unknown switch '%s'. Exiting...\n" $BASENAME $SWITCH
    exit 2
  fi
}

# Check to see if we have a valid state
check_states() {
  # Check to see if we have a known switch
  # $1 == the state to check
  # $2 == the array of states
  local STATE=$1
  shift
  local ARR=("$@")
  array_contains $STATE "${ARR[@]}"
  local ALLOWED=$?

  if [ $ALLOWED -eq 1 ]; then
    printf "%s: Unknown state '%s'. Exiting...\n" $BASENAME $STATE
    exit 2
  fi
}

get_state() {
  local SWITCH=$1
  local AUTH="Authorization: Bearer $HA_TOKEN"
  local CONTENT="Content-Type: application/json"
  local CMD=$(curl -s -X GET -H "$AUTH" -H "$CONTENT" ${HA_BASE_URL}/api/states/${SWITCH})
  if [ $DEBUG -eq 1 ]; then
    echo curl -s -X GET -H "$AUTH" -H "$CONTENT" ${HA_BASE_URL}/api/states/${SWITCH}
  fi
  echo $CMD | python3 -m json.tool
}

set_state() {
  local SWITCH=$1
  local STATE=$2
  local AUTH="Authorization: Bearer $HA_TOKEN"
  local CONTENT="Content-Type: application/json"
  local ENTITY="{\"entity_id\": \"$SWITCH\"}"
  if [ $DEBUG -eq 1 ]; then
    echo curl -s -X POST -H "$AUTH" -H "$CONTENT" -d "$ENTITY" ${HA_BASE_URL}/api/services/switch/turn_$STATE
  fi
  local CMD=$(curl -s -X POST -H "$AUTH" -H "$CONTENT" -d "$ENTITY" ${HA_BASE_URL}/api/services/switch/turn_$STATE)
}

# cmdline processing
if [ "$#" -eq 1 ]; then
  check_switch $1 "${KNOWN_SWITCHES[@]}"
  get_state $1
elif [ "$#" -eq 2 ]; then
  check_switch $1 "${KNOWN_SWITCHES[@]}"
  check_states $2 "${VALID_STATES[@]}"
  set_state $1 $2
else
  # Unknown command
  printf "Usage: %s <switch> [<state>]\n" $BASENAME
  exit 3
fi

