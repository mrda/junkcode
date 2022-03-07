#~/bin/sh
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

# There are some things we always want running
declare -a REQDPROGS=( poll-internet slack )
for PROG in "${REQDPROGS[@]}"; do
    if ! check_process_running ${PROG} ; then
        print_message_box "The program \"${PROG}\" is not running"
    fi
done

# Reauthenticate if we can
run_if_avail rhauth.sh

# See if there's any software updates
if [ -f /etc/redhat-release ]; then
    if is_available dnf ; then
        if ! dnf check-update >& /dev/null ; then
            echo "There are software updates available via dnf"
        fi
    else
        echo "There's no 'dnf' available"
    fi
else
    echo "You're not using a supported operating system, so I can't check for available updates"
fi
