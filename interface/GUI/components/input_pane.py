from tkinter import ttk
from application.app import App
from infrastructure.environment.environment import Env
from interface.GUI.components.button import Button
from interface.GUI.components.dropdown_selector import DropdownSelector
from interface.GUI.components.output_pane import OutputPane
from interface.GUI.components.section_title import SectionTitle


class InputPane:
    def __init__(self, panned_window, initial_width, style, app: App, output_pane: OutputPane) -> None:
        self.controller_section_frame = None
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
        self.test_selector = None
        self.new_test_button = None

        self.configurations_section_title = None
        self.statistics_section_title     = None


    def render(self):
        # Create the left pane container
        self.pane_tk = ttk.Frame(
            self.panned_window,
            width=int(self.screen_width * self.initial_width)
        )
        self.pane_tk.pack_propagate(False)  # prevent frame from shrinking
        self.panned_window.add(self.pane_tk)

        # Controller Section (frame that can be toggled on and off)
        self.controller_section_frame = ttk.Frame(self.pane_tk, padding=10)

        # Section title that can toggle the controller_section_frame
        self.controller_section_title = SectionTitle(
            self.pane_tk,
            "Controller",
            self.controller_section_frame
        )
        self.controller_section_title.render()

        # Widgets go inside controller_section_frame
        self.test_selector = DropdownSelector(
            self.controller_section_frame,
            "tests",
            print
        )
        self.test_selector.render()
        # --------------------------------
        self.new_test_button = Button(self.controller_section_frame, "➕", print, 4)
        self.new_test_button.render()
        # --------------------------------
        self.run_test_button = Button(self.controller_section_frame, "🞂", print, 4)
        self.run_test_button.render()
        # ================================

        # Configurations Section
        self.configurations_section_title = SectionTitle(self.pane_tk, "Configurations").render()

        #Statistics Section
        self.statistics_section_title     = SectionTitle(self.pane_tk, "Statistics").render()

        return self
