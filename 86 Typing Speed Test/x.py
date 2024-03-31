import time
from tkinter import *
import random
from tkinter import messagebox
from common_words import random_words

words_list = []
typed_words = []
curr_word = ''
word = ''
char = 0
chars_typed = 0
accurate_typed = 0
position = 0

window = Tk()
window.geometry("300x150")
heading_label = Label(text="Typing Speed Test",
                      font=("Helvetica", 20), pady=15)
heading_label.pack()

rules_label = Label(text="Type the words that appear as fast and as accurately as you can in the box below, with one space between each word.  You can backspace and fix an error with no penalty.",  font=(
    "Helvetica", 12), pady=15, wraplength=500)
rules_label.pack()


def click(key):
    global word
    global chars_typed
    global accurate_typed
    global curr_word
    global position
    global typed_words
    chars_typed += 1

    if key.keysym == 'space':
        typing_box.delete(0, END)
        try:
            typed_words[word] = curr_word
        except IndexError:
            typed_words.append(curr_word)
        word += 1
        curr_word = ''
        chars_typed -= 1

    elif key.keysym == 'BackSpace':
        chars_typed -= 1

        length = len(curr_word) - 1

        if len(curr_word) == 0:
            if word > 0:
                word -= 1
                typing_box.insert(0, f"{typed_words[word]}")
                curr_word = typed_words[word]
                typed_words = typed_words[:-1]

        elif len(curr_word) != 0:
            try:
                my_word = words_list[word][length]
                if curr_word[-1] == my_word:
                    accurate_typed -= 1
            except IndexError:
                pass

            curr_word = curr_word[:-1]
            chars_typed -= 1

    elif key.char != ' ':
        curr_word += key.char
    curr_char = len(curr_word) - 1
    selected_word = words_list[word]

    if len(curr_word) > len(words_list[word]):
        position = len(''.join(words_list[:word])) + \
            len(typed_words) + len(selected_word) - 1

    else:
        position = len(''.join(words_list[:word])) + \
            len(typed_words) + len(curr_word) - 1

    if key.keysym != 'BackSpace' and key.keysym != 'space':
        try:
            selected = selected_word[curr_char]

        except IndexError:
            curr_char = len(selected_word) - 1
            selected = selected_word[curr_char]

        if selected == key.char and len(selected_word) >= len(curr_word):
            accurate_typed += 1
            text.tag_add("correct", f"1.{position}")
            text.tag_remove("incorrect", f"1.{position}")

        if selected != key.char:
            text.tag_add("incorrect", f"1.{position}")
            text.tag_remove("correct", f"1.{position}")

    text.tag_configure("correct", foreground="green")
    text.tag_configure("incorrect", foreground="red")


def start_test():
    global word
    global typing_box
    global text
    global position
    global typed_words
    global words_list
    global curr_word
    global chars_typed
    global accurate_typed
    curr_word = ''
    word = 0
    typed_words = []
    words_list = []
    position = 0
    chars_typed = 0
    accurate_typed = 0
    timer = 60
    start_button.pack_forget()
    for x in range(0, 200):
        chosen_word = random.choice(random_words).strip()
        words_list.append(chosen_word)
    text = Text(window, font=("Helvetica", 12), wrap=WORD)
    text.insert(INSERT, words_list)
    text.pack()
    typing_box = Entry()
    typing_box.pack()
    typing_box.focus()

    while timer > 0:
        window.update()
        time.sleep(.01)
        timer -= .01
        typing_box.bind("<Key>", click)
    if timer < 0:
        for i in range(0, len(typed_words)):
            if len(typed_words[i]) < len(words_list[i]):
                accurate_typed -= 1
        print(accurate_typed)
        percent = (accurate_typed/chars_typed) * 100
        message = f"You typed CPM:  {chars_typed},  WPM: {
            chars_typed/5}, accuracy = {percent:.2f}%"
        messagebox.showinfo("Information", message)

        typing_box.destroy()
        text.destroy()
        start_button.pack()


start_button = Button(text="Start", command=lambda: start_test())
start_button.pack()


window.mainloop()
