from settings import *
import turtle


class Ship(turtle.Turtle):
    def __init__(self, screen: turtle._Screen) -> None:
        super().__init__()
        self.screen = screen
        self.penup()
        self.color(SHIP_COLOR)
        self.shape('ship')
        self.setheading(90)
        self.shapesize(3, 3)
        self.goto(x=0, y=SCREEN_BOT + 50)

    def move_left(self):
        if self.xcor() > SCREEN_L + 10:
            self.goto(self.xcor() - SHIP_MOVE_DISTANCE, self.ycor())
            self.screen.update()

    def move_right(self):
        if self.xcor() < SCREEN_R - 60:
            self.goto(self.xcor() + SHIP_MOVE_DISTANCE, self.ycor())
            self.screen.update()

    def fire(self):
        print('fire')

    def bind_movement(self):
        self.screen.onkey(self.move_left, 'a')
        self.screen.onkey(self.move_left, 'Left')
        self.screen.onkey(self.move_right, 'd')
        self.screen.onkey(self.move_right, 'Right')
        self.screen.onkey(self.fire, 'w')
        self.screen.onkey(self.fire, 'Up')
        self.screen.onkey(self.fire, 'space')
