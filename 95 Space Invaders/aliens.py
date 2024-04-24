from settings import *
import turtle
import random
from laser import AlienLaser, ShipLaser


class Alien(turtle.Turtle):
    def __init__(self, species) -> None:
        super().__init__()
        self.penup()
        self.species = species
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
        self.screen.ontimer(self.clear, 300)


class Aliens():
    def __init__(self) -> None:
        self.all_aliens: list[Alien] = []
        self.move_direction = 1
        self.wave_number = 0
        self.create_aliens()
        self.move_speed = ALIEN_MOVE_SPEED
        self.laser_chance = 3000
        self.lasers: list[AlienLaser] = []

    def create_aliens(self):
        for i in range(5):
            species = 1 if i == 0 else 3 if i > 2 else 2
            for j in range(11):
                alien = Alien(species)
                x = SCREEN_L + ALIEN_MOVE_DISTANCE * 3
                y = 250 - (self.wave_number * 100)
                y = 0 if y < 0 else y
                alien.goto(x + (j * ALIEN_X_GAP), y - (i * ALIEN_Y_GAP))
                self.all_aliens.append(alien)

    def move(self):
        if self.check_for_edge():
            self.move_direction *= -1
            for alien in self.all_aliens:
                alien.goto(alien.xcor(), alien.ycor() -
                           ALIEN_MOVE_DISTANCE * 3)
        for alien in self.all_aliens:
            alien.goto(alien.xcor() + ALIEN_MOVE_DISTANCE *
                       self.move_direction, alien.ycor())

    def check_for_laser(self, laser: ShipLaser):
        for alien in self.all_aliens:
            if laser.hits(alien, 18):
                laser.goto(GRAVEYARD)
                alien.explode()
                self.all_aliens.remove(alien)
                self.move_speed -= 6000
                return (4 - alien.species) * 10

    def shoot_lasers(self):
        for alien in self.all_aliens:
            if random.randint(0, self.laser_chance) == self.laser_chance:
                self.lasers.append(AlienLaser(alien))

    def clear_lasers(self):
        for laser in self.lasers:
            laser.goto(GRAVEYARD)
        self.lasers = []

    def check_for_edge(self):
        for alien in self.all_aliens:
            if alien.xcor() > SCREEN_R - ALIEN_MOVE_DISTANCE * 4 or alien.xcor() < SCREEN_L + ALIEN_MOVE_DISTANCE * 3:
                return True
        return False

    def reset(self):
        self.move_speed = ALIEN_MOVE_SPEED
        self.wave_number += 1
        self.create_aliens()
