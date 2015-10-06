#!/usr/bin/env python
#
# hostkeys.py - display the hostkeys on localhost
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
import glob
import os
import socket


print("<<<< Displaying ssh host keys for %s >>>>" % socket.getfqdn())
files = []
for dir in ['/etc/', '/etc/ssh/']:
    t = glob.glob(dir+'ssh_host_*_key.pub')
    if t:
        for f in t:
            files.append(f)
    t = glob.glob(dir+'ssh_host_key.pub')
    if t:
        for f in t:
            files.append(f)

for host_key in files:
    os.system("ssh-keygen -l -f %s" % host_key)
