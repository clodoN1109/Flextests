from tkinter import ttk

class Button:
    # Keep track of created buttons per parent for default row placement
    _grid_counters = {}

    def __init__(self, parent, text: str, cmd=None, width: int = 5,
                 manager: str = "pack", manager_opts: dict | None = None):
        """
        :param parent: Parent widget
        :param text: Button label
        :param cmd: Command to run on click
        :param width: Button width
        :param manager: "pack" or "grid"
        :param manager_opts: Optional dict to override default manager options
        """
        self.parent = parent
        self.text = text
        self.cmd = cmd
        self.width = width
        self.manager = manager
        self.manager_opts = manager_opts or {}
        self.widget = None

    def render(self):
        self.widget = ttk.Button(self.parent, text=self.text, command=self.cmd, width=self.width)

        if self.manager == "pack":
            # Default: place horizontally in a row
            opts = {"side": "left", "padx": 2, "pady": 2}
            opts.update(self.manager_opts)
            self.widget.pack(**opts)

        elif self.manager == "grid":
            # Initialize counter for this parent if necessary
            if self.parent not in Button._grid_counters:
                Button._grid_counters[self.parent] = 0

            row = 0  # Always in row 0 for default
            column = Button._grid_counters[self.parent]
            opts = {"row": row, "column": column, "padx": 2, "pady": 2, "sticky": "w"}
            opts.update(self.manager_opts)

            self.widget.grid(**opts)

            # Increment column counter for next button
            Button._grid_counters[self.parent] += 1

        return self.widget
