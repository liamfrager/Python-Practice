import turtle as t
import random

screen = t.Screen()
screen.title('Welcome to the turtle races!')
screen.setup(width=500, height=400)

finish_line = t.Turtle()
finish_line.shape('square')
finish_line.right(90)
finish_line.color('black')

for i in range(3):
    if i % 2 == 0:
        finish_line.teleport(230 - (20 * i), 190)
    else:
        finish_line.teleport(230 - (20 * i), 170)
    while finish_line.ycor() > -200:
        finish_line.stamp()
        finish_line.teleport(finish_line.xcor(), finish_line.ycor() - 40)


user_bet = screen.textinput(
    title="Make a bet",
    prompt="Which turtle will win the race? Enter a color:"
)


colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
turtles = []

for i in range(6):
    trtl = t.Turtle(shape='turtle')
    trtl.color(colors[i])
    trtl.up()
    spacing = 30
    num_of_turtles = 6
    trtl.goto(-230, (spacing * (num_of_turtles - 1) / 2) - (spacing * i))
    turtles.append(trtl)

is_racing = True

while is_racing:
    for turtle in turtles:
        turtle.forward(random.randint(0, 10))
        if turtle.xcor() >= 170:
            is_racing = False
            has_won_bet = 'won' if user_bet == turtle.pencolor() else 'lost'
            screen.title(f"The {turtle.pencolor()} turtle won! You {has_won_bet} the bet.")


screen.exitonclick()
