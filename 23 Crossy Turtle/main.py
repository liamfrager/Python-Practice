import turtle as t
import time
from player import Turt
from cars import Cars
from scoreboard import Scoreboard

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
NUMBER_OF_CARS = 20

t.colormode(255)
t.mode('logo')

screen = t.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.listen()

# Setup scoreboard
scoreboard = Scoreboard()

# Setup turt
player = Turt()
screen.onkeypress(player.move, 'space')

# Setup cars
cars = Cars()

# Setup game
game_is_on = True
loop = 0
while game_is_on:
    loop += 1
    if loop % 6 == 0:
        cars.make_new_car()
    cars.move_cars()
    print(cars.have_squished(player))
    if cars.have_squished(player):
        game_is_on = False
        scoreboard.game_over()
    if player.has_crossed_the_road():  # If turtle at finish line
        player.to_start()
        scoreboard.level_up()
        cars.accelerate()
    time.sleep(0.1)
    screen.update()


screen.exitonclick()
