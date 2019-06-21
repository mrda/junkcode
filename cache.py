#!/usr/bin/env python3
#
# cache.py - Simple caching decorator for pure python functions
#            (note that you probably don't want this, but instead
#             you want to use functools.lru_cache)
#
# Note: There is no maximum size for the cache, so that's a denial
#       of service (DoS) waiting to happen.
#
# Example:
#       @cache
#       def my_pure_func(n)
#           return 37 * n
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
from functools import wraps

CACHE_DEBUG = False


def cache(func):
    cached = {}

    @wraps(func)
    def localfunc(*args):
        if args in cached:
            if CACHE_DEBUG:
                return cached[args], True
            else:
                return cached[args]
        result = func(*args)
        cached[args] = result
        if CACHE_DEBUG:
            return result, False
        else:
            return result
    return localfunc


if __name__ == '__main__':

    import unittest

    CACHE_DEBUG = True

    @cache
    def my_pure_func(n):
        return 37 * n

    class TestCaching(unittest.TestCase):
        def test_caching(self):
            result, cached = my_pure_func(6)
            self.assertFalse(cached)
            result, cached = my_pure_func(6)
            self.assertTrue(cached)
            result, cached = my_pure_func(7)
            self.assertFalse(cached)
            result, cached = my_pure_func(8)
            self.assertFalse(cached)
            result, cached = my_pure_func(6)
            self.assertTrue(cached)
            result, cached = my_pure_func(6)
            self.assertTrue(cached)
            result, cached = my_pure_func(8)
            self.assertTrue(cached)
            result, cached = my_pure_func(1)
            self.assertFalse(cached)

    unittest.main()
