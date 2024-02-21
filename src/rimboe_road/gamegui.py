# gamegui.py

import tkinter as tk
from tkinter import messagebox
from rimboe_road.board import Board, State, Mark
import math
import copy


class GameGUI:
    def __init__(self, size, depth, opp_name, turn):
        self.root = tk.Tk()
        self.root.title("Rimboe Road")
        self.board_size = size
        self.rimboe_board = Board(size, turn)
        self.depth = depth
        self.game_report = ""
        self.opp_name = opp_name
        self.turn = turn

        value = 125 * size

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - value) / 2)
        y_position = int((screen_height - value) / 2)

        self.root.geometry(f"{value}x{value}+{x_position}+{y_position}")

        for i in range(self.board_size + 2):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(self.board_size):
            self.root.grid_columnconfigure(j, weight=1)

        self.label = tk.Label(
            self.root,
            font=("Helvetica", 16)
        )
        self.label.grid(
            row=1,
            column=0,
            columnspan=self.board_size,
            sticky="n"
        )

        self.create_board_buttons()

        if self.rimboe_board.get_turn_to_play() == Mark.A:
            self.ai_move()
            self.update_board_buttons([])

        self.update_board_buttons([])
        self.root.mainloop()

    def get_game_report(self):
        return self.game_report

    def create_board_buttons(self):
        button_size = 10  # Adjust the button size

        for i in range(self.board_size):
            for j in range(self.board_size):
                button_colour = self.get_button_colour(i, j)
                button = tk.Button(
                    self.root,
                    fg=button_colour,
                    bg=button_colour,
                    activebackground=button_colour,
                    activeforeground=button_colour,
                    width=button_size,
                    height=button_size // 2,
                    command=lambda x=i, y=j: self.on_button_click(x, y)
                )
                # Adjust row and column offsets
                button.grid(
                    row=i + 2,
                    column=j,
                    sticky="nsew"
                )

    def on_button_click(self, i, j):
        flag = False
        if self.rimboe_board.get_turn_to_play() == Mark.H:
            pos = self.rimboe_board.get_pos()
            move = (i, j)

            if pos is None and self.rimboe_board.is_free(move):
                flag = True
            elif move in self.rimboe_board.get_possible_moves(pos):
                flag = True

            if flag is True:
                self.rimboe_board.make_move(move)
                self.update_board_buttons([])

                self.ai_move()
                self.update_board_buttons(
                    self.rimboe_board.get_possible_moves(move))

    def ai_move(self):
        if self.rimboe_board.get_state() == State.ONGOING:
            pos = self.rimboe_board.get_pos()
            if pos is None:
                best_move = self.rimboe_board.get_random_pos()
            else:
                board = copy.deepcopy(self.rimboe_board)
                board.set_real_game(False)
                best_score = -math.inf
                best_move = None
                alpha = -math.inf
                beta = math.inf
                for move in board.get_possible_moves(pos):
                    board.make_move(move)
                    score = self.minimax(False, Mark.A.value, board, self.depth,
                                         alpha, beta)
                    board.undo()
                    if score > best_score:
                        best_score = score
                        best_move = move
                    alpha = max(alpha, best_score)
            self.rimboe_board.make_move(best_move)

    def minimax(self, is_max_turn, maximizer_mark, board, depth, alpha, beta):
        state = board.get_state()
        if state is State.DRAW:
            return 0
        elif state is State.OVER:
            return 1 if board.get_winner() is maximizer_mark else -1
        elif depth == 1:
            return board.get_heuristic_value()
        elif depth == 0:
            return 0

        if is_max_turn:
            max_score = -math.inf
            for move in board.get_possible_moves(board.get_pos()):
                board.make_move(move)
                score = self.minimax(False, maximizer_mark, board, depth - 1,
                                     alpha, beta)
                board.undo()
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = math.inf
            for move in board.get_possible_moves(board.get_pos()):
                board.make_move(move)
                score = self.minimax(True, maximizer_mark, board, depth - 1,
                                     alpha, beta)
                board.undo()
                min_score = min(min_score, score)
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score

    def update_board_buttons(self, possible_moves):
        for i in range(self.board_size):
            for j in range(self.board_size):
                button_text = self.get_button_colour(i, j)
                button = self.get_button(i, j)
                if (i, j) in possible_moves and button_text == "white":
                    button_text = "light blue"
                # else:
                #     button.config(borderwidth=1,
                #                   highlightbackground="white")
                button.config(bg=button_text, fg=button_text,
                              activebackground=button_text,
                              activeforeground=button_text)

        if self.rimboe_board.get_state() != State.ONGOING:
            self.show_winner_popup()

        self.update_label_text()

    def update_label_text(self):
        tmp = f"Opponent: {self.opp_name}\n"
        if self.turn == 0:
            tmp += "First move: You"
        else:
            tmp += f"First move: {self.opp_name}"
        self.label.config(text=tmp)

    def show_winner_popup(self):
        winner = self.rimboe_board.get_winner()
        if winner == Mark.H.value:
            result = "Human won!"
        elif winner == Mark.A.value:
            result = "AI won!"
        else:
            result = "Draw!"

        messagebox.showinfo("Game Over", result)

        self.game_report += str(self.rimboe_board.get_board_report())
        self.game_report += "Result: " + str(result) + "\n\n"
        self.root.destroy()

    def get_button_colour(self, i, j):
        value = self.rimboe_board.matrix[i][j]
        if value == Mark.FULL.value:
            return "black"
        elif value == Mark.A.value:
            return "red"
        elif value == Mark.H.value:
            return "blue"
        else:
            return "white"

    def get_button(self, i, j):
        for child in self.root.winfo_children():
            if (
                    isinstance(child, tk.Button)
                    and child.grid_info().get("row") == i + 2
                    and child.grid_info().get("column") == j
            ):
                return child
