#!/usr/bin/env python3
#
# maze.py - helper code for mazes
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

import random


class Cell(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self._links = {}

    def link(self, cell, bidi=True):
        if not cell:
            return
        self._links[cell] = True
        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi=True):
        if not cell:
            return
        if cell in self._links:
            del self._links[cell]
        if bidi:
            cell.unlink(self, False)

    def links(self):
        return self._links

    def islinked(self, cell):
        return cell in self._links

    def neighbours(self):
        n = []
        if self.north:
            n.append(self.north)
        if self.south:
            n.append(self.south)
        if self.east:
            n.append(self.east)
        if self.west:
            n.append(self.west)
        return n

    def __str__(self):
        s = "Cell at (%d, %d)\n" % (self.row, self.col)
        if self.north:
            s += "  North neighbour is (%d, %d)\n" % (self.north.row,
                                                      self.north.col)
        if self.south:
            s += "  South neighbour is (%d, %d)\n" % (self.south.row,
                                                      self.south.col)
        if self.east:
            s += "  East neighbour is (%d, %d)\n" % (self.east.row,
                                                     self.east.col)
        if self.west:
            s += "  West neighbour is (%d, %d)\n" % (self.west.row,
                                                     self.west.col)
        if self._links:
            for c in self._links:
                if self._links[c]:
                    s += "  Linked to Cell(%d, %d)\n" % (c.row, c.col)
        return s

    def coords(self):
        return (self.row, self.col)

    def coords_str(self):
        return "(%d, %d)" % (self.row, self.col)


class Grid(object):

    def __init__(self, rows, cols):
        self.row_size = rows
        self.col_size = cols
        self.clear_grid()

    def clear_grid(self, grid=None):
        if grid:
            grid = [[Cell(row, col) for col in range(grid.col_size)]
                    for row in range(grid.row_size)]
        else:
            self.grid = [[Cell(row, col) for col in range(self.col_size)]
                         for row in range(self.row_size)]

        for row in range(self.row_size):
            for col in range(self.col_size):
                if row != 0:
                    self.grid[row][col].north = self.grid[row-1][col]
                if row != self.row_size-1:
                    self.grid[row][col].south = self.grid[row+1][col]
                if col != 0:
                    self.grid[row][col].west = self.grid[row][col-1]
                if col != self.col_size-1:
                    self.grid[row][col].east = self.grid[row][col+1]

    def get_cell(self, row, col):
        if row < 0 or row >= self.row_size:
            return None
        if col < 0 or col >= self.col_size:
            return None
        return self.grid[row][col]

    def get_random_cell(self):
        rand_row = random.randrange(self.row_size)
        rand_col = random.randrange(self.col_size)
        return self.grid[rand_row][rand_col]

    def size(self):
        return self.row_size * self.col_size

    def each_row(self):
        for row in range(self.row_size):
            yield self.grid[row]

    def each_cell(self):
        for row in range(self.row_size):
            for col in range(self.col_size):
                yield self.grid[row][col]

    def dump(self):
        b = '+' + '-------' * self.col_size + '+' "\n"
        for row in range(self.row_size):
            b += '|'
            for col in range(self.col_size):
                b += self.grid[row][col].coords_str() + " "
            b += '|' + "\n"
        b += '+' + '-------' * self.col_size + '+' "\n"
        return b

    def __str__(self, curr_row=None, curr_col=None):
        output = '+' + '---+' * self.col_size + '\n'
        for row in range(self.row_size):
            output += '|'
            for col in range(self.col_size):
                if row == curr_row and col == curr_col:
                    output += ' * '
                else:
                    output += '   '
                cell = self.grid[row][col]
                if cell.islinked(cell.east):
                    output += ' '
                else:
                    output += '|'
            output += '\n+'
            for col in range(self.col_size):
                cell = self.grid[row][col]
                if cell.islinked(cell.south):
                    output += '   +'
                else:
                    output += '---+'
            output += '\n'
        return output

