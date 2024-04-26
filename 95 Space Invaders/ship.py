from settings import *
import turtle
from laser import ShipLaser
from audio import play_sound


class Ship(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.color(SHIP_COLOR)
        self.shape('ship')
        self.setheading(90)
        self.shapesize(3, 3)
        self.laser = ShipLaser()
        self.goto(x=0, y=SCREEN_BOT + 50)

    def reset(self):
        self.clear()
        self.showturtle()

    def fire(self):
        if self.laser.pos() == GRAVEYARD:
            self.laser.goto(self.pos())
            play_sound('shoot_laser')

    def explode(self):
        angle = 150
        side = 6
        pointies = 9
        rotation = 360/pointies
        self.pendown()
        for _ in range(pointies):
            self.forward(side)
            self.right(angle)
            self.forward(side)
            self.left(angle)
            self.right(rotation)
        self.penup()
        self.hideturtle()
        self.screen.update()
        play_sound('ship_explode')

    def move_left(self):
        if self.xcor() > SCREEN_L + 10:
            self.goto(self.xcor() - SHIP_MOVE_DISTANCE, self.ycor())
            self.screen.update()

    def move_right(self):
        if self.xcor() < SCREEN_R - 60:
            self.goto(self.xcor() + SHIP_MOVE_DISTANCE, self.ycor())
            self.screen.update()

    def bind_movement(self):
        self.screen.onkey(self.move_left, 'a')
        self.screen.onkey(self.move_left, 'Left')
        self.screen.onkey(self.move_right, 'd')
        self.screen.onkey(self.move_right, 'Right')
        self.screen.onkey(self.fire, 'w')
        self.screen.onkey(self.fire, 'Up')
        self.screen.onkey(self.fire, 'space')

    def unbind_movement(self):
        keys = ['a', 'Left', 'd', 'Right', 'w', 'Up', 'space']
        for key in keys:
            self.screen.onkey(None, key)

    def follow_cursor(self, x, y):
        if x > SCREEN_L + 10 and x < SCREEN_R - 60:
            self.goto(x, self.ycor())
