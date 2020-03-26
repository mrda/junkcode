#!/usr/bin/bash
#
# vm-list.sh - list the currently running VMs and their IP addresses
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
[[ $EUID -ne 0 ]] && \
printf "$(basename $0): Sorry, you need to run this as root\n"

VM_NAMES=($(virsh list | tail -n +2 | awk '{print $2}'))

printf "%s\n" "------ Active VMs ------"
for VM in ${VM_NAMES[*]}; do
    IPS=()
    VM_IP=($(virsh domifaddr $VM | tail -n +2 | awk '{print $4}' \
           | cut -f1 -d"/"))
    printf "$VM ${VM_IP[*]}\n"
done

printf "\n%s \n" "----- Inactive VMs -----"
INACTIVE_VM_NAMES=($(virsh list --inactive | tail -n +2 | awk '{print $2}'))
printf "${INACTIVE_VM_NAMES[*]}\n\n"
