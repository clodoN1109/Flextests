import tkinter as tk

class SectionTitle:
    def __init__(self, parent, title: str, target_frame=None) -> None:
        self.parent = parent
        self.title = title
        self.target_frame = target_frame

        self.is_visible = True
        self.frame = None
        self.arrow_label = None
        self.title_label = None

    def render(self):
        # Container frame for arrow + title
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="x", padx=0, pady=(0, 2))

        # Arrow on the left
        self.arrow_label = tk.Label(
            self.frame,
            text="▼",
            anchor="w",
            cursor="hand2",
            fg="white"  # optional for contrast
        )
        self.arrow_label.pack(side="left")

        # Title centered
        self.title_label = tk.Label(
            self.frame,
            text=self.title.upper(),
            anchor="center",
        )
        self.title_label.pack(side="left", fill="x", expand=True)

        # Bind both labels to toggle
        self.arrow_label.bind("<Button-1>", self.toggle)
        self.title_label.bind("<Button-1>", self.toggle)

        return self

    def toggle(self, event=None):
        if self.is_visible:
            if self.target_frame is not None:
                self.target_frame.pack_forget()
            self.arrow_label.config(text="▶")
        else:
            if self.target_frame is not None:
                self.target_frame.pack(fill="x", padx=10, pady=(0, 10))
            self.arrow_label.config(text="▼")

        self.is_visible = not self.is_visible
