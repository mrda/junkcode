#!/bin/bash
#
# bashshuf - Example script to show how to shuffle an array
#            Invoke via `array_shuffle ARRAYNAME`.
#
#            i.e. you just provide the NAME of the array,
#            and the functions grabs the contents of the
#            array and overwrites it with the shuffled
#            contents.
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
array_shuffle ()
{
    # Keep a copy of the input array name for copying over once
    # we've made a shuffled copy of the input array
    local ARRAY_NAME=$1

    # Build up the input array name, forcing the variable to
    # to look like an array variable
    local ARRAY_NAME_AS_ARRAY=$ARRAY_NAME[@]

    # Dereference the input array name, getting us the array
    local INPUT_ARRAY=( ${!ARRAY_NAME_AS_ARRAY} )

    # Grab the index of the last element
    local LAST_ELEM_IDX=$(( ${#INPUT_ARRAY[@]} - 1 ))

    # Create a new shuffled list of array indexes
    local NEW_IDX_SEQ=$( shuf -i 0-$LAST_ELEM_IDX )

    # Create a new array by copying the input array,
    # using the shuffled indexes
    declare -a OUTPUT_ARRAY
    for i in $NEW_IDX_SEQ; do
        OUTPUT_ARRAY+=( ${INPUT_ARRAY[$i]} )
    done

    # Assign the new array on top of the input array
    eval unset $ARRAY_NAME
    eval $ARRAY_NAME="'${OUTPUT_ARRAY[*]}'"
}

if [[ $1 == "-h" ]]; then
    printf "Usage: %s -h | [<list of items to shuffle>]\n" $(basename $0)
    exit 1
fi

if [[ $# -eq 0 ]]; then
    printf "%s: No list provided, supplying an example\n" $(basename $0)
    MYARR=( john paul george ringo )
else
    MYARR=( "$@" )
fi

array_shuffle MYARR
printf "${MYARR[*]}\n"
