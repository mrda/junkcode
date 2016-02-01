#!/usr/bin/env python
#
# get_disk_info - return information about a disk device
# Refer: http://pyudev.readthedocs.org/en/v0.15/guide.html
# and https://github.com/openstack/ironic-python-agent/blob/master/ironic_python_agent/hardware.py#L93-L108  # noqa
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
import os
import pyudev
import sys

if (len(sys.argv) == 1):
    progname = os.path.basename(__file__)
    sys.exit('Usage: %s <device>, where <device> is something'
             'like "/dev/sda"' % progname)

context = pyudev.Context()
udev = pyudev.Device.from_device_file(context, sys.argv[1])

extra = {key: udev.get('ID_%s' % udev_key) for key, udev_key in
         [('wwn', 'WWN'), ('serial', 'SERIAL_SHORT'),
          ('wwn_with_extension', 'WWN_WITH_EXTENSION'),
          ('wwn_vendor_extension', 'WWN_VENDOR_EXTENSION')]}

print("Disk info for %s" % sys.argv[1])
for key in extra:
    print("  %-25s%s" % (key, extra[key]))
