from copy import copy
from random import randint, choice
from .Ball import *
from .Point import *
from sortedcontainers import SortedList
from enum import Enum
from itertools import combinations as combs


def quadratic_solve(a, b, c):
    d = b * b - 4 * a * c
    if d > 0:
        return (-b - sqrt(d)) / (2 * a), (-b + sqrt(d)) / (2 * a)
    elif d == 0:
        return -b / (2 * a),
    else:
        return ()


def collision_time(a, b):
    if isinstance(a, Wall):
        a, b = b, a
    if isinstance(b, Wall):
        if b == Wall.UP:
            if a.velocity.y >= 0:
                return None
            return abs((a.pos.y - a.radius) / a.velocity.y)
        elif b == Wall.DOWN:
            if a.velocity.y <= 0:
                return None
            return abs((a.field.canvas.winfo_height() - a.pos.y - a.radius) / a.velocity.y)
        elif b == Wall.LEFT:
            if a.velocity.x >= 0:
                return None
            return abs((a.pos.x - a.radius) / a.velocity.x)
        elif b == Wall.RIGHT:
            if a.velocity.x <= 0:
                return None
            return abs((a.field.canvas.winfo_width() - a.pos.x - a.radius) / a.velocity.x)
    elif isinstance(b, Ball):
        res = quadratic_solve((a.velocity - b.velocity) * (a.velocity - b.velocity),
                              2 * (a.pos - b.pos) * (a.velocity - b.velocity),
                              (a.pos - b.pos) * (a.pos - b.pos) - (a.radius + b.radius) ** 2)
        if len(res) == 2:
            return res[0]
        else:
            return None


def collide_balls(a, b):
    a.velocity, b.velocity = (a.velocity - (2 * b.mass / (a.mass + b.mass)) * (
            (a.velocity - b.velocity) * (a.pos - b.pos)) / abs(
        a.pos - b.pos) ** 2 * (a.pos - b.pos)), \
                             (b.velocity - (2 * a.mass / (a.mass + b.mass)) * (
                                     (b.velocity - a.velocity) * (b.pos - a.pos)) / abs(
                                 b.pos - a.pos) ** 2 * (b.pos - a.pos))


def collide_with_wall(ball, wall):
    if wall == Wall.UP or wall == Wall.DOWN:
        ball.velocity.y *= -1
    elif wall == Wall.LEFT or wall == Wall.RIGHT:
        ball.velocity.x *= -1


