#!/usr/bin/python
# palindrome.py - checks whether a sring is a palindrome
# Copyright (C) 2012 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#

import fileinput
import sys

def check_palindrome(str, debug=False):
    length = len(str)
    i = 0
    success = True
    while i < length/2 and success:
        firstchar = str[i]
        secondchar = str[length-i-2]
        if firstchar != secondchar:
            if debug:
                print "Failed palindrom check because because '%s' doesn't equal '%s' (examing character index '%d')" % (firstchar, secondchar, i+1)
            success = False
        i += 1
    return success

if __name__ == '__main__':
    debug = True
    for line in fileinput.input():
        if check_palindrome(line, debug):
            print "That's a palindrome"
        else:
            print "That's NOT a palindrome"

