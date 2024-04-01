import tkinter as tk
from datetime import datetime
from common_words import random_paragraph
import time

BG_COLOR = 'lightblue'
HIGHLIGHT_COLOR = 'yellow'
CORRECT_COLOR = 'green'
ERROR_COLOR = 'red'
FONT_COLOR = 'white'
FONT = ('Courier', 20, 'bold')
TIMER_LENGTH = 60


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # GUI
        self.title('Typing Speed Test')
        self.config(padx=30, pady=30, bg=BG_COLOR)
        self.heading = tk.Label(
            text='Typing Speed Test',
            font=('Courier', 40, 'bold'),
            bg=BG_COLOR,
            fg=FONT_COLOR
        ).pack()
        # Start message
        self.start_msg = tk.Text(
            wrap='word',
            font=FONT,
            bg=BG_COLOR,
            fg=FONT_COLOR,
            highlightbackground=BG_COLOR,
            height=3
        )
        self.start_msg.insert(
            tk.END,
            f"Welcome to the Speed Typing Test!\n"
            f"The goal is to type as many words correctly "
            f"as you can in {TIMER_LENGTH} seconds.\n"
            f"Press the spacebar to begin."
        )
        self.start_msg.tag_add('center', '1.0', 'end')
        self.start_msg.tag_configure('center', justify='center')
        self.start_msg.config(state='disabled')
        # End message
        self.end_frame = tk.Frame(self)
        self.end_frame.config(bg=BG_COLOR)
        self.stats = tk.Label(
            self.end_frame,
            text='',
            font=FONT,
            bg=BG_COLOR,
            fg=FONT_COLOR
        )
        self.stats.pack(pady=2)
        self.play_again = tk.Label(
            self.end_frame,
            text=f"Would you like to play again?",
            font=FONT,
            bg=BG_COLOR,
            fg=FONT_COLOR
        )
        self.play_again.pack(pady=2)
        self.button = tk.Button(
            self.end_frame,
            text="Play again",
            font=FONT,
            highlightbackground=BG_COLOR,
            command=self.reset
        )
        self.button.pack(pady=2)
        # Begin
        self.show_start_msg()
        self.mainloop()

    def show_start_msg(self):
        self.start_msg.pack(pady=5)
        # Variables
        self.char_index = 0
        self.word_index = 0
        self.word_start = 0
        self.typed_char = 0
        self.errors = 0
        self.bind('<space>', self.start_test)

    def start_test(self, event):
        self.start_msg.pack_forget()
        self.timer_display = tk.Label(
            text='60:00',
            font=FONT,
            bg=BG_COLOR,
            fg=FONT_COLOR
        )
        self.timer_display.pack()
        self.test_text = random_paragraph(150).split()
        self.textbox = tk.Text(
            wrap='word',
            font=FONT,
            height=12,
            bg='white',
            fg='black'
        )
        self.textbox.insert(tk.END, self.test_text)
        self.textbox.config(state='disabled')
        self.textbox.pack(pady=5)
        self.set_styling()
        self.highlight_word()
        self.current_word = ''
        self.unbind('<space>')
        self.timer()

    def on_key(self, event):
        if event.keysym == 'BackSpace':
            self.on_backspace()
        elif event.keysym == 'space' and self.char_index != 0:
            self.on_space()
        elif len(event.keysym) == 1:
            self.on_letter(event.keysym)

    def on_backspace(self):
        if self.char_index != self.word_start:
            self.char_index -= 1
            self.typed_char -= 1
            self.current_word = self.current_word[:-1]
            deleting = self.textbox.tag_names(f'1.{self.char_index}')[1]
            if deleting == 'error':
                self.errors -= 1
            self.textbox.tag_remove(
                deleting,
                f'1.{self.char_index}'
            )

    def on_space(self):
        if self.char_index < self.word_end:
            self.textbox.tag_add(
                'error',
                f'1.{self.char_index}',
                f'1.{self.word_end}'
            )
            self.errors += 1
        self.textbox.tag_remove(
            'highlight', f'1.{self.word_start}', f'1.{
                self.word_end}'
        )
        self.current_word = ''
        self.char_index = self.word_end + 1
        self.word_start = self.char_index
        self.word_index += 1
        self.typed_char += 1
        self.highlight_word()

    def on_letter(self, letter):
        if self.char_index == self.word_end:
            self.on_backspace()
        self.current_word += letter
        if letter == self.textbox.get(f'1.{self.char_index}'):
            tag = 'correct'
        else:
            tag = 'error'
            self.errors += 1
        self.textbox.tag_add(
            tag,
            f'1.{self.char_index}'
        )
        self.char_index += 1
        self.typed_char += 1

    def highlight_word(self):
        self.textbox.tag_add(
            'highlight',
            f'1.{self.word_start}',
            f'1.{self.word_end}',
        )

    def set_styling(self):
        self.textbox.tag_configure(
            'highlight', background=HIGHLIGHT_COLOR
        )
        self.textbox.tag_configure(
            'correct', foreground=CORRECT_COLOR
        )
        self.textbox.tag_configure(
            'error', foreground=ERROR_COLOR
        )

    def timer(self):
        self.bind('<KeyRelease>', self.on_key)
        self.start_time = datetime.now().timestamp()
        while datetime.now().timestamp() < self.start_time + TIMER_LENGTH:
            self.update()
            time.sleep(.01)
            elapsed_time = '{:.2f}'.format(round(
                TIMER_LENGTH - (datetime.now().timestamp() - self.start_time), 2)).replace(".", ":")
            self.timer_display.config(text=elapsed_time)
        self.timer_display.config(text="Time's up!")
        self.unbind('<KeyRelease>')
        self.show_end_msg()

    def show_end_msg(self):
        self.textbox.pack_forget()
        self.cpm = int(self.typed_char // (TIMER_LENGTH / 60)) + 1
        self.wpm = int(((self.typed_char / 5) - self.errors) //
                       (TIMER_LENGTH / 60)) + 1
        self.stats.config(
            text=f"Your typing stats: "
            f"{self.cpm} CPM, "
            f"{self.errors} ERR, "
            f"{self.wpm} WPM"
        )
        self.end_frame.pack()

    def reset(self):
        self.end_frame.pack_forget()
        self.timer_display.pack_forget()
        self.show_start_msg()

    @property
    def word_end(self):
        return self.word_start + len(self.test_text[self.word_index])


app = GUI()
