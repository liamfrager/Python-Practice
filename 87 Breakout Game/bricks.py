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
            x=SCREEN_LEFT +
            (col * (BRICK_WIDTH + (BRICK_GAP * 2))) +
            BRICK_WIDTH / 2,
            y=SCREEN_TOP -
            ((row + .5) * (BRICK_HEIGHT + (BRICK_GAP * 2))) -
            TOP_GAP
        )


class Bricks():
    def __init__(self):
        self.all_bricks: list[Brick] = []
        self.bricks_broken = 0
        self.load_bricks()

    def load_bricks(self):
        self.clear()
        colors = BRICK_COLORS
        for color in range(len(colors)):
            for row in range(2):
                for col in range(BRICKS_PER_ROW):
                    brick = Brick(colors[color], color * 2 + row, col)
                    self.all_bricks.append(brick)

    def all(self):
        return self.all_bricks

    def destroy(self, brick):
        brick.goto(GRAVEYARD)

    def clear(self):
        for brick in self.all_bricks:
            self.destroy(brick)
