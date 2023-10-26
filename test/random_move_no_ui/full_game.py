import random
from my_player import MyPlayer
from my_playing_field import MyPlayingField


def create_players(bot_amount, player_amount):
    players = []
    player_idx = 0
    for idx in range(bot_amount):
        players.append(MyPlayer(True, "Bot_" + str(player_idx), player_idx))
        player_idx += 1

    for idx in range(player_amount):
        players.append(
            MyPlayer(False, "Player_" + str(player_idx), player_idx))
        player_idx += 1

    return players


def human_player_first_move(field):
    while True:
        x_pos = int(
            input(
                "Set Horizontal Position (1 - " + str(field.size) + "): "))
        y_pos = int(
            input("Set Vertical Position (1 - " + str(field.size) + "): "))
        move_pos = [x_pos - 1, y_pos - 1]
        if field.is_spot_free(move_pos):
            return move_pos
        print("Location Unavailable")


def human_player_move(player, field):
    while True:
        x_pos = int(
            input("Horizontal Change (1 - " + str(field.size) + "): "))
        y_pos = int(
            input("Vertical Change (1 - " + str(field.size) + "): "))
        move_pos = [y_pos - 1, x_pos - 1]
        possible_moves = field.get_possible_moves(player.get_position())
        if move_pos in possible_moves:
            return move_pos
        print("Invalid Movement / Location Unavailable")


def evaluate(players):
    tmp_players = []
    for idx in range(len(players)):
        if players[idx].get_rounds_dead() <= 1:
            tmp_players.append(players[idx])
    print("\n-----------------------------------")
    for player in tmp_players:
        if player.get_rounds_dead() == 0:
            print(player.get_name() + " Won!")
            return
    print("Draw Between ", end="")
    for idx in range(len(tmp_players) - 1):
        print(tmp_players[idx].get_name(), end=", ")
    print(tmp_players[-1].get_name() + "!")


def game():
    playing_field_size = int(input("Set Board Size:"))
    bot_amount = int(input("Amount Of Bots:"))
    player_amount = int(input("Amount Of Human Players:"))

    playing_field = MyPlayingField(playing_field_size)
    players = create_players(bot_amount, player_amount)

    print("\nGame Starts!")
    cur_player_idx = random.randint(0, len(players) - 1)
    last_to_move = players[cur_player_idx - 1].get_player_idx()
    flag = 0
    while True:
        if players[cur_player_idx].get_rounds_dead() > 0:
            players[cur_player_idx].update_rounds_dead()
        else:
            print("\n" + players[cur_player_idx].get_name() + "'s turn")
            cur_player_pos = players[cur_player_idx].get_position()
            possible_moves = playing_field.get_possible_moves(
                cur_player_pos)
            if len(possible_moves) == 0:
                players[cur_player_idx].update_rounds_dead()
                print(players[cur_player_idx].get_name() + " Out Of Moves")
                flag += 1
            else:
                if players[cur_player_idx].is_bot():
                    if players[cur_player_idx].get_start():
                        player_move = random.choice(possible_moves)
                    else:
                        player_move = playing_field.get_random_position()
                        players[cur_player_idx].set_start()
                else:
                    if players[cur_player_idx].get_start():
                        player_move = human_player_move(
                            players[cur_player_idx],
                            playing_field)
                    else:
                        player_move = human_player_first_move(
                            playing_field)
                        players[cur_player_idx].set_start()

                print("Player moves towards: [" + str(
                    player_move[0] + 1) + "," + str(
                    player_move[1] + 1) + "]")
                playing_field.move(player_move)
                players[cur_player_idx].set_position(player_move)
                print("New field:")
                print(playing_field.generate_display_matrix(players))

        if flag >= len(players) - 1 and cur_player_idx == last_to_move:
            break

        # Keep iterating until game ends.
        cur_player_idx = cur_player_idx + 1
        if cur_player_idx == len(players):
            cur_player_idx = 0

    evaluate(players)
    print(playing_field.generate_display_matrix(players))
    print("")
