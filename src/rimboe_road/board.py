# board.py

from enum import Enum
import random
import numpy as np
import pandas


class Mark(Enum):
    H = 1
    A = 2
    FULL = 3
    EMPTY = 4


class State(Enum):
    DRAW = 1
    ONGOING = 2
    OVER = 3


class Board:
    def __init__(self, size, turn):
        self.size = size
        self.labels = np.arange(1, self.size + 1)
        self.matrix = [[Mark.EMPTY.value for x in range(size)] for y in
                       range(size)]
        # Randomly choose starting player
        tmp = [Mark.H, Mark.A]
        self.turn_to_play = tmp[0-turn]
        self.last_to_play = tmp[-1-turn]

        self.a_pos = None
        self.h_pos = None

        self.state = State.ONGOING
        self.winner = None
        self.moves = []
        self.real_game = True
        self.last_turn = False
        self.heuristic_value = 0

        if self.real_game:
            self.board_report = "Starting player: " + str(self.turn_to_play) + "\n"
            self.board_report += self.print_board()

    def get_turn_to_play(self):
        return self.turn_to_play

    def get_state(self):
        return self.state

    def get_winner(self):
        return self.winner

    def get_board_report(self):
        return self.board_report

    def get_heuristic_value(self):
        return self.heuristic_value

    def set_real_game(self, value):
        self.real_game = value

    def get_pos(self):
        if len(self.moves) > 1:
            return self.moves[-2]
        else:
            return None

    def set_pos(self, pos):
        if self.get_turn_to_play() == Mark.A:
            self.a_pos = pos
        else:
            self.h_pos = pos

    def get_random_pos(self):
        pos = None
        while pos is None:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.matrix[x][y] == Mark.EMPTY.value:
                pos = (x, y)
        return pos

    def get_possible_moves(self, pos):
        possible_moves = []
        for value in range(1, 4):
            if pos[0] - value >= 0:
                tmp_x = pos[0] - value
                if self.matrix[tmp_x][pos[1]] == Mark.EMPTY.value:
                    possible_moves.append((tmp_x, pos[1]))
            if pos[0] + value < self.size:
                tmp_x = pos[0] + value
                if self.matrix[tmp_x][pos[1]] == Mark.EMPTY.value:
                    possible_moves.append((tmp_x, pos[1]))
            if pos[1] - value >= 0:
                tmp_y = pos[1] - value
                if self.matrix[pos[0]][tmp_y] == Mark.EMPTY.value:
                    possible_moves.append((pos[0], tmp_y))
            if pos[1] + value < self.size:
                tmp_y = pos[1] + value
                if self.matrix[pos[0]][tmp_y] == Mark.EMPTY.value:
                    possible_moves.append((pos[0], tmp_y))
        random.shuffle(possible_moves)
        return possible_moves

    def is_free(self, pos):
        if self.matrix[pos[0]][pos[1]] == Mark.EMPTY.value:
            return True
        return False

    def make_move(self, new_pos):
        old_pos = None
        # Check if this is a player's first move
        if len(self.moves) > 1:
            old_pos = self.moves[-2]
        if old_pos is not None:
            self.matrix[old_pos[0]][old_pos[1]] = Mark.FULL.value
        self.matrix[new_pos[0]][new_pos[1]] = self.turn_to_play.value
        self.set_pos(new_pos)

        if self.real_game:
            self.turn_string()

        self.__update_board_state()
        # self.__update_heuristic_value()
        self.__switch_players()
        self.moves.append(new_pos)
        if self.last_turn is True and self.real_game is False:
            self.make_move(self.finish_last_turn())
            self.undo()

    def finish_last_turn(self):
        pos = self.get_pos()
        moves = self.get_possible_moves(pos)
        for move in moves:
            if len(self.get_possible_moves(move)) > 0:
                return move
        return moves[0]

    def undo(self):
        old_pos = self.moves[-3]
        last_move = self.moves.pop()
        if last_move:
            self.matrix[last_move[0]][last_move[1]] = Mark.EMPTY.value
            self.__switch_players()
            self.matrix[old_pos[0]][old_pos[1]] = self.turn_to_play.value
            self.set_pos(old_pos)

    def turn_string(self):
        self.board_report += "\n/---------------------/\n"
        self.board_report += str(self.get_turn_to_play()) + " played: \n"
        self.board_report += self.print_board()

    def evaluate_board_state(self):
        if self.a_pos is None or self.h_pos is None:
            return State.ONGOING

        a_move_amount = len(self.get_possible_moves(self.a_pos))
        h_move_amount = len(self.get_possible_moves(self.h_pos))

        tot_move_amount = a_move_amount + h_move_amount
        if tot_move_amount == 0:
            self.heuristic_value = 0
        else:
            self.heuristic_value = (a_move_amount - h_move_amount) / tot_move_amount

        flag = False
        if self.last_to_play != self.turn_to_play:
            flag = True

        if a_move_amount == 0 and h_move_amount > 0:
            if flag and self.last_to_play == Mark.H:
                self.last_turn = True
                return State.ONGOING
            self.winner = Mark.H.value

            return State.OVER

        if h_move_amount == 0 and a_move_amount > 0:
            if flag and self.last_to_play == Mark.A:
                self.last_turn = True
                return State.ONGOING
            self.winner = Mark.A.value

            return State.OVER

        if h_move_amount == 0 and a_move_amount == 0:
            if self.turn_to_play != self.last_to_play:
                if self.turn_to_play == Mark.A:
                    self.winner = Mark.A.value
                    return State.OVER
                else:
                    self.winner = Mark.H.value
                    return State.OVER
            else:
                return State.DRAW

        return State.ONGOING

    # def __update_heuristic_value(self):
    #     a_move_amount = len(self.get_possible_moves(self.a_pos))
    #     h_move_amount = len(self.get_possible_moves(self.h_pos))
    #
    #     tot_move_amount = a_move_amount + h_move_amount
    #     if tot_move_amount == 0:
    #         self.heuristic_value = 0
    #     else:
    #         self.heuristic_value = (a_move_amount - h_move_amount) / tot_move_amount

    def __update_board_state(self):
        self.winner = None
        self.last_turn = False
        self.heuristic = None
        self.state = self.evaluate_board_state()

    def __switch_players(self):
        self.turn_to_play = Mark.H if self.turn_to_play is Mark.A else Mark.A

    def print_board(self):
        display_matrix = np.full((self.size, self.size), "\0")
        for idx1 in range(self.size):
            for idx2 in range(self.size):
                if self.matrix[idx1][idx2] == Mark.FULL.value:
                    display_matrix[idx1][idx2] = '■'
                elif self.matrix[idx1][idx2] == Mark.A.value:
                    display_matrix[idx1][idx2] = 'A'
                elif self.matrix[idx1][idx2] == Mark.H.value:
                    display_matrix[idx1][idx2] = 'H'
                else:
                    display_matrix[idx1][idx2] = '□'

        df = pandas.DataFrame(display_matrix, columns=self.labels,
                              index=self.labels)

        return str(df) + "\n"
