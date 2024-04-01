from settings import *
from turtle import Turtle, Screen, mode
from brick import Brick
from paddle import Paddle
from ball import Ball
import time

mode('logo')


class Breakout:
    def __init__(self):
        # Screen
        self.screen = Screen()
        self.screen.title('Pong')
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor('black')
        self.screen.tracer(0)
        self.screen.listen()
        # Bricks
        self.all_bricks: list[Brick] = []
        self.load_bricks()
        # Paddle
        self.paddle = Paddle()
        self.screen.onkeypress(self.paddle.right, 'Right')
        self.screen.onkeypress(self.paddle.left, 'Left')
        # Ball
        self.ball = Ball()

        self.start_game()

    def load_bricks(self):
        colors = ['red', 'orange', 'green', 'yellow']
        for color in range(len(colors)):
            for row in range(2):
                for col in range(BRICKS_PER_ROW):
                    brick = Brick(colors[color], color * 2 + row, col)
                    self.all_bricks.append(brick)

    def start_game(self):
        while True:
            time.sleep(self.ball.move_speed)
            self.screen.update()
            self.ball.move()
            # Detect paddle collision
            if self.ball.is_collide_top_bot(self.paddle):
                self.ball.y_bounce()
            # Detect brick collision
            for brick in self.all_bricks:
                if self.ball.distance(brick) <= BRICK_WIDTH / 2 + BALL_SIZE:
                    if self.ball.is_collide_left_right(brick):
                        brick.destroy()
                        self.ball.x_bounce()
                    elif self.ball.is_collide_top_bot(brick):
                        brick.destroy()
                        self.all_bricks.remove(brick)
                        self.ball.y_bounce()

            # Detect side wall collision
            if self.ball.xcor() > SCREEN_RIGHT - BALL_SIZE or self.ball.xcor() < SCREEN_LEFT + BALL_SIZE:
                self.ball.x_bounce()
            # Detect top wall collision
            if self.ball.ycor() > SCREEN_TOP - BALL_SIZE:
                self.ball.y_bounce()
            # Detect bottom wall collision (lose ball)
            if self.ball.ycor() < SCREEN_BOTTOM:
                print('game over')
                break
                # scoreboard.increase_score(side)
                match_is_on = False


app = Breakout()
