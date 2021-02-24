from .Point import Point
from sys import float_info
import tkinter


class VelocityVector:
    def __init__(self, ball, k):
        self.k = k
        self.ball = ball
        self.end = self.ball.pos + self.ball.velocity * self.k
        self.arrow = self.ball.field.canvas.create_line(self.ball.pos.x, self.ball.pos.y, self.end.x, self.end.y,
                                                        arrow=tkinter.LAST)

    def update(self):
        self.end = self.ball.pos + self.ball.velocity * self.k
        self.ball.field.canvas.coords(self.arrow, self.ball.pos.x, self.ball.pos.y, self.end.x, self.end.y)


class Ball:
    EPS = float_info.epsilon

    def __init__(self, field, pos, radius, density, velocity, color, k):
        # field: Field, pos: Point, radius: int, density: real,
        # velocity: Point, color: Color, mass: real
        # ignore_horizontal: bool, ignore_vertical: bool
        self.field = field
        self.pos = pos
        self.radius = radius
        self.density = density
        self.velocity = velocity
        self.color = color
        self.mass = density * (radius ** 2)
        self.oval = field.canvas.create_oval((self.pos.x - self.radius, self.pos.y - self.radius), (
            self.pos.x + self.radius, self.pos.y + self.radius), fill=self.color)
        field.ball_ids[self.oval] = self
        self.ignore_horizontal = False
        self.ignore_vertical = False

        self.vector = VelocityVector(self, k)

    def move(self, time):
        self.pos += self.velocity * time
        self.field.canvas.coords(self.oval, self.pos.x - self.radius, self.pos.y - self.radius,
                                 self.pos.x + self.radius, self.pos.y + self.radius)
        self.check_collisions()
        self.vector.update()

    def collide_wall_vertical(self, num):
        if num:
            self.field.canvas.coords(self.oval, 7, self.pos.y - self.radius, 7 + 2 * self.radius,
                                     self.pos.y + self.radius)
        else:
            self.field.canvas.coords(self.oval, self.field.canvas.winfo_width() - 7, self.pos.y - self.radius,
                                     self.field.canvas.winfo_width() - 7 - 2 * self.radius, self.pos.y + self.radius)
        self.velocity.x *= -1

    def collide_wall_horizontal(self, num):
        if num:
            self.field.canvas.coords(self.oval, self.pos.x - self.radius, 7, self.pos.x + self.radius,
                                     7 + 2 * self.radius)
        else:
            self.field.canvas.coords(self.oval, self.pos.x - self.radius, self.field.canvas.winfo_height() - 7,
                                     self.pos.x + self.radius, self.field.canvas.winfo_height() - 7 - 2 * self.radius)

        self.velocity.y *= -1

    def check_collisions(self):
        if self.pos.x - self.radius - 7 < -self.EPS or self.pos.x + self.radius - self.field.canvas.winfo_width() + 7 > self.EPS:
            num = self.pos.x - self.radius - 7 < -self.EPS
            if self.ignore_vertical:
                self.ignore_vertical = False
            else:
                self.collide_wall_vertical(num)
                self.ignore_vertical = True
        if self.pos.y - self.radius - 7 < -self.EPS or self.pos.y + self.radius - self.field.canvas.winfo_height() + 7 > self.EPS:
            num = self.pos.y - self.radius - 7 < -self.EPS
            if self.ignore_horizontal:
                self.ignore_horizontal = False
            else:
                self.collide_wall_horizontal(num)
                self.ignore_horizontal = True
        overlapping = self.field.canvas.find_overlapping(self.pos.x - self.radius, self.pos.y - self.radius,
                                                         self.pos.x + self.radius, self.pos.y + self.radius)
        for obj in overlapping:
            if obj == self.oval or obj not in self.field.ball_ids:
                continue
            other = self.field.ball_ids[obj]
            if ball_overlap(self, other):
                if self.oval < other.oval:
                    self.field.ball_collisions.add((self, other))
                else:
                    self.field.ball_collisions.add((other, self))


def ball_overlap(a, b):
    return abs(a.pos - b.pos) - (a.radius + b.radius) <= Ball.EPS


def collide_balls(a, b):
    a.velocity, b.velocity = (a.velocity - (2 * b.mass / (a.mass + b.mass)) * (
            (a.velocity - b.velocity) * (a.pos - b.pos)) / abs(
        a.pos - b.pos) ** 2 * (a.pos - b.pos)), \
                             (b.velocity - (2 * a.mass / (a.mass + b.mass)) * (
                                     (b.velocity - a.velocity) * (b.pos - a.pos)) / abs(
                                 b.pos - a.pos) ** 2 * (b.pos - a.pos))
