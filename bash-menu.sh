#!/bin/bash
#
# bash-menu.sh - sample text menu in bash
#
# Copyright (C) 2016 Michael Davies <michael@the-davies.net>
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

___choose_option ()
# $1 is the prompt string, $2 is the array of choices, $3 is the selected choice
{
    declare -a OPT=("${!2}")
    EXIT_LOOP=0
    while [ $EXIT_LOOP -ne 1 ];
    do
        j=0
        echo $1
        for i in ${OPT[@]}
        do
            echo $j $i
            j=$[j+1]
        done

        read -p "Which option would you like to choose? " -r
        if [ $REPLY -gt 0 ] && [ $REPLY -lt $j ]
        then
            EXIT_LOOP=1
        else
            echo "\"$REPLY\" is not a valid option, please choose again"
        fi
    done

    eval "$3=${OPT[$REPLY]}"
}

OPTIONS=( ham eggs bacon spam tofu banana )

___choose_option "Please choose your breakfast option" OPTIONS[@] YOURCHOICE

echo "The user selected \"$YOURCHOICE\""

