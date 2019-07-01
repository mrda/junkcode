#!/bin/sh
#
# setup_path.sh - create a bunch of symlinks so my junkcode scripts are
#                 available on my path
#
# Copyright (C) 2013-2019 Michael Davies <michael@the-davies.net>
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
JUNKCODE=${HOME}/src/junkcode
NOARCH=${HOME}/bin/noarch

SCRIPTS=$(ls -1 ${JUNKCODE}/*.py ${JUNKCODE}/*.sh ${JUNKCODE}/*.pl \
          ${JUNKCODE}/rem*)

LN=`which ln`
CP=`which cp`

# Ensure the directories we need are here
mkdir -p ${NOARCH}
mkdir -p ${HOME}/bin/$(arch)/$(uname)

# Copy noarch scripts into place
for FILE in ${SCRIPTS}
do
    # -f is required because some links may already exist
    ${LN} -s -f ${FILE} ${NOARCH}
done

# Copy dot files into place
for DOT in ${JUNKCODE}/dots/.[a-z]*
do
    # -f is required because some links may already exist
    ${LN} -s -f ${DOT} ${HOME}
done

# Copy some binaries into place
if [ -d ${HOME}/src/blink1-tool ]; then
    ${CP} ${HOME}/src/blink1-tool/blink1-tool ${HOME}/bin/$(arch)/$(uname)
else
    echo "WARNING: No blink1-tool available"
fi

# Append my config on the end of the provided bash startup scripts
if [ -f /etc/bashrc ]; then
cat <<- EOF >> ${HOME}/.bashrc

# Michael's local bash customisations
if [ -f ${HOME}/.bash_aliases ]; then
    . ${HOME}/.bash_aliases
fi
EOF
fi

# Remind the user to setup bash_completions
echo "*** Remember to copy bash_completion scripts into place"
echo "sudo cp ${HOME}/src/junkcode/bash_completions.d/* /etc/bash_completion.d"

