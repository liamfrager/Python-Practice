from settings import *
from turtle import Screen
from aliens import Aliens
from ship import Ship
from barriers import Barriers
from datetime import datetime


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
        self.screen.register_shape('ship', SHIP_COORDS)
        self.screen.register_shape('alien1', ALIEN_1_COORDS)
        self.screen.register_shape('alien2', ALIEN_2_COORDS)
        self.screen.register_shape('alien3', ALIEN_3_COORDS)
        self.screen.register_shape('ufo', UFO_COORDS)
        # Ship
        self.ship = Ship(self.screen)
        self.ship.bind_movement()
        # Aliens
        self.aliens = Aliens()
        # Barriers
        self.barriers = Barriers()
        # Other
        self.start_game()
        self.screen.mainloop()

    def start_game(self):
        self.start_time = datetime.now()
        self.play_game()

    def play_game(self):
        self.ship.laser.move()
        if (datetime.now() - self.start_time).microseconds > self.aliens.move_speed:
            self.aliens.move()
            self.start_time = datetime.now()
        self.barriers.check_for_laser(self.ship.laser)
        self.barriers.check_for_aliens(self.aliens.all_aliens)
        self.aliens.check_for_laser(self.ship.laser)
        self.screen.update()
        if len(self.aliens.all_aliens) > 0 and not self.aliens.all_aliens[-1].ycor() <= self.ship.ycor() + 20:
            self.play_game()
        else:
            self.game_over()

    def game_over(self):
        if len(self.aliens.all_aliens) == 0:
            print('you win!')
        else:
            print('game over')


app = SpaceInvaders()

# TODO: add win condition
# TODO: add lose condition
# TODO: fix barrier breaking
