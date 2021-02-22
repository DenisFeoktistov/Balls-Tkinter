import tkinter


from MainWindow.MainWindow import MainWindow


class App:
    def __init__(self):
        self.master = tkinter.Tk()
        self.main_window = MainWindow(self)

    def show(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = App()
    app.show()
