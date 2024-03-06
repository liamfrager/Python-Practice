import settings as s
from turtle import Turtle

LEFT_PADDLE_X = s.SCREEN_LEFT + 40
RIGHT_PADDLE_X = s.SCREEN_RIGHT - 40


class Paddle(Turtle):
    def __init__(self, side):
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.shapesize(1, s.PADDLE_SIZE, 1)
        self.side = side
        self.to_starting_position()

    def to_starting_position(self):
        if self.side == 'left':
            self.goto(LEFT_PADDLE_X, 0)
        elif self.side == 'right':
            self.goto(RIGHT_PADDLE_X, 0)

    def up(self):
        if self.ycor() < s.SCREEN_TOP - ((s.PADDLE_SIZE + 1) / 2 * 20):
            self.forward(20)

    def down(self):
        if self.ycor() > s.SCREEN_BOTTOM + ((s.PADDLE_SIZE + 1) / 2 * 20):
            self.backward(20)
