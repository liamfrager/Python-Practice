from turtle import Turtle
import random
from paddle import LEFT_PADDLE_X, RIGHT_PADDLE_X


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.x_move = -10
        self.y_move = -10
        self.move_speed = .08

    def to_starting_position(self):
        self.goto(0, 0)
        self.move_speed = .08
        self.x_move *= -1

    def move(self):
        self.setx(self.xcor() + self.x_move)
        self.sety(self.ycor() + self.y_move)

    def paddle_bounce(self):
        self.x_move *= -1
        if self.x_move > 0:
            self.setx(LEFT_PADDLE_X + 20)
        else:
            self.setx(RIGHT_PADDLE_X - 20)
        self.move_speed *= .9

    def wall_bounce(self):
        self.y_move *= -1
