#!/bin/sh
#
# check-status - Run the provided command, checking the return status.
#                If it's zero, invoke the ${CHECK_STATUS_SUCCESS}
#                command (if provided, otherwise use a default).
#                Otherwise, run the ${CHECK_STATUS_FAILURE} command
#                (if provided, otherwise use a default)
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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

blink1-tool --off >/dev/null 2>&1

# Run whatever, just pass it all through
"$@"
status=$?

if [ ${status} -eq 0 ]; then
    ${CHECK_STATUS_SUCCESS:-blink1-tool --green} >/dev/null 2>&1
else
    ${CHECK_STATUS_FAILURE:-blink1-tool --red} >/dev/null 2>&1
fi

# Keep track of when we run check_status
TMPFILE=${CHECK_STATUS_TIMESTAMP:-/tmp/.check_status_timestamp}
date '+%s' > ${TMPFILE}

exit ${status}

