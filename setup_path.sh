#!/bin/sh
#
# setup_path.sh - create a bunch of symlinks so my junkcode scripts are
#                 available on my path
#
# Copyright (C) 2013 Michael Davies <michael@the-davies.net>
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

SCRIPTS=`ls -1 ${JUNKCODE}/*.py ${JUNKCODE}/*.sh ${JUNKCODE}/*.pl \
         ${JUNKCODE}/rem*`

LN=`which ln`
CP=`which cp`

if [ ! -d ${NOARCH} ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir -p ${NOARCH}
fi

for FILE in ${SCRIPTS}
do
    # -f is required because some links may already exist
    ${LN} -s -f ${FILE} ${NOARCH}
done

for DOT in ${JUNKCODE}/dots/.[a-z]*
do
    # -f is required because some links may already exist
    ${LN} -s -f ${DOT} ${HOME}
done

# one last hack for different OSes
${LN} -s -f ${HOME}/.bash_aliases ${HOME}/.bash_profile


