#!/bin/bash
#
# life-reader.sh - read .cells files, and decipher row/col coords
#
# Copyright (C) 2020 Michael Davies <michael@the-davies.net>
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
[[ ! -r $1 ]] && printf "%s: Please provide a file to decipher\n" $(basename $0) && exit 1

row=0
while read -ra LINE; do
    for (( i=0; i<${#LINE}; i++ )); do
        [[ "${LINE:$i:1}" == "O" ]] && printf "row $row col $i\n"
    done
    ((row++))
done < "$1"
