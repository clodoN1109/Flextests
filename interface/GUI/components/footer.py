import tkinter as tk
from interface.GUI.gui_styles import GUIStyle


class Footer:
    STATE_SYMBOLS = {
        "idle": "\u25CB",        # ○ open circle
        "processing": "\u25B6",  # ▶ play
        "error": "\u2716",       # ✖ cross
    }

    def __init__(self, parent, style:GUIStyle, window:"Window", build: str = "dev", version: str = "0.0.1"):
        """
        :param parent: Tkinter or ttk parent widget
        :param build: Build string
        :param version: Version string
        """
        self.parent = parent
        self.style = style
        self.window = window

        self.build = build
        self.version = version
        self.state = "idle"
        self.frame = None
        self.state_label = None
        self.info_label = None

    def render(self):
        """Create the footer widgets inside the parent."""
        if self.frame is not None:
            # already rendered
            return

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side="bottom", fill="x")

        # Left: state
        self.state_label = tk.Label(self.frame, text=self._state_text())
        self.state_label.pack(side="left", padx=(6, 6))

        # Right: build/version
        self.info_label = tk.Label(self.frame, text=self._info_text())
        self.info_label.pack(side="right", padx=(6, 6))

        return self

    def _state_text(self) -> str:
        symbol = self.STATE_SYMBOLS.get(self.state, "?")
        return f"{symbol} {self.state.capitalize()}"

    def _info_text(self) -> str:
        return f"Build: {self.build} | Version: {self.version}"

    def set_state(self, state: str, message: str = ""):
        if state not in self.STATE_SYMBOLS:
            raise ValueError(f"Invalid state: {state}")
        self.state = state
        if self.state_label:
            self.state_label.config(text=f"{self._state_text()} {message}")
            self.state_label.update_idletasks()

    def set_build_version(self, build: str, version: str):
        self.build = build
        self.version = version
        if self.info_label:
            self.info_label.config(text=self._info_text())
