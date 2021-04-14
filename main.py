import tkinter


from MainWindow.MainWindow import MainWindow


class App:
    FPS = 30
    DEBUG_ARROWS = False

    def __init__(self):
        # master: tkinter.Tk, main_window: MainWindow
        self.master = tkinter.Tk()

        self.main_window = MainWindow(self)

    def show(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = App()
    app.show()
