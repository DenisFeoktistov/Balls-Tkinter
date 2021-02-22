from .MainWindowClasses.Field import Field
from .MainWindowClasses.Settings import Settings


class MainWindow:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800

    def __init__(self, app):
        self.app = app

        SCREEN_WIDTH = self.app.master.winfo_screenwidth()
        SCREEN_HEIGHT = self.app.master.winfo_screenheight()

        window_x = (SCREEN_WIDTH - MainWindow.WINDOW_WIDTH) // 2
        window_y = (SCREEN_HEIGHT - MainWindow.WINDOW_HEIGHT) // 2

        self.app.master.geometry(f"{MainWindow.WINDOW_WIDTH}x{MainWindow.WINDOW_HEIGHT}+{window_x}+{window_y}")

        self.settings = Settings(self)
        self.field = Field(self)
