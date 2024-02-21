import tkinter as tk


class GameExplanation:
    def __init__(self):
        self.user_accepted = False
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.mainloop()

    def setup_window(self):
        self.root.title("Game Explanation")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - 700) / 2)
        y_position = int((screen_height - 600) / 2)
        self.root.geometry(f"700x600+{x_position}+{y_position}")
        # self.root.attributes('-fullscreen', True)

    def create_widgets(self):
        self.create_consent_message()
        self.create_accept_button()

    def create_consent_message(self):
        message = ('Welcome to Rimboe Road, a strategic thinking game.\n\n'
                   'Here is how the game works:\n'
                   'You start off with a grid of squares. Choose your starting\n'
                   'position by clicking on one of them. From your current \n'
                   'position you are allowed to move 1-3 squares up, down, left \n'
                   'and right. After a player has left their position, this \n'
                   'square becomes unavailable for the rest of the game.\n'
                   'You can still jump over unavailable squares!\n\n'
                   ''
                   'The first player unable to move anywhere loses.\n\n'
                   ''
                   'Pay Attention: The turn ends when both players have made \n'
                   'their move. This means that if the starting player gets \n'
                   'stuck, the other player still has to make a move.\n\n'
                   ''
                   'You will first be able to practise and when you are ready \n'
                   'you will play against three AI players. You will play each\n'
                   'player twice and afterwards you will be asked to rank the \n'
                   'skill level of each player from 1-10.'
                   )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_accept_button(self):
        accept_button = tk.Button(
            self.root,
            text="Next",
            command=self.accept_consent,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        accept_button.pack(pady=20)

    def accept_consent(self):
        self.root.destroy()
