#!/bin/bash
#
# ensure-net-ifaces.sh <list if net ifaces> - Makes sure the supplied list
#                                             of network interfaces are
#                                             present
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
#
ensure-net-ifaces ()
{
    mapfile -t ALL_IFACES < <( ls -1 /sys/class/net )

    for IFACE in "$@"; do
        [[ ! " ${ALL_IFACES[@]} " =~ " ${IFACE} " ]] && printf "${IFACE} not in \"%s\"\n" "${ALL_IFACES[*]}" && exit 1
    done
    exit 0
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && ensure-net-ifaces $@
