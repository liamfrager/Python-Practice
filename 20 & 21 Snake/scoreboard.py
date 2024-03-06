from turtle import Turtle
import settings as s

ALIGNMENT = "center"
FONT = ('Courier', 24, 'normal')
POSITION = (0, (s.SCREEN_HEIGHT / 2) - 30)


class Scoreboard(Turtle):
    def __init__(self):
        self.score = 0
        with open('20 & 21 Snake/highscore.txt') as hs:
            self.highscore = int(hs.read())
        super().__init__()
        self.pu()
        self.speed(0)
        self.hideturtle()
        self.color('white')
        self.update()

    def update(self):
        self.clear()
        self.goto(POSITION)
        self.write(f"Score: {self.score} High Score: {
                   self.highscore}", align=ALIGNMENT, font=FONT)

    def increase(self):
        self.score += 1
        self.update()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        if self.score > self.highscore:
            self.highscore = self.score
            with open('20 & 21 Snake/highscore.txt', mode='w') as hs:
                hs.write(str(self.highscore))
        self.score = 0
