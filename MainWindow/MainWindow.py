from .MainWindowClasses.Field import Field
from .MainWindowClasses.Settings import Settings


class MainWindow:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    BG_COLOR = '#B4B4B4'
    FG_COLOR = '#000000'

    def __init__(self, app):
        # app: App, settings: Settings, field: Field
        self.app = app

        self.resize()
        self.init_background()
        self.init_title()

        self.settings = Settings(self, relx=0.51, rely=0.1, relwidth=0.48, relheight=0.8)
        self.field = Field(self, relx=0.01, rely=0.1, relwidth=0.48, relheight=0.8)

    def init_background(self):
        self.app.master["bg"] = MainWindow.BG_COLOR

    def init_title(self):
        self.app.master.title("Balls")

    def resize(self):
        screen_width = self.app.master.winfo_screenwidth()
        screen_height = self.app.master.winfo_screenheight()
        window_x = (screen_width - MainWindow.WINDOW_WIDTH) // 2
        window_y = (screen_height - MainWindow.WINDOW_HEIGHT) // 2
        self.app.master.geometry(f"{MainWindow.WINDOW_WIDTH}x{MainWindow.WINDOW_HEIGHT}+{window_x}+{window_y}")
