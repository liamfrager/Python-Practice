import turtle as t

trtl = t.Turtle()


def on_w():
    trtl.fd(10)


def on_s():
    trtl.bk(10)


def on_a():
    trtl.lt(10)


def on_d():
    trtl.rt(10)


def on_c():
    trtl.clear()
    trtl.teleport(0, 0)
    trtl.setheading(0)


screen = t.Screen()
screen.listen()
screen.onkey(on_w, "w")
screen.onkey(on_s, "s")
screen.onkey(on_a, "a")
screen.onkey(on_d, "d")
screen.onkey(on_c, "c")

screen.exitonclick()
