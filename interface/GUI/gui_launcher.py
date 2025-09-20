from tkinter import Tk
from typing import List
from application.app import App
from interface.GUI.gui_renderer import GUIRenderer
from interface.GUI.gui_styles import GUIStyle


class GUI:
    def __init__(self):
        self.app: App | None = None
        self.settings: List[str] = []
        self.root = None
        self.style = None

    def prepare(self, app: App, settings: List[str]) -> None:
        self.app = app
        self.settings = settings
        self.root = Tk()
        self.style = GUIStyle('dark')

    def launch(self) -> None:
        GUIRenderer(self).render()
        self.root.mainloop()

