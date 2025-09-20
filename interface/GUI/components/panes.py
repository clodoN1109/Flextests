from application.app import App
from infrastructure.environment.environment import Env
import tkinter as tk
from interface.GUI.components.input_pane import InputPane
from interface.GUI.components.output_pane import OutputPane


class Panes:
    def __init__(self, window_tk, style, app: App) -> None:
        self.tk = window_tk
        self.style = style
        self.app = app

        self.left_pane = None
        self.right_pane = None
        self.paned_window = None

        screen = Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

    def render(self):
        self.paned_window = tk.PanedWindow(
            self.tk,
            orient="horizontal",
            sashwidth=5,
            borderwidth=0,
            background=f"{self.style.separator_bg}"  # proper bg
        )
        self.paned_window.pack(fill="both", expand=True)

        # Render left and right panes
        self.left_pane = InputPane(self.paned_window, 0.16, self.style, self.app).render()
        self.right_pane = OutputPane(self.paned_window, 0.84, self.style, self.app).render()

        return self