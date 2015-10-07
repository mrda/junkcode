#!/usr/bin/env python
#
# maze_binary.py <nums rows> <num cols> - build a maze using binary tree
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

from maze import Cell
from maze import Grid
import os
import random
import sys


def _flip_coin():
    """Returns True for a head, or False for tails"""
    return (random.randint(0, 1) == 0)


def _make_path(grid, row, col):
    cell = grid.get_cell(row, col)

    at_eastern_boundary = cell.east is None
    at_northern_boundary = cell.north is None

    if at_northern_boundary:
        # Have to choose east, unless top-right corner
        if at_eastern_boundary:
            return
        direction = 'east'
    elif at_eastern_boundary:
        direction = 'north'
    else:
        direction = 'north'
        if _flip_coin():
            direction = 'east'

    if direction == 'north':
        cell.link(cell.north)
    else:
        cell.link(cell.east)


def create_binary_maze(row_size, col_size):
    g = Grid(row_size, col_size)
    for row in reversed(range(row_size)):
        for col in range(col_size):
            _make_path(g, row, col)
    return g


if __name__ == '__main__':
    # Allow the user to specify a board size
    progname = os.path.basename(__file__)
    try:
        if len(sys.argv) == 1:
            rows, cols = 7, 7
        elif len(sys.argv) == 3:
            rows = int(sys.argv[1])
            cols = int(sys.argv[2])
        else:
            sys.exit('usage: %s [<num rows> <num cols>]' % progname)
    except ValueError:
        sys.exit('%s: Board sizes need to be integers' %
                 progname)

    maze = create_binary_maze(rows, cols)
    print maze
