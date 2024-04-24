from settings import *
import turtle


class Scoreboard(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color('white')
        self.score = 0
        self.update_score()

    def score_points(self, points):
        self.score += points if points != None else 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(SCREEN_L + 50, SCREEN_TOP - 50)
        self.write(
            f'Score: {self.score}',
            align='left',
            font=('Courier', 24, 'bold')
        )
