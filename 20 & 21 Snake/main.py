import turtle as t
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import settings as s


screen = t.Screen()
screen.setup(height=s.SCREEN_HEIGHT, width=s.SCREEN_WIDTH)
screen.bgcolor('black')
screen.title('Snake')
screen.listen()
screen.tracer(0)

scoreboard = Scoreboard()
snake = Snake()
food = Food()

screen.onkeypress(snake.head_n, 'w')
screen.onkeypress(snake.head_n, 'Up')
screen.onkeypress(snake.head_s, 's')
screen.onkeypress(snake.head_s, 'Down')
screen.onkeypress(snake.head_e, 'd')
screen.onkeypress(snake.head_e, 'Right')
screen.onkeypress(snake.head_w, 'a')
screen.onkeypress(snake.head_w, 'Left')


def reset_game():
    scoreboard.game_over()
    screen.update()
    time.sleep(1)
    scoreboard.update()
    snake.reset()


game_on = True
while game_on:
    screen.update()
    time.sleep(.1)
    snake.move()

    # Detect collision with food
    if snake.head.distance(food) < 15:
        scoreboard.increase()
        snake.eat()
        food.respawn()

    # Detect collision with wall
    if snake.head.xcor() > s.X_MAX or snake.head.xcor() < s.X_MIN or snake.head.ycor() > s.Y_MAX or snake.head.ycor() < s.Y_MIN:
        reset_game()

    # Detect collition with snake
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) == 0:
            reset_game()

screen.exitonclick()
