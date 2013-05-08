#!/usr/bin/env python
#
# imify.py - Turn computer-speak into English for passing through software
#            that parses and prevents things like URLs and Email Addresses
#            from being accepted.  Note that both the encode and decode
#            methods are provided - they should be symmetric.
#
# Copyright (C) 2007 Michael Davies (michael@the-davies.net)
#
# e.g. Encoding example:
# mrda@carbon:$ ./imify.py http://catb.org/~esr/jargon/
# http colon slash slash catb dot org slash tilde esr slash jargon slash
#
# e.g. Decoding example
# mrda@carbon:$ ./imify.py dec "michael at the hyphen davies dot net"
# michael@the-davies.net
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
import re
import sys

def imify(strings):
    for str in strings:
        return _enc(str)

def _enc(str):
    dots = re.compile(r'\.')
    slashes = re.compile(r'\/')
    backslashes = re.compile(r'\\')
    ats = re.compile(r'\@')
    colons = re.compile(r'\:')
    tildes = re.compile(r'\~')
    semis = re.compile(r'\;')
    hyphens = re.compile(r'\-')
    excessws = re.compile(r'\ \ ')
    str1 = dots.sub(' dot ', str)
    str2 = backslashes.sub(' backslash ', str1)
    str3 = slashes.sub(' slash ', str2)
    str4 = ats.sub(' at ', str3)
    str5 = colons.sub(' colon ', str4)
    str6 = tildes.sub(' tilde ', str5)
    str7 = semis.sub(' semicolon ', str6)
    str8 = hyphens.sub(' hyphen ', str7)
    str9 = excessws.sub(' ', str8)
    return str9

def deimify(strings):
    for str in strings:
        return "".join([_dec(atom) for atom in str.split()])

def _dec(str):
    if (str) == 'dot':
        return '.'
    elif (str) == 'backslash':
        return '\\'
    elif (str) == 'slash':
        return '/'
    elif (str) == 'at':
        return '@'
    elif (str) == 'colon':
        return ':'
    elif (str) == 'tilde':
        return '~'
    elif (str) == 'semicolon':
        return ';'
    elif (str) == 'hyphen':
        return '-'
    else:
        return str

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        pass
    elif (sys.argv[1] == "enc") or (sys.argv[1] == "encode"):
        print imify(sys.argv[2:])
    elif (sys.argv[1] == "dec") or (sys.argv[1] == "decode"):
        print deimify(sys.argv[2:])
    elif (sys.argv[0] == "deimify.py"):
        print deimify(sys.argv[1:])
    else:
        print imify(sys.argv[1:])
