from settings import *
from turtle import Screen
from aliens import Aliens
from ship import Ship
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
        # Ship
        self.ship = Ship(self.screen)
        self.ship.bind_movement()
        # Aliens
        self.screen.register_shape('ufo', UFO_COORDS)
        self.aliens = Aliens()
        # Other
        self.start_game()
        self.screen.mainloop()

    def start_game(self):
        start_time = datetime.now()
        while True:
            self.ship.laser.move()
            if (datetime.now() - start_time).microseconds > 500000:
                self.aliens.move()
                start_time = datetime.now()
            self.aliens.check_for_laser(self.ship.laser)
            self.screen.update()


app = SpaceInvaders()
