import turtle as t

MOVE_DISTANCE = 20
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()

    def create_snake(self):
        self.heading = (1, 0)
        for i in range(3):
            self.extend((0 - (20 * i), 0))

    def move(self):
        x = self.segments[0].xcor() + MOVE_DISTANCE * self.heading[0]
        y = self.segments[0].ycor() + MOVE_DISTANCE * self.heading[1]
        self.segments[-1].teleport(x, y)
        self.segments = self.segments[-1:] + self.segments[:-1]
        self.head = self.segments[0]

    def head_n(self):
        self.heading = NORTH if self.heading != SOUTH else SOUTH

    def head_s(self):
        self.heading = SOUTH if self.heading != NORTH else NORTH

    def head_e(self):
        self.heading = EAST if self.heading != WEST else WEST

    def head_w(self):
        self.heading = WEST if self.heading != EAST else EAST

    def extend(self, pos):
        s = t.Turtle(shape='square')
        s.color('white')
        s.pu()
        s.goto(pos)
        self.segments.append(s)

    def eat(self):
        self.extend((self.segments[-1].xcor(), self.segments[-1].ycor()))

    def reset(self):
        for s in self.segments:
            s.hideturtle()
        self.segments.clear()
        self.create_snake()
