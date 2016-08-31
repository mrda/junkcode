#!/bin/bash
#
# take_photo.sh - Take a photo using a webcam connected to a remote host, copy
#                 the file to the current directory, and if this is run on a
#                 mac, open the image.
#
# Copyright (C) 2016 Michael Davies <michael@the-davies.net>
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

BASE=$(basename $0)
if [ -z "$1" ] || [ -z "$2" ]; then
  printf "Usage: ${BASE} <hostname> <filename>\n"
  exit 1
fi

DELAY=5 # seconds
SKIP=20 # frames

ssh $1 fswebcam -D ${DELAY} -S ${SKIP} $2 &> /dev/null
scp $1:$2 .

# If we are running on a Mac
if [ "$(uname)" == "Darwin" ]; then
    open $2
fi
