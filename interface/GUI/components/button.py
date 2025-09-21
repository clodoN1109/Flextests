from tkinter import ttk


class Button:

    def __init__(self, parent, text: str, cmd = None, width:int = 5):
        self.parent = parent
        self.text = text
        self.widget = None
        self.cmd = cmd
        self.width = width

    def render(self):
        Button.add_button(self.parent, self.text, self.cmd, self.width)

    @staticmethod
    def add_button(parent, text, cmd, width):
        widget = ttk.Button(
            parent,
            text=text,
            command=cmd,
            width=width,
        )
        widget.pack(side="left", padx=(2, 5), pady=(2, 2))
        return widget