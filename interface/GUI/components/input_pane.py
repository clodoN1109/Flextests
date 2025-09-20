from tkinter import ttk
from application.app import App
from infrastructure.environment.environment import Env
from interface.GUI.components.section_title import SectionTitle


class InputPane:
    def __init__(self, panned_window, initial_width, style, app: App) -> None:
        self.pane_tk = None
        screen = Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

        self.initial_width = initial_width
        self.panned_window = panned_window
        self.app = app
        self.style = style

        # elements
        self.controller_section_title     = None
        self.configurations_section_title = None
        self.statistics_section_title     = None


    def render(self):
        # Create the frame
        self.pane_tk = ttk.Frame(self.panned_window, width=int(self.screen_width * self.initial_width))
        self.pane_tk.pack_propagate(False)  # prevent frame from shrinking to its content

        # Add to PanedWindow
        self.panned_window.add(self.pane_tk)

        # Controller Section
        self.controller_section_title     = SectionTitle(self.pane_tk, "Controller").render()

        # Configurations Section
        self.configurations_section_title = SectionTitle(self.pane_tk, "Configurations").render()

        #Statistics Section
        self.statistics_section_title     = SectionTitle(self.pane_tk, "Statistics").render()

        return self
