from settings import *
import turtle


class Alien(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.color(ALIEN_COLOR)
        self.shape('alien1.gif')
