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

# Turn on debugging if requested
DEBUG="${DEBUG:-0}"
[[ $DEBUG -eq 1 ]] && set -xev

# Check to see if this library is being sourced
IS_SOURCED=1
SCRIPTNAME=unknown
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    SCRIPTNAME=$(basename $0)
    IS_SOURCED=0
fi

# Check to see if this is an interactive shell
IS_INTERACTIVE=0
if [[ $- == *i* ]]; then
  IS_INTERACTIVE=1
fi

# See if a certain command is available
is_available() {
    command -v "$1" &> /dev/null
}

# Run command, including it's parms, if available
run_if_avail() {
    if is_available "$1" ; then
        $@
    fi
}

# Ensure a certain command is available, exit if it doesn't
# $1: the command to test for
ensure_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "*** Required command "$1" doesn't exist"
        [[ $IS_SOURCED -ne 1 ]] && exit 3
    fi
}

ensure_cmd basename
ensure_cmd id
ensure_cmd stat
ensure_cmd zenity

# See if a process is running
check_process_running() {
    $(ps aux | grep "$1" | grep -v grep >& /dev/null);
}

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

# Print the character "$1" the number of times given by "$2"
print_char ()
{
    # $3 is a secret param, provided to help print_line :)
    printf "%0$2s$3" | tr " " "$1"
}

# Print the character "$1" the number of times given by "$2" with newline
print_line ()
{
    print_char $1 $2 $'\n'
}

# Display the message $1 in a box made up of $2 characters,
# with $2 being optional
# Note that you need to handle \n's correctly, i.e.
# print_message_box $'This is a \ntest message\nsplit over several lines' 'X'
# print_message_box $'This is a \ntest message\nsplit over several lines'
print_message_box ()
{
    local CHAR ARR MAXLEN BOXLEN

    # If no box char specified...
    CHAR=$2
    [[ "z${CHAR}" == "z" ]] && CHAR="#"

    readarray ARR <<< $1

    # Find longest line length, and remove pesky newline characters
    MAXLEN=0
    for IDX in "${!ARR[@]}"; do
        ARR[IDX]=$(tr -d $'\n' <<< ${ARR[IDX]})
        [[ ${#ARR[IDX]} -gt $MAXLEN ]] && MAXLEN=${#ARR[IDX]}
    done
    BOXLEN=$((MAXLEN+4))  # $CHAR and a space either side

    print_line ${CHAR} ${BOXLEN}
    for ELEM in "${ARR[@]}"; do
        printf "${CHAR} %-${MAXLEN}s ${CHAR}\n" "${ELEM}"
    done
    print_line ${CHAR} ${BOXLEN}
}

# Busy-wait for $1 minutes, using $2 as a title (optional)
# If $2 isn't supplied, "Time Remaining:" is used
# This relies on having a smart tty device that can handle line redraws
timebar() {
    TOTSECS=$(( $1 * 60 ))
    MINS=$(($1-1))
    LEN=30

    TITLE=${2:-"Time Remaining:"}

    for m in $(seq $MINS -1 0) ; do
        for s in $(seq 59 -1 0) ; do
            SECS_REMAINING=$(( $m*60 + $s ))
            PERCENT=$(bc <<< "scale=0; ($TOTSECS - $SECS_REMAINING) * 100 / $TOTSECS")
            NUMHASHES=$( bc <<< "scale=0; (($LEN * $PERCENT) / 100)" )
            NUMDOTS=$( bc <<< "scale=0; $LEN - $NUMHASHES" )

            HASHES=""
            if [ $NUMHASHES -ne 0 ]; then
                HASHES=$( printf "%-${NUMHASHES}s" "#" )
                HASHES=${HASHES// /#}
            fi

            DOTS=""
            if [ $NUMDOTS -ne 0 ]; then
                DOTS=$( printf "%-${NUMDOTS}s" "." )
                DOTS=${DOTS// /.}
            fi
            printf "\r%s %02d:%02d [ %s%s ] %01d%% " "$TITLE" $m $s "$HASHES" "$DOTS" $PERCENT
            sleep 1s
        done
    done
    echo ""
}

beep ()
{
    echo -en "\007"
}

# Display a modal dialog box, blocking until the user acks
# $1 is the title
# $2 is the message to display
dialogbox ()
{
    TITLE=${1:-"Title goes here"}
    BODY=${2:-"Message goes here"}
    zenity --info --text="$BODY" --title="$TITLE" --width=300 --height=200 >& /dev/null
}

# Re-run this script in the background in a seamless way
# Note that you lose stdin and stdout as a result
backgroundme ()
{
    PASS="startinthebackground"
    if [ "$SCB" != "$PASS" ]; then
        export SCB="$PASS"
        nohup "$0" "$@" </dev/null >/dev/null 2>&1 &
        exit
    fi
}
