import turtle as turt
import random as rand
import colorgram


t = turt.Turtle()
turt.colormode(255)
t.hideturtle()
t.speed(0)


def random_color():
    r = rand.randint(0, 255)
    g = rand.randint(0, 255)
    b = rand.randint(0, 255)
    return (r, g, b)

# # Polygon Cycle
# for i in range(3, 10):
#     t.pencolor(random_color())
#     for _ in range(i):
#         t.right(360/i)
#         t.forward(100)


# # Random Walk
# for i in range(1000):
#     t.width(10)
#     t.pencolor(random_color())
#     t.forward(30)
#     t.right(90 * rand.randint(0, 3))

# # Circle Of Circles
# x = 5
# for i in range(int(360 / x)):
#     t.pencolor(random_color())
#     t.setheading(i * x)
#     t.circle(100)

# Hirst Spot Painting
colors = colorgram.extract(
    '/Users/liamfrager/Documents/💾/{ code }/udemy/python/18 Turtle/hirst-spot-painting.jpg', 28)
color_palette = []
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
    if r > 220 and g > 220 and b > 220:
        pass
    else:
        color_palette.append((r, g, b))

color_i = 0
for i in range(5):
    for j in range(5):
        t.teleport(-80 + (j * 50), 80 - (i * 50))
        t.dot(20, color_palette[color_i])
        color_i += 1

screen = turt.Screen()
screen.exitonclick()
