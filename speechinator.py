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
import random
import sys

phrases = [ "%s, sing us a song!",
            "Come, spin us a yarn, %s",
            "%s, what's troublin' you today, sailor?",
            "Hey %s, why don't you bust a move?",
            "Time for you to sing 'Soft Kitty' to us, %s",
            "%s: What's happenin' in the hood, dawg?",
            "Tell us a story, %s",
            "Yo %s, what's going down, dude?",
          ]

idx = 0
len_phrases = len(phrases)-1
names = sys.argv[1:]

random.shuffle(phrases)
random.shuffle(names)

for name in names :
    print phrases[idx] % name
    if idx == len_phrases:
        idx = 0
    else:
        idx += 1

