#!/usr/bin/env python3
#
# character-freq.py - work out the frequency of all characters in the
#                     supplied input
#
# Usage: <STDIN> | character-freq.py or character-freq.py <files>
#
# Copyright (C) 2013 Michael Davies <michael@the-davies.net>
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
import sys
import fileinput
from os.path import basename

def get_char_frequencies(string):
    """ Count character frequencies of supplied "string", return
        a dictionary of these counters indexed on character """
    table = {}
    for c in string:
        if c in table:
            table[c] += 1
        else:
            table[c] = 1
    return table

def dump_char_freq_table(table):
    """ Dump to STDOUT the character frequency table, taking special care to
        handle non-printing characters """
    # iterate over dictionary in reverse value sorted order
    for key in sorted(table, key=table.get, reverse=True):
        if key == '\n':
            pkey = '\\n'
        elif key == '\t':
            pkey = '\\t'
        elif key == '\r':
            pkey = '\\r'
        elif key == ' ':
            pkey = 'space'
        else:
            pkey = key
        print("'%s' appears %s times" % (pkey, table[key]))

if __name__ == '__main__':
    try:
        buffer = ""
        for line in fileinput.input():
            buffer += ' %s' % line # Not great for big files
        freq_table = get_char_frequencies(buffer)
        dump_char_freq_table(freq_table)
    except IOError as e:
        print("%s: [Errno %s] %s: '%s'" % (basename(sys.argv[0]),
              e.errno, e.strerror, fileinput.filename()))
        sys.exit(e.errno)
