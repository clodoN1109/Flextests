import tkinter as tk
import tkinter.font as tkFont
from application.app import App
from infrastructure.environment.environment import Env
from interface.GUI.components.window import Window
from interface.GUI.gui_config import GUIConfig


class GUIRenderer:

    def __init__(self, gui):
        self.window: Window|None = None
        self.gui    = gui
        self.root   = gui.root
        self.app: App   = gui.app
        self.config: GUIConfig = gui.config
        self.style  = gui.style
        self.config_os_window_navbar()
        self.set_font(self.root, "courier", 10)

    def render(self):
        self.window = Window(self.root, self.style, self.app, self.config).render("flextests", 1000, 650)
        self.style.apply_style(self.window)
        self.apply_config()

    def config_os_window_navbar(self):
        self.root.iconphoto(False, tk.PhotoImage(file=f"{Env.get_script_path()}/assets/icons/icon.png"))

    @staticmethod
    def set_font(widget: tk.Tk, font_family, size):
        widget.default_font = tkFont.Font(family=font_family, size=size)

    def apply_config(self):
        if (self.config.dark_mode and self.window.title_bar.style.prefix == "light") \
                or (not self.config.dark_mode and self.window.title_bar.style.prefix == "dark"):
            self.window.title_bar.toggle_dark_mode()
        if (self.config.maximized and not self.window.title_bar.is_maximized) \
                or (not self.config.maximized and self.window.title_bar.is_maximized):
            self.window.title_bar.toggle_maximize()
        if (self.config.transparent and not self.window.title_bar.is_transparent) \
                or (not self.config.transparent and self.window.title_bar.is_transparent):
            self.window.title_bar.toggle_transparency()

