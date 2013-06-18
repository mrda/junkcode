#!/usr/bin/python
#
# word-freq.py - work out the frequency of all words in the
#                supplied input
#
# Usage: <STDIN> | word-freq.py or word-freq.py <files>
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

def get_word_frequencies(word_list):
    """ Count word frequencies of supplied "string", return
        a dictionary of these counters indexed on word """
    table = {}
    for word in word_list:
        if word in table:
            table[word] += 1
        else:
            table[word] = 1
    return table

def dump_word_freq_table(table):
    """ Dump to STDOUT the word frequency table """
    # iterate over dictionary in reverse value sorted order
    for key in sorted(table, key=table.get, reverse=True):
        print "'%s' appears %s times" % (key, table[key])

if __name__ == '__main__':
    try:
        words = []
        for line in fileinput.input():
            # TODO use re.split here and split on everything not in [a-zA-Z]
            # which will result in a better frequency table
            words.extend(line.split())
        freq_table = get_word_frequencies(words)
        dump_word_freq_table(freq_table)
    except IOError as e:
        print "%s: [Errno %s] %s: '%s'" % \
            (basename(sys.argv[0]), e.errno, e.strerror, fileinput.filename())
        sys.exit(e.errno)

