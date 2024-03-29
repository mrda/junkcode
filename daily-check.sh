#!/bin/sh
#
# daily-check.sh - make sure things are running, reauthentication
#                  is done, things that you want to do everyday
#
# Copyright (C) 2022 Michael Davies <michael@the-davies.net>
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

# Include bash library
command -v bashlib.sh &> /dev/null || \
{ echo >&2 "$(basename $0): Can't find bashlib.sh.  Aborting."; exit 1; }
. bashlib.sh

# Command line argument processing
NOASK=0
for ARG in "$@"; do
    case $ARG in
        -h)
            echo >&2 "Usage: $(basename $0) [-h] [-n]"
            echo >&2 "  -h display this help"
            echo >&2 "  -n ask before applying updates"
            exit 1
            ;;
        -n)
            NOASK=1
            ;;
        *)
            ;;
    esac
done

# There are some things we always want running
declare -a REQDPROGS=( poll-internet slack )
for PROG in "${REQDPROGS[@]}"; do
    if ! check_process_running ${PROG} ; then
        print_message_box "The program \"${PROG}\" is not running"
    fi
done

update_dnf ()
{
    if is_available dnf ; then
        if ! dnf check-update >& /dev/null ; then
            if [ $NOASK -eq 1 ]; then
                confirm_continue "Do you want to install software updates? "
            fi
            sudo dnf update -y
        fi
    else
        echo "There's no 'dnf' available"
    fi
}

update_flatpak ()
{
    # flatpak
    if is_available flatpak ; then
        sudo flatpak update --noninteractive >& /dev/null
    else
        if [ ! -e ${HOME}/.flatpak ]; then
            echo "There's no 'flatpak' available"
            touch ${HOME}/.flatpak
        fi
    fi
}

update_snap ()
{
    # flatpak
    if is_available snap ; then
        sudo snap refresh >& /dev/null
    else
	if [ ! -e ${HOME}/.snap ]; then
            echo "There's no 'snap' available"
            touch ${HOME}/.snap
        fi
    fi
}

# Reauthenticate if we can
run_if_avail auth.sh

# See if there's any software updates
OSTYPE=$( guess_os )
if [ "${OSTYPE}" = "Red Hat" ]; then
    update_dnf
    update_flatpak
    update_snap  # ...even though this isn't really a thing on Red Hat
else
    echo "You're not using a supported operating system, so I can't check for available updates"
fi
