# ---------------------------- IMPORTS ---------------------------- #
from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
import time

# ---------------------------- CONSTANTS & GLOBALS ---------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
word = {}

# ---------------------------- FUNCTIONS ---------------------------- #


def display(word, language):
    card_canvas.itemconfig(language_display, text=language,
                           fill='white' if language == 'English' else 'black')
    card_canvas.itemconfig(word_display, text=word,
                           fill='white' if language == 'English' else 'black')
    card_canvas.itemconfig(
        card_display, image=card_back if language == 'English' else card_front)


def next_word():
    global word
    word = random.choice(to_learn)
    french_word = word['French']
    english_word = word['English']

    display(french_word, 'French')
    window.update()
    window.after(3000, display(english_word, 'English'))


def on_wrong():
    next_word()


def on_right():
    global word
    to_learn.remove(word)
    pd.DataFrame(to_learn).to_csv('./data/words_to_learn.csv', index=False)
    next_word()


# ---------------------------- DATA ---------------------------- #
try:
    data = pd.read_csv('./data/words_to_learn.csv')
except FileNotFoundError as error:
    data = pd.read_csv('./data/french_words.csv')
finally:
    to_learn = data.to_dict(orient='records')
    # ---------------------------- UI ---------------------------- #
    window = Tk()
    window.title("Flashy")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    card_front = PhotoImage(file='./images/card_front.png')
    card_back = PhotoImage(file='./images/card_back.png')
    wrong_image = PhotoImage(file='./images/wrong.png')
    right_image = PhotoImage(file='./images/right.png')

    card_canvas = Canvas(width=800, height=526)
    card_canvas.config(highlightbackground=BACKGROUND_COLOR,
                       bg=BACKGROUND_COLOR)
    card_display = card_canvas.create_image(400, 263, image=card_front)
    language_display = card_canvas.create_text(400, 150, text="",
                                               font=('Ariel', 40, 'italic'))
    word_display = card_canvas.create_text(400, 263, text="",
                                           font=('Ariel', 60, 'bold'))
    card_canvas.grid(row=0, column=0, columnspan=2)

    wrong_button = Button(image=wrong_image, command=on_wrong)
    wrong_button.config(
        highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR)
    wrong_button.grid(row=1, column=0)

    right_button = Button(image=right_image, command=on_right)
    right_button.config(
        highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR)
    right_button.grid(row=1, column=1)

    next_word()

    window.mainloop()
