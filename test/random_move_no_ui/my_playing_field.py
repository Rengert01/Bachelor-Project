from enum import Enum

import numpy as np
import pandas
import random


class State(Enum):
    PLAY = 1
    OVER = 2
    DRAW = 3


class MyPlayingField:
    def __init__(self, size):
        self.size = size
        self.matrix = np.zeros((self.size, self.size))
        self.labels = np.arange(1, self.size + 1)
        self.state = State.PLAY

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def get_matrix(self):
        return self.matrix

    def generate_display_matrix(self, players):
        display_matrix = np.full((self.size, self.size), "\0")
        for idx1 in range(self.size):
            for idx2 in range(self.size):
                if self.matrix[idx1][idx2] == 0:
                    display_matrix[idx1][idx2] = '□'
                else:
                    display_matrix[idx1][idx2] = '■'

        for player in players:
            if not player.get_start() or player.get_rounds_dead() > 1:
                continue
            cur_player_pos = player.get_position()
            display_matrix[cur_player_pos[0]][cur_player_pos[1]] = str(
                player.get_player_idx())

        df = pandas.DataFrame(display_matrix, columns=self.labels,
                              index=self.labels)

        return df

    def get_random_position(self):
        while True:
            rand_x = random.randint(0, self.size - 1)
            rand_y = random.randint(0, self.size - 1)
            if self.matrix[rand_x][rand_y] == 0:
                self.matrix[rand_x][rand_y] = 1
                return [rand_x, rand_y]

    def get_possible_moves(self, pos):
        possible_moves = []
        for value in range(1, 4):
            if pos[0] - value >= 0:
                tmp_x = pos[0] - value
                if self.matrix[tmp_x][pos[1]] == 0:
                    possible_moves.append([tmp_x, pos[1]])
            if pos[0] + value < self.size:
                tmp_x = pos[0] + value
                if self.matrix[tmp_x][pos[1]] == 0:
                    possible_moves.append([tmp_x, pos[1]])
            if pos[1] - value >= 0:
                tmp_y = pos[1] - value
                if self.matrix[pos[0]][tmp_y] == 0:
                    possible_moves.append([pos[0], tmp_y])
            if pos[1] + value < self.size:
                tmp_y = pos[1] + value
                if self.matrix[pos[0]][tmp_y] == 0:
                    possible_moves.append([pos[0], tmp_y])
        return possible_moves

    def move(self, pos):
        if self.matrix[pos[0]][pos[1]] == 0:
            self.matrix[pos[0]][pos[1]] = 1

    def is_spot_free(self, pos):
        if self.matrix[pos[0]][pos[1]] == 0:
            return True

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
