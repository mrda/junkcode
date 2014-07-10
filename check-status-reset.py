#!/usr/bin/env python
#
# check-status-reset.py - Reset whatever check-status.sh did
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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
import os
import time
from subprocess import call

TMP_FILE = os.getenv('CHECK_STATUS_TIMESTAMP', '/tmp/.check_status_timestamp')
CHECK_STATUS_RESET = os.getenv('CHECK_STATUS_RESET',
                               '/home/mrda/bin/noarch/blink-off.sh')

# Duration in seconds
DURATION = 150

with open(TMP_FILE, 'r') as f:
    timestamp = int(f.read())
    now = int(time.time())

    if (now - timestamp) > DURATION:
        call([CHECK_STATUS_RESET])
