import tkinter as tk
from datetime import datetime
from common_words import random_paragraph

BG_COLOR = "lightblue"


class Timer:
    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        return  # Time


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Typing Speed Test')
        self.config(padx=30, pady=30, bg=BG_COLOR)

        self.heading = tk.Label(
            text='Typing Speed Test',
            font=('Georgia', 40, 'bold'),
            bg=BG_COLOR,
            fg='white'
        ).pack()
        self.load_test()
        self.type_spot = tk.Text(
            wrap='word',
            height=25
        )
        self.type_spot.pack(pady=5)
        self.bind('<KeyRelease>', self.on_key)
        self.mainloop()

    def load_test(self):
        text = random_paragraph(300)
        self.test = tk.Text(
            wrap='word',
            height=25
        )
        self.test.insert(tk.END, text)
        self.test.config(state='disabled')
        self.test.pack(pady=5)

    def on_key(self, event):
        key = event.keysym
        index = int(self.type_spot.index(tk.CURRENT).split(".")[1]) - 1
        if key == self.test.get(f"1.{index}"):
            self.test.tag_add(
                str(index),
                f"1.{index}",
                f"1.{index + 1}"
            )
            self.test.tag_configure(
                str(index), foreground='green'
            )


app = GUI()
