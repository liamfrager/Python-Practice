from settings import *
import turtle


class Scoreboard(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.hideturtle()
        self.score = 0
        self.welcome()

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

    def reset_score(self):
        self.score = 0
        self.update_score()

    def welcome(self):
        self.goto(0, 10)
        self.color(LOGO_COLOR)
        self.write(
            LOGO,
            align='center',
            font=('Courier', 20, 'bold')
        )
        self.goto(0, -10)
        self.color('white')
        self.write(
            'Press ENTER to play',
            align='center',
            font=('Courier', 18, 'bold')
        )

    def game_over(self):
        self.goto(0, 10)
        self.color('firebrick')
        self.write(
            'GAME OVER',
            align='center',
            font=('Courier', 40, 'bold')
        )
        self.goto(0, -10)
        self.color('white')
        self.write(
            'Press ENTER to play again',
            align='center',
            font=('Courier', 18, 'bold')
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

    def add_life(self):
        if len(self.lives) < 3:
            self.goto(SCREEN_R - (len(self.lives) + 1) * 50, SCREEN_TOP - 50)
            id = self.stamp()
            self.lives.append(id)
            self.goto(GRAVEYARD)

    def lose_life(self):
        try:
            id = self.lives.pop()
        except IndexError:
            return
        else:
            self.clearstamp(id)

    def reset_lives(self):
        for _ in range(3):
            self.lose_life()
        for _ in range(2):
            self.add_life()
