from settings import *
import turtle


class Laser(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.setheading(90)
        self.shapesize(.1, .5)
        self.goto(GRAVEYARD)

    def move(self):
        if self.ycor() > SCREEN_TOP:
            self.goto(GRAVEYARD)
        if self.pos() != GRAVEYARD:
            self.goto(self.xcor(), self.ycor() + LASER_MOVE_DISTANCE)

    def hits(self, alien):
        return abs(self.xcor() - alien.xcor()) < 18 and abs(self.ycor() - alien.ycor()) < 18
