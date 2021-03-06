#!/usr/bin/env python
#
# speechinator.py - come up with some random ways of asking people to speak
#                   for IRC meetings.
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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
import random
import sys


phrases = ["%s, sing us a song!",
           "Come, spin us a yarn, %s",
           "%s, what's troublin' you today, sailor?",
           "Hey %s, why don't you bust a move?",
           "Time for you to sing 'Soft Kitty' to us, %s",
           "What's happenin' in the hood, %s?",
           "Tell us a story, %s",
           "Yo %s, what's going down, dude?",
           "Earth to %s, copy?",
           "%s, Engage!",
           "What's up, %s?",
           "%s: What's shakin'?",
           "%s, S'Up?",
           "So we meet again, %s, for the last time!",
           "Here's looking at you, %s",
           "%s phone home",
           "%s, Show me the money!",
           "Open the pod bay doors please, %s",
           "Yo, %s!",
           "Please state the nature of the medical emergency, %s",
           "%s, Why are there so many songs about rainbows?",
           "Nobody puts %s in a corner"]


filename = os.environ.get('HOME')
if filename is None:
    print "%s: Can't find home directory" % os.path.basename(sys.argv[0])
    print "Exiting..."
    sys.exit(1)
filename += "/.team_nicks"

names = None
try:
    fd = open(filename, 'r')
    names = [line.strip() for line in fd]
except (OSError, IOError) as e:
    print "%s: %s" % (os.path.basename(sys.argv[0]), e)
    print "Exiting..."
    sys.exit(2)

random.shuffle(phrases)
random.shuffle(names)

for idx, name in enumerate(names):
    print phrases[idx] % name
