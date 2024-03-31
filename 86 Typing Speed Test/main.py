import tkinter as tk
from datetime import datetime
from common_words import random_paragraph
import time

BG_COLOR = 'lightblue'
FONT = 'Courier'
TIMER_LENGTH = 3


class Timer:

    def time_stop(self):
        return  # Time


class GUI(tk.Tk, Timer):
    def __init__(self):
        super().__init__()
        # GUI
        self.title('Typing Speed Test')
        self.config(padx=30, pady=30, bg=BG_COLOR)
        self.heading = tk.Label(
            text='Typing Speed Test',
            font=(FONT, 40, 'bold'),
            bg=BG_COLOR,
            fg='white'
        ).pack()
        # Start message
        self.start_msg = tk.Text(
            wrap='word',
            font=(FONT),
            bg=BG_COLOR,
            fg='white',
            highlightbackground=BG_COLOR
        )
        self.start_msg.insert(
            tk.END,
            '''Welcome to the Speed Typing Test!\nThe goal is to type as many words correctly as you can in one minute.\nPress the spacebar to begin.'''
        )
        self.start_msg.tag_add("center", "1.0", "end")
        self.start_msg.tag_configure("center", justify='center')
        self.start_msg.config(state='disabled')
        # End message
        self.end_frame = tk.Frame(self)
        self.end_frame.config(bg=BG_COLOR)
        self.stats = tk.Label(
            self.end_frame,
            text='',
            font=(FONT),
            bg=BG_COLOR,
            fg='white'
        )
        self.stats.pack(pady=2)
        self.play_again = tk.Label(
            self.end_frame,
            text=f'Would you like to play again?',
            font=(FONT),
            bg=BG_COLOR,
            fg='white'
        )
        self.play_again.pack(pady=2)
        self.button = tk.Button(
            self.end_frame,
            text='Play again',
            font=(FONT),
            highlightbackground=BG_COLOR,
            command=self.reset
        )
        self.button.pack(pady=2)
        ##########
        self.cpm = 0
        self.show_start_msg()
        self.mainloop()

    def show_start_msg(self):
        self.start_msg.pack(pady=5)
        # Variables
        self.char_index = 0
        self.word_index = 0
        self.wordstart = 0
        self.bind('<space>', self.start_test)

    def start_test(self, event):
        self.start_msg.pack_forget()
        self.timer_display = tk.Label(
            text='60:00',
            font=(FONT),
            bg=BG_COLOR,
            fg='white'
        )
        self.timer_display.pack()
        self.test_text = random_paragraph(300).split()
        self.textbox = tk.Text(
            wrap='word',
            font=(FONT),
            height=25,
            bg='white',
            fg='black'
        )
        self.textbox.insert(tk.END, self.test_text)
        self.textbox.config(state='disabled')
        self.textbox.pack(pady=5)
        self.highlight_word()
        self.unbind('<space>')
        self.timer()

    def on_key(self, event):
        if event.keysym == 'BackSpace':
            if self.char_index != self.wordstart:
                self.char_index -= 1
                self.textbox.tag_delete(
                    'char' + str(self.char_index)
                )
        elif event.keysym == 'space' and self.char_index != 0:
            self.char_index = self.wordstart + \
                len(self.test_text[self.word_index]) + 1
            self.wordstart = self.char_index
            self.word_index += 1
            self.textbox.tag_delete(
                'word' + str(self.word_index - 1)
            )
            self.highlight_word()
        elif len(event.keysym) == 1:
            self.textbox.tag_add(
                'char' + str(self.char_index),
                f"1.{self.char_index}"
            )
            self.textbox.tag_configure(
                'char' + str(self.char_index), foreground='green' if event.keysym == self.textbox.get(f"1.{self.char_index}") else 'red'
            )
            self.char_index += 1

    def highlight_word(self):
        self.textbox.tag_add(
            'word' + str(self.word_index),
            f"1.{self.char_index}",
            f"1.{self.char_index + len(self.test_text[self.word_index])}",
        )
        self.textbox.tag_configure(
            'word' + str(self.word_index), background='yellow'
        )

    def timer(self):
        self.bind('<KeyRelease>', self.on_key)
        self.start_time = datetime.now().timestamp()
        while datetime.now().timestamp() < self.start_time + TIMER_LENGTH:
            self.update()
            time.sleep(.01)
            elapsed_time = '{:.2f}'.format(
                round(TIMER_LENGTH - (datetime.now().timestamp() - self.start_time), 2)).replace(".", ":")
            self.timer_display.config(text=elapsed_time)
            print(elapsed_time)
        self.timer_display.config(text='Times up!')
        self.unbind('<KeyRelease>')
        self.show_end_msg()

    def show_end_msg(self):
        self.textbox.pack_forget()
        self.calculate_score()
        self.stats.config(
            text=f'Your typing stats: {self.cpm} CPM, {self.cpm // 5} WPM'
        )
        self.end_frame.pack()

    def calculate_score(self):
        pass

    def reset(self):
        self.end_frame.pack_forget()
        self.show_start_msg()


app = GUI()
