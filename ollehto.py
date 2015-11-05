#!/usr/bin/env python
#
# ollehto.py - play the game of ollehto
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

DOT = '.'
FREE = ' '
DARK = 'X'
LIGHT = 'O'

HUMAN = 'human'
ROBOT = 'robot'

import inspect


class Cell(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.owner = FREE

    def isfree(self):
        return self.owner == FREE

    def __str__(self):
        if self.isfree():
            s = " is free"
        else:
            s = " is owned by %s" % self.owner
        return "Cell at (%d, %d) %s" % (self.row, self.col, s)


class Board(object):

    def __init__(self, rows=8, cols=8):
        self.row_size = rows
        self.col_size = cols
        self.clear_grid()

    def set(self, row, col, owner):
        self.grid[row][col].owner = owner

    def initialise_board(self):
        """Initialise the board to the starting positions"""
        self.set(3, 3, LIGHT)
        self.set(4, 4, LIGHT)
        self.set(3, 4, DARK)
        self.set(4, 3, DARK)

    def clear_grid(self, grid=None):
        if grid:
            grid = [[Cell(row, col) for col in range(grid.col_size)]
                    for row in range(grid.row_size)]
        else:
            self.grid = [[Cell(row, col) for col in range(self.col_size)]
                         for row in range(self.row_size)]

    def dump(self):
        b = '+' + '-------' * self.col_size + '+' "\n"
        for row in range(self.row_size):
            b += '|'
            for col in range(self.col_size):
                b += self.grid[row][col].coords_str() + " "
            b += '|' + "\n"
        b += '+' + '-------' * self.col_size + '+' "\n"
        return b

    def _centre(self, st, width=4):
        return st.center(width, ' ')

    def format_coords(self, row, col):
        return('%s%s' % (chr(65+row), col))

    def __str__(self, curr_row=None, curr_col=None, include_score=True):
        output = '     '
        for r in range(self.row_size):
            output += self._centre(str(r))
        output += '\n'
        output += '    '
        output += '+' + '---+' * self.col_size + '\n'
        for row in range(self.row_size):
            output += self._centre(chr(65+row))
            output += '|'
            for col in range(self.col_size):
                cell = self.grid[row][col]
                output += ' ' + cell.owner + ' '
                output += '|'
            output += '\n'
            output += '    '
            output += '+'
            for col in range(self.col_size):
                cell = self.grid[row][col]
                output += '---+'
            output += '\n'
        if include_score:
            s = 'Score: White=%d. Black=%d' % (self.score(LIGHT),
                                               self.score(DARK))
            output += self._centre(s, 38)
        output += '\n'
        return output

    def is_on_board(self, row, col):
        """Check to see that the row, col is on this board"""
        # Ignore row where off the board
        if row < 0 or row >= self.row_size:
            return False
        # Ignore col where off the board
        if col < 0 or col >= self.col_size:
            return False
        return True

    def get_opponent(self, colour):
        if colour == DARK:
            return LIGHT
        return DARK

    def copy_board(self):
        b = Board(self.row_size, self.col_size)
        for row in range(self.row_size):
            for col in range(self.col_size):
                b.set(row, col, self.grid[row][col].owner)
        return b

    def build_possibilities_board(self, candidates):
        cand_board = self.copy_board()
        for cand in candidates:
            cand_board.set(cand['row'], cand['col'], DOT)
        return cand_board

    def find_all_valid_moves(self, colour):
        slots = []
        for row in range(self.row_size):
            for col in range(self.col_size):
                cell = self.grid[row][col]
                if cell.owner == colour:
                    cell_cands = (
                        self.find_valid_moves_for_cell(row, col, colour))
                    slots.extend(cell_cands)
        return slots

    def find_valid_moves_for_cell(self, row, col, colour):
        candidate_list = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:

                # Ignore the zero transform
                if dr == 0 and dc == 0:
                    continue

                # Keep searching in this direction until we find
                # that this spot is invalid, or is valid
                dir_result = self.valid_moves_for_cell_in_direction(row,
                                                                    col,
                                                                    dr,
                                                                    dc,
                                                                    colour)
                if dir_result is not None:
                    candidate_list.append(dir_result)

        return candidate_list

    def valid_moves_for_cell_in_direction(self, row, col, dr, dc, colour):
        opponent = self.get_opponent(colour)

        cand_row = row
        cand_col = col

        flips = []

        while True:

            cand_row += dr
            cand_col += dc

            if not self.is_on_board(cand_row, cand_col):
                return None
            elif self.grid[cand_row][cand_col].owner == FREE:
                if len(flips) > 0:
                    result = {'row': cand_row,
                              'col': cand_col,
                              'count': len(flips),
                              'flips': flips}
                    return result
                else:
                    return None
            elif self.grid[cand_row][cand_col].owner == opponent:
                flips.append((cand_row, cand_col))
            elif self.grid[cand_row][cand_col].owner == colour:
                return None

    def _print_candidates(self, candidates):
        for c in candidates:
            print("Possible candidates are: %s with count %d" %
                  (self.format_coords(c['row'], c['col']), c['count']))
            print("  and they are:")
            st = ""
            for f in c['flips']:
                st += self.format_coords(f[0], f[1]) + " "
            print("  " + st)

    def is_valid_move(self, row, col, colour):
        candidates = self.find_all_valid_moves(colour)
        for candidate in candidates:
            if candidate['row'] == row and candidate['col'] == col:
                return True
        return False

    def score(self, colour):
        count = 0
        for row in range(self.row_size):
            for col in range(self.col_size):
                if self.grid[row][col].owner == colour:
                    count += 1
        return count

    def find_flips_in_direction(self, row, col, dr, dc, colour):
        """ Search in dr, dc direction from row, col and find all the flips
        required """
        opponent = self.get_opponent(colour)

        flips = []

        cand_row = row
        cand_col = col

        while True:
            cand_row += dr
            cand_col += dc

            if not self.is_on_board(cand_row, cand_col):
                return None
            elif self.grid[cand_row][cand_col].owner == FREE:
                return None
            elif self.grid[cand_row][cand_col].owner == opponent:
                flips.append((cand_row, cand_col))
            elif self.grid[cand_row][cand_col].owner == colour:
                return flips

    def find_flips(self, row, col, colour):
        """ Find the tokens that need to flip as a result of player
        placing a token at row, col"""
        all_flips = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:

                # Ignore the zero transform
                if dr == 0 and dc == 0:
                    continue

                flips = self.find_flips_in_direction(row, col, dr, dc, colour)
                if flips is not None:
                    all_flips.extend(flips)

        return all_flips

    def make_move(self, row, col, colour):
        self.grid[row][col].owner = colour
        flips = self.find_flips(row, col, colour)
        for f in flips:
            self.grid[f[0]][f[1]].owner = colour


class Player(object):

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def make_move(self, board):
        # http://norvig.com/python-iaq.html
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')


class Human(Player):

    def __init__(self, name, colour):
        self.kind = HUMAN
        super(Human, self).__init__(name, colour)

    def make_move(self, board):
        valid_moves = board.find_all_valid_moves(self.colour)
        if len(valid_moves) == 0:
            print("Sorry %s, there are no valid moves for you. "
                  "You have to skip" % self.name)
            return True

        row, col = self.get_user_input(board, valid_moves)
        board.make_move(row, col, self.colour)
        return False

    def get_user_input(self, board, valid_moves):
        input_str = (
            "%s, you're playing %s and it's your turn.  Enter your move: "
            % (self.name, self.colour))
        possibility_board = board.build_possibilities_board(valid_moves)
        valid_move = False
        while not valid_move:
            print possibility_board
            raw_move = raw_input(input_str).upper()
            if raw_move is None or raw_move == '':
                continue

            move = raw_move.strip()
            try:
                row = ord(move[0]) - 65  # 'A' == 65
                col = int(move[1])
            except ValueError:
                # Don't care what the problem is, the entered
                # characters just aren't valid
                row = -1
                col = -1

            if board.is_valid_move(row, col, self.colour):
                valid_move = True
            else:
                print "Sorry, '%s' is an invalid move" % raw_move
        return row, col


class Robot(Player):

    def __init__(self, name, colour):
        self.kind = ROBOT
        super(Robot, self).__init__(name, colour)


class SimpleRobot(Robot):

    def __init__(self, colour):
        name = 'Penny'
        super(SimpleRobot, self).__init__(name, colour)

    def make_move(self, board):
        best_move = None
        for move in board.find_all_valid_moves(self.colour):
            if best_move is None:
                best_move = move
            else:
                if move['count'] > best_move['count']:
                    best_move = move
        if best_move is None:
            print("%s must skip a move :-(" % self.name)
            return True  # Must skip a move
        else:
            print("%s has decided to move to %s" %
                  (self.name,
                   board.format_coords(best_move['row'], best_move['col'])))
            board.make_move(best_move['row'], best_move['col'], self.colour)
            return False


class Game(object):

    def __init__(self, player1, player2):
        self.b = Board()
        self.b.initialise_board()
        self.player1 = player1
        self.player2 = player2

    def print_valid_moves(self, colour, valid_moves):
        for move in valid_moves:
            coords = self.b.format_coords(move['row'], move['col'])
            print("Player %s can choose %s which has a count of %d" %
                  (colour, coords, move['count']))

    def _debug_current_moves(self, board):
        for colour in (DARK, LIGHT):
            valid_moves = self.b.find_all_valid_moves(colour)
            self.print_valid_moves(colour, valid_moves)

    def end_of_game_message(self, winner, player1_score, player2_score):
        print "***** GAME OVER *****"
        s1 = max(player1_score, player2_score)
        s2 = min(player1_score, player2_score)
        if winner is not None:
            report = ("Congratulations %s, you won %d to %d\n"
                      % (winner.name, s1, s2))
        else:
            report = "Wow, a draw! Congratulations to both players!\n"
        return report

    def determine_winner(self, player1_score, player2_score):
        if player1_score > player2_score:
            winning_player = self.player1
        elif player2_score > player1_score:
            winning_player = self.player2
        else:
            winning_player = None
        return winning_player

    def play_game(self):
        still_playing = True
        player1_skip = False
        player2_skip = False

        while still_playing:
            player1_skip = self.player1.make_move(self.b)
            if player1_skip and player2_skip:
                break

            player2_skip = self.player2.make_move(self.b)
            if player1_skip and player2_skip:
                break

        player1_score = self.b.score(player1.colour)
        player2_score = self.b.score(player2.colour)
        winner = self.determine_winner(player1_score, player2_score)

        print self.end_of_game_message(winner, player1_score, player2_score)
        print self.b.__str__(include_score=False)

        return winner, player1_score, player2_score


if __name__ == '__main__':

    player1 = Human('Michael', DARK)
    player2 = SimpleRobot(LIGHT)

    g = Game(player1, player2)
    winner, player1_score, player2_score = g.play_game()
