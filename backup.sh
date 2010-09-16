#!/bin/sh
#
# backup - Make backup copies of the list of files/directories specified
#          as parameters to this script. Create the ~/backup-`year` dir
#          if required
#
# Copyright (C) 2007 Michael Davies <michael@the-davies.net>
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

BDIR=${HOME}/backup-`date +%Y`
if ! [ -d ${BDIR} ]; then
    echo "Backup directory doesn't exist.  Creating ${BDIR} now...";
    mkdir ${BDIR};
fi
for FILE; do
    # Using basename to remove trailing / and hence copy directories,
    # not just the contents
    LFILE=`basename ${FILE}`
    DFILE=${LFILE}-`date +%Y%m%d-%H%M%S`
    echo "Copying \"${LFILE}\" to ${BDIR}/${DFILE}";
    cp -rp ${LFILE} ${BDIR}/${DFILE};
done

