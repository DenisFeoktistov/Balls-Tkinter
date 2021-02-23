import tkinter
import json


class ParamWidget:
    def __init__(self, settings, param, relx, rely, relwidth, relheight):
        self.settings = settings
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.param = param

        self.button_up = tkinter.Button(master=self.settings.window.app.master, bg=self.settings.window.COLOR, text="▲",
                                        font="sans 30", fg="#000000", highlightbackground=self.settings.window.COLOR,
                                        relief=tkinter.FLAT, overrelief=tkinter.FLAT,
                                        activebackground=self.settings.window.COLOR, activeforeground='#000000', bd=0,
                                        command=self.increase)
        self.button_down = tkinter.Button(master=self.settings.window.app.master, bg=self.settings.window.COLOR,
                                          text="▼", font="sans 30", fg="#000000",
                                          highlightbackground=self.settings.window.COLOR,
                                          relief=tkinter.FLAT, overrelief=tkinter.FLAT,
                                          activebackground=self.settings.window.COLOR, activeforeground='#000000', bd=0,
                                          command=self.decrease)
        self.button_up.place(relx=self.relx + self.relwidth * 0.8, rely=self.rely + self.relheight * 0.1,
                             relwidth=self.relwidth * 0.2,
                             relheight=0.35 * self.relheight)
        self.button_down.place(relx=self.relx + self.relwidth * 0.8, rely=self.rely + self.relheight * 0.6,
                               relwidth=self.relwidth * 0.2,
                               relheight=0.35 * self.relheight)

        self.param_label = tkinter.Label(master=self.settings.window.app.master, bg=self.settings.window.COLOR,
                                         text=self.param, font="sans 30", fg='#000000')
        self.param_label.place(relx=self.relx, rely=self.rely + self.relheight * 0.1,
                               relwidth=self.relwidth * 0.6,
                               relheight=0.8 * self.relheight)

        self.value_label = tkinter.Label(master=self.settings.window.app.master, bg=self.settings.window.COLOR,
                                         text=str(self.settings.state[self.param]['value']), font="sans 40", fg='#000000')
        self.value_label.place(relx=self.relx + self.relwidth * 0.6, rely=self.rely + self.relheight * 0.1,
                               relwidth=self.relwidth * 0.2,
                               relheight=0.8 * self.relheight)

    def update_value(self):
        self.value_label['text'] = str(self.settings.state[self.param]['value'])

    def increase(self):
        if self.settings.state[self.param]['value'] < 100:
            self.settings.state[self.param]['value'] += 1
            self.update_value()

    def decrease(self):
        if self.settings.state[self.param]['value'] > 0:
            self.settings.state[self.param]['value'] -= 1
            self.update_value()


class Settings:
    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: real, rely: real,
        # relwidth: real, relheight: real,
        # title: tkinter.Label, canvas: tkinter.Canvas
        # state: dict

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.state = {}

        self.init_title()
        self.init_regenerate_button()
        self.init_param_widgets()

    def init_param_widgets(self):
        with open("settings.json", "r") as file:
            self.state = json.load(file)
        self.widgets = list()
        for i, param in enumerate(self.state):
            self.widgets.append(ParamWidget(relx=self.relx,
                                            rely=self.rely + self.relheight * 0.1 + self.relheight * 0.85 * i / len(
                                                self.state),
                                            relwidth=self.relwidth,
                                            relheight=self.relheight * 0.8 / len(self.state),
                                            param=param, settings=self))

    def init_regenerate_button(self):
        self.regenerate_button = tkinter.Button(master=self.window.app.master, text='Save & regenerate',
                                                justify=tkinter.CENTER,
                                                bg=self.window.COLOR, fg='#000000', font='sans 20', command=self.regenerate)
        self.regenerate_button.place(relx=self.relx, rely=self.rely + self.relheight * 0.95,
                                     relwidth=self.relwidth,
                                     relheight=0.05 * self.relheight)

    def init_title(self):
        self.title = tkinter.Label(master=self.window.app.master, text='Settings', justify=tkinter.CENTER,
                                   bg=self.window.COLOR, fg='#000000', font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05 * self.relheight)

    def regenerate(self):
        with open("settings.json", "w") as file:
            json.dump(self.state, file)
        # TODO: generate balls
