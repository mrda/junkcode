#!/bin/sh
#
# ocp-suspend.sh - Suspend OCP cluster running in kvm
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

# Include bash library
command -v bashlib.sh &> /dev/null || \
{ echo >&2 "$(basename $0): Can't find bashlib.sh.  Aborting."; exit 1; }
. bashlib.sh

ensure_cmd oc
ensure_cmd virsh

CONNECT="${CONNECT:=qemu:///system}"

if $(virsh -c "${CONNECT}" list --all | grep "$USER" | grep 'shut off' >/dev/null 2>&1); then
    echo "There are **no** VMs that need suspending"
    exit 0
fi

echo -n "Current time in UTC: "
TZ=UTC date

echo "Current VMs state for $USER..."

virsh -c "${CONNECT}" list --all | grep "$USER"

for node in $(oc get nodes -o jsonpath='{.items[*].metadata.name}'); do
  oc debug node/${node} -- chroot /host shutdown -h 1
done

timebar 4 "Sleeping to give VMs time to shutdown"

echo "Current VMs state for $USER..."
virsh -c "${CONNECT}" list --all | grep "$USER"