if __name__ == '__main__':

    import unittest

    class TestCell(unittest.TestCase):

        def setUp(self):
            self.a = Cell(1, 2)
            self.b = Cell(5, 6)
            self.c = Cell(5, 6)  # Same coords as b

        def test_initial_state(self):
            self.assertEqual(1, self.a.row)
            self.assertEqual(2, self.a.col)
            self.assertIsNone(self.a.north)
            self.assertIsNone(self.a.south)
            self.assertIsNone(self.a.east)
            self.assertIsNone(self.a.west)
            self.assertEqual(0, len(self.a._links))

        def test_birectional_links(self):
            self.a.link(self.b)
            self.assertTrue(self.a.islinked(self.b))
            self.assertTrue(self.b.islinked(self.a))

        def test_unidirectional_link(self):
            self.a.link(self.b, False)
            self.assertTrue(self.a.islinked(self.b))
            self.assertFalse(self.b.islinked(self.a))

        def test_link_unity(self):
            self.a.link(self.b)
            self.assertEqual(1, len(self.a._links))
            self.assertTrue(self.a.islinked(self.b))
            self.assertFalse(self.a.islinked(self.c))
            self.a.link(self.c)
            self.assertTrue(self.a.islinked(self.c))
            self.assertEqual(2, len(self.a._links))

        def test_neighbours(self):
            self.a.north = self.b
            self.a.west = self.c
            self.assertEqual(2, len(self.a.neighbours()))

    class TestGrid(unittest.TestCase):

        def setUp(self):
            self.g = Grid(10, 7)

        def test_top_left(self):
            cell = self.g.grid[0][0]
            self.assertEqual((1, 0), cell.south.coords())
            self.assertEqual((0, 1), cell.east.coords())
            self.assertIsNone(cell.north)
            self.assertIsNone(cell.west)

        def test_top_right(self):
            cell = self.g.grid[0][6]
            self.assertEqual((1, 6), cell.south.coords())
            self.assertEqual((0, 5), cell.west.coords())
            self.assertIsNone(cell.north)
            self.assertIsNone(cell.east)

        def test_bottom_right(self):
            cell = self.g.grid[9][6]
            self.assertEqual((8, 6), cell.north.coords())
            self.assertEqual((9, 5), cell.west.coords())
            self.assertIsNone(cell.south)
            self.assertIsNone(cell.east)

        def test_bottom_left(self):
            cell = self.g.grid[9][0]
            self.assertEqual((8, 0), cell.north.coords())
            self.assertEqual((9, 1), cell.east.coords())
            self.assertIsNone(cell.south)
            self.assertIsNone(cell.west)

        def test_happy_cell(self):
            cell = self.g.grid[4][3]
            self.assertEqual((3, 3), cell.north.coords())
            self.assertEqual((5, 3), cell.south.coords())
            self.assertEqual((4, 4), cell.east.coords())
            self.assertEqual((4, 2), cell.west.coords())

        def test_get_cell_ok(self):
            cell = self.g.get_cell(4, 3)
            self.assertEqual((4, 3), cell.coords())

        def test_get_cell_out_of_bounds(self):
            c = self.g.get_cell(-1, 3)
            d = self.g.get_cell(1, self.g.col_size)
            e = self.g.get_cell(-1, 300)
            self.assertIsNone(c)
            self.assertIsNone(d)
            self.assertIsNone(e)

        def test_get_random_cells(self):
            # When is enough? :-P
            for i in range(50):
                self.assertIsNotNone(self.g.get_random_cell())

        def test_size(self):
            self.assertEqual(70, self.g.size())

        def test_each_row(self):
            last_row = None
            count = 0
            for row in self.g.each_row():
                self.assertEqual(self.g.col_size, len(row))
                last_row = row
                count += 1
            cell_start = last_row[0]
            cell_end = last_row[6]
            self.assertEqual((9, 0), cell_start.coords())
            self.assertEqual((9, 6), cell_end.coords())
            self.assertEqual(self.g.row_size, count)

        def test_each_cell(self):
            first_cell = None
            last_cell = None
            count = 0
            for cell in self.g.each_cell():
                count += 1
                if not first_cell:
                    first_cell = cell
                last_cell = cell
            self.assertEqual((0, 0), first_cell.coords())
            self.assertEqual((9, 6), last_cell.coords())
            self.assertEqual(self.g.size(), count)

    unittest.main()
