#!/usr/bin/bash
#
# vm-ssh.sh - ssh to <user> on <vm>
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

[[ $# -ne 2 ]] && printf "Usage: $MYNAME <user> <vm-name>\n" && exit 2

VM_NAMES=($(virsh list | tail -n +2 | awk '{print $2}'))

[[ ! " ${VM_NAMES[@]} " =~ " $2 " ]] && \
    printf "$MYNAME: Couldn't find vm '$2'\n" && \
    exit 3

IP_ADDRS=$(virsh domifaddr $2 | tail -n +2 | awk '{print $4}' | cut -f1 -d"/")

[[ -z $IP_ADDRS ]] && printf "$MYNAME: No IP addresses found for $2\n" && \
    exit 4

# Grab the real pre-sudo username
USERNAME=$(pstree -lu -s $$ | grep --max-count=1 -o '([^)]*)' | head -n 1 | tr -d '()')

for IP in ${IP_ADDRS[*]}; do
    ping -c1 $IP >& /dev/null
    if [ $? -eq 0 ]; then
        # TODO: Don't assume that id_rsa is the key to use
        ssh -i /home/${USERNAME}/.ssh/id_rsa $1@$IP
        exit 0
    fi
done
printf "$MYNAME: No routable interface found for $2\n"
exit 5
