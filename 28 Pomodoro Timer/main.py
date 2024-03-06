from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(timer)
    global reps
    reps = 0
    title.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_display, text="00:00")


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1
    if reps % 8 == 0:
        title.config(text="Break", fg=RED)
        countdown(LONG_BREAK_MIN * 60)
    elif reps % 2 == 0:
        title.config(text="Break", fg=PINK)
        countdown(SHORT_BREAK_MIN * 60)
    else:
        title.config(text="Work", fg=GREEN)
        countdown(WORK_MIN * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(count):
    min = math.floor(count / 60)
    sec = count % 60
    if sec < 10:
        sec = f"0{sec}"
    canvas.itemconfig(timer_display, text=f"{min}:{sec}")
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count-1)
    else:
        global reps
        checks = ""
        for _ in range(math.ceil((reps % 8) / 2)):
            checks += "✓ "
        check_label.config(text=checks)
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=50, bg=YELLOW)

title = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50), pady=20)
title.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato)
timer_display = canvas.create_text(100, 132, text="00:00", fill='white',
                                   font=(FONT_NAME, 24, 'bold'))
canvas.grid(column=1, row=1)


check_label = Label(bg=YELLOW, fg=GREEN)
check_label.grid(column=1, row=3)

start_button = Button(text="Start", bg=YELLOW,
                      highlightbackground=YELLOW, command=start_timer)
start_button.grid(column=0, row=2)


reset_button = Button(text="Reset", bg=YELLOW,
                      highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=2)

window.mainloop()
