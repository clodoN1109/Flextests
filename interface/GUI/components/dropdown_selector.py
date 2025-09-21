import tkinter as tk
from tkinter import ttk


class DropdownSelector:

    def __init__(self, container, title, function=None, style=None):
        self.container = container
        self.title = title
        self.function = function
        self.style = style or ttk.Style()
        self.box = None
        self.var = None

    def render(self):
        self._add_dropdown(
            self.container,
            str(self.title).lower(),
            values=[],
            button=("  🖋️", self.function, 4),
        )

    def _add_dropdown(self, parent, label, values, button=None):
        """Add a labeled dropdown, with optional small square button on the right."""

        # Label with tighter spacing to dropdown
        ttk.Label(
            parent,
            text=label,
            anchor="w",
        ).pack(
            anchor="w",
            fill="x",
            padx=0,
            pady=(2, 0),  # small gap below label (close to dropdown)
        )

        # Container for combobox + optional button
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=0, pady=(0, 6))

        self.var = tk.StringVar(master=self.container)

        combo_frame = tk.Frame(frame)
        combo_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.combobox = ttk.Combobox(
            combo_frame,
            textvariable=self.var,
            state="readonly",
            values=values,
        )
        #ipady increments the dropdown's height
        self.combobox.pack(fill="x", expand=True, ipady=0)

        if button:
            text, cmd, width = button
            self._add_button(frame, text, cmd, width)

    @staticmethod
    def _add_button(frame, text, cmd, width):
        ttk.Button(
            frame,
            text=text,
            command=cmd,
            width=width,
        ).pack(side="left")

