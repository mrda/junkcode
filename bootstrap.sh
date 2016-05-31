#!/usr/bin/env bash
#
# bootstrap.sh - set up things on a new machine
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

# Get the system up to date, and install the bare essentials
apt-get update
apt-get upgrade -y
apt-get install -y \
    build-essential \
    python-dev screen \
    git \
    git-review \
    ack-grep \
    python-pygments

# Install basic repos and setup the environment
mkdir -p ${HOME}/src
cd ${HOME}/src
git clone https://github.com/mrda/junkcode
git clone https://github.com/mrda/shiny-engine
cd ${HOME}/src/junkcode
./setup_path.sh
cd ${HOME}/src/shiny-engine/scripts
./se-setup.py
. ${HOME}/.bash_aliases

printf "\nYou're running on a ${PLATFORM} platform\n"
printf "If you want 'rack' go and read https://developer.rackspace.com/docs/rack-cli/configuration/\n"
printf "All done\n"
