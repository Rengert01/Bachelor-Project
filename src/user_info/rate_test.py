# test_rating.py
import tkinter as tk
from tkinter import messagebox


class TestRating:
    def __init__(self, opp_name):
        self.test_rating = None
        self.opp_name = opp_name
        self.root = tk.Tk()
        self.root.title("Player Rating Form")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - 500) / 2)
        y_position = int((screen_height - 500) / 2)
        self.root.geometry(f"500x500+{x_position}+{y_position}")
        # self.root.attributes('-fullscreen', True)

        self.create_rating_input()
        self.create_submit_button()
        self.root.mainloop()
        self.rating_entry = None
        self.root.mainloop()

    def get_test_rating(self):
        return self.test_rating

    def create_rating_input(self):
        label = tk.Label(
            self.root,
            text=f"Rate the Difficulty playing against {self.opp_name} (1-10):",
            font=("Helvetica", 16)
        )
        label.pack(pady=10)

        self.rating_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.rating_entry.pack(pady=10)

    def create_submit_button(self):
        submit_button = tk.Button(
            self.root,
            text="Submit",
            command=self.submit_rating,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )

        submit_button.pack(pady=20)

    def submit_rating(self):
        rating_text = self.rating_entry.get()
        try:
            self.test_rating = int(rating_text)
            if 1 <= self.test_rating <= 10:
                self.root.destroy()
            else:
                messagebox.showwarning("Warning",
                                       "Please enter a rating between 1 and 10.")
        except ValueError:
            messagebox.showwarning("Warning",
                                   "Please enter a valid numerical rating.")
