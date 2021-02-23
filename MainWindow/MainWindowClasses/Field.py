import tkinter


class Field:
    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: real, rely: real,
        # relwidth: real, relheight: real,
        # title: tkinter.Label, canvas: tkinter.Canvas
        # ball_ids: dictionary

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.ball_ids = {}
        self.ball_collisions = set()

        self.init_title()
        self.init_canvas()

    def init_title(self):
        self.title = tkinter.Label(self.window.app.master, text='Field', justify=tkinter.CENTER, bg=self.window.COLOR, fg='#000000', font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05*self.relheight)

    def init_canvas(self):
        self.canvas = tkinter.Canvas(self.window.app.master, bg=self.window.COLOR, width=self.relwidth*self.window.WINDOW_WIDTH, height=0.95*self.relheight*self.window.WINDOW_HEIGHT, highlightthickness=7, highlightcolor="#000000")
        self.canvas.place(relx=self.relx, rely=self.rely+0.05*self.relheight, relwidth=self.relwidth, relheight=0.95*self.relheight)
        #self.canvas.create_oval((100, 100), (300, 300), fill='green')