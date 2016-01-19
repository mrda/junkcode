#!/bin/bash
#
# delete-lxc-containers.sh - deleet and cleanup lxc containers
#
# Copyright (C) 2016 Michael Davies <michael@the-davies.net>
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

# TODO(mrda): Add in confirmation

read -p "Are you sure you want to delete your lxc containers? " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    for i in $(lxc-ls)
    do
        echo "Deleting \"$i\""
        lxc-stop -n $i
        lxc-destroy -n $i
        if [ -d "${i}" ]; then
            rm -rf "/openstack/$i"
        fi
    done
else
    echo "Ok, won't do anything"
fi

