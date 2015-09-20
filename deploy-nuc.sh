#!/bin/bash
#
# deploy-nuc.sh - helper script to deploy a NUC
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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

# Change these settings to match your environment
export NUC="<NUCNAME>"
export NUCMAC="**:**:**:**:**:**"
export NUCIP="<NUC IP ADDRESS>"
export NUCPORT="16992"
export NUCADMIN="admin"
export NUCPASSWORD="<NUCPASSWORD>"   # Remember to escape $ and \
export NUCDEPLOYKERNEL="file:///Images/deploy-ramdisk.kernel"
export NUCDEPLOYIMAGE="file:///Images/deploy-ramdisk.initramfs"
export NUCUSERIMAGE="file:///Images/user-image"


# Fake authentication, and point to where ironic-api is running
export OS_AUTH_TOKEN=fake-token
export IRONIC_URL=http://localhost:6385/

# Unenroll and delete the nuc if it's there
ironic node-set-maintenance ${NUC} on &> /dev/null
ironic node-delete ${NUC} &> /dev/null

# Deploy!
ironic node-create -d pxe_amt -n ${NUC} -i amt_password=${NUCPASSWORD} -i amt_username=${NUCADMIN} -i amt_address=${NUCIP} -i deploy_ramdisk=${NUCDEPLOYIMAGE} -i deploy_kernel=${NUCDEPLOYKERNEL}

ironic node-update ${NUC} add instance_info/image_source=${NUCUSERIMAGE}.qcow2 instance_info/kernel=${NUCUSERIMAGE}.vmlinuz instance_info/root_gb=10 instance_info/ramdisk=${NUCUSERIMAGE}.initrd

NODEUUID=$(ironic node-list | tail -n +4 | head -n -1 | awk -F "| " '{print $2}')

ironic port-create -n ${NODEUUID} -a ${NUCMAC}

ironic node-validate ${NUC}

# Make sure the AMT interface is awake before we kick off the provision
while true; do
    nc -zv ${NUCIP} ${NUCPORT}
    if [ "$?" == "0" ]; then
        break;
    fi;
done

ironic node-set-provision-state ${NUC} active
