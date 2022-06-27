#!/usr/bin/env python3
#
# periodictable.py - Display a simplistic periodic table
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


class Element(object):

    def __init__(self, name, symbol, atomic_number):
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number


class PeriodicTable(object):

    def __init__(self, maxrow=10, maxcol=18):
        self.maxrow = maxrow
        self.maxcol = maxcol
        self.table = [[None for c in range(maxcol)]
                      for r in range(maxrow)]
        self.SPACING = '       '
        self.EXTSPACING = self.SPACING + ' '

    def add_element(self, name, symbol, atomic_number, row, col):
        self.table[row-1][col-1] = Element(name, symbol, atomic_number)

    def _centre(self, st):
        return st.center(len(self.SPACING), ' ')

    def is_right_cell_occupied(self, row, col):
        if col == self.maxcol-1:
            return False
        return self.table[row][col+1] is not None

    def is_left_cell_occupied(self, row, col):
        if col == 0:
            return False
        return self.table[row][col-1] is not None

    def is_top_row(self, row, col):
        return row == 0

    def is_leftmost_cell(self, row, col):
        return col == 0

    def is_rightmost_cell(self, row, col):
        return col == self.maxcol-1

    def is_cell_below_occupied(self, row, col):
        if row == self.maxrow:
            return False
        return self.table[row+1][col] is None

    def is_cell_above_occupied(self, row, col):
        if row == 0:
            return False
        return self.table[row-1][col] is not None

    def is_cell_occupied(self, row, col):
        return self.table[row][col] is not None

    def is_cell_above_and_right_occupied(self, row, col):
        if row == 0 or col == self.maxcol-1:
            return False
        return self.table[row-1][col+1] is not None

    def is_cell_above_and_left_occupied(self, row, col):
        if row == 0 or col == 0:
            return False
        return self.table[row-1][col-1] is not None

    def __str__(self):
        output = ''
        lastrow = -1

        for r in range(self.maxrow):
            topline = ''
            firstline = ''
            secondline = ''
            firstcolinrow = -1

            for c in range(self.maxcol):
                e = self.table[r][c]
                anycellsinrow = False

                firstcellinrow = False
                # Keep track of the first column occupied in a row
                if self.is_cell_occupied(r, c):
                    anycellsinrow = True
                    if lastrow != r:
                        # This is the first cell occupied in the row
                        firstcellinrow = True
                        lastrow = r
                        firstcolinrow = c

                # Work out the topline first
                if (self.is_cell_occupied(r, c) or
                   self.is_cell_above_occupied(r, c) or
                   self.is_cell_above_and_left_occupied(r, c)):
                    if not (self.is_cell_occupied(r, c-1) and
                            not self.is_right_cell_occupied(r, c-1)):
                        topline += '+'
                else:
                    if not self.is_left_cell_occupied(r, c):
                        topline += ' '
                if (self.is_cell_occupied(r, c) or
                   self.is_cell_above_occupied(r, c)):
                    topline += '-------'
                else:
                    topline += self.SPACING

                # Add in '+' on the top right corner where no right cell
                if (self.is_cell_occupied(r, c) and
                   not self.is_right_cell_occupied(r, c)):
                    topline += '+'
                # Or if there are no cells underneath, ie. a blank line
                if c == self.maxcol-1 and not anycellsinrow:
                    topline += '+'

                # Add in the left-most '|' for this cell
                if self.is_cell_occupied(r, c):
                    if self.is_leftmost_cell(r, c):
                        firstline += '|'
                        secondline += '|'
                    firstline += self._centre(str(e.atomic_number))
                    secondline += self._centre(str(e.symbol))
                else:
                    # If we're in the first col, but the cell isn't occupied,
                    # we need an extra space
                    if c == 0:
                        firstline += ' '
                        secondline += ' '
                    firstline += self.SPACING
                    secondline += self.SPACING

                # Work out the right edge
                if (self.is_right_cell_occupied(r, c) or
                   self.is_rightmost_cell(r, c) or
                   (self.is_cell_occupied(r, c) and
                       not self.is_right_cell_occupied(r, c))):
                    # Need to exclude the right-most '|' for blank rows
                    if not anycellsinrow and c == self.maxcol-1:
                        firstline += ' '
                        secondline += ' '
                    else:
                        firstline += '|'
                        secondline += '|'
                else:
                    firstline += ' '
                    secondline += ' '

            output += topline + '\n'
            output += firstline + '\n'
            output += secondline + '\n'

        # Fix up the last row
        # The last row might not start with a box, so add padding if necessary
        padcol = self.maxcol - firstcolinrow

        output += '        ' * firstcolinrow + '+-------' * padcol + '+'
        output += '\n'

        return output


