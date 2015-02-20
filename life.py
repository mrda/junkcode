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
import os
import random
import sys
import time


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


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def build_randomised(life, base_row=0, base_col=0):
    # 1/n percentage of a square having life
    n = 10
    for row in range(life.max_row):
        for col in range(life.max_col):
            if random.randrange(0, n) == 1:
                life.create(row, col)


def initialise_life(life, x, y):
    # Randomly generate the initial life layout
    dispatch = [
        build_acorn,
        build_glider,
        build_lwss,
        build_beetle,
    ]
    dispatch[random.randrange(0, len(dispatch))](life, x, y)


if __name__ == '__main__':
    # Get the terminal size
    rows, cols = os.popen('stty size', 'r').read().split()
    rows = int(rows)
    cols = int(cols)

    life = Life(rows, cols)
    initialise_life(life, (rows/2-10), (cols/2-10))
    while(1):
        n = 0
        while(n < 150):
            clear_screen()
            print life
            life.tick()
            time.sleep(0.2)
            n += 1
        # Design shouts Designer
        build_randomised(life)
