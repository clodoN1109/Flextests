import tkinter as tk
import tkinter.font as tkFont
from infrastructure.environment.environment import Env
from interface.GUI.components.title_bar import TitleBar
from interface.GUI.components.window import Window


class GUIRenderer:

    def __init__(self, gui):
        self.gui    = gui
        self.root   = gui.root
        self.app    = gui.app
        self.style  = gui.style
        self.config_os_window_navbar()
        self.set_font(self.root, "courier", 10)

    def render(self):
        window = Window(self.root).render("flextests", 1000, 600)
        title_bar = TitleBar(window, self.style).render()
        self.style.apply_style()

    def config_os_window_navbar(self):
        self.root.iconphoto(False, tk.PhotoImage(file=f"{Env.get_script_path()}/assets/icons/icon.png"))

    @staticmethod
    def set_font(widget: tk.Tk, font_family, size):
        widget.default_font = tkFont.Font(family=font_family, size=size)



