from copy import copy
from random import randint, choice
from .Ball import *
from .Point import *


class Field:
    BORDER_THICKNESS = 7

    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: float, rely: float,
        # relwidth: float, relheight: float,
        # title: tkinter.Label, canvas: tkinter.Canvas
        # ball_ids: dict, balls: list, active: bool
        # ball_collisions: set, collision_blacklist: set

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.ball_ids = dict()
        self.ball_collisions = set()
        self.collision_blacklist = set()
        self.active = False
        self.title = None
        self.canvas = None
        self.balls = list()

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
        self.canvas.delete('all')
        max_count = state['count']['min'] + state['count']['value'] * (
                state['count']['max'] - state['count']['min']) // 100
        max_size = state['size']['min'] + state['size']['value'] * (
                state['size']['max'] - state['size']['min']) // 100
        max_velocity = state['velocity']['min'] + state['velocity']['value'] * (
                state['velocity']['max'] - state['velocity']['min']) // 100
        k = state['vector\nscale']['min'] + (state['vector\nscale']['max'] - state['vector\nscale']['min']) * \
            state['vector\nscale']['value'] // 100
        count = randint(state['count']['min'], max_count)
        for _ in range(count):
            size = randint(state['size']['min'], max_size)
            velocity_x = randint(state['velocity']['min'], max_velocity) * choice([-1, 1])
            velocity_y = randint(state['velocity']['min'], max_velocity) * choice([-1, 1])
            self.balls.append(Ball(self, Point(randint(size + self.BORDER_THICKNESS + 1,
                                                       self.canvas.winfo_width() - size - self.BORDER_THICKNESS - 1),
                                               randint(size + self.BORDER_THICKNESS + 1,
                                                       self.canvas.winfo_height() - size - self.BORDER_THICKNESS - 1)),
                                   size, 1, Point(velocity_x, velocity_y), 'red', k))
        if not self.active:
            self.update()
            self.active = True

    def update(self):
        self.collision_blacklist = copy(self.ball_collisions)
        self.ball_collisions.clear()
        for ball in self.balls:
            ball.move(1 / self.window.app.FPS)
        for collision in self.ball_collisions:
            if collision in self.collision_blacklist:
                continue
            collide_balls(collision[0], collision[1])
        self.canvas.after(1000 // self.window.app.FPS, self.update)
