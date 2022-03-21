#!/usr/bin/env python3
#
# maze.py - create a simple maze, using binary tree
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

import os
import random
import sys


class Board:

    def __init__(self, size):
        self.wall = 'X'
        self.passage = ' '
        self.size = size
        self.clear_board()

    def clear_board(self, board=None):
        if board:
            board = [[self.wall for x in range(b.size)] for x in range(b.size)]
        else:
            self.board = [[self.wall for x in range(self.size)]
                          for x in range(self.size)]

    def __str__(self):
        b = '+' + '-' * self.size + '+' "\n"
        for row in range(self.size):
            b += '|'
            for col in range(self.size):
                b += self.board[row][col]
            b += '|' + "\n"
        b += '+' + '-' * self.size + '+' "\n"
        return b

    def _clear_north_or_east(self, y, x):
        if y == 0:
            # Top line
            if x == self.size - 1:
                # Can't do anything at top right corner
                return
            else:
                direction = 'east'
        elif x == self.size - 1:
            # Right hand edge
            if y == 0:
                # Can't do anything at top right corner
                return
            else:
                direction = 'north'
        else:
            if random.randint(0, 1):
                direction = 'north'
            else:
                direction = 'east'
        if direction == 'north':
            delta_x, delta_y = 0, -1
        else:  # East
            delta_x, delta_y = 1, 0

        self.board[y + delta_y][x + delta_x] = self.passage

    def create_maze(self):
        # Start at bottom left and iterate up
        for y in reversed(range(self.size)):
            for x in range(self.size):
                self._clear_north_or_east(y, x)


def build_maze(size):
    board = Board(size)
    board.create_maze()
    return board


if __name__ == '__main__':
    # Allow the user to specify a board size
    progname = os.path.basename(__file__)
    try:
        if len(sys.argv) == 1:
            size = 30
        elif len(sys.argv) == 2:
            size = int(sys.argv[1])
        else:
            sys.exit('usage: %s [board size]' % progname)
    except ValueError:
        sys.exit('%s: Board sizes need to be integers' %
                 progname)

    maze = build_maze(size)
    print(maze)
