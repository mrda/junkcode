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
__does_command_exist ()
{
    hash ${1} &> /dev/null
    return $?
}

__does_command_exist lolcat
if [ $? -eq 0 ]; then

addlols ()
{
"$@" | lolcat
}

function colourise () {
    alias $1="addlols $1"
}

colourise ls
colourise find
colourise ps
colourise history
colourise git
colourise pwd

fi

echo "You need to source this script, like this: . $0"
