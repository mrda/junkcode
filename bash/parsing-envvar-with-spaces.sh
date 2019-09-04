#!/bin/bash
#
# Demonstrating a few things:
#  1) How to parse a csv list of directories that have spaces in them
#  2) How to find out the name of a python package
#  3) How to expand shell shortcuts like ~
#  4) How to call eval safely, preventing shell redirection attacks
#  5) How to do bash conditions inline
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
PYTHON_PKG_DIRS="~/src/../src/ironic,~/src/fake os-traits,/etc/passwd > /tmp/foobar"

IFS=',' read -ra PKG_DIRS <<< "$PYTHON_PKG_DIRS"
for PKG_DIR in "${PKG_DIRS[@]}"; do
    EXP_PKG_DIR=$(eval echo ${PKG_DIR//>})
    [[ -d "$EXP_PKG_DIR" ]] && \
    echo "$(cd "$EXP_PKG_DIR"; python setup.py --name) is in dir $EXP_PKG_DIR"
done
