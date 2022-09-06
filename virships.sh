#!/bin/sh
#
# virships.sh - print ip addresses associated with virsh vms
#
# Copyright (C) 2022 Michael Davies <michael@the-davies.net>
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

#CONNECT='-c qemu:///system'
CONNECT=

VM_NAMES=( $(virsh ${CONNECT} list | awk 'NR>2 { print $2 }') )
for VM in ${VM_NAMES[*]}; do
    IPADDRS=( $(virsh ${CONNECT} domifaddr ${VM} |\
        awk 'NR>2 { split($4, ip, "/"); print ip[1] }' ) )
    printf "${VM} ${IPADDRS[*]}\n"
done
