#!/usr/bin/env bash
#
# Wordle word adder
#
# Copyright (C) 2023 Michael Davies <michael@the-davies.net>
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

DIRNAME=$HOME/.wordle
ensure_dir $DIRNAME

if [[ $# -ne 1 ]]; then
    printf "Usage: %s <word> - add <word> to dictionary. Exiting...\n" $(basename $0)
    exit 1
fi

grep "$1" $DIRNAME/words >& /dev/null
if [ $? -eq 0 ]; then
    echo "\"$1\" is already in the dictionary, not adding"
    exit 2
fi

echo "$1" >> $DIRNAME/words
