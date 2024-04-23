from settings import *
import turtle


class Alien(turtle.Turtle):
    def __init__(self, species) -> None:
        super().__init__()
        self.penup()
        self.color(ALIEN_1_COLOR if species == 1 else ALIEN_2_COLOR if species ==
                   2 else ALIEN_3_COLOR if species == 3 else UFO_COLOR)
        self.shape('alien1' if species == 1 else 'alien2' if species ==
                   2 else 'alien3' if species == 3 else 'ufo')
        self.setheading(90)
        self.shapesize(3, 3)
