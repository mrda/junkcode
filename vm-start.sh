#!/usr/bin/bash
#
# vm-start.sh - Start a stopped VM
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
MYNAME=$(basename $0)

[[ $EUID -ne 0 ]] && \
printf "$MYNAME: Sorry, you need to run this as root\n" && \
exit 1

VM_NAMES=($(virsh list --inactive | tail -n +2 | awk '{print $2}'))

[[ $# -ne 1 ]] && printf "Usage: $MYNAME <vm-name>\n" && \
    printf "Available <vm-name>s are: ${VM_NAMES[*]}\n" && exit 2

if [[ ! " ${VM_NAMES[@]} " =~ " $1 " ]]; then
    printf "$MYNAME: Unknown <vm-name>\n"
    printf "Available <vm-name>s are: ${VM_NAMES[*]}\n"
    exit 3
fi

virsh start $1
