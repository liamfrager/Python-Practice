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
        # Aliens
        self.screen.register_shape('alien1.gif')
        self.screen.register_shape('alien2.gif')
        self.screen.register_shape('alien3.gif')
        self.create_aliens()
        print(self.screen._shapes)
        self.screen.mainloop()

    def create_aliens(self):
        self.aliens = []
        for _ in range(5):
            row = []
            for _ in range(11):
                row.append(Alien())
        for alien in self.aliens:
            pass


app = SpaceInvaders()
