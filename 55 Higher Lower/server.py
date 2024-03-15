from flask import Flask
import random

app = Flask(__name__)

the_number = random.randint(0, 9)


@app.route('/guess/<int:guess>')
def guess(guess):
    if guess > the_number:
        message = "Too high!"
        gif = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
    elif guess < the_number:
        message = "Too low!"
        gif = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
    else:
        message = "You guessed the number!"
        gif = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"
    return \
        f'<h1>{message}</h1>' \
        '<br><br>' \
        f'<img src="{gif}"/>'


@app.route('/')
def home():
    return \
        '<h1>Guess a number between 0 and 9</h1>' \
        '<br><br>' \
        '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"/>'


if __name__ == "__main__":
    app.run(debug=True)
