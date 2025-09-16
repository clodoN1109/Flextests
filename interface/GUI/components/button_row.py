from tkinter import ttk
from typing import Callable, Sequence


class ButtonRow:
    def __init__(self, parent, buttons: Sequence[tuple[str, Callable]], width: int | None = None):
        self.parent = parent
        self.ref = self._add_button_row(parent, buttons, width)

    @staticmethod
    def _add_button_row(parent, buttons: Sequence[tuple[str, Callable]], width: int | None = None):
        """Add a horizontal row of buttons and return the containing frame."""
        frame = ttk.Frame(parent, width=width)
        frame.pack(fill="x")

        for text, cmd in buttons:
            ttk.Button(
                frame,
                text=text,
                command=cmd,
            ).pack(side="left")

        return frame
