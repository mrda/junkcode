#!/usr/bin/env python
#
# exception_catcher.py - sample code for catching all exceptions except
#                        for the ones you specify
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

# In Python...
#   User-defined exceptions should be derived from Exception
#   Built-in exceptions derive from StopIteration, StandardError, or Warning
# See https://docs.python.org/2/library/exceptions.html for more details


debug = False


class MyOwnException(Exception):
    pass


class MoreSpecificException(MyOwnException):
    pass


def is_standard_exception(ex):
    """Is the passed in exception considered a standard exception?

    Determine whether the exception passed in should be caught
    based upon whether it is a "standard" exception or not.

    :param ex: The excetpion to check

    :returns: True if the exception is a standard exception, False otherwise
    """
    if (isinstance(ex, StopIteration) or
            isinstance(ex, StandardError) or
            isinstance(ex, Warning)):
        if debug:
            print ("%s is a standard exception" % type(ex).__name__)
        return True
    else:
        if debug:
            print ("%s is a NOT a standard exception" % type(ex).__name__)
        return False


def check_raise_exception(ex):
    """Test raising exceptions to see if they are standard.

    Raise the specified exception inside a local try/except block
    and determine if it's a standard exception.

    :param ex: The exception to raise and check
    """
    try:
        raise ex
    except Exception as e:
        return is_standard_exception(e)


if __name__ == '__main__':

    import unittest

    class TestExceptionHandling(unittest.TestCase):
        def test_standard_exceptions(self):
            self.assertTrue(check_raise_exception(StandardError))
            self.assertTrue(check_raise_exception(StopIteration))
            self.assertTrue(check_raise_exception(ImportError))
            self.assertTrue(check_raise_exception(NotImplementedError))
            self.assertTrue(check_raise_exception(Warning))
            self.assertTrue(check_raise_exception(SyntaxWarning))

        def test_local_exceptions(self):
            self.assertFalse(check_raise_exception(MyOwnException))
            self.assertFalse(check_raise_exception(MoreSpecificException))

    unittest.main()
