import tkinter


class ParamWidget:
    def __init__(self, settings, param, relx, rely, relwidth, relheight):
        self.settings = settings
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.param = param

        self.button_up = tkinter.Button(master=self.settings.window.app.master, bg=self.settings.window.COLOR, text="▲",
                                        font="sans 30", fg="#000000", bd=0)
        self.button_down = tkinter.Button(master=self.settings.window.app.master, bg=self.settings.window.COLOR,
                                          text="▼", font="sans 30", fg="#000000", bd=0)

        self.button_up.place(relx=self.relx + self.relwidth * 0.8, rely=self.rely + self.relheight * 0.1,
                             relwidth=self.relwidth * 0.2,
                             relheight=0.3 * self.relheight)
        self.button_down.place(relx=self.relx + self.relwidth * 0.8, rely=self.rely + self.relheight * 0.6,
                               relwidth=self.relwidth * 0.2,
                               relheight=0.3 * self.relheight)

        self.param_label = tkinter.Label(master=self.settings.window.app.master, bg=self.settings.window.COLOR,
                                         text=self.param, font="sans 30")
        self.param_label.place(relx=self.relx, rely=self.rely + self.relheight * 0.1,
                               relwidth=self.relwidth * 0.6,
                               relheight=0.8 * self.relheight)

        self.value_label = tkinter.Label(master=self.settings.window.app.master, bg=self.settings.window.COLOR,
                                         text=0, font="sans 40")
        self.value_label.place(relx=self.relx + self.relwidth * 0.6, rely=self.rely + self.relheight * 0.1,
                               relwidth=self.relwidth * 0.2,
                               relheight=0.8 * self.relheight)


class Settings:
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

        params = ["tessdwswsdt1", "test2", "test3", "test4", "test5"]

        self.widgets = list()
        for i, param in enumerate(params):
            self.widgets.append(ParamWidget(relx=self.relx,
                                            rely=self.rely + self.relheight * 0.1 + self.relheight * 0.9 * i / len(
                                                params),
                                            relwidth=self.relwidth,
                                            relheight=self.relheight * 0.8 / len(params),
                                            param=param, settings=self))

    def init_title(self):
        self.title = tkinter.Label(self.window.app.master, text='Settings', justify=tkinter.CENTER,
                                   bg=self.window.COLOR, fg='#000000', font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05 * self.relheight)
