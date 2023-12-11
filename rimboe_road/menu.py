# menu.py
import tkinter as tk
from tkinter import *
from rimboe_road.gamegui import GameGUI


class MainMenu:
    def __init__(self, text, depth, name):
        self.ai_player_name = name
        self.report = None
        self.root = tk.Tk()
        self.root.title("Rimboe Road Menu")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - 500) / 2)
        y_position = int((screen_height - 500) / 2)
        self.root.geometry(f"500x500+{x_position}+{y_position}")
        # self.root.attributes('-fullscreen', True)
        self.create_start_button(text, depth)
        self.root.mainloop()

    def get_report(self):
        return self.report

    def create_start_button(self, text, depth):
        start_button = tk.Button(
            self.root,
            text=text,
            command=lambda: self.start_game(depth),
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )

        start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def start_game(self, depth):
        turn = [0, 1]
        try:
            self.root.destroy()
            board_size = 6

            game_gui_player1 = GameGUI(board_size, depth, self.ai_player_name,
                                       turn[0])
            self.report = "Match against: " + str(self.ai_player_name) + "\n"
            self.report += str(game_gui_player1.get_game_report())

            game_gui_player2 = GameGUI(board_size, depth, self.ai_player_name,
                                       turn[1])
            self.report += "Match against: " + str(
                self.ai_player_name) + "\n"
            self.report += str(game_gui_player2.get_game_report())
        except Exception as e:
            print(f"An error occurred: {e}")

