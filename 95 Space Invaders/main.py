from settings import *
from turtle import Screen
from aliens import Aliens, UFO
from ship import Ship
from barriers import Barriers
from scoreboard import Scoreboard, Lives
from audio import play_ufo_sound
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
        self.screen.register_shape('alien1a', ALIEN_1A_SHAPE)
        self.screen.register_shape('alien1b', ALIEN_1B_SHAPE)
        self.screen.register_shape('alien2a', ALIEN_2A_SHAPE)
        self.screen.register_shape('alien2b', ALIEN_2B_SHAPE)
        self.screen.register_shape('alien3a', ALIEN_3A_SHAPE)
        self.screen.register_shape('alien3b', ALIEN_3B_SHAPE)
        self.screen.register_shape('ufo', UFO_SHAPE)
        self.screen.register_shape('alien_laser', ALIEN_LASER_SHAPE)
        # Ship
        self.ship = Ship()
        self.lives = Lives()
        # Aliens
        self.aliens = Aliens()
        self.ufo = UFO()
        # Barriers
        self.barriers = Barriers()
        # Scoreboard
        self.scoreboard = Scoreboard()
        # Other
        self.screen.onkey(self.new_game, 'Return')
        self.screen.mainloop()

    def follow_cursor(self, bool):
        def onmove(self, fun, add=None):
            def eventfun(event):
                fun(self.cv.canvasx(event.x) / self.xscale, -
                    self.cv.canvasy(event.y) / self.yscale)
            self.cv.bind('<Motion>', eventfun, add)
        onmove(self.screen, self.ship.follow_cursor if bool else None)

    def new_game(self):
        self.screen.onkey(None, 'enter')
        self.follow_cursor(True)
        self.aliens.__init__()
        self.aliens.create_aliens()
        self.barriers.reset_barriers()
        self.barriers.create_barriers()
        self.lives.reset_lives()
        self.scoreboard.reset_score()
        self.start_game()

    def start_game(self):
        self.ship.bind_movement()
        is_shot = self.play_game()
        self.ship.unbind_movement()
        self.aliens.clear_lasers()
        self.aliens.stop()
        self.ufo.reset()
        self.ship.laser.goto(GRAVEYARD)
        self.screen.update()
        if is_shot:
            if len(self.lives.lives) == 0:
                self.game_over()
            else:
                self.lives.lose_life()
                self.screen.ontimer(self.start_game, 2000)
        else:
            self.game_over()

    def new_wave(self):
        self.aliens.new_wave()
        self.lives.add_life()
        self.start_game()

    def play_game(self):
        self.aliens.go()
        self.ship.reset()
        while True:
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
            # Move aliens
            if random.randint(0, UFO_CHANCE) == UFO_CHANCE:
                self.ufo.pick_side()
            self.ufo.fly()
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
                self.ship.explode()
                return False
            self.screen.update()

    def game_over(self):
        self.follow_cursor(False)
        self.scoreboard.game_over()
        self.aliens.clear_aliens()
        self.screen.update()
        self.screen.onkey(self.new_game, 'enter')


app = SpaceInvaders()

# TODO: increase difficulty on later rounds (laser rate, speed)
