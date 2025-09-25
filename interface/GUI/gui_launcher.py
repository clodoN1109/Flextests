from tkinter import Tk
from typing import List
from application.app import App
from interface.GUI.gui_config import GUIConfig
from interface.GUI.gui_renderer import GUIRenderer
from interface.GUI.gui_styles import GUIStyle


class GUI:
    def __init__(self):
        self.app: App | None = None
        self.config = GUIConfig()
        self.root = None
        self.style = None

    def prepare(self, app: App, config:GUIConfig) -> None:
        self.app = app
        self.config = config
        self.root = Tk()
        if self.config is None:
            self.style = GUIStyle('dark')
        else :
            self.style = GUIStyle('light')

    def launch(self) -> None:
        GUIRenderer(self).render()
        self.root.mainloop()

