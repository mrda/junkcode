#!/bin/bash
#
# Pretty print a password provided on the command-line or prompted for
# NOTE: This is not secure.  Caveat emptor.  Proof of concept only.
#
# Copyright (C) 2019, 2022 Michael Davies <michael@the-davies.net>
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

# WARN(mrda): This is a very simplistic attempt to hide command-line params
# This is really problematic for many reasons:
# 1) if someone is inotifying /proc/$$/cmdline they'll see your password
# 2) if someone grabs the process table after this script runs, and before
#    the exec call, you're snaffled too (i.e. timing attack)
# 3) And if you run GNOME or something else that grabs the command-line
#    to let you know when the command completes, you'll have the command line
#    stored, and printed. Whoops.
# 4) Don't forget your shell's history.  We can't prevent that from being
#    saved from inside this script. KAPOW!
# 5) And you can be p4wn3d in many other ways too.
#
# So don't do this, really.  It's not secure
#

# Include bash library
command -v bashlib.sh &> /dev/null || \
{ echo >&2 "$(basename $0): Can't find bashlib.sh.  Aborting."; exit 1; }
. bashlib.sh

# Exec ourselves, storing the cmdline params in a subshell env var
BGSECRET="startinbackground"
if [ "$BGS" != "$BGSECRET" ]; then
    export BGS="$BGSECRET"
    export PARAM1=$1
    if [ ! -z $PARAM1 ]; then
        echo "WARNING: Passwords provided on the command-line are not"
        echo "         secure.  You should consider them compromised!"
    fi
    exec "$0"
fi

# If the password wasn't provided on the command line
# prompt for it
while [ -z $PARAM1 ]; do
    read -p "Enter the string to pretty print: (^C to exit) " PARAM1
done

colourprint $PARAM1

# If we can print things phonetically, and speak it out, do that as well
PHONETIC='phonetic.py'
SAY='espeak'
SAY_PARAMS='-ven -s 100'
if hash $PHONETIC &> /dev/null; then
    $PHONETIC $PARAM1
    if hash $SAY &> /dev/null; then
        $PHONETIC $PARAM1 | $SAY $SAY_PARAMS
    fi
fi

