#!/usr/bin/env python
#
# sudoko - solve Sudoku puzzles. If you provide an argument, it is
#          assumed to be a filename to a Sudoku puzzle that needs
#          solving.  If none are provided, it just creates and
#          solves a random puzzle.
#
#          Refer: http://en.wikipedia.org/wiki/Sudoku
#
# Files to be read in as command line args need to be in the
# following format:
#
# 007650000
# 000007300
# 810300006
# 400000063
# 050000080
# 620000009
# 900002048
# 005800000
# 000073900
#
# or
#
# ..765....
# .....73..
# 81.3....6
# 4......63
# .5.....8.
# 62......9
# 9....2.48
# ..58.....
# ....739..
#
# Sorry, it's not very flexible for now.
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
import argparse
import os
import random
import string
import sys

SIZE = 9
VALS = 9


class Board():

    def __init__(self, verbose, random_vals=0):
        self.board = [[0 for x in range(1, SIZE+1)] for x in range(1, SIZE+1)]
        if random_vals != 0:
            if verbose:
                print ("Generating Sudoku board")
            for i in range(random_vals):
                while True:
                    row = random.randrange(SIZE)
                    col = random.randrange(SIZE)
                    val = random.randrange(1, VALS+1)
                    if self.is_valid(val, row, col):
                        break
                    else:
                        if verbose:
                            print ("*** Tried %s at %s,%s" % (val, row, col))
                if verbose:
                    print ("Added %s at %s,%s" % (val, row, col))
                self.board[row][col] = val

    def print_board(self, with_zeros=False):
        segment = '+' + '-' * 7
        print segment + segment + segment + '+'
        for row in range(SIZE):
            for col in range(SIZE):
                if col % 3 == 0:
                    print '|',
                if self.board[row][col] == 0:
                    if with_zeros:
                        print self.board[row][col],
                    else:
                        print ' ',
                else:
                    print self.board[row][col],
            print('|')
            if row % 3 == 2:
                print segment + segment + segment + '+'

    def _find_segment(self, val):
        if val < 3:
            return 0
        elif val < 6:
            return 3
        else:
            return 6

    def get_segment_top_left(self, row, col):
        return self._find_segment(row), self._find_segment(col)

    def is_valid(self, number, row, col):
        """Check to see if number is allowed at (x,y)"""
        # Check row
        for c in range(SIZE):
            if c != col:
                if self.board[row][c] == number:
                    return False
        # Check column
        for r in range(SIZE):
            if r != row:
                if self.board[r][col] == number:
                    return False
        # Check section
        top_r, top_c = self.get_segment_top_left(row, col)
        for r in range(top_r, top_r + 3):
            for c in range(top_c, top_c + 3):
                if self.board[r][c] == number:
                    return False
        return True

    def find_solution(self, verbose=False):
        """Find a solution to the current puzzle.

        Returns True if a solution can be found, False otherwise.
        """
        # Note(mrda): This is a terrible brute force approach
        empty_slot = False
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == 0:
                    empty_slot = True
                    for val in range(1, VALS+1):
                        solution = False
                        if self.is_valid(val, row, col):
                            self.board[row][col] = val
                            if self.find_solution(verbose):
                                if verbose:
                                    print("Success: %s at (%s, %s) ok" %
                                          (val, row, col))
                                return True
                            else:
                                if verbose:
                                    print("Backtracking: %s at (%s, %s)" %
                                          (val, row, col))
                                self.board[row][col] = 0
                    if not solution:
                        if verbose:
                            print("No solution for (%s, %s) found" %
                                  (row, col))
                        return False
        if not empty_slot:
            # Everything solved!
            return True
        else:
            if verbose:
                print("Expensive backtrack needed...")
            return False


def generate_sudoku(difficulty, verbose=False):
    if difficulty == 'easy':
        hints = 24
    elif difficulty == 'medium':
        hints = 10
    elif difficulty == 'hard':
        hints = 6
    else:
        # somewhere inbetween
        hints = 14

    # Generate a random Sudoku and see if it's solvable
    while True:
        b = Board(verbose, hints)
        b.print_board()
        if b.find_solution(verbose):
            break
        print("*** Rats, that random puzzle didn't work, trying again")
    b.print_board(verbose)


def read_sudoku_from_filename(filename, verbose):
    b = None
    allowed = set(string.digits + '.')
    with open(filename, 'r') as fd:
        b = Board(verbose)
        lines = fd.readlines()
        if len(lines) != 9:
            if verbose:
                print("Wrong number of lines - found %s" % len(lines))
            return None
        row = 0
        for line in lines:
            # Each line should only contain the numbers 0..9
            # and only 0 can be repeated
            # TODO(mrda): Should add more validation here
            line = line.rstrip()
            if len(line) != 9:
                if verbose:
                    print("Line %d has %d chars" % (row, len(line)))
                return None
            col = 0
            for ch in list(line):
                if ch not in allowed:
                    return None
                if ch == '.':
                    ch = 0
                num = int(ch)
                if verbose:
                    print("Setting (%s, %s) to %s" % (row, col, num))
                b.board[row][col] = num
                col += 1
            row += 1
    return b


def solve_sudoku_from_filename(filename, verbose):
    b = read_sudoku_from_filename(filename, verbose)
    b.print_board()
    if b.find_solution(verbose):
        b.print_board()
    else:
        print "No solution found"


if __name__ == '__main__':
    progname = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Print our working out')

    parser.add_argument('-d', '--difficulty',
                        choices=['easy', 'medium', 'hard'],
                        help='Difficulty level for generated Sudokus')

    parser.add_argument('filenames', metavar='filename', type=str, nargs='*',
                        help='list of files containing puzzles to solve')

    args = parser.parse_args()

    # Generate a Sudoku
    if not args.filenames:
        if args.verbose:
            print("Generating a Sudoko...")
        generate_sudoku(args.difficulty, args.verbose)
        sys.exit(0)

    # Otherwise, solve some puzzles
    for filename in args.filenames:
        if args.verbose:
            print("Processing puzzle '%s'" % filename)
        solve_sudoku_from_filename(filename, args.verbose)
