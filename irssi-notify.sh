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

# Use DEBUG from the environment, but ensure that we don't error if it's not
if [ -z "$DEBUG" ]; then
  DEBUG=0
fi

if [ -z "$LOCALLOGGING" ]; then
  LOCALLOGGING=1
fi

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

# Find my nick
if [[ -z "$NICK" ]]; then
    NICK_FILE=${HOME}/.nick
    if [ ! -r $NICK_FILE ]; then
        printf "%s: You don't have your nick defined in \$NICK \
and cannot find nick file %s\n" $BASENAME $NICK_FILE
        exit 1
    fi
    . $NICK_FILE
fi


# Allow platform specific capabilities
ADDSOUND=false
ADDICON=false
case "$OSTYPE" in
  darwin*)
    check_cmd_avail osascript
    check_cmd_avail blink1-tool
    ADDSOUND=true
    ;;
  linux*)
    check_cmd_avail notify-send
    check_cmd_avail blink1-tool
    ADDICON=true
    ;;
  *)
    # Do nothing
    ;;
esac

# Add in $HOST specific icons and/or sounds
SOUND=""
ICON=""
if [ $ADDSOUND=true ]; then
    SOUND="sound name \"Sosumi\""
fi

if [ $ADDICON=true ]; then
    if [ "$1" = "rh-bos-fs" ]; then
        ICON="${HOME}/Pictures/redhat.jpg"
    fi
    if [ "$1" = "gce" ]; then
        ICON="${HOME}/Pictures/Tux.png"
    fi
fi


blink ()
{
  blink1-tool --playpattern '10,#ff4500,0.2,0,#00ff00,0.2,0' >& /dev/null
}

clear_blink ()
{
  blink1-tool --off >& /dev/null
}

# Notify the user on their desktop
desktop_notify ()
{
  # $1 is the header
  # $2 is the message

  if [ "$DEBUG" -eq 1 ] ; then
    printf "H:$1\tM:$2\n"
  fi

  case "$OSTYPE" in
    darwin*)
      osascript -e "display notification \"$1: $2\" with title \"irssi on $HOST\" $SOUND"
      blink
      ;;
    linux*)
      notify-send -a "irssi-notify" -i "$ICON" "$1" "$2"
      blink
      ;;
    *)
      printf "H:$heading\tM:$message\n"
   esac
}

clear_notification ()
{
  # $1 is the header
  # $2 is the message

  if [ "$DEBUG" -eq 1 ] ; then
    printf "H:$1\tM:$2\n"
  fi

  clear_blink
}

# Change the title bar
echo -ne "\033]0;[irssi on $HOST] - Status\007"

# Go and poll the notifications
ssh -q $HOST "echo \#status New Connection on $HOST;tail -n0 -f .irssi/fnotify" | \
while read heading message ; do

    # FIXME: Add a check for escapable characters and do $something

    # Keep a local copy of conversations
    if [ "$LOCALLOGGING" -eq 1 ] ; then
      printf "$(date +%Y%m%d-%H%M%S) $heading: $message\n" >> $HOME/.irssi-log
    fi

    if [ "$heading" == "$NICK" ]; then
        clear_notification "$heading" "$message"
    else
        desktop_notify "$heading" "$message"
    fi
done

