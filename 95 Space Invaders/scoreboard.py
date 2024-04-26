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


class Lives(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.shape('ship')
        self.color('white')
        self.setheading(90)
        self.shapesize(3, 3)
        self.lives = []
        for _ in range(2):
            self.add_life()

    def add_life(self):
        if len(self.lives) < 3:
            self.goto(SCREEN_R - (len(self.lives) + 1) * 50, SCREEN_TOP - 50)
            id = self.stamp()
            self.lives.append(id)
            self.goto(GRAVEYARD)

    def lose_life(self):
        id = self.lives.pop()
        self.clearstamp(id)
