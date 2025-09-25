import tkinter as tk

class FormField:
    def __init__(
        self,
        parent,
        row=None,
        label_text="",
        variable=None,
        unit=None,
        right_widget_fn=None,
        width=12,
        padding_left: int = 12,
        manager: str = "grid",  # "grid" or "pack"
        **manager_opts  # extra kwargs for grid or pack
    ):
        self.parent = parent
        self.row = row
        self.manager = manager
        self.manager_opts = manager_opts

        self.padding_left = padding_left

        # --- Label ---
        self.label = tk.Label(parent, text=label_text)

        # --- Frame to hold Entry + Unit + Right Widget ---
        self.entry_frame = tk.Frame(parent)

        # --- Entry ---
        self.entry = tk.Entry(self.entry_frame, textvariable=variable, width=width)

        # --- Unit ---
        self.unit_label = None
        if unit:
            self.unit_label = tk.Label(self.entry_frame, text=unit)

        # --- Optional Right Widget ---
        self.right_widget = None
        if right_widget_fn:
            self.right_widget = right_widget_fn(self.entry_frame)

        # --- Store variable reference ---
        self.variable = variable

        # --- Render all widgets ---
        self._render()

    def _render(self):
        if self.manager == "grid":
            # Label
            label_opts = {"row": self.row, "column": 0, "padx": (self.padding_left, 3), "pady": 3, "sticky": "w"}
            label_opts.update(self.manager_opts)
            self.label.grid(**label_opts)

            # Frame
            frame_opts = {"row": self.row, "column": 1, "padx": 0, "pady": 3, "sticky": "w"}
            frame_opts.update(self.manager_opts)
            self.entry_frame.grid(**frame_opts)

            # Entry + unit + right widget inside frame using pack (always horizontal)
            self.entry.pack(side="left")
            if self.unit_label:
                self.unit_label.pack(side="left", padx=(2, 5))
            if self.right_widget:
                self.right_widget.pack(side="left", padx=(5, 0))

        elif self.manager == "pack":
            self.label.pack(**self.manager_opts, side="left", padx=(0, 10), pady=8)
            self.entry_frame.pack(**self.manager_opts, side="left")
            self.entry.pack(side="left")
            if self.unit_label:
                self.unit_label.pack(side="left", padx=(2, 5))
            if self.right_widget:
                self.right_widget.pack(side="left", padx=(10, 0))
        else:
            raise ValueError(f"Unsupported manager: {self.manager}")

    # --- Hide/Show methods ---
    def hide(self):
        if self.manager == "grid":
            self.label.grid_remove()
            self.entry_frame.grid_remove()
        else:
            self.label.pack_forget()
            self.entry_frame.pack_forget()

    def show(self):
        if self.manager == "grid":
            self.label.grid()
            self.entry_frame.grid()
        else:
            self.label.pack(**self.manager_opts)
            self.entry_frame.pack(**self.manager_opts)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)


