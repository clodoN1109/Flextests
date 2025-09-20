from tkinter import ttk
from application.app import App
from infrastructure.environment.environment import Env


class OutputPane:
    def __init__(self, container_tk, initial_width, style, app: App) -> None:
        self.pane_tk = None
        screen = Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

        self.initial_width = initial_width
        self.container = container_tk
        self.app = app
        self.style = style

    def render(self):
        # Create the frame
        self.pane_tk = ttk.Frame(self.container, width=int(self.screen_width * self.initial_width))
        self.pane_tk.pack_propagate(False)  # prevent frame from shrinking to its content

        # Add to PanedWindow
        self.container.add(self.pane_tk)

        return self.pane_tk
