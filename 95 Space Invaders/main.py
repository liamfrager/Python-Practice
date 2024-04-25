from settings import *
from turtle import Screen
from aliens import Aliens, UFO
from ship import Ship
from barriers import Barriers
from scoreboard import Scoreboard, Lives
from datetime import datetime
import random


class SpaceInvaders:
    def __init__(self) -> None:
        # Screen
        self.screen = Screen()
        self.screen.title('Space Invaders')
        self.screen.setup(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT
        )
        self.screen.bgcolor('black')
        self.screen.getcanvas().config(cursor="none")
        self.screen.tracer(0)
        self.screen.listen()
        # Shapes
        self.screen.register_shape('ship', SHIP_SHAPE)
        self.screen.register_shape('alien1', ALIEN_1_SHAPE)
        self.screen.register_shape('alien2', ALIEN_2_SHAPE)
        self.screen.register_shape('alien3', ALIEN_3_SHAPE)
        self.screen.register_shape('ufo', UFO_SHAPE)
        self.screen.register_shape('alien_laser', ALIEN_LASER_SHAPE)

        # Ship
        self.ship = Ship()
        self.follow_cursor(True)
        self.lives = Lives()
        # Aliens
        self.aliens = Aliens()
        self.ufo = UFO()
        # Barriers
        self.barriers = Barriers()
        # Scoreboard
        self.scoreboard = Scoreboard()
        # Other
        self.start_game()
        self.screen.mainloop()

    def follow_cursor(self, bool):
        def onmove(self, fun, add=None):
            def eventfun(event):
                fun(self.cv.canvasx(event.x) / self.xscale, -
                    self.cv.canvasy(event.y) / self.yscale)
            self.cv.bind('<Motion>', eventfun, add)
        onmove(self.screen, self.ship.follow_cursor if bool else None)

    def start_game(self):
        self.ship.bind_movement()
        if self.play_game():
            self.ship.unbind_movement()
            self.aliens.clear_lasers()
            self.ship.laser.goto(GRAVEYARD)
            if len(self.lives.lives) == 0:
                self.game_over()
            else:
                self.lives.lose_life()
                self.screen.ontimer(self.start_game, 1000)

    def new_wave(self):
        self.aliens.reset()
        self.lives.add_life()
        self.start_game()

    def play_game(self):
        start_time = datetime.now()
        self.ship.reset()
        while True:
            # Move aliens
            if (datetime.now() - start_time).microseconds > self.aliens.move_speed:
                self.aliens.move()
                start_time = datetime.now()
            if random.randint(0, UFO_CHANCE) == UFO_CHANCE:
                self.ufo.pick_side()
            self.ufo.fly()
            # Lasers
            self.aliens.shoot_lasers()
            lasers = self.aliens.lasers + [self.ship.laser]
            for laser in lasers:
                laser.move()
                if self.barriers.is_hit_by(laser):
                    laser.goto(GRAVEYARD)
                    if laser != self.ship.laser:
                        self.aliens.lasers.remove(laser)
                if laser != self.ship.laser and laser.hits(self.ship, 24):
                    laser.goto(GRAVEYARD)
                    self.aliens.lasers.remove(laser)
                    self.ship.explode()
                    return True
            # Points for hit aliens
            points = self.aliens.check_for_laser(self.ship.laser)
            points += self.ufo.check_for_laser(self.ship.laser)
            self.scoreboard.score_points(points)
            # Destroy barriers with alien collision
            self.barriers.check_for_aliens(self.aliens.all_aliens)
            # Continue?
            if len(self.aliens.all_aliens) == 0:
                self.new_wave()
            elif self.aliens.all_aliens[-1].ycor() <= self.ship.ycor() + 20:
                break
            self.screen.update()
        self.game_over()

    def game_over(self):
        self.ship.unbind_movement()
        self.follow_cursor(False)
        print('game over')


app = SpaceInvaders()

# TODO: add wiggle animation
# TODO: add sounds
# TODO: add UFO shape
# TODO: increase difficulty on later rounds (laser rate, speed)
# TODO: game over screen
