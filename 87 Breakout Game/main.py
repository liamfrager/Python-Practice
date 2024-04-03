from settings import *
from turtle import Screen, mode
from scoreboard import Scoreboard
from border import Border
from bricks import Bricks, Brick
from paddle import Paddle
from ball import Ball
import time
from pygame import mixer


mode('logo')


class Breakout:
    def __init__(self):
        # Screen
        self.screen = Screen()
        self.screen.title('Breakout')
        self.screen.setup(
            width=SCREEN_WIDTH + BRICK_WIDTH,
            height=SCREEN_HEIGHT + BRICK_WIDTH
        )
        self.screen.bgcolor('black')
        self.screen.tracer(0)
        self.screen.listen()
        self.screen.getcanvas().config(cursor="none")
        self.is_paused = False
        # Sounds
        mixer.init()
        self.new_game_sound = mixer.Sound('sfx/new_game.ogg')
        self.low_sound = mixer.Sound('sfx/low.ogg')
        self.high_sound = mixer.Sound('sfx/high.ogg')
        self.lose_sound = mixer.Sound('sfx/lose.ogg')
        # Scoreboard
        self.scoreboard = Scoreboard()
        self.border = Border()
        # Bricks
        self.bricks = Bricks()
        # Paddle
        self.paddle = Paddle()
        # Ball
        self.ball = Ball()
        # Start Game
        self.screen.update()
        self.screen.onkeypress(self.start_game, 'space')
        self.screen.mainloop()

    def follow_cursor(self, bool):
        def onmove(self, fun, add=None):
            def eventfun(event):
                fun(self.cv.canvasx(event.x) / self.xscale, -
                    self.cv.canvasy(event.y) / self.yscale)
            self.cv.bind('<Motion>', eventfun, add)
        onmove(self.screen, self.paddle.follow_cursor if bool else None)

    def start_game(self):
        self.new_game_sound.play()
        self.screen.onkeypress(self.pause, 'space')
        # Init paddle controls
        self.screen.onkeypress(self.paddle.right, 'Right')
        self.screen.onkeypress(self.paddle.left, 'Left')
        self.follow_cursor(True)
        # Reset components
        self.bricks.bricks_broken = 0
        self.scoreboard.to_zero()
        while True:
            self.screen.update()
            if not self.is_paused:
                time.sleep(self.ball.move_speed)
                self.ball.move()
                # Detect paddle collision
                if self.ball.ycor() == PADDLE_Y + (PADDLE_HEIGHT + BALL_SIZE) / 2:
                    if self.ball.xcor() >= self.paddle.xcor() - PADDLE_WIDTH / 2 and self.ball.xcor() <= self.paddle.xcor() + PADDLE_WIDTH / 2:
                        self.high_sound.play()
                        self.ball.goto(
                            self.ball.xcor() // BRICK_GAP * BRICK_GAP,
                            self.ball.ycor()
                        )
                        if self.ball.distance(self.paddle) < self.paddle.size / 10:
                            angle = 1
                            self.ball.set_move_speed(.8)
                        elif self.ball.distance(self.paddle) < self.paddle.size / 10 * 3:
                            angle = 2
                            self.ball.set_move_speed(1)
                        else:
                            angle = 4
                            self.ball.set_move_speed(1.5)
                        if self.ball.xcor() > self.paddle.xcor():
                            self.ball.x_move = angle
                        else:
                            self.ball.x_move = -angle
                        self.ball.y_bounce()
                # Detect brick collision
                for brick in self.bricks.all():
                    if self.ball.distance(brick) <= BRICK_WIDTH:
                        if self.detect_brick_collision(brick):
                            self.high_sound.play()
                            self.on_brick_destroy(brick)
                # Detect side wall collision
                if self.ball.xcor() >= SCREEN_RIGHT - BALL_SIZE or self.ball.xcor() <= SCREEN_LEFT + BALL_SIZE:
                    self.low_sound.play()
                    self.ball.x_bounce()

                # Detect top wall collision
                if self.ball.ycor() > SCREEN_TOP - BALL_SIZE:
                    if not self.ball.has_hit_top_wall:
                        self.ball.has_hit_top_wall = True
                        self.paddle.shrink()
                    self.ball.y_bounce()
                    self.low_sound.play()
                # Detect bottom wall collision (lose ball)
                if self.ball.ycor() < SCREEN_BOTTOM:
                    self.lose_sound.play()
                    if self.ball.has_hit_top_wall:
                        self.paddle.grow()
                        self.ball.has_hit_top_wall = False
                    if not self.ball.get_new_ball():
                        break
                # Detect last brick broken
                if self.bricks.bricks_broken == BRICKS_PER_ROW * NUMBER_OF_ROWS:
                    self.screen.update()
                    break
            else:
                time.sleep(.1)
        # Game Over
        self.scoreboard.game_over(
            win=self.bricks.bricks_broken == BRICKS_PER_ROW * NUMBER_OF_ROWS)
        self.screen.onkeypress(self.new_game, 'space')

    def detect_brick_collision(self, brick: Brick):
        if self.ball.collides_x(brick):
            self.ball.x_bounce()
        elif self.ball.collides_y(brick):
            self.ball.y_bounce()
        else:
            return False
        return True

    def on_brick_destroy(self, brick: Brick):
        self.bricks.destroy(brick)
        self.bricks.bricks_broken += 1
        if self.bricks.bricks_broken == 4:
            self.ball.hit_four = True
        elif self.bricks.bricks_broken == 12:
            self.ball.hit_twelve = True
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

    def pause(self):
        if self.is_paused:
            self.follow_cursor(True)
            self.scoreboard.update_score()
            self.screen.getcanvas().config(cursor="none")
        else:
            self.follow_cursor(False)
            self.scoreboard.notify('P A U S E D')
            self.screen.getcanvas().config(cursor="arrow")
        self.is_paused = False if self.is_paused else True

    def new_game(self):
        self.bricks.load_bricks()
        self.ball.clear()
        self.ball.load_balls()
        self.ball.get_new_ball()
        self.paddle.to_starting_position()
        self.start_game()


app = Breakout()

# TODO: Hide cursor
