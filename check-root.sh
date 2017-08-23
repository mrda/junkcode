#!/bin/bash
#
# check-root.sh - example test for running as root
#                 Note: This isn't tsting for the root user, but
#                 whether you are effectively running as root.
#                 i.e. either the root user, or sudo privilege escalation
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
if [[ $EUID -eq 0 ]]; then
   echo "You are running as root" 1>&2
else
   echo "You are NOT running as root" 1>&2
fi

