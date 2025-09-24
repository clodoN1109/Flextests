import json
import urllib.request
import subprocess
import sys
import shutil
import os
from typing import Any, Callable, TypeVar, List

T = TypeVar("T")


class JsonFetcher:
    def __init__(self, max_depth: int | None = None):
        """
        :param max_depth: Maximum nesting depth to parse. None means no limit.
        """
        self.max_depth = max_depth

    # ---------------- public API ----------------

    def fetch(self, source: str) -> Any:
        """Fetch JSON from a URL, local file, or script and return a parsed object."""
        raw_text = self._load_source(source)
        return self.parse_json(raw_text)

    def fetch_as(self, source: str, factory: Callable[[dict], T]) -> List[T]:
        """
        Fetch JSON and map it into a list of objects using a factory function.
        The factory must accept a dict and return an instance of T.
        """
        raw = self.fetch(source)
        if not isinstance(raw, list):
            raise ValueError("Expected JSON root to be a list for fetch_as()")
        return [factory(item) for item in raw]

    def build_cmd(self, script_path: str) -> list[str]:
        """Return the command line (list) used to run the script identified by path."""
        ext = os.path.splitext(script_path)[1].lower()

        interpreters = {
            ".py": [shutil.which("python") or shutil.which("python3") or sys.executable],
            ".ps1": ["pwsh", "-ExecutionPolicy", "Bypass", "-File"],
            ".sh": ["bash"],
            ".bat": None,   # run directly
            ".rb": ["ruby"],
        }

        if ext not in interpreters:
            raise RuntimeError(f"Unsupported script type: {ext}")

        cmd = interpreters[ext]
        if cmd is None:
            return [script_path]
        # ensure interpreter exists
        if shutil.which(cmd[0]) is None:
            raise RuntimeError(f"Interpreter not found: {cmd[0]}")
        return cmd + [script_path]

    def spawn_process(self, script_path: str, capture_output: bool = True) -> subprocess.Popen:
        """
        Spawn the process (non-blocking) and return a Popen instance.
        Caller is responsible for .communicate() and checking returncode.
        """
        cmdline = self.build_cmd(script_path)
        return subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
        )

    def parse_json(self, text: str) -> Any:
        """Parse JSON text and apply depth limiting."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e
        return self._limit_depth(data, self.max_depth)

    # ---------------- internal helpers ----------------

    def _load_source(self, source: str) -> str:
        """Load text content from URL, file, or script (script executed)."""
        if self._is_url(source):
            with urllib.request.urlopen(source) as response:
                return response.read().decode("utf-8")

        if self._is_script(source):
            # run script and capture stdout (blocking)
            return self._run_script_blocking(source)

        # default: local file
        with open(source, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _is_url(source: str) -> bool:
        return source.startswith("http://") or source.startswith("https://")

    @staticmethod
    def _is_script(source: str) -> bool:
        ext = os.path.splitext(source)[1].lower()
        return ext in (".py", ".ps1", ".sh", ".bat", ".rb")

    def _run_script_blocking(self, script_path: str) -> str:
        """Run a script (blocking) and return its stdout (used by fetch())."""
        cmdline = self.build_cmd(script_path)

        proc = subprocess.run(
            cmdline,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if proc.returncode != 0:
            raise RuntimeError(f"Script failed with exit code {proc.returncode}:\n{proc.stderr}")

        return proc.stdout.strip()

    def _limit_depth(self, data: Any, max_depth: int | None, current_depth: int = 0) -> Any:
        """Recursively trim data structure to max_depth if provided."""
        if max_depth is None:
            return data
        if current_depth >= max_depth:
            return None
        if isinstance(data, dict):
            return {k: self._limit_depth(v, max_depth, current_depth + 1) for k, v in data.items()}
        if isinstance(data, list):
            return [self._limit_depth(v, max_depth, current_depth + 1) for v in data]
        return data
