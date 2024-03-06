from turtle import Turtle
import random

CAR_START_SPEED = 5
CAR_INCREASE_SPEED_AMOUNT = 5


class Cars():
    def __init__(self):
        self.all_cars = []
        self.car_speed = CAR_START_SPEED

    def make_new_car(self):
        new_car = Turtle()
        new_car.penup()
        new_car.color(self.random_color())
        new_car.shape('square')
        new_car.shapesize(2, 1)
        new_car.goto(320, round(random.randint(-200, 200) / 30) * 30)
        self.all_cars.append(new_car)

    def random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def move_cars(self):
        for car in self.all_cars:
            car.setx(car.xcor() - self.car_speed)

    def accelerate(self):
        self.car_speed += CAR_INCREASE_SPEED_AMOUNT

    def have_squished(self, turtle):
        for car in self.all_cars:
            turtle_y = turtle.ycor()
            car_x = car.xcor()
            car_y = car.ycor()

            squish_x = car_x > -30 and car_x < 30
            squish_y = turtle_y > car_y - 30 and turtle_y < car_y + 20

            if squish_x and squish_y:
                return True
        return False
