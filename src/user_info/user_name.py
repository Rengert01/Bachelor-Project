# user_input.py
import tkinter as tk
from tkinter import messagebox

class UserInput:
    def __init__(self):
        self.user_name = None
        self.root = tk.Tk()
        self.root.title("User Input Form")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - 500) / 2)
        y_position = int((screen_height - 500) / 2)
        self.root.geometry(f"500x500+{x_position}+{y_position}")
        # self.root.attributes('-fullscreen', True)

        self.create_name_input()
        self.create_submit_button()
        self.root.mainloop()
        self.name_entry = None

    def get_user_name(self):
        return self.user_name

    def create_name_input(self):
        label = tk.Label(
            self.root,
            text="Enter Your Full Name:",
            font=("Helvetica", 16)
        )
        label.pack(pady=10)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.name_entry.pack(pady=10)

    def create_submit_button(self):
        submit_button = tk.Button(
            self.root,
            text="Submit",
            command=self.submit_name,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )

        submit_button.pack(pady=20)

    def submit_name(self):
        self.user_name = self.name_entry.get()
        if self.user_name:
            self.root.destroy()
        else:
            messagebox.showwarning("Warning",
                                   "Please enter your name.")
