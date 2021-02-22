from .MainWindowClasses.Field import Field
from .MainWindowClasses.Settings import Settings


class MainWindow:
    def __init__(self):
        self.settings = Settings()
        self.field = Field()

    def show(self):
        pass
