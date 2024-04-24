from settings import *
import turtle


class ShipLaser(turtle.Turtle):
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


class AlienLaser(turtle.Turtle):
    def __init__(self, alien) -> None:
        super().__init__()
        self.penup()
        self.color('yellow')
        self.shape('alien_laser')
        self.shapesize(1.5, 1.5)
        self.goto(alien.pos())

    def move(self):
        if self.ycor() < SCREEN_BOT:
            self.goto(GRAVEYARD)
        if self.pos() != GRAVEYARD:
            self.goto(self.xcor(), self.ycor() - LASER_MOVE_DISTANCE)

    def hits(self, object: turtle.Turtle, hit_box):
        return abs(self.xcor() - object.xcor()) < hit_box and abs(self.ycor() - object.ycor()) < hit_box
