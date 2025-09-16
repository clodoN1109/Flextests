from infrastructure.environment.environment import Env
import tkinter as tk

class Window:
    def __init__(self, root) -> None:
        self.root = root
        self.tk =  root
        self._is_maximized = False
        self._is_transparent = False
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
        self._drag_data = {"x": 0, "y": 0, "action": None}

        # Bind events
        self.root.bind("<Motion>", self.on_motion)
        self.root.bind("<ButtonPress-1>", self.on_press)

        return self

    def on_motion(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x, y = event.x_root - self.root.winfo_rootx(), event.y_root - self.root.winfo_rooty()
        b = self.border_size

        if x <= b:
            self._drag_data["action"], cursor = "resize_l", "size_we"
        elif x >= w - b:
            self._drag_data["action"], cursor = "resize_r", "size_we"
        elif y <= b:
            self._drag_data["action"], cursor = "resize_t", "size_ns"
        elif y >= h - b:
            self._drag_data["action"], cursor = "resize_b", "size_ns"
        else:
            self._drag_data["action"], cursor = "move", "arrow"

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
        if action.startswith("resize"):
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


    def on_drag(self, event):
        # Only resize if a ghost exists
        if not hasattr(self, "ghost_frame"):
            return

        dx = event.x_root - self._drag_data["x"]
        dy = event.y_root - self._drag_data["y"]
        x, y, w, h = (self._drag_data["orig_x"], self._drag_data["orig_y"],
                      self._drag_data["orig_w"], self._drag_data["orig_h"])
        action = self._drag_data["action"]

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
            new_x, new_y = x + (w - new_w), y + (h - new_h)
        elif action == "resize_tr":
            new_w = max(self.min_width, w + dx)
            new_h = max(self.min_height, h - dy)
            new_y = y + (h - new_h)
        elif action == "resize_bl":
            new_w = max(self.min_width, w - dx)
            new_h = max(self.min_height, h + dy)
            new_x = x + (w - new_w)

        # Update ghost window
        self.ghost_frame.geometry(f"{new_w}x{new_h}+{new_x}+{new_y}")
        self.root.bind("<ButtonRelease-1>", self.on_release)


    def on_release(self, event):
        if hasattr(self, "ghost_frame"):
            # Apply ghost geometry
            self.root.geometry(self.ghost_frame.geometry())
            self.ghost_frame.withdraw()

            # Update drag references so move works again
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
        if self.tk.state() != "iconic":  # not minimized
            if not self.tk.overrideredirect():
                self.tk.overrideredirect(True)

        # Schedule the next check
        self.tk.after(interval_ms, self.ensure_overrideredirect, interval_ms)


