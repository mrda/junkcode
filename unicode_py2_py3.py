#!/usr/bin/env python
#
# unicode_py2_py3.py - example code on handling unicode across py2/py3
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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
import six

class Foo:
    def __init__(self):
        if six.PY3:
            self.field = chr(233) + chr(0x0bf2) + chr(3972)
        else:
            self.field = unichr(233) + unichr(0x0bf2) + unichr(3972)

    def __str__(self):
        if not six.PY3:
            return unicode(self.field).encode('utf-8')
        return self.field


if __name__ == '__main__':
    if six.PY2:
        print("We're running this test under Python2")
    else:
        print("We're running this test under Python3")
    f = Foo()
    expected = b'\xc3\xa9\xe0\xaf\xb2\xe0\xbe\x84'
    if six.PY3:
        expected = expected.decode('utf-8')
    assert f.__str__() == expected
