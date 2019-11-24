#!/bin/bash
#
# colourise.sh - make your shell a little more colourful
#                You need to source this, i.e. ". ./colourise.sh"
#
# Brought to you by "Friday afternoon hacks of sillyness".
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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

# Notes: Launching an editor from git once colourised breaks things.
COMMANDS=( ls find ps history pwd )

[[ "${BASH_SOURCE[0]}" == "$0" ]] && echo "You need to source this script, like this: . $0"  && exit 1

hash lolcat &> /dev/null
if [ $? -eq 0 ]; then

function addlols ()
{
"$@" | lolcat
}

for CMD in "${COMMANDS[@]}"; do
    alias $CMD="addlols $CMD"
done

fi
