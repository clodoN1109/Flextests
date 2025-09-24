from tkinter import ttk
import tkinter as tk
from infrastructure.environment.environment import Env
from interface.GUI.components.button import Button
from interface.GUI.gui_styles import GUIStyle


class TitleBar:

    def __init__(self, window_tk, style: GUIStyle, window):
        self.window = window
        self.window_tk = window_tk
        self.style = style
        self._is_maximized = False
        self._is_transparent = False

    def render(self):
        # Title bar frame
        title_bar = ttk.Frame(self.window_tk)
        title_bar.pack(fill="x")

        icon_path = f"{Env.get_script_path()}/../assets/icons/logo_{self.style.prefix}_96px.png"
        self.set_logo_image(title_bar, icon_path)

        # Title text (align left)
        self.window_tk.title_label = ttk.Label(
            title_bar, text="", anchor="w", font=("Courier", 10, "italic")
        )
        # Use asymmetric pady → smaller bottom, bigger top
        self.window_tk.title_label.pack(side="left", padx=5, pady=(2, 1))

        # Control buttons
        btn_frame = ttk.Frame(title_bar)
        btn_frame.pack(side="right", padx=5, pady=(2, 1))

        style = ttk.Style()
        style.configure("TitleBar.TButton", relief="flat", padding=4)

        Button(btn_frame, "○/⬤", self._toggle_transparency, width=10).render()
        Button(btn_frame, "☽/☀", self.toggle_dark_mode, width=10).render()
        Button(btn_frame, "🗕", self._minimize, width=10).render()
        Button(btn_frame, "🗖", self._toggle_maximize, width=10).render()
        Button(btn_frame, "✕", self.window_tk.destroy, width=10).render()

        self.window_tk.title_separator = tk.Frame(
            self.window_tk,
            height=5,  # thinner separator looks crisper
            bd=0,
            bg="#ff0000"
        )
        self.window_tk.title_separator.pack(fill="x", side="top")

        # Enable dragging by clicking the title area
        def start_move(event):
            self.window_tk._x = event.x
            self.window_tk._y = event.y

        def on_move(event):
            x = self.window_tk.winfo_pointerx() - self.window_tk._x
            y = self.window_tk.winfo_pointery() - self.window_tk._y
            self.window_tk.geometry(f"+{x}+{y}")

        # Bind dragging to both the title label and the icon (if present)
        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", on_move)
        self.window_tk.title_label.bind("<Button-1>", start_move)
        self.window_tk.title_label.bind("<B1-Motion>", on_move)
        if icon_path:
            self.icon_label.bind("<Button-1>", start_move)
            self.icon_label.bind("<B1-Motion>", on_move)

        return self

    def _minimize(self):
        self.window_tk.update_idletasks()
        # Enables the OS window management before calling iconify.
        self.window_tk.overrideredirect(False)
        self.window_tk.iconify()


    def _toggle_transparency(self):
        if self._is_transparent:
            self.window_tk.attributes("-alpha", 1)
            self._is_transparent = False
        else:
            self.window_tk.attributes("-alpha", 0.9)
            self._is_transparent = True


    def _toggle_maximize(self):
        if self._is_maximized:
            self.window_tk.geometry(self.window_tk._restore_geometry)
            self._is_maximized = False
        else:
            self.window_tk._restore_geometry = self.window_tk.geometry()
            self.window_tk.geometry(f"{self.window_tk.winfo_screenwidth()}x{self.window_tk.winfo_screenheight()}+0+0")
            self._is_maximized = True

    def toggle_dark_mode(self):
        self.style.toggle_dark_mode(self.window)
        self.update_logo_image()

    def set_logo_image(self, frame, icon_path):
        try:
            self.icon_image = tk.PhotoImage(file=icon_path)  # keep reference
            self.icon_label = ttk.Label(frame, image=self.icon_image)
            self.icon_label.pack(side="left", padx=(5, 2), pady=(4, 4))
        except Exception as e:
            print(f"Failed to load icon: {e}")

    def update_logo_image(self):
        icon_path = f"{Env.get_script_path()}/../assets/icons/logo_{self.style.prefix}_96px.png"
        self.icon_image = tk.PhotoImage(file=icon_path)  # overwrite reference
        self.icon_label.configure(image=self.icon_image)
