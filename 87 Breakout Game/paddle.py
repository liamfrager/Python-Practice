from settings import *
from turtle import Turtle


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.shapesize(PADDLE_SIZE, PADDLE_HEIGHT / 20, 1)
        self.to_starting_position()

    def to_starting_position(self):
        self.goto(0, PADDLE_Y)

    def left(self):
        if self.xcor() > SCREEN_LEFT + ((PADDLE_SIZE + 1) / 2 * 20):
            self.goto(self.xcor() - 20, self.ycor())

    def right(self):
        if self.xcor() < SCREEN_RIGHT - ((PADDLE_SIZE + 1) / 2 * 20):
            self.goto(self.xcor() + 20, self.ycor())
