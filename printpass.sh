#!/bin/bash
#
# Pretty print a password provided on the command-line or prompted for
# NOTE: This is not secure.  Caveat emptor.  Proof of concept only.
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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

# Control codes to change colour on the terminal
FG_CLEAR="\033[0m"
FG_BLACK="\033[0;30m"
FG_RED="\033[0;31m"
FG_GREEN="\033[0;32m"
FG_YELLOW="\033[0;33m"
FG_BLUE="\033[0;34m"
FG_MAGNETA="\033[0;35m"
FG_CYAN="\033[0;36m"
FG_WHITE="\033[0;37m"

colourprintchar () {
    LETTER_COLOUR=$FG_WHITE
    UPPER_COLOUR=$FG_YELLOW
    NUMBER_COLOUR=$FG_GREEN
    SYMBOL_COLOUR=$FG_RED
    case "$1" in
        [a-z]) echo -ne "${LETTER_COLOUR}${1}${FG_CLEAR}";;
        [A-Z]) echo -ne "${UPPER_COLOUR}${1}${FG_CLEAR}";;
        [0-9]) echo -ne "${NUMBER_COLOUR}${1}${FG_CLEAR}";;
        *)     echo -ne "${SYMBOL_COLOUR}${1}${FG_CLEAR}";;
    esac
}

colourprint () {
    str=$1
    for ((i=0; i<${#str}; i++)); do
        colourprintchar ${str:$i:1}
    done
    echo ""
}

colourprint $PARAM1

# If we can print things phonetically, and speak it out, do that as well
PHONETIC='phonetic.py'
#SAY='espeak'
#SAY_PARAMS='-ven -s 100'
if hash $PHONETIC &> /dev/null; then
    $PHONETIC $PARAM1
#    if hash $SAY &> /dev/null; then
#        $PHONETIC $PARAM1 | $SAY $SAY_PARAMS
#    fi
fi

