#!/bin/bash
#
# find-duplicates.sh - find duplicate files
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

# Do another check to see that the files really are duplicates
check_dups()
{
    F1="$1"
    F2="$2"
    diff "$F1" "$F2" >& /dev/null
    if [[ $? -eq 0 ]]; then
        if [[ "$F1" < "$f2" ]]; then
            printf "rm \"$F1\" # File to keep: \"$F2\"\n"
        else
            printf "rm \"$F2\" # File to keep: \"$F1\"\n"
        fi
    else
        printf "# *** These files aren't duplicates as expected \"$F1\" \"$F2\"\n"
    fi
}

# Simple command line parsing
# See https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash for something better
if [[ $# -ne 0 ]]; then
    if [[ $1 == "-h" ]]; then
        echo "Usage: $(basename $0)"
        exit 0
    fi
fi

# TODO(mrda): Add support for specifying a directory

HASHFILE=$(mktemp /tmp/find-duplicates.XXX)

find . -type f -iname "*" | while read f
do
    echo "Calculating hash for \"$f\""
    echo $(md5sum "$f") >> ${HASHFILE}
done
echo "Output sent to ${HASHFILE}"

# Sort file in place
sort -o ${HASHFILE}{,}

# Find duplicates and recommend which one to delete
COUNT=0
while read HASH FILE; do
    if [[ "${PREV_HASH}" == "${HASH}" ]]; then
        ((COUNT=COUNT+1))
        check_dups "$PREV_FILE" "$FILE"
    fi
    PREV_HASH="${HASH}"
    PREV_FILE="${FILE}"
done < ${HASHFILE}

if [[ $COUNT -eq 0 ]]; then
    echo "No duplicates found"
else
    echo "There are potentially $COUNT duplicates"
    echo "Use 'xdg-open' to examine"
fi

