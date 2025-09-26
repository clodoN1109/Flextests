import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk


class DropdownSelector:
    def __init__(self, parent, title, button=None, style=None, row=None, manager="grid", **manager_opts):
        self.parent = parent
        self.title = title
        self.style = style or ttk.Style()
        self.var = None
        self.button = button
        self.row = row
        self.manager = manager
        self.manager_opts = manager_opts
        self.label_widget = None
        self.combobox = None

    def render(self, values=None):
        values = values or []
        if self.manager == "grid":
            self._add_dropdown_grid(values)
        elif self.manager == "pack":
            self._add_dropdown_pack(values)
        else:
            raise ValueError(f"Unsupported manager: {self.manager}")

    def _add_dropdown_grid(self, values):
        # Label
        self.label_widget = ttk.Label(self.parent, text=self.title, anchor="w")
        label_opts = {
            "row": self.row,
            "column": 0,
            "padx": (2, 3),
            "pady": 3,
            "sticky": "w",
        }
        label_opts.update(self.manager_opts)
        self.label_widget.grid(**label_opts)

        # Frame for combobox + optional button
        frame = ttk.Frame(self.parent)
        frame_opts = {
            "row": self.row,
            "column": 1,
            "padx": 0,
            "pady": 3,
            "sticky": "w",
        }
        frame_opts.update(self.manager_opts)
        frame.grid(**frame_opts)

        # Combobox
        self.var = tk.StringVar(master=self.parent)
        self.combobox = ttk.Combobox(frame, textvariable=self.var, state="readonly", values=values)
        self.combobox.pack(side="left", fill="x", expand=True)

        # Optional button
        if self.button:
            text, cmd, width = self.button
            ttk.Button(frame, text=text, command=cmd, width=width).pack(side="left", padx=(5, 0))

    def _add_dropdown_pack(self, values):
        # Label
        self.label_widget = ttk.Label(self.parent, text=self.title, anchor="w")
        self.label_widget.pack(anchor="w", fill="x", padx=0, pady=(2, 0))

        # Frame for combobox + optional button
        frame = ttk.Frame(self.parent)
        frame.pack(fill="x", padx=0, pady=(0, 6))

        # Combobox
        self.var = tk.StringVar(master=self.parent)
        self.combobox = ttk.Combobox(frame, textvariable=self.var, state="readonly", values=values)
        self.combobox.pack(side="left", fill="x", expand=True)

        # Optional button
        if self.button:
            text, cmd, width = self.button
            ttk.Button(frame, text=text, command=cmd, width=width).pack(side="left", padx=(5, 0))


