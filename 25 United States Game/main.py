import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

t = turtle.Turtle()
t.penup()
t.hideturtle()

data = pandas.read_csv('50_states.csv')
all_states = data.state.to_list()
correct_guesses = []

score = turtle.Turtle()
score.penup()
score.hideturtle()
score.goto(300, 300)


def update_score():
    score.clear()
    score.write(f"{len(correct_guesses)}/50", align='right',
                font=('Courier', 30, 'normal'))


update_score()
while len(correct_guesses) < 50:
    answer_state = screen.textinput(
        title="Guess a state", prompt="What's another state's name?").title()
    if answer_state == "Exit":
        break
    if answer_state in all_states and answer_state not in correct_guesses:
        correct_guesses.append(answer_state)
        x = float(data[data.state == answer_state].x)
        y = float(data[data.state == answer_state].y)
        t.goto(x, y)
        t.write(f"{answer_state}")
        update_score()

if len(correct_guesses) == 50:
    t.goto(0, 300)
    t.write("You win!", align='center', font=('Courier', 30, 'normal'))
else:
    states_to_learn = [
        state for state in all_states if state not in correct_guesses]
    pandas.DataFrame(states_to_learn).to_csv('states_to_learn.csv')
