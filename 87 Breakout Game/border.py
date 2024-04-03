from settings import *
from turtle import Turtle


class Border(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.trace_outline()
        self.add_colors()

    def trace_outline(self):
        self.penup()
        self.hideturtle()
        self.shape('square')
        self.color('white')
        self.pensize(width=BALL_SIZE)
        self.goto(SCREEN_LEFT, SCREEN_TOP)
        self.pendown()
        self.goto(SCREEN_RIGHT, SCREEN_TOP)
        self.goto(SCREEN_RIGHT, SCREEN_BOTTOM)
        self.goto(SCREEN_LEFT, SCREEN_BOTTOM)
        self.goto(SCREEN_LEFT, SCREEN_HEIGHT // 2)
        self.goto(SCREEN_RIGHT, SCREEN_HEIGHT // 2)
        self.goto(SCREEN_RIGHT, SCREEN_TOP)
        self.penup()

    def add_colors(self):
        # Bricks
        for color in range(len(BRICK_COLORS)):
            self.color(BRICK_COLORS[color])
            self.shapesize(BALL_SIZE / 20, (BRICK_GAP * 8) / 20)
            self.goto(
                x=SCREEN_LEFT,
                y=SCREEN_TOP -
                (color * 2 * (BRICK_HEIGHT + (BRICK_GAP * 2))) -
                TOP_GAP - BRICK_HEIGHT * 2
            )
            self.stamp()
            self.goto(
                SCREEN_RIGHT,
                self.ycor()
            )
            self.stamp()
        # Paddle
        self.color(PADDLE_COLOR)
        self.goto(SCREEN_LEFT, PADDLE_Y)
        self.stamp()
        self.goto(
            SCREEN_RIGHT,
            self.ycor()
        )
        self.stamp()
