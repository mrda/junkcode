#!/usr/bin/env python
#
# introspection-iterator.py - execute functions in order using
#                             introspection
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


class Commands(object):

    def step_1_foo(self):
        print("This is step 1")

    def step_2_bar(self):
        print("This is step 2")

    def step_3_baz(self):
        print("This is step 3")

    def step_4_spam(self):
        print("This is step 4")

    def step_5_eggs(self):
        print("This is step 5")

    def step_11_bacon(self):
        print("This is step 11")

    def step_101_chocolate(self):
        print("This is step 101")

    def _get_functions_to_run(self):
        unsorted_steps = [s for s in dir(self) if s.startswith('step_')]
        steps = sorted(unsorted_steps, key=lambda s: int(s.split('_', 2)[1]))
        for name in steps:
            yield name, getattr(self, name)

    def run_steps(self):
        for name, func in self._get_functions_to_run():
            print('Function "%s":' % name),
            func()


if __name__ == '__main__':
    c = Commands()
    c.run_steps()
