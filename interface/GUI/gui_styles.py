from tkinter import ttk
import tkinter as tk


class GUIStyle:

    def __init__(self, style: str = "dark") -> None:
        self.prefix = None

        self.footer_bg = None
        self.section_separator_bg = None
        self.section_separator_fg = None
        self.button_border_color_accent = None
        self.semantic_info = None
        self.grid_color = None
        self.text_fg = None
        self.text_bg = None
        self.separator_bg = None
        self.accent_hover = None
        self.accent_bg = None
        self.primary_fg = None
        self.primary_bg = None

        self.select_style(style)

    def select_style(self, style) -> None:
        if style == "dark":
            self.prefix = "dark"
            self.primary_bg = "#252526"  # deep background (like VS Code dark)
            self.primary_fg = "#f0f0f0"  # main text, near-white
            self.accent_bg = "#333333"  # buttons, inputs (entry field)
            self.accent_hover = "#444444"  # button hover
            self.separator_bg = "#333333"  # subtle dividers (kept subtle/invisible)
            self.text_bg = "#252526"  # sub-panes / stats background
            self.text_fg = "#f0f0f0"  # text in sub-panes
            self.grid_color = "#3a3a3a"  # chart grid, softer than fg
            self.semantic_info = "#569cd6"  # highlights (blue, like VS Code)
            self.button_border_color_accent = "#569cd6"
            self.section_separator_fg = "#f0f0f0"
            self.section_separator_bg = "#434343"
            self.footer_bg = "#333333"

        elif style == "light":
            self.prefix = "light"
            self.primary_bg = "#ffffff"  # clean white
            self.primary_fg = "#252526"  # strong black text
            self.accent_bg = "#f0f0f0"  # buttons, inputs (entry field)
            self.accent_hover = "#e0e0e0"  # button hover
            self.separator_bg = "#e5e5e5"  # subtle divider
            self.text_bg = "#fafafa"  # sub-panes background
            self.text_fg = "#2b2b2b"  # text in sub-panes
            self.grid_color = "#d0d0d0"  # chart grid
            self.semantic_info = "#2e7d32"  # Pythonic green
            self.button_border_color_accent = "#ffd43b" # Pythonic yellow
            self.section_separator_fg = "#252526"
            self.section_separator_bg = "#f0f0f0"
            self.footer_bg = "#f0f0f0"
        else:
            raise ValueError(f"Unknown style mode: {style}")

    def toggle_dark_mode(self, window):
        if self.prefix == "dark":
            self.select_style("light")
        else: self.select_style("dark")
        self.apply_style(window)

    def apply_style(self, window):
        tk_root = window.tk

        def _apply(widget):
            # Background and foreground colors
            try:
                if isinstance(widget, (tk.Frame, ttk.Frame)):
                    widget.configure(bg=self.primary_bg)
                elif isinstance(widget, (tk.Label, ttk.Label)):
                    widget.configure(background=self.primary_bg, foreground=self.primary_fg)
                elif isinstance(widget, (tk.Button, ttk.Button)):
                    widget.configure(background=self.accent_bg, foreground=self.primary_fg)
                elif isinstance(widget, (tk.Entry, ttk.Entry, tk.Text)):
                    widget.configure(background=self.text_bg, foreground=self.text_fg,
                                     insertbackground=self.primary_fg)  # caret color
                elif isinstance(widget, tk.Toplevel):
                    widget.configure(bg=self.primary_bg)
            except tk.TclError:
                # Some ttk widgets don’t allow direct bg/fg config
                pass

            # Recurse through children
            for child in widget.winfo_children():
                _apply(child)

        # Start recursive application from root
        _apply(tk_root)

        # Update ttk global styles via Style object
        style = ttk.Style(tk_root)
        style.theme_use("default")

        style.configure("TFrame", background=self.primary_bg)
        style.configure("TLabel", background=self.primary_bg, foreground=self.primary_fg)

        # 🔹 Button styling with vertical padding
        style.configure(
            "TButton",
            background=self.accent_bg,
            foreground=self.primary_fg,
            padding=(4, 2)  # (horizontal, vertical) → adjust vertical to match combobox
        )
        style.map(
            "TButton",
            background=[("active", self.accent_hover)],
            foreground=[("disabled", "#888888")]
        )

        style.configure("TEntry", fieldbackground=self.text_bg, foreground=self.text_fg)

        # Update specific tk elements
        tk_root.title_separator.configure(bg=self.separator_bg)
        window.panes.paned_window.configure(bg=self.separator_bg)
        window.panes.input_pane.controller_section_title.title_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.controller_section_title.arrow_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.configurations_section_title.title_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.configurations_section_title.arrow_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.statistics_section_title.title_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.statistics_section_title.arrow_label.configure(bg=f"{self.section_separator_bg}")
        tk_root.update_idletasks()



