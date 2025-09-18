import inspect
import sys
from pathlib import Path
import platform
import ctypes
import subprocess
import inspect
import sys
from pathlib import Path


class Env:
    @staticmethod
    def get_script_path() -> str:
        """
        Return the directory of the caller script as a POSIX string.
        """
        frame = inspect.stack()[1]
        caller_file = Path(frame.filename).resolve().parent
        return caller_file.as_posix()

    @staticmethod
    def base_dir() -> Path:
        """
        Return the base path of the application.
        - If running as a PyInstaller bundle, use the executable's directory.
        - Otherwise, use the project root (two levels up from this file).
        """
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent.resolve()
        return Path(__file__).parent.parent.parent.resolve()

    @staticmethod
    def get_data_dir() -> Path:
        """
        Return the path to the data directory, creating it if it doesn't exist.
        - In a PyInstaller bundle: uses 'data'
        - In normal Python: uses 'infrastructure/database/dev'
        """
        if getattr(sys, "frozen", False):
            data_path = Env.base_dir().joinpath("data").resolve()
        else:
            data_path = Env.base_dir().joinpath("infrastructure", "database", "dev").resolve()

        data_path.mkdir(parents=True, exist_ok=True)
        return data_path

    @staticmethod
    def get_window() -> dict:
        system = platform.system()
        info = {"os": system}

        try:
            if system == "Windows":
                user32 = ctypes.windll.user32
                info["screen_width"] = user32.GetSystemMetrics(0)
                info["screen_height"] = user32.GetSystemMetrics(1)

            elif system == "Linux":
                # use xrandr to get current resolution
                output = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True)
                width, height = map(int, output.decode().strip().split("x"))
                info["screen_width"] = width
                info["screen_height"] = height

            elif system == "Darwin":  # macOS
                output = subprocess.check_output(
                    "system_profiler SPDisplaysDataType | grep Resolution", shell=True
                ).decode().strip()
                # Example: "Resolution: 2560 x 1600 Retina"
                parts = [int(p) for p in output.split() if p.isdigit()]
                if len(parts) >= 2:
                    info["screen_width"], info["screen_height"] = parts[0], parts[1]

        except Exception as e:
            info["error"] = str(e)

        return info