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
import inspect
import os
import random
import string
import sys
import time

SIZE = 9
VALS = 9


def abstract():
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


class AbstractSolver:
    def find_solution(self, board, verbose):
        abstract()


class BruteForceSolver(AbstractSolver):
    def find_solution(self, board, verbose):
        """Find a solution to the current puzzle.

        Returns True if a solution can be found, False otherwise.
        """
        # Note(mrda): This is a terrible brute force approach
        empty_slot = False
        for row in range(SIZE):
            for col in range(SIZE):
                if board.board[row][col] == 0:
                    empty_slot = True
                    for val in range(1, VALS+1):
                        solution = False
                        if board.is_valid(val, row, col):
                            board.board[row][col] = val
                            if self.find_solution(board, verbose):
                                if verbose == 2:
                                    print("Success: %s at (%s, %s) ok" %
                                          (val, row, col))
                                return True
                            else:
                                if verbose == 2:
                                    print("Backtracking: %s at (%s, %s)" %
                                          (val, row, col))
                                board.board[row][col] = 0
                    if not solution:
                        if verbose == 2:
                            print("No solution for (%s, %s) found" %
                                  (row, col))
                        return False
        if not empty_slot:
            # Everything solved!
            return True
        else:
            if verbose == 2:
                print("Expensive backtrack needed...")
            return False


class PossibilitiesSolver(AbstractSolver):
    def __init__(self, board, verbose):
        # Initialise possible values
        if verbose == 2:
            board.print_board()
        self.poss = [[0 for x in range(1, SIZE+1)] for x in range(1, SIZE+1)]
        for row in range(SIZE):
            for col in range(SIZE):
                if board.board[row][col] == 0:
                    self.poss[row][col] = (self.get_possible_values(
                                           board, row, col))
                    if verbose == 2:
                        print("(%s, %s) has possibilities %s" %
                              (row, col, str(self.poss[row][col])))

    def get_possible_values(self, board, row, col):
        s = set(list('123456789'))
        # Remove all the numbers in my segment
        top_r, top_c = board.get_segment_top_left(row, col)
        for r in range(top_r, top_r + 3):
            for c in range(top_c, top_c + 3):
                elem = str(board.board[r][c])
                if elem != '0':
                    s.discard(elem)

        # Remove all numbers in my row
        for c in range(SIZE):
            elem = str(board.board[row][c])
            if elem != '0':
                s.discard(elem)

        # Remove all numbers in my column
        for r in range(SIZE):
            elem = str(board.board[r][col])
            if elem != '0':
                s.discard(elem)

        # Double check
        assert(len(s) != 0)

        return s

    def find_solution(self, board, verbose):
        """Find a solution to the current puzzle.

        Returns True if a solution can be found, False otherwise.
        """
        empty_slot = False
        for row in range(SIZE):
            for col in range(SIZE):
                if board.board[row][col] == 0:
                    empty_slot = True
                    for val in self.poss[row][col]:
                        solution = False
                        if board.is_valid(val, row, col):
                            board.board[row][col] = val
                            if self.find_solution(board, verbose):
                                if verbose == 2:
                                    print("Success: %s at (%s, %s) ok" %
                                          (val, row, col))
                                return True
                            else:
                                if verbose == 2:
                                    print("Backtracking: %s at (%s, %s)" %
                                          (val, row, col))
                                board.board[row][col] = 0
                    if not solution:
                        if verbose == 2:
                            print("No solution for (%s, %s) found" %
                                  (row, col))
                        return False
        if not empty_slot:
            # Everything solved!
            return True
        else:
            if verbose == 2:
                print("Expensive backtrack needed...")
            return False


class Board:
    def __init__(self, verbose, random_vals=0):
        self.verbose = verbose
        self.board = [[0 for x in range(1, SIZE+1)] for x in range(1, SIZE+1)]
        if random_vals != 0:
            if verbose == 1:
                print ("Generating Sudoku board")
            for i in range(random_vals):
                while True:
                    row = random.randrange(SIZE)
                    col = random.randrange(SIZE)
                    val = random.randrange(1, VALS+1)
                    if self.is_valid(val, row, col):
                        break
                    else:
                        if verbose > 1:
                            print ("*** Tried %s at %s,%s" % (val, row, col))
                if verbose > 1:
                    print ("Added %s at %s,%s" % (val, row, col))
                self.board[row][col] = val

    def copy(self):
        obj = Board(self.verbose)
        new = [[0 for x in range(1, SIZE+1)] for x in range(1, SIZE+1)]
        for r in range(SIZE):
            for c in range(SIZE):
                new[r][c] = self.board[r][c]
        obj.board = new
        return obj

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


