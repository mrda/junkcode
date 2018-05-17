#!/bin/sh
#
# Simple tests for bashlib
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

. $(dirname $0)/bashlib.sh

test_ensure_cmd() {
    # Shell built-in
    assertReturn "$(ensure_cmd 'hash')" 0
    # Commands that exist
    assertReturn "$(ensure_cmd 'ls')" 0
    assertReturn "$(ensure_cmd '/bin/bash')" 0
    # Commands that don't exist
    assertReturn "$(ensure_cmd 'frobnitz')" 3
    assertReturn "$(ensure_cmd '/usr/share/lib/i-dont-exist')" 3
}

test_scriptname() {
    assertEqual "$SCRIPTNAME" "test-bashlib.sh"
}

BASHLIB=$(dirname $0)/../bashunit/bashunit.bash
if [ -f "$BASHLIB" ]; then
    . "$BASHLIB"
else
    echo "*** You need to git clone https://github.com/djui/bashunit"
    exit 3
fi
