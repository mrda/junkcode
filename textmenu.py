#!/usr/bin/env python3
#
# textmenu.py - simple textmenu utility library
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
# 02111-1307, USA.#
#


class TextMenuWrongUsage(Exception):
    pass


class TextMenu:

    def __init__(self, title):
        self.exit = None
        self.options = {}
        self.title = '<<<<< ' + title + ' >>>>>'

    def add_exit(self, key, msg, top=False):
        if len(key) != 1:
            raise TextMenuWrongUsage("add_exit: 'key' should be a single char")
        self.exit = (key, msg)
        self.exit_at_top = top

    def add_option(self, key, msg, func):
        if len(key) != 1:
            raise TextMenuWrongUsage("add_option: 'key' should be a "
                                     "single char")
        self.options[key] = (msg, func)

    def _print_options(self):
        print("\n" + self.title + "\n")
        if self.exit is not None and self.exit_at_top:
            print("'%s' : %s" % (self.exit[0], self.exit[1]))

        for key in sorted(self.options):
            print("'%s' : %s" % (key, self.options[key][0]))

        if self.exit is not None and not self.exit_at_top:
            print("'%s' : %s" % (self.exit[0], self.exit[1]))

    def start_menu(self):
        while True:
            self._print_options()
            print("\n")
            raw = input('Please enter your selection: ')
            if len(raw) == 1:

                if raw == self.exit[0]:
                    return

                if raw in self.options:
                    print("You selected '%s'" % raw)
                    option = self.options[raw][1]
                    if hasattr(option, '__call__'):
                        return option()
                    else:
                        return option

            print("\n*** %s is not a valid option\n" % raw)


if __name__ == '__main__':
    print('TODO(mrda): Please add tests to textmenu.py here')
