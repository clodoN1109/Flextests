from tkinter import ttk


class Button:

    @staticmethod
    def add_button(parent, text, cmd, width):
        return ttk.Button(
            parent,
            text=text,
            command=cmd,
            width=width,
        ).pack(side="left", padx=(2, 5), pady=(2, 2))

    @staticmethod
    def add_button_row(parent, buttons):
        """Add a horizontal row of buttons."""
        frame = ttk.Frame(parent)
        frame.pack(fill="x")
        for text, cmd in buttons:
            ttk.Button(
                frame,
                text=text,
                command=cmd,
            ).pack(side="left")
