import tkinter


from MainWindow.MainWindow import MainWindow


class App:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800

    def __init__(self):
        self.master = tkinter.Tk()

        SCREEN_WIDTH = self.master.winfo_screenwidth()
        SCREEN_HEIGHT = self.master.winfo_screenheight()

        WINDOW_X = (SCREEN_WIDTH - App.WINDOW_WIDTH) // 2
        WINDOW_Y = (SCREEN_HEIGHT - App.WINDOW_HEIGHT) // 2

        self.master.geometry(f"{App.WINDOW_WIDTH}x{App.WINDOW_HEIGHT}+{WINDOW_X}+{WINDOW_Y}")
        self.main_window = MainWindow(self)

    def show(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = App()
    app.show()
