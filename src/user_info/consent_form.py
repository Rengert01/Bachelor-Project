import tkinter as tk
from tkinter import messagebox


class UserConsent:
    def __init__(self):
        self.user_accepted = False
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.mainloop()

    def setup_window(self):
        self.root.title("User Consent Form")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - 700) / 2)
        y_position = int((screen_height - 500) / 2)
        self.root.geometry(f"700x500+{x_position}+{y_position}")
        # self.root.attributes('-fullscreen', True)

    def create_widgets(self):
        self.create_consent_message()
        self.create_accept_button()

    def create_consent_message(self):
        message = (
            'You are invited to participate in an experiment conducted by \n'
            'Rengert van Dolderen to investigate the performance of different\n'
            'artificial intelligence (AI) in a game called Rimboe Road\n'
            'Participation is voluntary, and you can withdraw at any time.\n'
            'Your data will be kept confidential.\n\n'
            # 'Initially the program will ask for your name, your name\n'
            # 'will only be used to find your match history in case an issue is\n'
            # 'encountered during the experiment\n\n'
            'By continuing, you acknowledge and agree to participate\n'
            'voluntarily.'
        )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_accept_button(self):
        accept_button = tk.Button(
            self.root,
            text="Accept",
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
        self.user_accepted = True
        self.root.destroy()

    def get_user_accepted(self):
        return self.user_accepted
