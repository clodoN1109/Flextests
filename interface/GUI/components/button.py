from tkinter import ttk


class Button:
    _grid_counters = {}

    def __init__(self, parent, text: str, cmd=None, width: int = 5,
                 manager: str = "grid", manager_opts: dict | None = None):
        self.parent = parent
        self.text = text
        self.cmd = cmd
        self.width = width
        self.manager = manager  # default to grid for Statistics section
        self.manager_opts = manager_opts or {}
        self.widget = None

    def render(self):
        self.widget = ttk.Button(self.parent, text=self.text, command=self.cmd, width=self.width)

        if self.manager == "grid":
            # Initialize counter for this parent if necessary
            if self.parent not in Button._grid_counters:
                Button._grid_counters[self.parent] = 0

            row = 0  # row can be parameterized later
            column = Button._grid_counters[self.parent]
            opts = {"row": row, "column": column, "padx": 2, "pady": 2, "sticky": "w"}
            opts.update(self.manager_opts)
            self.widget.grid(**opts)

            # Increment column counter for next button
            Button._grid_counters[self.parent] += 1

        elif self.manager == "pack":
            # Only use pack if you are in a frame with other pack-managed widgets
            opts = {"side": "left", "padx": 2, "pady": 2}
            opts.update(self.manager_opts)
            self.widget.pack(**opts)

        return self.widget
