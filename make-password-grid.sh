#!/bin/sh
#
# make-password-grid.sh - build a grid of 8x4 16 character passwords,
#                         and optionally send them to the printer
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

random_password ()
{
    echo $(LC_ALL=C tr -dc '[:alnum:]@#$%^()[]{};:",.<>?' </dev/urandom | head -c $1)
}

make_password_grid ()
{
    TMPFILE=$1
    for LINES in $(seq 1 8); do
        for PASSWORDS in $(seq 1 4); do
            PASS="$(random_password 16)"
            COLOURISED=$(colourprint "$PASS")
            echo -n "$COLOURISED  " | tee -a $TMPFILE
        done
        echo "" | tee -a $TMPFILE
    done
}

display_usage ()
{
    printf "%s [-h] [-p]\n" $(basename $0)
    printf "  -h  display this help\n"
    printf "  -p  send output to the default printer\n"
}

PRINT=0
for ARG in "$@"; do
    case $ARG in
        -h)
            display_usage
            exit 0
            ;;
        -p)
            PRINT=1
            ensure_cmd aha
            ensure_cmd wkhtmltopdf
            ;;
        *)
            display_usage
            echo "Unknown option, exiting..."
            exit 1
            ;;
    esac
done

OUTPUTFILE=$(mktemp "${TMPDIR:-/tmp/}$(basename $0).XXXXXXXXXXXX")
make_password_grid $OUTPUTFILE

if [ $PRINT -eq 1 ]; then
    $(cat $OUTPUTFILE  | aha | wkhtmltopdf -q - - | lpr) &> /dev/null
fi

rm $OUTPUTFILE
