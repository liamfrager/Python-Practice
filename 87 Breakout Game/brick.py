from settings import *
from turtle import Turtle


class Brick(Turtle):
    def __init__(self, color, row, col):
        super().__init__()
        self.penup()
        self.color(color)
        self.shape('square')
        self.shapesize(BRICK_WIDTH / 20, BRICK_HEIGHT / 20, 1)
        self.goto(
            x=SCREEN_LEFT + ((col + .5) * (BRICK_WIDTH + BRICK_GAP)),
            y=SCREEN_TOP - ((row + 3.5) * (BRICK_HEIGHT + BRICK_GAP))
        )

    def destroy(self):
        self.goto(GRAVEYARD)
