import tkinter as tk
from datetime import datetime

BG_COLOR = "lightblue"


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Typing Speed Test')
        self.config(padx=30, pady=30, bg=BG_COLOR)

        self.mainloop()


app = GUI()
