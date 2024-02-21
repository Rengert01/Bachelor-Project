import tkinter as tk


class EndOfPractise:
    def __init__(self):
        self.experiment_start = False
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
        self.create_buttons()

    def create_consent_message(self):
        message = (
            'That was the end of the practise round!\n'
            'If you do not yet have clear understanding of the game, feel free\n'
            'to play another practise round and/or ask any questions.'
        )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_buttons(self):
        start_button = tk.Button(
            self.root,
            text="Start Experiment",
            command=lambda: self.start_experiment(True),
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        start_button.pack(pady=20)

        redo_button = tk.Button(
            self.root,
            text="Practise",
            command=lambda: self.start_experiment(False),
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        redo_button.pack(pady=20)

    def start_experiment(self, flag):
        self.experiment_start = flag
        self.root.destroy()

    def get_experiment_start(self):
        return self.experiment_start
