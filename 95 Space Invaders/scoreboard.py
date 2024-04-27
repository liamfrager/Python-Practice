from settings import *
import turtle


class HighScore(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color('white')

    def get_highscore(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def write_highscore(self, new_highscore):
        with open('highscore.txt', 'w') as f:
            f.write(str(new_highscore))
        self.update_highscore()

    def update_highscore(self):
        self.clear()
        self.goto(0 - 100, SCREEN_TOP - 50)
        self.write(
            f'Hi-Score: {self.get_highscore()}',
            align='left',
            font=('Courier', 24, 'bold')
        )


class Scoreboard(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.hideturtle()
        self.score = 0
        self.welcome()
        self.highscore = HighScore()

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
        self.highscore.update_highscore()

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
        if self.score > self.highscore.get_highscore():
            self.highscore.write_highscore(self.score)
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
