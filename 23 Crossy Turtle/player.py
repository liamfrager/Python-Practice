from turtle import Turtle


class Turt(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('turtle')
        self.color('black')
        self.to_start()

    def to_start(self):
        self.sety(-280)

    def move(self):
        self.sety(self.ycor() + 10)

    def has_crossed_the_road(self):
        return self.ycor() > 250
