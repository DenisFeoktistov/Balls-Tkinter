import tkinter


class Field:
    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: real, rely: real,
        # relwidth: real, relheight: real,
        # title: tkinter.Label, canvas: tkinter.Canvas

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight

        self.init_title()
        #self.init_canvas()

    def init_title(self):
        self.title = tkinter.Label(self.window.app.master, text='Field', justify=tkinter.CENTER, bg=self.window.COLOR, fg='#000000', font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05*self.relheight)