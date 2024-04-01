from settings import *
from turtle import Turtle
from brick import Brick
from paddle import Paddle
from datetime import datetime
import random


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('circle')
        self.shapesize(BALL_SIZE / 20, BALL_SIZE / 20, 1)
        self.x_move = random.choice([-5, 5])
        self.y_move = -5
        self.to_starting_position()

    def to_starting_position(self):
        self.goto(0, 0)
        self.move_speed = .03
        self.x_move *= -1

    def move(self):
        self.setx(self.xcor() + self.x_move)
        self.sety(self.ycor() + self.y_move)

    def x_bounce(self):
        self.x_move *= -1
        self.last_bounce_time = datetime.now().time()
        # print(self.last_bounce_time)

    def y_bounce(self):
        self.y_move *= -1
        self.last_bounce_time = datetime.now().time()
        # print(self.last_bounce_time)

    def get_object_sides(self, object: Brick | Paddle):
        object_width = BRICK_WIDTH if type(object) == Brick else PADDLE_WIDTH
        object_height = BRICK_HEIGHT if type(
            object) == Brick else PADDLE_HEIGHT
        object_l = object.xcor() - (object_width + BALL_SIZE) / 2
        object_r = object.xcor() + (object_width + BALL_SIZE) / 2
        object_t = object.ycor() + (object_height + BALL_SIZE) / 2
        object_b = object.ycor() - (object_height + BALL_SIZE) / 2
        return (object_l, object_r, object_t, object_b)

    def is_collide_left_right(self, object: Brick):
        # print(f'--x: {self.xcor()}, y: {self.ycor()}')
        # print(f'    {object_t}\n{object_l}  {object_r}\n    {object_b}')
        object_l, object_r, object_t, object_b = self.get_object_sides(object)
        if self.xcor() == object_l or self.xcor() == object_r:
            if self.ycor() >= object_b and self.ycor() <= object_t:
                return True
        return False

    def is_collide_top_bot(self, object: Brick):
        object_l, object_r, object_t, object_b = self.get_object_sides(object)
        if self.ycor() == object_t or self.ycor() == object_b:
            if self.xcor() >= object_l and self.xcor() <= object_r:
                return True
        return False

    def speed_up(self):
        self.move_speed *= .9
