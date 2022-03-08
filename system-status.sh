#!/bin/bash
#
# system-status - tell me interesting things about my linux box
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
_check_cmd_avail ()
{
    if ! hash ${1} &> /dev/null; then
        echo "The required command '$1' could not be found, exiting"
        exit 1
    fi
}
_check_cmd_avail neofetch
_check_cmd_avail dnf

neofetch
printf "\nSystem Info:\n"
sudo dmidecode -t system
printf "\nUptime:\n"
uptime
printf "\nMeminfo:\n"
awk '$3=="kB"{$2=$2/1024**2;$3="GB";} 1' /proc/meminfo | column -t
printf "\nProcesses:\n"
ps -aef --forest
printf "\nMounts:\n"
findmnt -lo source,target,fstype,label,options,avail,used
printf "\nServices:\n"
systemctl --no-pager
printf "\nRPM Repositories:\n"
dnf repolist
printf "\nInstalled Packages:\n"
dnf list installed
