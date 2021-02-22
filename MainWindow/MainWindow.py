from .MainWindowClasses.Field import Field
from .MainWindowClasses.Settings import Settings


class MainWindow:
    def __init__(self, app):
        self.app = app

        self.settings = Settings(self)
        self.field = Field(self)