def generate_sudoku(difficulty, algorithm, verbose):
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
    looping = True
    while looping:
        b = Board(verbose, hints)

        brute_b = b.copy()
        poss_b = b.copy()

        brute_solver = BruteForceSolver()
        poss_solver = PossibilitiesSolver(poss_b, verbose)

        if verbose == 1:
            print ("Problem to solve")
        b.print_board()

        if algorithm in ['brute', 'all']:
            with Timer() as t:
                if brute_solver.find_solution(brute_b, verbose):
                    looping = False
            if verbose >= 1:
                print('That took %.03f seconds' % t.interval)

        if algorithm in ['possible', 'all']:
            with Timer() as t:
                if poss_solver.find_solution(poss_b, verbose):
                    looping = False
            if verbose >= 1:
                print('That took %.03f seconds' % t.interval)

        if looping:
            if verbose == 1:
                print("*** Rats, that random puzzle didn't work, trying again")

    if algorithm in ['brute', 'all']:
        if verbose == 1:
            print ("Brute force solution")
        brute_b.print_board(verbose)
    if algorithm in ['possible', 'all']:
        if verbose == 1:
            print ("Possibilities solution")
        poss_b.print_board(verbose)


def read_sudoku_from_filename(filename, verbose):
    b = None
    allowed = set(string.digits + '.')
    with open(filename, 'r') as fd:
        b = Board(verbose)
        lines = fd.readlines()
        if len(lines) != 9:
            if verbose == 1:
                print("Wrong number of lines - found %s" % len(lines))
            return None
        row = 0
        for line in lines:
            # Each line should only contain the numbers 0..9
            # and only 0 can be repeated
            # TODO(mrda): Should add more validation here
            line = line.rstrip()
            if len(line) != 9:
                if verbose == 1:
                    print("Line %d has %d chars" % (row, len(line)))
                return None
            col = 0
            for ch in list(line):
                if ch not in allowed:
                    return None
                if ch == '.':
                    ch = 0
                num = int(ch)
                if verbose == 2:
                    print("Setting (%s, %s) to %s" % (row, col, num))
                b.board[row][col] = num
                col += 1
            row += 1
    return b


def solve_sudoku_from_filename(filename, algorithm, verbose):
    b = read_sudoku_from_filename(filename, verbose)
    b.print_board()
    poss_solver = PossibilitiesSolver(b, verbose)
    brute_solver = BruteForceSolver()

    if algorithm in ['brute', 'all']:
        with Timer() as t:
            if brute_solver.find_solution(b, verbose):
                b.print_board()
            else:
                print "No solution found"
        if verbose >= 1:
            print('That took %.03f seconds' % t.interval)

    if algorithm in ['possible', 'all']:
        with Timer() as t:
            if poss_solver.find_solution(b, verbose):
                b.print_board()
            else:
                print "No solution found"
        if verbose >= 1:
            print('That took %.03f seconds' % t.interval)


if __name__ == '__main__':
    progname = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        help='Increase verbosity')

    parser.add_argument('-d', '--difficulty',
                        choices=['easy', 'medium', 'hard'],
                        help='Difficulty level for generated Sudokus')

    parser.add_argument('-a', '--algorithm',
                        choices=['brute', 'possible', 'all'],
                        default='possible',
                        help='Choose algorithm to solve the puzzle')

    parser.add_argument('filenames', metavar='filename', type=str, nargs='*',
                        help='list of files containing puzzles to solve')

    args = parser.parse_args()

    # Generate a Sudoku
    if not args.filenames:
        if args.verbose == 1:
            print("Generating a Sudoko...")
        generate_sudoku(args.difficulty, args.algorithm, args.verbose)
        sys.exit(0)

    # Otherwise, solve some puzzles
    for filename in args.filenames:
        if args.verbose == 1:
            print("Processing puzzle '%s'" % filename)
        solve_sudoku_from_filename(filename, args.algorithm, args.verbose)
