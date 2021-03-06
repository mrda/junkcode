#!/bin/bash
#
# check-command.sh - small smaple code showing how to test
#                    for the availability of a command
#
# Copyright (C) 2017 Michael Davies <michael@the-davies.net>
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
__does_command_exist ()
{
    hash ${1} &> /dev/null
    return $?
}

__check_cmd_avail ()
{
    if hash ${1} &> /dev/null; then
        echo "$1 exists"
    else
        echo "$1 does NOT exist"
    fi
}

# Ensure a command was provided
if [ $# -eq 0 ]; then
  echo "Usage: $(basename $0) <command>"
  exit 1
fi

__check_cmd_avail ${1}
