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
            SCREEN_LEFT + (BRICK_WIDTH / 2) +
            (col * (BRICK_WIDTH + BRICK_GAP)),
            SCREEN_TOP - (BRICK_HEIGHT / 2) -
            ((row + 3) * (BRICK_HEIGHT + BRICK_GAP))
        )

    def destroy(self):
        self.goto(GRAVEYARD)
