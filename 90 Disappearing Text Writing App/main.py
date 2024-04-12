import tkinter as tk
import time
import random


BG_COLOR = 'tomato'
FONT_COLOR = 'white'
FONT_NAME = 'Courier'
FONT_SIZE = 20
FONT = (FONT_NAME, FONT_SIZE)
MAX_IDLE_SECONDS = 5
SESSION_MINUTES = 4.5
SESSION_TIME = SESSION_MINUTES * 60
START_MESSAGE = 'You have five minutes to write as much as you can. But, be careful! If you stop writing for 5 seconds, all your work will get deleted! After the five minutes are up, your work will no longer be in jeopardy. Press any key to begin.'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Dangerous Writing App')
        self.config(padx=30, pady=30, bg=BG_COLOR)
        # Heading
        self.heading = tk.Label(
            text='Write Dangerously',
            font=(FONT_NAME, 40, 'bold'),
            bg=BG_COLOR,
            fg=FONT_COLOR,
        ).pack()
        # Timer
        self.session_timer_display = tk.Label()
        self.session_timer_display.config(
            font=FONT,
            fg=FONT_COLOR,
            bg=BG_COLOR,
            pady=20
        )
        self.session_timer_display.pack()
        # Text Area
        self.text_area = tk.Text()
        self.text_area.config(padx=10, pady=10, wrap='word')
        self.text_area.insert(
            '1.0', START_MESSAGE)
        self.text_area.pack()
        # Reset button
        self.reset_button = tk.Button(text='Reset timer')
        self.reset_button.config(
            command=self.reset_timers,
            highlightbackground=BG_COLOR,
            highlightcolor=BG_COLOR,
            highlightthickness=0,
        )
        self.reset_button.pack()
        # Finish init
        self.reset_timers()
        self.mainloop()

    def reset_timers(self):
        self.bind('<KeyPress>', self.start_timers)
        self.idle_timer = MAX_IDLE_SECONDS
        self.session_timer = SESSION_TIME
        self.session_timer_display.config(
            text=f'{int(SESSION_TIME // 60)}:{'0' if SESSION_TIME %
                                              60 < 10 else ''}{int(SESSION_TIME % 60)}'
        )
        self.reset_button.pack_forget()

    def start_timers(self, event):
        self.unbind('<KeyPress>')
        self.text_area.focus_set()
        if self.text_area.get(1.0, 'end').strip() == START_MESSAGE or self.text_area.get(1.0, 'end').strip()[:-1] == START_MESSAGE:
            self.clear_text()
            self.text_area.insert('1.0', event.char)
        self.pass_second()

    def pass_second(self):
        if self.session_timer > 0:
            self.set_timer_display()
            self.session_timer -= 1
            if self.idle_timer > 0:
                self.idle_timer -= 1
                self.bind('<KeyPress>', self.reset_idle_timer)
                self.recolor()
                self.update()
            else:
                self.clear_text()
            self.after(1000, self.pass_second)
        else:
            self.times_up()

    def reset_idle_timer(self, event):
        if len(event.keysym) == 1:
            self.idle_timer = MAX_IDLE_SECONDS + 1
            self.text_area.config(fg='black')
            self.update()

    def times_up(self):
        self.session_timer_display.config(text='0:00')
        self.text_area.config(fg='black')
        self.reset_button.pack()
        self.update()

    def clear_text(self):
        self.text_area.delete('1.0', tk.END)

    def recolor(self):
        if self.idle_timer == 0:
            self.text_area.config(fg='red')
        elif self.idle_timer == 1:
            self.text_area.config(fg='darkorange')
        elif self.idle_timer == 2:
            self.text_area.config(fg='gold')

    def set_timer_display(self):
        if self.session_timer != 0:
            self.session_timer_display.config(
                text=f'{int(self.session_timer // 60)}:{'0' if self.session_timer %
                                                        60 < 10 else ''}{int(self.session_timer % 60)}'
            )


app = App()
