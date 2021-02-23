from Field import Field
from Point import Point


class Ball:
    def __init__(self, field, pos, radius, density, velocity):
        # field: Field, pos: Point, radius: int, density: real,
        # velocity: Point, mass: real
        self.field = field
        self.pos = pos
        self.radius = radius
        self.density = density
        self.velocity = velocity
        self.mass = density * (radius ** 2)

    def move(self, time):
        self.pos += self.velocity * time

    def collide_wall_vertical(self):
        self.velocity.x *= -1

    def collide_wall_horizontal(self):
        self.velocity.y *= -1


def collide_balls(a, b):
    a.velocity -= (2 * b.mass / (a.mass + b.mass)) * ((a.velocity - b.velocity) * (a.pos - b.pos)) / (
                a.pos - b.pos).absv() ** 2 * (a.pos - b.pos)
    b.velocity -= (2 * a.mass / (a.mass + b.mass)) * ((b.velocity - a.velocity) * (b.pos - a.pos)) / (
            b.pos - a.pos).absv() ** 2 * (b.pos - a.pos)
