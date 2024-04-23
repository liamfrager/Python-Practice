from settings import *
import turtle
import time


class Alien(turtle.Turtle):
    def __init__(self, screen: turtle._Screen, species) -> None:
        super().__init__()
        self.penup()
        self.alien_color = ALIEN_1_COLOR if species == 1 else ALIEN_2_COLOR if species == 2 else ALIEN_3_COLOR if species == 3 else UFO_COLOR
        self.color(self.alien_color)
        self.alien_shape = 'alien1' if species == 1 else 'alien2' if species == 2 else 'alien3' if species == 3 else 'ufo'
        self.shape(self.alien_shape)
        self.setheading(90)
        self.shapesize(3, 3)

    def die(self):
        for _ in range(3):
            self.color('red')
            self.screen.update()
            time.sleep(.05)
            self.color(self.alien_color)
            self.screen.update()
            time.sleep(.05)
        self.goto(GRAVEYARD)
