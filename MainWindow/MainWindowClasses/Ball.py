import tkinter


class VelocityVector:
    # k: float, ball: Ball, end: Point, arrow: int
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
    def __init__(self, field, pos, radius, density, velocity, color, k):
        # field: Field, pos: Point, radius: int, density: float,
        # velocity: Point, color: Color, mass: float
        # ignore_horizontal: bool, ignore_vertical: bool, oval: int, vector: VelocityVector
        self.field = field
        self.pos = pos
        self.radius = radius
        self.density = density
        self.velocity = velocity
        self.color = color
        self.mass = density * (radius ** 2)
        self.oval = field.canvas.create_oval((self.pos.x - self.radius, self.pos.y - self.radius), (
            self.pos.x + self.radius, self.pos.y + self.radius), fill=self.color)

        if self.field.window.app.DEBUG_ARROWS:
            self.vector = VelocityVector(self, k)

    def move(self, time):
        self.pos += self.velocity * time
        self.field.canvas.coords(self.oval, self.pos.x - self.radius, self.pos.y - self.radius,
                                 self.pos.x + self.radius, self.pos.y + self.radius)
        if self.field.window.app.DEBUG_ARROWS:
            self.vector.update()

    def __hash__(self):
        return hash((self.pos, self.radius, self.velocity))


