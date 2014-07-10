#!/usr/bin/env python
#
# ignore.py - Backport of Python 3.4's ignore construct
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
#
# Instead of:
#       try:
#           some_function(...)
#       except SomeException:
#           pass
#
# Do this:
#       import ignored
#
#       with ignored(SomeException):
#           some_function(...)
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
from contextlib import contextmanager


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass

if __name__ == '__main__':

    import unittest

    def some_function():
        raise ValueError

    class TestIgnored(unittest.TestCase):
        def test_not_used(self):
            self.assertRaises(ValueError, some_function)

        def test_success(self):
            try:
                with ignored(ValueError):
                    some_function()
            except Exception:
                self.fail("Didn't ignore the exception")

        def test_success_wrong_exception(self):
            with self.assertRaises(ValueError):
                with ignored(TypeError):
                    some_function()

    unittest.main()
