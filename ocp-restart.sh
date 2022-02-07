#!/bin/sh
#
# ocp-restart.sh - Restart OCP cluster running in kvm
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

ensure_cmd virsh
ensure_cmd oc

CONNECT="${CONNECT:=qemu:///system}"

INACTIVES=0
for DOMAIN in $(virsh -c "${CONNECT}" list --inactive --name | grep "$USER"); do
    virsh -c "${CONNECT}" start "$DOMAIN"
    INACTIVES=1
done

if [[ "$INACTIVES" == "0" ]]; then
    echo "No inactive VMs found"
    exit 0
else  # "$INACTIVES" == "1"

    timebar 1 "Waiting for VMs to rehydrate"

    virsh -c "${CONNECT}" list --all | grep "$USER"

    echo "*** Control Plane Nodes ***"
    oc get nodes -l node-role.kubernetes.io/master

    echo "*** Worker Nodes ***"
    oc get nodes -l node-role.kubernetes.io/worker

    echo "*** Cluster Operators ***"
    oc get clusteroperators

cat << EOF

Note:

If we have any issues you might want to look at certificates, i.e.

oc get csr
oc describe csr <csr_name>
oc adm certificate approve <csr_name>

See also https://docs.openshift.com/container-platform/4.9/backup_and_restore/graceful-cluster-restart.html#graceful-restart-cluster

EOF

fi
