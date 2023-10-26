from enum import Enum
import random
import numpy as np
import pandas


class Mark(Enum):
    B = 1
    A = 2
    FULL = 3
    EMPTY = 4


class State(Enum):
    DRAW = 1
    ONGOING = 2
    OVER = 3


class Board:
    def __init__(self, size):
        self.size = size
        self.labels = np.arange(1, self.size + 1)
        self.matrix = [[Mark.EMPTY.value for x in range(size)] for y in
                       range(size)]
        # Randomly choose starting player
        tmp = [Mark.B, Mark.A]
        random.shuffle(tmp)
        self.turnToPlay = tmp[0]
        self.lastToPlay = tmp[-1]
        self.state = State.ONGOING
        self.winner = None
        self.moves = []
        self.real_game = True

    def get_turn_to_play(self):
        return self.turnToPlay

    def get_state(self):
        return self.state

    def get_winner(self):
        return self.winner

    def get_board(self):
        return self.matrix

    def get_size(self):
        return self.size

    def set_real_game(self, value):
        self.real_game = value

    def get_real_game(self):
        return self.real_game

    def get_possible_moves(self, pos):
        # Iterate over possible places to move towards and check if available
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
        return possible_moves

    def make_move(self, new_pos):
        old_pos = None
        # Check if this is a player's first move
        if len(self.moves) > 1:
            old_pos = self.moves[-2]
        if self.matrix[new_pos[0]][new_pos[1]] == Mark.EMPTY.value:
            if old_pos is not None:
                self.matrix[old_pos[0]][old_pos[1]] = Mark.FULL.value
            self.matrix[new_pos[0]][new_pos[1]] = self.turnToPlay.value
            self.__update_board_state()
            self.__switch_players()
            self.moves.append(new_pos)
            return 1
        else:
            print("Move not possible")
            return 0

    def undo(self):
        old_pos = self.moves[-3]
        last_move = self.moves.pop()
        if last_move:
            self.matrix[last_move[0]][last_move[1]] = Mark.EMPTY.value
            self.__switch_players()
            self.matrix[old_pos[0]][old_pos[1]] = self.turnToPlay.value

    def __update_board_state(self):
        self.winner = None
        self.state = self.evaluate_board_state()

    def __switch_players(self):
        self.turnToPlay = Mark.B if self.turnToPlay is Mark.A else Mark.A

    def print_board(self):
        display_matrix = np.full((self.size, self.size), "\0")
        for idx1 in range(self.size):
            for idx2 in range(self.size):
                if self.matrix[idx1][idx2] == Mark.FULL.value:
                    display_matrix[idx1][idx2] = '■'
                elif self.matrix[idx1][idx2] == Mark.A.value:
                    display_matrix[idx1][idx2] = 'A'
                elif self.matrix[idx1][idx2] == Mark.B.value:
                    display_matrix[idx1][idx2] = 'B'
                else:
                    display_matrix[idx1][idx2] = '□'

        df = pandas.DataFrame(display_matrix, columns=self.labels,
                              index=self.labels)

        print(df)
        print("")

    def print_result(self, m_move_amount, b_move_amount, statement):
        print("\nM move amount: " + str(m_move_amount))
        print("B move amount: " + str(b_move_amount))
        print("Turn to play: " + str(self.get_turn_to_play()))
        print("Last to play: " + str(self.lastToPlay))
        print(statement)
        self.print_board()

    def evaluate_board_state(self):
        m_pos = None
        b_pos = None
        for x in range(self.size):
            for y in range(self.size):
                state = Mark(self.matrix[x][y])
                if state is Mark.A:
                    m_pos = (x, y)
                if state is Mark.B:
                    b_pos = (x, y)

        if m_pos is None or b_pos is None:
            return State.ONGOING

        m_move_amount = len(self.get_possible_moves(m_pos))
        b_move_amount = len(self.get_possible_moves(b_pos))

        # if self.get_turn_to_play().value == self.lastToPlay.value:
        if m_move_amount == 0 and b_move_amount > 0:
            self.winner = Mark.B.value
            if self.get_real_game() is True:
                self.print_result(m_move_amount, b_move_amount, "Bot won!")
            return State.OVER

        if b_move_amount == 0 and m_move_amount > 0:
            self.winner = Mark.A.value
            if self.get_real_game() is True:
                self.print_result(m_move_amount, b_move_amount, "AI won!")
            return State.OVER

        if b_move_amount == 0 and m_move_amount == 0:
            if self.get_real_game() is True:
                self.print_result(m_move_amount, b_move_amount, "Draw!")
            return State.DRAW

        return State.ONGOING

    def get_pos(self):
        if len(self.moves) > 1:
            return self.moves[-2]
        else:
            return None

    def get_random_pos(self):
        pos = None
        while pos is None:
            x = random.randint(0, self.get_size() - 1)
            y = random.randint(0, self.get_size() - 1)
            if self.matrix[x][y] == Mark.EMPTY.value:
                pos = (x, y)
        return pos
