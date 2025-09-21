from tkinter import ttk, filedialog
import tkinter as tk
from application.app import App
from domain.test import Test
from infrastructure.environment.environment import Env
from interface.GUI.components.button import Button
from interface.GUI.components.dropdown_selector import DropdownSelector
from interface.GUI.components.output_pane import OutputPane
from interface.GUI.components.section_title import SectionTitle

class InputPane:
    def __init__(self, panned_window, initial_width, style, app: App, output_pane: OutputPane) -> None:
        self.run_test_button = None
        self.controller_section_frame = None
        self.pane_tk = None
        screen = Env.get_window()
        self.screen_width = screen.get("screen_width")
        self.screen_height = screen.get("screen_height")

        self.initial_width = initial_width
        self.panned_window = panned_window
        self.app = app
        self.style = style

        # elements
        self.controller_section_title     = None
        self.test_selector = None
        self.new_test_button = None

        self.configurations_section_title = None
        self.statistics_section_title     = None


    def render(self):
        # Create the left pane container
        self.pane_tk = ttk.Frame(
            self.panned_window,
            width=int(self.screen_width * self.initial_width)
        )
        self.pane_tk.pack_propagate(False)  # prevent frame from shrinking
        self.panned_window.add(self.pane_tk)

        # Controller Section (frame that can be toggled on and off)
        self.controller_section_frame = ttk.Frame(self.pane_tk, padding=8)

        # Section title that can toggle the controller_section_frame
        self.controller_section_title = SectionTitle(
            self.pane_tk,
            "Controller",
            self.controller_section_frame
        )
        self.controller_section_title.render()

        # Widgets go inside controller_section_frame
        self.test_selector = DropdownSelector(
            self.controller_section_frame,
            "tests",
            self.edit_test_form
        )
        self.test_selector.render()
        # --------------------------------
        self.new_test_button = Button(self.controller_section_frame, "➕", self.new_test_form, 4)
        self.new_test_button.render()
        # --------------------------------
        self.run_test_button = Button(self.controller_section_frame, "🞂", self.run_selected_test, 4)
        self.run_test_button.render()
        # ================================

        # Configurations Section
        self.configurations_section_title = SectionTitle(self.pane_tk, "Configurations").render()

        #Statistics Section
        self.statistics_section_title     = SectionTitle(self.pane_tk, "Statistics").render()

        return self

    def run_selected_test(self):
        selected_test_name = self.get_selected_test_name()
        self.app.run_test(
            selected_test_name, 10
        )

    def get_selected_test_name(self):
        return self.test_selector.var.get()

    def get_selected_test(self) -> Test:
        test_name = self.get_selected_test_name()
        return self.app.get_test_by_name(test_name)

    def new_test_form(self):
        self._test_form("new test")

    def edit_test_form(self):
        self._test_form("test editing")

    def _test_form(self, title:str):
        # Create a temporary popup
        popup = tk.Toplevel()
        popup.title(title)
        popup.grab_set()  # make it modal
        popup.iconphoto(False, tk.PhotoImage(file=f"{Env.base_dir()}/interface/GUI/assets/icons/icon.png"))

        width = 372
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

                popup.destroy()  # close the popup
                # self.refresh_observables()
            else:
                tk.messagebox.showerror("Error", "Name and Simulation path are required!")

        # --- Buttons ---
        tk.Button(popup, text="Confirm", command=submit, width=8).grid(row=4, column=1, pady=10, padx=(0,10), sticky="e")
        tk.Button(popup, text="Cancel", command=popup.destroy, width=8).grid(row=4, column=2, pady=10, sticky="w")

        # Focus on the name field
        name_entry.focus()



