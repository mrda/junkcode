#!/bin/bash
#
# worldtime - Print out the time in major cities around the world
#             Why? because timezones are hard, especially daylight
#             savings :)
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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
declare -a location=("America/Vancouver" "America/Phoenix"\
           "America/Chicago" "America/New_York" "America/Caracas"\
           "America/Sao_Paulo" "Europe/London" "Europe/Paris"
           "Asia/Jerusalem" "Asia/Baghdad" "Europe/Moscow" "Asia/Karachi"\
           "Asia/Calcutta" "PRC" "Asia/Hong_Kong" "Asia/Tokyo"\
           "Australia/Perth" "Australia/Adelaide" "Australia/Brisbane"\
           "Australia/Sydney" "Pacific/Auckland")

for l in "${location[@]}"
do
    printf "%-20s\t%s\n" "$l" "$(TZ=$l date)"
done
