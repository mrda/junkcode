#!/usr/bin/env bash
#
# Bash library functions
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

# Ensure a certain command is available, exit if it doesn't
# $1: the command to test for
ensure_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "*** Required command "$1" doesn't exist"
        exit 3
    fi
}

ensure_cmd basename
ensure_cmd id
ensure_cmd stat

# What the invoking script name is
SCRIPTNAME=$(basename $0)

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

# Ensure a certain directory exists, if it doesn't, create it if possible
# $1: the directory to test for/create
ensure_dir ()
{
    if [ ! -d "${1}" ]; then
        mkdir -p ${1} >& /dev/null
        if [[ $? -ne 0 ]]; then
            echo "*** Couldn't create directory ${1}"
            exit 2
        fi
    fi
}

# Change to the specified directory if possible, exit if we can't
# $1: the directory to go to
change_dir ()
{
    if [[ ! "z$(pwd)" == "z${1}" ]]; then
        cd ${1}
        if [[ $? -ne 0 ]]; then
            echo "*** Couldn't change directory to ${1}"
            exit 3
        else
            echo "--- Changing directory to $(pwd)"
        fi
    fi
}

# Check that there's enough disk space available on the local filesystem
# Exit if there isn't
# $1: the required amount of disk space
check_disk_space ()
{
    local FREE_SPACE=$(($(stat -f --format="%a*%S" .)))
    if [[ ${FREE_SPACE} -lt ${1} ]]; then
        echo "*** Not enough disk space. ${FREESPACE} available, require ${1}."
        echo "Exiting..."
        exit 4
    fi
}

# Check that this script is running as the specified user, exit if not
# $1: the user this should be running as
check_user ()
{
    if [ "z$(id -u -n)" != "z${1}" ]; then
        echo "${SCRIPT}: Please re-run this script as the '${1}' user"
        exit 5
    fi
}

# Prompt the user with a string, asking whether the script should continue
# Y means continue, N means exit
# $1: prompt string
confirm_continue ()
{
    local EXIT_LOOP=0
    while [[ ${EXIT_LOOP} -ne 1 ]]; do
        read -p "${1}" -r
        if [[ ${REPLY} =~ ^[Nn]$ ]]; then
            echo "*** Exiting..."
            exit 6
        fi
        if [[ ${REPLY} =~ ^[Yy]$ ]]; then
            EXIT_LOOP=1
        fi
    done
}

# Allow the user to choose from a number of options
# $1: prompt string
# $2: array of choices
# $3: the variable to update with the selected choice
choose_option ()
{
    local OLDIFS=$IFS
    IFS=$'\n'

    declare -a OPT=("${!2}")
    local EXIT_LOOP=0
    while [ $EXIT_LOOP -ne 1 ];
    do
        j=0
        echo $1
        for i in ${OPT[@]}
        do
            echo $j - $i
            j=$[j+1]
        done

        read -p "Which option would you like to choose? " -r
        if [ ${REPLY} == "q" ]; then
            EXIT_LOOP=1
        else
            if [ ${REPLY} -ge 0 ] && [ ${REPLY} -lt $j ] || \
               [ ${REPLY} == "q" ]; then
                EXIT_LOOP=1
            else
                echo "\"${REPLY}\" is not a valid option, please choose again"
            fi
        fi
    done

    IFS=$OLDIFS

    if [ ${REPLY} == "q" ]; then
        eval "${3}='"${REPLY}"'"
    else
        eval "${3}='"${OPT[$REPLY]}"'"
    fi
}

