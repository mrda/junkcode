#!/bin/sh
#
# auth.sh - authenticate against all the things
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

$(nmcli connection show --active | grep -q "${VPNENDPOINT}") || nmcli connection up "${VPNENDPOINT}" > /dev/null
if ! klist -s ; then
    PASS=$(zenity --title "Kerberos Password" --password 2> /dev/null)
    echo -n "$PASS" | kinit -r 7d ${IPA1}
    echo -n "$PASS" | kinit -r 7d ${IPA2}
else
    kinit -R
fi

# Seed sudo while we're at it
$(sudo -n /bin/true >& /dev/null)
if [ $? -eq 1 ]; then
    if [ -z $PASS ]; then
        PASS=$(zenity --title "Kerberos Password" --password 2> /dev/null)
    fi
    echo -n "$PASS" | sudo -S /usr/bin/true >& /dev/null
fi
