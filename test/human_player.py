import random
import numpy as np

class MyPlayer:
    def __init__(self, bot, name, player_idx):
        self.bot = bot
        self.name = name
        self.pos_x = 0
        self.pos_y = 0
        self.player_idx = player_idx
        self.start = False

    def set_position(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def get_position(self):
        return [self.pos_x, self.pos_y]

    def get_name(self):
        return self.name

    def is_bot(self):
        return self.bot

    def get_start(self):
        if self.start is True:
            return True
        else:
            self.start = True
            return False

    def get_player_idx(self):
        return self.player_idx


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

    def generate_display_matrix(self, players):
        display_matrix = np.full((self.size, self.size), "\0")
        for idx1 in range(self.size):
            for idx2 in range(self.size):
                if self.matrix[idx1][idx2] == 0:
                    display_matrix[idx1][idx2] = '□'
                else:
                    display_matrix[idx1][idx2] = '■'

        for player in players:
            cur_player_pos = player.get_position()
            display_matrix[cur_player_pos[0]][cur_player_pos[1]] = str(player.get_player_idx())

        return display_matrix

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

    def is_spot_free(self, pos):
        if self.matrix[pos[0]][pos[1]] == 0:
            return True


def create_players(bot_amount, player_amount):
    players = []
    player_idx = 1
    for idx in range(bot_amount):
        players.append(MyPlayer(True, "bot_" + str(idx), player_idx))
        player_idx += 1

    for idx in range(player_amount):
        players.append(MyPlayer(False, "player_" + str(idx), player_idx))
        player_idx += 1

    return players


def human_player_move(player, field):
    if player.get_start() is False:
        x_pos = int(input("Set Horizontal Position (1 - " + str(field.size) + "): "))
        y_pos = int(input("Set Vertical Position (1 - " + str(field.size) + "): "))
        move_pos = [x_pos - 1, y_pos - 1]
        if field.is_spot_free(move_pos):
            player.set_position(move_pos)
            field.move(move_pos)
            return move_pos
        print("Location Unavailable")

    while True:
        x_pos = int(input("Horizontal Change (1 - " + str(field.size) + "): "))
        y_pos = int(input("Vertical Change (1 - " + str(field.size) + "): "))
        move_pos = [x_pos - 1, y_pos - 1]
        possible_moves = field.get_possible_moves(player.get_position())
        if move_pos in possible_moves:
            player.set_position(move_pos)
            field.move(move_pos)
            return move_pos
        print("Invalid Movement / Location Unavailable")


def main():
    playing_field_size = 4
    bot_amount = 1
    player_amount = 1

    playing_field = MyPlayingField(playing_field_size)
    players = create_players(bot_amount, player_amount)

    # for player in players:
    #     if player.is_bot():
    #         tmp_pos = playing_field.get_random_position()
    #         player.set_position(tmp_pos)
    #         print("Starting position " + player.get_name() + ": " + str(
    #             player.get_position()))

    # Two bots have taken random position on the board.
    print("Starting positions:")
    print(playing_field.generate_display_matrix(players))

    cur_player_idx = 0
    while True:
        cur_player_pos = players[cur_player_idx].get_position()
        possible_moves = playing_field.get_possible_moves(cur_player_pos)
        if len(possible_moves) == 0:
            print("\n" + players[cur_player_idx].get_name() + " loses")
            break
        print("\n" + players[cur_player_idx].get_name() + "'s turn")

        if players[cur_player_idx].is_bot():
            if players[cur_player_idx].get_start():
                player_move = random.choice(possible_moves)
            else:
                player_move = playing_field.get_random_position()
        else:
            player_move = human_player_move(players[cur_player_idx],
                                            playing_field)

        print("Player moves towards: [" + str(player_move[0]+1) + "," + str(player_move[1]+1) + "]")
        playing_field.move(player_move)
        players[cur_player_idx].set_position(player_move)
        print("New field:")
        print(playing_field.generate_display_matrix(players))

        # Keep iterating until game ends.
        cur_player_idx = cur_player_idx + 1
        if cur_player_idx == len(players):
            cur_player_idx = 0

    print(playing_field.generate_display_matrix(players))


if __name__ == "__main__":
    main()
