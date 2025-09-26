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

    def toggle_dark_mode(self, window: "Window"):
        if self.prefix == "dark":
            self.select_style("light")
            window.config.dark_mode = False
        else:
            self.select_style("dark")
            window.config.dark_mode = True
        window.title_bar.save_config(window.config)
        self.apply_style(window)

    def apply_style(self, window: "Window") -> None:
        tk_root = window.tk

        def _apply(widget):
            """
            Recursively restyle Tkinter and ttk widgets, including Frames, Labels, Buttons,
            Entry/Text, Toplevels, and Treeviews.
            """
            try:
                # Tk widgets
                if isinstance(widget, (tk.Frame, ttk.Frame)):
                    widget.configure(bg=self.primary_bg)
                elif isinstance(widget, (tk.Label, ttk.Label)):
                    widget.configure(background=self.primary_bg, foreground=self.primary_fg)
                elif isinstance(widget, (tk.Button, ttk.Button)):
                    widget.configure(background=self.accent_bg, foreground=self.primary_fg)
                elif isinstance(widget, (tk.Entry, ttk.Entry, tk.Text)):
                    widget.configure(
                        background=self.text_bg,
                        foreground=self.text_fg,
                        insertbackground=self.primary_fg  # caret color
                    )
                elif isinstance(widget, tk.Toplevel):
                    widget.configure(bg=self.primary_bg)
                # ttk Treeview
                elif isinstance(widget, ttk.Treeview):
                    style = ttk.Style()
                    style.configure("Custom.Treeview",
                                    background=self.text_bg,
                                    foreground=self.text_fg,
                                    fieldbackground=self.text_bg)
                    style.configure("Custom.Treeview.Heading",
                                    background=self.primary_bg,
                                    foreground=self.primary_fg)
                    widget.configure(style="Custom.Treeview")
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
        # Treeview base style
        style.configure(
            "Custom.Treeview",
            background=self.text_bg,
            foreground=self.text_fg,
            fieldbackground=self.text_bg,
            rowheight=22  # optional, adjust row height
        )
        # Treeview heading style
        style.configure(
            "Custom.Treeview.Heading",
            background=self.primary_bg,
            foreground=self.primary_fg,
            relief="flat"
        )
        # Hover / active state for headings
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", self.accent_bg)],
            foreground=[("active", self.primary_fg)]
        )
        # Frames and labels
        style.configure("TFrame", background=self.primary_bg)
        style.configure("TLabel", background=self.primary_bg, foreground=self.primary_fg)
        # Buttons
        style.configure(
            "TButton",
            background=self.accent_bg,
            foreground=self.primary_fg,
            padding=(4, 2)  # (horizontal, vertical)
        )
        style.map(
            "TButton",
            background=[("active", self.accent_hover)],
            foreground=[("disabled", "#888888")]
        )
        # Entries
        style.configure("TEntry", fieldbackground=self.text_bg, foreground=self.text_fg)
        # Scrollbars
        style.configure(
            "Vertical.TScrollbar",
            troughcolor=self.primary_bg,
            background=self.accent_bg,
            arrowcolor=self.primary_fg,
            bordercolor=self.primary_bg,
            gripcount=0
        )
        style.configure(
            "Horizontal.TScrollbar",
            troughcolor=self.primary_bg,
            background=self.accent_bg,
            arrowcolor=self.primary_fg,
            bordercolor=self.primary_bg,
            gripcount=0
        )

        # Update specific tk elements
        tk_root.title_separator.configure(bg=self.separator_bg)
        window.panes.paned_window.configure(bg=self.separator_bg)
        window.panes.input_pane.controller_section_title.title_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.controller_section_title.arrow_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.configurations_section_title.title_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.configurations_section_title.arrow_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.statistics_section_title.title_label.configure(bg=f"{self.section_separator_bg}")
        window.panes.input_pane.statistics_section_title.arrow_label.configure(bg=f"{self.section_separator_bg}")
        window.footer.frame.configure(bg=self.footer_bg)
        window.footer.info_label.configure(bg=self.footer_bg)
        window.footer.state_label.configure(bg=self.footer_bg)

        textbox = getattr(window.panes.output_pane, "description_textbox", None)
        if textbox and str(textbox) and textbox.winfo_exists():
            textbox.configure(bg=self.primary_bg)

        self.apply_style_to_plot(window)

        tk_root.update_idletasks()

    def apply_style_to_plot(self, window:"Window"):
        # --- matplotlib re-style ---
        output_pane: "OutputPane" = window.panes.output_pane
        ax = output_pane.ax
        fig = output_pane.fig
        canvas = output_pane.canvas
        title = output_pane.plot_title
        subtitle = output_pane.plot_subtitle

        if ax is not None and fig is not None and canvas is not None:
            # Figure and axes background
            fig.set_facecolor(self.primary_bg)
            ax.set_facecolor(self.text_bg)

            # Tick labels
            ax.tick_params(colors=self.primary_fg, which="both")  # major + minor

            # Axis labels
            ax.xaxis.label.set_color(self.primary_fg)
            ax.yaxis.label.set_color(self.primary_fg)

            # Title (force re-apply with correct color)
            ax.set_title(title, fontsize=12, fontweight="bold", loc="left", pad=10, color=f"{self.primary_fg}")
            ax.text(
                0, 1, subtitle,
                transform=ax.transAxes,
                fontsize=9, style="italic",
                ha="left", va="bottom", color=f"{self.primary_fg}"
            )

            # Grid styling
            ax.grid(
                color=self.grid_color,
                linestyle="--",
                linewidth=0.5,
                alpha=0.7
            )

            # Spines (borders)
            for spine in ax.spines.values():
                spine.set_edgecolor(self.primary_fg)
                spine.set_linewidth(0.8)

            # Redraw
            canvas.draw_idle()



