from settings import *
import turtle
from laser import Laser


class Alien(turtle.Turtle):
    def __init__(self, species) -> None:
        super().__init__()
        self.penup()
        self.alien_color = ALIEN_1_COLOR if species == 1 else ALIEN_2_COLOR if species == 2 else ALIEN_3_COLOR if species == 3 else UFO_COLOR
        self.color(self.alien_color)
        self.alien_shape = 'alien1' if species == 1 else 'alien2' if species == 2 else 'alien3' if species == 3 else 'ufo'
        self.shape(self.alien_shape)
        self.setheading(90)
        self.shapesize(3, 3)

    def explode(self):
        angle = 150
        side = 6
        pointies = 9
        rotation = 360/pointies
        self.pendown()
        for _ in range(pointies):
            self.forward(side)
            self.right(angle)
            self.forward(side)
            self.left(angle)
            self.right(rotation)
        self.penup()
        self.goto(GRAVEYARD)


class Aliens():
    def __init__(self) -> None:
        self.all_aliens: list[Alien] = []
        self.move_direction = 1
        self.create_aliens()
        self.last_dead = None
        self.move_speed = 500000

    def create_aliens(self):
        for i in range(5):
            species = 1 if i == 0 else 3 if i > 2 else 2
            for j in range(11):
                alien = Alien(species)
                alien.goto(x=SCREEN_L + ALIEN_MOVE_DISTANCE * 3 + (j * ALIEN_X_GAP),
                           y=150 - (i * ALIEN_Y_GAP))
                self.all_aliens.append(alien)

    def move(self):
        self.clear_explosions()
        if self.check_for_edge():
            self.move_direction *= -1
            for alien in self.all_aliens:
                alien.goto(alien.xcor(), alien.ycor() -
                           ALIEN_MOVE_DISTANCE * 3)
        for alien in self.all_aliens:
            alien.goto(alien.xcor() + ALIEN_MOVE_DISTANCE *
                       self.move_direction, alien.ycor())

    def check_for_laser(self, laser: Laser):
        for alien in self.all_aliens:
            if laser.hits(alien, 18):
                self.clear_explosions()
                laser.goto(GRAVEYARD)
                alien.explode()
                self.last_dead = alien
                self.all_aliens.remove(alien)
                self.move_speed -= 6000

    def check_for_edge(self):
        for alien in self.all_aliens:
            if alien.xcor() > SCREEN_R - ALIEN_MOVE_DISTANCE * 4 or alien.xcor() < SCREEN_L + ALIEN_MOVE_DISTANCE * 3:
                return True
        return False

    def clear_explosions(self):
        if self.last_dead != None:
            self.last_dead.clear()
