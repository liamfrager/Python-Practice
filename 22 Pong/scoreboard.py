from turtle import Turtle
import settings as s

ALIGN = 'center'
FONT = ('Arial', 100, 'normal')


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(0, s.SCREEN_TOP - 100)
        self.color('white')
        self.left_score = 0
        self.right_score = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"{self.left_score}   {self.right_score}",
                   align=ALIGN, font=FONT)

    def increase_score(self, side):
        if side == 'left':
            self.left_score += 1
        elif side == 'right':
            self.right_score += 1
        self.update_score()
