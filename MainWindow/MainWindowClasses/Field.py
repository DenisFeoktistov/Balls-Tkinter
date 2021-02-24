import tkinter
from copy import copy
from random import randint, choice
from .Ball import *
from .Point import *


class Field:
    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: real, rely: real,
        # relwidth: real, relheight: real,
        # title: tkinter.Label, canvas: tkinter.Canvas
        # ball_ids: dictionary, balls: list, active: bool
        # ball_collisions: set, collision_blacklist: set

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.ball_ids = {}
        self.ball_collisions = set()
        self.collision_blacklist = set()
        self.active = False

        self.init_title()
        self.init_canvas()

    def init_title(self):
        self.title = tkinter.Label(self.window.app.master, text='Field', justify=tkinter.CENTER, bg=self.window.COLOR,
                                   fg='#000000', font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05 * self.relheight)

    def init_canvas(self):
        self.canvas = tkinter.Canvas(self.window.app.master, bg=self.window.COLOR,
                                     width=self.relwidth * self.window.WINDOW_WIDTH,
                                     height=0.95 * self.relheight * self.window.WINDOW_HEIGHT, highlightthickness=7,
                                     highlightcolor="#000000")
        self.canvas.place(relx=self.relx, rely=self.rely + 0.05 * self.relheight, relwidth=self.relwidth,
                          relheight=0.95 * self.relheight)
        # self.canvas.create_oval((100, 100), (300, 300), fill='green')

    def generate(self, state):
        self.canvas.delete('all')
        max_count = state['count']['min'] + state['count']['value'] * (
                state['count']['max'] - state['count']['min']) // 100
        max_size = state['size']['min'] + state['size']['value'] * (
                state['size']['max'] - state['size']['min']) // 100
        max_velocity = state['velocity']['min'] + state['velocity']['value'] * (
                state['velocity']['max'] - state['velocity']['min']) // 100
        count = randint(state['count']['min'], max_count)
        self.balls = list()
        for _ in range(count):
            size = randint(state['size']['min'], max_size)
            velocity_x = randint(state['velocity']['min'], max_velocity) * choice([-1, 1])
            velocity_y = randint(state['velocity']['min'], max_velocity) * choice([-1, 1])
            self.balls.append(Ball(self, Point(randint(size + 8, self.canvas.winfo_width() - size - 8),
                                               randint(size + 8, self.canvas.winfo_height() - size - 8)),
                                   size, 1, Point(velocity_x, velocity_y), 'red'))
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
