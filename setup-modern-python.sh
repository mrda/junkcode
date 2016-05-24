#!/bin/bash
#
# setup-modern-python.sh - set up a modern Python on a Debian or
#                          Debian-like system.
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
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get purge -y python-pip python-tox python-distribute          \
                 python-setuptools python-virtualenv python-wheel
apt-get purge -y python3-pip python3-tox python3-setuptools       \
                 python3-virtualenv python3-wheel


pushd /tmp
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py
popd

pip install --upgrade tox setuptools virtualenv wheel flake8 bindep \
                      virtualenvwrapper