class Wall(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Event:
    def __init__(self, a, b, offset):
        if isinstance(a, Wall):
            a, b = b, a
        self.ball = a
        self.obstacle = b
        self.time = collision_time(a, b) + offset

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time

    def __hash__(self):
        return hash((self.ball, self.obstacle, self.time))


# @dataclass(frozen=True, eq=True, order=True)
# class Event:
#     time: float
#     ball: Ball
#     obstacle: Union[Ball, Wall]


class Field:
    BORDER_THICKNESS = 7

    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: float, rely: float,
        # relwidth: float, relheight: float,
        # title: tkinter.Label, canvas: tkinter.Canvas,
        # ball_ids: dict, balls: list, active: bool,
        # ball_collisions: set, collision_blacklist: set,
        # events: SortedList<Event>, timer: float

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.ball_ids = dict()
        # self.ball_collisions = set()
        # self.collision_blacklist = set()
        self.active = False
        self.title = None
        self.canvas = None
        self.balls = list()
        self.events = SortedList()
        self.timer = 0

        self.init_title()
        self.init_canvas()

    def init_title(self):
        self.title = tkinter.Label(self.window.app.master, text='Field', justify=tkinter.CENTER,
                                   bg=self.window.BG_COLOR,
                                   fg=self.window.FG_COLOR, font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05 * self.relheight)

    def init_canvas(self):
        self.canvas = tkinter.Canvas(self.window.app.master, bg=self.window.BG_COLOR,
                                     width=self.relwidth * self.window.WINDOW_WIDTH,
                                     height=0.95 * self.relheight * self.window.WINDOW_HEIGHT,
                                     highlightthickness=self.BORDER_THICKNESS,
                                     highlightcolor=self.window.FG_COLOR)
        self.canvas.place(relx=self.relx, rely=self.rely + 0.05 * self.relheight, relwidth=self.relwidth,
                          relheight=0.95 * self.relheight)

    def generate(self, state):
        self.timer = 0
        self.events.clear()
        self.canvas.delete('all')
        count = state['count']['min'] + state['count']['value'] * (
                state['count']['max'] - state['count']['min']) // 100
        max_size = state['size']['min'] + state['size']['value'] * (
                state['size']['max'] - state['size']['min']) // 100
        max_velocity = state['velocity']['min'] + state['velocity']['value'] * (
                state['velocity']['max'] - state['velocity']['min']) // 100
        k = state['vector scale']['min'] + (state['vector scale']['max'] - state['vector scale']['min']) * \
            state['vector scale']['value'] / 100

        density = dict()
        for color in ["red", "blue", "green"]:
            density[color] = state[f'{color} density']['min'] + (
                    state[f'{color} density']['max'] - state[f'{color} density']['min']) * \
                             state[f'{color} density']['value']
        self.balls.clear()
        for _ in range(count):
            color = choice(["green", "red", "blue"])

            size = randint(state['size']['min'], max_size)
            velocity_x = randint(state['velocity']['min'], max_velocity) * choice([-1, 1])
            velocity_y = randint(state['velocity']['min'], max_velocity) * choice([-1, 1])
            self.balls.append(Ball(self, Point(randint(size + self.BORDER_THICKNESS + 1,
                                                       self.canvas.winfo_width() - size - self.BORDER_THICKNESS - 1),
                                               randint(size + self.BORDER_THICKNESS + 1,
                                                       self.canvas.winfo_height() - size - self.BORDER_THICKNESS - 1)),
                                   size, density[color], Point(velocity_x, velocity_y), color, k))
        for (b1, b2) in combs(self.balls, 2):
            if b2 == b1:
                continue
            if collision_time(b1, b2) is not None:
                self.events.add(Event(b1, b2, self.timer))
        for b1 in self.balls:
            for w in [Wall.UP, Wall.RIGHT, Wall.DOWN, Wall.LEFT]:
                if collision_time(b1, w) is not None:
                    self.events.add(Event(b1, w, self.timer))

        if not self.active:
            self.update()
            self.active = True

    def update(self):
        if self.events[0].time - self.timer > 1 / self.window.app.FPS:
            for ball in self.balls:
                ball.move(1 / self.window.app.FPS)
            self.timer += 1 / self.window.app.FPS
            self.canvas.after(1000 // self.window.app.FPS, self.update)
        else:
            event = self.events.pop(0)
            tdelta = event.time - self.timer
            for ball in self.balls:
                ball.move(tdelta)
            self.timer += tdelta
            self.events = SortedList(filter(lambda x: x.ball != event.ball and x.obstacle != event.ball, self.events))
            
            if isinstance(event.obstacle, Ball):
                collide_balls(event.ball, event.obstacle)
                self.events = SortedList(
                    filter(lambda x: x.ball != event.obstacle and x.obstacle != event.obstacle, self.events))
                for b2 in self.balls:
                    if event.ball == b2 or event.obstacle == b2:
                        continue
                    if collision_time(event.obstacle, b2) is not None:
                        self.events.add(Event(event.obstacle, b2, self.timer))
            elif isinstance(event.obstacle, Wall):
                collide_with_wall(event.ball, event.obstacle)
            for b2 in self.balls:
                if event.ball == b2:
                    continue
                if collision_time(event.ball, b2) is not None:
                    self.events.add(Event(event.ball, b2, self.timer))
            self.canvas.after(int(tdelta * 1000), self.update)

        # self.timer += 1 / self.window.app.FPS
        # while self.events[0].time < self.timer:
        #     event = self.events.pop(0)
        #     event.ball.move(event.time - self.timer + 1 / self.window.app.FPS)
        #     if isinstance(event.obstacle, Ball):
        #         event.obstacle.move(event.time - self.timer + 1 / self.window.app.FPS)
        #         collide_balls(event.ball, event.obstacle)
        #         event.obstacle.move(self.timer - event.time)
        #     elif isinstance(event.obstacle, Wall):
        #         collide_with_wall(event.ball, event.obstacle)
        #     event.ball.move(self.timer - event.time)
        #
        # self.collision_blacklist = copy(self.ball_collisions)
        # self.ball_collisions.clear()
        # for ball in self.balls:
        #     ball.move(1 / self.window.app.FPS)
        # for collision in self.ball_collisions:
        #     if collision in self.collision_blacklist:
        #         continue
        #     collide_balls(collision[0], collision[1])
        # self.canvas.after(1000 // self.window.app.FPS, self.update)