def get_periodic_table():
    p = PeriodicTable()

    p.add_element('Hydrogen', 'H', 1, 1, 1)
    p.add_element('Helium', 'He', 2, 1, 18)

    p.add_element('Lithium', 'Li', 3, 2, 1)
    p.add_element('Berelium', 'Be', 4, 2, 2)
    p.add_element('Boron', 'B', 5, 2, 13)
    p.add_element('Carbon', 'C', 6, 2, 14)
    p.add_element('Nitrogen', 'N', 7, 2, 15)
    p.add_element('Oxygen', 'O', 8, 2, 16)
    p.add_element('Fluorine', 'F', 9, 2, 17)
    p.add_element('Neon', 'Ne', 10, 2, 18)
    p.add_element('Sodium', 'Na', 11, 3, 1)
    p.add_element('Magnesium', 'Mg', 12, 3, 2)
    p.add_element('Aluminium', 'Al', 13, 3, 13)
    p.add_element('Silicon', 'Si', 14, 3, 14)
    p.add_element('Phosphoros', 'P', 15, 3, 15)
    p.add_element('Sulfur', 'S', 16, 3, 16)
    p.add_element('Chlorine', 'Cl', 17, 3, 17)
    p.add_element('Argon', 'Ar', 18, 3, 18)

    p.add_element('Potassium', 'K', 19, 4, 1)
    p.add_element('Calcium', 'Ca', 20, 4, 2)
    p.add_element('Scandium', 'Sc', 21, 4, 3)
    p.add_element('Titanium', 'Ti', 22, 4, 4)
    p.add_element('Vanadium', 'V', 23, 4, 5)
    p.add_element('Chromium', 'Cr', 24, 4, 6)
    p.add_element('Manganese', 'Mn', 25, 4, 7)
    p.add_element('Iron', 'Fe', 26, 4, 8)
    p.add_element('Cobalt', 'Co', 27, 4, 9)
    p.add_element('Nickel', 'Ni', 28, 4, 10)
    p.add_element('Copper', 'Cu', 29, 4, 11)
    p.add_element('Zinc', 'Zn', 30, 4, 12)
    p.add_element('Gallium', 'Ga', 31, 4, 13)
    p.add_element('Germanium', 'Ge', 32, 4, 14)
    p.add_element('Arsenic', 'As', 33, 4, 15)
    p.add_element('Selenium', 'Se', 34, 4, 16)
    p.add_element('Bromine', 'Br', 35, 4, 17)
    p.add_element('Krypton', 'Kr', 36, 4, 18)

    p.add_element('Rubidium', 'Rb', 37, 5, 1)
    p.add_element('Strontium', 'Sr', 38, 5, 2)
    p.add_element('Yttrium', 'Y', 39, 5, 3)
    p.add_element('Zirconium', 'Zr', 40, 5, 4)
    p.add_element('Niobium', 'Nb', 41, 5, 5)
    p.add_element('Molybdenum', 'Mo', 42, 5, 6)
    p.add_element('Technetium', 'Tc', 43, 5, 7)
    p.add_element('Ruthenium', 'Ru', 44, 5, 8)
    p.add_element('Rhodium', 'Rh', 45, 5, 9)
    p.add_element('Palladium', 'Pd', 46, 5, 10)
    p.add_element('Silver', 'Ag', 47, 5, 11)
    p.add_element('Cadmium', 'Ca', 48, 5, 12)
    p.add_element('Indium', 'In', 49, 5, 13)
    p.add_element('Tin', 'Sn', 50, 5, 14)
    p.add_element('Antimony', 'Sb', 51, 5, 15)
    p.add_element('Tellurium', 'Te', 52, 5, 16)
    p.add_element('Iodine', 'I', 53, 5, 17)
    p.add_element('Xenon', 'Xe', 54, 5, 18)

    p.add_element('Caesium', 'Cs', 55, 6, 1)
    p.add_element('Barium', 'Ba', 56, 6, 2)
