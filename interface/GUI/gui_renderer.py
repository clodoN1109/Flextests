import tkinter as tk
import tkinter.font as tkFont
from infrastructure.environment.environment import Env
from interface.GUI.components.window import Window


class GUIRenderer:

    def __init__(self, gui):
        self.window: Window = None
        self.gui    = gui
        self.root   = gui.root
        self.app    = gui.app
        self.style  = gui.style
        self.config_os_window_navbar()
        self.set_font(self.root, "courier", 10)

    def render(self):
        self.window = Window(self.root, self.style, self.app).render("flextests", 1000, 650)
        self.style.apply_style(self.window)

    # OBSOLETE
    def update_state(self):
        def update_controller_section():
            test_names_list = [test.name for test in self.app.get_tests_list()]
            self.window.panes.input_pane.test_selector.combobox.configure(values=test_names_list)
        update_controller_section()

    def config_os_window_navbar(self):
        self.root.iconphoto(False, tk.PhotoImage(file=f"{Env.get_script_path()}/assets/icons/icon.png"))

    @staticmethod
    def set_font(widget: tk.Tk, font_family, size):
        widget.default_font = tkFont.Font(family=font_family, size=size)



