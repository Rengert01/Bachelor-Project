from board import Board, State, Mark
import math
import random
import copy


class Game:
    def __init__(self, size):
        self.rimboe_board = Board(size)
        self.botPlayer = Mark.B
        self.aiPlayer = Mark.A

    def play(self):
        # Keep iterating while game is in play
        while self.rimboe_board.get_state() is State.ONGOING:
            pos = self.rimboe_board.get_pos()
            # Take position on the board if player does not have one already
            if pos is None:
                self.rimboe_board.make_move(self.rimboe_board.get_random_pos())
            elif self.rimboe_board.get_turn_to_play() is self.aiPlayer:
                # Make deep copy of board to prevent printing
                board = copy.deepcopy(self.rimboe_board)
                board.set_real_game(False)
                best_score = -math.inf
                best_move = None
                for move in board.get_possible_moves(pos):
                    board.make_move(move)
                    score = self.minimax(False, self.aiPlayer.value,
                                         board)
                    board.undo()
                    if score > best_score:
                        best_score = score
                        best_move = move
                self.rimboe_board.make_move(best_move)
            else:
                # Bot makes random move
                moves = self.rimboe_board.get_possible_moves(pos)
                self.rimboe_board.make_move(random.choice(moves))
        return self.rimboe_board.get_winner()

    def minimax(self, is_max_turn, maximizer_mark, board):
        state = board.get_state()
        if state is State.DRAW:
            return 0
        elif state is State.OVER:
            return 1 if board.get_winner() is maximizer_mark else -1

        scores = []
        for move in board.get_possible_moves(board.get_pos()):
            board.make_move(move)
            scores.append(self.minimax(not is_max_turn, maximizer_mark, board))
            board.undo()
            if (is_max_turn and max(scores) == 1) or (
                    not is_max_turn and min(scores) == -1):
                break
        # print(scores)
        return max(scores) if is_max_turn else min(scores)


if __name__ == "__main__":
    bot_wins = 0
    ai_wins = 0
    for epoch in range(100):
        print("---------------- Epoch #" + str(epoch) + " ----------------")
        game = Game(4)
        winner = game.play()
        if winner == 1:
            bot_wins += 1
        if winner == 2:
            ai_wins += 1

    print("Bot wins: " + str(bot_wins))
    print("AI wins: " + str(ai_wins))
