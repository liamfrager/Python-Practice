from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = [
        let for let in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZY"
    ]
    numbers = [num for num in "1234567890"]
    symbols = [sym for sym in "!@#$%^&*()_+-="]

    let = [random.choice(letters) for _ in range(random.randint(8, 10))]
    num = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    sym = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    random_password_list = let + num + sym
    random.shuffle(random_password_list)
    random_password = "".join(random_password_list)
    password_input.delete(0, END)
    password_input.insert(END, random_password)
    pyperclip.copy(random_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_input.get()
    email_username = email_username_input.get()
    password = password_input.get()
    new_password = {
        website: {
            "email": email_username,
            "password": password,
        }
    }
    if website == "" or email_username == "" or password == "":
        messagebox.showwarning(title="Empty Fields",
                               message="Don't leave any fields blank!")
    else:
        try:
            with open('passwords.json', mode='r') as pw_file:
                data = json.load(pw_file)
                data.update(new_password)
        except FileNotFoundError:
            data = new_password
        finally:
            with open('passwords.json', mode='w') as pw_file:
                json.dump(data, pw_file, indent=4)
                website_input.delete(0, END)
                password_input.delete(0, END)
        messagebox.showinfo(title="Password Saved!",
                            message="Password saved!")

# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    search = website_input.get()
    try:
        with open('passwords.json', mode='r') as pw_file:
            data = json.load(pw_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error",
                             message="You don't have any passwords saved.")
    else:
        if search in data:
            email_username = data[search]['email']
            password = data[search]['password']
            messagebox.showinfo(
                title=search, message=f"Email/Username: {email_username}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error",
                                 message=f"You don't have a password saved for {search}.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(height=200, width=200, padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_photo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_photo)
canvas.grid(row=0, column=0, columnspan=3)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_input = Entry(width=25)
website_input.grid(row=1, column=1)
website_input.focus()
search_password_button = Button(
    text="Search",
    command=search_password,
    width=13
)
search_password_button.grid(row=1, column=2)


email_username_label = Label(text="Email/Username:")
email_username_label.grid(row=2, column=0)
email_username_input = Entry(width=42)
email_username_input.grid(row=2, column=1, columnspan=2)
email_username_input.insert(END, "liam.frager@gmail.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_input = Entry(width=25)
password_input.grid(row=3, column=1)
generate_password_button = Button(
    text="Generate Password",
    command=generate_password,
    width=13
)
generate_password_button.grid(row=3, column=2)

add_password_button = Button(
    text="Add",
    command=save_password,
    width=40
)
add_password_button.grid(row=4, column=1, columnspan=2)


window.mainloop()
