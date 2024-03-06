from turtle import Turtle
from random import randint
import settings as s


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.pu()
        self.shapesize(.5, .5)
        self.color('red')
        self.speed(0)
        self.respawn()

    def respawn(self):
        rand_x = round(randint(s.X_MIN, s.X_MAX) / 20) * 20
        rand_y = round(randint(s.Y_MIN, s.Y_MAX) / 20) * 20
        self.goto(rand_x, rand_y)
