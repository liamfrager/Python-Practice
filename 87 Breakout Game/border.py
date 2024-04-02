from settings import *
from turtle import Turtle


class Border(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.shape('square')
        self.color('white')
        self.pensize(width=BALL_SIZE)
        self.goto(SCREEN_LEFT, SCREEN_TOP)
        self.pendown()
        self.goto(SCREEN_RIGHT, SCREEN_TOP)
