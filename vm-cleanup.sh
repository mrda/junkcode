#!/usr/bin/bash
#
# Cleanup local VMs and associated assets
# Adapted from original version by Andy McCrae <andy.mccrae@gmail.com>
#
# Copyright (C) 2021 Michael Davies <michael@the-davies.net>
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
[[ $EUID -ne 0 ]] && printf "$(basename $0): Sorry, you need to run this as root\n" && exit 1

USAGE="Usage: $(basename $0) <vm name>\nSee 'virsh list' for possible <vm name>s\n"
[ $# -ne 1 ] && printf "$USAGE" && exit 0

INSTALL_NAME=${1:-}

echo "cleaning up $INSTALL_NAME"
for i in `virsh list --all | grep $INSTALL_NAME | awk '{print $2}'`; do
  echo "cleaning up instances"
  if virsh list | grep -q $i; then
    virsh destroy $i
  fi
  virsh undefine $i
done

if virsh net-list --all | grep -q $INSTALL_NAME; then
  echo "cleaning up network"
  if virsh net-list | grep -q $INSTALL_NAME; then
    virsh net-destroy $INSTALL_NAME;
  fi
  virsh net-undefine $INSTALL_NAME;
fi

if virsh pool-list --all | grep -q $INSTALL_NAME; then
  echo "cleaning up storage pool"
  if virsh pool-list | grep -q $INSTALL_NAME; then
    virsh pool-destroy $INSTALL_NAME;
  fi
  rm -rf /var/lib/libvirt/openshift-images/$INSTALL_NAME*;
  virsh pool-undefine $INSTALL_NAME;
fi
