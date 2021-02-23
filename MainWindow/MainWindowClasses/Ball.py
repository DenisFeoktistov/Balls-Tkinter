from Field import Field
from Point import Point


class Ball:
    def __init__(self, field, pos, radius, density, velocity, color):
        # field: Field, pos: Point, radius: int, density: real,
        # velocity: Point, color: Color, mass: real
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

    def move(self, time):
        self.pos += self.velocity * time
        self.field.canvas.coords(self.oval, (self.pos.x - self.radius, self.pos.y - self.radius), (
            self.pos.x + self.radius, self.pos.y + self.radius))
        self.check_collisions()

    def collide_wall_vertical(self):
        self.velocity.x *= -1

    def collide_wall_horizontal(self):
        self.velocity.y *= -1

    def check_collisions(self):
        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > self.field.canvas.width:
            self.collide_wall_vertical()
        if self.pos.y - self.radius < 0 or self.pos.y + self.radius > self.field.canvas.height:
            self.collide_wall_horizontal()
        overlapping = self.field.canvas.find_overlapping((self.pos.x - self.radius, self.pos.y - self.radius), (
            self.pos.x + self.radius, self.pos.y + self.radius))
        for obj in overlapping:
            other = self.field.ball_ids[obj]
            if ball_overlap(self, other):
                if self.oval < other.oval:
                    self.field.ball_collisions.add((self, other))
                else:
                    self.field.ball_collisions.add((other, self))


def ball_overlap(a, b):
    return (a.pos - b.pos).absv() <= (a.radius + b.radius)


def collide_balls(a, b):
    a.velocity -= (2 * b.mass / (a.mass + b.mass)) * ((a.velocity - b.velocity) * (a.pos - b.pos)) / (
            a.pos - b.pos).absv() ** 2 * (a.pos - b.pos)
    b.velocity -= (2 * a.mass / (a.mass + b.mass)) * ((b.velocity - a.velocity) * (b.pos - a.pos)) / (
            b.pos - a.pos).absv() ** 2 * (b.pos - a.pos)
