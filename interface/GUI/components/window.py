from application.app import App
from infrastructure.environment.environment import Env
import tkinter as tk
from interface.GUI.components.panes import Panes
from interface.GUI.components.title_bar import TitleBar
from interface.GUI.gui_config import GUIConfig
from interface.GUI.gui_styles import GUIStyle

class Window:
    def __init__(self, root, style: GUIStyle, app: App, config: GUIConfig) -> None:
        # elements
        self.title_bar:TitleBar|None = None
        self.panes = None

        self.root = root
        self.tk = root
        self.app = app
        self.config: GUIConfig = config
        self.style = style
        self.ensure_overrideredirect()

    def render(self, title: str, window_width: int, window_height: int):
        # Remove native decorations
        self.root.overrideredirect(True)
        self.root.title(title)

        # Get screen dimensions
        screen = Env.get_window()
        screen_width = screen.get('screen_width', window_width)
        screen_height = screen.get('screen_height', window_height)

        # Limit window size to screen size
        width = min(window_width, screen_width)
        height = min(window_height, screen_height)

        # Compute top-left coordinates to center the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window_width = width
        self.window_height = height

        # Apply geometry
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # -------------------------
        # Make window draggable & resizable
        # -------------------------
        self.min_width = 200
        self.min_height = 150
        self.border_size = 8
        # drag data will store info for move/resize operations
        self._drag_data = {"x": 0, "y": 0, "action": None}
        # Bind events
        self.root.bind("<Motion>", self.on_motion)
        self.root.bind("<ButtonPress-1>", self.on_press)

        # Render elements
        self.title_bar = TitleBar(self.tk, self.style, self).render()
        self.panes = Panes(self.tk, self.style, self.app).render()

        return self

    # -------------------------
    # Mouse & drag handlers
    # -------------------------
    def on_motion(self, event):
        """
        Called whenever the mouse moves over the window. Decides which action
        (move / resize side / resize corner) should occur if user presses.
        Also sets an appropriate cursor.
        """
        if self.event_in_paned_content(event):
            self.root.config(cursor="arrow")
            self._drag_data["action"] = None
            return
        try:
            w, h = self.root.winfo_width(), self.root.winfo_height()
            x = event.x_root - self.root.winfo_rootx()
            y = event.y_root - self.root.winfo_rooty()
            b = self.border_size
        except Exception:
            # If window info not available, default to move cursor
            self.root.config(cursor="arrow")
            self._drag_data["action"] = "move"
            return

        # Determine if pointer is near edges - consider corners first
        on_left = x <= b
        on_right = x >= (w - b)
        on_top = y <= b
        on_bottom = y >= (h - b)

        cursor = "arrow"
        action = "move"

        # corners
        if on_left and on_top:
            action, cursor = "resize_tl", "size_nw_se"
        elif on_right and on_top:
            action, cursor = "resize_tr", "size_ne_sw"
        elif on_left and on_bottom:
            action, cursor = "resize_bl", "size_ne_sw"
        elif on_right and on_bottom:
            action, cursor = "resize_br", "size_nw_se"
        # edges
        elif on_left:
            action, cursor = "resize_l", "size_we"
        elif on_right:
            action, cursor = "resize_r", "size_we"
        elif on_top:
            action, cursor = "resize_t", "size_ns"
        elif on_bottom:
            action, cursor = "resize_b", "size_ns"
        else:
            action, cursor = "move", "arrow"

        self._drag_data["action"] = action
        self.root.config(cursor=cursor)

    def on_press(self, event):

        action = self._drag_data.get("action", "")

        # Record mouse and window start positions for both move and resize
        self._drag_data["x"], self._drag_data["y"] = event.x_root, event.y_root
        self._drag_data["orig_x"] = self.root.winfo_x()
        self._drag_data["orig_y"] = self.root.winfo_y()
        self._drag_data["orig_w"] = self.root.winfo_width()
        self._drag_data["orig_h"] = self.root.winfo_height()

        # Only create ghost Toplevel if this is a resize
        if hasattr(action, "startswith") and action.startswith("resize"):
            self.root.bind("<B1-Motion>", self.on_drag)

            if not hasattr(self, "ghost_frame"):
                self.ghost_frame = tk.Toplevel(self.root)
                self.ghost_frame.overrideredirect(True)
                self.ghost_frame.attributes("-alpha", 0.3)  # semi-transparent
                self.ghost_frame.config(bg="#1f77b4")  # visible ghost for testing

            # Match original window size/position
            self.ghost_frame.geometry(
                f"{self._drag_data['orig_w']}x{self._drag_data['orig_h']}+"
                f"{self._drag_data['orig_x']}+{self._drag_data['orig_y']}"
            )
            self.ghost_frame.deiconify()
            self.ghost_frame.lift()

    def on_move(self, event):
        """
        Move the window while the mouse button is held down (live).
        """
        # compute delta from original press
        dx = event.x_root - self._drag_data["x"]
        dy = event.y_root - self._drag_data["y"]

        new_x = self._drag_data["orig_x"] + dx
        new_y = self._drag_data["orig_y"] + dy

        # Optionally clamp to screen bounds
        screen = Env.get_window()
        screen_w = screen.get("screen_width", None)
        screen_h = screen.get("screen_height", None)
        if screen_w is not None and screen_h is not None:
            # ensure the window doesn't go fully off-screen (optional)
            new_x = max(0, min(new_x, screen_w - self.root.winfo_width()))
            new_y = max(0, min(new_y, screen_h - self.root.winfo_height()))

        self.root.geometry(f"+{new_x}+{new_y}")

    def on_drag(self, event):
        """
        Resize the ghost_frame according to the pressed corner/edge and current mouse.
        """
        # If ghost not created, nothing to do
        if not hasattr(self, "ghost_frame") or self.ghost_frame is None:
            return

        dx = event.x_root - self._drag_data["x"]
        dy = event.y_root - self._drag_data["y"]

        x = self._drag_data["orig_x"]
        y = self._drag_data["orig_y"]
        w = self._drag_data["orig_w"]
        h = self._drag_data["orig_h"]
        action = self._drag_data.get("action", "")

        new_x, new_y, new_w, new_h = x, y, w, h

        if action == "resize_r":
            new_w = max(self.min_width, w + dx)
        elif action == "resize_b":
            new_h = max(self.min_height, h + dy)
        elif action == "resize_br":
            new_w = max(self.min_width, w + dx)
            new_h = max(self.min_height, h + dy)
        elif action == "resize_l":
            new_w = max(self.min_width, w - dx)
            new_x = x + (w - new_w)
        elif action == "resize_t":
            new_h = max(self.min_height, h - dy)
            new_y = y + (h - new_h)
        elif action == "resize_tl":
            new_w = max(self.min_width, w - dx)
            new_h = max(self.min_height, h - dy)
            new_x = x + (w - new_w)
            new_y = y + (h - new_h)
        elif action == "resize_tr":
            new_w = max(self.min_width, w + dx)
            new_h = max(self.min_height, h - dy)
            new_y = y + (h - new_h)
        elif action == "resize_bl":
            new_w = max(self.min_width, w - dx)
            new_h = max(self.min_height, h + dy)
            new_x = x + (w - new_w)

        # Update ghost geometry
        self.ghost_frame.geometry(f"{new_w}x{new_h}+{new_x}+{new_y}")
        self.root.bind("<ButtonRelease-1>", self.on_release)

    def on_release(self, event):
        if hasattr(self, "ghost_frame"):
            # Apply ghost geometry
            self.root.geometry(self.ghost_frame.geometry())
            self.ghost_frame.withdraw()

            # Update drag reference so move works again
            self._drag_data["orig_x"] = self.root.winfo_x()
            self._drag_data["orig_y"] = self.root.winfo_y()
            self._drag_data["orig_w"] = self.root.winfo_width()
            self._drag_data["orig_h"] = self.root.winfo_height()
        self.root.unbind("<ButtonRelease-1>")
        self.root.unbind("<B1-Motion>")

    def ensure_overrideredirect(self, interval_ms: int = 100):
        """
        Ensure the window stays in overrideredirect mode.
        This checks every `interval_ms` milliseconds.
        """
        # Only apply if the window is visible
        try:
            if self.tk.state() != "iconic":  # not minimized
                # calling with no arg should return current value; set True only if False
                if not self.tk.overrideredirect():
                    self.tk.overrideredirect(True)
        except Exception:
            # Some platforms may raise if called too early; ignore
            try:
                self.tk.overrideredirect(True)
            except Exception:
                pass

        # Schedule the next check
        try:
            self.tk.after(interval_ms, self.ensure_overrideredirect, interval_ms)
        except Exception:
            pass

    def event_in_paned_content(self, event):
        """
        Returns True if the event is inside the PanedWindow content area,
        but **not near the edges** (where window resize is expected).
        """
        if not self.panes or not self.panes.paned_window:
            return False

        pw = self.panes.paned_window
        x, y = event.x_root, event.y_root
        px1, py1 = pw.winfo_rootx(), pw.winfo_rooty()
        px2, py2 = px1 + pw.winfo_width(), py1 + pw.winfo_height()

        # define "inner area" inside PanedWindow where sash moves happen
        margin = 4  # pixels near edge still count as window resize
        return (px1 + margin < x < px2 - margin) and (py1 + margin < y < py2 - margin)