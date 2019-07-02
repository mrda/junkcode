#!/bin/bash
#
# get-ifaces.sh - display my network interfaces
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
UNUSED_IFS=()
IFACE_MAXWIDTH=0
for IFACE in $(ls /sys/class/net); do
  IFACE_LEN=${#IFACE}
  if [[ "$IFACE_LEN" -gt "$IF_MAXWIDTH" ]]; then
    IF_MAXWIDTH=$IFACE_LEN
  fi
done

printf "Configured Interfaces:\n"
for IFACE in $(ls /sys/class/net); do
  IPADDR=$(ip addr show dev $IFACE | grep "inet " | awk -F'[: /]+' '{ print $3 }')
  if [ "z$IPADDR" = "z" ]; then
    UNUSED_IFS+=($IFACE)
  else
    printf "  %${IF_MAXWIDTH}s\t%s\n" $IFACE $IPADDR
  fi
done

printf "Unconfigured interfaces:\n"
printf "  %${IF_MAXWIDTH}s\n" "${UNUSED_IFS[@]}"
