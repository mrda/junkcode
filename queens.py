#!/usr/bin/env python
#
# queens - find a solution to the eight queens problem using simple
#          backtracking.  Note, you'll need to go make a coffee if you
#          change the board size to N > 17, at least for my Late 2013
#          MacBook Pro.
#
#          Refer: http://en.wikipedia.org/wiki/Eight_queens_puzzle
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
import sys


class Board:

    def __init__(self, size):
        self.size = size
        self.clear_board()

    def clear_board(self, board=None):
        if board:
            board = [[0 for x in range(b.size)] for x in range(b.size)]
        else:
            self.board = [[0 for x in range(self.size)]
                          for x in range(self.size)]

    def print_board(self):
        for row in range(self.size):
            for col in range(self.size):
                print(self.board[row][col]),
            print

    def is_valid_spot(self, row, col):
        fail = False
        # Check rows and columns
        for i in range(self.size):
            if self.board[row][i] or self.board[i][col]:
                fail = True
        # Check diagonals
        for row_delta in [-1, 1]:
            for col_delta in [-1, 1]:
                new_row = row
                new_col = col
                for i in range(self.size):
                    new_row = new_row + row_delta
                    new_col = new_col + col_delta
                    if (new_row in range(self.size) and
                       new_col in range(self.size)):
                        if self.board[new_row][new_col]:
                            fail = True
        return not fail

    def place_queen(self, row, col):
        """ Returns False if we cannot """
        ok = self.is_valid_spot(row, col)
        if ok:
            self.board[row][col] = 1
        return ok

    def clear_queen(self, row, col):
        self.board[row][col] = 0


def _solve(board, row):
    # Edge condition, we've run off the board
    if row >= board.size:
        return True

    for col in range(board.size):
        if board.place_queen(row, col):
            if _solve(board, row+1):
                return True
            else:
                board.clear_queen(row, col)
    return False


def solve_queens(size=8):
    # TODO(mrda): We could save the solution we find, and keep on
    # looking for more (after clearing the board).  We would need
    # to consider solutions that are simply transformations of each
    # other (rotation or symmetry). Probably best to do this in a
    # generator, since for large boards this could take a _long_
    # time, and there's no known way (AFAIK) to know if all
    # solutions have been discovered.  As the board increases in size,
    # more solutions exist for where a Queen is in the current row.
    # This means _solve() would need reworking to look for multiple
    # solutions from the current point onwards.

    board = Board(size)
    board.print_board()

    # Start looking for a solution from the first row
    _solve(board, 0)

    print
    board.print_board()


if __name__ == '__main__':
    # Allow the user to specify a board size
    progname = os.path.basename(__file__)
    try:
        if len(sys.argv) == 1:
            size = 8
        elif len(sys.argv) == 2:
            size = int(sys.argv[1])
        else:
            sys.exit('usage: %s [board size]' % progname)
    except ValueError:
        sys.exit('%s: Board sizes need to be integers' %
                 progname)

    solve_queens(size)
