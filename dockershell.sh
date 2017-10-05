#!/usr/bin/env bash
#
# dockershell.sh <pattern> - start a bash shell on the first docker
#                            process matching <pattern>
#
# Copyright (C) 2017 Michael Davies <michael@the-davies.net>
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

__check_cmd_avail ()
{
    if ! hash ${1} &> /dev/null; then
        echo "The command '$1' could not be found, exiting"
        exit 1
    fi
}

# Verify we have the commands we need
DOCKER=docker
__check_cmd_avail ${DOCKER}

USAGE="$(basename $0) <pattern>: Please specify a docker name pattern"
if [ $# -eq 0 ]; then
  echo ${USAGE}
  exit 2
fi

PATTERN=$1
FIRST_PROC=$(${DOCKER} ps -a | grep ${PATTERN} | head -1)
FIRST_PROC_ID=$(echo "${FIRST_PROC}" | cut -f1 -d" ")

if [ -z "${FIRST_PROC}" ]; then
    echo "No process found matching \"${PATTERN}\""
    exit 3
fi

${DOCKER} exec -it "${FIRST_PROC_ID}" bash
