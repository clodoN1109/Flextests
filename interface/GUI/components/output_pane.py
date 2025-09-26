import time
import tkinter as tk
from tkinter import ttk
from typing import Any, List
from interface.GUI.gui_styles import GUIStyle
from interface.GUI.models.OutputPaneData import OutputPaneData
from interface.GUI.models.PlotOptions import PlotOptions
from interface.GUI.models.ResultsPlotData import ResultsPlotData
from interface.GUI.models.ResultsSummaryTable import ResultsSummaryTable
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class OutputPane:
    TABS = ("DESCRIPTION", "REFERENCES", "RESULTS", "STATISTICS")

    def __init__(self, container_tk, initial_width: float, style: GUIStyle, app, window) -> None:

        self.container = container_tk
        self.app = app
        self.style = style
        self.window = window

        screen = __import__("infrastructure.environment.environment", fromlist=["Env"]).Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

        self.initial_width = initial_width
        self.pane_tk: ttk.Frame | None = None

        # UI pieces
        self.navbar_frame: ttk.Frame | None = None
        self.content_frame: ttk.Frame | None = None
        self.tab_buttons: dict[str, ttk.Button] = {}
        self.current_tab: str = OutputPane.TABS[0]

        # persistent frames for each tab
        self._frames: dict[str, ttk.Frame] = {}

        # Data placeholder
        self.output_pane_data:OutputPaneData = None

        # plot canvas reference
        self._plot_canvas = None

        # matplotlib references
        self.fig = None
        self.ax = None
        self.canvas = None
        self.plot_title = None
        self.plot_subtitle = None
        self.plot_area = None

        # components
        self.description_textbox: tk.Text | None = None
        self.results_table_frame: ttk.Frame | None = None
        self.summary_frame: ttk.Frame | None = None
        self.references_table_frame: ttk.Frame | None = None
        self.plot_frame = None
        self.warning_label = None


    # ------------------- rendering the static frame -------------------
    def render(self):
        """Create the pane frame and static navbar + content area (grid-only inside)."""
        self.pane_tk = ttk.Frame(self.container, width=int(self.screen_width * self.initial_width))
        self.pane_tk.pack_propagate(False)
        self.container.add(self.pane_tk)

        # Layout: navbar row 0, content_frame row 1
        self.pane_tk.grid_rowconfigure(1, weight=1)
        self.pane_tk.grid_columnconfigure(0, weight=1)

        # navbar frame
        self.navbar_frame = ttk.Frame(self.pane_tk)
        self.navbar_frame.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 2))
        self.navbar_frame.grid_columnconfigure(len(OutputPane.TABS), weight=1)

        # content frame
        self.content_frame = ttk.Frame(self.pane_tk)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # create persistent frames for tabs
        for tab in OutputPane.TABS:
            frame = ttk.Frame(self.content_frame)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            self._frames[tab] = frame

        # navbar buttons
        for idx, tab in enumerate(OutputPane.TABS):
            btn = ttk.Button(self.navbar_frame, text=tab, command=lambda t=tab: self._on_tab_selected(t))
            btn.grid(row=0, column=idx, padx=(0, 6), sticky="w")
            self.tab_buttons[tab] = btn

        self._highlight_active_tab()
        return self.pane_tk

    # ------------------- public update -------------------
    def update(self, output_pane_data: Any):
        self.output_pane_data = output_pane_data
        self._render_current_tab()
        self.style.apply_style(self.window)

    # ------------------- tab management -------------------
    def _on_tab_selected(self, tab_name: str):
        self.clear_warning()
        self.current_tab = tab_name
        self._highlight_active_tab()
        self._render_current_tab()
        self.style.apply_style(self.window)

    def _highlight_active_tab(self):
        for tab, btn in self.tab_buttons.items():
            if tab == self.current_tab:
                btn.state(["pressed"])
            else:
                btn.state(["!pressed"])

    # ------------------- content rendering -------------------
    def _render_current_tab(self):
        for tab, frame in self._frames.items():
            if tab == self.current_tab:
                frame.tkraise()

        if not self.output_pane_data:
            return

        if self.current_tab == "DESCRIPTION":
            self._render_description()
        elif self.current_tab == "REFERENCES":
            self._render_references()
        elif self.current_tab == "RESULTS":
            self._render_results()
        elif self.current_tab == "STATISTICS":
            self._render_statistics()

    # ------------------- DESCRIPTION -------------------
    def _render_description(self):
        frame = self._frames["DESCRIPTION"]
        for child in frame.winfo_children():
            child.destroy()

        text_frame = ttk.Frame(frame)
        text_frame.grid(sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.description_textbox = tk.Text(text_frame, wrap="word", height=10)
        self.description_textbox.insert("1.0", getattr(self.output_pane_data, "test_description", ""))
        self.description_textbox.configure(state="disabled", padx=10, pady=10)
        self.description_textbox.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        vsb = ttk.Scrollbar(text_frame, orient="vertical", command=self.description_textbox.yview)
        self.description_textbox.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns", pady=4)

    # ------------------- REFERENCES -------------------
    def _render_references(self):
        frame = self._frames["REFERENCES"]
        for child in frame.winfo_children():
            child.destroy()

        table_data = getattr(self.output_pane_data, "references_table_data", None)
        if not table_data:
            ttk.Label(frame, text="No references available.").grid(sticky="nsew")
            return

        self.references_table_frame = ttk.Frame(frame)
        self.references_table_frame.grid(row=0, column=0, sticky="nsew")
        self.references_table_frame.grid_rowconfigure(0, weight=1)
        self.references_table_frame.grid_columnconfigure(0, weight=1)
        self._render_table(self.references_table_frame, table_data)

    # ------------------- RESULTS -------------------
    def _render_results(self):
        frame = self._frames["RESULTS"]
        for child in frame.winfo_children():
            child.destroy()

        # table
        self.results_table_frame = ttk.Frame(frame)
        self.results_table_frame.grid(row=0, column=0, sticky="nsew")
        self.results_table_frame.grid_rowconfigure(0, weight=1)
        self.results_table_frame.grid_columnconfigure(0, weight=1)
        self._render_table(self.results_table_frame, getattr(self.output_pane_data, "results_table_data", None))

    def _render_statistics(self):
        plot_data_list: List[ResultsPlotData] = getattr(
            self.output_pane_data, "plot_data", None
        )
        plot_options: PlotOptions = getattr(
            self.output_pane_data, "plot_options", None
        )

        # no data or no options
        if not plot_data_list or not plot_options:
            self.show_warning("No data to display.")
            return
        else:
            self.clear_warning()

        # find the matching variable
        plot_data = next(
            (
                pd
                for pd in plot_data_list
                if pd.variable_name == plot_options.selected_variable
            ),
            None,
        )
        if not plot_data or not plot_data.data:
            self.show_warning("No statistics to display.")
            return
        self.clear_warning()

        # container for plot + summary
        # allow content_frame to expand its child
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # container for plot + summary
        self.plot_frame = ttk.Frame(self.content_frame)
        self.plot_frame.grid(row=0, column=0, sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)  # plot row expands
        self.plot_frame.grid_rowconfigure(1, weight=0)  # summary row stays compact
        self.plot_frame.grid_columnconfigure(0, weight=1)

        # plot area
        self.plot_area = ttk.Frame(self.plot_frame)
        self.plot_area.grid(row=0, column=0, sticky="nsew")

        # render matplotlib figure inside plot_area
        self.canvas = self._render_plot_with_matplotlib(
            self.plot_area,
            plot_data,
            plot_type=plot_options.plot_type,
            resolution=plot_options.resolution,
        )

        # ensure the canvas stretches
        if hasattr(self.canvas, "get_tk_widget"):
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # summary
        self.summary_frame = ttk.Frame(self.plot_frame)
        self.summary_frame.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        self._render_summary(
            getattr(self.output_pane_data, "results_summary_data", None),
            self.summary_frame,
        )

    def _render_plot_with_matplotlib(
            self,
            parent,
            plot_data: ResultsPlotData,
            plot_type: str,
            resolution: int
    ):
        # Create figure + axis
        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)  # larger base size

        # Clear previous plot
        self.ax.clear()

        # --- Plot type handling ---
        if plot_type == "series":
            self.ax.plot(
                range(len(plot_data.data)),
                plot_data.data,
                marker="o",
                linestyle="-"
            )
            self.ax.set_xlabel("Index")
            self.ax.set_ylabel(plot_data.variable_name)
            self.ax.xaxis.get_major_locator().set_params(integer=True)

        elif plot_type == "distribution":
            bins = max(1, int(resolution))  # clamp resolution
            self.ax.hist(
                plot_data.data,
                bins=bins,
                edgecolor="black",
                alpha=0.7
            )
            self.ax.set_xlabel(plot_data.variable_name)
            self.ax.set_ylabel("Frequency")

        # --- Titles ---
        if plot_data.title:
            self.plot_title = plot_data.title
            self.ax.set_title(
                self.plot_title,
                fontsize=12,
                fontweight="bold",
                loc="left",
                pad=10,
                color=f"{self.style.primary_fg}"
            )
        if self.output_pane_data.plot_options:
            self.plot_subtitle = self.output_pane_data.plot_options.plot_type
            self.ax.text(
                0,
                1,
                self.plot_subtitle,
                transform=self.ax.transAxes,
                fontsize=9,
                style="italic",
                ha="left",
                va="bottom",
                color=f"{self.style.primary_fg}"
            )

        # --- Styling ---
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.fig.tight_layout()

        # --- Embed into Tkinter ---
        canvas = FigureCanvasTkAgg(self.fig, master=parent)
        widget = canvas.get_tk_widget()

        # let the canvas expand
        widget.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.style.apply_style_to_plot(self.window)
        canvas.draw()

        return canvas
    # ------------------- helpers: table rendering -------------------
    def _render_table(self, parent: ttk.Frame, table_obj: Any):
        """
        Generic renderer for ResultsTable / ReferencesTable style objects:
        - expects table_obj.headers: list[str]
        - expects table_obj.rows: iterable of row-objects where row[h] returns value for header h
        """
        headers = getattr(table_obj, "headers", None)
        rows = getattr(table_obj, "rows", None)
        if headers is None or rows is None:
            if isinstance(table_obj, dict):
                headers = list(table_obj.keys())
                rows = [table_obj]
                self.clear_warning()
            else:
                self.show_warning("No data to display.")
                return
        else:
            self.clear_warning()

        # treeview and scrollbars
        tree = ttk.Treeview(parent, columns=headers, show="headings")
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # create columns
        for h in headers:
            tree.heading(h, text=h)
            # allow column to stretch a bit, initial width guess
            tree.column(h, width=max(60, min(300, int(len(h) * 10))), anchor="w", stretch=True)

        # insert rows
        for r in rows:
            try:
                values = [self._cell_to_string(self._get_row_value(r, h)) for h in headers]
            except Exception:
                values = [self._cell_to_string(self._get_row_value_fallback(r, h)) for h in headers]
            tree.insert("", "end", values=values)

        # layout - place treeview with scrollbars using grid
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew", columnspan=2)

        # ensure parent grid expands treeview
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        if len(parent.winfo_children())>0:
            self._make_sortable_treeview(parent.winfo_children()[0])


    def _get_row_value(self, row_obj: Any, header: str):
        # try dataclass-like or dict-like access
        if hasattr(row_obj, "__getitem__"):
            try:
                return row_obj[header]
            except Exception:
                pass
        # attribute style
        if hasattr(row_obj, header):
            return getattr(row_obj, header)
        # try dict
        if isinstance(row_obj, dict):
            return row_obj.get(header)
        # fallback: try parameters attr (for ReferenceRow/ResultRow)
        if hasattr(row_obj, "parameters") and isinstance(row_obj.parameters, dict):
            return row_obj.parameters.get(header)
        # give None if nothing found
        return None

    def _get_row_value_fallback(self, row_obj: Any, header: str):
        # last-resort fallback tries keys lowercased and underscore
        key = header.strip().lower().replace(" ", "_")
        if hasattr(row_obj, "__getitem__"):
            try:
                return row_obj[key]
            except Exception:
                pass
        if hasattr(row_obj, "parameters") and isinstance(row_obj.parameters, dict):
            return row_obj.parameters.get(key)
        if isinstance(row_obj, dict):
            return row_obj.get(key)
        return None

    def _cell_to_string(self, v: Any) -> str:
        if v is None:
            return "-"
        if isinstance(v, float):
            return f"{v:.4g}"
        return str(v)
    # ------------------- helpers: summary renderer -------------------
    def _render_summary(self, summary_obj: ResultsSummaryTable, parent: ttk.Frame):
        """
        Attempt to show a lightweight summary.
        If it looks like a table (headers/rows) render it as a small Treeview,
        else if it is dict-like or a ResultsSummaryTable, show key: value lines.
        """

        # Case 1: table-like (has headers/rows)
        if getattr(summary_obj, "headers", None) and getattr(summary_obj, "rows", None):
            self._render_table(parent, summary_obj)
            return

        # Case 2: dict-like
        if isinstance(summary_obj, dict):
            left = ttk.Frame(parent)
            left.grid(row=0, column=0, sticky="w")
            for idx, (k, v) in enumerate(summary_obj.items()):
                ttk.Label(left, text=f"{k}:").grid(row=idx, column=0, sticky="w", padx=(0, 6))
                ttk.Label(left, text=str(v)).grid(row=idx, column=1, sticky="w")
            return

        # Case 3: ResultsSummaryTable
        if isinstance(summary_obj, ResultsSummaryTable):
            metrics = [
                ("Sample Size", summary_obj.sample_size),
                ("Effective Instances", summary_obj.effective_instances),
                ("Efficient Instances", summary_obj.efficient_instances),
                ("Compliance Rate", f"{summary_obj.compliance:.2%}"),
            ]
            left = ttk.Frame(parent)
            left.grid(row=0, column=0, sticky="w")
            for idx, (label, value) in enumerate(metrics):
                ttk.Label(left, text=f"{label}:").grid(row=idx, column=0, sticky="w", padx=(0, 6))
                ttk.Label(left, text=str(value)).grid(row=idx, column=1, sticky="w")
            return

        # Fallback: show repr
        ttk.Label(
            parent,
            text=repr(summary_obj),
            wraplength=int(self.screen_width * 0.3)
        ).grid(sticky="w")

    # ------------------- helpers - warnings -------------------

    def show_warning(self, message: str):
        # remove old warning if exists
        self.clear_warning()
        # create new label at the bottom of the common frame
        self.warning_label = ttk.Label(self.pane_tk, text=message, anchor="center")
        self.warning_label.place(relx=0.5, rely=0.5, anchor="center")

    def clear_warning(self):
        if hasattr(self, "warning_label") and self.warning_label is not None:
            self.warning_label.destroy()
            self.warning_label = None

    # ------------------- utility -------------------
    def destroy(self):
        if self.pane_tk:
            try:
                self.pane_tk.destroy()
            except Exception:
                pass
            self.pane_tk = None

    def _clear_content_frame(self):
        for child in self.content_frame.winfo_children():
            child.destroy()
        self.description_textbox = None
        self.results_table_frame = None
        self.summary_frame = None
        self.references_table_frame = None

    @staticmethod
    def _make_sortable_treeview(tree: ttk.Treeview):
        """
        Add click-to-sort capability for a ttk.Treeview.
        """
        tree._sort_column = None  # track current sorted column
        tree._sort_descending = False

        def sort_column(event):
            # Check if click is on a heading
            region = tree.identify_region(event.x, event.y)
            if region != "heading":
                return  # ignore clicks outside headers

            # Identify the column clicked
            col = tree.identify_column(event.x)
            col_index = int(col.replace("#", "")) - 1  # "#1", "#2", ...
            col_id = tree["columns"][col_index]

            # Get all items
            data = [(tree.set(k, col_id), k) for k in tree.get_children("")]

            # Try numeric conversion
            try:
                data = [(float(v), k) for v, k in data]
            except ValueError:
                pass  # leave as strings if not numbers

            # Determine order
            descending = False
            if tree._sort_column == col_id:
                descending = not tree._sort_descending
            tree._sort_column = col_id
            tree._sort_descending = descending

            # Sort data
            data.sort(reverse=descending)

            # Reorder rows
            for index, (_, k) in enumerate(data):
                tree.move(k, "", index)

        # Bind clicks on the **heading area only**
        tree.bind("<Button-1>", sort_column)
