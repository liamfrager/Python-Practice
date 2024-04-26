from settings import *
import turtle
from laser import ShipLaser, AlienLaser
from aliens import Alien


class Barrier(turtle.Turtle):
    def __init__(self, position) -> None:
        super().__init__()
        self.penup()
        self.color('white')
        self.shape('square')
        self.shapesize(BARRIER_SIZE / 20, BARRIER_SIZE / 20)
        self.goto(position)


class Barriers(turtle.Turtle):
    def __init__(self) -> None:
        self.all_barriers: list[Barrier] = []

    def create_barriers(self):
        for barrier in range(2, 10, 2):
            x = SCREEN_L + (SCREEN_WIDTH // 9) * barrier - BARRIER_SIZE * 8
            y = SCREEN_BOT + 100
            for row in range(6):
                for col in range(8):
                    if not (row < 2 and (col > 1 and col < 6)) and not (row == 2 and col in (3, 4)) and col + 5 > row and 7 - col + 5 > row:
                        position = (x + col * BARRIER_SIZE,
                                    y + row * BARRIER_SIZE)
                        barrier = Barrier(position)
                        self.all_barriers.append(barrier)

    def is_hit_by(self, laser: ShipLaser | AlienLaser):
        for barrier in self.all_barriers:
            if laser.hits(barrier, 10):
                laser.goto(GRAVEYARD)
                barrier.goto(GRAVEYARD)
                self.all_barriers.remove(barrier)
                return True
        return False

    def check_for_aliens(self, aliens: list[Alien]):
        for barrier in self.all_barriers:
            for alien in aliens:
                if abs(alien.xcor() - barrier.xcor()) < 20 and abs(alien.ycor() - barrier.ycor()) < 20:
                    barrier.goto(GRAVEYARD)
                    self.all_barriers.remove(barrier)

    def reset_barriers(self):
        for barrier in self.all_barriers:
            barrier.goto(GRAVEYARD)
        self.all_barriers = []
