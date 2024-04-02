from settings import *
from turtle import Turtle


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self. size = PADDLE_WIDTH
        self.to_starting_position()

    def shrink(self):
        self.size *= .5
        self.shapesize(self.size / 40, PADDLE_HEIGHT / 20, 1)

    def to_starting_position(self):
        self.shapesize(self.size / 20, PADDLE_HEIGHT / 20, 1)
        self.goto(0, PADDLE_Y)

    def left(self):
        if self.xcor() > SCREEN_LEFT + (self.size + BRICK_HEIGHT + BRICK_GAP) / 2:
            self.goto(self.xcor() - 20, self.ycor())

    def right(self):
        if self.xcor() < SCREEN_RIGHT - (self.size + BRICK_HEIGHT + BRICK_GAP) / 2:
            self.goto(self.xcor() + 20, self.ycor())

    def follow_cursor(self, x, y):
        print(x, y)
        if x > SCREEN_LEFT + (self.size + BRICK_HEIGHT + BRICK_GAP) / 2 and x < SCREEN_RIGHT - (self.size + BRICK_HEIGHT + BRICK_GAP) / 2:
            self.goto(x, self.ycor())
