#!/usr/bin/env python
#
# life - A simple implementation of Conway's Game of Life
#        Refer: http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
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
from select import select

import getopt
import glob
import os
import random
import sys
import time


# Number of default iterations before we start over
NUM_ITERATIONS = 250


class Life:

    def __init__(self, max_row, max_col):
        self.max_row = max_row
        self.max_col = max_col
        self.clear_board()

    def __str__(self):
        output = ''
        for row in range(self.max_row):
            for col in range(self.max_col):
                if self.board[row][col]:
                    output += 'O'
                else:
                    output += ' '
            output += '\n'
        return output

    def clear_board(self, board=None):
        if board:
            board = [[0 for x in range(b.max_col)] for x in range(b.max_row)]
        else:
            self.board = [[0 for x in range(self.max_col)]
                          for x in range(self.max_row)]

    def how_many_neighbours(self, row, col):
        neighbours = 0
        for row_delta in [-1, 0, +1]:
            for col_delta in [-1, 0, +1]:
                new_row = row + row_delta
                new_col = col + col_delta
                if (new_row in range(self.max_row) and
                   new_col in range(self.max_col)):
                    if self.board[new_row][new_col]:
                        neighbours += 1
        # Exclude ourselves
        if self.board[row][col]:
            neighbours -= 1
        return neighbours

    def create(self, row, col):
        self.board[row][col] = 1

    def check_for_life(self, row, col):
        neighbours = self.how_many_neighbours(row, col)
        if self.board[row][col] == 1:
            if neighbours in [2, 3]:
                return True
        else:
            if neighbours == 3:
                return True
        return False

    def tick(self):
        new_creation = Life(self.max_row, self.max_col)
        for row in range(self.max_row):
            for col in range(self.max_col):
                if self.check_for_life(row, col):
                    new_creation.create(row, col)
        self.board = new_creation.board


class CellQueue:

    def __init__(self):
        self.q = []
        self.idx = 0

    def add_filename(self, filename):
        self.q.append(filename)

    def length(self):
        return len(self.q)

    def next(self):
        elem = self.q[self.idx]
        if self.idx+1 < len(self.q):
            self.idx += 1
        else:
            self.idx = 0
        return elem


def build_acorn(life, base_row=40, base_col=12):
    life.create(base_row+1, base_col+2)
    life.create(base_row+2, base_col+4)
    life.create(base_row+3, base_col+1)
    life.create(base_row+3, base_col+2)
    life.create(base_row+3, base_col+5)
    life.create(base_row+3, base_col+6)
    life.create(base_row+3, base_col+7)


def build_glider(life, base_row=40, base_col=12):
    life.create(base_row+1, base_col+2)
    life.create(base_row+2, base_col+3)
    life.create(base_row+3, base_col+1)
    life.create(base_row+3, base_col+2)
    life.create(base_row+3, base_col+3)


def build_lwss(life, base_row=40, base_col=12):
    life.create(base_row+2, base_col+3)
    life.create(base_row+2, base_col+6)
    life.create(base_row+3, base_col+2)
    life.create(base_row+4, base_col+2)
    life.create(base_row+4, base_col+6)
    life.create(base_row+5, base_col+2)
    life.create(base_row+5, base_col+3)
    life.create(base_row+5, base_col+4)
    life.create(base_row+5, base_col+5)


