#!/usr/bin/env python
#
# dynamic_object.py - code snippet to show adding an attibute to an
#                     existing object
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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


class DynamicObject(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def on_the_fly(self, **kw):
        self.__dict__.update(kw)


if __name__ == '__main__':
    b = DynamicObject(foo='bar', baz=1)
    b.on_the_fly(spam='guido', eggs=False)

    b.me = True
    setattr(b, 'you', False)

    print("foo = %s" % b.foo)
    print("baz = %d" % b.baz)
    print("spam = %s" % b.spam)
    print("eggs = %s" % b.eggs)
    print("me = %s" % b.me)
    print("you = %s" % b.you)
