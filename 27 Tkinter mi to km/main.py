from tkinter import *

window = Tk()
window.title("Convert mi/km")
window.config(padx=20, pady=20)


input = Entry(width=4, text=0)
input.grid(row=0, column=1)

mile_label = Label(text="Miles")
mile_label.grid(row=0, column=2)

equals_label = Label(text="is equal to")
equals_label.grid(row=1, column=0)

result = Label(text="0")
result.grid(row=1, column=1)

km_label = Label(text="Kilometers")
km_label.grid(row=1, column=2)


def convert():
    miles = int(input.get())
    km = miles * 1.60934
    result.config(text=round(km, 2))


submit_button = Button(text="Calculate", command=convert)
submit_button.grid(row=2, column=1)


window.mainloop()
