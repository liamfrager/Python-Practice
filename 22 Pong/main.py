import settings as s
from turtle import Turtle, Screen, mode
import time
from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard

mode('logo')

# Setup screen
screen = Screen()
screen.title('Pong')
screen.setup(width=s.SCREEN_WIDTH, height=s.SCREEN_HEIGHT)
screen.bgcolor('black')
screen.tracer(0)
screen.listen()

# Setup stuff
midline = Turtle(shape='square')
midline.pu()
midline.teleport(0, s.SCREEN_BOTTOM)
midline.shapesize(.5, 1, 1)
midline.color('white')
midline.width(10)
while midline.ycor() < s.SCREEN_TOP:
    midline.stamp()
    midline.forward(30)

scoreboard = Scoreboard()
ball = Ball()

paddle_l = Paddle('left')
screen.onkeypress(paddle_l.up, 'w')
screen.onkeypress(paddle_l.down, 's')
paddle_r = Paddle('right')
screen.onkeypress(paddle_r.up, 'Up')
screen.onkeypress(paddle_r.down, 'Down')


game_is_on = True
while game_is_on:
    ball.to_starting_position()
    paddle_l.to_starting_position()
    paddle_r.to_starting_position()
    screen.update()
    time.sleep(1)

    match_is_on = True
    while match_is_on:
        time.sleep(ball.move_speed)
        screen.update()
        ball.move()
        if (ball.distance(paddle_r) < 50 and ball.xcor() > s.SCREEN_RIGHT - 60) or (ball.distance(paddle_l) < 50 and ball.xcor() < s.SCREEN_LEFT + 60):
            ball.paddle_bounce()

        if ball.ycor() > s.SCREEN_TOP - 30 or ball.ycor() < s.SCREEN_BOTTOM + 30:
            ball.wall_bounce()

        if ball.xcor() > s.SCREEN_RIGHT or ball.xcor() < s.SCREEN_LEFT:
            side = 'left' if ball.xcor() > 0 else 'right'
            scoreboard.increase_score(side)
            match_is_on = False

    if scoreboard.right_score == 7 or scoreboard.left_score == 7:
        game_is_on = False

screen.exitonclick()
