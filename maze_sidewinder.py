#!/usr/bin/env python
#
# maze_sidewinder.py <nums rows> <num cols> - build a maze following the
#                                             sidewinder algorithm
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


def _choose_random_element(list_of_elems):
    idx = random.randint(0, len(list_of_elems)-1)
    return list_of_elems[idx]


def create_sidewinder_maze(row_size, col_size):
    g = Grid(row_size, col_size)
    for row in reversed(range(row_size)):
        current_run = []
        for col in range(col_size):
            cell = g.get_cell(row, col)
            current_run.append(cell)

            at_eastern_boundary = cell.east is None
            at_northern_boundary = cell.north is None

            close_out_run = (
                at_eastern_boundary or
                (not at_northern_boundary and _flip_coin()))

            if close_out_run:
                chosen_cell = _choose_random_element(current_run)
                chosen_cell.link(chosen_cell.north)
                current_run = []
            else:
                cell.link(cell.east)
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

    maze = create_sidewinder_maze(rows, cols)
    print maze
