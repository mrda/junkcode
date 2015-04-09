#!/usr/bin/env python
#
# filecache.py - save or retrieve data to a unique file stored in a temporary
#                location, indexed on a supplied prefix and using your public
#                IP address.
# i.e. filecache.py save
#      Enter data to save: foo
#      Data stored to /tmp/file-cache.py-w8Ku17-172.16.69.179.txt is 'foo'
#
# i.e. filecache.py retrieve
#      Data stored to /tmp/file-cache.py-w8Ku17-172.16.69.179.txt is 'foo'
#
# Copyright (C) 2015 Michael Davies (michael@the-davies.net)
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

from datetime import datetime as dt
import glob
import os
import socket
import sys
import tempfile


myname = os.path.basename(__file__)


def record_state(data, ipaddr, prefix=None, suffix='.txt'):
    """Record the supplied data to a unique file with certain params."""
    name = ''
    suffix = '-' + ipaddr + suffix
    prefix += '-'
    fd = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix,
                                     delete=False)
    fd.write(data)
    name = fd.name
    fd.flush()
    return name


def _delete_all_but_youngest(files):
    """Delete all but the most recent modified file form the list.

    Return the most recently modified file from the list of files supplied, and
    delete all the others.
    """
    youngest = -1
    youngest_f = ''
    # Shouldn't need to do this as we should only have one file per ip address
    # but just to be sure
    for f in files:
        secs = seconds_since_modified(os.path.getmtime(f))
        if (youngest == -1) or (secs < youngest):
            youngest = secs
            youngest_f = f
    # Delete all but the youngest
    for f in files:
        if f != youngest_f:
            print "Deleting %s as there's too many files" % f
            os.unlink(f)
    return youngest_f


def retrieve_state(expiry_secs, ipaddr, prefix, suffix):
    """Retrieve data from the provided file if it hasn't gone stale."""
    dir_to_search = tempfile.gettempdir()
    pattern = dir_to_search + '/' + prefix + '-*-' + ipaddr + suffix
    files = glob.glob(pattern)
    lines = []
    f = ''
    if files:
        f = _delete_all_but_youngest(files)
        # Check to see whether the current file hasn't expired
        if seconds_since_modified(os.path.getmtime(f)) > expiry_secs:
            # Too old, delete
            print "Can't use the data in '%s' as it's too old" % f
            os.unlink(f)
        else:
            # Yay, data to use
            fd = open(f)
            lines = fd.readlines()
            fd.close()
    return f, lines


def get_data(expiry_secs=3600, ipaddr=None, prefix=None, suffix='.txt'):
    """Retrieve the 1st line of data from a temporary file if it's fresh."""
    fn, lines = retrieve_state(expiry_secs=expiry_secs, prefix=prefix,
                               ipaddr=ipaddr, suffix=suffix)
    if lines:
        # We only care about the text on the first line of the file
        return fn, lines[0]
    else:
        return None, None


def seconds_since_modified(d):
    # TODO(mrda): Should really do this taking into consideration timezones
    return int((dt.now() - dt.fromtimestamp(d)).total_seconds())


def get_my_public_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 80))
    ipaddr = (s.getsockname()[0])
    s.close()
    return ipaddr


def save_data():
    print("Enter data to save: "),
    data = raw_input()
    ipaddr = get_my_public_ip_address()
    filename = record_state(prefix=myname, ipaddr=ipaddr, data=data)
    print("Data stored to %s is '%s'" % get_data(expiry_secs=60, prefix=myname,
                                                 ipaddr=ipaddr))


def retrieve_data():
    ipaddr = get_my_public_ip_address()
    fname, data = get_data(expiry_secs=60, prefix=myname, ipaddr=ipaddr)
    if fname is None:
        print "No data retrieved"
    else:
        print("Data retrieved to '%s' is '%s'" % (fname, data))


def display_usage():
    exit('Usage: %s [save|retrieve]' % myname)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        display_usage()
    elif sys.argv[1] == 'save':
        save_data()
    elif sys.argv[1] == 'retrieve':
        retrieve_data()
    else:
        display_usage()
