#!/usr/bin/bash
#
# vm-create.sh - create a new VM
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

[[ $# -ne 2 ]] && printf "Usage: $MYNAME <os> <vm-name>\n" && exit 1

[[ ! -d ${HOME}/src/mongrel-punt ]] && \
    printf "$MYNAME: Cannot find mongrel-punt\n" && \
    printf "You can install it as follows: " && \
    printf "mkdir -p $HOME/src && cd $HOME/src && " && \
    printf "git clone https://github.com/mrda/mongrel-punt.git\n" && \
    exit 2

OSES=()
for NAME in $(find $HOME/src/mongrel-punt -name inventory\*); do
    FN=$(basename -s .yml $NAME | cut -f2 -d'-')
    OSES+=( $FN )
done

if [[ ! " ${OSES[@]} " =~ " $1 " ]]; then
    printf "$MYNAME: '$1' is an unsupported <os>\n"
    printf "$MYNAME: The list of supported <os> are: ${OSES[*]}\n"
    exit 3
fi

printf "$MYNAME: Build a VM named '$2' with operating system '$1'\n"

cd $HOME/src/mongrel-punt
ansible-playbook -K -i inventory-$1.yml playbooks/build-vm.yml -e "name=$2"
