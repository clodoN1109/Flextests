import os
import sys
import traceback
from tkinter import ttk, filedialog
import tkinter as tk
from typing import List
from application.app import App
from domain.test import Test
from infrastructure.environment.environment import Env
from interface.GUI.components.button import Button
from interface.GUI.components.dropdown_selector import DropdownSelector
from interface.GUI.components.form_field import FormField
from interface.GUI.components.output_pane import OutputPane
from interface.GUI.components.section_title import SectionTitle
from interface.GUI.gui_styles import GUIStyle
from interface.GUI.models.OutputPaneData import OutputPaneData
from interface.GUI.models.PlotOptions import PlotOptions
from interface.GUI.models.ReferencesTable import ReferencesTable
from interface.GUI.models.ResultsPlotData import ResultsPlotData
from interface.GUI.models.ResultsTable import ResultsTable
from interface.GUI.models.ResultsSummaryTable import ResultsSummaryTable


class InputPane:
    def __init__(self, panned_window, initial_width, style: GUIStyle, app: App, output_pane: OutputPane, window:"Window") -> None:

        screen = Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

        self.initial_width = initial_width
        self.app = app
        self.style = style
        self.window = window
        self.output_pane = output_pane
        self.output_pane_data: OutputPaneData = None

        # gui elements
        self.panned_window = panned_window
        self.controller_section_title     = None
        self.test_selector = None
        self.new_test_button = None
        self.configurations_section_title = None
        self.statistics_section_title     = None
        self.scalability_button = None
        self.domain_size_field = None
        self.number_of_runs_field = None
        self.reference_source = None
        self.reference_source_var = None
        self.reference_data_points_var = None
        self.configurations_section_frame = None
        self.run_test_button = None
        self.controller_section_frame = None
        self.pane_tk = None
        self.statistics_frame = None
        self.plot_selector = None
        self.resolution_var = None
        self.resolution_label = None
        self.resolution_spinbox = None
        self.variable_selector = None
        self.max_duration_var = None
        self.compliance_var = None
        self.max_memory_var = None
        self.mean_memory_var = None
        self.test_data_points_var = None
        self.data_points_label = None
        self.test_data_spinbox = None


    def render(self):
        # Create the left pane container
        self.pane_tk = ttk.Frame(
            self.panned_window,
            width=int(self.screen_width * self.initial_width)
        )
        self.pane_tk.pack_propagate(False)  # prevent frame from shrinking
        self.panned_window.add(self.pane_tk)

        # -------------------- Controller Section --------------------
        self.controller_section_title = SectionTitle(self.pane_tk, "Controller").render()

        # Widgets go inside controller_section_title.target_frame
        self.test_selector = DropdownSelector(
            self.controller_section_title.target_frame,
            "tests",
            ("  🖋️", self.edit_test_form, 4),
            manager="pack"
        )
        self.test_selector.render()
        self.test_selector.combobox.bind("<<ComboboxSelected>>", self.load_test_config, add="+")
        self.test_selector.combobox.bind("<<ComboboxSelected>>", self.present_test_info, add="+")

        self.new_test_button = Button(
            self.controller_section_title.target_frame,
            "➕",
            self.new_test_form,
            4,
            manager="pack"
        )
        self.new_test_button.render()

        self.run_test_button = Button(
            self.controller_section_title.target_frame,
            "🞂",
            self.run_selected_test,
            4,
            manager="pack"
        )
        self.run_test_button.render()

        # -------------------- Configurations Section --------------------
        self.configurations_section_title = SectionTitle(self.pane_tk, "Configurations").render()
        self.configurations_section_title.toggle()
        configurations_frame = self.configurations_section_title.target_frame  # Shortcut

        # Row 0 - Criteria
        tk.Label(configurations_frame, text="criteria:").grid(row=0, column=0, padx=2, pady=3, sticky="w")

        # Row 1 - Max Duration
        self.max_duration_var = tk.DoubleVar()
        max_duration_field = FormField(configurations_frame, 1, "max duration:", self.max_duration_var, "seconds")

        # Row 2 - Max Memory
        self.max_memory_var = tk.DoubleVar()
        max_memory_field = FormField(configurations_frame, 2, "max memory:", self.max_memory_var, "MB")

        # Row 3 - Mean Memory
        self.mean_memory_var = tk.DoubleVar()
        mean_memory_field = FormField(configurations_frame, 3, "mean memory:", self.mean_memory_var, "MB")

        # Row 4 - Compliance
        self.compliance_var = tk.DoubleVar()
        compliance_field = FormField(configurations_frame, 4, "compliance:", self.compliance_var, "%")

        # --- Reference Label ---
        tk.Label(configurations_frame, text="reference:").grid(
            row=5, column=0, padx=2, pady=5, sticky="w"
        )
        # --- File Path (Text Field with Browse Button) ---
        self.reference_source_var = tk.StringVar()
        def browse_file(parent, variable):
            def callback():
                path = filedialog.askopenfilename(
                    title="Select Reference Source",
                    filetypes=[
                        ("Scripts/JSON", "*.json *.py *.ps1 *.sh *.bat *.rb"),
                        ("All Files", "*.*")
                    ]
                )
                if path:
                    variable.set(path)

            return tk.Button(parent, text="🗁", command=callback, width=4)
        self.reference_source = FormField(
            configurations_frame,
            row=6,
            label_text="source:",
            variable=self.reference_source_var,
            right_widget_fn=lambda parent: browse_file(parent, self.reference_source_var),
            width=14
        )
        # --- Reference Sample - Data Points (Integer Field) ---
        self.reference_data_points_var = tk.IntVar()
        self.data_points_field = FormField(
            configurations_frame,
            row=7,
            label_text="sample:",
            variable=self.reference_data_points_var,
            unit="data points"
        )

        # -------------------- Statistics Section --------------------
        self.statistics_section_title = SectionTitle(self.pane_tk, "Statistics").render()
        self.statistics_section_title.toggle()
        self.statistics_frame = self.statistics_section_title.target_frame

        # Row counter for consistent placement
        row = 0

        # --- Variable selector ---
        self.variable_selector = DropdownSelector(
            self.statistics_frame,
            "variables:",
            row=row,
            manager="grid"
        )
        self.variable_selector.render(values=["duration", "max memory", "mean memory", "min memory"])
        self.variable_selector.combobox.bind("<<ComboboxSelected>>", self.update_selected_variable)

        row += 1

        # --- Test Sample Spinbox ---
        self.test_data_points_var = tk.IntVar(value=1)
        self.data_points_label = tk.Label(self.statistics_frame, text="sample:")
        self.data_points_label.grid(row=row, column=0, padx=0, pady=2, sticky="w")
        self.test_data_spinbox = tk.Spinbox(
            self.statistics_frame,
            from_=0,
            to=100000,
            textvariable=self.test_data_points_var,
            width=5,
            command=self.run_selected_test
        )
        self.test_data_spinbox.bind("<Return>", self.update_test_sample)

        self.test_data_spinbox.grid(row=row, column=1, padx=0, pady=2, sticky="w")
        self.data_points_label = tk.Label(self.statistics_frame, text="data points")
        self.data_points_label.grid(row=row, column=1, padx=50, pady=2, sticky="w")
        row += 1

        # --- Plot selector ---
        self.plot_selector = DropdownSelector(
            self.statistics_frame,
            "plots:",
            None,
            row=row,
            manager="grid",
        )
        self.plot_selector.render(values=["series", "distribution"])
        row += 1

        # --- Resolution Spinbox ---
        self.resolution_var = tk.IntVar(value=2)
        self.resolution_var.trace_add("write", lambda *args: self.update_plot_resolution())
        self.resolution_label = tk.Label(self.statistics_frame, text="resolution:")
        self.resolution_spinbox = tk.Spinbox(
            self.statistics_frame,
            from_=0,
            to=10,
            textvariable=self.resolution_var,
            width=5
        )
        resolution_row = row
        row += 1  # increment row counter for next widget

        def update_resolution_visibility(*args):
            plot = self.plot_selector.combobox.get()
            if plot == "distribution":
                self.resolution_label.grid(row=resolution_row, column=0, padx=(0, 3), pady=3, sticky="w")
                self.resolution_spinbox.grid(row=resolution_row, column=1, padx=(2, 5), pady=3, sticky="w")
            else:
                self.resolution_label.grid_remove()
                self.resolution_spinbox.grid_remove()

        self.plot_selector.combobox.bind("<<ComboboxSelected>>", update_resolution_visibility, add="+")
        self.plot_selector.combobox.bind("<<ComboboxSelected>>", self.update_plot_type, add="+")
        update_resolution_visibility()

        self.update_all_sections()
        return self

    def present_test_info(self, event=None):
        selected_test_name = self.get_selected_test_name()
        if not selected_test_name:
            return

        selected_test:Test = self.app.get_test_by_name(selected_test_name)
        test_description = selected_test.description
        references_table_data:ReferencesTable = ReferencesTable.get_references_table(selected_test)

        self.output_pane_data = OutputPaneData(test_description, references_table_data)
        self.send_data_to_output_pane()

    def run_selected_test(self):

        try:
            self.window.footer.set_state("processing")

            self.save_test_config()

            selected_test_name = self.get_selected_test_name()
            if not selected_test_name:
                return

            completed_test = self.app.run_test(selected_test_name, self.test_data_points_var.get())

            test_description:str = completed_test.description

            plot_data:List[ResultsPlotData] = []
            for variable_name in ["duration", "max memory", "mean memory", "min memory"]:
                plot_data.append(self.get_results_plot_data(variable_name, completed_test))

            results_summary_data:ResultsSummaryTable = self.get_results_summary(completed_test)

            results_table_data:ResultsTable = ResultsTable.get_results_table(completed_test)

            references_table_data:ReferencesTable = ReferencesTable.get_references_table(completed_test)

            plot_options = PlotOptions(self.variable_selector.var.get(), self.plot_selector.var.get(), int(self.resolution_spinbox.get()))

            self.output_pane_data = OutputPaneData(test_description,
                                                   references_table_data,
                                                   results_summary_data,
                                                   results_table_data,
                                                   plot_data,
                                                   plot_options)

            self.send_data_to_output_pane()

            self.window.footer.set_state("idle")

        except Exception as e:
            tb = sys.exc_info()[2]  # traceback object
            last_frame = traceback.extract_tb(tb)[-1]
            filename = last_frame.filename
            lineno = last_frame.lineno
            func_name = last_frame.name
            self.window.footer.set_state(
                "error",
                f"{e} (File: {filename}, line: {lineno}, in {func_name})"
            )


    def update_test_sample(self, event=None):
        self.run_selected_test()

    def send_data_to_output_pane(self):
        self.output_pane.update(self.output_pane_data)

    def update_plot_type(self, event=None):
        if self.output_pane_data is not None:
            self.output_pane_data.plot_options.plot_type = self.plot_selector.var.get()
            self.send_data_to_output_pane()

    def update_plot_resolution(self, event=None):
        if self.output_pane_data is not None:
            try:
                self.output_pane_data.plot_options.resolution = int(self.resolution_spinbox.get())
            except ValueError:
                self.output_pane_data.plot_options.resolution = 0  # fallback if user typed junk
            self.send_data_to_output_pane()

    def update_selected_variable(self, event=None):
        if self.output_pane_data is not None:
            self.output_pane_data.plot_options.selected_variable = self.variable_selector.var.get()
            self.send_data_to_output_pane()

    @staticmethod
    def get_results_summary(completed_test):
        return ResultsSummaryTable(completed_test.stats)

    def get_results_plot_data(self, variable_name, completed_test: Test)-> ResultsPlotData:
        if variable_name is not None and variable_name != "":
            title = f"{variable_name}".upper()
            subtitle = self.plot_selector.combobox.get().upper()
            data = [result.simulation.stats.get_value_by_name(variable_name) for result in completed_test.results]
            return ResultsPlotData(title, subtitle, variable_name, data)
        else:
            return ResultsPlotData()

    def get_selected_test_name(self):
        return self.test_selector.var.get()

    def get_selected_test(self) -> Test:
        test_name = self.get_selected_test_name()
        return self.app.get_test_by_name(test_name)

    def new_test_form(self):
        self._test_form("new test")

    def edit_test_form(self):
        test_name = self.get_selected_test_name()
        if len(test_name) != 0:
           self._test_form("test editing")
        else:
            self.new_test_form()

    def _test_form(self, title:str):
        # Create a temporary popup
        popup = tk.Toplevel()
        popup.title(title)
        popup.grab_set()  # make it modal
        
        # Set popup icon
        pyinstaller_path = f"{Env.base_dir()}/_internal/interface/GUI/assets/icons/icon.png"
        pythonic_path    = f"{Env.base_dir()}/interface/GUI/assets/icons/icon.png"
        path = None
        if os.path.exists(pyinstaller_path):
            path = pyinstaller_path
        elif os.path.exists(pythonic_path):
            path = pythonic_path
        if path:
            popup.iconphoto(False, tk.PhotoImage(file=path))

        width = 382
        height = 225
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        # --- Name ---
        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_var = tk.StringVar()
        name_entry = tk.Entry(popup, textvariable=name_var, width=45)
        name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # --- Description (multiline) ---
        tk.Label(popup, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="ne")
        description_text = tk.Text(popup, width=34, height=4, wrap="word")
        description_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # --- Simulation ---
        tk.Label(popup, text="Simulation:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        path_var = tk.StringVar()
        path_entry = tk.Entry(popup, textvariable=path_var, width=33)
        path_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        if title == "test editing":
            name_var.set(self.get_selected_test().name)
            description_text.delete("1.0", tk.END)  # clear first
            description_text.insert("1.0", self.get_selected_test().description)
            path_var.set(self.get_selected_test().simulation.script_path)


        def browse_path():
            path = filedialog.askopenfilename(
                title="Select Simulation File",
                filetypes=[
                    ("Supported scripts", "*.py *.ps1 *.sh *.bat *.rb"),
                    ("All files", "*.*"),
                ]
            )
            if path:
                path_var.set(path)

        browse_btn = tk.Button(popup, text="Browse", command=browse_path, width=8)
        browse_btn.grid(row=2, column=2, padx=(0,0), pady=5, sticky="w")

        tk.Label(
            popup,
            text="(path to a .py, .ps1, .sh, .bat, or .rb file)",
            fg="gray",
            font=("TkDefaultFont", 8)
        ).grid(row=3, column=1, columnspan=2, padx=0, pady=(0, 10), sticky="w")

        def submit():
            name        = name_var.get().strip()
            description = description_text.get("1.0", "end").strip()
            script_location    = path_var.get().strip()
            if name and script_location:
                if title=="new test":
                    self.app.new_test(name, description, script_location)
                elif title=="test editing":
                   self.app.edit_test(self.get_selected_test_name(), name, description, script_location)
                self.update_controller_section(name)

                popup.destroy()  # close the popup
                # self.refresh_observables()
            else:
                tk.messagebox.showerror("Error", "Name and Simulation path are required!")

        def delete_selected_test():
            test_name = self.get_selected_test_name()
            self.app.delete_test(test_name)
            self.update_controller_section("")
            popup.destroy()

        # --- Buttons ---
        if title == "test editing":
            tk.Button(popup, text="Delete", command=delete_selected_test, width=8).grid(row=4, column=0, pady=10, padx=(10,10), sticky="e")
        tk.Button(popup, text="Confirm", command=submit, width=8).grid(row=4, column=1, pady=10, padx=(0,10), sticky="e")
        tk.Button(popup, text="Cancel", command=popup.destroy, width=8).grid(row=4, column=2, pady=10, sticky="w")

        # Focus on the name field
        name_entry.focus()

    def update_controller_section(self, current_item_name=""):
        test_names_list = [test.name for test in self.app.get_tests_list()]
        self.test_selector.combobox.configure(values=test_names_list)
        self.test_selector.combobox.set(current_item_name)
        self.present_test_info()

    def load_test_config(self, event=None):
        selected_test = self.get_selected_test()
        if selected_test:
            self.max_duration_var.set(selected_test.criteria.duration)
            self.max_memory_var.set(selected_test.criteria.max_memory)
            self.mean_memory_var.set(selected_test.criteria.mean_memory)
            self.compliance_var.set(selected_test.criteria.compliance_rate * 100)
            self.reference_source_var.set(selected_test.reference_source
                                           if (selected_test.reference_source is not None) else "")
            self.reference_data_points_var.set(len(selected_test.reference))

    def save_test_config(self):
        selected_test = self.get_selected_test()
        if not selected_test:
            return

        if self.reference_source_var.get() != selected_test.reference_source:
            self.app.set_reference_source(selected_test.name, self.reference_source_var.get())

        if self.reference_data_points_var.get() != len(selected_test.reference):
            self.app.update_reference(selected_test.name, self.reference_data_points_var.get())

        self.app.set_criterion(selected_test.name, "duration", self.max_duration_var.get())
        self.app.set_criterion(selected_test.name, "max_memory", self.max_memory_var.get())
        self.app.set_criterion(selected_test.name, "mean_memory", self.mean_memory_var.get())
        self.app.set_criterion(selected_test.name, "compliance_rate", self.compliance_var.get() / 100)
        self.load_test_config()

    def update_all_sections(self):
        self.update_controller_section()
        self.load_test_config()