#    p.add_element('Blank', 'Bla', 57, 6, 3)
    p.add_element('Hafnium', 'Hf', 72, 6, 4)
    p.add_element('Tantalum', 'Ta', 73, 6, 5)
    p.add_element('Tungsten', 'W', 74, 6, 6)
    p.add_element('Rhenium', 'Re', 75, 6, 7)
    p.add_element('Osmium', 'Os', 76, 6, 8)
    p.add_element('Iridium', 'Ir', 77, 6, 9)
    p.add_element('Platinum', 'Pt', 78, 6, 10)
    p.add_element('Gold', 'Au', 79, 6, 11)
    p.add_element('Mercury', 'Hg', 80, 6, 12)
    p.add_element('Thalium', 'Tl', 81, 6, 13)
    p.add_element('Lead', 'Pb', 82, 6, 14)
    p.add_element('Bismuth', 'Bi', 83, 6, 15)
    p.add_element('Polonium', 'Po', 84, 6, 16)
    p.add_element('Astatine', 'At', 85, 6, 17)
    p.add_element('Radon', 'Rn', 86, 6, 18)

    p.add_element('Francium', 'Fr', 87, 7, 1)
    p.add_element('Radium', 'Ra', 88, 7, 2)
#    p.add_element('Blank', 'Bla', 89, 7, 3)
    p.add_element('Rutherfordium', 'Rf', 104, 7, 4)
    p.add_element('Dubnium', 'Db', 105, 7, 5)
    p.add_element('Seaborgium', 'Sg', 106, 7, 6)
    p.add_element('Bohrium', 'Bh', 107, 7, 7)
    p.add_element('Hassium', 'Hs', 108, 7, 8)
    p.add_element('Meitnreium', 'Mt', 109, 7, 9)
    p.add_element('Damstadium', 'Ds', 110, 7, 10)
    p.add_element('Roentgenium', 'Rg', 111, 7, 11)
    p.add_element('Copernicium', 'Cn', 112, 7, 12)
    p.add_element('Nihonium', 'Nh', 113, 7, 13)
    p.add_element('Flerovium', 'Fl', 114, 7, 14)
    p.add_element('Moscovium', 'Mc', 115, 7, 15)
    p.add_element('Livermonium', 'Lv', 116, 7, 16)
    p.add_element('Tennessine', 'Ts', 117, 7, 17)
    p.add_element('Organesson', 'Og', 118, 7, 18)

    # Lanthanoids
    p.add_element('Lanthanum', 'La', 57, 9, 4)
    p.add_element('Cerium', 'Ce', 58, 9, 5)
    p.add_element('Praeseodymium', 'Pr', 59, 9, 6)
    p.add_element('Neodymium', 'Nd', 60, 9, 7)
    p.add_element('Promethium', 'Pm', 61, 9, 8)
    p.add_element('Samarium', 'Sm', 62, 9, 9)
    p.add_element('Europium', 'Eu', 63, 9, 10)
    p.add_element('Gadolinium', 'Gd', 64, 9, 11)
    p.add_element('Terbium', 'Tb', 65, 9, 12)
    p.add_element('Dysprosium', 'Dy', 66, 9, 13)
    p.add_element('Holmium', 'Ho', 67, 9, 14)
    p.add_element('Erbium', 'Er', 68, 9, 15)
    p.add_element('Thulium', 'Tm', 69, 9, 16)
    p.add_element('Ytterbium', 'Yb', 70, 9, 17)
    p.add_element('Lutetium', 'Lu', 71, 9, 18)

    # Actinoids
    p.add_element('Actinium', 'Ac', 89, 10, 4)
    p.add_element('Thorium', 'Th', 90, 10, 5)
    p.add_element('Protactinium', 'Pa', 91, 10, 6)
    p.add_element('Uranium', 'U', 92, 10, 7)
    p.add_element('Neptunium', 'Np', 93, 10, 8)
    p.add_element('Plutonium', 'Pu', 94, 10, 9)
    p.add_element('Americium', 'Am', 95, 10, 10)
    p.add_element('Curium', 'Cm', 96, 10, 11)
    p.add_element('Berkelium', 'Bk', 97, 10, 12)
    p.add_element('Californium', 'Cf', 98, 10, 13)
    p.add_element('Einsteinium', 'Es', 99, 10, 14)
    p.add_element('Fermium', 'Fm', 100, 10, 15)
    p.add_element('Mendelevium', 'Md', 101, 10, 16)
    p.add_element('Nobelium', 'No', 102, 10, 17)
    p.add_element('Lawrencium', 'Lr', 103, 10, 18)

    return p.__str__()


if __name__ == '__main__':
    p = get_periodic_table()
    print(p)
