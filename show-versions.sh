#!/usr/bin/env bash
#
# show-versions.sh - Print out what we know about software on this machine
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
PAD=15

ARCH=$(arch)
EXTRA=""
[[ $ARCH != "x86_64" ]] && EXTRA=" ($(LD_SHOW_AUXV=1 /bin/true | grep AT_PLATFORM | cut -f2 -d':' | tr -d '[:blank:]')) "

printf "%${PAD}s %s%s\n" "Architecture:" "$ARCH" "$EXTRA"

[[ -r /etc/redhat-release ]]  && \
  printf "%${PAD}s %s\n" "RHEL:" "$(cat /etc/redhat-release)"

[[ -r /etc/rhosp-release ]] && \
  printf "%${PAD}s %s\n" "RHOS:" "$(cat /etc/rhosp-release)"

[[ -r /var/lib/rhos-release/latest-installed ]] && \
  printf "%${PAD}s %s\n" "RHOS Puddle:" \
         "$(cat /var/lib/rhos-release/latest-installed)"

if command -v "rhos-release" &> /dev/null; then
  printf "%${PAD}s %s\n" "Yum Repos:" \
         "$(rhos-release -L | tail -n +2 | tr -d '\n' | \
  sed -e 's/^[[:space:]]*//')"
fi

if command -v "oc" &> /dev/null; then
    OCP_VERSION="$(oc version 2>/dev/null | grep Server | cut -f2 -d':' | tr -d '[:blank:]')"
    [[ "$OCP_VERSION" != "" ]] && printf "%${PAD}s %s\n" "OCP Version:" "$OCP_VERSION"
fi

if command -v "loginctl" &> /dev/null; then
    DISPLAY_SERVER="$(loginctl show-session 2 -p Type 2>/dev/null | cut -f2 -d'=')"
    [[ "$DISPLAY_SERVER" != "" ]] && printf "%${PAD}s %s\n" "Display Server:" "$DISPLAY_SERVER"
fi
