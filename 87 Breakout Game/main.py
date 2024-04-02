from settings import *
from turtle import Turtle, Screen, mode
from scoreboard import Scoreboard
from border import Border
from brick import Brick
from paddle import Paddle
from ball import Ball
import time

mode('logo')


class Breakout:
    def __init__(self):
        # Screen
        self.screen = Screen()
        self.screen.title('Breakout')
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor('black')
        self.screen.tracer(0)
        self.screen.listen()
        # Scoreboard
        self.scoreboard = Scoreboard()
        self.border = Border()
        # Bricks
        self.all_bricks: list[Brick] = []
        self.load_bricks()
        self.bricks_broken = 0
        # Paddle
        self.paddle = Paddle()
        self.screen.onkeypress(self.paddle.right, 'Right')
        self.screen.onkeypress(self.paddle.left, 'Left')

        def onmove(self, fun, add=None):
            """
            Bind fun to mouse-motion event on screen.

            Arguments:
            self -- the singular screen instance
            fun  -- a function with two arguments, the coordinates
                of the mouse cursor on the canvas.

            Example:

            >>> onmove(turtle.Screen(), lambda x, y: print(x, y))
            >>> # Subsequently moving the cursor on the screen will
            >>> # print the cursor position to the console
            >>> screen.onmove(None)
            """
            def eventfun(event):
                fun(self.cv.canvasx(event.x) / self.xscale, -
                    self.cv.canvasy(event.y) / self.yscale)
            self.cv.bind('<Motion>', eventfun, add)
        onmove(self.screen, self.paddle.follow_cursor)
        # Ball
        self.ball = Ball()
        # Other
        self.start_game()

    def start_game(self):
        while True:
            time.sleep(self.ball.move_speed)
            self.screen.update()
            self.ball.move()
            # Detect paddle collision
            if self.ball.is_collide_top_bot(self.paddle):
                if self.ball.distance(self.paddle) < self.paddle.size / 10:
                    angle = 1
                    self.ball.move_speed = BALL_SPEED * self.ball.speed_multiplier * .5
                elif self.ball.distance(self.paddle) < self.paddle.size / 10 * 3:
                    angle = 2
                    self.ball.move_speed = BALL_SPEED * self.ball.speed_multiplier * 1
                else:
                    angle = 4
                    self.ball.move_speed = BALL_SPEED * self.ball.speed_multiplier * 1.5
                self.ball.goto(
                    self.ball.xcor() // BRICK_GAP * BRICK_GAP,
                    self.ball.ycor()
                )
                if self.ball.xcor() > self.paddle.xcor():
                    self.ball.x_move = angle
                else:
                    self.ball.x_move = -angle
                self.ball.y_bounce()
            # Detect brick collision
            for brick in self.all_bricks:
                if self.ball.distance(brick) <= BRICK_WIDTH:
                    if self.detect_brick_collision(brick):
                        self.on_brick_destroy(brick)
            # Detect side wall collision
            if self.ball.xcor() >= SCREEN_RIGHT - BALL_SIZE or self.ball.xcor() <= SCREEN_LEFT + BALL_SIZE:
                self.ball.x_bounce()

            # Detect top wall collision
            if self.ball.ycor() > SCREEN_TOP - BALL_SIZE:
                if not self.ball.has_hit_top_wall:
                    self.ball.has_hit_top_wall = True
                    self.paddle.shrink()
                self.ball.y_bounce()
            # Detect bottom wall collision (lose ball)
            if self.ball.ycor() < SCREEN_BOTTOM and not self.ball.get_new_ball():
                break
        # Game Over
        self.scoreboard.game_over()
        self.screen.onkeypress(self.new_game, 'space')
        self.screen.mainloop()

    def load_bricks(self):
        colors = ['red', 'orange', 'green', 'yellow']
        for color in range(len(colors)):
            for row in range(2):
                for col in range(BRICKS_PER_ROW):
                    brick = Brick(colors[color], color * 2 + row, col)
                    self.all_bricks.append(brick)

    def detect_brick_collision(self, brick: Brick):
        if self.ball.is_collide_left_right(brick):
            self.ball.x_bounce()
        elif self.ball.is_collide_top_bot(brick):
            self.ball.y_bounce()
        else:
            return False
        return True

    def on_brick_destroy(self, brick: Brick):
        brick.destroy()
        self.bricks_broken += 1
        if self.bricks_broken == 4:
            self.ball.hit_four = True
        elif self.bricks_broken == 12:
            self.ball.hit_twelve = True
        self.all_bricks.remove(brick)
        match brick.color()[0]:
            case 'yellow':
                points = 1
            case 'green':
                points = 3
            case 'orange':
                self.ball.hit_orange = True
                points = 5
            case 'red':
                self.ball.hit_red = True
                points = 7
        self.scoreboard.add_points(points)
        self.ball.move_speed = BALL_SPEED * self.ball.speed_multiplier

    def new_game(self):
        self.screen.onkeypress(None, 'space')
        self.ball.clear()
        self.ball.load_balls()
        self.ball.get_new_ball()
        self.load_bricks()
        self.paddle.to_starting_position()
        self.scoreboard.to_zero()
        self.bricks_broken = 0
        self.start_game()


app = Breakout()

# TODO: Add SFX
