#!/bin/bash
#
# ensure-macs.sh <list of mac addrs> - Makes sure the supplied list
#                                      of MAC addresses are
#                                      present
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
ensure-macs ()
{
    mapfile -t ALL_MACS < <( ip link | grep link\/ether | awk '{ print $2 }' )

    for MAC in "$@"; do
        [[ ! " ${ALL_MACS[@]} " =~ " ${MAC} " ]] && printf "${MAC} not in \"%s\"\n" "${ALL_MACS[*]}" && exit 1
    done
    exit 0
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && ensure-macs $@
