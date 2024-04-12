import tkinter as tk


BG_COLOR = 'tomato'
FONT_COLOR = 'white'
FONT_NAME = 'Courier'
FONT_SIZE = 20
FONT = (FONT_NAME, FONT_SIZE)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Dangerous Writing App')
        self.config(padx=30, pady=30, bg=BG_COLOR)
        self.heading = tk.Label(
            text='Dangerous Typing App',
            font=(FONT_NAME, 40, 'bold'),
            bg=BG_COLOR,
            fg=FONT_COLOR
        ).pack()
        self.mainloop()


app = App()
