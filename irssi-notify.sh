#!/bin/bash
#
# irssi_notify.sh - poll a remote irssi bounce host for nick mentions and
#                   display them locally on this desktop.
#
#                   Thanks to tonyb for the skeleton of this
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
DEBUG=true

case "$1" in
  start)
    shift 1
      while : ; do
        $0 "$*"
        echo 'Restarting'
        sleep 5
      done
      exit 0
      ;;
  *)
    if [ -z "$1" ]; then
      printf "Usage: $(basename $0) [start] <irssi bounce host>\n"
      exit 1
    fi
    HOST=$1
    ;;
esac

# Check to see if the required commands are available
check_cmd_avail ()
{
    if ! hash ${1} &> /dev/null; then
        echo "The command '$1' could not be found, exiting"
        exit 1
    fi
}

#TODO: Add in $HOST specific icons and/or sounds

# Platform and host specific changes
SOUND=""
ICON=""
case "$OSTYPE" in
  darwin*)
    check_cmd_avail osascript
    check_cmd_avail blink1-tool
    #SOUND="sound name \"Sosumi\""
    ;;
  linux*)
    check_cmd_avail desktop_notify
    check_cmd_avail blink1-tool
    #ICON="-i $HOME/.local/share/icons/hicolor/128x128/redhat.png"
    ;;
  *)
    # Do nothing
    ;;
esac

blink ()
{
  blink1-tool --playpattern '10,#ff4500,0.2,0,#00ff00,0.2,0' >& /dev/null
}

# Notify the user on their desktop
desktop_notify ()
{
  # $1 is the header
  # $2 is the message

  if [ "$DEBUG" = true ] ; then
    printf "H:$heading\tM:$message\n"
  fi

  case "$OSTYPE" in
    darwin*)
      osascript -e "display notification \"$1: $2\" with title \"irssi on $HOST\" $SOUND"
      blink
      ;;
    linux*)
      desktop_notify "$ICON" -a "irssi-notify" "$1" "$2"
      blink
      ;;
    *)
      printf "H:$heading\tM:$message\n"
   esac

}

# Change the title bar
echo -ne "\033]0;[irssi on $HOST] - Status\007"

# Go and poll the notifications
ssh -q $HOST "echo \#status New Connection on $HOST;tail -n0 -f .irssi/fnotify" | \
while read heading message ; do
    # FIXME: Add a check for escapable characters and do $something
    desktop_notify "$heading" "$message"
done