def build_beetle(life, base_row=40, base_col=12):
    life.create(base_row+2, base_col+23)
    life.create(base_row+3, base_col+20)
    life.create(base_row+3, base_col+21)
    life.create(base_row+3, base_col+22)
    life.create(base_row+3, base_col+23)
    life.create(base_row+4, base_col+15)
    life.create(base_row+4, base_col+18)
    life.create(base_row+4, base_col+20)
    life.create(base_row+4, base_col+21)
    life.create(base_row+5, base_col+15)
    life.create(base_row+6, base_col+2)
    life.create(base_row+6, base_col+3)
    life.create(base_row+6, base_col+4)
    life.create(base_row+6, base_col+5)
    life.create(base_row+6, base_col+2)
    life.create(base_row+6, base_col+14)
    life.create(base_row+6, base_col+18)
    life.create(base_row+6, base_col+20)
    life.create(base_row+6, base_col+21)
    life.create(base_row+7, base_col+2)
    life.create(base_row+7, base_col+6)
    life.create(base_row+7, base_col+12)
    life.create(base_row+7, base_col+13)
    life.create(base_row+7, base_col+15)
    life.create(base_row+7, base_col+16)
    life.create(base_row+7, base_col+18)
    life.create(base_row+7, base_col+20)
    life.create(base_row+7, base_col+22)
    life.create(base_row+7, base_col+23)
    life.create(base_row+7, base_col+24)
    life.create(base_row+7, base_col+25)
    life.create(base_row+7, base_col+26)
    life.create(base_row+8, base_col+2)
    life.create(base_row+8, base_col+12)
    life.create(base_row+8, base_col+13)
    life.create(base_row+8, base_col+15)
    life.create(base_row+8, base_col+17)
    life.create(base_row+8, base_col+19)
    life.create(base_row+8, base_col+22)
    life.create(base_row+8, base_col+23)
    life.create(base_row+8, base_col+24)
    life.create(base_row+8, base_col+25)
    life.create(base_row+8, base_col+26)
    life.create(base_row+9, base_col+3)
    life.create(base_row+9, base_col+6)
    life.create(base_row+9, base_col+9)
    life.create(base_row+9, base_col+10)
    life.create(base_row+9, base_col+13)
    life.create(base_row+9, base_col+17)
    life.create(base_row+9, base_col+18)
    life.create(base_row+9, base_col+19)
    life.create(base_row+9, base_col+22)
    life.create(base_row+9, base_col+24)
    life.create(base_row+9, base_col+25)
    life.create(base_row+10, base_col+8)
    life.create(base_row+10, base_col+11)
    life.create(base_row+10, base_col+13)
    life.create(base_row+10, base_col+14)
    life.create(base_row+11, base_col+8)
    life.create(base_row+11, base_col+13)
    life.create(base_row+11, base_col+14)
    life.create(base_row+12, base_col+8)
    life.create(base_row+12, base_col+11)
    life.create(base_row+12, base_col+13)
    life.create(base_row+12, base_col+14)
    life.create(base_row+13, base_col+3)
    life.create(base_row+13, base_col+6)
    life.create(base_row+13, base_col+9)
    life.create(base_row+13, base_col+10)
    life.create(base_row+13, base_col+13)
    life.create(base_row+13, base_col+17)
    life.create(base_row+13, base_col+18)
    life.create(base_row+13, base_col+19)
    life.create(base_row+13, base_col+22)
    life.create(base_row+13, base_col+24)
    life.create(base_row+13, base_col+25)
    life.create(base_row+14, base_col+2)
    life.create(base_row+14, base_col+12)
    life.create(base_row+14, base_col+13)
    life.create(base_row+14, base_col+15)
    life.create(base_row+14, base_col+17)
    life.create(base_row+14, base_col+19)
    life.create(base_row+14, base_col+22)
    life.create(base_row+14, base_col+23)
    life.create(base_row+14, base_col+24)
    life.create(base_row+14, base_col+25)
    life.create(base_row+14, base_col+26)
    life.create(base_row+15, base_col+2)
    life.create(base_row+15, base_col+6)
    life.create(base_row+15, base_col+12)
    life.create(base_row+15, base_col+13)
    life.create(base_row+15, base_col+15)
    life.create(base_row+15, base_col+16)
    life.create(base_row+15, base_col+18)
    life.create(base_row+15, base_col+20)
    life.create(base_row+15, base_col+22)
    life.create(base_row+15, base_col+23)
    life.create(base_row+15, base_col+24)
    life.create(base_row+15, base_col+25)
    life.create(base_row+15, base_col+26)
    life.create(base_row+16, base_col+2)
    life.create(base_row+16, base_col+3)
    life.create(base_row+16, base_col+4)
    life.create(base_row+16, base_col+5)
    life.create(base_row+16, base_col+2)
    life.create(base_row+16, base_col+14)
    life.create(base_row+16, base_col+18)
    life.create(base_row+16, base_col+20)
    life.create(base_row+16, base_col+21)
    life.create(base_row+17, base_col+15)
    life.create(base_row+18, base_col+15)
    life.create(base_row+18, base_col+18)
    life.create(base_row+18, base_col+20)
    life.create(base_row+18, base_col+21)
    life.create(base_row+19, base_col+20)
    life.create(base_row+19, base_col+21)
    life.create(base_row+19, base_col+22)
    life.create(base_row+19, base_col+23)
    life.create(base_row+20, base_col+23)


def build_gosper_glider_gun(life, base_row=40, base_col=12):
    life.create(base_row+0, base_col+24)

    life.create(base_row+1, base_col+22)
    life.create(base_row+1, base_col+24)

    life.create(base_row+2, base_col+12)
    life.create(base_row+2, base_col+13)
    life.create(base_row+2, base_col+20)
    life.create(base_row+2, base_col+21)
    life.create(base_row+2, base_col+34)
    life.create(base_row+2, base_col+35)

    life.create(base_row+3, base_col+11)
    life.create(base_row+3, base_col+15)
    life.create(base_row+3, base_col+20)
    life.create(base_row+3, base_col+21)
    life.create(base_row+3, base_col+34)
    life.create(base_row+3, base_col+35)

    life.create(base_row+4, base_col+0)
    life.create(base_row+4, base_col+1)
    life.create(base_row+4, base_col+10)
    life.create(base_row+4, base_col+16)
    life.create(base_row+4, base_col+20)
    life.create(base_row+4, base_col+21)

    life.create(base_row+5, base_col+0)
    life.create(base_row+5, base_col+1)
    life.create(base_row+5, base_col+10)
    life.create(base_row+5, base_col+14)
    life.create(base_row+5, base_col+16)
    life.create(base_row+5, base_col+17)
    life.create(base_row+5, base_col+22)
    life.create(base_row+5, base_col+24)

    life.create(base_row+6, base_col+10)
    life.create(base_row+6, base_col+16)
    life.create(base_row+6, base_col+24)

    life.create(base_row+7, base_col+11)
    life.create(base_row+7, base_col+15)

    life.create(base_row+8, base_col+12)
    life.create(base_row+8, base_col+13)


