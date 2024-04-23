from settings import *
import turtle


class Laser(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.shapesize(.5, .1)
        self.goto(GRAVEYARD)

    def move(self):
        if self.ycor() > SCREEN_TOP:
            self.goto(GRAVEYARD)
        if self.pos() != GRAVEYARD:
            self.goto(self.xcor(), self.ycor() + LASER_MOVE_DISTANCE)

    def hits(self, object, hit_box):
        return abs(self.xcor() - object.xcor()) < hit_box and abs(self.ycor() - object.ycor()) < hit_box
