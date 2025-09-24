from mimetypes import inited
from tkinter import ttk, filedialog
import tkinter as tk
from application.app import App
from domain.test import Test
from infrastructure.environment.environment import Env
from interface.GUI.components.button import Button
from interface.GUI.components.dropdown_selector import DropdownSelector
from interface.GUI.components.form_field import FormField
from interface.GUI.components.output_pane import OutputPane
from interface.GUI.components.section_title import SectionTitle
from interface.GUI.gui_styles import GUIStyle


class InputPane:
    def __init__(self, panned_window, initial_width, style: GUIStyle, app: App, output_pane: OutputPane) -> None:

        screen = Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

        self.initial_width = initial_width
        self.app = app
        self.style = style

        # elements
        self.panned_window = panned_window
        self.controller_section_title     = None
        self.test_selector = None
        self.new_test_button = None
        self.configurations_section_title = None
        self.statistics_section_title     = None
        self.scalability_button = None
        self.external_source_button = None
        self.update_references_button = None
        self.domain_size_field = None
        self.number_of_runs_field = None
        self.file_field = None
        self.external_source_var = None
        self.data_points_field = None
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
            ("  🖋️", self.edit_test_form, 4)
        )
        self.test_selector.render()

        self.new_test_button = Button(
            self.controller_section_title.target_frame,
            "➕",
            self.new_test_form,
            4
        )
        self.new_test_button.render()

        self.run_test_button = Button(
            self.controller_section_title.target_frame,
            "🞂",
            self.run_selected_test,
            4
        )
        self.run_test_button.render()

        # -------------------- Configurations Section --------------------
        self.configurations_section_title = SectionTitle(self.pane_tk, "Configurations").render()
        configurations_frame = self.configurations_section_title.target_frame  # Shortcut

        # Row 0 - Criteria
        tk.Label(configurations_frame, text="criteria:").grid(row=0, column=0, padx=2, pady=3, sticky="w")

        # Row 1 - Max Duration
        max_duration_var = tk.StringVar()
        max_duration_field = FormField(configurations_frame, 1, "max duration:", max_duration_var, "seconds")

        # Row 2 - Max Memory
        max_memory_var = tk.StringVar()
        max_memory_field = FormField(configurations_frame, 2, "max memory:", max_memory_var, "MB")

        # Row 3 - Mean Memory
        mean_memory_var = tk.StringVar()
        mean_memory_field = FormField(configurations_frame, 3, "mean memory:", mean_memory_var, "MB")

        # Row 4 - Compliance
        compliance_var = tk.StringVar()
        compliance_field = FormField(configurations_frame, 4, "compliance:", compliance_var, "%")

        # --- References Label ---
        tk.Label(configurations_frame, text="references:").grid(
            row=5, column=0, padx=2, pady=5, sticky="w"
        )
        # --- File Path (Text Field with Browse Button) ---
        file_var = tk.StringVar()

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

        self.file_field = FormField(
            configurations_frame,
            row=6,
            label_text="source:",
            variable=file_var,
            right_widget_fn=lambda parent: browse_file(parent, file_var),
            width=14
        )
        # --- Data Points (Integer Field) ---
        data_points_var = tk.IntVar()
        self.data_points_field = FormField(
            configurations_frame,
            row=7,
            label_text="data:",
            variable=data_points_var,
            unit="points"
        )
        self.update_references_button = Button(
            configurations_frame,
            "💾",
            lambda: self.update_references(),
            8,
            "grid",
            {"row": 8, "column": 1, "padx": 0, "pady": 10}
        )
        self.update_references_button.render()

        # -------------------- Statistics Section --------------------
        self.statistics_section_title = SectionTitle(self.pane_tk, "Statistics").render()
        self.statistics_frame = self.statistics_section_title.target_frame

        # --- Variable selector ---
        self.variable_selector = DropdownSelector(
            self.statistics_frame,
            "variables",
            None,
            10
        )
        self.variable_selector.render()
        self.variable_selector.combobox.configure(values=["duration", "max memory", "mean memory", "compliance"])
        self.variable_selector.combobox.set("")

        # --- Plot selector ---
        self.plot_selector = DropdownSelector(
            self.statistics_frame,
            "plots",
            ("🞂", lambda: self.plot(), 4)
        )
        self.plot_selector.render()
        self.plot_selector.combobox.configure(values=["series", "distribution"])
        self.plot_selector.combobox.set("series")

        # --- Resolution Spinbox (only for distribution plots) ---
        self.resolution_var = tk.IntVar(value=2)  # default value
        self.resolution_label = tk.Label(self.statistics_frame, text="resolution:")
        self.resolution_spinbox = tk.Spinbox(
            self.statistics_frame,
            from_=0,
            to=10,
            textvariable=self.resolution_var,
            width=5
        )

        # --- Callback to show/hide resolution depending on plot ---
        def update_resolution_visibility(*args):
            plot = self.plot_selector.combobox.get()
            if plot == "distribution":
                self.resolution_label.pack(side="left", padx=(12, 3), pady=3)
                self.resolution_spinbox.pack(side="left", padx=(2, 5), pady=3)
            else:
                self.resolution_label.pack_forget()
                self.resolution_spinbox.pack_forget()

        self.plot_selector.combobox.bind("<<ComboboxSelected>>", update_resolution_visibility)
        update_resolution_visibility()  # initial visibility

        self.update_all_sections()
        return self

    def run_selected_test(self):
        selected_test_name = self.get_selected_test_name()
        self.app.run_test(
            selected_test_name, 10
        )

    def update_references(self):
        pass

    def plot(self):
        print(2)
        pass

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
        popup.iconphoto(False, tk.PhotoImage(file=f"{Env.base_dir()}/interface/GUI/assets/icons/icon.png"))

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

    def update_all_sections(self):
        self.update_controller_section()
