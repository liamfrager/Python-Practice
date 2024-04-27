from settings import *
import turtle
import random
from laser import AlienLaser, ShipLaser
from audio import play_sound, play_ufo_sound


class Alien(turtle.Turtle):
    def __init__(self, species) -> None:
        super().__init__()
        self.penup()
        self.species = species
        self.alien_color = ALIEN_1_COLOR if species == 1 else ALIEN_2_COLOR if species == 2 else ALIEN_3_COLOR if species == 3 else UFO_COLOR
        self.color(self.alien_color)
        self.alien_shapes = [
            '',
            f'alien{self.species}a',
            f'alien{self.species}b'
        ]
        self.shape_index = 1
        self.shape(self.alien_shapes[self.shape_index])
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
        play_sound('alien_explode')
        self.screen.ontimer(self.clear, 300)

    def wiggle(self):
        self.shape_index *= -1
        self.shape(self.alien_shapes[self.shape_index])


class Aliens():
    def __init__(self, screen: turtle._Screen) -> None:
        self.screen = screen
        self.all_aliens: list[Alien] = []
        self.move_direction = 1
        self.moving = False
        self.wave_number = 0
        self.move_speed = ALIEN_MOVE_SPEED
        self.on_edge = False
        self.move_sound = 1
        self.lasers: list[AlienLaser] = []

    def create_aliens(self):
        self.clear_aliens()
        for i in range(5):
            species = 1 if i == 0 else 3 if i > 2 else 2
            for j in range(11):
                alien = Alien(species)
                x = SCREEN_L + ALIEN_MOVE_DISTANCE * 3
                y = 250 - (self.wave_number * 100)
                y = -50 if y < -50 else y
                alien.goto(x + (j * ALIEN_X_GAP), y - (i * ALIEN_Y_GAP))
                self.all_aliens.append(alien)

    def clear_aliens(self):
        for alien in self.all_aliens:
            alien.goto(GRAVEYARD)
        self.all_aliens = []

    def move(self):
        if self.move_speed > 0:
            self.screen.ontimer(self.move, self.move_speed)
        else:
            self.screen.ontimer(self.move, 0)
        if self.moving:
            play_sound(f'alien_{self.move_sound}')
            self.move_sound = self.move_sound + 1 if self.move_sound < 4 else 1
            if self.is_on_edge():
                self.move_direction *= -1
                self.move_speed - 25
                for alien in self.all_aliens:
                    alien.wiggle()
                    alien.goto(alien.xcor(), alien.ycor() -
                               ALIEN_MOVE_DISTANCE * 3)
                return
            for alien in self.all_aliens:
                alien.wiggle()
                alien.goto(alien.xcor() + ALIEN_MOVE_DISTANCE *
                           self.move_direction, alien.ycor())

    def go(self):
        self.moving = True

    def stop(self):
        self.moving = False

    def check_for_laser(self, laser: ShipLaser):
        for alien in self.all_aliens:
            if laser.hits(alien, 18):
                laser.goto(GRAVEYARD)
                alien.explode()
                self.all_aliens.remove(alien)
                self.move_speed -= 5
                return (4 - alien.species) * 10
        return 0

    def shoot_lasers(self):
        for alien in self.all_aliens:
            chance = ALIEN_LASER_CHANCE - (550 * self.wave_number)
            chance = 550 if chance < 550 else chance
            if random.randint(0, chance) == chance:
                self.lasers.append(AlienLaser(alien))

    def clear_lasers(self):
        for laser in self.lasers:
            laser.goto(GRAVEYARD)
        self.lasers = []

    def is_on_edge(self):
        if self.on_edge == True:
            self.on_edge = False
            return False
        for alien in self.all_aliens:
            if alien.xcor() > SCREEN_R - ALIEN_MOVE_DISTANCE * 4 or alien.xcor() < SCREEN_L + ALIEN_MOVE_DISTANCE * 3:
                self.on_edge = True
                return self.on_edge
        return False

    def new_wave(self):
        self.stop()
        self.move_direction = 1
        self.wave_number += 1
        self.move_speed = ALIEN_MOVE_SPEED - (55 * self.wave_number)
        self.move_speed = 330 if self.move_speed < 330 else self.move_speed
        self.clear_lasers()
        self.create_aliens()


class UFO(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.shape('ufo')
        self.color(UFO_COLOR)
        self.setheading(90)
        self.shapesize(3, 3)
        self.goto(GRAVEYARD)
        self.side = 0

    def pick_side(self):
        if self.pos() == GRAVEYARD:
            play_ufo_sound()
            sides = [SCREEN_L, SCREEN_R]
            self.side = random.choice(sides)
            self.goto(self.side, UFO_FLY_Y)

    def fly(self):
        if self.pos() != GRAVEYARD:
            direction = 1 if self.side < 0 else -1
            self.goto(self.xcor() + UFO_MOVE_DISTANCE * direction, UFO_FLY_Y)
            if self.xcor() < SCREEN_L or self.xcor() > SCREEN_R:
                play_ufo_sound(False)
                self.goto(GRAVEYARD)

    def check_for_laser(self, laser: ShipLaser):
        if self.pos() != GRAVEYARD and laser.hits(self, 24):
            laser.goto(GRAVEYARD)
            self.explode()
            return random.choice([50, 100, 150, 200])
        return 0

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
        self.screen.ontimer(self.clear, 300)
        play_sound('alien_explode')
        self.reset()

    def reset(self):
        self.goto(GRAVEYARD)
        play_ufo_sound(False)
