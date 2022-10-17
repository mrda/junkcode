#!/bin/bash
#
# Print the latencies between a list of IP Addresses
#
# Copyright (C) 2022 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#

# Set IPADDRS and DEFAULT_IF in your environment if you want something else
#
# These are my default IPs for OCP libvirt VMs
IPADDRS=${IPADDRS:-192.168.131.11 192.168.131.12 192.168.131.13 192.168.131.51 192.168.131.52}
DEFAULT_IF=${DEFAULT_IF:-enc2}  # Default network interface for rhel8

display_usage ()
{
    printf "%s [-h] \n" $(basename $0)
    printf "  -h  display this help\n"
    printf "This script recognises the following environment variables:\n"
    printf "  DEFAULT_IF - the default network interface on this machine\n"
    printf "  IPADDRS    - space seperated list of IP addresses to poll\n"
}

for ARG in "$@"; do
    case $ARG in
        -h)
            display_usage
            exit 0
            ;;
        *)
            ;;
    esac
done

clear
echo -n 'My IP Address: '
ip addr show $DEFAULT_IF | grep 'inet ' | awk -F'[: /]+' '{ print $3 }'
for IP in $IPADDRS; do
    ping -c 1 $IP | grep from | cut -f4,7 -d' '
done
