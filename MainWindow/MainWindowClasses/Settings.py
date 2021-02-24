import tkinter
import json


class ParamWidget:
    def __init__(self, settings, param, relx, rely, relwidth, relheight):
        # settings: Settings, relx: float, rely: float, relwidth: float, relheight: float, param: str, job_id: int

        self.settings = settings
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.param = param
        self.job_id = None

        self.button_up = tkinter.Button(master=self.settings.window.app.master, bg=self.settings.window.BG_COLOR,
                                        text="▲",
                                        font="sans 30", fg=self.settings.window.FG_COLOR,
                                        highlightbackground=self.settings.window.BG_COLOR,
                                        relief=tkinter.FLAT, overrelief=tkinter.FLAT,
                                        activebackground=self.settings.window.BG_COLOR,
                                        activeforeground=self.settings.window.FG_COLOR,
                                        bd=0)
        self.button_down = tkinter.Button(master=self.settings.window.app.master, bg=self.settings.window.BG_COLOR,
                                          text="▼", font="sans 30", fg=self.settings.window.FG_COLOR,
                                          highlightbackground=self.settings.window.BG_COLOR,
                                          relief=tkinter.FLAT, overrelief=tkinter.FLAT,
                                          activebackground=self.settings.window.BG_COLOR,
                                          activeforeground=self.settings.window.FG_COLOR, bd=0)

        self.button_up.bind('<ButtonPress-1>', lambda event: self.increase_event_handler())
        self.button_up.bind('<ButtonRelease-1>', lambda event: self.button_up.after_cancel(self.job_id))

        self.button_down.bind('<ButtonPress-1>', lambda event: self.decrease_event_handler())
        self.button_down.bind('<ButtonRelease-1>', lambda event: self.button_up.after_cancel(self.job_id))

        self.button_up.place(relx=self.relx + self.relwidth * 0.8, rely=self.rely + self.relheight * 0.1,
                             relwidth=self.relwidth * 0.2,
                             relheight=0.4 * self.relheight)
        self.button_down.place(relx=self.relx + self.relwidth * 0.8, rely=self.rely + self.relheight * 0.6,
                               relwidth=self.relwidth * 0.2,
                               relheight=0.4 * self.relheight)

        self.param_label = tkinter.Label(master=self.settings.window.app.master, bg=self.settings.window.BG_COLOR,
                                         text=self.param, font="sans 24", fg=self.settings.window.FG_COLOR,
                                         justify=tkinter.LEFT, anchor='w')
        self.param_label.place(relx=self.relx, rely=self.rely + self.relheight * 0.1,
                               relwidth=self.relwidth * 0.6,
                               relheight=0.8 * self.relheight)

        self.value_label = tkinter.Label(master=self.settings.window.app.master, bg=self.settings.window.BG_COLOR,
                                         text=str(self.settings.state[self.param]['value']), font="sans 40",
                                         fg=self.settings.window.FG_COLOR, justify=tkinter.RIGHT,  anchor='e')
        self.value_label.place(relx=self.relx + self.relwidth * 0.5, rely=self.rely + self.relheight * 0.1,
                               relwidth=self.relwidth * 0.3,
                               relheight=0.8 * self.relheight)

    def update_value(self):
        self.value_label['text'] = str(self.settings.state[self.param]['value'])

    def increase_event_handler(self):
        if self.settings.state[self.param]['value'] < 100:
            self.settings.state[self.param]['value'] += 1
            self.update_value()
        self.job_id = self.button_up.after(500, self.increase)

    def decrease_event_handler(self):
        if self.settings.state[self.param]['value'] > 0:
            self.settings.state[self.param]['value'] -= 1
            self.update_value()
        self.job_id = self.button_up.after(500, self.decrease)

    def increase(self):
        if self.settings.state[self.param]['value'] < 100:
            self.settings.state[self.param]['value'] += 1
            self.update_value()
        self.job_id = self.button_up.after(10, self.increase)

    def decrease(self):
        if self.settings.state[self.param]['value'] > 0:
            self.settings.state[self.param]['value'] -= 1
            self.update_value()
        self.job_id = self.button_up.after(10, self.decrease)


class Settings:
    def __init__(self, window, relx, rely, relwidth, relheight):
        # window: MainWindow, relx: real, rely: real, relwidth: real, relheight: real,
        # title: tkinter.Label, canvas: tkinter.Canvas, state: dict, widgets: list, regenerate_button: tkinter.Button

        self.window = window
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        self.state = {}
        self.widgets = list()
        self.regenerate_button = None
        self.title = None

        self.init_title()
        self.init_regenerate_button()
        self.init_param_widgets()

    def init_param_widgets(self):
        with open("settings.json", "r") as file:
            self.state = json.load(file)
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
                                                bg=self.window.BG_COLOR, fg=self.window.FG_COLOR, font='sans 20',
                                                command=self.regenerate)
        self.regenerate_button.place(relx=self.relx, rely=self.rely + self.relheight * 0.95,
                                     relwidth=self.relwidth,
                                     relheight=0.05 * self.relheight)

    def init_title(self):
        self.title = tkinter.Label(master=self.window.app.master, text='Settings', justify=tkinter.CENTER,
                                   bg=self.window.BG_COLOR, fg=self.window.FG_COLOR, font='sans 20')
        self.title.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=0.05 * self.relheight)

    def regenerate(self):
        with open("settings.json", "w") as file:
            json.dump(self.state, file)
        self.window.field.generate(self.state)