def build_john_conway(life, base_row=40, base_col=12):
    # https://xkcd.com/2293/
    life.create(base_row+1, base_col+10)
    life.create(base_row+1, base_col+11)
    life.create(base_row+1, base_col+12)

    life.create(base_row+2, base_col+10)
    life.create(base_row+2, base_col+12)

    life.create(base_row+3, base_col+10)
    life.create(base_row+3, base_col+12)

    life.create(base_row+4, base_col+11)

    life.create(base_row+5, base_col+8)
    life.create(base_row+5, base_col+10)
    life.create(base_row+5, base_col+11)
    life.create(base_row+5, base_col+12)

    life.create(base_row+6, base_col+9)
    life.create(base_row+6, base_col+11)
    life.create(base_row+6, base_col+13)

    life.create(base_row+7, base_col+11)
    life.create(base_row+7, base_col+14)

    life.create(base_row+8, base_col+10)
    life.create(base_row+8, base_col+12)

    life.create(base_row+8, base_col+10)
    life.create(base_row+8, base_col+12)


def build_randomised(life, base_row=0, base_col=0):
    # 1/n percentage of a square having life
    n = 10
    for row in range(life.max_row):
        for col in range(life.max_col):
            if random.randrange(0, n) == 1:
                life.create(row, col)


def process_file(life, filename, base_row=40, base_col=12):
    # Note(mrda): Blank lines are important
    with open(filename) as f:
        row = 0
        for line in f:
            length = len(line)

            # Skip comment lines
            if line[0] == '!':
                continue

            for col, ch in enumerate(line):
                if ch == 'O':
                    life.create(base_row+row, base_col+col)
            row += 1


def add_directory(life, queue, directory):
    for fn in glob.glob(os.path.join(directory, "*.cells")):
        queue.add_filename(fn)


def pick_builtin_sim(life, x, y):
    # Randomly generate the initial life layout
    dispatch = [
        build_acorn,
        build_glider,
        build_lwss,
        build_beetle,
        build_gosper_glider_gun,
        build_randomised,
        build_john_conway,
    ]
    dispatch[random.randrange(0, len(dispatch))](life, x, y)


def time_to_exit(timeout=None):
    # Note(mrda): select() on stdin might not work on non-Unixes
    exit = False
    if not timeout:
        timeout = 0.4  # seconds
    rlist, wlist, xlist = select([sys.stdin], {}, {}, timeout)
    if rlist:
        s = sys.stdin.readline().rstrip()
        if s in ['q', 'Q']:
            exit = True
    return exit


def print_exit_info(row, cols, timeout=None):
    # Clear the screen in a platform independent way
    os.system(['clear', 'cls'][os.name == 'nt'])
    if not timeout:
        timeout = 3  # seconds
    message = "Life: Press 'q' and <RETURN> to exit"
    center_spacing = (cols - len(message)) // 2
    vertical_spacing = int(1.0/3 * rows)
    print('\n' * vertical_spacing)
    print(' ' * center_spacing + message)
    time.sleep(timeout)


def reset_board(life, x, y, queue=None):
    if queue is None or queue.length() == 0:
        pick_builtin_sim(life, (rows//2-10), (cols//2-10))
    else:
        process_file(life, queue.next())


def usage():
    myname = os.path.basename(sys.argv[0])
    print("Usage: {} [-h|--help] [-i|--iterations <iterations>] "
          "[-s|--speed <seconds>] "
          "[files or directories]".format(myname))
    print("\nYou can find definition files at https://www.conwaylife.com/")


if __name__ == '__main__':
    # Get the terminal size
    rows, cols = os.popen('stty size', 'r').read().split()
    rows = int(rows)
    cols = int(cols)

    iterations = NUM_ITERATIONS
    speed = 0.5  # seconds

    # Command line processing
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:s:',
                                   ['help', 'iterations=', 'speed='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-s', '--speed'):
            try:
                speed = float(a)
            except Exception as e:
                print(e)
                usage()
                sys.exit(3)
        elif o in ('-i', '--iterations'):
            try:
                iterations = int(a)
            except Exception as e:
                print(e)
                usage()
                sys.exit(4)

    # Create the petri dish
    life = Life(rows, cols)

    my_queue = CellQueue()

    for ford in args:
        if os.path.isfile(ford):
            my_queue.add_filename(ford)
        elif os.path.isdir(ford):
            add_directory(life, my_queue, ford)

    # TODO(mrda): We should check to see that the petri dish is large
    # enough for the simulation that we're prepopulating.

    init_x = rows//2-10
    init_y = cols//2-10

    # Design shouts Designer
    reset_board(life, init_x, init_y, my_queue)
    exit = False
    while(not exit):
        print_exit_info(rows, cols)
        n = 0
        while(n < iterations and not exit):
            print(life)
            life.tick()
            n += 1
            exit = time_to_exit(speed)
        life.clear_board()
        reset_board(life, init_x, init_y, my_queue)
