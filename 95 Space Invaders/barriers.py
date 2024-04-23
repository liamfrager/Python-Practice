from settings import *
import turtle
from laser import Laser
from aliens import Alien


class Barrier(turtle.Turtle):
    def __init__(self, position) -> None:
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.shapesize(.4, .4)
        self.goto(position)


class Barriers(turtle.Turtle):
    def __init__(self) -> None:
        self.all_barriers: list[Barrier] = []
        self.create_barriers()

    def create_barriers(self):
        for barrier in range(1, 5):
            x = SCREEN_L + (SCREEN_WIDTH // 5) * barrier - 64
            y = SCREEN_BOT + 100
            for i in range(12):
                for j in range(16):
                    if not (i < 4 and (j > 3 and j < 12)):
                        if j + 8 > i and j < 23 - i:
                            position = (x + j * 6, y + i * 6)
                            barrier = Barrier(position)
                            self.all_barriers.append(barrier)

    def check_for_laser(self, laser: Laser):
        for barrier in self.all_barriers:
            if laser.hits(barrier, 6):
                laser.goto(GRAVEYARD)
                barrier.goto(GRAVEYARD)
                self.all_barriers.remove(barrier)

    def check_for_aliens(self, aliens: list[Alien]):
        for barrier in self.all_barriers:
            for alien in aliens:
                if abs(alien.xcor() - barrier.xcor()) < 20 and abs(alien.ycor() - barrier.ycor()) < 20:
                    barrier.goto(GRAVEYARD)
                    self.all_barriers.remove(barrier)
