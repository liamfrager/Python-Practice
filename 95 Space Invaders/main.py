from settings import *
from turtle import Screen
from alien import Alien
from ship import Ship


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
        # Aliens
        self.screen.register_shape('alien1', ALIEN_1_COORDS)
        self.screen.register_shape('alien2', ALIEN_2_COORDS)
        self.screen.register_shape('alien3', ALIEN_3_COORDS)
        self.screen.register_shape('ufo', UFO_COORDS)
        self.create_aliens()
        self.screen.update()
        self.screen.mainloop()

    def create_aliens(self):
        self.aliens: list[list[Alien]] = []
        for i in range(5):
            row = []
            species = 1 if i == 0 else 3 if i > 2 else 2
            for j in range(11):
                alien = Alien(species)
                alien.goto(x=-150 + (j * 40), y=150 - (i * 40))
                row.append(alien)


app = SpaceInvaders()
