import random
import numpy as np


class MyPlayer:
    def __init__(self, bot, name):
        self.bot = 0
        self.name = name
        self.pos_x = 0
        self.pos_y = 0

    def set_position(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def get_position(self):
        return [self.pos_x, self.pos_y]

    def get_name(self):
        return self.name


class MyPlayingField:
    def __init__(self, size):
        self.size = size
        self.matrix = np.zeros((self.size, self.size))

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def get_matrix(self):
        return self.matrix

    def get_random_position(self):
        while (1):
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


def main():
    playing_field_size = 4
    bot_amount = 2

    playing_field = MyPlayingField(playing_field_size)
    players = []
    for idx in range(bot_amount):
        players.append(MyPlayer(1, "bot_" + str(idx)))

    for player in players:
        tmp_pos = playing_field.get_random_position()
        player.set_position(tmp_pos)
        print("Starting position " + player.get_name() + ": " + str(
            player.get_position()))

    # Two bots have taken random position on the board.
    print("Starting positions:")
    print(playing_field.get_matrix())

    cur_player_idx = 0
    while True:
        cur_player_pos = players[cur_player_idx].get_position()
        possible_moves = playing_field.get_possible_moves(cur_player_pos)
        if len(possible_moves) == 0:
            print("\n" + players[cur_player_idx].get_name() + " loses")
            break
        print("\n" + players[cur_player_idx].get_name() + "'s turn")

        # Random move:
        player_move = random.choice(possible_moves)
        print("Player moves towards: " + str(player_move))
        playing_field.move(player_move)
        players[cur_player_idx].set_position(player_move)
        print("New field:")
        print(playing_field.matrix)

        # Keep iterating until game ends.
        cur_player_idx = cur_player_idx + 1
        if cur_player_idx == len(players):
            cur_player_idx = 0

    print(playing_field.get_matrix())


if __name__ == "__main__":
    main()
