#!/usr/bin/env python
#
# mocking_properties.py - example code on how to mock @property functions.
#                         This was too hard to work out when I needed it not to
#                         save it for later :)
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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
import mock
import six


class ParentClass(type):
    @property
    def my_property(cls):
        return 'Hello there'


@six.add_metaclass(ParentClass)
class ChildClass(object):

    def frobnicate(self):
        return 'frobnication'

    def call(self, method):
        strng = ChildClass.my_property
        return "%s: %s %s" % (method, strng, self.frobnicate())


if __name__ == '__main__':

    import unittest

    class TestMocking(unittest.TestCase):

        def test_no_mock(self):
            pc = ChildClass()
            self.assertEqual('Yow: Hello there frobnication',
                             pc.call('Yow'))

        @mock.patch.object(ParentClass, 'my_property',
                           new_callable=mock.PropertyMock)
        @mock.patch.object(ChildClass, 'frobnicate')
        def test_mock_my_property(self, mock_frob, mock_my_property):
            mock_frob.return_value = 'dogs'
            mock_my_property.return_value = 'cats and'
            pc = ChildClass()
            self.assertEqual('Yow: cats and dogs',
                             pc.call('Yow'))

    unittest.main()
