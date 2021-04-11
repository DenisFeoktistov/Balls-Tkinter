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
        field.ball_ids[self.oval] = self
        self.ignore_horizontal = False
        self.ignore_vertical = False

        self.vector = VelocityVector(self, k)

    def move(self, time):
        self.check_collisions()
        self.pos += self.velocity * time
        self.field.canvas.coords(self.oval, self.pos.x - self.radius, self.pos.y - self.radius,
                                 self.pos.x + self.radius, self.pos.y + self.radius)
        self.vector.update()

    # def collide_wall_vertical(self, num):
    #     if num:
    #         self.pos.x = self.field.BORDER_THICKNESS + self.radius + 1
    #         # self.field.canvas.coords(self.oval, self.field.BORDER_THICKNESS + 1, self.pos.y - self.radius,
    #         #                         self.field.BORDER_THICKNESS + 2 * self.radius + 1,
    #         #                         self.pos.y + self.radius)
    #     else:
    #         self.pos.x = self.field.canvas.winfo_width() - self.field.BORDER_THICKNESS - self.radius - 1
    #         # self.field.canvas.coords(self.oval, self.field.canvas.winfo_width() - self.field.BORDER_THICKNESS - 1,
    #         #                          self.pos.y - self.radius,
    #         #                          self.field.canvas.winfo_width() -
    #         #                          self.field.BORDER_THICKNESS - 2 * self.radius - 1,
    #         #                          self.pos.y + self.radius)
    #     self.velocity.x *= -1
    #
    # def collide_wall_horizontal(self, num):
    #     if num:
    #         self.pos.y = self.field.BORDER_THICKNESS + self.radius + 1
    #         # self.field.canvas.coords(self.oval, self.pos.x - self.radius, self.field.BORDER_THICKNESS + 1,
    #         #                          self.pos.x + self.radius,
    #         #                          self.field.BORDER_THICKNESS + 2 * self.radius + 1)
    #     else:
    #         self.pos.y = self.field.canvas.winfo_height() - self.field.BORDER_THICKNESS - self.radius - 1
    #         # self.field.canvas.coords(self.oval, self.pos.x - self.radius,
    #         #                          self.field.canvas.winfo_height() - self.field.BORDER_THICKNESS - 1,
    #         #                          self.pos.x + self.radius,
    #         #                          self.field.canvas.winfo_height() -
    #         #                          self.field.BORDER_THICKNESS - 2 * self.radius - 1)
    #
    #     self.velocity.y *= -1
    #
    # def check_collisions(self):
    #     if self.pos.x - self.radius - self.field.BORDER_THICKNESS < 0 or \
    #             self.pos.x + self.radius - self.field.canvas.winfo_width() + self.field.BORDER_THICKNESS > 0:
    #         num = self.pos.x - self.radius - self.field.BORDER_THICKNESS < 0
    #         if self.ignore_vertical:
    #             self.ignore_vertical = False
    #         else:
    #             self.collide_wall_vertical(num)
    #             self.ignore_vertical = True
    #     if self.pos.y - self.radius - self.field.BORDER_THICKNESS < 0 or \
    #             self.pos.y + self.radius - self.field.canvas.winfo_height() + self.field.BORDER_THICKNESS > 0:
    #         num = self.pos.y - self.radius - self.field.BORDER_THICKNESS < 0
    #         if self.ignore_horizontal:
    #             self.ignore_horizontal = False
    #         else:
    #             self.collide_wall_horizontal(num)
    #             self.ignore_horizontal = True
    #     overlapping = self.field.canvas.find_overlapping(self.pos.x - self.radius, self.pos.y - self.radius,
    #                                                      self.pos.x + self.radius, self.pos.y + self.radius)
    #     for obj in overlapping:
    #         if obj == self.oval or obj not in self.field.ball_ids:
    #             continue
    #         other = self.field.ball_ids[obj]
    #         if ball_overlap(self, other):
    #             if self.oval < other.oval:
    #                 self.field.ball_collisions.add((self, other))
    #             else:
    #                 self.field.ball_collisions.add((other, self))

    def check_collisions(self):
        pass

    def __hash__(self):
        return hash((self.pos, self.radius, self.velocity))


def ball_overlap(a, b):
    return abs(a.pos - b.pos) - (a.radius + b.radius) <= 0


