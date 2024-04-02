from settings import *
from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color('white')
        self.score = 0
        self.update_score()

    def add_points(self, points: int):
        self.score += points
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(SCREEN_LEFT + BRICK_WIDTH, SCREEN_TOP + BRICK_HEIGHT)
        if self.score < 10:
            leading_zeros = '00'
        elif self.score < 100:
            leading_zeros = '0'
        else:
            leading_zeros = ''
        self.write(f"{leading_zeros}{self.score}",
                   align='left', font=(FONT_NAME, BRICK_HEIGHT * 6, 'bold'))

    def game_over(self):
        self.goto(0, -BRICK_WIDTH)
        self.color('red')
        self.write('Game Over!', align='center', font=(
            FONT_NAME, BRICK_HEIGHT * 4, 'bold'))
        self.goto(0, -BRICK_WIDTH * 2)
        self.color('white')
        self.write('Press the spacebar to play again!', align='center', font=(
            FONT_NAME, BRICK_HEIGHT, 'normal'))

    def to_zero(self):
        self.score = 0
        self.update_score()
