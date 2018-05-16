#!/usr/bin/env bash
#
# Bash string library functions
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
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

# Get a non-empty string and store it in the provided variable
# $1: variable to update
# $2: prompt string
get_non_empty_str ()
{
    local EXIT_LOOP=0
    while [[ ${EXIT_LOOP} -ne 1 ]];
    do
        read -p "${2}" -r
        if [[ ! -z "${REPLY}" ]]; then
            eval "${1}='"${REPLY}"'"
            EXIT_LOOP=1
        fi
    done
}
