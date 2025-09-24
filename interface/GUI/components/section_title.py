import tkinter as tk

class SectionTitle:
    def __init__(self, parent, title: str):
        self.parent = parent
        self.title = title
        self.is_visible = True

        # This frame wraps everything: title row + content
        self.frame = tk.Frame(self.parent)
        self.title_row = tk.Frame(self.frame)
        self.target_frame = tk.Frame(self.frame, padx=10, pady=10)  # content container

        self.arrow_label = None
        self.title_label = None

    def render(self):
        # Pack outer frame
        self.frame.pack(fill="x", padx=0, pady=(0,2))

        # Pack title row
        self.title_row.pack(fill="x")

        # Arrow + title
        self.arrow_label = tk.Label(self.title_row, text="▼", cursor="hand2", fg="white")
        self.arrow_label.pack(side="left")
        self.title_label = tk.Label(self.title_row, text=self.title.upper(), anchor="center")
        self.title_label.pack(side="left", fill="x", expand=True)

        # Pack target frame (starts visible)
        self.target_frame.pack(fill="x")

        # Bind toggle
        self.arrow_label.bind("<Button-1>", self.toggle)
        self.title_label.bind("<Button-1>", self.toggle)

        return self

    def toggle(self, event=None):
        if self.is_visible:
            self.target_frame.pack_forget()
            self.arrow_label.config(text="▶")
        else:
            self.target_frame.pack(fill="x")
            self.arrow_label.config(text="▼")
        self.is_visible = not self.is_visible
